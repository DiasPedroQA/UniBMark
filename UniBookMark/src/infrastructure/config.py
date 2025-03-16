"""
Módulo de configuração para carregar variáveis de ambiente
relacionadas à integração com o JIRA.

Este módulo utiliza o pacote `dotenv` para carregar
variáveis de ambiente de um arquivo `.env`, se ele existir.
As seguintes variáveis de ambiente são esperadas:
- JIRA_URL: A URL da instância do JIRA.
- JIRA_USER: O nome de usuário para autenticação no JIRA.
- JIRA_API_TOKEN: O token de API para autenticação no JIRA.
- JIRA_PROJECT_KEY: A chave do projeto JIRA para interagir.
"""


import os

from dotenv import load_dotenv

# Carregar variáveis do .env (se existirem)
load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_USER = os.getenv("JIRA_USER")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
