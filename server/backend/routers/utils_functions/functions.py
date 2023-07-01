from .models import UserSchema
from .crud import checkUsername, checkEmail

def checkUserInformation(user: UserSchema):
    if not checkUsername(user.username):
        return {
            "result": False,
            "error": "Lo username è già utilizzato"
        }
    elif not checkEmail(user.email):
        return {
            "result": False,
            "error": "La mail è già utilizzata"
        }
    else:
        return {
            "result": True
        }

