from flask_mail import Message
from flask import render_template, current_app as app
from flask_mail import Mail
import os

class EmailSenderService:
    def __init__(self):
        self.mail = Mail(app)  # Inicializa o serviço de e-mail com a configuração do Flask-Mail
    
    def send_email(self, destinatario, nome=None, tipo=None, file=None):
        """Função para enviar e-mail"""
        msg = Message("Assunto do E-mail", recipients=[destinatario])
        msg.body = "Versão alternativa em texto simples."

        # Carrega o template HTML baseado no tipo (por exemplo, tipo = 'boas_vindas')
        if tipo:
            html_content = render_template(f"{tipo}.html", nome=nome)
            msg.html = html_content
        else:
            raise ValueError("Todos os emails têm de ter um tipo")

        # Se tiver anexo, adiciona usando caminho automático da pasta 'pdfs'
        if file:
            pdf_path = os.path.join('pdfs', file)
            with open(pdf_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(f.name)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

        try:
            # Envia o e-mail
            self.mail.send(msg)
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
            raise ValueError(f"Erro ao enviar email: {e}")
