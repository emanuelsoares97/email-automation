from flask import Blueprint, request, jsonify
from app import db
from app.services.auth_service import AuthService
from app.models.contact import Contact

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/add_contact', methods=['POST'])
@AuthService.token_required
def add_contact():
    # Recuperar o JSON enviado
    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')
    email = data.get('email')

    # valida se ja existe esse email na lista do utilizador
    existing_contact = Contact.query.filter_by(user_id=user_id, email=email).first()
    if existing_contact:
        return jsonify({"error": "Já existe um contato com este e-mail para este usuário."}), 400

    # Criar novo contato
    new_contact = Contact(user_id=user_id, name=name, email=email)

    # Adicionar ao banco de dados
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contato adicionado com sucesso!"}), 201
