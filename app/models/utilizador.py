from sqlalchemy import Column, Integer, String, Boolean
from app.models.abstrata import BaseModel

class Utilizador(BaseModel):  
    __tablename__ = "utilizadores"

    id = Column(Integer, primary_key=True, autoincrement=True)  #Garantir que `id` fica primeiro!
    nome = Column(String(100), nullable=False)
    email= Column(String, nullable=False)
    password=Column(String, nullable=False)
    role = Column(String, default="user") 
    ativo = Column(Boolean, default=True)