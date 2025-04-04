from app.database.database import db
from app.models.tokenrevogado import TokenRevogado
from app.utils.logger_util import get_logger

logger = get_logger(__name__)

class TokenService:
    """Gerencia a blacklist de tokens JWT"""

    @staticmethod
    def adicionar_token_na_blacklist(token_jti):
        """Adiciona um token revogado ao banco de dados"""
        try:
            # Adiciona o token à blacklist
            token_revogado = TokenRevogado(token_jti=token_jti)
            db.session.add(token_revogado)
            db.session.commit()
            logger.info(f"Token revogado adicionado com sucesso: {token_jti}")

        except Exception as e:
            # Em caso de erro no banco de dados, realiza rollback e log o erro
            db.session.rollback()
            logger.error(f"Erro ao adicionar token na blacklist: {e}")
            raise Exception(f"Erro ao adicionar token na blacklist: {e}")

    @staticmethod
    def esta_na_blacklist(token_jti):
        """Verifica se um token está na blacklist"""
        try:
            # Verifica se o token está na blacklist
            return db.session.query(TokenRevogado).filter_by(token_jti=token_jti).first() is not None
        
        except Exception as e:
            logger.error(f"Erro ao verificar token na blacklist: {e}")
            return False
