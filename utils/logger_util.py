import os
import logging

# Criar diretório para logs se não existir
caminho_logs= os.path.join(os.getcwd(), "logs")
os.makedirs(caminho_logs, exist_ok=True)

# Caminhos dos ficheiros de log
LOG_GERAL = os.path.join(caminho_logs, "logs_geral.log")
LOG_ERROS = os.path.join(caminho_logs, "logs_erros.log")
LOG_DEBUG = os.path.join(caminho_logs, "logs_debug.log")

# Criar formatador para os logs
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

# Criar handlers para diferentes tipos de log
file_handler_geral = logging.FileHandler(LOG_GERAL, encoding="utf-8")
file_handler_geral.setLevel(logging.INFO)  # Guarda INFO e WARNING
file_handler_geral.setFormatter(formatter)

file_handler_erros = logging.FileHandler(LOG_ERROS, encoding="utf-8")
file_handler_erros.setLevel(logging.ERROR)  # Guarda ERROR e CRITICAL
file_handler_erros.setFormatter(formatter)

file_handler_debug = logging.FileHandler(LOG_DEBUG, encoding="utf-8")
file_handler_debug.setLevel(logging.DEBUG)  # Guarda DEBUG
file_handler_debug.setFormatter(formatter)

# Criar função para obter um logger específico
def get_logger(nome):
    """Cria e retorna um logger específico para uma classe/módulo."""
    logger = logging.getLogger(nome)
    logger.setLevel(logging.DEBUG)  # Aceita todos os níveis de log

    # Evitar duplicação de handlers
    if not logger.handlers:
        logger.addHandler(file_handler_geral)
        logger.addHandler(file_handler_erros)
        logger.addHandler(file_handler_debug)

    return logger
