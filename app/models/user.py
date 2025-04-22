from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, ForeignKey
from app.models.abstract import BaseModel
from sqlalchemy.orm import relationship

class User(BaseModel):  
    __tablename__ = "users"

    __table_args__ = (
    UniqueConstraint("email", name="uq_users_email"),
) #garante email unico por user

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user") 
    active = Column(Boolean, default=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    area_id= Column(Integer, ForeignKey("areas.id"), nullable=True)

    # Relacionamento 
    organization = relationship("Organization", back_populates="users")

    area = relationship("Area", back_populates="users")

    contacts = relationship("Contact", back_populates="users", lazy="dynamic")

    templates = relationship("Template", back_populates="users", lazy="dynamic")

    plans = relationship("UserPlan", back_populates="uuserser", lazy="dynamic")

    email_logs = relationship("EmailLog", back_populates="users", lazy="dynamic")



    

    def __repr__(self):
        return f'<User {self.nome}>'
