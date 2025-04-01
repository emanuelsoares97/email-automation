from flask import Blueprint, request, jsonify
from app.services.utilizador_service import UtilizadorService
from app.utils.logger_util import get_logger
from app.services.auth_service import AuthService
from utils.validacao import validar_email


logger = get_logger(__name__)

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    """Validar login"""
    try:
        logger.debug("Rota /api/auth/login chamada.")

        if not request.is_json:
            logger.info("Formato recebido incorreto, não é JSON")
            return jsonify({"erro": "Formato inválido, envia em JSON"}), 400
        
        data = request.get_json()

        logger.info(f"Dado recebidos: {data}")

        if not data or "email" not in data or "password" not in data:
            logger.warning(f"Tentativa de login sem credenciais.")
            return jsonify({"erro": "Email e password são obrigatorios."}), 400
        
        if not validar_email(data.get("email")):
            logger.warning("Tenativa de login de email invalido.")
            return jsonify({"erro": "Email inválido"}), 400
        
        utilizador= UtilizadorService.autenticar(data.get("email"), data.get("password"))

        if not utilizador:
            logger.warning(f"Falha na autenticação para o email: {data.get('email')}")
            return jsonify({"erro": "Credenciais inválidas"}), 403
        
        if not utilizador.ativo:
            logger.warning(f"Tentativa de login de utilizador inativo: {utilizador.email}")
            return jsonify({"erro": "Conta inativa. Entrar em contacto com o suporte."}), 403
        
        access_token, refresh_token = AuthService.gerar_tokens(utilizador)

        logger.info(f"Utilizador autenticado: {utilizador.email}")

        return jsonify({
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
            "utilizador": {
                "id": utilizador.id,
                "email": utilizador.email,
                "role": utilizador.role
            }


        }), 200

    except Exception as e:
        logger.error(f"Erro inesperado no login: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500
        
        
