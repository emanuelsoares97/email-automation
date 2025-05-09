from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from datetime import datetime, timezone
from app.models.abstract import BaseModel

class BlacklistedToken(BaseModel):
    __tablename__ = "black_listed_token"

    __table_args__ = (
    UniqueConstraint("token_jti", name="uq_tokensrevogados_token_jti"),
) # ID único do token


    id = Column(Integer, primary_key=True)
    token_jti = Column(String, nullable=False)  
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<TokenRevogado(id={self.id}, token_jti={self.token_jti}, criado_em={self.criado_em})>"
