from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import get_username, get_id_user
from .utils_functions.models import (
    NewPWSchema, UserLoginSchema, NewUsernameSchema, 
    PicUrlSchema, UpdateMyInfo, UpdateRelation
    )

from .utils_functions.crud import (
    tryLogin, updatePW, updateUsername, 
    checkUsername, changePic, changeMyInfo,
    get_id_user_from_username, changeRelation
    )

router = APIRouter()


@router.get("/postmain/")
async def hel():
    return {"Hello": "world by post route"}

@router.post("/password", dependencies=[Depends(JWTBearer())])
async def changePW_function(updatePWObj: NewPWSchema = Body(...)):
    user = UserLoginSchema(username=get_username(updatePWObj.token), password=updatePWObj.current)
    res = tryLogin(user=user)
    if res == None:
        return {
            "result": False,
            "error": "La password corrente non è corretta"
        }
    if updatePW(id_user=res, password=updatePWObj.new):
        return {
            "result": True
        }
    return{
        "result": False,
        "error": "Qualcosa è andato storto nel salvare la nuova password"
    }

@router.post("/username", dependencies=[Depends(JWTBearer())])
async def changeUsername_function(updateUNObj: NewUsernameSchema = Body(...)):
    if get_username(updateUNObj.token) == updateUNObj.new:
        return {
            "result": False,
            "error": "Il nuovo username non può essere uguale a quello vecchio"
        }
    if not checkUsername(username=updateUNObj.new):
        return {
            "result": False,
            "error": "Il nuovo username appartiere a qualcun'altro"
        }
    id_user =  get_id_user(updateUNObj.token)
    if updateUsername(id_user=id_user, new=updateUNObj.new) and id_user != None:
        return {
            "result": True
        }
    return{
        "result": False,
        "error": "Qualcosa è andato storto nel cambiare lo username"
    }
    
    
@router.post("/pic", dependencies=[Depends(JWTBearer())])
async def changeProfilePic_function(updatePicObj: PicUrlSchema = Body(...)):
    id_user = get_id_user(updatePicObj.token)
    if updatePicObj.url == '':
        updatePicObj.url = None
    if changePic(id_user=id_user, new=updatePicObj.url) and id_user != None:
        return {"result": True}
    return {"result": False}

@router.post("/myinfo", dependencies=[Depends(JWTBearer())])
async def changeMyInfo_function(updateMyInfo: UpdateMyInfo = Body(...)):
    id_user = get_id_user(updateMyInfo.token)
    if changeMyInfo(id_user=id_user, data=updateMyInfo) and id_user != None:
        return {"result": True}
    return {"result": False}


#Credo che questa route sia inutile, non so dove viene chiamata
@router.post("/relation", dependencies=[Depends(JWTBearer())])
async def changeRelation_function(updateMyRelation: UpdateRelation = Body(...)):
    id_user_sender = get_id_user(updateMyRelation.token)
    id_user_recipient = get_id_user_from_username(username=updateMyRelation.username_recipient)
    
    if changeRelation(id_user_sender=id_user_sender, id_user_recipient=id_user_recipient, new_state=updateMyRelation.new_state) and id_user_sender != None:
        return {
            "result": True,
            "Mittente": id_user_sender,
            "Destintario": id_user_recipient
        }
    return {
        "result": False,
        "error": "Qualcosa è andato storto nella richista"
    }
    
