# pylint: disable=C0114, C0115, C0116

import hashlib
import platform

import pytest

from src.models.caminhos import ValidadorCaminho  # Substitua pelo seu módulo

# Configuração para testes multiplataforma
SISTEMA = platform.system()
IS_WINDOWS = SISTEMA == "Windows"
IS_LINUX = SISTEMA == "Linux"
IS_MAC = SISTEMA == "Darwin"


# --------------------------------------------------
# 1. Validação + Classificação + Feedback
# --------------------------------------------------
class TestValidacaoClassificacao:
    @pytest.mark.parametrize("caminho, esperado", [
        # Windows
        pytest.param("C:\\Users\\file.txt", True, marks=pytest.mark.windows),
        pytest.param("C:\\Users\\*?.txt", False, marks=pytest.mark.windows),

        # Linux/macOS
        pytest.param("/home/user/file.txt", True, marks=pytest.mark.linux_mac),
        pytest.param("/home/user/\0file", False, marks=pytest.mark.linux_mac),

        # Multiplataforma
        ("./relativo/../file", True),
        ("", False)
    ])
    def test_valida_sintaxe(self, caminho, esperado):
        assert ValidadorCaminho(caminho).eh_valido() == esperado

    def test_classificacao_tipo(self, tmp_path):
        # Cria arquivo e pasta temporários
        arquivo = tmp_path / "teste.txt"
        arquivo.write_text("")
        pasta = tmp_path / "subpasta"
        pasta.mkdir()

        val_arquivo = ValidadorCaminho(str(arquivo))
        val_pasta = ValidadorCaminho(str(pasta))

        assert val_arquivo.eh_arquivo()
        assert val_pasta.eh_pasta()


# --------------------------------------------------
# 2. Normalização + Segurança + Operações
# --------------------------------------------------
class TestNormalizacaoSeguranca:
    @pytest.mark.parametrize("caminho, esperado", [
        # Windows
        pytest.param(
            "C:\\Users\\..\\Windows",
            "C:/Windows" if IS_WINDOWS else "/mnt/c/Windows",
            marks=pytest.mark.windows
        ),

        # Linux/macOS
        pytest.param(
            "/tmp//pasta/../file",
            "/tmp/file",
            marks=pytest.mark.linux_mac
        )
    ])
    def test_normalizacao(self, caminho, esperado):
        assert ValidadorCaminho(caminho).normalizar() == esperado

    def test_path_traversal(self):
        validador = ValidadorCaminho("../../../etc/passwd")
        assert not validador.evitar_path_injection()


# --------------------------------------------------
# 3. Existência + Sugestões + Criação
# --------------------------------------------------
class TestSugestoesCriacao:
    def test_sugestao_caminho(self, mocker):
        mocker.patch("os.listdir", return_value=["documentos", "imagens"])
        sugestoes = ValidadorCaminho(
            "/home/user/documentos"
        ).sugerir_alternativas()
        assert "documentos" in sugestoes

    def test_criacao_automatica(self, tmp_path):
        caminho = tmp_path / "novo_arquivo.txt"
        validador = ValidadorCaminho(str(caminho))
        validador.criar_se_nao_existir(como_arquivo=True)
        assert caminho.exists()


# --------------------------------------------------
# 4. Metadados + Comparação + Hash
# --------------------------------------------------
class TestMetadadosHash:
    def test_metadados_arquivo(self):
        validador = ValidadorCaminho("/home/user/arquivo.txt")
        assert validador.extrair_nome_arquivo() == "arquivo.txt"
        assert validador.extrair_extensao() == ".txt"

    def test_hash_arquivo(self, tmp_path):
        arquivo = tmp_path / "teste_hash.txt"
        arquivo.write_text("conteúdo")
        hash_esperado = hashlib.md5("conteúdo".encode()).hexdigest()
        assert ValidadorCaminho(str(arquivo)).gerar_hash() == hash_esperado


# --------------------------------------------------
# 5. Segurança + Validação + Feedback
# --------------------------------------------------
class TestSeguranca:
    @pytest.mark.skipif(not IS_LINUX, reason="Requer Linux")
    def test_permissao_negada_linux(self):
        validador = ValidadorCaminho("/root/")
        assert not validador.validar_permissoes()

    def test_log_tentativa_invalida(self, mocker):
        mock_log = mocker.patch("seu_modulo.log_seguranca")
        ValidadorCaminho("/invalid/path*").validar()
        assert mock_log.called
        assert mock_log.called
