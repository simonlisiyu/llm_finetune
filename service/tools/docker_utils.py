# import subprocess
# import threading
from datetime import datetime
import docker
from service.tools.file_utils import write_csv_file
from service.settings import Settings

client = docker.from_env()
my_settings = Settings()
docker_info_split = ",,"

'''
Docker SDK way
'''


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



def llm_docker_start(model_name, parent_dir, model_dir, gpus, ip, port, additional_args):
    environment = {
        "NVIDIA_DRIVER_CAPABILITIES": "compute,utility",
        "NVIDIA_VISIBLE_DEVICES": "all"
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
    command = f"poetry run python3 -m localai.worker " \
              f"--model-path /LLMs/{model_dir} " \
              f"--controller http://{ip}:23620 " \
              f"--worker http://{ip}:{port} " \
              f"--model-names {model_name} " \
              f"--gpus {gpus} " \
              f"--limit-model-concurrency 1 {additional_args}"

    start_df = datetime.now().strftime(my_settings.datatime_sft)
    print("=====>>>>> 大语言模型docker开始执行:", command)
    container = client.containers.run(
        "docker.li.com/dmc/localai",
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
