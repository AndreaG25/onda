from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import  get_id_user, get_username
from .utils_functions.models import (
    UpdateRelation, TokenLoginSchema, RelationAnswer
)

from .utils_functions.crud import (
    get_id_user_from_username, changeRelation, getFollowRequests,
    get_relation, checkUserRequest, accept_refuse_request, blockUser,
    getFollowers, getFollowed, getRequests
)

from .utils_functions.new_not import newNotification_follow

router = APIRouter()


@router.get("/relmain/")
async def hel():
    return {"Hello": "world by post route"}

@router.post("/update", dependencies=[Depends(JWTBearer())])
async def changeRelation_function(updateMyRelation: UpdateRelation = Body(...)):
    id_user_sender = get_id_user(updateMyRelation.token)
    id_user_recipient = get_id_user_from_username(username=updateMyRelation.username_recipient)
    current_relation = get_relation(id_user_recipient=id_user_recipient, id_user_sender=id_user_sender)
    if ((updateMyRelation.new_state != 0 and updateMyRelation.new_state != 1 and updateMyRelation.new_state != 2) and (current_relation != 3 and updateMyRelation.new_state == 2 ) or (id_user_sender == id_user_recipient)):
        blockUser(id_user=id_user_sender)
        return {
            "result": False,
            "error": "Violazione individuata"
        }

    if updateMyRelation.new_state == 1 and current_relation == 0:
        newNotification_follow(sender=get_username(jwtoken=updateMyRelation.token), recipient=id_user_recipient)

    if changeRelation(id_user_sender=id_user_sender, id_user_recipient=id_user_recipient, new_state=updateMyRelation.new_state) and id_user_sender != None:
        return {
            "result": True,
            "Mittente": id_user_sender,
            "Destintatio": id_user_recipient
        }
    return {
        "result": False,
        "error": "Qualcosa è andato storto nella richista"
    }

@router.post("/home", dependencies=[Depends(JWTBearer())])
async def getRelation_function(myToken: TokenLoginSchema = Body(...)):
    id_user = get_id_user(myToken.token)
    res = getFollowRequests(id_user=id_user)
    if res or res == []:
        return {
            "result": True,
            "data": res
        }
    return {
        "result": False,
        "error": "Qualcosa è andato storto nella richista"
    }


@router.post("/getrelations", dependencies=[Depends(JWTBearer())])
async def getRelation_function(myToken: TokenLoginSchema = Body(...)):
    id_user = get_id_user(myToken.token)
    return {
        "followers": getFollowers(id_user=id_user),
        "followed": getFollowed(id_user=id_user),
        "requests": getRequests(id_user=id_user)
    }

@router.post("/answer", dependencies=[Depends(JWTBearer())])
async def getRelation_function(myAnswer: RelationAnswer = Body(...)):
    id_user = get_id_user(myAnswer.token)
    if checkUserRequest(id_follow=myAnswer.id_follow, id_user=id_user):
        if accept_refuse_request(id_follow=myAnswer.id_follow, answer=myAnswer.answer):
            return {
                "result": True
            }
        return {
            "result": False,
            "error": "Qualcosa è andato storto nella risposta alla richiesta"
        }
    blockUser(id_user=id_user)
    return {
            "result": False,
            "error": "Violazione individuata"
        }
    
    
    
