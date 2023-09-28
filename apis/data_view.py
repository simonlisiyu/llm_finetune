from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
import os
import json
from datetime import datetime
from fastapi.templating import Jinja2Templates
from service.tools.file_utils import (write_json_to_excel, read_dataset_info, validate_json, delete_key_in_json,
                                      append_to_json, create_directory, excel_to_json, delete_file)
from service.settings import Settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
my_settings = Settings()

"""
data.html
"""


@router.post("/do_upload")
async def upload_data_file(request: Request):
    form = await request.form()
    file = form['file'].file
    filename = form['file'].filename
    target_folder, directory_name = create_directory(filename, my_settings.base_data_dir)
    upload_file = os.path.join(target_folder, filename)

    if os.path.splitext(filename)[1] == ".xlsx":
        with open(my_settings.base_data_dir + "/temp_file.xlsx", "wb") as temp_file:
            temp_file.write(file.read())
        contents = excel_to_json(my_settings.base_data_dir + "/temp_file.xlsx")
        data_count = len(contents)

        filename = filename.replace('.xlsx', '.json')
        upload_file = upload_file.replace('.xlsx', '.json')
        with open(upload_file, 'w', encoding='utf-8') as f:
            json.dump(contents, f, ensure_ascii=False, indent=4)
    elif os.path.splitext(filename)[1] == ".json":
        contents = file.read()
        is_valid, err, data_count = validate_json(contents)
        if not is_valid:
            return {"message": "文件json格式校验失败...", "err": str(err)}
        with open(upload_file, 'wb') as f:
            f.write(contents)
    else:
        return {"message": "未知文件类型", "err": str(filename)}

    # 追加数据到dataset JSON文件
    json_file = my_settings.base_data_dir + '/' + my_settings.script['datafile']
    new_data = {filename.split('.')[0]:
                    {'file_name': directory_name + "/" + filename,
                     'data_count': str(data_count),
                     'upload_at': datetime.now().strftime(my_settings.datatime_sft)
                     }}
    append_to_json(json_file, new_data)

    return {'message': 'File {} uploaded successfully'.format(filename)}


@router.get("/data")
async def list_data(request: Request):
    try:
        dataset_info = read_dataset_info(my_settings.base_data_dir + "/dataset_info.json")
    except Exception as e:
        dataset_info = []

    return templates.TemplateResponse(
        "data.html",
        {
            "request": request,
            "dataset_info": dataset_info,
        },
    )


@router.get("/data/{path}/{filename}")
def get_one_data_file(request: Request, path: str, filename: str):
    lines = []
    data_path = my_settings.data_path + path + "/" + filename
    print("data_path: ", data_path)
    with open(data_path, "r") as file:
        for line in file:
            lines.append(line.strip())  # 将每行日志添加到列表中

    return templates.TemplateResponse("logs.html", {"request": request, "logs": lines})


@router.post("/do_download")
async def download_data_excel(request: Request):
    form_data = await request.form()
    json_path = form_data["filepath"]
    if not os.path.exists(json_path):
        return {"message": "文件不存在"}
    excel_path, excel_name = write_json_to_excel(json_path)
    return FileResponse(excel_path,
                        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        filename=excel_name)


@router.post("/do_delete")
async def delete_data_file(request: Request):
    form_data = await request.form()
    json_path = form_data["filepath"]
    if not os.path.exists(json_path):
        return {"message": "文件不存在"}
    delete_return = delete_file(json_path)

    json_file = my_settings.base_data_dir + '/' + my_settings.script['datafile']
    key_name = json_path.split("/")[-1].split('.')[0]
    delete_key_in_json(json_file, key_name)
    return {'message': 'File deleted finished. response is {}'.format(delete_return)}