# Email Automation - Módulo RH

Este projeto é um sistema de envio automático de e-mails com anexo e template HTML personalizado, ideal para uso interno em equipes como RH, atendimento, ou comunicação corporativa.

## Funcionalidades
- Envio de e-mails com templates HTML responsivos
- Personalização de nome no conteúdo
- Anexos PDF individuais para cada colaborador
- Leitura dos destinatários via arquivo CSV
- Logs de sucesso e erro com `logging`
- Agendamento de envios com `schedule`
- Suporte a vários tipos de mensagens: boas-vindas, aniversário, elogio, 1 ano de casa

## Estrutura do Projeto
```
email-automation/
├── core/
│   ├── email_sender.py
│   ├── scheduler_runner.py
│   └── template_loader.py
├── templates/
│   ├── boas_vindas.html
│   ├── aniversario.html
│   ├── elogio.html
│   └── um_ano_empresa.html
├── utils/
│   ├── caminhos.py
│   ├── logger_util.py
│   └── readcsv.py
├── pdfs/
│   └── (anexos individuais dos colaboradores)
├── contacts/
│   └── colaboradores.csv
├── tests/
│   └── test_email_sender.py
├── .env.example
├── requirements.txt
└── main.py
```

## Formato do CSV
Arquivo: `contacts/colaboradores.csv`

```csv
nome,email,anexo,tipo
tuta,tuta@email.com,tuta.pdf,boas_vindas
ana,ana@email.com,,aniversario
carlos,carlos@email.com,relatorio.pdf,elogio
```

## Como Usar
1. Renomeie `.env.example` para `.env` e preencha:
```env
EMAIL=seu@email.com
EMAIL_PASSWORD=sua_senha_ou_senha_de_app
```

2. Instale dependências:
```bash
pip install -r requirements.txt
```

3. Rode o script principal:
```bash
python main.py
```

4. Para usar o agendamento automático:
```bash
python core/scheduler_runner.py
```

## Testes Automatizados
Utiliza `pytest` para testar:
- Carregamento de templates HTML
- Validação de erros (ex: tipo ausente)
- Simula envio real sem enviar e-mail de verdade com `monkeypatch`

Rode com:
```bash
pytest tests/
```

## Logger
Os logs são salvos automaticamente com informações de envio, erros e anexos.

## Licença
Este projeto é para fins educacionais e demonstração de aplicação real com Python.

---
Desenvolvido por Emanuel Soares

