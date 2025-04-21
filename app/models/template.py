from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from app.models.abstrata import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Template(BaseModel):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('utilizadores.id'), nullable=True)  # Pode ser NULL para templates gerais
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now())
    is_global = Column(Boolean, default=False)  # Indica se o template é geral

    
    user_id  = Column(Integer, ForeignKey("utilizadores.id"), nullable=True)

    utilizador = relationship("Utilizador", back_populates="templates")


    def __repr__(self):
        return f"<Template {self.name} - {self.subject}>"