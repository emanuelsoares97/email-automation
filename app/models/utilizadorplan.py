from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.abstrata import BaseModel

class UserPlan(BaseModel):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    utilizador_id = Column(Integer, ForeignKey("utilizadores.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    emails_enviados = Column(Integer, default=0)
    subscrito_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    utilizador = relationship("Utilizador", back_populates="planos")
    plano = relationship("Plan", backref="user_plans")

