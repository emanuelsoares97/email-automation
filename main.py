from utils.logger_util import get_logger
from core.email_sender import send_email
from utils.readcsv import read_contacts
from utils.caminhos import caminho_csv_colaboradores


logger= get_logger(__name__)

def main():
    
    contactos=read_contacts(caminho_csv_colaboradores)

    for contacto in contactos:
        nome = contacto["nome"]
        email= contacto["email"]
        anexo = contacto["anexo"]
        tipo= contacto["tipo"]
    
        try:
            send_email(destinatario=email, nome=nome, file=anexo, tipo=tipo)
            logger.info(f"Email enviado com sucesso para {nome} <{email}>")

        except Exception as e:
            logger.error(f"Erro ao envio email para: {nome} <{email}>: {e}")

if __name__=="__main__":
    main()