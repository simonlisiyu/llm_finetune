from fastapi import APIRouter, Request
import threading
from fastapi.templating import Jinja2Templates
from ...service.finetune_service import get_task_log, get_dataset_names, get_models_names
from ...service.eval_service import offline_eval_task, get_eval_tasks

router = APIRouter()
templates = Jinja2Templates(directory="templates")

"""
eval.html
"""


@router.get("/eval")
async def eval_list(request: Request):
    return templates.TemplateResponse(
        "eval.html",
        {
            "request": request,
            "eval_info": get_task_log("offline_eval_task"),
            "models": get_models_names(),
            "datasets": get_dataset_names(),
            "tasks": get_eval_tasks(),
        },
    )


@router.post("/eval/task/run")
async def process_eval(request: Request):
    form_data = await request.form()
    eval_task = form_data.get("eval_task")
    model_name = form_data.get("model_name")
    eval_data = form_data.get("eval_data")
    gpus = form_data.get("gpus")
    hparams = form_data.get("hparams")
    hparams = '{}' if hparams == "" or hparams is None else hparams
    task_thread = threading.Thread(target=offline_eval_task,
                                   args=(eval_task, model_name, eval_data, hparams, gpus))
    task_thread.start()

    return {"message": "离线训练任务已启动..."}