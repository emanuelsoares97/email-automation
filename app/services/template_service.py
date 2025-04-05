from app.models.template import Template
from app import db
from flask import g
from app.utils.logger_util import get_logger
from sqlalchemy import or_

logger= get_logger(__name__)

class TemplateService:

    @staticmethod
    def create_template(user, name, subject, body, is_global=False):
        if is_global and user.role != 'admin':
            raise Exception("Somente admins podem criar templates globais.")
        
        new_template = Template(
            user_id=None if is_global else user.id,
            name=name,
            subject=subject,
            body=body,
            is_global=is_global
        )
        db.session.add(new_template)
        db.session.commit()
        return new_template

    @staticmethod
    def get_template(template_id):
        return Template.query.get(template_id)

    @staticmethod
    def get_list_template(user_id):

        try:
            logger.info("Lista de templates")
            
            if g.current_user["role"]== "admin":

                listas = Template.query.all()

                return [lista.to_dict() for lista in listas]
            else:
                
                listas = Template.query.filter(or_(Template.is_global== True, Template.user_id==user_id)).all()

                return [lista.to_dict() for lista in listas]
            
        except Exception as e:
            logger.error(f"Erro ao tentar buscar a lista de templates com o utilizador: {g.current_user['email']}, erro: {str(e)}", exc_info=True)
            return ({"erro": "Erro interno no servidor"}), 500

    @staticmethod
    def update_template(template_id, data):
        template = Template.query.get(template_id)
        if template:
            template.name = data.get('name', template.name)
            template.subject = data.get('subject', template.subject)
            template.body = data.get('body', template.body)
            template.is_global = data.get('is_global', template.is_global)
            db.session.commit()
            return template
        return None

    @staticmethod
    def delete_template(template_id):
        template = Template.query.get(template_id)
        if template:
            db.session.delete(template)
            db.session.commit()
            return True
        return False
