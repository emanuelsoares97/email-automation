from flask import Blueprint, request, jsonify, make_response, g
from app.services.utilizador_service import UtilizadorService
from app.services.tokenrevogado_service import TokenService
from app.utils.logger_util import get_logger
from app.services.auth_service import AuthService
from app.models.utilizador import Utilizador
from app.utils.validacao import validar_email
import jwt
from collections import namedtuple
from config import Config
from app.services.template_service import TemplateService
from sqlalchemy.exc import SQLAlchemyError


logger = get_logger(__name__)

template_bp = Blueprint("template", __name__)

@template_bp.route("/list", methods=["GET"])
@AuthService.token_required
def lista_templates():
    """Endpoint para listar templates"""
    try:
        logger.info(f"Utilizador {g.current_user['email']}, está a ver a lista de templates")

        lista = TemplateService.get_list_template(g.current_user["id"])

        return jsonify(lista), 200

    except SQLAlchemyError as e:
        logger.error(f"Erro ao acessar o banco de dados: {str(e)}")
        return jsonify({"erro": "Erro ao carregar templates."}), 500
    except Exception as e:
        logger.error(f"Erro desconhecido ao listar templates: {str(e)}")
        return jsonify({"erro": "Erro desconhecido."}), 500
   
            