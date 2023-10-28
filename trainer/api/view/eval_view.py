from fastapi import APIRouter, Request
import threading
from fastapi.templating import Jinja2Templates
from ...service.finetune_service import get_task_log, get_dataset_names, get_models_names
from ...service.eval_service import offline_eval_task

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
        },
    )


@router.post("/eval/task/run")
async def process_eval(request: Request):
    form_data = await request.form()
    model_name = form_data.get("model_name")
    train_data = form_data.get("eval_data")
    hparams = form_data.get("hparams")
    hparams = '{}' if hparams == "" or hparams is None else hparams
    task_thread = threading.Thread(target=offline_eval_task,
                                   args=(model_name, train_data, hparams))
    task_thread.start()

    return {"message": "离线训练任务已启动..."}