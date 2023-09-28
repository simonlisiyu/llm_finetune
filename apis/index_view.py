from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import subprocess

router = APIRouter()
templates = Jinja2Templates(directory="templates")

"""
index.html
"""


@router.get("/")
async def gpu_usage(request: Request):
    output = subprocess.check_output(["nvidia-smi", "--query-gpu=index,name,utilization.gpu,memory.used,memory.total",
                                      "--format=csv,noheader,nounits"])
    gpu_info = output.decode("utf-8").strip().split("\n")
    gpu_info = [info.split(", ") for info in gpu_info]

    class GPUInfo:
        def __init__(self, index, name, utilization, memory_used, memory_total):
            self.index = index
            self.name = name
            self.utilization = utilization
            self.memory_used = memory_used
            self.memory_total = memory_total

    gpu_info = [GPUInfo(*info) for info in gpu_info]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "gpu_info": gpu_info,
        },
    )