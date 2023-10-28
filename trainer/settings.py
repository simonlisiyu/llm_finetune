import yaml
from datetime import datetime


class Singleton(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__call__(*args, **kwargs)
        return cls.instances[cls]


class Settings(metaclass=Singleton):
    def __init__(self):
        with open("config/trainer.yaml", "r") as file:
            yaml_conf = yaml.safe_load(file)

            # application
            self.app_ip = yaml_conf["application"]["ip"]
            self.app_port = yaml_conf["application"]["port"]
            self.app_log_level = yaml_conf["application"]["log_level"]

            # controller
            self.controller_ip = yaml_conf["controller"]["ip"]
            self.controller_port = yaml_conf["controller"]["port"]
            self.controller_url = "http://" + self.controller_ip  + ":" + str(self.controller_port)
            self.chat_url = self.controller_url + "/chat"

            # worker
            self.worker_model_path = yaml_conf["worker"]["model_dir"]

            # trainer
            self.train_ports = yaml_conf["trainer"]["ports"]

            self.base_dir = yaml_conf["trainer"]["base_dir"]
            self.data_dir = yaml_conf["trainer"]["data_dir"]
            self.model_dir = yaml_conf["trainer"]["model_dir"]
            self.log_dir = yaml_conf["trainer"]["log_dir"]
            self.dev_script_dir = yaml_conf["trainer"]["dev_script_dir"]

            self.data_file = yaml_conf["trainer"]["data_file"]
            self.model_file = yaml_conf["trainer"]["model_file"]

            self.base_data_path = self.base_dir + self.data_dir
            self.base_model_path = self.base_dir + self.model_dir

            # redis
            self.redis_ip = yaml_conf["redis"]["ip"]
            self.redis_port = yaml_conf["redis"]["port"]
            self.redis_password = yaml_conf["redis"]["password"]

        # 常量
        self.datatime_sft = '%Y-%m-%d_%H:%M:%S'
        self.ALL_TASK_METRIC_MQ = 'ALITA:TASK:TRAIN:METRIC'
        self.TRAIN_TASK_RESULT_KEY = 'ALITA:TASK:TRAIN:RESULT'
        self.EVAL_TASK_RESULT_KEY = 'ALITA:TASK:EVAL:RESULT'
        self.task_params = {
            'script': {
                'copy_file_script': 'scripts/file_copy.sh',
                'sft_script': 'scripts/run_sft_params.sh',
                'merge_script': 'scripts/run_merge_params.sh',
                'eval_script': 'scripts/run_eval_params.sh',
                'logging_steps': '10',
                'save_steps': '1000',
            },
            'job_general': {
                'task_id': "task_" + datetime.now().strftime(self.datatime_sft),
                'train_data': "self_cognition",
                'eval_data': "self_cognition",
                'checkpoint_path': self.model_dir + "sft_checkpoint/",
                'output_path': self.model_dir + "merge_output/",
                'eval_path': self.model_dir + "eval_result/",
                'log_path': "logs/",
                'gpus': '0',
                'nnodes': '1',
                'nproc_per_node': '1',
                'master_addr': self.app_ip,
                'master_port': self.train_ports[datetime.now().minute % len(self.train_ports)],
            },
            'hparams_general': {
                'epochs': '10',
                'lr': '3e-4',
                'per_device_train_batch_size': '1',
                'per_device_eval_batch_size': '1',
                'gradient_accumulation_steps': '1',
                'lr_scheduler_type': 'cosine',
                'quantization_bit': '',
                'max_source_length': '512',
                'max_target_length': '512',
                'max_samples': '512',
                'logging_steps': '10',
                'save_steps': '1000',
            },
            'chatglm2': {
                'template': 'chatglm2',
                'finetuning_type': 'lora',
                'lora_target': 'query_key_value',
            },
            'llama': {
                'template': 'default',
                'finetuning_type': 'lora',
                'lora_target': 'q_proj,v_proj',
            },
            'llama2': {
                'template': 'llama2',
                'finetuning_type': 'lora',
                'lora_target': 'q_proj,v_proj',
            },
            'baichuan': {
                'template': 'baichuan',
                'finetuning_type': 'lora',
                'lora_target': 'W_pack',
            },
            'baichuan2': {
                'template': 'baichuan2',
                'finetuning_type': 'lora',
                'lora_target': 'W_pack',
            }
        }


