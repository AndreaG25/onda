import string
import random

def createID(aim: str):
    chars = string.ascii_letters.lower() + string.digits
    random_string = ''.join(random.choices(chars, k=36))
    result = f"{aim}_{random_string}"
    return result