from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from app.models.abstrata import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Contact(BaseModel):

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('utilizadores.id'), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=True)


     # Definição dos relacionamentos
    utilizador= relationship("Utilizador", backref="contacts")
