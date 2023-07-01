from fastapi import APIRouter, Body, Depends
from .utils_functions.models import (
    TokenLoginSchema
)
from .utils_functions.createid import createID
from ..auth.auth_handler import get_username, get_id_user
from ..auth.auth_bearer import JWTBearer

from .utils_functions.crud import (getRecentPost,
     getprofilePic, getPostbyFollower)

router = APIRouter()


@router.post("/", dependencies=[Depends(JWTBearer())])
async def home_function(token: TokenLoginSchema = Body(...)):
    id_user = get_id_user(jwtoken=token.token)
    return {
        "profile_pic": getprofilePic(id_user=id_user),
        "recent_post": getRecentPost(),
        "post_by_follower": getPostbyFollower(id_user=id_user)
    }
