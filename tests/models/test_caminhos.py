import pytest
from _pytest.monkeypatch import MonkeyPatch

from src.models.caminhos import CaminhoInvalidoErro, CaminhoVazioErro, ValidadorCaminho


def test_validador_caminho_vazio() -> None:
    with pytest.raises(CaminhoVazioErro) as excinfo:
        ValidadorCaminho("")
    assert str(excinfo.value) == "O caminho não pode ser vazio ou conter apenas espaços."


def test_validador_caminho_apenas_espacos() -> None:
    with pytest.raises(CaminhoVazioErro) as excinfo:
        ValidadorCaminho("   ")
    assert str(excinfo.value) == "O caminho não pode ser vazio ou conter apenas espaços."


def test_validador_caminho_invalido_windows(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("os.name", "nt")
    with pytest.raises(CaminhoInvalidoErro) as excinfo:
        ValidadorCaminho("C:/invalid|path")
    assert str(excinfo.value) == "O caminho não é válido para o sistema operacional atual."


def test_validador_caminho_invalido_posix(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("os.name", "posix")
    with pytest.raises(CaminhoInvalidoErro) as excinfo:
        ValidadorCaminho("/invalid|path")
    assert str(excinfo.value) == "O caminho não é válido para o sistema operacional atual."


def test_validador_caminho_valido_windows(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("os.name", "nt")
    caminho = "C:\\valid\\path"
    validador = ValidadorCaminho(caminho)
    assert validador.obter_caminho() == caminho
    assert validador.obter_sistema_operacional() == "nt"
    assert validador.caminho_eh_valido()


def test_validador_caminho_valido_posix(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("os.name", "posix")
    caminho = "/valid/path"
    validador = ValidadorCaminho(caminho)
    assert validador.obter_caminho() == caminho
    assert validador.obter_sistema_operacional() == "posix"
    assert validador.caminho_eh_valido()


def test_validador_caminho_sistema_operacional_nao_suportado(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr("os.name", "unsupported_os")
    with pytest.raises(CaminhoInvalidoErro) as excinfo:
        ValidadorCaminho("/valid/path")
    assert str(excinfo.value) == "Sistema operacional não suportado."
