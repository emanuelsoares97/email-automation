from flask import Flask
from app.routes.api import auth, utilizador
def init_routes(app: Flask):
    """Registra todos os Blueprints da aplicação"""
    blueprints = [
        
        (auth.auth_bp, "/api/auth"),
        (utilizador.utilizador_bp, "/api/utilizador")
        
    ]
    for bp, prefix in blueprints:
        app.register_blueprint(bp, url_prefix=prefix)  # Registra cada um dinamicamente