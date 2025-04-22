from app.models.user import Utilizador
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.logger_util import get_logger
from app.utils.validacao import validar_email
from app.database.database import db
import secrets
import string
from flask import g



class UtilizadorService:
    """Gerencia autenticação e operações com utilizadores"""

    logger = get_logger(__name__)

    @staticmethod
    def gerar_password_temporaria(tamanho=10):
        """Gera uma senha temporária aleatória"""
        caracteres = string.ascii_letters + string.digits + "!@#$%&*"
        return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

    @classmethod
    def autenticar(cls, email, password):
        """Verifica credenciais e retorna o utilizador autenticado"""
        try:
            utilizador = Utilizador.query.filter_by(email=email).first()

            if utilizador and check_password_hash(utilizador.password, password):
                cls.logger.info(f"Utilizador {utilizador.email} autenticado.")
                return utilizador

            cls.logger.info(f"Credenciais inválidas para o email: {email}")
            return None
        except Exception as e:
            cls.logger.error(f"Erro ao autenticar o utilizador: {str(e)}")
            return None

    @classmethod
    def criar_utilizador(cls, nome, email, password=None, role="user"):
        """Cria um novo utilizador se não existir"""
        if not nome or not email or not password:
            cls.logger.error("Tentativa de criar utilizador com dados em falta.")
            return {"erro": "Nome, email e senha são obrigatórios!"}, 400

        if not validar_email(email):
            cls.logger.error(f"Tentativa de email inválido: {email}.")
            return {"erro": "Email inválido!"}, 400

        if Utilizador.query.filter_by(email=email).first():
            cls.logger.info(f"Tentativa de criar utilizador com email já registado, {email}.")
            return {"erro": "Já existe um utilizador com este email!"}, 400

        if role == "admin" and g.current_user["role"] != "admin":
            cls.logger.error("Tentativa de criar utilizador admin sem permissão.")
            return {"erro": "Apenas administradores podem criar contas com permissão de admin."}, 403

        if not password:
            password = cls.gerar_password_temporaria()

        hashed_password = generate_password_hash(password)

        if role not in ["admin", "user"]:
            return {"erro": "Tipo de role inválido!"}, 400

        novo_utilizador = Utilizador(nome=nome, email=email, password=hashed_password, role=role)

        try:
            db.session.add(novo_utilizador)
            db.session.commit()
            cls.logger.info(f"Utilizador {nome} criado com sucesso.")
            return {
                "mensagem": "Utilizador criado com sucesso!",
                "utilizador": {
                    "id": novo_utilizador.id,
                    "nome": novo_utilizador.nome,
                    "email": novo_utilizador.email
                }
            }, 201
        except IntegrityError as e:
            db.session.rollback()
            cls.logger.error(f"Erro ao criar utilizador: {str(e)}")
            return {"erro": "Erro ao criar utilizador. Por favor, tente novamente."}, 500
        except Exception as e:
            db.session.rollback()
            cls.logger.error(f"Erro desconhecido ao criar utilizador: {str(e)}")
            return {"erro": "Erro desconhecido ao criar utilizador."}, 500

    @classmethod
    def listar_utilizadores(cls, ativos=True):
        """Lista utilizadores, podendo filtrar apenas os ativos"""
        try:
            if ativos:
                utilizadores = Utilizador.query.filter_by(ativo=True).all()
            else:
                utilizadores = Utilizador.query.all()

            return [{"id": u.id, "nome": u.nome, "email": u.email, "role": u.role, "ativo": u.ativo} for u in utilizadores]
        except Exception as e:
            cls.logger.error(f"Erro ao listar utilizadores: {str(e)}")
            return {"erro": "Erro ao listar utilizadores."}, 500

    @classmethod
    def atualizar_utilizador(cls, utilizador_id, nome=None, email=None, password=None, role=None, ativo=None):
        """Atualiza um utilizador"""
        try:
            utilizador = Utilizador.query.filter_by(id=utilizador_id).first()

            if not utilizador:
                return {"erro": "Utilizador não encontrado!"}, 404

            if nome:
                utilizador.nome = nome

            if email:
                if not validar_email(email):
                    cls.logger.error(f"Tentativa de email inválido: {email}.")
                    return {"erro": "Email inválido!"}, 400
                utilizador.email = email

            if password:
                utilizador.password = generate_password_hash(password)

            if role is not None:
                if role == "admin" and g.current_user["role"] != "admin":
                    cls.logger.error("Tentativa de promover um utilizador para admin sem autorização.")
                    return {"erro": "Apenas administradores podem promover contas para admin."}, 403

                if utilizador.role == "admin" and g.current_user["role"] != "admin":
                    cls.logger.error("Tentativa de modificar um administrador sem autorização.")
                    return {"erro": "Apenas administradores podem alterar contas de outros administradores."}, 403

                if role not in ["admin", "user"]:
                    return {"erro": "Tipo de role inválido!"}, 400

                utilizador.role = role

            if ativo is not None:
                utilizador.ativo = ativo

            db.session.commit()
            cls.logger.info(f"Utilizador {utilizador.id} atualizado com sucesso.")
            return {
                "mensagem": "Utilizador atualizado com sucesso!",
                "utilizador": {
                    "id": utilizador.id,
                    "nome": utilizador.nome,
                    "email": utilizador.email,
                    "role": utilizador.role,
                    "ativo": utilizador.ativo
                }
            }
        except IntegrityError as e:
            db.session.rollback()
            cls.logger.error(f"Erro ao atualizar utilizador: {str(e)}")
            return {"erro": "Erro ao atualizar utilizador. Por favor, tente novamente."}, 500
        except Exception as e:
            db.session.rollback()
            cls.logger.error(f"Erro desconhecido ao atualizar utilizador: {str(e)}")
            return {"erro": "Erro desconhecido ao atualizar utilizador."}, 500

    @classmethod
    def desativar_utilizador(cls, utilizador_id):
        """Marca um utilizador como inativo em vez de remover"""
        try:
            utilizador = Utilizador.query.filter_by(id=utilizador_id).first()

            if not utilizador:
                return {"erro": "Utilizador não encontrado!"}, 404

            utilizador.ativo = False
            db.session.commit()
            cls.logger.info(f"Utilizador {utilizador.id} desativado com sucesso.")
            return {"mensagem": f"Utilizador '{utilizador.nome}' desativado com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            cls.logger.error(f"Erro ao desativar utilizador: {str(e)}")
            return {"erro": "Erro ao desativar utilizador."}, 500

    @classmethod
    def reativar_utilizador(cls, utilizador_id):
        """Reativa um utilizador marcado como inativo"""
        try:
            utilizador = Utilizador.query.filter_by(id=utilizador_id).first()

            if not utilizador:
                return {"erro": "Utilizador não encontrado!"}, 404

            if utilizador.ativo:
                return {"erro": "O utilizador já está ativo!"}, 400

            utilizador.ativo = True
            db.session.commit()
            cls.logger.info(f"Utilizador {utilizador.id} reativado com sucesso.")
            return {"mensagem": f"Utilizador '{utilizador.nome}' foi reativado com sucesso!"}, 200
        except Exception as e:
            db.session.rollback()
            cls.logger.error(f"Erro ao reativar utilizador: {str(e)}")
            return {"erro": "Erro ao reativar utilizador."}, 500
