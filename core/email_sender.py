import os
from email.message import EmailMessage
from core.template_loader import load_template
import smtplib
from dotenv import load_dotenv
from utils.logger_util import get_logger

logger= get_logger(__name__)

def send_email(destinatario, nome=None, file=None, tipo=None):
    try:
        load_dotenv()
        email = os.environ.get("EMAIL")
        password = os.environ.get("EMAIL_PASSWORD")

        msg = EmailMessage()
        msg["Subject"] = "Mensagem Automática"
        msg["From"] = email
        msg["To"] = destinatario
        msg.set_content("Versão alternativa em texto simples.")

        if tipo:
            # Carrega o HTML com base no tipo de e-mail (do CSV)
            html = load_template(f"{tipo}.html", nome)
            msg.add_alternative(html, subtype="html")
        else:
            logger.warning("Tentativa de enviar email sem tipo")
            raise ValueError("Todos os emails têm de ter um tipo")

        # Se tiver anexo, adiciona usando caminho automático da pasta 'pdfs'
        if file:
            pdf_path = os.path.join('pdfs', file)
            with open(pdf_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(f.name)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
            logger.info(f"Anexo adicionado: {file}")

        # 3️⃣ Envia o e-mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
    
    except Exception as e:
        logger.error(f"Tentativa de enviar email, erro: {e}")
        raise f"Erro ao enviar email: {e}"