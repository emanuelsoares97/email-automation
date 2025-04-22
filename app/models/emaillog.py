from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.abstract import BaseModel
from datetime import datetime, timezone

class EmailLog(BaseModel):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('templates.id'), nullable=False)
    status = Column(String(50), nullable=False)  # Success, Failed, Pending
    created = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Definição dos relacionamentos
    user = relationship("User", back_populates="email_logs")
    contact = relationship("Contact", back_populates="email_logs")
    template = relationship("Template", back_populates="email_logs")

