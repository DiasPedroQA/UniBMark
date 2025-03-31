# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

# Classe para Representar Caminhos de Sistema Operacional com Testes em Pytest

# Implementação da Classe PathOS

import os
import re


class PathOS:
    def __init__(self, path_str):
        """Inicializa o caminho, normalizando de acordo com o sistema operacional"""
        self.original_path = path_str
        self.normalized_path = self._normalize_path(path_str)

    def _normalize_path(self, path_str):
        """Normaliza o caminho de acordo com o SO"""
        # Substitui barras invertidas por barras normais para consistência
        path = path_str.replace('\\', '/')

        # Remove barras duplicadas
        path = re.sub(r'/+', '/', path)

        # Remove barra final (exceto para root)
        if len(path) > 1 and path.endswith('/'):
            path = path[:-1]

        return path

    def is_absolute(self):
        """Verifica se o caminho é absoluto"""
        return os.path.isabs(self.normalized_path)

    def get_components(self):
        """Retorna os componentes do caminho como uma lista"""
        if self.normalized_path == '/':
            return ['/']
        return [comp for comp in self.normalized_path.split('/') if comp]

    def join(self, *paths):
        """Junta o caminho atual com outros caminhos fornecidos"""
        joined = self.normalized_path
        for path in paths:
            path_obj = PathOS(path)
            if path_obj.is_absolute():
                joined = path_obj.normalized_path
            else:
                if not joined.endswith('/'):
                    joined += '/'
                joined += path_obj.normalized_path
        return PathOS(joined)

    def get_parent(self):
        """Retorna o diretório pai do caminho"""
        components = self.get_components()
        if len(components) <= 1:
            return PathOS('/')
        return PathOS('/'.join(components[:-1]))

    def get_filename(self):
        """Retorna o nome do arquivo ou último componente do caminho"""
        components = self.get_components()
        if not components:
            return ''
        return components[-1]

    def get_extension(self):
        """Retorna a extensão do arquivo, se houver"""
        filename = self.get_filename()
        if '.' not in filename:
            return ''
        return filename.split('.')[-1]

    def exists(self):
        """Verifica se o caminho existe no sistema de arquivos real"""
        return os.path.exists(self.original_path)

    def __str__(self):
        """Representação em string do caminho"""
        return self.normalized_path

    def __repr__(self):
        """Representação oficial do objeto"""
        return f"PathOS('{self.normalized_path}')"

    def __eq__(self, other):
        """Comparação de igualdade com outro PathOS ou string"""
        if isinstance(other, PathOS):
            return self.normalized_path == other.normalized_path
        if isinstance(other, str):
            return self.normalized_path == PathOS(other).normalized_path
        return False


# Testes com Pytest


def test_path_initialization():
    # Teste com caminho simples
    p1 = PathOS("caminho/para/arquivo")
    assert str(p1) == "caminho/para/arquivo"

    # Teste normalização de barras
    p2 = PathOS("caminho\\para\\arquivo")
    assert str(p2) == "caminho/para/arquivo"

    # Teste com barras duplicadas
    p3 = PathOS("caminho//para///arquivo")
    assert str(p3) == "caminho/para/arquivo"

    # Teste com caminho absoluto Unix
    p4 = PathOS("/usr/local/bin")
    assert str(p4) == "/usr/local/bin"
    assert p4.is_absolute() is True

    # Teste com caminho absoluto Windows
    p5 = PathOS("C:\\Windows\\System32")
    assert str(p5) == "C:/Windows/System32"
    assert p5.is_absolute() is True


def test_path_components():
    p = PathOS("caminho/para/arquivo.txt")
    assert p.get_components() == ["caminho", "para", "arquivo.txt"]

    p_root = PathOS("/")
    assert p_root.get_components() == ["/"]

    p_abs = PathOS("/usr/bin/python")
    assert p_abs.get_components() == ["usr", "bin", "python"]


def test_path_joining():
    p1 = PathOS("diretorio")
    p2 = p1.join("subdir")
    assert str(p2) == "diretorio/subdir"

    p3 = p2.join("/absoluto")
    assert str(p3) == "/absoluto"

    p4 = PathOS("/").join("usr", "local", "bin")
    assert str(p4) == "/usr/local/bin"


def test_parent_and_filename():
    p = PathOS("dir1/dir2/arquivo.ext")
    assert str(p.get_parent()) == "dir1/dir2"
    assert p.get_filename() == "arquivo.ext"
    assert p.get_extension() == "ext"

    p_root = PathOS("/")
    assert str(p_root.get_parent()) == "/"
    assert p_root.get_filename() == "/"
    assert p_root.get_extension() == ""


def test_equality():
    p1 = PathOS("caminho/arquivo")
    p2 = PathOS("caminho/arquivo")
    p3 = PathOS("outro/caminho")

    assert p1 == p2
    assert p1 != p3
    assert p1 == "caminho/arquivo"
    assert p1 != "outro/caminho"


def test_exists(monkeypatch):
    # Teste com mock para exists
    def mock_exists(path):
        return path in ["/existe", "C:/existe"]

    monkeypatch.setattr(os.path, 'exists', mock_exists)

    assert PathOS("/existe").exists() is True
    assert PathOS("/nao_existe").exists() is False
    assert PathOS("C:/existe").exists() is True


def test_edge_cases():
    # Caminho vazio
    p_empty = PathOS("")
    assert str(p_empty) == ""

    # Caminho com apenas pontos
    p_dots = PathOS("./../.")
    assert str(p_dots) == "./../."

    # Caminho com espaços
    p_spaces = PathOS("caminho com espaços/arquivo.txt")
    assert str(p_spaces) == "caminho com espaços/arquivo.txt"
