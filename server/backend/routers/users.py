from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import get_id_user
from .utils_functions.models import TokenLoginSchema
from .utils_functions.crud import getInfo, getPostsFromID_user, get_id_user_from_username, get_relation, getInfoByRelation


router = APIRouter()

@router.post("/myinfo", dependencies=[Depends(JWTBearer())])
async def getMyInfo_function(token: TokenLoginSchema = Body(...)):
    id_user = get_id_user(token.token)
    return {
        "result": True,
        "info": getInfo(id_user=id_user),
        "posts": getPostsFromID_user(id_user=id_user, rel=10),
    }

@router.post("/get/{username_recipient}", dependencies=[Depends(JWTBearer())])
async def getInfo_function(username_recipient: str, token: TokenLoginSchema = Body(...)):
    id_user_recipient = get_id_user_from_username(username_recipient)
    if not id_user_recipient: 
        return {
            "result": False,
            "code": 404,
            "error": "Nessun profilo con questo username"
        }
    id_user_sender = get_id_user(token.token)
    relation = get_relation(id_user_recipient=id_user_recipient, id_user_sender=id_user_sender)
    if relation == -99:
        return {
            "result": False,
            "error": "Qualcosa è andato storto durante la creazione della relazione"
        } 
    return getInfoByRelation(id_user_recipient=id_user_recipient, relation=relation)