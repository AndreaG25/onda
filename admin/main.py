from fastapi import FastAPI, Body, Depends
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import timedelta
import bcrypt
from auth import signJWT, validate_token
from bearer import JWTBearer
from crud import (
    getUser, get_users_data,
    changeState, get_tickets,
    getInfoTicket, setTicket
)
from sendemail import send_answer_email, send_notification_email


origins = ["*"]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])
]
app = FastAPI(middleware=middleware)





class Login(BaseModel):
    username: str
    password: str

class TokenSchema(BaseModel):
    token: str

class EditUser(BaseModel):
    state: int
    id_user: str 

class AnswerTicket(BaseModel):
    id_ticket: str
    res: str

class InfoTicket(BaseModel):
    subject: str
    fullname: str

class NotificationSchema(BaseModel):
    subject: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello Admin"}


@app.get('/home', dependencies=[Depends(JWTBearer())]) 
def home_function():
    return {True}


@app.post('/validateadmintoken') 
def validateadmintoken_function(token: TokenSchema):
    return {
        "result": validate_token(token=token.token)
    }


@app.post('/answerTicket', dependencies=[Depends(JWTBearer())]) 
async def answerTicket_function(answerTicketOBJ: AnswerTicket):
    info = getInfoTicket(id_ticket=answerTicketOBJ.id_ticket)
    print(f'Informazioni: {info}')
    await send_answer_email(infoTicket=info, answerTicketOBJ=answerTicketOBJ)
    if setTicket(id_ticket=answerTicketOBJ.id_ticket):
        return {
            "result": True,
            "msg": "Risposta inviata"
        }
    return {
        "result": False,
        "error": "Qualcosa è andato storto"
    }

@app.get('/users', dependencies=[Depends(JWTBearer())]) 
async def users_function():
    return {
        "result": get_users_data()
    }

@app.get('/tickets', dependencies=[Depends(JWTBearer())]) 
async def users_function():
    return {
        "result": get_tickets()
    }



@app.post('/edituser', dependencies=[Depends(JWTBearer())])
async def editUser_function(data: EditUser):
    return {
        "result": changeState(data)
    }

@app.post('/login')
async def adminlogin_function(data: Login):
    user = getUser(username=data.username)
    if user:
        if verify_password(password=data.password, hashed_password=user[2]):
            return signJWT(username=data.username, id_admin=user[0])
    return {"result":"accesso negato"}

@app.post('/newemail', dependencies=[Depends(JWTBearer())])
async def se_function(emailGroupOBJ: NotificationSchema):
    await send_notification_email(subject=emailGroupOBJ.subject, content=emailGroupOBJ.content)
    return {
        "result":True
    }

def verify_password(password: str, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
