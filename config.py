import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuração base da aplicação"""
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    SECRET_KEY = os.environ.get("SECRET_KEY", "sua_chave_secreta")

    # Garante fallback se estiver ausente ou vazio
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_db_path = os.path.join(base_dir, "db", "database.db")
    default_db_uri = f"sqlite:///{default_db_path}"

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or default_db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações do Flask-Mail
    MAIL_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("SMTP_PORT", 465))  # 465 para SSL, 587 para TLS
    MAIL_USE_SSL = bool(os.environ.get("MAIL_USE_SSL", True))  # Usar SSL por padrão
    MAIL_USERNAME = os.environ.get("EMAIL")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("EMAIL_NAME", "Seu Nome de Remetente")



class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
