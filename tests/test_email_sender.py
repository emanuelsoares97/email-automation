import pytest
from core.email_sender import send_email
from core.template_loader import load_template

# Teste básico do carregamento de template
def test_template_carrega_html():
    html = load_template("boas_vindas.html", "Maria")
    assert "Olá Maria" in html

# Teste de erro quando tipo está ausente
def test_erro_quando_tipo_ausente():
    with pytest.raises(ValueError):
        send_email(destinatario="teste@email.com", nome="João", tipo=None)

# Teste de envio com dados simulados (sem anexo)
def test_envio_com_sucesso_sem_anexo(monkeypatch):
    def fake_smtp(*args, **kwargs):
        class FakeSMTP:
            def __enter__(self): return self
            def __exit__(self, *a): pass
            def login(self, email, pwd): pass
            def send_message(self, msg): pass
        return FakeSMTP()
    
    monkeypatch.setattr("smtplib.SMTP_SSL", fake_smtp)

    send_email(destinatario="teste@email.com", nome="João", tipo="boas_vindas")
