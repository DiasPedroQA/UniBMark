# Código Ajustado e Completo:

import os
import re
from typing import Union

# 1. **CaminhoErro** e suas subclasses:


class CaminhoErro(Exception):
    """Exceção base para erros relacionados a validação de caminhos."""
    def __init__(self, mensagem: str) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem


class CaminhoVazioErro(CaminhoErro):
    """Exceção levantada quando o caminho fornecido está vazio ou contém apenas espaços."""
    def __init__(
        self,
        mensagem: str = "O caminho não pode ser vazio ou conter apenas espaços."
    ) -> None:
        super().__init__(mensagem)


class CaminhoInvalidoErro(CaminhoErro):
    """Exceção levantada quando o caminho fornecido é inválido."""
    def __init__(self, mensagem: str = "O caminho fornecido é inválido.") -> None:
        super().__init__(mensagem)


# 2. **ValidadorBase** (Classe Base):

class ValidadorBase:
    """Classe base para validadores genéricos."""
    def __init__(self, entrada: Union[str, os.PathLike]) -> None:
        self.entrada = str(entrada).strip()
        if not self.entrada:
            raise CaminhoVazioErro()

    def validar(self) -> None:
        """Método que deve ser implementado por subclasses para validação específica."""
        raise NotImplementedError("O método 'validar' deve ser implementado na subclasse.")

    def obter_entrada(self) -> str:
        """Retorna a entrada validada."""
        return self.entrada


# 3. **ValidadorCaminho** (Validador para Caminhos):

class ValidadorCaminho(ValidadorBase):
    """Validador para caminhos de arquivos ou diretórios."""
    def __init__(self, entrada: Union[str, os.PathLike]) -> None:
        super().__init__(entrada)
        self.sistema_operacional = os.name  # 'posix' para Linux/Mac, 'nt' para Windows
        self.validar()

    def validar(self) -> None:
        """Valida o caminho com base no sistema operacional."""
        if self.sistema_operacional == "nt":  # Windows
            padrao = r"^[a-zA-Z]:\\(?:[^<>:\"/\\|?*\r\n]+\\?)*$"
            if not re.match(padrao, self.entrada):
                raise CaminhoInvalidoErro(
                    "O caminho não é válido para o sistema operacional atual.")
        elif self.sistema_operacional == "posix":  # Linux/Mac
            padrao_posix = r"^(/[^<>:\"|?*\r\n]+)+/?$"
            if not re.match(padrao_posix, self.entrada):
                raise CaminhoInvalidoErro(
                    "O caminho não é válido para o sistema operacional atual.")
        else:
            raise CaminhoInvalidoErro("Sistema operacional não suportado.")


# 4. **ValidadorURL** (Validador para URLs):

class ValidadorURL(ValidadorBase):
    """Validador para URLs."""
    def validar(self) -> None:
        """Valida se a entrada é uma URL válida."""
        padrao_url = r"^(https?|ftp)://[^\s/$.?#].[^\s]*$"
        if not re.match(padrao_url, self.entrada):
            raise CaminhoInvalidoErro("A URL fornecida é inválida.")


# 5. **Validador** (Classe principal para validação genérica):

class Validador:
    """Classe principal para validação genérica."""
    def __init__(self, entrada: Union[str, os.PathLike], tipo: str = "caminho") -> None:
        """
        Inicializa o validador com base no tipo de entrada.

        Args:
            entrada (Union[str, os.PathLike]): A entrada a ser validada.
            tipo (str): O tipo de validação ('caminho' ou 'url').
        """
        self.entrada = entrada
        self.tipo = tipo.lower()
        self.validador = self._selecionar_validador()

    def _selecionar_validador(self) -> ValidadorBase:
        """Seleciona o validador apropriado com base no tipo."""
        if self.tipo == "caminho":
            return ValidadorCaminho(self.entrada)
        if self.tipo == "url":
            return ValidadorURL(self.entrada)
        raise ValueError(f"Tipo de validação '{self.tipo}' não suportado.")

    def validar(self) -> None:
        """Executa a validação usando o validador apropriado."""
        self.validador.validar()

    def obter_entrada(self) -> str:
        """Retorna a entrada validada."""
        return self.validador.obter_entrada()


# Exemplos de Uso:

# 1. **ValidadorCaminho (Validação de Caminhos):**


# Exemplo de uso do ValidadorCaminho
try:
    caminho_valido = ValidadorCaminho("C:/MeusArquivos/teste.txt")
    print(f"Caminho válido: {caminho_valido.obter_entrada()}")
except CaminhoErro as e:
    print(f"Erro: {e}")

# Exemplo de caminho inválido no Windows
try:
    caminho_invalido = ValidadorCaminho("C:/MeusArquivos/<teste>.txt")
except CaminhoErro as e:
    print(f"Erro: {e}")


# 2. **ValidadorURL (Validação de URLs):**

# Exemplo de uso do ValidadorURL
try:
    url_valida = ValidadorURL("https://www.exemplo.com")
    print(f"URL válida: {url_valida.obter_entrada()}")
except CaminhoErro as e:
    print(f"Erro: {e}")

# Exemplo de URL inválida
try:
    url_invalida = ValidadorURL("htp://www.exemplo.com")
except CaminhoErro as e:
    print(f"Erro: {e}")


# 3. **Validador (Validação Genérica):**

# Exemplo de uso do Validador com caminho
try:
    validador = Validador("C:/MeusArquivos/teste.txt", tipo="caminho")
    validador.validar()
    print(f"Caminho validado: {validador.obter_entrada()}")
except CaminhoErro as e:
    print(f"Erro: {e}")

# Exemplo de uso do Validador com URL
try:
    validador_url = Validador("https://www.exemplo.com", tipo="url")
    validador_url.validar()
    print(f"URL validada: {validador_url.obter_entrada()}")
except CaminhoErro as e:
    print(f"Erro: {e}")
