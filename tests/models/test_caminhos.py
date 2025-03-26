# pylint: disable=W0212

"""
Este módulo contém testes para a classe `Caminho` localizada em `src.models.caminhos`.
Os testes abrangem a inicialização, propriedades, métodos e comportamentos esperados
da classe, incluindo cenários de sucesso e falha.

Testes incluem:
- Inicialização com caminhos válidos e inválidos.
- Validação de permissões e tipos de caminho.
- Métodos de conversão para dicionário e JSON.
- Métodos especiais como `__repr__` e `__eq__`.
- Uso de mocks para simular comportamentos específicos.

Nota: Este módulo utiliza o framework pytest para a execução dos testes.

"""

import json
import os
from unittest.mock import patch

import pytest

from src.models.caminhos import Caminho


class TestCaminho:
    """Testes para a classe Caminho"""

    @pytest.fixture
    def temp_dir(self, tmp_path):
        """Cria um diretório temporário para testes."""
        d = tmp_path / "test_dir"
        d.mkdir()
        return str(d)

    @pytest.fixture
    def temp_file(self, tmp_path):
        """Cria um arquivo temporário para testes."""
        f = tmp_path / "test_file.txt"
        f.write_text("test content")
        return str(f)

    def test_init_com_caminho_valido(self, temp_dir):
        """Testa a inicialização com um caminho válido."""
        caminho = Caminho(temp_dir)
        assert caminho.caminho == os.path.abspath(temp_dir)

    def test_init_com_caminho_invalido(self):
        """Testa a inicialização com um caminho inválido."""
        with pytest.raises(TypeError):
            Caminho(123)  # type: ignore

        with pytest.raises(TypeError):
            Caminho("")

    def test_init_com_caminho_inexistente(self):
        """Testa a inicialização com um caminho que não existe."""
        with pytest.raises(FileNotFoundError):
            Caminho("/caminho/inexistente/123456")

    def test_init_sem_permissao(self, temp_file):
        """Testa a inicialização sem permissão de leitura/escrita."""
        os.chmod(temp_file, 0o000)  # Torna o arquivo não legível
        try:
            with pytest.raises(PermissionError):
                Caminho(temp_file)
        finally:
            os.chmod(temp_file, 0o644)  # Restaura permissões para evitar problemas nos testes

    def test_property_caminho(self, temp_dir):
        """Testa a propriedade `caminho`."""
        caminho = Caminho(temp_dir)
        assert caminho.caminho == os.path.abspath(temp_dir)

    def test_validar_caminho(self, temp_dir):
        """Testa o método estático `_validar_caminho`."""
        validado = Caminho._validar_caminho(temp_dir)
        assert validado == os.path.abspath(temp_dir)

    def test_verificar_permissao(self, temp_dir):
        """Testa o método estático `_verificar_permissao`."""
        assert Caminho._verificar_permissao(temp_dir) is True

    def test_to_dict(self, temp_dir):
        """Testa o método `to_dict`."""
        caminho = Caminho(temp_dir)
        result = caminho.to_dict()

        assert isinstance(result, dict)
        assert result["caminho"] == os.path.abspath(temp_dir)
        assert result["tipo"] == "diretório"
        assert result["existe"] is True
        assert result["permissao"] is True
        assert result["normalizado"] == os.path.abspath(temp_dir)

    def test_to_json(self, temp_dir):
        """Testa o método `to_json`."""
        caminho = Caminho(temp_dir)
        json_str = caminho.to_json()

        assert isinstance(json_str, str)
        json_data = json.loads(json_str)
        assert json_data["caminho"] == os.path.abspath(temp_dir)

    def test_eq(self, temp_dir):
        """Testa o método especial `__eq__`."""
        caminho1 = Caminho(temp_dir)
        caminho2 = Caminho(temp_dir)
        caminho3 = Caminho(os.path.dirname(temp_dir))

        assert caminho1 == caminho2
        assert caminho1 != caminho3
        assert caminho1 != "not a Caminho object"

    @patch("os.path.exists", return_value=True)
    @patch("src.models.caminhos.Caminho._verificar_permissao", return_value=True)
    def test_validar_caminho_mocked(self, mock_verificar_permissao, mock_exists):
        """Testa o método `_validar_caminho` utilizando mocks."""
        result = Caminho._validar_caminho("/qualquer/caminho")
        assert result == os.path.abspath("/qualquer/caminho")
        mock_exists.assert_called_once_with("/qualquer/caminho")
        mock_verificar_permissao.assert_called_once_with("/qualquer/caminho")

    def test_determinar_tipo_diretorio(self, tmp_path):
        """Testa quando o caminho é um diretório"""
        dir_path = str(tmp_path / "test_dir")
        os.mkdir(dir_path)

        caminho = Caminho(dir_path)
        assert caminho._determinar_tipo() == "diretório"

    def test_determinar_tipo_arquivo(self, tmp_path):
        """Testa quando o caminho é um arquivo"""
        file_path = str(tmp_path / "test_file.txt")
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write("test")

        caminho = Caminho(file_path)
        assert caminho._determinar_tipo() == "arquivo"

    def test_determinar_tipo_link_simbolico(self, tmp_path):
        """Testa quando o caminho é um link simbólico"""
        target_path = str(tmp_path / "target.txt")
        link_path = str(tmp_path / "link.txt")

        with open(target_path, "w", encoding="utf-8") as f:
            f.write("target")
        os.symlink(target_path, link_path)

        caminho = Caminho(link_path)
        assert caminho._determinar_tipo() == "arquivo"
        caminho = Caminho(link_path)
        assert caminho._determinar_tipo() == "arquivo"
