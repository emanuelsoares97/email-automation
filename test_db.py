from app.__init__ import create_app


app = create_app()

print("✅ App criada:", app)
print("📦 Tipo do app:", type(app))

with app.app_context():
    print("🚀 Consegui acessar o app_context!")
