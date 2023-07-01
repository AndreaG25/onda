import os
import requests

"""
def getToken():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir, os.pardir))
    file_path = os.path.join(parent_dir, 'env', 'token.txt')
    myf = open(file_path, 'r')
    token = myf.readline().strip()
    myf.close()
    return token
"""
def newNotification_comment(sender: str, recipient: str, id_post: str):
    pass
"""
    comment = {"sender": sender, "recipient": recipient, "id_post": id_post, "token": getToken()}
    response = requests.post("http://localhost:6500/newcomment", json=comment)
    if response.json().get('result') == True:
        print('notifica inviata con successo')
    else:
        if response.json().get('code') == 1:
            print('utente non connesso')
        elif response.json().get('code') == 2:
            print('il token è scaduto')
"""
def newNotification_follow(sender: str, recipient: str):
    pass
    """
    follow = {"sender": sender, "recipient": recipient, "token": getToken()}
    response = requests.post("http://localhost:6500/newfollow", json=follow)
    if response.json().get('result') == True:
        print('notifica inviata con successo')
    else:
        if response.json().get('code') == 1:
            print('utente non connesso')
        elif response.json().get('code') == 2:
            print('il token è scaduto')
"""

