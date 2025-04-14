from app.models.template import Template
from app import db
from flask import g
from app.utils.logger_util import get_logger
from sqlalchemy import or_

logger= get_logger(__name__)

class TemplateService:

    @staticmethod
    def create_template(user, name, subject, body, is_global=False):

        user = g.current_user

        try: 
            if is_global and user["role"] != 'admin':
                raise Exception("Somente admins podem criar templates globais.")            

            
            new_template = Template(
                user_id=None if is_global else user["id"],
                name=name,
                subject=subject,
                body=body,
                is_global=is_global
            )

            exist_template = Template.query.filter(
                    Template.name == name,
                    Template.user_id == user["id"]
                ).first()

            if exist_template:
                return {"error": "Já existe um template com esse nome, usa outro."}, 400

            db.session.add(new_template)
            db.session.commit()
            return new_template.to_dict(), 201
        
        except Exception as e:
            logger.error(f"Erro ao tentar criar um template com o utilizador: {g.current_user['email']}, erro: {str(e)}", exc_info=True)
            return ({"erro": "Erro interno no servidor"}), 500
           

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
    def update_template(user_id, template_id, data):
        user = g.current_user

        try:
            template = Template.query.filter(
                Template.user_id == user["id"],
                Template.id == template_id
            ).first()

            if template:
                template.name = data.get('name', template.name)
                template.subject = data.get('subject', template.subject)
                template.body = data.get('body', template.body)
                template.is_global = data.get('is_global', template.is_global)
            

                exist_template = Template.query.filter(
                    Template.name == template.name,
                    Template.user_id == user["id"]
                ).first()

                if exist_template and exist_template.id != template.id:
                    return {"error": "Já existe um template com esse nome, usa outro."}, 400

                db.session.commit()
                logger.info(f"Template ID {template_id} atualizado por {user['email']}")
                return template, 200

            logger.warning(f"Tentativa inválida de update no template ID {template_id} por {user['email']}")
            return {"erro": "Tentativa de aceder a um template que não pertence ao utilizador"}, 403

        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar template ID {template_id}: {str(e)}", exc_info=True)
            return {"erro": "Erro interno ao atualizar template"}, 500



    @staticmethod
    def delete_template(template_id):
        template = Template.query.get(template_id)
        if template:
            db.session.delete(template)
            db.session.commit()
            return True
        return False
