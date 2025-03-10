from jira_api import JiraClient
from test_runner import rodar_testes

def main():
    jira = JiraClient()
    erros = rodar_testes()
    
    if erros:
        print(f"⚠️ {len(erros)} erro(s) encontrado(s). Criando tickets no Jira...")
        for erro in erros:
            jira.criar_ticket(titulo="Bug detectado", descricao=erro)
    else:
        print("✅ Nenhum erro encontrado!")

if __name__ == "__main__":
    main()
