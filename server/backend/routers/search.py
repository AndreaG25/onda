from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from .utils_functions.models import searchUser
from .utils_functions.createid import createID
from .utils_functions.crud import search

router = APIRouter()

@router.get("/{string}", dependencies=[Depends(JWTBearer())])
async def newPost_function(string: str):
    res = search(string=string)
    return {
        "result": True,
        "data": res
    }
