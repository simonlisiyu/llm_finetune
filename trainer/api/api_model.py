# __author__ "lisiyu"
# date 2023/10/28

from fastapi import APIRouter
from ..service.model_service import get_template_list

router = APIRouter(prefix="/trainer/model", tags=["trainer model api"])


@router.get('/template/list', summary="模型template接口", description="list template")
async def list_model_template():
    return {"status": 0, "message": "模型template列表.", "data": get_template_list()}