# """
# Este módulo define classes para representar caminhos no sistema
# operacional, incluindo pastas e arquivos de texto.

# Classes:
#     Caminho: Classe base que representa um caminho genérico no sistema operacional.
#     Pasta: Subclasse de Caminho que representa uma pasta no sistema operacional.
#     Arquivo: Subclasse de Caminho que representa um arquivo de texto no sistema operacional.

# Classes e Métodos:
#     Caminho:
#         __init__(self, caminho: str): Inicializa o caminho.
#         __str__(self): Retorna a representação em string do caminho.
#         __repr__(self): Retorna uma representação mais detalhada do caminho.
#         existe(self) -> bool: Verifica se o caminho existe no sistema
#         operacional (deve ser implementado nas subclasses).

#     Pasta(Caminho):
#         __init__(self, caminho: str): Inicializa a pasta com o caminho.
#         existe(self) -> bool: Verifica se a pasta existe (simulação).
#         listar_conteudo(self): Lista os conteúdos da pasta (simulação).

#     Arquivo(Caminho):
#         __init__(self, caminho: str, conteudo: str = ""): Inicializa o
#         arquivo de texto com o caminho e conteúdo opcional.
#         existe(self) -> bool: Verifica se o arquivo existe (simulação).
#         ler(self) -> str: Lê o conteúdo do arquivo (simulação).
#         escrever(self, novo_conteudo: str): Escreve novo conteúdo no arquivo.
# """


# class Caminho:
#     """Classe base para representar um caminho no sistema operacional."""

#     def __init__(self, caminho: str):
#         """Inicializa o caminho."""
#         self.caminho = caminho

#     def __str__(self):
#         """Retorna o caminho como string."""
#         return self.caminho

#     def __repr__(self):
#         """Retorna uma representação detalhada do caminho."""
#         return f"Caminho({self.caminho!r})"

#     @property
#     def caminho_absoluto(self):
#         """Retorna o caminho absoluto simulado."""
#         return f"/simulado{self.caminho}"


# class Pasta:
#     """Classe que representa uma pasta."""

#     def __init__(self, caminho: str):
#         """Inicializa a pasta com o caminho."""
#         self.caminho = Caminho(caminho).caminho

#     def existe(self) -> bool:
#         """Simula a verificação da existência da pasta."""
#         return self.caminho.endswith("/")

#     def listar_conteudo(self):
#         """Simula a listagem do conteúdo da pasta."""
#         return [f"{self.caminho}arquivo1.txt", f"{self.caminho}arquivo2.txt"]

#     @property
#     def nome(self):
#         """Retorna o nome da pasta."""
#         return self.caminho.strip("/").split("/")[-1]


# class Arquivo:
#     """Classe que representa um arquivo de texto."""

#     def __init__(self, caminho: str, conteudo: str = ""):
#         """Inicializa o arquivo com caminho e conteúdo opcional."""
#         self.caminho = Caminho(caminho).caminho
#         self.conteudo = conteudo

#     def existe(self) -> bool:
#         """Simula a verificação da existência do arquivo."""
#         return not self.caminho.endswith("/")

#     def ler(self) -> str:
#         """Retorna o conteúdo do arquivo."""
#         return self.conteudo

#     def escrever(self, novo_conteudo: str):
#         """Altera o conteúdo do arquivo."""
#         self.conteudo = novo_conteudo

#     @property
#     def extensao(self):
#         """Retorna a extensão do arquivo."""
#         return self.caminho.split(".")[-1] if "." in self.caminho else ""


# # Exemplo de uso
# if __name__ == "__main__":
#     pasta = Pasta("/home/pedro-pm-dias/Downloads/Firefox/")
#     arquivo = Arquivo(
#         "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
#         "Este é o conteúdo do arquivo.",
#     )

#     print(f"Pasta existe? {pasta.existe()}")
#     print(f"Nome da pasta: {pasta.nome}")
#     print(f"Conteúdo da pasta: {pasta.listar_conteudo()}")

#     print(f"Arquivo existe? {arquivo.existe()}")
#     print(f"Extensão do arquivo: {arquivo.extensao}")
#     print(f"Conteúdo do arquivo: {arquivo.ler()}")

#     arquivo.escrever("Novo conteúdo no arquivo.")
#     print(f"Conteúdo do arquivo após alteração: {arquivo.ler()}")
