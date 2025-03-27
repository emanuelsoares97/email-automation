from dotenv import load_dotenv
import os
from email.message import EmailMessage
import smtplib
import filetype



def send_email(destinatario, nome=None, file=None):
    load_dotenv()  # carrega variáveis do .env
    email = os.environ.get("EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    msg= EmailMessage()
    msg["Subject"] = "grafico"
    msg["From"]= email
    msg["To"]= destinatario
    msg.set_content("somos uma familia bonita")

    if file:
        with open(file, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(f.name)

        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    msg.add_alternative(f"""
        <!DOCTYPE html>
        <html>

        <body>
            <h1 style="color: blue;"> Olá {nome}</h1>
        </body>
        </html>   
        """, subtype="html")

    #fazer o login ao servidor do email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

        smtp.login(email, password)

        smtp.send_message(msg)