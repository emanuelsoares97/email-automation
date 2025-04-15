from app.models.contact import Contact
from app import db
from flask import g
from app.utils.logger_util import get_logger
from sqlalchemy import or_


logger= get_logger(__name__)

class ContactService:
    
    @staticmethod
    def list_contacts():
        # Consulta os contatos do usuário (ou do admin)
        contacts = Contact.query.all()  # Modifique conforme necessário
        return {"contacts": [contact.to_dict() for contact in contacts]}, 200

    @staticmethod
    def create_contact(data):
        # Criação de um novo contato
        new_contact = Contact(name=data['name'], email=data['email'], user_id=g.current_user['id'])
        db.session.add(new_contact)
        db.session.commit()
        return {"message": "Contato criado com sucesso!"}, 201

    @staticmethod
    def update_contact(contact_id, data):
        contact = Contact.query.filter_by(id=contact_id, user_id=g.current_user['id']).first()
        if not contact:
            return {"error": "Contato não encontrado ou você não tem permissão para editar."}, 404
        contact.name = data.get('name', contact.name)
        contact.email = data.get('email', contact.email)
        db.session.commit()
        return {"message": "Contato atualizado com sucesso!"}, 200

    @staticmethod
    def delete_contact(contact_id):
        contact = Contact.query.filter_by(id=contact_id, user_id=g.current_user['id']).first()
        if not contact:
            return {"error": "Contato não encontrado ou você não tem permissão para deletar."}, 404
        db.session.delete(contact)
        db.session.commit()
        return '', 204  # Resposta vazia com status 204
