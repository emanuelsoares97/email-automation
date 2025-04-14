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
def list_templates():
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
   
@template_bp.route("/new", methods=["POST"])
@AuthService.token_required
def new_template():

    try:
        data=request.get_json()

        if not isinstance(data, dict):
            return jsonify({"erro": "Dados inválidos."}), 400

        if not data or "name" not in data or "subject" not in data or "body" not in data:
                logger.warning("Tentativa de criar template sem dados completos.")
                return jsonify({"erro": "Nome, assunto e corpo do email são obrigatórios!"}), 400
        
        isglobal = data.get("is_global")

        if not isglobal:
            isglobal=False

        resposta, status = TemplateService.create_template(
            g.current_user["id"],
            data.get("name"),
            data.get("subject"),
            data.get("body"),
            data.get("is_global")
        )

        return jsonify(resposta), status

    except Exception as e:
        logger.error(f"Erro ao criar template: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500
    
@template_bp.route("/<int:template_id>", methods=["PATCH"])
@AuthService.token_required
def update_template(template_id):

    data=request.get_json()

    if not isinstance(data, dict):
            return jsonify({"erro": "Dados inválidos."}), 400
    
    resposta, status = TemplateService.update_template(
         g.current_user["id"], 
         template_id, 
         data
    )
    
    return jsonify(resposta), status

@template_bp.route("/<int:template_id>", methods=["DELETE"])
@AuthService.token_required
def delete_template(template_id):
    resposta, status = TemplateService.delete_template(template_id)

    return resposta, status 

    


