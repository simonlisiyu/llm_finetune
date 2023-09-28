
class FinetuneLog:
    def __init__(self, task, start, end, base, train, epoch, log):
        self.task = task
        self.start = start
        self.end = end
        self.base = base
        self.train = train
        self.epoch = epoch
        self.log = log


class MergeLog:
    def __init__(self, task, start, end, base, out, log):
        self.task = task
        self.start = start
        self.end = end
        self.base = base
        self.out = out
        self.log = log

def capture_output(process, log_file):
    for line in process.stdout:
        log_file.write(line)
        print(line)
        log_file.flush()  # 刷新缓冲区，确保实时写入日志文件
