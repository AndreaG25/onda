from fastapi import FastAPI
from backend.routers import (post, users, change, auth,
 relation, comments, like, search, chat, support, home
)
#from fastapi.middleware.cors import CORSMiddleware
#from .auth.auth_handler import signJWT, validate_token, getUsernameFromToken
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


origins = ["*"]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]

app = FastAPI(middleware=middleware)
app.include_router(
    users.router,
    prefix="/user",
    tags=["users"]
)
app.include_router(
    post.router, 
    prefix="/post",
    tags=["post"]
)
app.include_router(
    change.router, 
    prefix="/change",
    tags=["change"]
)

app.include_router(
    auth.router, 
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    relation.router, 
    prefix="/relation",
    tags=["relation"]
)

app.include_router(
    comments.router, 
    prefix="/comments",
    tags=["comments"]
)


app.include_router(
    like.router, 
    prefix="/like",
    tags=["like"]
)

app.include_router(
    search.router, 
    prefix="/search",
    tags=["search"]
)

app.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
)

app.include_router(
    support.router,
    prefix="/support",
    tags=["support"]
)

app.include_router(
    home.router,
    prefix="/home",
    tags=["home"]
)



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

