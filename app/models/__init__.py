import os
import importlib
from app.database.database import db

def register_models():
    models_dir = os.path.dirname(__file__)  # Obtém o diretório onde o arquivo atual está (app/models)
    for filename in os.listdir(models_dir):
        # Verifica se é um arquivo Python (e não o __init__.py)
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"app.models.{filename[:-3]}"  # Remove a extensão .py e gera o nome do módulo
            importlib.import_module(module_name)  # Importa o módulo
    db.create_all()  # Cria as tabelas após o registro
