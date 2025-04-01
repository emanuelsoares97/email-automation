from app import create_app
from app.database.database import db
from app.models.utilizador import Utilizador
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    if not Utilizador.query.filter_by(email="admin@email.com").first():
        admin = Utilizador(
            nome="Administrador",
            email="admin@email.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin criado com sucesso.")
    else:
        print("⚠️ O admin já existe.")
