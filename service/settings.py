import yaml


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Settings(metaclass=Singleton):
    def __init__(self):
        # with open("../config/env.yaml", "r") as file:
        with open("config/env.yaml", "r") as file:
            yaml_conf = yaml.safe_load(file)
            self.app_ip = yaml_conf["application"]["ip"]
            self.localai_url = yaml_conf["localai"]["url"]
            self.models = yaml_conf["models"]
            self.script = yaml_conf["script"]
            self.file_copy_script = "scripts/file_copy.sh"
            self.finetune_script = "scripts/run_sft_params_llama.sh"
            self.merge_script = "scripts/run_merge_glm2.sh"
            self.docker_script = "scripts/run_localai_docker.sh"
            self.logs_path = "logs/"
            self.data_path = "data/"
            self.merge_log_prefix = "merge"
            self.finetune_log_prefix = "finetune"
            self.datatime_sft = '%Y-%m-%d_%H:%M:%S'
            self.base_data_dir = yaml_conf['dir']['base_data_dir']
            self.base_model_dir = yaml_conf['dir']['base_model_dir']
            self.dev_script_dir = yaml_conf['dir']['dev_script_dir']
            self.host_model_dir = yaml_conf['dir']['host_model_dir']


# obj1 = Settings()
# obj2 = Settings()
#
# print(obj1.localai_url)  # 输出 1
# print(obj1 is obj2)  # 输出 True


