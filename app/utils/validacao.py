import re

def validar_email(email: str) -> bool:
    """Valida se o email está em um formato correto."""
    padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(padrao, email))

def validar_telemovel(telemovel: str) -> bool:
    """
    Valida se o número de telemóvel possui exatamente 9 dígitos e começa com 9.
    """
    padrao = r"^9(?:1|2|3|6)\d{7}$"
    return bool(re.match(padrao, telemovel))