from fastapi import APIRouter, Body, Depends
from .utils_functions.models import (
    TokenLoginSchema, messageOBJ, NewChatOBJ
)
from ..auth.auth_bearer import JWTBearer

from .utils_functions.createid import createID
from ..auth.auth_handler import get_username, get_id_user

from .utils_functions.crud import (getChats, getMessages, 
    storeMessage, get_id_user_from_username, get_relation,
    createChat, check_chat_exists, checkUserInChat, blockUser
    )

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
from os import getenv
from dotenv import load_dotenv

load_dotenv()
# Chiave di cifratura
key = getenv("KEY")
key = hashlib.sha256(key.encode()).digest()[:32]

# Funzione per cifrare un messaggio
def encrypt_message(message):
    # Inizializza il cifrario
    cipher = AES.new(key, AES.MODE_CBC)
    # Cifra il messaggio con il padding
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    # Ritorna il vettore di inizializzazione concatenato con il testo cifrato
    return cipher.iv + ciphertext

# Funzione per decifrare un messaggio cifrato
def decrypt_message(ciphertext):
    # Estrae il vettore di inizializzazione e il testo cifrato
    iv, ciphertext = ciphertext[:AES.block_size], ciphertext[AES.block_size:]
    # Inizializza il cifrario
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # Decifra il messaggio con l'unpadding
    message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # Ritorna il testo decifrato come stringa
    return message.decode('utf-8')

router = APIRouter()


@router.post("/direct", dependencies=[Depends(JWTBearer())])
async def direct_function(token: TokenLoginSchema = Body(...)):
    id_user = get_id_user(jwtoken=token.token)
    return {
        "result": True,
        "chats": getChats(id_user=id_user)
    }

@router.post("/get/{id_chat}", dependencies=[Depends(JWTBearer())])
async def chat_function(id_chat: str, token: TokenLoginSchema):
    id_user = get_id_user(jwtoken=token.token)
    if checkUserInChat(id_user=id_user, id_chat=id_chat):
        res = getMessages(id_chat=id_chat)
        for el in res:
            el['content'] = decrypt_message(el['content'])
        return {
            "result": True,
            "data": res
        }
    else:
        #blockUser(id_user=id_user)
        return {
            "result": False,
            "error": "Violazione individuata"
        }

@router.post("/new_message")
async def newMessage_function(message: messageOBJ):
    message.content = encrypt_message(message=message.content)
    if storeMessage(message):
        return {
            "result": True
        }
    return {
        "result": False
    }

@router.post("/new", dependencies=[Depends(JWTBearer())])
async def createChat_function(newChatOBJ: NewChatOBJ = Body(...)):
    id_user_sender = get_id_user(jwtoken=newChatOBJ.token)
    id_user_recipient = get_id_user_from_username(username=newChatOBJ.username)
    
    chat_exist = check_chat_exists(id_user_1=id_user_sender, id_user_2=id_user_recipient)
    if chat_exist[0]:
        return {
            "result": True,
            "chat": chat_exist[1]
        }
    relation = get_relation(id_user_sender=id_user_sender, id_user_recipient=id_user_recipient)
    if relation == 2:
        new = createChat(id_user_first=id_user_sender, id_user_second=id_user_recipient)
        if new:
            chat = check_chat_exists(id_user_1=id_user_sender, id_user_2=id_user_recipient)[1]
            return{
                "result": True,
                "chat": chat
            }
        else:
            return {
                "return": False,
                "error": "Qualcosa è andato storto"
            }
    blockUser(id_user=id_user_sender)
    return {
        "return": False,
        "error": "violazione individuata"
    }


    