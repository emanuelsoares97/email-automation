from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from app.models.abstrata import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Area(BaseModel):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Relação de volta para a organização
    organization = relationship(
        "Organization",
        back_populates="areas"
    )

    # Relação para os contactos desta área
    contacts = relationship(
        "Contact",
        back_populates="area",
        lazy="dynamic"
    )

    # Relação para os utilizadores desta área
    users = relationship(
        "Utilizador",
        back_populates="area",
        lazy="dynamic"
    )
 