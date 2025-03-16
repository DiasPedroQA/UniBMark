from jira_api import JiraClient
# sourcery skip: dont-import-test-modules
from test_runner import rodar_testes


def main():
    jira = JiraClient()
    if erros := rodar_testes():
        print(f"⚠️ {len(erros)} erro(s) encontrado(s). Criando tickets no Jira...")
        for erro in erros:
            jira.criar_ticket(titulo="Bug detectado", descricao=erro)
    else:
        print("✅ Nenhum erro encontrado!")


if __name__ == "__main__":
    main()
