from sqlalchemy import Column, Integer, String
from app.models.abstract import BaseModel
from sqlalchemy.orm import relationship

class Plan(BaseModel):

    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email_limit = Column(Integer, nullable=False)

    user_plans = relationship("UserPlan", back_populates="plans", lazy="dynamic")
