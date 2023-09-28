# encoding: utf8
import threading
from os.path import join, dirname, basename
from datetime import datetime
from fastapi import APIRouter, Request, File, Form, UploadFile
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from service.finetune_service import offline_finetune_task, copy_file_to_directory
from service.merge_service import offline_merge_task
from service.tools.log_utils import MergeLog
from service.tools.file_utils import read_csv_file, validate_json, create_directory
from service.tools.docker_utils import llm_docker_start
from service.settings import Settings

router = APIRouter(prefix="/api", tags=["http api"])
my_settings = Settings()

@router.post("/do_upload", summary="上传训练数据")
async def do_upload(file: UploadFile):
    filename = file.filename
    target_folder = create_directory(filename, my_settings.base_data_dir)
    contents = await file.read()
    is_valid, err = validate_json(contents)
    if not is_valid:
        return {"status": 1, "message": "文件json格式校验失败...", "err": str(err)}

    with open(join(target_folder, filename), 'wb') as f:
        f.write(contents)
    return {"status": 0, 'message': 'File {} uploaded successfully'.format(filename)}


class FtItem(BaseModel):
    backbone_model: str
    train_data: str
    model_path: str
    hyper_parameters: dict


def offline_finetune_and_merge(model_path: str, valid_data_file: str, hparams: dict, output_path: str, start_df: str):
    data_path = copy_file_to_directory(valid_data_file)
    print("data_path:", data_path)
    offline_finetune_task(model_path, data_path, hparams, start_df)
    offline_merge_task(model_path, output_path)


@router.post('/finetune', summary="微调接口", description="finetune")
async def finetune(item: FtItem):
    model_path = item.backbone_model
    train_data_file = item.train_data
    output_path = item.model_path
    # epochs = item.hyper_parameters.get("epochs", 10)
    start_df = datetime.now().strftime(my_settings.datatime_sft)
    # offline_finetune_and_merge(model_path, train_data_file, item.hyper_parameters, output_path, start_df)
    task_thread = threading.Thread(target=offline_finetune_and_merge,
                                   args=(model_path, train_data_file, item.hyper_parameters, output_path, start_df))
    task_thread.start()
    return {"status": 0, "message": "离线训练任务已启动.", "data":{"start time":start_df}}


class JobsItem(BaseModel):
    model_path: str = None


@router.post('/finetune_jobs', summary="训练任务列表")
async def finetune_jobs(item: JobsItem):
    try:
        data = read_csv_file("offline_merge_task")
    except Exception as e:
        data = []
    model_path = item.model_path
    merge_info = [MergeLog(*info) for info in data if not model_path or info[4]==model_path]
    return {"status": 0, "message": "OK", "data":[ml.__dict__ for ml in merge_info]}

class StartItem(BaseModel):
    model_path: str
    model_name: str
    gpus: str
    api_port: int

@router.post('/start_service', summary="启动模型服务")
async def start_service(item: StartItem, **kwargs):
    model_name = item.model_name
    model_path = item.model_path
    #parent_dir = dirname(model_path)
    #model_dir = basename(model_path)
    parent_dir = my_settings.host_model_dir
    if model_path.startswith(my_settings.base_model_dir):
        model_dir = model_path[len(my_settings.base_model_dir):].lstrip("/")
    else:
        model_dir = model_path
    gpus = item.gpus
    ip = my_settings.app_ip
    port = item.api_port

    # 处理额外的可变参数
    additional_args = ""
    for key, value in kwargs.items():
        additional_args += " --{} {}".format(key, value)

    task_thread = threading.Thread(target=llm_docker_start,
                                   args=(model_name, parent_dir, model_dir, gpus, ip, port, additional_args))
    task_thread.start()

    return {"status": 0, "message": "LLM docker已在启动...", "data": {"ip":ip, "port":port}}


