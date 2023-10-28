import subprocess
import psutil
from ..model import GPUInfo, CPUInfo, MemInfo, DiskInfo


def get_gpu_info() -> [GPUInfo]:
    # gpu
    output = subprocess.check_output(["nvidia-smi", "--query-gpu=index,name,utilization.gpu,memory.used,memory.total",
                                      "--format=csv,noheader,nounits"])
    # tpu todo
    # xpu todo

    gpu_split = output.decode("utf-8").strip().split("\n")
    gpu_info_split = [info.split(", ") for info in gpu_split]
    gpu_info = [GPUInfo(*info) for info in gpu_info_split]
    return gpu_info


def get_cpu_info() -> [CPUInfo]:
    cpu_freq = str(psutil.cpu_freq().current) + "MHz"
    cpu_percents = psutil.cpu_percent(interval=1, percpu=True)
    cpus = [[i, cpu_freq, percent] for i, percent in enumerate(cpu_percents)]
    cpu_info = [CPUInfo(*info) for info in cpus]
    return cpu_info


def get_mem_info() -> [MemInfo]:
    mem = psutil.virtual_memory()
    total_mem = round(mem.total / (1024 ** 2), 2)  # 转换为GB并保留两位小数
    available_mem = round(mem.available / (1024 ** 2), 2)
    mem_percent = mem.percent
    mem_info = [MemInfo(total_mem, available_mem, mem_percent)]
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
    return disk_info

