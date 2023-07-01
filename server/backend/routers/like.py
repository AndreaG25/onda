from fastapi import APIRouter, Body, Depends
from .utils_functions.models import (
    likeSchema
)
from .utils_functions.createid import createID
from ..auth.auth_handler import get_username, get_id_user
from ..auth.auth_bearer import JWTBearer

from .utils_functions.crud import updateLike

router = APIRouter()


@router.post("/new", dependencies=[Depends(JWTBearer())])
async def like_function(like: likeSchema = Body(...)):
    id_user = get_id_user(jwtoken=like.token)
    id_like = createID("like")
    if updateLike(id_user=id_user, id_like=id_like, like=like):
        return {
            "result": True
        }
    return {
        "result": False,
        "error": "Qualcosa è andato storto durante l'inserimento del like"
    }