import jwt
import uuid  #uuid para gerar identificadores únicos
from flask import request, jsonify, g 
from functools import wraps
from config import Config
from datetime import datetime, timezone, timedelta
from app.services.tokenrevogado_manager import TokenService
from app.utils.logger_util import get_logger

logger= get_logger(__name__)

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
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=15)  # Expira em 15 min
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )

            refresh_token = jwt.encode(
                {
                    "id": utilizador.id,  # Agora acessamos como objeto
                    "jti": jti_refresh,  # Adicionamos `jti` ao refresh token
                    "exp": datetime.now(timezone.utc) + timedelta(days=7)  # Expira em 7 dias
                },
                Config.SECRET_KEY,
                algorithm="HS256"
            )

            logger.info("Token gerado com sucesso.")
            return access_token, refresh_token
        
            

        except Exception as e:
            logger.error(f"Tentativa de gerar token, erro: {str(e)}")
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

            logger.debug("Token validado com sucesso.")
            return payload, None
        except jwt.ExpiredSignatureError:
            logger.warning("Tentativa de validar token expirado")
            return None, "Token expirado. Faça login novamente."
        except jwt.InvalidTokenError:
            logger.warning("Tentativa de válidar token inválido.")
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
                "email": payload["email"],
                "nome": payload["nome"],
                "role": payload["role"],
                "jti": payload["jti"]  # identificador único do token
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
                user_nome= g.current_user["nome"]

                if user_role not in required_roles:
                    logger.warning(f"Tentativa de alterar dados sem permissão, {user_nome}")
                    return jsonify({"Alerta": f"Acesso negado, utilizador '{user_role}' sem permissão!"}), 403
                return f(*args, **kwargs)
            return decorated_function
        return decorator