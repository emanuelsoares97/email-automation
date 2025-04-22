from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.abstract import BaseModel
from datetime import datetime, timezone

class Organization(BaseModel):

    __tablename__ = "organizations"

    id   = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    areas = relationship("Area", back_populates="organizations", lazy="dynamic")
    contacts = relationship("Contact", back_populates="organizations", lazy="dynamic")
    users = relationship("User", back_populates="organizations", lazy="dynamic")

