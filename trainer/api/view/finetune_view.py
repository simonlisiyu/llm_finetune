from fastapi import APIRouter, Request
import json
import threading
from fastapi.templating import Jinja2Templates
from ...service.finetune_service import get_task_log, get_dataset_names, get_models_names, offline_finetune_task

router = APIRouter()
templates = Jinja2Templates(directory="templates")

"""
finetune.html
"""


@router.get("/finetune")
async def finetune(request: Request):
    return templates.TemplateResponse(
        "finetune.html",
        {
            "request": request,
            "finetune_info": get_task_log("offline_finetune_task"),
            "models": get_models_names(),
            "datasets": get_dataset_names(),
        },
    )


@router.post("/finetune/task/run")
async def process_finetune(request: Request):
    form_data = await request.form()
    model_name = form_data.get("model_name")
    train_data = form_data.get("train_data")
    epochs = form_data.get("epochs")
    hparams = form_data.get("hparams")
    hparams = '{}' if hparams == "" or hparams is None else hparams
    hparams_json = json.loads(hparams)
    hparams_json["epochs"] = epochs
    task_thread = threading.Thread(target=offline_finetune_task,
                                   args=(model_name, train_data, hparams_json))
    task_thread.start()

    return {"message": "离线训练任务已启动..."}
