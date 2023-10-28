# __author__ "lisiyu"
# date 2023/10/19

import threading

from fastapi import APIRouter
from ..service.api_task_service import total_task_run, task_kill
from ..model import TrainTaskRequest, TasksRequest

router = APIRouter(prefix="/trainer/task", tags=["trainer task api"])


@router.post('/start', summary="训练、评估、合并任务启动接口", description="task_start")
async def task_start(request: TrainTaskRequest):
    task_id = request.task_id
    template = request.template
    model_path = request.train_model
    data_path = request.train_data
    eval_data = request.eval_data
    checkpoint_path = request.checkpoint_path
    output_path = request.output_path
    log_path = request.log_path
    gpus = request.gpus
    finetuning_type = request.finetuning_type
    hyper_parameters = request.hyper_parameters

    task_thread = threading.Thread(target=total_task_run,
                                   args=(task_id, template, model_path, data_path, eval_data,
                                         checkpoint_path, output_path, log_path, gpus, finetuning_type,
                                         hyper_parameters))
    task_thread.start()
    return {"status": 0, "message": "Task任务已启动.", "data": {}}


@router.post('/stop', summary="训练、评估、合并任务停止接口", description="stop_tasks")
async def tasks_stop(request: TasksRequest):
    task_id = request.task_id
    task_kill(task_id)
    return {"status": 0, "message": "指定TaskId任务已停止.", "data": {}}

#
# @router.post('/train/start', summary="训练任务启动接口", description="start_train")
# async def train_start(request: TrainTaskRequest):
#     task_id = request.task_id
#     model_path = request.train_model
#     data_path = request.train_data
#     output_path = request.output_path
#     log_path = request.log_path
#     hyper_parameters = request.hyper_parameters
#     # epochs = request.hyper_parameters.get("epochs", "3.0")
#     # gpus = request.hyper_parameters.get("gpus", 0)
#     # lr = request.hyper_parameters.get("lr", "5e-5")
#     # per_device_train_batch_size = request.hyper_parameters.get("per_device_train_batch_size", 1)
#     # gradient_accumulation_steps = request.hyper_parameters.get("gradient_accumulation_steps", 1)
#     # lr_scheduler_type = request.hyper_parameters.get("lr", "5e-5")
#     # max_source_length = request.hyper_parameters.get("max_source_length", 512)
#     # max_target_length = request.hyper_parameters.get("max_source_length", 512)
#     # max_samples = request.hyper_parameters.get("max_samples", 512)
#     start_df = datetime.now().strftime(my_settings.datatime_sft)
#     task_thread = threading.Thread(target=offline_finetune_task_run,
#                                    args=(task_id, model_path, data_path, output_path, log_path, hyper_parameters, "0"))
#     task_thread.start()
#     return {"status": 0, "message": "离线训练任务已启动.", "data":{}}
#
#
# @router.post('/eval/start', summary="训练任务启动接口", description="start_train")
# async def eval_start(request: TrainTaskRequest):
#     task_id = request.task_id
#     model_path = request.train_model
#     data_path = request.eval_data
#     output_path = request.checkpoint_path
#     log_path = request.log_path
#     hyper_parameters = request.hyper_parameters
#     start_df = datetime.now().strftime(my_settings.datatime_sft)
#     task_thread = threading.Thread(target=offline_finetune_task_run,
#                                    args=(task_id, model_path, data_path, output_path, log_path, hyper_parameters, "1"))
#     task_thread.start()
#     return {"status": 0, "message": "离线评估任务已启动.", "data":{}}
#
#
# @router.post('/merge/start', summary="合并任务启动接口", description="start_train")
# async def merge_start(request: TrainTaskRequest):
#     task_id = request.task_id
#     model_path = request.train_model
#     checkpoint_path = request.checkpoint_path
#     output_path = request.output_path
#     log_path = request.log_path
#     task_thread = threading.Thread(target=offline_merge_task_run,
#                                    args=(model_path, checkpoint_dir, output_path, log_path))
#     task_thread.start()
#     return {"status": 0, "message": "离线合并任务已启动.", "data":{}}
