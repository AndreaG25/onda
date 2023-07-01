from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import jwt
from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
import pytz
from os import getenv
timezone = pytz.timezone('Europe/Rome')


load_dotenv()
SECRET = getenv("EMAIL_SECRET")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

email_sender = "agapps.email.test@gmail.com"


context = ssl.create_default_context()



class TokenData(BaseModel):
    email: str
    id_user: str
    exp: Optional[int] = None

class TokenCPWData(BaseModel):
    email: str
    exp: Optional[int] = None

def create_confirmation_token(email: str, id_user: str) -> str:
    current_time = datetime.now(timezone)
    exp_time = int((current_time + timedelta(days=1)).timestamp())
    data = TokenData(email=email, id_user=id_user, exp=exp_time)
    token = jwt.encode(data.dict(), SECRET, algorithm="HS256")

    return token

def validate_confirmation_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        token_data = TokenData(**payload)
        id_user = token_data.id_user    
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        return [False]
    return [True, id_user]


#da sviluppare
def create_changePW_token(email: str):
    current_time = datetime.now(timezone)
    exp_time = int((current_time + timedelta(minutes=30)).timestamp())
    data = TokenCPWData(email=email, exp=exp_time)
    token = jwt.encode(data.dict(), SECRET, algorithm="HS256")

    return token

def validate_changePW_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        print(payload)
        token_data = TokenCPWData(**payload)
        email = token_data.email
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as error:
        print(error)
        return [False]
    return [True, email]

async def send_confirmation_email(email: str, token: str):
    email_receiver = email
    subject = "Conferma registrazione!"
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                padding: 20px;
            }}
            .container {{
                background-color: #fff;
                border-radius: 4px;
                padding: 20px;
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            p {{
                color: #555;
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 10px;
            }}
            .ticket-info {{
                font-weight: bold;
                margin-top: 30px;
            }}
            .ticket-info span {{
                color: #888;
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Conferma Account</h1>
            <p>Clicca sul seguente link per confermare la creazione del tuo account:</p>
            <p><a href="http://localhost:5000/frontend/html/confirm.html?token={token}">Conferma Account</a></p>
            <p>Se il link non funziona, copia e incolla l'URL nel tuo browser:</p>
            <p>http://localhost:5000/frontend/html/confirm.html?token={token}</p>
            <div class="footer">
                <p>Questo è un messaggio generato automaticamente. Per favore, non rispondere a questa email.</p>
                <p>Se hai domande o bisogno di assistenza, <a href="http://localhost:5000/frontend/html/assistance.html">contattaci</a>.</p>
            </div>
        </div>
    </body>
    </html>
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['subject'] = subject
    em.set_content(body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, EMAIL_PASSWORD)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

async def send_changepw_email(email: str, token: str):
    email_receiver = email
    subject = "Cambia la password"
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                padding: 20px;
            }}
            .container {{
                background-color: #fff;
                border-radius: 4px;
                padding: 20px;
            }}
            h1 {{
                color: #333;
                font-size: 24px;
                margin-bottom: 20px;
            }}
            p {{
                color: #555;
                font-size: 16px;
                line-height: 1.5;
                margin-bottom: 10px;
            }}
            .ticket-info {{
                font-weight: bold;
                margin-top: 30px;
            }}
            .ticket-info span {{
                color: #888;
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Cambio della password</h1>
            <p>Clicca sul seguente link per cambiare la password del account:</p>
            <p><a href="http://localhost:5000/frontend/html/change_pw_page.html?token={token}">Cambia password!</a></p>
            <p>Se il link non funziona, copia e incolla l'URL nel tuo browser:</p>
            <p>http://localhost:5000/frontend/html/change_pw_page.html?token={token}</p>
            <p>NON CONDIVIDERE QUESTO LINK CON NESSUNO</p>
            <div class="footer">
                <p>Questo è un messaggio generato automaticamente. Per favore, non rispondere a questa email.</p>
                <p>Se hai domande o bisogno di assistenza, <a href="http://localhost:5000/frontend/html/assistance.html">contattaci</a>.</p>
            </div>
        </div>
    </body>
    </html>
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['subject'] = subject
    em.set_content(body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, EMAIL_PASSWORD)
        smtp.sendmail(email_sender, email_receiver, em.as_string())






