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
            self.worker_model_path = yaml_conf["trainer"]["base_dir"] + "llm/"

            # trainer
            self.train_ports = [9901, 9902, 9903, 9904, 9905, 9906, 9907, 9908, 9909, 9910]

            self.base_dir = yaml_conf["trainer"]["base_dir"]
            self.data_dir = 'data/'
            self.model_dir = 'llm/'
            self.log_dir = 'logs/'
            self.dev_script_dir = 'scripts/dev/'

            self.data_file = "data/dataset_info.json"
            self.model_file = "config/model_info.json"

            self.base_data_path = self.base_dir + self.data_dir
            self.base_model_path = self.base_dir + self.model_dir

            # redis
            self.redis_ip = '127.0.0.1'
            self.redis_port = 6379
            self.redis_password = ""

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
                'ceval_script': 'scripts/run_ceval_params.sh',
                'logging_steps': '10',
                'save_steps': '1000',
            },
            'job_general': {
                'task_id': "task_" + datetime.now().strftime(self.datatime_sft),
                'train_data': "self_cognition",
                'eval_data': "self_cognition",
                'eval_task': "ceval",
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
            'eval_general': {
                'eval_task_type': ['bleu&rouge', 'ceval', 'mmlu', 'cmmlu'],
                'ceval': 'validation',
                'mmlu': 'validation',
                'cmmlu': 'test',
                'lang': "zh",
                'n_shot': "5",
                'batch_size': "4",
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
            },
            'qwen': {
                'template': 'qwen',
                'finetuning_type': 'lora',
                'lora_target': 'c_attn',
            },
            'mistral': {
                'template': 'mistral',
                'finetuning_type': 'lora',
                'lora_target': 'q_proj,v_proj',
            },
            'xverse': {
                'template': 'xverse',
                'finetuning_type': 'lora',
                'lora_target': 'q_proj,v_proj',
            },
            'intern': {
                'template': 'intern',
                'finetuning_type': 'lora',
                'lora_target': 'q_proj,v_proj',
            }
        }
        self.hyper_params_desc = [
            {
                "name": "epochs",
                "title": "训练轮次",
                "type": "str", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "1",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    1, 1000
                ],
                "help": "控制训练过程中迭代轮数",
            },
            {
                "name": "per_device_train_batch_size",
                "title": "批处理大小",
                "type": "str", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "1",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    1, 32
                ],
                "help": "在每次训练迭代中使用的样本数",
            },
            {
                "name": "lr",
                "title": "学习率",
                "type": "str", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "0.00002",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    0, 1
                ],
                "help": "AdamW优化器的初始学习率",
            },
            {
                "name": "max_source_length",
                "title": "输入序列最大长度",
                "type": "number", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "512",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    8, 32768
                ],
                "help": "输入序列分词后的最大token长度",
            },
            {
                "name": "max_target_length",
                "title": "输出序列最大长度",
                "type": "number", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "512",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    8, 32768
                ],
                "help": "输出序列分词后的最大token长度",
            },
            {
                "name": "gradient_accumulation_steps",
                "title": "梯度累积",
                "type": "str", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "1",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    1, 32
                ],
                "help": "梯度累积的步数",
            }
        ]
        self.additional_params_desc = [
            {
                "name": "lr_scheduler_type",
                "title": "学习率调度策略",
                "type": "str", #str/number/list/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "cosine",
                "choices_type": "list", #range数值范围/list列表
                "choices": [
                    "cosine", "linear", "polynomial", "constant", "constant_with_warmup",
                    "cosine_with_restarts", "inverse_sqrt", "reduce_lr_on_plateau"
                ],
                "help": "选择学习率调度策略的算法",
            },
            {
                "name": "quantization_bit",
                "title": "量化微调",
                "type": "str", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "",
                "choices_type": "list", #range数值范围/list列表
                "choices": [
                    "4", "8"
                ],
                "help": "启用量化微调的比特大小",
            },
            {
                "name": "max_samples",
                "title": "样本数",
                "type": "number", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "512",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    0, 2048
                ],
                "help": "训练最大样本数",
            },
            {
                "name": "logging_steps",
                "title": "日志metric输出步数",
                "type": "number", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "5",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    5, 1000
                ],
                "help": "经过步数后打印metric",
            },
            {
                "name": "save_steps",
                "title": "检查点保存步数",
                "type": "number", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "10",
                "choices_type": "range", #range数值范围/list列表
                "choices": [
                    10, 10000
                ],
                "help": "经过步数后保存checkpoint检查点",
            },
            {
                "name": "precision",
                "title": "模型精度",
                "type": "str", #str/number/bool
                "method": ["all"], #all/full/lora
                "action": ["all"], #train/merge/eval
                "stage": ["all"], #pt/sft/rm/ppo/dpo
                "required": True,
                "default": "1",
                "choices_type": "list", #range数值范围/list列表
                "choices": [
                    "fp16", "bf16"
                ],
                "help": "模型保存的精度粒度",
            }
        ]


