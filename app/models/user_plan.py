from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.models.abstract import BaseModel

class UserPlan(BaseModel):
    __tablename__ = "user_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)
    emails_send = Column(Integer, default=0)
    subscribe = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    users = relationship("Utilizador", back_populates="plans")

    plans = relationship("Plan", back_populates="user_plans")


