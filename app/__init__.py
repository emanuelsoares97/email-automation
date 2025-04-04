from flask import Flask
from flask_migrate import Migrate
from app.utils.logger_util import get_logger
from config import Config
from app.database.database import db
from app.routes import init_routes

logger = get_logger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    logger.info("Iniciando a app Flask.")
    logger.debug(f"Configurações carregadas {app.config}")

    db.init_app(app)

    # Configurando Flask-Migrate
    migrate = Migrate(app, db) #cuida da criaçao das tabelas

    with app.app_context():
        from app.models import register_models
        register_models()

    init_routes(app)

    return app


__all__ = ['create_app']
