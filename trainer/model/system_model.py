

class HostInfo:
    def __init__(self, hostname, ip, port, tag):
        self.hostname = hostname
        self.ip = ip
        self.port = port
        self.tag = tag
        self.status = 'up'


class GPUInfo:
    def __init__(self, index, name, utilization, memory_used, memory_total):
        self.index = index
        self.name = name
        self.utilization = utilization
        self.memory_used = memory_used
        self.memory_total = memory_total


class CPUInfo:
    def __init__(self, index, freq, utilization):
        self.index = index
        self.freq = freq
        self.utilization = utilization


class MemInfo:
    def __init__(self, total, available, percent):
        self.total = total
        self.available = available
        self.percent = percent


class DiskInfo:
    def __init__(self, index, mount, total, available, percent):
        self.index = index
        self.mount = mount
        self.total = total
        self.available = available
        self.percent = percent


class GPUProcessInfo:
    def __init__(self, name, usage):
        self.name = name
        self.usage = usage
