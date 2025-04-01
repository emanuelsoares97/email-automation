# config.py

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





class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
