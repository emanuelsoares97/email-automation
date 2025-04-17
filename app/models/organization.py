from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.abstrata import BaseModel
from datetime import datetime, timezone

class Organization(BaseModel):

    __tablename__ = "organization"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)

    utilizador = relationship("Utilizador", backref="organization", lazy=True)
