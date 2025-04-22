from flask import Blueprint, request, jsonify
from app.services.user_service import UtilizadorService
from app.services.auth_service import AuthService
from app.utils.logger_util import get_logger
from flask import g

logger = get_logger(__name__)

user_bp = Blueprint("user", __name__)

@user_bp.route("/new", methods=["POST"])
@AuthService.token_required
@AuthService.role_required("admin")
def create_new_user():
    """Cria um novo utilizador"""
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"erro": "Dados inválidos."}), 400

        
        if not data or "name" not in data or "email" not in data or "password" not in data:
            logger.warning("Tentativa de criar utilizador sem dados completos.")
            return jsonify({"erro": "Nome, email e senha são obrigatórios!"}), 400
        
        passw = data.get("password")

        if not passw or len(passw) < 6:
            return jsonify({"erro": "A password deve ter pelo menos 6 caracteres."}), 400


        logger.info(f"Tentativa de criar utilizador: {data.get('email')}")
        resposta, status = UserService.criar_utilizador(
                data.get("name"),
                data.get("email"),
                data.get("password")
        )

        return jsonify(resposta), status

    except Exception as e:
        logger.error(f"Erro ao criar utilizador: {str(e)}", exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), 500