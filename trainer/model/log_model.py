
class FinetuneLog:
    def __init__(self, task, job_info, model_info, hparams, log):
        self.task = task
        self.job_info = job_info
        self.model_info = model_info
        self.hparams = hparams
        self.log = log


class MergeLog:
    def __init__(self, task, start, base, out, log):
        self.task = task
        self.start = start
        self.base = base
        self.out = out
        self.log = log
