import jwt
SECRET = "mykey"

def validate_jwt_token(token):
    try:
        # Verifichiamo la firma del token usando la chiave segreta
        decoded_token = jwt.decode(token, SECRET, algorithms=["HS256"])
        
        # Qui puoi inserire la logica per verificare eventuali altre proprietà del token
        # ad esempio, la data di scadenza o il ruolo dell'utente.
        # Se il token è valido, restituisci True
        return True
        
    except jwt.ExpiredSignatureError:
        # Se il token è scaduto, restituisci False
        print("Token scaduto.")
        return False
        
    except jwt.InvalidTokenError:
        # Se il token non è valido, restituisci False
        print("Token non valido.")
        return False

def getIdUser(token):
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=["HS256"])
        id_user = decoded_token['id_user']
    except:
        id_user = None
    return id_user