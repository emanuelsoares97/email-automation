import csv

def read_contacts(caminho_csv):
    contatos = []
    with open(caminho_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            # Valida se nome e email estão presentes
            if not linha.get("nome") or not linha.get("email"):
                continue  # se nao tiverem no csv nao considera

            contatos.append({
                "nome": linha.get("nome"),
                "email": linha.get("email"),
                "anexo": linha.get("anexo") or None,
                "tipo": linha.get("tipo") or None
            })
    return contatos

