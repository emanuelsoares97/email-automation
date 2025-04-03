from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from app.models.abstrata import BaseModel
from datetime import datetime, timezone

class Template(BaseModel):

    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
