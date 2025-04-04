from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.models.abstrata import BaseModel

class TokenRevogado(BaseModel):
    __tablename__ = "tokens_revogados"

    id = Column(Integer, primary_key=True)
    token_jti = Column(String, nullable=False, unique=True)  # ID único do token
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TokenRevogado(id={self.id}, token_jti={self.token_jti}, criado_em={self.criado_em})>"
