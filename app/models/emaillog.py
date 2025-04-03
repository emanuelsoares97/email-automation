from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.abstrata import BaseModel
from datetime import datetime, timezone

class EmailLog(BaseModel):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('utilizadores.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=False)
    status = Column(String(50), nullable=False)  # Success, Failed, Pending
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Definição dos relacionamentos
    utilizador = relationship("Utilizador", backref="email_logs")
    contacto = relationship("Contact", backref="email_logs")
    template = relationship("Template", backref="email_logs")
