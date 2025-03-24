# Author: Pedro Paulo Machado Dias
# Date: 2021-06-27
# Description: Testes para a classe Caminho.

# pylint: disable=wrong-import-order, wrong-import-position, import-error, redefined-outer-name, protected-access

"""
Módulo de testes para a classe Caminho.

Testa diversas funcionalidades, incluindo a verificação de tipos, permissões e conversão para JSON.
"""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.models.caminhos import Caminho


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("/home/pedro-pm-dias/Downloads/Firefox/", True),
        # ("C:\\Users\\User\\arquivo.txt", True),
        ("/caminho/inexistente", False),
        ("", False),
        (12345, False),
        (None, False),
    ],
)
def test_validacao_caminho(entrada, esperado):
    """Testa diferentes cenários de validação de caminho."""
    if esperado:
        caminho = Caminho(str(entrada))
        assert caminho.caminho.exists()
    else:
        with pytest.raises((TypeError, FileNotFoundError, ValueError)):
            Caminho(str(entrada))


@pytest.fixture
def arquivo_temporario(tmp_path: Path):
    """Cria um arquivo temporário para os testes."""
    arquivo = tmp_path / "arquivo_teste.txt"
    arquivo.write_text("conteúdo de teste")
    return arquivo


@pytest.fixture
def diretorio_temporario(tmp_path: Path):
    """Cria um diretório temporário para os testes."""
    return tmp_path


@pytest.fixture
def mock_permissao_negada():
    """Mock para simular permissão negada."""
    with patch("os.access", return_value=False):
        yield


def test_permissao_negada(arquivo_temporario):
    """Testa se a classe detecta um arquivo sem permissão de leitura/escrita."""
    with pytest.raises(PermissionError):
        Caminho(str(arquivo_temporario))


def test_to_dict(arquivo_temporario):
    """Testa se o método to_dict() retorna um dicionário válido e correto."""
    caminho = Caminho(str(arquivo_temporario))
    dict_result = caminho.to_dict()
    esperado = {
        "caminho": str(arquivo_temporario.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_temporario.resolve()),
    }
    assert dict_result == esperado


def test_to_json(arquivo_temporario):
    """Testa se o método to_json() retorna um JSON válido e correto."""
    caminho = Caminho(str(arquivo_temporario))
    json_result = caminho.to_json()
    esperado = {
        "caminho": str(arquivo_temporario.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_temporario.resolve()),
    }
    assert json.loads(json_result) == esperado


def test_caminho_relativo(diretorio_temporario):
    """Testa se caminhos relativos são convertidos corretamente para absolutos."""
    caminho_relativo = diretorio_temporario / "subdir" / "arquivo.txt"
    caminho_relativo.parent.mkdir(parents=True)
    caminho_relativo.write_text("teste")
    caminho = Caminho(str(caminho_relativo.relative_to(diretorio_temporario)))
    assert caminho.caminho == caminho_relativo.resolve()


def test_determinar_tipo_arquivo(arquivo_temporario):
    """Testa se o tipo do caminho é corretamente identificado como arquivo."""
    caminho = Caminho(str(arquivo_temporario))
    assert caminho.to_dict()["tipo"] == "arquivo"


def test_determinar_tipo_diretorio(diretorio_temporario):
    """Testa se o tipo do caminho é corretamente identificado como diretório."""
    caminho = Caminho(str(diretorio_temporario))
    assert caminho.to_dict()["tipo"] == "diretório"


def test_determinar_tipo_link_simbolico(tmp_path: Path):
    """Testa se o tipo do caminho é corretamente identificado como link simbólico."""
    arquivo = tmp_path / "arquivo_teste.txt"
    arquivo.write_text("conteúdo de teste")
    link = tmp_path / "link_teste"
    link.symlink_to(arquivo)
    caminho = Caminho(str(link))
    assert caminho.to_dict()["tipo"] == "link simbólico"
    caminho = Caminho(str(link))
    assert caminho.to_dict()["tipo"] == "link simbólico"
