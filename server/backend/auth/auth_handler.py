import time
from datetime import timedelta, datetime
from typing import Dict
from os import getenv
import jwt
from dotenv import load_dotenv
import pytz
timezone = pytz.timezone('Europe/Rome')

load_dotenv()

JWT_SECRET = getenv("SECRET")
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return {
        "result": True,
        "access_token": token
    }


def signJWT(username: str, id_user: str) -> Dict[str, str]:
    current_time = datetime.now(timezone)
    expires = int((current_time + timedelta(days=14)).timestamp())
    payload = {
        "app": "onda_ag_app_socialmedia",
        "username": username,
        "id_user": id_user,
        "expires": expires
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    

def validate_token(token):
    isTokenValid: bool = False
    try:
        payload = decodeJWT(token)
    except:
        payload = None
    if payload:
        isTokenValid = True
    return isTokenValid

 
def get_username(jwtoken: str) -> str:
    try:
        payload = decodeJWT(jwtoken)
        id_user = payload['username']
    except:
        id_user = None
    return id_user

def get_id_user(jwtoken: str) -> str:
    try:
        payload = decodeJWT(jwtoken)
        id_user = payload['id_user']
    except:
        id_user = None
    return id_user

