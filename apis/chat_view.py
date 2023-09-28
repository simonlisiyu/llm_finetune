from fastapi import APIRouter, Request
import threading
from fastapi.templating import Jinja2Templates
from service.tools.file_utils import get_directories
from service.tools.docker_utils import (DockerInfo,
                                        show_docker_containers, docker_info_split, llm_docker_start,
                                        start_docker_container_by_id, stop_docker_container_by_id,
                                        show_container_logs_by_id)
from service.settings import Settings

router = APIRouter()
templates = Jinja2Templates(directory="templates")
my_settings = Settings()

"""
chat.html
"""


@router.get("/chat")
async def chat(request: Request):
    ai_url = my_settings.localai_url
    app_ip = my_settings.app_ip
    model_dir = my_settings.base_model_dir
    dirs = get_directories(my_settings.base_model_dir)
    host_dir = my_settings.host_model_dir

    container_info = show_docker_containers()
    chat_info = [DockerInfo(*info.split(docker_info_split)) for info in container_info]
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "chat_info": chat_info,
            "dirs": dirs,
            "host": f"{host_dir}",
            "ai_url": f"{ai_url}",
            "app_ip": f"{app_ip}",
            "model_dir": f"{model_dir}",
        },
    )


@router.post("/process_chat")
async def process_chat(request: Request):
    form_data = await request.form()
    model_name = "llm_" + form_data.get("model_name")
    # parent_dir = form_data.get("parent_dir")
    parent_dir = my_settings.host_model_dir
    model_dir = form_data.get("model_dir")
    gpus = form_data.get("gpus")
    # ip = form_data.get("ip")
    ip = my_settings.app_ip
    port = form_data.get("port")
    task_thread = threading.Thread(target=llm_docker_start,
                                   args=(model_name, parent_dir, model_dir, gpus, ip, port, ""))
    task_thread.start()

    return {"message": "LLM docker已在启动..."}


@router.get("/logs/{log}")
def read_logs(request: Request, log: str):
    logs = []
    log_path = my_settings.logs_path + log + ".log"
    print("log_path: ", log_path)
    with open(log_path, "r") as file:
        for line in file:
            logs.append(line.strip())  # 将每行日志添加到列表中

    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})


@router.post("/start-container")
async def start_container(request: Request):
    form_data = await request.form()
    return start_docker_container_by_id(form_data["container_id"])


@router.post("/stop-container")
async def stop_container(request: Request):
    form_data = await request.form()
    return stop_docker_container_by_id(form_data["container_id"])


@router.post("/logs-container")
async def container(request: Request):
    form_data = await request.form()
    logs = show_container_logs_by_id(form_data["container_id"])
    return templates.TemplateResponse(
        "message.html",
        {
            "request": request,
            "message": logs,
        },
    )


'''
subprocess way
'''
# @app.post("/start-container")
# async def start_container(request: Request):
#     form_data = await request.form()
#     container_id = form_data["container_id"]
#     try:
#         subprocess.run(["docker", "start", container_id], check=True)
#         return {"message": f"Container {container_id} started successfully"}
#     except subprocess.CalledProcessError:
#         return {"error": f"Failed to start container {container_id}"}
#
#
# @app.post("/stop-container")
# async def stop_container(request: Request):
#     form_data = await request.form()
#     container_id = form_data["container_id"]
#     try:
#         subprocess.run(["docker", "stop", container_id], check=True)
#         return {"message": f"Container {container_id} stopped successfully"}
#     except subprocess.CalledProcessError:
#         return {"error": f"Failed to stop container {container_id}"}
