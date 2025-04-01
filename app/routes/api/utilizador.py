from flask import Blueprint, request, jsonify
from app.services.utilizador_service import UtilizadorService
from app.services.auth_service import AuthService
from app.utils.logger_util import get_logger
from config import Config
import jwt
from flask import g

logger = get_logger(__name__)

utilizador_bp = Blueprint("utilizador", __name__)

@utilizador_bp.route("/novo", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin")
def criar_utilizador():
    """Cria um novo utilizador"""
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"erro": "Dados inválidos."}), 400

        
        if not data or "nome" not in data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de criar utilizador sem dados completos.")
            return jsonify({"erro": "Nome, email e senha são obrigatórios!"}), 400
        
        passw = data.get("password")

        if not passw or len(passw) < 6:
            return jsonify({"erro": "A password deve ter pelo menos 6 caracteres."}), 400


        logger.info(f"Tentativa de criar utilizador: {data.get('email')}")
        resposta, status = UtilizadorService.criar_utilizador(
                data.get("nome"),
                data.get("email"),
                data.get("password")
        )

        return jsonify(resposta), status

    except Exception as e:
        logger.error(f"Erro ao criar utilizador: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500