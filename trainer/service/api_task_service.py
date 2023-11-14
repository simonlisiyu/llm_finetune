from datetime import datetime
from .tools.params_utils import append_model_info_by_merge_task
from .finetune_service import offline_finetune_task_run, get_file_name
from .merge_service import offline_merge_task_run
from .eval_service import offline_eval_task_run
from .tools.file_utils import append_to_json
from ..settings import Settings

my_settings = Settings()


def total_task_run(task_id: str, template: str, model_path: str, data_path: str, eval_data: str,
                   checkpoint_path: str, output_path: str, log_path: str, gpus: str, finetuning_type: str,
                   hyper_parameters: dict):

    data_name = get_file_name(data_path)
    eval_name = get_file_name(eval_data)

    # 追加数据到dataset JSON文件
    data_json_file = my_settings.base_dir + my_settings.data_file
    new_data = {data_name:
                    {'file_name': my_settings.base_dir + data_path,
                     'data_count': 'unknown',
                     'upload_at': datetime.now().strftime(my_settings.datatime_sft)
                     }}
    print("new_data: ", new_data)
    append_to_json(data_json_file, new_data)
    new_data = {eval_name:
                    {'file_name': my_settings.base_dir + eval_data,
                     'data_count': 'unknown',
                     'upload_at': datetime.now().strftime(my_settings.datatime_sft)
                     }}
    print("new_data: ", new_data)
    append_to_json(data_json_file, new_data)

    # 追加模型到model_info JSON文件
    model_name = model_path.split('/')[-1]
    model_dir = model_path.split('/')[:-1]
    model_dir_str = '/'.join([str(s) for s in model_dir])
    model_info = {'model_name': model_name, 'model_path': model_path, 'model_template': template, 'finetuning_type': finetuning_type, 'size': '-1'}
    print("model_info: ", model_info)
    append_model_info_by_merge_task(model_dir_str, model_name, model_info)

    job_info = {'task_id': task_id, 'train_data': data_name, 'eval_data': eval_name, 'checkpoint_path': checkpoint_path,
                'output_path': output_path, 'log_path': log_path, 'gpus': gpus}
    print("total_task_run job_info: ", job_info)

    if offline_finetune_task_run(job_info, hyper_parameters, model_info) == 0:
        if offline_merge_task_run(job_info, model_info) == 0:
            if offline_eval_task_run(job_info, hyper_parameters, model_info) == 0:
                print("total_task_run success.")


def list_hyper_parameters() -> dict:
    hparams = my_settings.hyper_params_desc
    add_hparams = my_settings.additional_params_desc
    hyper_params = {
        'hparams': hparams,
        'additional': add_hparams
    }
    print("hyper_params: ", hyper_params)
    return hyper_params
