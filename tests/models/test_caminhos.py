# Author: Pedro Paulo Machado Dias
# Date: 2021-06-27
# Description: Testes para a classe Caminho.

# pylint: disable=wrong-import-order, wrong-import-position, import-error, redefined-outer-name, protected-access

"""
Módulo de testes para a classe Caminho.

Testa diversas funcionalidades, incluindo a verificação de tipos, permissões e conversão para JSON.
"""


### Testes com `pytest`:

import os
import pytest
from src.models.caminhos import Caminho


@pytest.fixture
def caminho_valido():
    return Caminho("/home/pedro-pm-dias/Downloads/Firefox/")


@pytest.fixture
def caminho_arquivo():
    return Caminho("/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html")


@pytest.fixture
def caminho_link_simbolico():
    caminho = "/home/pedro-pm-dias/Downloads/Firefox/sym_link"
    os.symlink("/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html", caminho)
    yield Caminho(caminho)
    os.remove(caminho)


def test_caminho_valido(caminho_valido):
    assert caminho_valido.caminho == os.path.abspath("/home/pedro-pm-dias/Downloads/Firefox/")


def test_caminho_inexistente():
    with pytest.raises(FileNotFoundError):
        Caminho("/caminho/inexistente")


def test_sem_permissao():
    # Criar um caminho sem permissão de leitura ou escrita pode ser complicado em testes,
    # então é necessário configurar as permissões de arquivo ou usar uma pasta específica
    # que você sabe que vai faltar permissão.
    caminho = "/root"
    with pytest.raises(PermissionError):
        Caminho(caminho)


def test_valida_tipo_diretorio(caminho_valido):
    assert caminho_valido._determinar_tipo() == "diretório"


def test_valida_tipo_arquivo(caminho_arquivo):
    assert caminho_arquivo._determinar_tipo() == "arquivo"


def test_valida_tipo_link_simbolico(caminho_link_simbolico):
    assert caminho_link_simbolico._determinar_tipo() == "link simbólico"


def test_comparacao_caminhos(caminho_valido, caminho_arquivo):
    caminho_valido2 = Caminho("/home/pedro-pm-dias/Downloads/Firefox/")
    caminho_arquivo2 = Caminho("/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html")
    assert caminho_valido == caminho_valido2
    assert caminho_arquivo != caminho_valido2


def test_to_dict(caminho_valido):
    dict_info = caminho_valido.to_dict()
    assert "caminho" in dict_info
    assert "tipo" in dict_info
    assert "permissao" in dict_info


def test_to_json(caminho_valido):
    json_info = caminho_valido.to_json()
    assert '"caminho":' in json_info
    assert '"tipo":' in json_info


def test_repr(caminho_valido):
    assert repr(caminho_valido) == f"Caminho(caminho={os.path.abspath('/home/pedro-pm-dias/Downloads/Firefox/')})"


### Modelo de uso complementado:


def uso_comum():
    # Caminho de uma pasta
    caminho_pasta = Caminho("/home/pedro-pm-dias/Downloads/Firefox/")
    print("Caminho da pasta:")
    print(caminho_pasta)
    print("Informações em formato JSON:")
    print(caminho_pasta.to_json())
    print("*" * 50)

    # Caminho de um arquivo
    caminho_arquivo = Caminho("/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html")
    print("Caminho do arquivo:")
    print(caminho_arquivo)
    print("Informações em formato JSON:")
    print(caminho_arquivo.to_json())
    print("*" * 50)

    # Comparação de caminhos
    caminho_comparacao = Caminho("/home/pedro-pm-dias/Downloads/Firefox/")
    caminho_comparacao2 = Caminho("/home/pedro-pm-dias/Downloads/Firefox/")
    caminho_comparacao3 = Caminho("/home/pedro-pm-dias/Downloads/Chrome/")
    print("Comparando dois caminhos iguais:", caminho_comparacao == caminho_comparacao2)
    print("Comparando dois caminhos diferentes:", caminho_comparacao == caminho_comparacao3)

    # Representação em formato legível
    print("Representação legível de um caminho:")
    print(repr(caminho_pasta))


if __name__ == "__main__":
    uso_comum()
