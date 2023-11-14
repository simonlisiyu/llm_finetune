# __author__ "lisiyu"
# date 2023/10/25
import copy
import json
from datetime import datetime
from ...service.tools.file_utils import append_to_json
from ...settings import Settings

my_settings = Settings()


def choose_default_or_request_params(key: str, default_info: dict, req_info: dict) :
    return default_info[key] if key not in req_info or req_info[key] == "" or req_info[key] is None else req_info[key]


def get_job_info(req_info: dict) -> dict:
    job_info = copy.deepcopy(my_settings.task_params['job_general'])
    job_info['start_time'] = datetime.now().strftime(my_settings.datatime_sft) \
        if "start_time" not in req_info or req_info['start_time'] == "" or req_info['start_time'] is None \
        else req_info['start_time']
    job_info['task_id'] = choose_default_or_request_params('task_id', job_info, req_info)
    job_info['train_data'] = choose_default_or_request_params('train_data', job_info, req_info)
    job_info['eval_data'] = choose_default_or_request_params('eval_data', job_info, req_info)
    job_info['eval_task'] = choose_default_or_request_params('eval_task', job_info, req_info)
    job_info['checkpoint_path'] = my_settings.base_dir + choose_default_or_request_params('checkpoint_path', job_info, req_info)
    job_info['output_path'] = my_settings.base_dir + choose_default_or_request_params('output_path', job_info, req_info)
    job_info['eval_path'] = my_settings.base_dir + choose_default_or_request_params('eval_path', job_info, req_info) + job_info['task_id']
    job_info['log_path'] = my_settings.base_dir + choose_default_or_request_params('log_path', job_info, req_info)
    job_info['gpus'] = choose_default_or_request_params('gpus', job_info, req_info)
    job_info['nnodes'] = choose_default_or_request_params('nnodes', job_info, req_info)
    job_info['nproc_per_node'] = str(len(choose_default_or_request_params('gpus', job_info, req_info).split(",")))
    # job_info['nproc_per_node'] = choose_default_or_request_params('nproc_per_node', job_info, req_info)
    job_info['master_addr'] = choose_default_or_request_params('master_addr', job_info, req_info)
    job_info['master_port'] = str(choose_default_or_request_params('master_port', job_info, req_info))
    return job_info


def get_hparams(req_info) -> dict:
    hparams = copy.deepcopy(my_settings.task_params['hparams_general'])
    hparams['epochs'] = choose_default_or_request_params('epochs', hparams, req_info)
    hparams['lr'] = choose_default_or_request_params('lr', hparams, req_info)
    hparams['per_device_train_batch_size'] = choose_default_or_request_params('per_device_train_batch_size', hparams, req_info)
    hparams['per_device_eval_batch_size'] = choose_default_or_request_params('per_device_eval_batch_size', hparams, req_info)
    hparams['gradient_accumulation_steps'] = choose_default_or_request_params('gradient_accumulation_steps', hparams, req_info)
    hparams['lr_scheduler_type'] = choose_default_or_request_params('lr_scheduler_type', hparams, req_info)
    hparams['quantization_bit'] = choose_default_or_request_params('quantization_bit', hparams, req_info)
    hparams['max_source_length'] = choose_default_or_request_params('max_source_length', hparams, req_info)
    hparams['max_target_length'] = choose_default_or_request_params('max_target_length', hparams, req_info)
    hparams['max_samples'] = choose_default_or_request_params('max_samples', hparams, req_info)
    hparams['logging_steps'] = choose_default_or_request_params('logging_steps', hparams, req_info)
    hparams['save_steps'] = choose_default_or_request_params('save_steps', hparams, req_info)
    return hparams


def get_model_info(req_info: dict) -> dict:
    json_file = my_settings.base_dir + my_settings.model_file
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    model_name = req_info['model_name']
    inner_model_path = choose_default_or_request_params('model_path', json_data[model_name], req_info)
    full_model_path = my_settings.base_dir + inner_model_path
    model_template = choose_default_or_request_params('template', json_data[model_name], req_info)
    size = choose_default_or_request_params('size', json_data[model_name], req_info)
    finetuning_type = choose_default_or_request_params('finetuning_type', my_settings.task_params[model_template], req_info)
    lora_target = choose_default_or_request_params('lora_target', my_settings.task_params[model_template], req_info)

    return {"model_name": model_name,
            "model_path": full_model_path,
            "model_template": model_template,
            "finetuning_type": finetuning_type,
            "lora_target": lora_target,
            "size": size}


# 追加数据到LLM JSON文件
def append_model_info_by_merge_task(model_dir: str, new_model_name: str, model_info: dict):
    json_file = my_settings.base_dir + my_settings.model_file
    new_data = {new_model_name:
                    {
                        'model_path': model_dir + new_model_name,
                        'template': model_info['model_template'],
                        'size': model_info['size'],
                        'update_at': datetime.now().strftime(my_settings.datatime_sft)
                     }
                }
    append_to_json(json_file, new_data)
