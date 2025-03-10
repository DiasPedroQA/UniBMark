"""
Este módulo fornece uma classe `JiraClient` para interagir
com a API do Jira e criar tickets de bug.

Classes:
    JiraClient: Classe para autenticar e criar tickets de bug no Jira.

Exceções:
    Nenhuma

Funções:
    Nenhuma
"""


import requests
from config import JIRA_URL, JIRA_USER, JIRA_API_TOKEN, JIRA_PROJECT_KEY


class JiraClient:
    """Classe para interagir com a API do Jira e criar tickets de bug."""

    def __init__(self):
        """Inicializa o JiraClient com autenticação e cabeçalhos.

        Configura o cliente Jira com as credenciais
        necessárias e cabeçalhos para realizar requisições API.
        """
        self.auth = (JIRA_USER, JIRA_API_TOKEN)
        self.headers = {"Content-Type": "application/json"}

    def criar_ticket(self, titulo, descricao):
        """Cria um ticket de bug no Jira."""
        url = f"{JIRA_URL}/rest/api/3/issue"
        payload = {
            "fields": {
                "project": {"key": JIRA_PROJECT_KEY},
                "summary": titulo,
                "description": descricao,
                "issuetype": {"name": "Bug"}
            }
        }

        response = requests.post(
            url, json=payload, headers=self.headers, auth=self.auth, timeout=10
        )

        if response.status_code == 201:
            print(f"✅ Ticket criado com sucesso: {response.json()['key']}")
        else:
            print(
                f"❌ Erro ao criar ticket: {response.status_code} - "
                f"{response.text}")
