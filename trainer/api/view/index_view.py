from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ...service import get_gpu_info, get_cpu_info, get_mem_info, get_disk_info

router = APIRouter()
templates = Jinja2Templates(directory="templates")

"""
index.html
"""


@router.get("/")
async def gpu_usage(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "gpu_info": get_gpu_info(),
            "cpu_info": get_cpu_info(),
            "mem_info": get_mem_info(),
            "disk_info": get_disk_info(),
        },
    )