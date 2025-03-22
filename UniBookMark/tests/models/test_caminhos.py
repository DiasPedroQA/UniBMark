import pytest
import json
import os
import sys
from pathlib import Path
from typing import Union

# Adiciona o diretório raiz ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

# Agora a importação funcionará
from models.caminhos import Caminho

@pytest.fixture
def arquivo_tmp(tmp_path):
    """Cria um arquivo temporário para os testes."""
    arquivo = tmp_path / "teste.txt"
    arquivo.write_text("conteúdo de teste")
    return arquivo

@pytest.fixture
def diretorio_tmp(tmp_path):
    """Cria um diretório temporário para os testes."""
    return tmp_path

@pytest.fixture
def link_simbolico_tmp(tmp_path, arquivo_tmp):
    """Cria um link simbólico apontando para um arquivo temporário."""
    link = tmp_path / "link_teste"
    link.symlink_to(arquivo_tmp)
    return link

def test_caminho_valido(arquivo_tmp):
    """Testa se a classe aceita caminhos válidos."""
    caminho = Caminho(str(arquivo_tmp))
    assert caminho.caminho == arquivo_tmp.resolve()

def test_caminho_inexistente():
    """Testa se um caminho inexistente levanta um erro."""
    with pytest.raises(FileNotFoundError):
        Caminho("/caminho/que/nao/existe")

def test_caminho_nao_string():
    """Testa se caminhos que não são string levantam erro."""
    with pytest.raises(TypeError):
        Caminho(123)

def test_caminho_vazio():
    """Testa se uma string vazia levanta erro."""
    with pytest.raises(TypeError):
        Caminho("")

def test_permissao_negada(monkeypatch, arquivo_tmp):
    """Testa se a classe detecta permissão negada."""
    def fake_access(path, mode):
        return False  # Simula falta de permissão

    monkeypatch.setattr(os, "access", fake_access)

    with pytest.raises(PermissionError):
        Caminho(str(arquivo_tmp))

def test_verificar_permissao_cache(arquivo_tmp):
    """Testa se a verificação de permissão usa cache."""
    caminho = Caminho(str(arquivo_tmp))
    assert caminho._cache[arquivo_tmp] is True

def test_determinar_tipo_arquivo(arquivo_tmp):
    """Testa se a classe identifica corretamente um arquivo."""
    caminho = Caminho(str(arquivo_tmp))
    assert caminho._determinar_tipo() == "arquivo"

def test_determinar_tipo_diretorio(diretorio_tmp):
    """Testa se a classe identifica corretamente um diretório."""
    caminho = Caminho(str(diretorio_tmp))
    assert caminho._determinar_tipo() == "diretório"

def test_determinar_tipo_link_simbolico(link_simbolico_tmp):
    """Testa se a classe identifica corretamente um link simbólico."""
    caminho = Caminho(str(link_simbolico_tmp))
    assert caminho._determinar_tipo() == "link simbólico"

def test_to_dict(arquivo_tmp):
    """Testa se o método to_dict() retorna as informações corretas."""
    caminho = Caminho(str(arquivo_tmp))
    esperado = {
        "caminho": str(arquivo_tmp.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_tmp.resolve()),
    }
    assert caminho.to_dict() == esperado

def test_to_json(arquivo_tmp):
    """Testa se o método to_json() retorna um JSON válido e correto."""
    caminho = Caminho(str(arquivo_tmp))
    resultado = json.loads(caminho.to_json())

    esperado = {
        "caminho": str(arquivo_tmp.resolve()),
        "tipo": "arquivo",
        "existe": True,
        "permissao": True,
        "normalizado": str(arquivo_tmp.resolve()),
    }
    assert resultado == esperado


# Lista de testes
caminhos_teste: list[Union[str, int, None]] = [
    "/storage/emulated/0/",                    # Caminho válido (Android)
    "/home/pedro-pm-dias/Downloads",           # Caminho válido (Linux)
    "/home/pedro-pm-dias/Downloads/Firefox/",  # Caminho válido (Linux)
    "/home/user/documento.txt",                # Caminho válido com permissão
    "/caminho/apenas_leitura.txt",             # Caminho somente leitura
    "/caminho/sem_permissao.txt",              # Caminho sem permissão
    "/home/user/documento.txt",                # Caminho válido absoluto (Linux/Mac)
    "C:\\Users\\User\\arquivo.txt",            # Caminho válido absoluto (Windows)
    "/caminho/que/nao/existe",                 # Caminho inexistente
    "C:\\Caminho\\Sem\\Permissao",             # Caminho sem permissão
    "\\\\Servidor\\Compartilhamento",          # Caminho de rede válido (Windows)
    "smb://servidor/pasta",                    # Caminho de rede válido (Linux/Mac)
    "documentos/arquivo.txt",                  # Caminho relativo (vai se tornar absoluto)
    "../outro_diretorio/arquivo.csv",          # Caminho relativo com `..` (vai se tornar absoluto)
    "12345",                                   # Entrada inválida (não é string)
    12345,                                     # Entrada inválida (não é string)
    "",                                        # String vazia (inválida)
    None                                       # Valor nulo (inválido)
]

# Teste da classe
for caminho in caminhos_teste:
    print(f"\n\nTestando caminho: ({caminho})")
    print(f"Tipo do caminho: {type(caminho)}")
    try:
        obj_caminho: Caminho = Caminho(caminho)
        
        # Convertendo para JSON e dicionário
        obj_json: str = obj_caminho.to_json()
        obj_dict: dict[str, Union[str, bool]] = obj_caminho.to_dict()
        
        print("JSON Output:")
        print(obj_json)
        
        print("\nDicionário Output:")
        print(obj_dict)
        
    except (TypeError, ValueError, FileNotFoundError, PermissionError, OSError) as e:
        print(f"Erro capturado: {e}")
