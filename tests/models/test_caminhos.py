import pytest

from src.models.caminhos import CaminhoInvalidoErro, CaminhoVazioErro, ValidadorCaminho


def test_validador_caminho_vazio() -> None:
    with pytest.raises(CaminhoVazioErro) as excinfo:
        ValidadorCaminho("")
    assert str(excinfo.value) == "O caminho não pode ser vazio ou conter apenas espaços."


def test_validador_caminho_apenas_espacos() -> None:
    with pytest.raises(CaminhoVazioErro) as excinfo:
        ValidadorCaminho("   ")
    assert str(excinfo.value) == "O caminho não pode ser vazio ou conter apenas espaços."


def test_validador_caminho_invalido_windows() -> None:
    # monkeypatch.setattr("os.name", "nt")
    with pytest.raises(CaminhoInvalidoErro) as excinfo:
        ValidadorCaminho("C:/invalid|path")
    assert str(excinfo.value) == "O caminho não é válido para o sistema operacional atual."


def test_validador_caminho_invalido_posix() -> None:
    with pytest.raises(CaminhoInvalidoErro) as excinfo:
        ValidadorCaminho("/invalid|path")
    assert str(excinfo.value) == "O caminho não é válido para o sistema operacional atual."


def test_validador_caminho_valido_posix() -> None:
    caminho = "/valid/path"
    validador = ValidadorCaminho(caminho)
    assert validador.obter_caminho() == caminho
    assert validador.obter_sistema_operacional() == "posix"
    assert validador.caminho_eh_valido()


def test_validador_caminho_sistema_operacional_nao_suportado() -> None:
    with pytest.raises(CaminhoInvalidoErro) as excinfo:
        ValidadorCaminho("/invalid/path")
    assert str(excinfo.value) == "Sistema operacional não suportado."
