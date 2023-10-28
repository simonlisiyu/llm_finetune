import psutil
from datetime import datetime
from .tools.params_utils import append_model_info_by_merge_task
from .finetune_service import offline_finetune_task_run, copy_file_to_directory
from .merge_service import offline_merge_task_run
from .eval_service import offline_eval_task_run
from .tools.file_utils import append_to_json
from ..settings import Settings

my_settings = Settings()


def total_task_run(task_id: str, template: str, model_path: str, data_path: str, eval_data: str,
                   checkpoint_path: str, output_path: str, log_path: str, gpus: str, finetuning_type: str,
                   hyper_parameters: dict):

    data_name = copy_file_to_directory(data_path)
    eval_name = copy_file_to_directory(eval_data)

    # 追加数据到dataset JSON文件
    data_json_file = my_settings.base_dir + my_settings.data_file
    new_data = {data_name:
                    {'file_name': data_name + "/" + data_name + ".json",
                     'data_count': 'unknown',
                     'upload_at': datetime.now().strftime(my_settings.datatime_sft)
                     }}
    append_to_json(data_json_file, new_data)
    new_data = {eval_name:
                    {'file_name': eval_name + "/" + eval_name + ".json",
                     'data_count': 'unknown',
                     'upload_at': datetime.now().strftime(my_settings.datatime_sft)
                     }}
    append_to_json(data_json_file, new_data)

    # 追加模型到model_info JSON文件
    model_name = model_path.split('/')[-1]
    model_dir = model_path.split('/')[:-1]
    model_dir_str = '/'.join([str(s) for s in model_dir])
    model_info = {'model_name': model_name, 'model_path': model_path, 'model_template': template, 'finetuning_type': finetuning_type, 'size': '-1'}
    append_model_info_by_merge_task(model_dir_str, model_name, model_info)

    job_info = {'task_id': task_id, 'train_data': data_name, 'eval_data': eval_name, 'checkpoint_path': checkpoint_path,
                'output_path': output_path, 'log_path': log_path, 'gpus': gpus}
    print("total_task_run job_info: ", job_info)

    offline_finetune_task_run(job_info, hyper_parameters, model_info)
    offline_merge_task_run(job_info, model_info)
    offline_eval_task_run(job_info, hyper_parameters, model_info)
    return True


def task_kill(task_id: str):
    all_processes = psutil.process_iter()
    # 遍历进程列表，查找包含指定task_id的进程
    for process in all_processes:
        try:
            # 获取进程的命令行参数
            cmdline = process.cmdline()
            if cmdline and task_id in cmdline:
                process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return True
