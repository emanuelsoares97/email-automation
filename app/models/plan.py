from sqlalchemy import Column, Integer, String
from app.models.abstrata import BaseModel

class Plan(BaseModel):

    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email_limit = Column(Integer, nullable=False)