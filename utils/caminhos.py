import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import os
from utils.readcsv import read_contacts

caminho_file_contacts= os.path.join(os.getcwd(), "contacts")
os.makedirs(caminho_file_contacts, exist_ok=True)

# Caminhos dos ficheiros de contactos
caminho_csv_colaboradores = os.path.join(caminho_file_contacts, "colaboradores.csv")