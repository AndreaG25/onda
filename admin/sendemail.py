from pydantic import BaseModel
from email.message import EmailMessage
import ssl
import smtplib
from os import getenv
from crud import get_users_4_notification
from dotenv import load_dotenv

load_dotenv()
email_sender = "agapps.email.test@gmail.com"
EMAIL_PASSWORD = getenv("PW_EMAIL")

context = ssl.create_default_context()

class AnswerTicket(BaseModel):
    id_ticket: str
    res: str

class InfoTicket(BaseModel):
    subject: str
    fullname: str
    email: str
    category: int




async def send_answer_email(answerTicketOBJ: AnswerTicket, infoTicket: InfoTicket):
    email_receiver = infoTicket.email
    subject = f'Risposta a {infoTicket.subject}'
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
            <h1>Gentile {infoTicket.fullname},</h1>
            <p>La ringraziamo per averci scritto. Di seguito troverà la sua risposta:</p>
            <p>{answerTicketOBJ.res}</p>
            <hr>
            <div class="ticket-info">
                <span>N. Ticket:</span> {answerTicketOBJ.id_ticket}<br>
                <span>Email generata, per rispondere copia il numero del ticket e invia un'altra richiesta di supporto</span>
            </div>
        </div>
    </body>
    </html>
"""
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = infoTicket.email
    em['subject'] = subject
    em.set_content(body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, EMAIL_PASSWORD)
        smtp.sendmail(email_sender, email_receiver, em.as_string())




async def send_notification_email(subject: str, content: str):
    mailList = get_users_4_notification()
    for user in mailList:
        email_receiver = user.get("email")
        subject = f'Risposta a {subject}'
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
                <h1>Gentile {user.get("fullname")},</h1>
                <p>{content}</p>
                <hr>
                <div class="ticket-info">
                    <span>Email generata, le risposte non verrano lette</span><br>
                    <span>Per non ricevere più questo tipo di mail, accedi la tuo account:<br> home > impostazioni > notifiche > email </span>
                </div>
            </div>
        </body>
        </html>
    """
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = user.get("email")
        em['subject'] = subject
        em.set_content(body, subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, EMAIL_PASSWORD)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

