import subprocess
import psutil
import json
# import threading
from datetime import datetime
import docker
from ...service.tools.file_utils import write_csv_file
from ...model import GPUProcessInfo
from ...settings import Settings

client = docker.from_env()
my_settings = Settings()
docker_info_split = ",,"
psutil.PROCFS_PATH = my_settings.procfs_path

'''
Docker SDK way
'''


class DockerPidInfo:
    def __init__(self, name, pid):
        self.name = name
        self.pid = pid


class DockerInfo:
    def __init__(self, name, created_at, status, ports, image, container_id):
        self.name = name
        self.created_at = created_at
        self.status = status
        self.ports = ports
        self.image = image
        self.container_id = container_id


def show_docker_containers():
    container_info = []
    try:
        for container in client.containers.list(all=True):
            name = container.name
            created_at = container.attrs['Created']
            status = container.status
            ports = container.attrs['HostConfig']['PortBindings']
            image = container.attrs['Config']['Image']
            container_id = container.short_id

            container_info.append(docker_info_split.join([name, created_at, status, str(ports), image, container_id]))
    except Exception as e:
        container_info = []
    return container_info


def start_docker_container_by_id(container_id):
    try:
        container = client.containers.get(container_id)
        container.start()
        return {"message": f"Container {container_id} started successfully"}
    except docker.errors.NotFound:
        return {"error": f"Container {container_id} not found"}


def show_container_logs_by_id(container_id):
    try:
        container = client.containers.get(container_id)
        logs = container.logs().decode('utf-8')
        return logs
    except docker.errors.NotFound:
        return {"error": f"Container {container_id} not found"}


def stop_docker_container_by_id(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {"message": f"Container {container_id} stopped successfully"}
    except docker.errors.NotFound:
        return {"error": f"Container {container_id} not found"}


def delete_docker_container_by_id(container_id):
    try:
        container = client.containers.get(container_id)
        container
        return {"message": f"Container {container_id} deleted successfully"}
    except docker.errors.NotFound:
        return {"error": f"Container {container_id} not found"}


def llm_docker_start(model_name, parent_dir, model_dir, gpus, cip, cport, ip, port, additional_args):
    environment = {
        "NVIDIA_DRIVER_CAPABILITIES": "compute,utility",
        "NVIDIA_VISIBLE_DEVICES": gpus
    }
    volumes = {
        parent_dir: {
            "bind": "/LLMs",
            "mode": "rw"
        }
    }
    # links = {
    #     "localai": "localai"
    # }
    ports = {
        "23621/tcp": port
    }
    command = f"python3 -m alita.worker " \
              f"--model-path /LLMs/{model_dir} " \
              f"--controller http://{cip}:{cport} " \
              f"--worker http://{ip}:{port} " \
              f"--model-names {model_name} " \
              f"--gpus {gpus} " \
              f"--limit-model-concurrency 1 {additional_args}"

    start_df = datetime.now().strftime(my_settings.datatime_sft)
    print("=====>>>>> 大语言模型docker开始执行:", command)
    container = client.containers.run(
        "docker.art.haizhi.com/dmc/alita",
        detach=True,
        name=model_name,
        environment=environment,
        volumes=volumes,
        runtime="nvidia",
        # links=links,
        ports=ports,
        command=command
    )
    end_df = datetime.now().strftime(my_settings.datatime_sft)
    print(f"===== 大语言模型 {container.name} docker执行完成: ", command, end_df)
    write_csv_file("llm_docker_localai", start_df, end_df, model_name, parent_dir, model_dir, gpus, ip, port)


def get_docker_nv_processes(process_list: list):
    # get all gpu
    gpu_uuid_map = {}
    gpus = subprocess.check_output(["nvidia-smi", "--query-gpu=gpu_uuid,index",
                                    "--format=csv,noheader,nounits"])
    gpu_split = gpus.decode("utf-8").strip().split("\n")
    gpu_info_split = [info.split(", ") for info in gpu_split]
    for gpu in gpu_info_split:
        gpu_uuid_map[gpu[0]] = gpu[1]
    print("gpu_uuid_map: ", gpu_uuid_map)

    # get all gpu process
    gpu_process_map = {}
    gpu_processes = subprocess.check_output(["nvidia-smi", "--query-compute-apps=pid,gpu_uuid,used_memory,name",
                                             "--format=csv,noheader,nounits"])
    gpu_processes_split = gpu_processes.decode("utf-8").strip().split("\n")
    gpu_process_split = [info.split(", ") for info in gpu_processes_split]
    for process in gpu_process_split:
        gpu_process_map[process[0]] = gpu_uuid_map[process[1]] + "卡: " + process[2] + "MiB：" + process[3]
    print("gpu_process_map: ", gpu_process_map)

    # get all gpu process's parent process
    old_map = dict(gpu_process_map)
    for pid in old_map.keys():  # 遍历所有的PID
        ppid = psutil.Process(int(pid)).ppid()  # 获取父进程的PID
        gpu_process_map[str(ppid)] = gpu_process_map[pid]  # 将父进程的GPU映射到子进程
    print("gpu_process_map: ", gpu_process_map)

    # 存储PID到容器ID的映射
    try:
        for container in get_docker_map():
            name = container.name
            docker_pid = container.pid
            print("docker_pid: ", docker_pid, name)
            if docker_pid in gpu_process_map:
                print(f"{docker_pid} 在 gpu_process_map 中")
                process_list.append(GPUProcessInfo("docker: " + name, gpu_process_map[docker_pid]))
    except Exception as e:
        print("err: ", e)

    return process_list


def get_docker_map():
    container_list = client.containers.list()
    pid_list = []
    for container in container_list:
        container_id = container.id
        container_info = client.api.inspect_container(container_id)
        container_name = container_info["Name"].lstrip('/')
        container_pid = container_info["State"]["Pid"]
        pid_list.append(DockerPidInfo(container_name, str(container_pid)))

    return pid_list
# def get_docker_map():
#     ps_output = subprocess.check_output(['docker', 'ps', '-q']).decode().strip()
#     container_ids = ps_output.split()
#
#     pid_list = []
#     for container_id in container_ids:
#         inspect_output = subprocess.check_output(['docker', 'inspect', container_id]).decode().strip()
#         inspect_json = json.loads(inspect_output)
#         container_name = inspect_json[0]["Name"].lstrip('/')
#         container_pid = inspect_json[0]["State"]["Pid"]
#         pid_list.append(DockerPidInfo(container_name, str(container_pid)))
#
#     return pid_list


'''
subprocess way
'''
# def llm_docker_start(model_name, model_dir, gpus, port):
#     script_args = [model_name, model_dir, gpus, port]
#     command = [docker_script] + script_args
#     start_df = datetime.now().strftime(datatime_sft)
#     log_file_path = logs_path + model_name + "_" + finetune_log_prefix + "_" + start_df
#     print("=====>>>>> 大语言模型docker开始执行:", command)
#     with open(log_file_path + ".log", 'a') as log_file:
#         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
#         output_thread = threading.Thread(target=capture_output, args=(process, log_file))
#         output_thread.start()
#         process.wait()
#         output_thread.join()
#
#     end_df = datetime.now().strftime(datatime_sft)
#     print("===== 大语言模型docker执行完成: ", command, end_df)
#     write_csv_file("llm_docker_localai", start_df, end_df, model_name, model_dir, gpus, port, log_file_path)
