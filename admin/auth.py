import time
from typing import Dict
from datetime import timedelta, datetime
import jwt
import pytz
from os import getenv
from dotenv import load_dotenv

load_dotenv()
timezone = pytz.timezone('Europe/Rome')




JWT_SECRET = getenv("SECRET")
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "result": True,
        "access_token": token
    }


def signJWT(username: str, id_admin: str) -> Dict[str, str]:
    expires = datetime.now(timezone) + timedelta(minutes=15)
    payload = {
        "app": "myappagtwitter",
        "admin": username,
        "id_admin": id_admin,
        "expires": expires.timestamp()
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



def get_id_admin(jwtoken: str) -> str:
    try:
        payload = decodeJWT(jwtoken)
        id_user = payload['id_admin']
    except:
        id_user = None
    return id_user


