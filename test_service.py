from app import create_app, db
from app.services.template_service import TemplateService
from app.models.utilizador import Utilizador

# Cria a app
app = create_app()

with app.app_context():
    # Busca um utilizador admin
    user = Utilizador.query.filter_by(role="admin").first()

    if user:
        # Cria um template
        template = TemplateService.create_template(
            user=user,
            name="Template de Boas-vindas",
            subject="Bem-vindo!",
            body="Olá {{nome}}, seja bem-vindo ao nosso sistema!",
            is_global=True
        )
        print(f"Template criado com sucesso: ID {template.id} - {template.name}")
    else:
        print("Nenhum utilizador com role 'admin' encontrado.")
