from fastapi import APIRouter, Request
import threading
from fastapi.templating import Jinja2Templates
from service.merge_service import offline_merge_task
from service.tools.log_utils import MergeLog
from service.tools.file_utils import read_csv_file
from service.settings import Settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
my_settings = Settings()

"""
merge.html
"""


@router.get("/merge")
async def merge(request: Request):
    try:
        data = read_csv_file("offline_merge_task")
    except Exception as e:
        data = []

    merge_info = [MergeLog(*info) for info in data]
    return templates.TemplateResponse(
        "merge.html",
        {
            "request": request,
            "merge_info": merge_info,
            "models": my_settings.models,
        },
    )


@router.post("/process_merge")
async def process_merge(request: Request):
    form_data = await request.form()
    base_model = form_data.get("model_path")
    output_dir = form_data.get("output_dir")
    task_thread = threading.Thread(target=offline_merge_task,
                                   args=(base_model, output_dir))
    task_thread.start()

    return {"message": "离线合并任务已启动..."}
