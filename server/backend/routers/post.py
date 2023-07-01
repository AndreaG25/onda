from fastapi import APIRouter, Body, Depends
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import get_username, get_id_user
from .utils_functions.models import (PostSchema, TokenLoginSchema, 
ChangePublicFlag, DeletePost, EditPostSchema)
from .utils_functions.createid import createID
from .utils_functions.crud import (
    newPost, get_relation, get_id_user_from_post, get_post_info, editPublic, deletePost,
    blockUser, getPost4Edit, editPost
)

router = APIRouter()



@router.post("/new", dependencies=[Depends(JWTBearer())])
async def newPost_function(newPostObj: PostSchema = Body(...)):
    id_user = get_id_user(newPostObj.token)
    id_post = createID("post")
    if newPost(id_user=id_user, id_post=id_post, post=newPostObj):
        return {
            "result": True
        }
    return {
        "result": False,
        "error": "Qualcosa è andato storto nell'inserimento del post"
    }


@router.post("/change_public_flag", dependencies=[Depends(JWTBearer())])
async def editPublic_function(editPublicObj: ChangePublicFlag = Body(...)):
    id_user = get_id_user(editPublicObj.token)
    if id_user == get_id_user_from_post(editPublicObj.id_post):
        return {
            "result": editPublic(id_post=editPublicObj.id_post, action=editPublicObj.action)
        }
    blockUser(id_user=id_user)
    return {
        "result": False,
        "error": "Violazione individuata"
    }

@router.post("/get/{id_post}", dependencies=[Depends(JWTBearer())])
async def getPost_function(id_post: str, token: TokenLoginSchema  = Body(...)):
    id_user_sender = get_id_user(token.token)
    id_user_author = get_id_user_from_post(id_post=id_post)
    if not id_user_author:
        return {
            "result": False,
            "error": "Il post che hai cercato non esiste"
        }
    rel = get_relation(id_user_recipient=id_user_author, id_user_sender=id_user_sender)
    if rel != 2 and rel != 3 and rel != 10:
        return {
            "result": False,
            "error": f"Non sei autorizzato a vedere questo post, effettua la richiesta per vedere il post"
        }
    return {
        "result": True,
        "data": get_post_info(id_post=id_post, id_user=id_user_sender, rel=rel)
    }


@router.post("/delete", dependencies=[Depends(JWTBearer())])
async def deletePost_function(deletePostObj: DeletePost = Body(...)):
    id_user = get_id_user(deletePostObj.token)
    if id_user == get_id_user_from_post(deletePostObj.id_post):
        return {
            "result": deletePost(id_post=deletePostObj.id_post)
        }
    blockUser(id_user=id_user)
    return {
        "result": False,
        "error": "Violazione individuata"
    }

@router.post("/post4edit", dependencies=[Depends(JWTBearer())])
async def post4edit_function(deletePostObj: DeletePost = Body(...)):
    id_user = get_id_user(deletePostObj.token)
    print(f"ID_USER: {id_user}")
    print(f"ID_POST: {deletePostObj.id_post}")
    print(f"Autore del post: {get_id_user_from_post(deletePostObj.id_post)}")
    id_user_author = get_id_user_from_post(deletePostObj.id_post)
    if not id_user_author:
        return {
            "result": False,
            "error": "Il post non esiste"
        }
    if id_user_author and (id_user_author != id_user):
        blockUser(id_user=id_user)
        return {
            "result": False,
            "error": "Violazione individuata"
        }
    if id_user_author == id_user:
        return {
            "result": True,
            "data": getPost4Edit(id_post=deletePostObj.id_post)
        }
    else:
        return {
            "result": False,
            "error": "Errore nel caricamento dei dati"
        }

@router.post("/edit", dependencies=[Depends(JWTBearer())])
async def edit_function(editPostObj: EditPostSchema = Body(...)):
    id_user = get_id_user(editPostObj.token)
    id_user_author = get_id_user_from_post(editPostObj.id_post)
    if not id_user_author:
        return {
            "result": False,
            "error": "Il post non esiste"
        }
    if id_user_author and (id_user_author != id_user):
        blockUser(id_user=id_user)
        return {
            "result": False,
            "error": "Violazione individuata"
        }
    if id_user_author == id_user:
        return {
            "result": editPost(post=editPostObj)
        }
    else:
        return {
            "result": False,
            "error": "Errore nel caricamento dei dati"
        }
    
    