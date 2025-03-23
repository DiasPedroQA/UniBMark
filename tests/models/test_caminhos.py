# Author: Pedro Paulo Machado Dias
# Date: 2021-06-27
# Description: Testes para a classe Caminho.

# pylint: disable=wrong-import-order, wrong-import-position, import-error, redefined-outer-name, protected-access

"""
Módulo de testes para a classe Caminho.

Testa diversas funcionalidades, incluindo a verificação de tipos, permissões e conversão para JSON.
"""

import json
import os
import sys
from pathlib import Path
from typing import Generator, Union

import pytest

# Adiciona o diretório raiz ao sys.path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

# Agora a importação funcionará
from src.models.caminhos import Caminho


@pytest.fixture
def arquivo_temporario(tmp_path: Path) -> Generator[Path, None, None]:
    """Cria um arquivo temporário para os testes."""
    arquivo_temp: Path = tmp_path / "teste.txt"
    arquivo_temp.write_text("conteúdo de teste")
    yield arquivo_temp


@pytest.fixture
def diretorio_temporario(tmp_path: Path) -> Generator[Path, None, None]:
    """Cria um diretório temporário para os testes."""
    yield tmp_path


@pytest.fixture
def link_simbolico_temporario(
    tmp_path: Path, arquivo_temporario: Path
) -> Generator[Path, None, None]:
    """Cria um link simbólico apontando para um arquivo temporário."""
    link_temp: Path = tmp_path / "link_teste"
    link_temp.symlink_to(arquivo_temporario)
    yield link_temp


def test_caminho_valido(arquivo_temporario: Path) -> None:
    """Testa se a classe aceita caminhos válidos."""
    caminho_obj: Caminho = Caminho(str(arquivo_temporario))
    assert caminho_obj.caminho == arquivo_temporario.resolve()


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


def test_permissao_negada(
    monkeypatch: pytest.MonkeyPatch, arquivo_temporario: Path
) -> None:
    """Testa se a classe detecta permissão negada."""

    def simular_falta_permissao(_path: str, _mode: int) -> bool:
        return False  # Simula falta de permissão

    monkeypatch.setattr(os, "access", simular_falta_permissao)

    with pytest.raises(PermissionError):
        Caminho(str(arquivo_temporario))


def test_determinar_tipo_arquivo(arquivo_temporario: Path) -> None:
    """Testa se a classe identifica corretamente um arquivo."""
    caminho_obj: Caminho = Caminho(str(arquivo_temporario))
    assert caminho_obj._determinar_tipo() == "arquivo"


def test_determinar_tipo_diretorio(diretorio_temporario: Path) -> None:
    """Testa se a classe identifica corretamente um diretório."""
    caminho_obj: Caminho = Caminho(str(diretorio_temporario))
    assert caminho_obj._determinar_tipo() == "diretório"


def test_determinar_tipo_link_simbolico(link_simbolico_temporario: Path) -> None:
    """Testa se a classe identifica corretamente um link simbólico."""
    caminho_obj: Caminho = Caminho(str(link_simbolico_temporario))
    assert caminho_obj._determinar_tipo() == "link simbólico"


def test_to_dict(arquivo_temporario: Path) -> None:
    """Testa se o método to_dict() retorna as informações corretas."""
    caminho_obj: Caminho = Caminho(str(arquivo_temporario))
    esperado_dict: dict[str, str | bool] = {
        "caminho": str(arquivo_temporario.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_temporario.resolve()),
    }
    assert caminho_obj.to_dict() == esperado_dict


def test_to_json(arquivo_temporario: Path) -> None:
    """Testa se o método to_json() retorna um JSON válido e correto."""
    caminho_obj: Caminho = Caminho(str(arquivo_temporario))
    resultado_json: dict[str, str | bool] = json.loads(caminho_obj.to_json())
    esperado_json: dict[str, str | bool] = {
        "caminho": str(arquivo_temporario.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_temporario.resolve()),
    }
    assert resultado_json == esperado_json


# Lista de testes
lista_caminhos_teste: list[Union[str, int, None]] = [
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
for caminho_teste in lista_caminhos_teste:
    print(f"\n\nTestando caminho: ({caminho_teste})")
    print(f"Tipo do caminho: {type(caminho_teste)}")
    try:
        caminho_obj: Caminho = (
            Caminho(str(caminho_teste))
            if isinstance(caminho_teste, str)
            else Caminho("")
        )
        objeto_json: str = caminho_obj.to_json()
        objeto_dict: dict[str, Union[str, bool, None]] = caminho_obj.to_dict()
        print("JSON Output:")
        print(objeto_json)
        print("\nDicionário Output:")
        print(objeto_dict)
    except (TypeError, ValueError, FileNotFoundError, PermissionError, OSError) as erro:
        print(f"Erro capturado: {erro}")
