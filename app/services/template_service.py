from app.models.template import Template
from app import db

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
