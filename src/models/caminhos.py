# Description: Manipulação segura de caminhos do sistema de arquivos
# Expected: A classe Caminho deve fornecer validação robusta de caminhos,
# controle de acesso via getter/setter com validação,
# verificação de permissões, identificação do tipo
# (arquivo, diretório, link), exportação para dict e JSON e representações consistentes do objeto.
# Actual: A classe Caminho fornece validação robusta de caminhos,
# controle de acesso via getter/setter com validação,
# verificação de permissões, identificação do tipo
# (arquivo, diretório, link), exportação para dict
# e JSON e representações consistentes do objeto.

"""
Módulo Caminho - Manipulação segura de caminhos do sistema de arquivos

Esta classe fornece:
- Validação robusta de caminhos
- Controle de acesso via getter/setter com validação
- Verificação de permissões
- Identificação do tipo (arquivo, diretório, link)
- Exportação para dict e JSON
- Representações consistentes do objeto

Exemplo de uso:
    >>> caminho = Caminho("/pasta/valida")
    >>> caminho.caminho = "/novo/caminho"  # Atualiza com validação
    >>> print(caminho.to_json())  # Saída formatada em JSON
    >>> dados = caminho.to_dict()  # Dicionário com metadados
"""

import json
import os


class Caminho:
    """
    Classe para manipulação segura de caminhos do sistema de arquivos.

    Attributes:
        _caminho (str): Caminho absoluto validado do arquivo/diretório
    """

    def __init__(self, caminho_inicial: str) -> None:
        """
        Inicializa a instância com validação do caminho.

        Args:
            caminho_inicial: Caminho a ser validado e armazenado

        Raises:
            TypeError: Se o caminho não for string ou for vazio
            FileNotFoundError: Se o caminho não existir
            PermissionError: Sem permissões de leitura/escrita
        """
        self._caminho = self._validar_caminho(caminho_inicial)

    @property
    def caminho(self) -> str:
        """
        Getter para o caminho armazenado.

        Returns:
            str: Caminho absoluto validado
        """
        return self._caminho

    @caminho.setter
    def caminho(self, novo_caminho: str) -> None:
        """
        Setter com validação para atualizar o caminho.

        Args:
            novo_caminho: Novo caminho a ser validado e armazenado

        Raises:
            Mesmas exceções que _validar_caminho
        """
        self._caminho = self._validar_caminho(novo_caminho)

    @staticmethod
    def _verificar_permissao(caminho_atual: str) -> bool:
        """Verifica permissão de leitura e escrita."""
        return os.access(caminho_atual, os.R_OK | os.W_OK)

    @staticmethod
    def _validar_caminho(caminho_atual: str) -> str:
        """
        Valida e normaliza um caminho.

        Args:
            caminho_atual: Caminho a ser validado

        Returns:
            str: Caminho absoluto validado

        Raises:
            TypeError: Se o caminho não for string ou for vazio
            FileNotFoundError: Se o caminho não existir
            PermissionError: Sem permissões de leitura/escrita
        """
        if not isinstance(caminho_atual, str) or not caminho_atual.strip():
            raise TypeError("O caminho deve ser uma string não vazia.")

        caminho_atual = os.path.abspath(caminho_atual)

        if not os.path.exists(caminho_atual):
            raise FileNotFoundError(f"O caminho não existe: {caminho_atual}")

        if not Caminho._verificar_permissao(caminho_atual):
            raise PermissionError(f"Sem permissão em: {caminho_atual}")

        return caminho_atual

    def _determinar_tipo(self) -> str:
        """Determina o tipo do caminho."""
        if os.path.isdir(self._caminho):
            return "diretório"
        if os.path.isfile(self._caminho):
            return "arquivo"
        if os.path.islink(self._caminho):
            return "link simbólico"
        return "desconhecido"

    def to_dict(self) -> dict:
        """
        Retorna metadados do caminho como dicionário.

        Returns:
            dict: {
                'caminho': str,
                'tipo': str,
                'existe': bool,
                'permissao': bool,
                'normalizado': str
            }
        """
        return {
            "caminho": self._caminho,
            "tipo": self._determinar_tipo(),
            "existe": os.path.exists(self._caminho),
            "permissao": self._verificar_permissao(self._caminho),
            "normalizado": os.path.abspath(self._caminho),
        }

    def to_json(self, indent: int = 4) -> str:
        """
        Retorna metadados do caminho como JSON formatado.

        Args:
            indent: Número de espaços para indentação

        Returns:
            str: JSON formatado
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def __repr__(self) -> str:
        """Representação oficial do objeto."""
        return f"Caminho(caminho={self._caminho!r})"

    def __str__(self) -> str:
        """Representação amigável do caminho."""
        return self._caminho

    def __eq__(self, other) -> bool:
        """Compara dois objetos pelo caminho absoluto."""
        return isinstance(other, Caminho) and self._caminho == other._caminho


# Exemplo de uso
if __name__ == "__main__":
    try:
        # Criação do objeto
        caminho_obj = Caminho(".")  # Diretório atual

        # Acessando propriedade
        print(f"\nCaminho atual: {caminho_obj.caminho}")

        # Atualizando caminho com setter
        caminho_obj.caminho = ".."  # Diretório pai
        print(f"\nNovo caminho: {caminho_obj.caminho}")

        # Saída em diferentes formatos
        print("\nMetadados como dicionário:")
        print(caminho_obj.to_dict())

        print("\nMetadados como JSON:")
        print(caminho_obj.to_json())

        print("\nRepresentação do objeto:")
        print(repr(caminho_obj))

    except (TypeError, FileNotFoundError, PermissionError) as e:
        print(f"\nErro: {e}")
