import subprocess
import psutil
from ...model import GPUProcessInfo
from ...settings import Settings

my_settings = Settings()


def get_system_nv_processes(process_list: list):
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
        process_list.append(GPUProcessInfo("process: " + process[0], gpu_uuid_map[process[1]] + "卡: " + process[2] + "MiB：" + process[3]))
    print("gpu_process_map: ", gpu_process_map)

    return process_list

