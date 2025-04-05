from sqlalchemy import Column, Integer
from sqlalchemy.inspection import inspect
from app.utils.logger_util import get_logger
from app.database.database import db

logger = get_logger(__name__)

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    logger.info("Classe Abstrata iniciada")

    def to_dict(self):
        
        """
            Converte o objeto SQLAlchemy em um dicionário com os atributos da tabela.

            Utiliza o módulo `inspect` do SQLAlchemy para iterar sobre todos os atributos 
            de coluna definidos no modelo e extrair seus valores.

            Returns:
                dict: Um dicionário com chave/valor representando os campos e dados do objeto.
                    Em caso de erro, retorna um dicionário com uma mensagem de erro.
        """
        try:
            if not hasattr(self, "__table__"):
                raise AttributeError("Modelo sem `__table__`, pode estar mal definido.")
            logger.info("Objeto convertido para JSON.")
            return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        except Exception as e:
            logger.error(f"Erro ao converter objeto para JSON: {str(e)}", exc_info=True)
            return {"erro": "Falha na conversão para JSON"}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


    @classmethod
    def criar_tabelas(cls):
        """Garante que as tabelas sejam criadas corretamente (por exemplo, em testes)"""
        try:
            from app.database import Database
            db = Database.get_session()
            cls.get_base().metadata.create_all(db.get_bind())  # Cria as tabelas no banco
            logger.info("Tabelas criadas para testes.")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")
            raise