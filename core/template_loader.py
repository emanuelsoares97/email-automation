import os

def load_template(nome_arquivo: str, nome_colaborador: str) -> str:
    caminho = os.path.join("templates", nome_arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        html = f.read()

    html_personalizado = html.replace("{{nome}}", nome_colaborador)
    return html_personalizado