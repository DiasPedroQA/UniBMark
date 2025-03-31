# pylint: disable=missing-module-docstring

from unittest.mock import MagicMock, patch

import pytest

from models.path_validator import PathValidator


# ========================
# Testes de Validação de Caminho
# ========================
class TestPathValidation:
    @pytest.mark.parametrize(
        "input_path, expected",
        [
            ("/home/user/file.txt", True),
            ("C:\\Users\\file.txt", True),
            ("invalid:/path", False),
            ("", False),
        ],
    )
    def test_validate_path_syntax(self, input_path: str, expected: bool) -> None:
        validator = PathValidator().set_path(input_path)
        assert validator.is_valid() == expected

    @pytest.mark.parametrize(
        "input_path, expected",
        [
            ("/home/user/file.txt", True),
            ("C:\\Users\\file.txt", True),
            ("file.txt", False),
            ("./file.txt", False),
        ],
    )
    def test_is_absolute(self, input_path: str, expected: bool) -> None:
        validator = PathValidator().set_path(input_path)
        assert validator.is_absolute() == expected


# ========================
# Testes de Existência e Tipo do Caminho
# ========================
class TestPathExistenceAndType:
    @patch("pathlib.Path.exists", return_value=True)
    def test_exists(self) -> None:
        validator = PathValidator().set_path("/home/user/file.txt")
        assert validator.exists() is True

    @patch("pathlib.Path.exists", return_value=False)
    def test_not_exists(self) -> None:
        validator = PathValidator().set_path("/home/user/file.txt")
        assert validator.exists() is False

    @pytest.mark.parametrize(
        "is_file, is_dir, expected",
        [(True, False, "file"), (False, True, "dir"), (False, False, "none")],
    )
    def test_get_type(self, is_file: bool, is_dir: bool, expected: str) -> None:
        with patch("pathlib.Path.is_file", return_value=is_file), patch(
            "pathlib.Path.is_dir", return_value=is_dir
        ):
            validator = PathValidator().set_path("/home/user/something")
            assert validator.get_type() == expected


# ========================
# Testes de Propriedades do Caminho
# ========================
class TestPathProperties:
    @patch("pathlib.Path.stat")
    def test_get_size(self, mock_stat: MagicMock) -> None:
        mock_stat.return_value.st_size = 1024
        validator = PathValidator().set_path("/home/user/file.txt")
        assert validator.get_size() == 1024

    @patch("pathlib.Path.stat")
    def test_get_permissions(self, mock_stat: MagicMock) -> None:
        mock_stat.return_value.st_mode = 0o777  # Permissões totais
        validator = PathValidator().set_path("/home/user/file.txt")
        assert validator.get_permissions() == {"read": True, "write": True, "execute": True}


# ========================
# Testes da Classe PathValidator
# ========================
class TestPathValidator:
    def test_set_path(self) -> None:
        validator = PathValidator()
        validator.set_path("/home/user/file.txt")
        assert str(validator.path) == "/home/user/file.txt"

    def test_is_valid_with_valid_path(self) -> None:
        validator = PathValidator("/home/user/file.txt")
        assert validator.is_valid() is True

    @patch("pathlib.Path.resolve", side_effect=OSError)
    def test_is_valid_with_invalid_path(self) -> None:
        validator = PathValidator("/invalid:/path")
        assert validator.is_valid() is False

    def test_exists_with_existing_path(self) -> None:
        with patch("pathlib.Path.exists", return_value=True):
            validator = PathValidator("/home/user/file.txt")
            assert validator.exists() is True

    def test_exists_with_non_existing_path(self) -> None:
        with patch("pathlib.Path.exists", return_value=False):
            validator = PathValidator("/home/user/file.txt")
            assert validator.exists() is False

    def test_is_absolute_with_absolute_path(self) -> None:
        validator = PathValidator("/home/user/file.txt")
        assert validator.is_absolute() is True

    def test_is_absolute_with_relative_path(self) -> None:
        validator = PathValidator("file.txt")
        assert validator.is_absolute() is False

    def test_get_type_with_file(self) -> None:
        with patch("pathlib.Path.is_file", return_value=True), patch(
            "pathlib.Path.is_dir", return_value=False
        ):
            validator = PathValidator("/home/user/file.txt")
            assert validator.get_type() == "file"

    def test_get_type_with_directory(self) -> None:
        with patch("pathlib.Path.is_file", return_value=False), patch(
            "pathlib.Path.is_dir", return_value=True
        ):
            validator = PathValidator("/home/user/dir")
            assert validator.get_type() == "dir"

    def test_get_type_with_none(self) -> None:
        with patch("pathlib.Path.is_file", return_value=False), patch(
            "pathlib.Path.is_dir", return_value=False
        ):
            validator = PathValidator("/home/user/none")
            assert validator.get_type() == "none"

    def test_get_size_with_existing_file(self) -> None:
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.is_file", return_value=True
        ), patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = 2048
            validator = PathValidator("/home/user/file.txt")
            assert validator.get_size() == 2048

    def test_get_size_with_non_existing_file(self) -> None:
        with patch("pathlib.Path.exists", return_value=False):
            validator = PathValidator("/home/user/file.txt")
            assert validator.get_size() == 0

    def test_get_permissions_with_existing_path(self) -> None:
        with patch("pathlib.Path.exists", return_value=True), patch(
            "pathlib.Path.stat"
        ) as mock_stat:
            mock_stat.return_value.st_mode = 0o777
            validator = PathValidator("/home/user/file.txt")
            assert validator.get_permissions() == {
                "read": True,
                "write": True,
                "execute": True,
            }

    def test_get_permissions_with_non_existing_path(self) -> None:
        with patch("pathlib.Path.exists", return_value=False):
            validator = PathValidator("/home/user/file.txt")
            assert validator.get_permissions() == {
                "read": False,
                "write": False,
                "execute": False,
            }
