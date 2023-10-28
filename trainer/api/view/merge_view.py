from fastapi import APIRouter, Request
import threading
from fastapi.templating import Jinja2Templates
from ...service.merge_service import offline_merge_task, get_task_log
from ...service.finetune_service import get_models_names

router = APIRouter()
templates = Jinja2Templates(directory="templates")

"""
merge.html
"""


@router.get("/merge")
async def merge(request: Request):
    return templates.TemplateResponse(
        "merge.html",
        {
            "request": request,
            "merge_info": get_task_log(),
            "models": get_models_names(),
        },
    )


@router.post("/merge/task/run")
async def process_merge(request: Request):
    form_data = await request.form()
    model_name = form_data.get("model_name")
    output_path = form_data.get("output_path")
    task_thread = threading.Thread(target=offline_merge_task,
                                   args=(model_name, output_path))
    task_thread.start()

    return {"message": "离线合并任务已启动..."}
