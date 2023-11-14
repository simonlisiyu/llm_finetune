import subprocess
import psutil
from ..model import GPUInfo, CPUInfo, MemInfo, DiskInfo, HostInfo, GPUProcessInfo
from ..service.tools.docker_utils import get_docker_nv_processes
from ..service.tools.system_utils import get_system_nv_processes
from ..settings import Settings

my_settings = Settings()


def get_process_info() -> GPUProcessInfo:
    process_list = []
    if my_settings.has_docker:
        process_list = get_docker_nv_processes(process_list)
    return get_system_nv_processes(process_list)


def get_host_info() -> HostInfo:
    hostname = subprocess.check_output('hostname', shell=True)
    host_inf = HostInfo(
        hostname.decode().rstrip('\n'),
        my_settings.app_ip,
        my_settings.app_port,
        my_settings.app_tag)
    print("host_inf: ", host_inf)
    return host_inf


def get_gpu_info() -> [GPUInfo]:
    # gpu
    output = subprocess.check_output(["nvidia-smi", "--query-gpu=index,name,utilization.gpu,memory.used,memory.total",
                                      "--format=csv,noheader,nounits"])
    # tpu todo
    # xpu todo

    gpu_split = output.decode("utf-8").strip().split("\n")
    gpu_info_split = [info.split(", ") for info in gpu_split]
    gpu_info = [GPUInfo(*info) for info in gpu_info_split]
    print("gpu_info: ", gpu_info)
    return gpu_info


def get_cpu_info() -> [CPUInfo]:
    cpu_freq = str(psutil.cpu_freq().current) + "MHz"
    cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
    cpus = [[i, cpu_freq, percent] for i, percent in enumerate(cpu_percents)]
    cpu_info = [CPUInfo(*info) for info in cpus]
    print("cpu_info: ", cpu_info)
    return cpu_info


def get_mem_info() -> [MemInfo]:
    mem = psutil.virtual_memory()
    total_mem = round(mem.total / (1024 ** 2), 2)  # 转换为GB并保留两位小数
    available_mem = round(mem.available / (1024 ** 2), 2)
    mem_percent = mem.percent
    mem_info = [MemInfo(total_mem, available_mem, mem_percent)]
    print("mem_info: ", mem_info)
    return mem_info


def get_disk_info() -> [DiskInfo]:
    partitions = psutil.disk_partitions()
    disk_usage = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        disk_usage.append((partition.mountpoint,
                           round(usage.total / (1024 ** 2), 2),
                           round(usage.free / (1024 ** 2), 2),
                           usage.percent))
    disk_usage = sorted(disk_usage, key=lambda x: x[3], reverse=True)
    disk_info = [DiskInfo(i, *info) for i, info in enumerate(disk_usage)]
    print("disk_info: ", disk_info)
    return disk_info


def task_kill(task_id: str):
    process_pattern = task_id
    pgrep_cmd = ["pgrep", "-f", process_pattern]
    pgrep_output = subprocess.check_output(pgrep_cmd)
    process_ids = pgrep_output.decode().split()

    for pid in process_ids:
        kill_cmd = ["kill", pid]
        subprocess.run(kill_cmd)
        print(f"进程 {pid} 已终止")

