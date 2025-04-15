from sqlalchemy import Column, Integer, String, Boolean, UniqueConstraint, ForeignKey
from app.models.abstrata import BaseModel
from sqlalchemy.orm import relationship

class Utilizador(BaseModel):  
    __tablename__ = "utilizadores"

    __table_args__ = (
    UniqueConstraint("email", name="uq_utilizadores_email"),
)

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user") 
    ativo = Column(Boolean, default=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=True)

    # Relacionamento 
    planos = relationship("UserPlan", back_populates="utilizador", lazy="dynamic")

    

    def __repr__(self):
        return f'<User {self.nome}>'
