import os
import sys

# Asegurarse de que el directorio del archivo main.py esté en el path de Python
base_path = os.path.dirname(os.path.abspath(__file__))
# Asegura que Python busque en el directorio actual
sys.path.insert(0, base_path)


def load_certificates():
    cert = os.path.join(base_path, '..', 'certificados',
                        'prex_zapto_org_1_fins2025.pem')
    key = os.path.join(base_path, '..', 'certificados', 'myserver.key')
    return cert, key
