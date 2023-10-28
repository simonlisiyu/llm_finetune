from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from ...settings import Settings
from ...service.tools.file_utils import (read_script_info, append_to_json)
from ...service.custom_script_service import offline_task
import json
import threading
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")
my_settings = Settings()

"""
script_list.html & script_detail.html
"""


@router.get("/script")
async def list_script(request: Request):
    try:
        script_info = read_script_info()
        print(script_info)
    except Exception as e:
        script_info = []

    print(script_info)
    return templates.TemplateResponse(
        "script_list.html",
        {
            "request": request,
            "script_info": script_info,
        },
    )


@router.post("/show_script")
async def script(request: Request):
    form_data = await request.form()
    file_path = form_data["filepath"]
    filename = form_data["name"]

    with open(file_path, "r") as file:
        file_content = file.read()

    return templates.TemplateResponse(
        "script_detail.html",
        {
            "request": request,
            "file_content": file_content,
            "filepath": file_path,
            "filename": filename
        })


@router.post("/save_script")
async def save(request: Request, file_content: str = Form(...)):
    form_data = await request.form()
    file_path = form_data["filepath"]
    filename = form_data["name"]

    with open(file_path, "w") as file:
        file.write(file_content)

    # 追加数据到dataset JSON文件
    json_file = my_settings.dev_script_dir + '/script_info.json'
    with open(json_file, 'r') as file:
        json_data = json.load(file)
        json_obj = json_data[filename]
        json_obj['update_at'] = datetime.now().strftime(my_settings.datatime_sft)
        json_data[filename] = json_obj
    with open(json_file, 'w') as file:
        json.dump(json_data, file, ensure_ascii=False)

    return {"message": "文件已保存"}


@router.post("/run_script")
async def run_script(request: Request):
    form_data = await request.form()
    filename = form_data["name"]
    file_path = form_data["filepath"]

    start_df = datetime.now().strftime(my_settings.datatime_sft)
    task_thread = threading.Thread(target=offline_task,
                                   args=(file_path, filename, start_df))
    task_thread.start()

    return {"message": "离线训练任务已启动..."}