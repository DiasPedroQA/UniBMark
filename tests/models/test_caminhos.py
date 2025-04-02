import pytest

from src.models.caminhos import (
    CaminhoInvalidoErro,
    CaminhoVazioErro,
    Validador,
    ValidadorCaminho,
    ValidadorURL,
)


# 1. Testes para ValidadorBase via ValidadorCaminho
def test_caminho_vazio() -> None:
    """Testa se um erro é levantado ao passar um caminho vazio."""
    with pytest.raises(CaminhoVazioErro):
        ValidadorCaminho("  ")  # Apenas espaços


# 2. Testes para ValidadorCaminho
@pytest.mark.parametrize(
    "caminho", ["C:\\Users\\teste\\arquivo.txt", "/home/user/arquivo.txt"]  # Windows  # Linux/Mac
)
def test_caminho_valido(caminho: str) -> None:
    """Testa caminhos válidos em diferentes sistemas operacionais."""
    validador = ValidadorCaminho(caminho)
    assert validador.obter_entrada() == caminho


@pytest.mark.parametrize(
    "caminho",
    [
        "C:\\Users\\<>?\\arquivo.txt",  # Windows inválido
        "/home/user/|arquivo.txt",  # Linux inválido
    ],
)
def test_caminho_invalido(caminho: str) -> None:
    """Testa caminhos inválidos."""
    with pytest.raises(CaminhoInvalidoErro):
        ValidadorCaminho(caminho)


# 3. Testes para ValidadorURL
@pytest.mark.parametrize(
    "url",
    [
        "https://www.exemplo.com",
        "http://meusite.com/path/to/page",
        "ftp://ftp.exemplo.com/arquivo.zip",
    ],
)
def test_url_valida(url: str) -> None:
    """Testa URLs válidas."""
    validador = ValidadorURL(url)
    assert validador.obter_entrada() == url


@pytest.mark.parametrize(
    "url", ["htp://www.exemplo.com", "http:/exemplo.com", "www.exemplo.com", "ftp:/ftp.exemplo.com"]
)
def test_url_invalida(url: str) -> None:
    """Testa URLs inválidas."""
    with pytest.raises(CaminhoInvalidoErro):
        ValidadorURL(url)


# 4. Testes para Validador Genérico
def test_validador_generico_caminho() -> None:
    """Testa a classe Validador genérica com caminhos."""
    validador = Validador("C:\\Users\\teste\\arquivo.txt", tipo="caminho")
    assert validador.obter_entrada() == "C:\\Users\\teste\\arquivo.txt"


def test_validador_generico_url() -> None:
    """Testa a classe Validador genérica com URLs."""
    validador = Validador("https://www.exemplo.com", tipo="url")
    assert validador.obter_entrada() == "https://www.exemplo.com"


def test_validador_tipo_invalido() -> None:
    """Testa um tipo inválido na classe Validador."""
    with pytest.raises(ValueError):
        Validador("alguma_coisa", tipo="desconhecido")
