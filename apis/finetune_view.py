from fastapi import APIRouter, Request
import os
import json
import threading
from datetime import datetime
from fastapi.templating import Jinja2Templates
from service.finetune_service import offline_finetune_task
from service.tools.log_utils import FinetuneLog
from service.tools.file_utils import (read_csv_file, validate_json, append_to_json, create_directory,
                                      get_directories, get_directories_and_files)
from service.settings import Settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
my_settings = Settings()

"""
finetune.html
"""


# @router.post("/do_upload")
# async def do_upload(request: Request):
#     form = await request.form()
#     file = form['file'].file
#     filename = form['file'].filename
#     target_folder = create_directory(filename, my_settings.base_data_dir)
#
#     contents = file.read()
#     is_valid, err = validate_json(contents)
#     if not is_valid:
#         return {"message": "文件json格式校验失败...", "err": str(err)}
#
#     with open(os.path.join(target_folder, filename), 'wb') as f:
#         f.write(contents)
#
#     # 追加数据到JSON文件
#     upload_file = target_folder + '/' + filename
#     json_file = my_settings.base_data_dir + '/' + my_settings.script['datafile']
#     new_data = {filename.split('.')[0]: {'file_name': upload_file}}
#     append_to_json(json_file, new_data)
#
#     return {'message': 'File {} uploaded successfully'.format(filename)}


@router.get("/finetune")
async def finetune(request: Request):
    try:
        data = read_csv_file("offline_finetune_task")
    except Exception as e:
        data = []

    finetune_info = [FinetuneLog(*info) for info in data]

    json_file = my_settings.base_data_dir + '/' + my_settings.script['datafile']
    with open(json_file, 'r') as file:
        json_data = json.load(file)
    dataset_keys = json_data.keys()

    # dirs = get_directories(my_settings.base_data_dir)
    # file_dict = get_directories_and_files(my_settings.base_data_dir)
    return templates.TemplateResponse(
        "finetune.html",
        {
            "request": request,
            "finetune_info": finetune_info,
            "models": my_settings.models,
            "datasets": dataset_keys,
            # "dirs": dirs,
            # "file_dict": file_dict,
        },
    )


@router.post("/process_finetune")
async def process_finetune(request: Request):
    form_data = await request.form()
    model_path = form_data.get("model_path")
    train_data_path = form_data.get("train_data_path")
    # epochs = form_data.get("epochs")
    hparams = {}
    hparams['epochs'] = form_data.get("epochs")
    hparams['gpus'] = ''
    hparams['lr'] = ''
    hparams['per_device_train_batch_size'] = ''
    hparams['gradient_accumulation_steps'] = ''
    hparams['lr_scheduler_type'] = ''
    hparams['max_source_length'] = ''
    hparams['max_target_length'] = ''
    hparams['max_samples'] = ''
    start_df = datetime.now().strftime(my_settings.datatime_sft)
    task_thread = threading.Thread(target=offline_finetune_task,
                                   args=(model_path, train_data_path, hparams, start_df))
    task_thread.start()

    return {"message": "离线训练任务已启动..."}
