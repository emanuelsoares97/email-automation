from flask import Blueprint, request, jsonify, make_response, g
from app.services.utilizador_service import UtilizadorService
from app.services.tokenrevogado_manager import TokenService
from app.utils.logger_util import get_logger
from app.services.auth_service import AuthService
from app.utils.validacao import validar_email
import jwt
from collections import namedtuple
from config import Config


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
        
        
@auth_bp.route("/auth", methods=["GET"])
@AuthService.token_required
def auth():
    """Rota protegida que verifica se o token é válido"""
    try:
        logger.info("Token validado com sucesso!")
        return jsonify({"mensagem": "Token válido, utilizador autenticado!"})

    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}", exc_info=True)
        return make_response(jsonify({"erro": "Erro interno no servidor"}), 500)

@auth_bp.route("/logout", methods=["POST"])
@AuthService.token_required  # Já valida o token automaticamente
def logout():
    """Revoga o access token do utilizador"""
    try:
        token = request.headers.get("Authorization").replace("Bearer ", "")

        # O token já foi validado pelo @AuthService.token_required, então podemos pegar o JTI
        TokenService.adicionar_token_na_blacklist(g.current_user["jti"])
        
        logger.info("Logout com sucesso")
        return jsonify({"mensagem": "Logout bem-sucedido!"}), 200
    
    except Exception as e:
        logger.error(f"Erro ao validar token: {str(e)}", exc_info=True)
        return jsonify({"mensagem": "Token em falta para logout"}), 401

@auth_bp.route("/refresh", methods=["POST"])
def refresh_token():
    """Renova o access token usando o refresh token"""
    token = request.headers.get("Authorization")  # Pega o token enviado pelo cliente

    if not token:
        logger.warning("Tentativa de refresh sem token")
        return jsonify({"erro": "Refresh token é obrigatório!"}), 401

    token = token.replace("Bearer ", "")  # Remove "Bearer " se estiver presente

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        
        Utilizador = namedtuple("Utilizador", ["id", "nome", "email", "role"])
        utilizador_obj = Utilizador(id=payload["id"], nome=payload.get("nome", ""), email="", role="")

        novo_access_token, _ = AuthService.gerar_tokens(utilizador_obj)

        return jsonify({"access_token": novo_access_token}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Refresh token expirado. Faça login novamente!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Refresh token inválido!"}), 401