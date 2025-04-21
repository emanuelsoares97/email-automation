import jwt
import uuid
from flask import request, jsonify, g
from functools import wraps
from config import Config
from datetime import datetime, timezone, timedelta
from app.services.tokenrevogado_service import TokenService
from app.utils.logger_util import get_logger

logger = get_logger(__name__)

class AuthService:
    """Classe responsável por gerenciar autenticação JWT"""

    @staticmethod
    def gerar_tokens(utilizador):
        """Gera um access token (curto prazo) e um refresh token (longo prazo) com `jti`"""
        try:
            jti_access = str(uuid.uuid4())  # Identificador único para o access token
            jti_refresh = str(uuid.uuid4())  # Identificador único para o refresh token

            access_token = jwt.encode(
                {
                    "id": utilizador.id,
                    "nome": utilizador.nome,
                    "email": utilizador.email,
                    "role": utilizador.role,
                    "jti": jti_access,  # `jti` ao access token
                    "exp": datetime.now(timezone.utc) + timedelta(days=7)  # Expira em 15 min
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )

            refresh_token = jwt.encode(
                {
                    "id": utilizador.id,
                    "jti": jti_refresh,  # Adicionamos `jti` ao refresh token
                    "exp": datetime.now(timezone.utc) + timedelta(days=7)  # Expira em 7 dias
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )

            logger.info(f"Tokens gerados com sucesso para o usuário {utilizador.email}.")
            return access_token, refresh_token

        except Exception as e:
            logger.error(f"Erro ao gerar tokens: {str(e)}")
            return {"mensagem": f"erro ao tentar gerar token: {str(e)}"}

    @staticmethod
    def validar_token(token):
        """Valida e decodifica um token JWT"""
        if not token:
            return None, "Token em falta"

        if "Bearer " in token:
            token = token.replace("Bearer ", "")

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])

            # Verifica se o token está na blacklist
            if TokenService.esta_na_blacklist(payload["jti"]):
                return None, "Token inválido. Faça login novamente."

            logger.debug(f"Token {payload['jti']} validado com sucesso.")
            return payload, None

        except jwt.ExpiredSignatureError:
            logger.warning(f"Token expirado: {token}")
            return None, "Token expirado. Faça login novamente."
        except jwt.InvalidTokenError:
            logger.warning(f"Token inválido: {token}")
            return None, "Token inválido."

    @staticmethod
    def token_required(f):
        """Decorator que protege rotas exigindo um token válido"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            payload, error = AuthService.validar_token(token)

            if error:
                return jsonify({"Alerta": error}), 401

            g.current_user = {
                "email": payload.get("email"),  # get(), se "email" não existir, retorna None
                "nome": payload.get("nome"),   
                "role": payload.get("role"),    
                "jti": payload.get("jti"),
                "organization_id": payload.get("organization_id"),      
                "id": payload.get("id")         
            }

            return f(*args, **kwargs)

        return decorated

    @staticmethod
    def role_required(*required_roles):
        """Decorator que protege rotas exigindo uma role específica"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_role = g.current_user["role"]
                user_nome = g.current_user["nome"]

                if user_role not in required_roles:
                    logger.warning(f"Tentativa de alterar dados sem permissão, {user_nome}")
                    return jsonify({"Alerta": f"Acesso negado, utilizador '{user_role}' sem permissão!"}), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator
