"""
Este módulo carrega as configurações da aplicação Flask a partir de variáveis de ambiente.

Classes:
    - Config: Contém as configurações da aplicação Flask,
    incluindo a chave secreta, modo de depuração e teste.

Funções:
    Nenhuma
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configurações da aplicação Flask"""

    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = True
    TESTING = True

    def __init__(self):
        pass
