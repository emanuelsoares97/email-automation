import os
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis do .env

class Config:
    """Configuração padrão para a aplicação"""
    DEBUG = os.environ.get("DEBUG", "False") == "True"
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db', 'database.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
