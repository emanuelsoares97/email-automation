from flask import Blueprint, request, jsonify, make_response, g
from app.services.user_service import UtilizadorService
from app.services.tokenrevogado_service import TokenService
from app.utils.logger_util import get_logger
from app.services.auth_service import AuthService
from app.models.user import Utilizador
from app.utils.validacao import validar_email
import jwt
from collections import namedtuple
from config import Config


logger = get_logger(__name__)

sendemail_bp = Blueprint("sendemail", __name__)

