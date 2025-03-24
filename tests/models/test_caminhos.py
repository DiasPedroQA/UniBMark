# Author: Pedro Paulo Machado Dias
# Date: 2021-06-27
# Description: Testes para a classe Caminho.

# pylint: disable=wrong-import-order, wrong-import-position, import-error, redefined-outer-name, protected-access

"""
Módulo de testes para a classe Caminho.

Testa diversas funcionalidades, incluindo a verificação de tipos, permissões e conversão para JSON.
"""


import os

import pytest

from src.models.caminhos import Caminho


@pytest.fixture
def mock_valid_path(tmp_path):
    """Cria um caminho válido temporário para os testes."""
    valid_path = tmp_path / "valid_dir"
    valid_path.mkdir()
    return str(valid_path)


@pytest.fixture
def mock_invalid_path():
    """Retorna um caminho inválido para os testes."""
    return "/invalid/path/that/does/not/exist"


def test_caminho_instantiation_with_valid_path(mock_valid_path):
    """Testa a criação de um objeto Caminho com um caminho válido."""
    caminho = Caminho(mock_valid_path)
    assert caminho.caminho == os.path.abspath(mock_valid_path)


def test_caminho_instantiation_with_invalid_path(mock_invalid_path):
    """Testa a criação de um objeto Caminho com um caminho inválido."""
    with pytest.raises(FileNotFoundError):
        Caminho(mock_invalid_path)


def test_caminho_instantiation_with_empty_string():
    """Testa a criação de um objeto Caminho com uma string vazia."""
    with pytest.raises(TypeError):
        Caminho("")


def test_caminho_instantiation_with_non_string():
    """Testa a criação de um objeto Caminho com um tipo não string."""
    with pytest.raises(TypeError):
        Caminho(12345)


def test_caminho_permission_error(tmp_path):
    """Testa a criação de um objeto Caminho sem permissões de leitura/escrita."""
    no_permission_path = tmp_path / "no_permission_dir"
    no_permission_path.mkdir()
    os.chmod(no_permission_path, 0o000)  # Remove todas as permissões

    try:
        with pytest.raises(PermissionError):
            Caminho(str(no_permission_path))
    finally:
        os.chmod(no_permission_path, 0o777)  # Restaura as permissões


def test_caminho_to_dict(mock_valid_path):
    """Testa o método to_dict da classe Caminho."""
    caminho = Caminho(mock_valid_path)
    caminho_dict = caminho.to_dict()
    assert caminho_dict["caminho"] == os.path.abspath(mock_valid_path)
    assert caminho_dict["tipo"] == "diretório"
    assert caminho_dict["existe"] is True
    assert caminho_dict["permissao"] is True
    assert caminho_dict["normalizado"] == os.path.abspath(mock_valid_path)


def test_caminho_to_json(mock_valid_path):
    """Testa o método to_json da classe Caminho."""
    caminho = Caminho(mock_valid_path)
    caminho_json = caminho.to_json()
    assert isinstance(caminho_json, str)
    assert '"caminho":' in caminho_json
    assert '"tipo": "diretório"' in caminho_json


def test_caminho_equality(mock_valid_path, tmp_path):
    """Testa a igualdade entre dois objetos Caminho."""
    another_valid_path = tmp_path / "another_valid_dir"
    another_valid_path.mkdir()

    caminho1 = Caminho(mock_valid_path)
    caminho2 = Caminho(mock_valid_path)
    caminho3 = Caminho(str(another_valid_path))

    assert caminho1 == caminho2
    assert caminho1 != caminho3
