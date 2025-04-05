from flask import Flask
from app.routes.api import auth, contacts, sendemail, template, utilizador
from app.utils.logger_util import get_logger

logger = get_logger(__name__)

def init_routes(app: Flask):
    """Regista todos os Blueprints da aplicação.

    Cada blueprint é registrado com um prefixo de URL específico.
    """
    
    # Lista de tuplas contendo o blueprint e seu prefixo
    blueprints = [
        (auth.auth_bp, "/api/auth"),
        (contacts.contact_bp, "/api/contact"),
        (sendemail.sendemail_bp, "/api/sendemail"),
        (template.template_bp, "/api/template"),
        (utilizador.utilizador_bp, "/api/utilizador")
    ]
    
    # Registro de cada blueprint na aplicação Flask
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)  # Registo dinâmico
        logger.info(f"Blueprint {bp.name} registrado com prefixo {prefix}")