from typing import Dict
import jwt
import time

JWT_SECRET_NOTIFICATION = "chiavepercomunicazioneserverserver"
JWT_ALGORITHM = "HS256"


def newToken():
    try:
        payload = {
            "app": "myappanotification_system",
            "expires": time.time() + 6000
        }
        token = jwt.encode(payload, JWT_SECRET_NOTIFICATION, algorithm=JWT_ALGORITHM)
        myf = open('../../env/token.txt', 'w')
        myf.write(token)
        myf.close()
        return True
    except:
        return False

"""
if newToken():
    print('token generato correttamente')
else:
    print('errore nella generazione del token')
"""