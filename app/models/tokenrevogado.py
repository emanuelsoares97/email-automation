from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.models.abstrata import BaseModel

class TokenRevogado(BaseModel):
    __tablename__ = "tokens_revogados"

    id = Column(Integer, primary_key=True)
    token_jti = Column(String, nullable=False, unique=True)  # ID único do token
    criado_em = Column(DateTime,  default=lambda: datetime.now(timezone.utc))