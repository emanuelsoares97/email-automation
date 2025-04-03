from app.database.database import db
from app.models.tokenrevogado import TokenRevogado
from app.utils.logger_util import get_logger

logger= get_logger(__name__)

class TokenService:
    """Gerencia a blacklist de tokens JWT"""

    

    @staticmethod
    def adicionar_token_na_blacklist(token_jti):
        """Adiciona um token revogado ao banco de dados"""
        token_revogado = TokenRevogado(token_jti=token_jti)
        logger.info(f"Token revogado: {token_revogado}")

        db.session.add(token_revogado)
        db.session.commit()

    @staticmethod
    def esta_na_blacklist(token_jti):
        """Verifica se um token está na blacklist"""
        
        return db.session.query(TokenRevogado).filter_by(token_jti=token_jti).first() is not None