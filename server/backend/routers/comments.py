from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import get_username, get_id_user
from .utils_functions.models import newCommentSchema
from .utils_functions.createid import createID
from .utils_functions.crud import newComment, canUserComment, get_id_user_from_post
from .utils_functions.new_not import newNotification_comment
router = APIRouter()



@router.post("/new", dependencies=[Depends(JWTBearer())])
async def newComments_function(newCommentObj: newCommentSchema = Body(...)):
    id_user = get_id_user(newCommentObj.token)
    id_comment = createID("comment")
    res = canUserComment(id_post=newCommentObj.id_post, id_user=id_user)
    if res[0]:
        if newComment(id_comment=id_comment, id_user=id_user, commentObj=newCommentObj) and id_user != None:
            newNotification_comment(sender=get_username(jwtoken=newCommentObj.token), recipient=get_id_user_from_post(newCommentObj.id_post), id_post=newCommentObj.id_post)
            return {
                "result": True
            }
        return {
            "result": False,
            "error": "Qualcosa è andato storto nell'inserimento del commento"
        }
    return {
        "result": False,
        "error": res[1]
    }

