import os
import importlib
from app.database.database import db

def register_models():
    models_dir = os.path.dirname(__file__)
    
    for filename in os.listdir(models_dir):
        
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"app.models.{filename[:-3]}"  
            importlib.import_module(module_name)  

    db.create_all()  # Cria as tabelas após o registro
