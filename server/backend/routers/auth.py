from fastapi import APIRouter, Body, Depends
from .utils_functions.email import (send_confirmation_email, create_confirmation_token
    , validate_confirmation_token, create_changePW_token, validate_changePW_token, 
    send_changepw_email)
from .utils_functions.models import (UserLoginSchema, UserSchema, 
TokenLoginSchema, resetPWSchema, emailSchema, deleteAccountSchema
)
from .utils_functions.functions import checkUserInformation, checkEmail
from .utils_functions.createid import createID
from .utils_functions.crud import (tryLogin, storeInformation,
    setState, getState, get_email_from_id_user, resetPW, 
    deleteAccount, checkUsernameAndIDUser
    )
from ..auth.auth_handler import signJWT, validate_token, get_id_user, get_username
from ..auth.auth_bearer import JWTBearer
from datetime import timedelta
router = APIRouter()


@router.post("/login")
async def login_function(user: UserLoginSchema = Body(...)):
    res =  tryLogin(user)
    if res:
        return signJWT(username=user.username, id_user=res)
    return {
        "result": False,
        "error": "Credenziali non valide, riprova"
    }

@router.post("/signup")
async def signup_function(user: UserSchema = Body(...)):
    res = checkUserInformation(user)
    if res.get("result"):
        new_id = createID("usr")
        if storeInformation(new_id, user):
            token = create_confirmation_token(user.email, id_user=new_id)
            await send_confirmation_email(user.email, token)
            return {
                "result": True,
                "msg": "Ti abbiamo inviato un'email di conferma!"
            }
            #return signJWT(username=user.username, id_user=new_id)
        else:
            return {
                "result": False,
                "error": "Qualcosa è andato storto durante la registrazione"
            }
    return res

@router.get("/confirm/{token}", tags=["auth"])
async def validateSignUPToken_function(token: str):
    res = validate_confirmation_token(token)
    if res[0]:
        if setState(2, res[1]):
            return {
                "result": True,
            }
        return {
            "result": False,
            "error": "Qualcosa è andato storto"
        }
    return {
        "result": False,
        "error": "Il link potrebbere essere errato o scaduto"
    }


@router.post('/resetpasswordrequest', tags=["auth"])
async def resetpasswordrequest_function(email: emailSchema):
    try:
        if not checkEmail(email=email.email):
            token = create_changePW_token(email=email.email)
            await send_changepw_email(email=email.email, token=token)
            return{
                "result": True
            }
        return {
            "result": False,
            "error": "L'indirizzo email non appartiene a nessun utente"
        }
    except:
        return {
            "result": False,
            "error": "Qualcosa è andato storto"
        }
    
@router.post('/resetpassword', tags=["auth"])
async def resetpasswordvalidate_function(data: resetPWSchema):
    res = validate_changePW_token(token=data.token)
    if res[0]:
        return {
            "result": resetPW(email=res[1], password=data.new)
        }
    else:
        return {
            "result": False,
            "error": "Il token non è valido, potrebbe essere scaduto, richiedine un altro"
        }
    



@router.post("/validateToken", tags=["auth"])
async def validateToken_function(token: TokenLoginSchema = Body(...)):
    id_user = get_id_user(jwtoken=token.token)
    username = get_username(jwtoken=token.token)
    if not checkUsernameAndIDUser(username=username, id_user=id_user):
        return {
            "result": False,
            "error": "Token non piu valido"
        }
    return {
        "result": validate_token(token.token),
        "userState": getState(id_user=id_user)[1]
    }

@router.post("/newemail", tags=["auth"])
async def newMail_function(token: TokenLoginSchema = Body(...)):
    id_user = get_id_user(jwtoken=token.token)
    email = get_email_from_id_user(id_user=id_user)
    confirmation_token = create_confirmation_token(email=email, id_user=id_user)
    await send_confirmation_email(email=email, token=confirmation_token)
    return {
        "result": True,
        "msg": "Ti abbiamo inviato un'altra email di conferma!"
    }


@router.post("/delete", tags=["auth"])
async def delete_function(data: deleteAccountSchema = Body(...)):
    username = get_username(jwtoken=data.token)
    id_user = get_id_user(jwtoken=data.token)
    user = UserLoginSchema(username=username, password=data.pw)
    res =  tryLogin(user)
    if res:
        if deleteAccount(id_user=id_user):
            return {
                "result": True
            }
        else:
            return {
                "result": False,
                "error": "Qualcosa è andato storto nell'eliminazione dell'account"
            }
    return {
        "result": False,
        "error": "Credenziali non valide, riprova"
    }
