import subprocess
import threading
import json
from datetime import datetime
from .tools.params_utils import get_job_info, get_hparams, get_model_info
from .tools.log_utils import capture_output
from .tools.file_utils import write_csv_file
from ..settings import Settings

my_settings = Settings()


def offline_eval_task_run(job_info: dict, hparams: dict, model_info: dict):
    eval_script = my_settings.task_params['script']['eval_script']
    job_info = get_job_info(job_info)
    hparams = get_hparams(hparams)
    model_info = get_model_info(model_info)
    script_args = [
        model_info['model_path'],
        job_info['eval_data'],
        job_info['eval_path'],
        model_info['model_template'],
        model_info['finetuning_type'],
        job_info['gpus'],
        hparams['per_device_eval_batch_size'],
        hparams['max_samples'],
        job_info['task_id']
    ]
    command = [eval_script] + script_args
    log_file_name = "_eval.log"
    log_file_path = job_info['log_path'] + job_info['task_id'] + log_file_name
    print("=====>>>>> 离线任务开始执行:", command)
    write_csv_file("offline_eval_task", job_info, model_info, hparams, log_file_path)
    with open(log_file_path, 'a') as log_file:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output_thread = threading.Thread(target=capture_output, args=(process, log_file))
        output_thread.start()
        process.wait()
        output_thread.join()

    end_df = datetime.now().strftime(my_settings.datatime_sft)
    # metric_json = dict()
    # metric_json["task_id"] = job_info['task_id']
    # metric_json["train_action"] = 1
    if process.returncode == 0:
        # metric_json["status"] = 2
        # try:
        #     r.publish('ALITA:TASK:TRAIN:METRIC', json.dumps(metric_json))
        #     print("success publish to ALITA:TASK:TRAIN:METRIC,", metric_json)
        # except Exception as e:
        #     print("failed publish to ALITA:TASK:TRAIN:METRIC,", e)
        print("===== 离线任务执行成功: ", command, end_df)
    else:
        # metric_json["status"] = 4
        # try:
        #     r.publish('ALITA:TASK:TRAIN:METRIC', json.dumps(metric_json))
        #     print("success publish to ALITA:TASK:TRAIN:METRIC,", metric_json)
        # except Exception as e:
        #     print("failed publish to ALITA:TASK:TRAIN:METRIC,", e)
        print("===== 离线任务执行失败: ", command, end_df)


def offline_eval_task(model_name: str, eval_data: str, hparams: dict):
    return offline_eval_task_run(
        {"eval_data": eval_data},
        hparams,
        {"model_name": model_name}
    )
