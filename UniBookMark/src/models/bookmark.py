class Caminho:
    """Classe base que representa um caminho no sistema operacional"""

    def __init__(self, caminho: str):
        """Inicializa o caminho"""
        self.caminho = caminho

    def __str__(self):
        """Retorna a representação em string do caminho"""
        return self.caminho

    def __repr__(self):
        """Representação mais detalhada do caminho"""
        return f"Caminho(caminho={self.caminho!r})"

    def existe(self) -> bool:
        """Método para verificar se o caminho existe no sistema operacional.
        Este método seria uma simulação, em um projeto real você utilizaria funções do os.path ou pathlib.
        """
        raise NotImplementedError(
            "Este método precisa ser implementado nas subclasses."
        )


class Pasta(Caminho):
    """Classe que representa uma pasta no sistema operacional, herdando de Caminho"""

    def __init__(self, caminho: str):
        """Inicializa a pasta com o caminho"""
        super().__init__(caminho)

    def existe(self) -> bool:
        """Simula a verificação se a pasta existe"""
        # Em uma implementação real, você usaria os.path.isdir ou pathlib.Path.is_dir
        return self.caminho.endswith("/")

    def listar_conteudo(self):
        """Simula listar os conteúdos da pasta"""
        # Em uma implementação real, você usaria os.listdir ou pathlib.Path.iterdir
        return [f"{self.caminho}/arquivo1.txt", f"{self.caminho}/arquivo2.txt"]


class ArquivoTexto(Caminho):
    """Classe que representa um arquivo de texto no sistema operacional, herdando de Caminho"""

    def __init__(self, caminho: str, conteudo: str = ""):
        """Inicializa o arquivo de texto com o caminho e conteúdo opcional"""
        super().__init__(caminho)
        self.conteudo = conteudo

    def existe(self) -> bool:
        """Simula a verificação se o arquivo existe"""
        # Em uma implementação real, você usaria os.path.isfile ou pathlib.Path.is_file
        return not self.caminho.endswith("/")

    def ler(self) -> str:
        """Simula a leitura do conteúdo do arquivo"""
        return self.conteudo

    def escrever(self, novo_conteudo: str):
        """Escreve novo conteúdo no arquivo"""
        self.conteudo = novo_conteudo


# Exemplo de uso
if __name__ == "__main__":
    pasta = Pasta("/home/pedro/pasta1/")
    arquivo = ArquivoTexto(
        "/home/pedro/pasta1/arquivo1.txt", "Este é o conteúdo do arquivo."
    )

    print(f"Pasta existe? {pasta.existe()}")  # True
    print(f"Conteúdo da pasta: {pasta.listar_conteudo()}")

    print(f"Arquivo existe? {arquivo.existe()}")  # True
    print(f"Conteúdo do arquivo: {arquivo.ler()}")  # 'Este é o conteúdo do arquivo.'

    arquivo.escrever("Novo conteúdo no arquivo.")
    print(
        f"Conteúdo do arquivo após alteração: {arquivo.ler()}"
    )  # 'Novo conteúdo no arquivo.'
