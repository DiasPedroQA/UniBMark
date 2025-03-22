import json
import os
import sys
from pathlib import Path
from typing import Generator, Union

import pytest

# Adiciona o diretório raiz ao sys.path
sys.path.insert(
    0, os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../../src"
        )
    )
)

# Agora a importação funcionará
from models.caminhos import Caminho


@pytest.fixture
def arquivo_tmp(tmp_path: Path) -> Generator[Path, None, None]:
    """Cria um arquivo temporário para os testes."""
    arquivo: Path = tmp_path / "teste.txt"
    arquivo.write_text("conteúdo de teste")
    yield arquivo


@pytest.fixture
def diretorio_tmp(tmp_path: Path) -> Generator[Path, None, None]:
    """Cria um diretório temporário para os testes."""
    yield tmp_path


@pytest.fixture
def link_simbolico_tmp(
    tmp_path: Path, arquivo_tmp: Path
) -> Generator[Path, None, None]:
    """Cria um link simbólico apontando para um arquivo temporário."""
    link: Path = tmp_path / "link_teste"
    link.symlink_to(arquivo_tmp)
    yield link


def test_caminho_valido(arquivo_tmp: Path) -> None:
    """Testa se a classe aceita caminhos válidos."""
    caminho: Caminho = Caminho(str(arquivo_tmp))
    assert caminho.caminho == arquivo_tmp.resolve()


def test_caminho_inexistente() -> None:
    """Testa se um caminho inexistente levanta um erro."""
    with pytest.raises(FileNotFoundError):
        Caminho("/caminho/que/nao/existe")


def test_caminho_nao_string() -> None:
    """Testa se caminhos que não são string levantam erro."""
    with pytest.raises(TypeError):
        Caminho(123)  # type: ignore


def test_caminho_vazio() -> None:
    """Testa se uma string vazia levanta erro."""
    with pytest.raises(TypeError):
        Caminho("")


def test_permissao_negada(monkeypatch: pytest.MonkeyPatch, arquivo_tmp: Path) -> None:
    """Testa se a classe detecta permissão negada."""

    def fake_access(_path: str, _mode: int) -> bool:
        return False  # Simula falta de permissão

    monkeypatch.setattr(os, "access", fake_access)

    with pytest.raises(PermissionError):
        Caminho(str(arquivo_tmp))


def test_determinar_tipo_arquivo(arquivo_tmp: Path) -> None:
    """Testa se a classe identifica corretamente um arquivo."""
    caminho: Caminho = Caminho(str(arquivo_tmp))
    assert caminho._determinar_tipo() == "arquivo"


def test_determinar_tipo_diretorio(diretorio_tmp_1: Path) -> None:
    """Testa se a classe identifica corretamente um diretório."""
    caminho_obj: Caminho = Caminho(str(diretorio_tmp))
    assert caminho_obj._determinar_tipo() == "diretório"


def test_determinar_tipo_link_simbolico(link_simbolico_tmp: Path) -> None:
    """
    Testa se a classe identifica corretamente um link simbólico.
    """
    caminho_link: Caminho = Caminho(str(link_simbolico_tmp))
    assert caminho_link._determinar_tipo() == "link simbólico"


def test_to_dict(arquivo_tmp: Path) -> None:
    """Testa se o método to_dict() retorna as informações corretas."""
    caminho: Caminho = Caminho(str(arquivo_tmp))
    esperado: dict[str, Union[str, bool]] = {
        "caminho": str(arquivo_tmp.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_tmp.resolve()),
    }
    assert caminho.to_dict() == esperado


def test_to_json(arquivo_tmp: Path) -> None:
    """Testa se o método to_json() retorna um JSON válido e correto."""
    caminho: Caminho = Caminho(str(arquivo_tmp))
    resultado: dict[str, Union[str, bool]] = json.loads(caminho.to_json())
    esperado: dict[str, Union[str, bool]] = {
        "caminho": str(arquivo_tmp.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_tmp.resolve()),
    }
    assert resultado == esperado


# Lista de testes
caminhos_teste: list[Union[str, int, None]] = [
    "/storage/emulated/0/",  # Caminho válido (Android)
    "/home/pedro-pm-dias/Downloads",  # Caminho válido (Linux)
    "C:\\Users\\User\\arquivo.txt",  # Caminho válido absoluto (Windows)
    "/caminho/que/nao/existe",  # Caminho inexistente
    "12345",  # Entrada inválida (não é string)
    12345,  # Entrada inválida (não é string)
    "",  # String vazia (inválida)
    None,  # Valor nulo (inválido)
]

# Teste da classe
for caminho in caminhos_teste:
    print(f"\n\nTestando caminho: ({caminho})")
    print(f"Tipo do caminho: {type(caminho)}")
    try:
        obj_caminho: Caminho = (
            Caminho(str(caminho)) if isinstance(caminho, str) else Caminho("")
        )
        obj_json: str = obj_caminho.to_json()
        obj_dict: dict[str, Union[str, bool]] = obj_caminho.to_dict()
        print("JSON Output:")
        print(obj_json)
        print("\nDicionário Output:")
        print(obj_dict)
    except (TypeError, ValueError, FileNotFoundError, PermissionError, OSError) as e:
        print(f"Erro capturado: {e}")
