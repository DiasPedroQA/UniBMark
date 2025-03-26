# pylint: disable=W0212, C0116

"""
Este módulo contém testes para a classe `Caminho` localizada em `src.models.caminhos`.
Os testes abrangem a inicialização, propriedades, métodos e comportamentos esperados
da classe, incluindo cenários de sucesso e falha.

Testes incluem:
- Inicialização com caminhos válidos e inválidos.
- Validação de permissões e tipos de caminho.
- Métodos de conversão para dicionário e JSON.
- Métodos especiais como `__str__`.
- Uso de mocks para simular comportamentos específicos.

Nota: Este módulo utiliza o framework pytest para a execução dos testes.

"""


from unittest.mock import patch

import pytest

from src.models.caminhos import Caminho, PathError, PathType


@pytest.fixture
def valid_file_path(tmp_path):
    """Cria um arquivo temporário válido para os testes."""
    file = tmp_path / "valid_file.txt"
    file.write_text("conteúdo de teste")
    return file


@pytest.fixture
def valid_dir_path(tmp_path):
    """Cria um diretório temporário válido para os testes."""
    dir_path = tmp_path / "valid_dir"
    dir_path.mkdir()
    return dir_path


@pytest.fixture
def invalid_path():
    """Retorna um caminho inválido."""
    return "/caminho/inexistente"


def test_caminho_valid_file(file_path_fixture):
    caminho = Caminho(str(file_path_fixture))
    assert caminho.is_valid is True
    assert caminho.type == PathType.FILE
    assert caminho.path == file_path_fixture.resolve()
    assert caminho.error is None
    assert caminho.to_dict()["permissions"]["readable"] is True
    assert caminho.to_dict()["permissions"]["writable"] is True


def test_caminho_valid_directory(valid_directory_path):
    caminho = Caminho(str(valid_directory_path))
    assert caminho.is_valid is True
    assert caminho.type == PathType.DIR
    assert caminho.path == valid_directory_path.resolve()
    assert caminho.error is None


def test_caminho_invalid_path(invalid_path_fixture):
    caminho = Caminho(invalid_path_fixture)
    assert caminho.is_valid is False
    assert caminho.type == PathType.INVALID
    assert caminho.path is None
    assert isinstance(caminho.error, PathError)
    assert caminho.error.type == "FileNotFoundError"


def test_caminho_permission_error(file_path_fixture):
    with patch("os.access", return_value=False):
        caminho = Caminho(str(file_path_fixture))
        assert caminho.is_valid is False
        assert caminho.type == PathType.INVALID
        assert caminho.error.type == "PermissionError"


def test_caminho_to_dict(file_path):
    caminho = Caminho(str(file_path))
    caminho_dict = caminho.to_dict()
    assert caminho_dict["raw_path"] == str(file_path)
    assert caminho_dict["is_valid"] is True
    assert caminho_dict["type"] == PathType.FILE.value
    assert caminho_dict["resolved_path"] == str(file_path.resolve())


def test_caminho_to_dict_invalid(invalid_path_fixture):
    caminho = Caminho(invalid_path_fixture)
    caminho_dict = caminho.to_dict()
    assert caminho_dict["raw_path"] == invalid_path_fixture
    assert caminho_dict["is_valid"] is False
    assert caminho_dict["type"] == PathType.INVALID.value
    assert "error" in caminho_dict
    assert caminho_dict["error"]["type"] == "FileNotFoundError"


def test_caminho_str(file_path_fixture):
    caminho = Caminho(str(file_path_fixture))
    assert str(caminho) == str(file_path_fixture)


def test_caminho_symlink(tmp_path):
    target = tmp_path / "target_file.txt"
    target.write_text("conteúdo de teste")
    symlink = tmp_path / "symlink"
    symlink.symlink_to(target)

    caminho = Caminho(str(symlink))
    assert caminho.is_valid is True
    assert caminho.type == PathType.SYMLINK
    assert caminho.path == symlink.resolve()
