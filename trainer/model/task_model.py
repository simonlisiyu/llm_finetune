# __author__ "lisiyu"
# date 2023/10/26
from pydantic import BaseModel


# 训练任务请求体的数据模型
class TrainTaskRequest(BaseModel):
    task_id: str
    template: str
    train_model: str
    train_data: str
    eval_data: str
    checkpoint_path: str
    output_path: str
    log_path: str
    gpus: str
    finetuning_type: str
    hyper_parameters: dict


# 训练任务响应体的数据模型
class TrainTaskResponse(BaseModel):
    status: str
    errstr: str = None
    result: dict = None


class TasksRequest(BaseModel):
    task_id: str
