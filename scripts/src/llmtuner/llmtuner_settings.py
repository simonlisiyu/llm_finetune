import yaml


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Settings(metaclass=Singleton):
    def __init__(self):
        with open("src/llmtuner/llmtuner.yaml", "r") as file:
            yaml_conf = yaml.safe_load(file)

            # redis
            self.redis_ip = yaml_conf["redis"]["ip"]
            self.redis_port = yaml_conf["redis"]["port"]
            self.redis_password = yaml_conf["redis"]["password"]

            # trainer
            self.dataset_info_path = yaml_conf["trainer"]["dataset_info_path"]

        # 常量
        self.ALL_TASK_METRIC_MQ = 'ALITA:TASK:TRAIN:METRIC'
        self.TRAIN_TASK_RESULT_KEY = 'ALITA:TASK:TRAIN:RESULT'
        self.EVAL_TASK_RESULT_KEY = 'ALITA:TASK:EVAL:RESULT'




