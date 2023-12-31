import subprocess
import threading
import json
from datetime import datetime
from ..model import MergeLog
from .tools.params_utils import get_job_info, get_model_info, append_model_info_by_merge_task
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


def get_task_log() -> [MergeLog]:
    try:
        data = read_csv_file("offline_merge_task")
    except Exception as e:
        data = []
    merge_info = [MergeLog(*info) for info in data]
    return merge_info


def offline_merge_task_run(job_info: dict, model_info: dict):
    merge_script = my_settings.task_params['script']['merge_script']
    new_model_name = str(job_info['output_path'])
    job_info['output_path'] = my_settings.model_dir + new_model_name
    job_info = get_job_info(job_info)
    model_info = get_model_info(model_info)
    script_args = [
        model_info['model_path'],
        job_info['checkpoint_path'],
        job_info['output_path'],
        model_info['model_template'],
        model_info['finetuning_type'],
        job_info['task_id']
    ]
    command = [merge_script] + script_args
    start_df = job_info['start_time']
    log_file_name = "_merge.log"
    log_file_path = job_info['log_path'] + job_info['task_id'] + log_file_name
    print("=====>>>>> 离线任务开始执行:", command)
    short_log_path = log_file_path.replace(my_settings.base_dir, "")
    write_csv_file("offline_merge_task", start_df, model_info['model_path'], job_info['output_path'], short_log_path)
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
    metric_json["train_action"] = 2
    if process.returncode == 0:
        metric_json["status"] = 2
        try:
            r.xadd('TRAINER:TASK:TRAIN:METRIC', {job_info['task_id']: json.dumps(metric_json)})
            print("success xadd to TRAINER:TASK:TRAIN:METRIC,", metric_json)
        except Exception as e:
            print("failed xadd to TRAINER:TASK:TRAIN:METRIC,", e)
        append_model_info_by_merge_task(my_settings.model_dir, new_model_name, model_info)
        print("===== 离线任务执行成功: ", command, end_df)
    else:
        metric_json["status"] = 4
        try:
            r.xadd('TRAINER:TASK:TRAIN:METRIC', {job_info['task_id']: json.dumps(metric_json)})
            print("success xadd to TRAINER:TASK:TRAIN:METRIC,", metric_json)
        except Exception as e:
            print("failed xadd to TRAINER:TASK:TRAIN:METRIC,", e)
        print("===== 离线任务执行失败: ", command, end_df)
    return process.returncode


def offline_merge_task(model_name, checkpoint_path, output_path):
    return offline_merge_task_run(
        {"task_id": "merge_task_" + datetime.now().strftime('%Y-%m-%d_%H:%M:%S'),
         "checkpoint_path": checkpoint_path, "output_path": output_path},
        {"model_name": model_name}
    )