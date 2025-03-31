import os
import re


class CaminhoVazioErro(Exception):
    """Exceção levantada quando o caminho fornecido está vazio ou contém apenas espaços."""

    def __init__(
        self, mensagem: str = "O caminho não pode ser vazio ou conter apenas espaços."
    ) -> None:
        """
        Inicializa a exceção com uma mensagem personalizada.

        Args:
            mensagem (str): Mensagem de erro a ser exibida.
            Padrão é "O caminho não pode ser vazio ou conter apenas espaços."
        """
        super().__init__(mensagem)


class CaminhoInvalidoErro(Exception):
    """Exceção levantada quando o caminho fornecido é inválido."""

    def __init__(self, mensagem: str = "O caminho fornecido é inválido.") -> None:
        """
        Inicializa a exceção com uma mensagem personalizada.

        Args:
            mensagem (str): Mensagem de erro a ser exibida.
            Padrão é "O caminho fornecido é inválido."
        """
        super().__init__(mensagem)


class ValidadorCaminho:
    """Classe responsável por validar caminhos de arquivos ou diretórios."""

    def __init__(self, caminho: str) -> None:
        """
        Inicializa a classe de validação de caminho.

        Args:
            caminho (str): O caminho do arquivo ou diretório a ser validado.

        Levanta:
            CaminhoVazioErro: Se o caminho for vazio ou contiver apenas espaços.
            CaminhoInvalidoErro: Se o caminho for inválido de acordo com o sistema operacional.
        """
        caminho = caminho.strip()  # Remove espaços extras no início e fim
        if not caminho:
            raise CaminhoVazioErro()
        self.caminho: str = caminho
        self.sistema_operacional: str = os.name  # 'posix' para Linux/Mac, 'nt' para Windows
        self.validar_caminho()

    def validar_caminho(self) -> None:
        """
        Valida o caminho com base no sistema operacional.

        Levanta:
            CaminhoInvalidoErro: Se o caminho não for válido para o sistema operacional atual.
        """
        if self.sistema_operacional == "nt":  # Windows
            padrao: str = r"^[a-zA-Z]:\\(?:[^<>:\"/\\|?*\r\n]+\\?)*$"
            if not re.match(padrao, self.caminho):
                raise CaminhoInvalidoErro(
                    "O caminho não é válido para o sistema operacional atual."
                )
        elif self.sistema_operacional == "posix":  # Linux/Mac
            padrao_posix: str = r"^(/[^<>:\"|?*\r\n]+)+/?$"
            if not re.match(padrao_posix, self.caminho):
                raise CaminhoInvalidoErro(
                    "O caminho não é válido para o sistema operacional atual."
                )
        else:
            raise CaminhoInvalidoErro("Sistema operacional não suportado.")

    def obter_caminho(self) -> str:
        """
        Retorna o caminho validado.

        Returns:
            str: O caminho fornecido, após ser validado.

        Levanta:
            CaminhoVazioErro: Se o caminho estiver vazio.
            CaminhoInvalidoErro: Se o caminho for inválido.
        """
        return self.caminho

    def obter_sistema_operacional(self) -> str:
        """
        Retorna o sistema operacional detectado.

        Returns:
            str: O sistema operacional ('posix' ou 'nt').
        """
        return self.sistema_operacional

    def caminho_eh_valido(self) -> bool:
        """
        Verifica se o caminho fornecido é válido.

        Returns:
            bool: True se o caminho for válido, False caso contrário.

        Levanta:
            CaminhoVazioErro: Se o caminho estiver vazio.
            CaminhoInvalidoErro: Se o caminho for inválido.
        """
        try:
            self.validar_caminho()
            return True
        except CaminhoInvalidoErro:
            return False
