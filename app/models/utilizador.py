from sqlalchemy import Column, Integer, String, Boolean
from app.models.abstrata import BaseModel
from sqlalchemy.orm import relationship

class Utilizador(BaseModel):  
    __tablename__ = "utilizadores"

    id = Column(Integer, primary_key=True, autoincrement=True)  #Garantir que `id` fica primeiro!
    nome = Column(String(100), nullable=False)
    email= Column(String, nullable=False)
    password=Column(String, nullable=False)
    role = Column(String, default="user") 
    ativo = Column(Boolean, default=True)

    # Relacionamento com o UserPlan para acessar o plano do usuário
    planos = relationship("UserPlan", backref="utilizador", lazy="dynamic")  # Acessa os planos associados ao utilizador