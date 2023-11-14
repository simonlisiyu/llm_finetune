# __author__ "lisiyu"
# date 2023/10/28

from fastapi import APIRouter
from ..service.system_service import get_host_info, get_gpu_info, get_cpu_info, get_mem_info, get_disk_info

router = APIRouter(prefix="/trainer/system", tags=["trainer system api"])


@router.get('/usage/list', summary="系统监控接口", description="list system usage")
async def list_system_usage():
    return {"status": 0, "message": "系统usage列表.", "data": {
        "host": get_host_info(),
        "cpu": get_cpu_info(),
        "memory": get_mem_info(),
        "gpu": get_gpu_info(),
        "disk": get_disk_info()
    }}
