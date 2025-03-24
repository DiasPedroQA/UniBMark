"""
Módulo Caminho (Versão sem pathlib e sem TypedDict)

Esta classe permite:
- Validação de caminhos fornecidos com expressões regulares.
- Verificação de permissões de leitura e escrita.
- Identificação do tipo do caminho (arquivo, diretório, link simbólico).
- Exportação de informações do caminho em dicionário ou JSON.

Compatível com Python 3.12.3
"""

import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class Caminho:
    """
    Classe para manipulação de caminhos usando apenas expressões regulares.
    """

    def __init__(self, caminho_inicial: str) -> None:
        """Inicializa a instância e valida o caminho."""
        self._caminho = self._validar_caminho(caminho_inicial)

    @property
    def caminho(self) -> str:
        """Retorna o caminho armazenado."""
        return self._caminho

    @staticmethod
    def _validar_caminho(caminho_atual: str) -> str:
        """Valida e normaliza um caminho usando regex."""
        if not isinstance(caminho_atual, str) or not caminho_atual.strip():
            raise TypeError("O caminho deve ser uma string não vazia.")

        caminho_atual = os.path.abspath(caminho_atual)  # Normaliza o caminho

        if not os.path.exists(caminho_atual):
            raise FileNotFoundError(f"O caminho atual não existe: {caminho_atual}")

        if not Caminho._verificar_permissao(caminho_atual):
            raise PermissionError(
                f"Sem permissão de leitura e escrita: {caminho_atual}"
            )

        return caminho_atual

    @staticmethod
    def _verificar_permissao(caminho_atual: str) -> bool:
        """Verifica permissão de leitura e escrita."""
        return os.access(caminho_atual, os.R_OK | os.W_OK)

    def _determinar_tipo(self) -> str:
        """Determina se o caminho é um arquivo, diretório ou link simbólico."""
        if os.path.isdir(self._caminho):
            return "diretório"
        if os.path.isfile(self._caminho):
            return "arquivo"
        if os.path.islink(self._caminho):
            return "link simbólico"
        return "desconhecido"

    def to_dict(self) -> dict:
        """Retorna um dicionário com informações do caminho."""
        return {
            "caminho": self._caminho,
            "tipo": self._determinar_tipo(),
            "existe": os.path.exists(self._caminho),
            "permissao": self._verificar_permissao(self._caminho),
            "normalizado": os.path.abspath(self._caminho),
        }

    def to_json(self) -> str:
        """Retorna um JSON formatado com as informações do caminho."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    def __repr__(self) -> str:
        """Representação legível do objeto."""
        return f"Caminho(caminho={self._caminho})"

    def __eq__(self, other) -> bool:
        """Compara dois objetos Caminho pelo caminho absoluto."""
        return isinstance(other, Caminho) and self._caminho == other._caminho


if __name__ == "__main__":
    caminho_pasta = Caminho("/home/pedro-pm-dias/Downloads/Firefox/")
    print(caminho_pasta)
    print(caminho_pasta.to_json())
    print("*" * 50)
    caminho_arquivo = Caminho("/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html")
    print(caminho_arquivo)
    print(caminho_arquivo.to_json())
