import yaml


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Settings(metaclass=Singleton):
    def __init__(self):
        with open("src/llmtuner/trainer.yaml", "r") as file:
            yaml_conf = yaml.safe_load(file)

            # redis
            self.redis_ip = "127.0.0.1"
            self.redis_port = 6379
            self.redis_db = 0
            self.redis_password = ""

            # trainer
            self.dataset_info_path = yaml_conf["trainer"]["base_dir"] + "data/"

        # 常量
        self.ALL_TASK_METRIC_MQ = 'TRAINER:TASK:TRAIN:METRIC'
        self.TRAIN_TASK_RESULT_KEY = 'TRAINER:TASK:TRAIN:RESULT'
        self.EVAL_TASK_RESULT_KEY = 'TRAINER:TASK:EVAL:RESULT'




