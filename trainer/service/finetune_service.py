import subprocess
import threading
import json
from datetime import datetime
from ..model import FinetuneLog
from .tools.params_utils import get_job_info, get_hparams, get_model_info
from .tools.redis_utils import RedisSingleton
from ..service.tools.log_utils import capture_output
from ..service.tools.file_utils import write_csv_file, read_csv_file
from ..settings import Settings

my_settings = Settings()
# Redis Client
redis_instance = RedisSingleton(host=my_settings.redis_ip,
                                port=my_settings.redis_port,
                                db=my_settings.redis_db,
                                password=my_settings.redis_password)
r = redis_instance.get_redis()


def get_task_log(task: str) -> [FinetuneLog]:
    try:
        data = read_csv_file(task)
    except Exception as e:
        data = []
    finetune_info = [FinetuneLog(*info) for info in data]
    return finetune_info


def get_dataset_names() -> [str]:
    json_file = my_settings.base_dir + my_settings.data_file
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    dataset_keys = json_data.keys()
    return dataset_keys


def get_models_names() -> [str]:
    json_file = my_settings.base_dir + my_settings.model_file
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    dataset_keys = json_data.keys()
    return dataset_keys


def offline_finetune_task_run(job_info: dict, hparams: dict, model_info: dict):
    finetune_script = my_settings.task_params['script']['sft_script']
    print("offline_finetune_task_run job_info: ", job_info)
    job_info = get_job_info(job_info)
    print("offline_finetune_task_run job_info: ", job_info)
    hparams = get_hparams(hparams)
    model_info = get_model_info(model_info)
    script_args = [model_info['model_path'],
                   job_info['train_data'],
                   hparams['epochs'],
                   job_info['checkpoint_path'],
                   job_info['nnodes'],
                   job_info['nproc_per_node'],
                   job_info['master_addr'],
                   job_info['master_port'],
                   job_info['gpus'],
                   hparams['lr'],
                   hparams['per_device_train_batch_size'],
                   hparams['gradient_accumulation_steps'],
                   hparams['lr_scheduler_type'],
                   hparams['quantization_bit'],
                   hparams['max_source_length'],
                   hparams['max_target_length'],
                   hparams['max_samples'],
                   job_info['task_id'],
                   model_info['model_template'],
                   model_info['finetuning_type'],
                   model_info['lora_target'],
                   hparams['logging_steps'],
                   hparams['save_steps'],
                   ]
    print("script_args, ", script_args)
    command = [finetune_script] + script_args
    print("command, ", command)
    log_file_name = "_train.log"
    log_file_path = job_info['log_path'] + job_info['task_id'] + log_file_name
    print("=====>>>>> 离线任务开始执行:", command, job_info['start_time'])
    short_log_path = log_file_path.replace(my_settings.base_dir, "")
    write_csv_file("offline_finetune_task", job_info, model_info, hparams, short_log_path)
    with open(log_file_path, 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        print("processid: ", process.pid)
        my_settings.process[job_info['task_id']] = process.pid
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()

    end_df = datetime.now().strftime(my_settings.datatime_sft)
    metric_json = dict()
    metric_json["task_id"] = job_info['task_id']
    metric_json["train_action"] = 0
    print("process: ", process)
    if process.returncode == 0:
        metric_json["status"] = 2
        try:
            r.xadd('ALITA:TASK:TRAIN:METRIC', {job_info['task_id']: json.dumps(metric_json)})
            print("success xadd to ALITA:TASK:TRAIN:METRIC,", metric_json)
        except Exception as e:
            print("failed xadd to ALITA:TASK:TRAIN:METRIC,", e)
        print("===== 离线任务执行成功: ", command, end_df)
    else:
        metric_json["status"] = 4
        try:
            r.xadd('ALITA:TASK:TRAIN:METRIC', {job_info['task_id']: json.dumps(metric_json)})
            print("success xadd to ALITA:TASK:TRAIN:METRIC,", metric_json)
        except Exception as e:
            print("failed xadd to ALITA:TASK:TRAIN:METRIC,", e)
        print("===== 离线任务执行失败: ", command, end_df)
    return process.returncode


def offline_finetune_task(model_name: str, train_data: str, checkpoint_path: str, hparams: dict, gpus: str):
    return offline_finetune_task_run(
        {"task_id": "finetune_task_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
         "train_data": train_data, "checkpoint_path": checkpoint_path, "gpus": gpus},
        hparams,
        {"model_name": model_name}
    )


def copy_file_to_directory(valid_data_file):
    script_args = [valid_data_file, my_settings.base_data_path, valid_data_file.split(".")[0]]
    command = [my_settings.task_params['script']['copy_file_script']] + script_args
    print("=====>>>>> 将文件拷贝到指定路径:", command)
    with open("logs/copy_data_file" + ".log", 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()
    return valid_data_file.split(".")[0]


def get_file_name(data_file_path):
    file_name = data_file_path.split('/')[-1].split('.')[0]
    return file_name


