# pylint: disable=protected-access

"""
Módulo Caminho - Manipulação segura de caminhos do sistema de arquivos

Python 3.12+ com type hints avançados:
- Uso de typing.Self
- Tipos literais e union types com sintaxe simplificada
- Pattern matching para tratamento de erros
"""

# **Classe Base (Versão Simplificada)**

import hashlib
import os
import platform
import re
from pathlib import Path


class ValidadorCaminho:
    def __init__(self, caminho):
        self.caminho_original = caminho
        self.caminho = str(caminho)  # Garante que é string
        self.so = platform.system()  # 'Windows', 'Linux', 'Darwin'

        # Flags de estado (serão preenchidas durante a validação)
        self._valido = None
        self._motivo_invalidez = None
        self._normalizado = None

    # --------------------------------------------------
    # 1. Validação + Classificação + Feedback
    # --------------------------------------------------
    def eh_valido(self):
        """Valida a sintaxe do caminho conforme as regras do SO."""
        if self._valido is not None:
            return self._valido

        self._valido = True
        self._motivo_invalidez = None

        # Verifica caracteres proibidos
        caracteres_proibidos = {
            'Windows': r'[*?"<>|]',
            'Linux': r'[\0]',
            'Darwin': r'[\0]'
        }.get(self.so, r'[\0]')

        if re.search(caracteres_proibidos, self.caminho):
            self._valido = False
            self._motivo_invalidez = "Contém caracteres inválidos para o SO"

        # Verifica caminho vazio
        elif not self.caminho.strip():
            self._valido = False
            self._motivo_invalidez = "Caminho vazio"

        return self._valido

    def get_motivo_invalidez(self):
        """Retorna o motivo da invalidez (se aplicável)."""
        return self._motivo_invalidez or "Caminho válido"

    def eh_arquivo(self):
        """Verifica se o caminho é um arquivo existente."""
        return os.path.isfile(self.obter_caminho_real())

    def eh_pasta(self):
        """Verifica se o caminho é uma pasta existente."""
        return os.path.isdir(self.obter_caminho_real())

    # --------------------------------------------------
    # 2. Normalização + Segurança
    # --------------------------------------------------
    def normalizar(self):
        """Padroniza o caminho para um formato interno (Unix-like)."""
        if self._normalizado is not None:
            return self._normalizado

        caminho = self.caminho

        # Substitui barras invertidas (Windows)
        caminho = caminho.replace("\\", "/")

        # Expande ~ (home directory)
        if caminho.startswith("~"):
            caminho = os.path.expanduser(caminho)

        # Converte caminhos Windows (C:\ → /mnt/c/)
        if self.so != "Windows" and ":/" in caminho:
            caminho = re.sub(r"^([A-Za-z]):/", r"/mnt/\1/", caminho)

        # Remove redundâncias (../, ./)
        caminho = os.path.normpath(caminho)

        self._normalizado = caminho
        return caminho

    def evitar_path_injection(self):
        """Bloqueia tentativas de path traversal (ex: ../../../etc/passwd)."""
        caminho_normalizado = self.normalizar()
        partes = caminho_normalizado.split("/")
        if ".." in partes:
            return False
        return True

    # --------------------------------------------------
    # 3. Existência + Sugestões
    # --------------------------------------------------
    def sugerir_alternativas(self, distancia_maxima=2):
        """Sugere caminhos similares existentes (fuzzy matching)."""
        from difflib import get_close_matches  # Importação tardia

        if self.eh_existente():
            return []

        dir_pai = os.path.dirname(self.obter_caminho_real())
        if not os.path.exists(dir_pai):
            return []

        itens = os.listdir(dir_pai)
        return get_close_matches(
            os.path.basename(self.caminho),
            itens,
            n=3,
            cutoff=0.6
        )

    def criar_se_nao_existir(self, como_arquivo=False):
        """Cria o arquivo/pasta se não existir."""
        caminho = self.obter_caminho_real()
        if os.path.exists(caminho):
            return

        if como_arquivo:
            Path(caminho).touch()
        else:
            Path(caminho).mkdir(parents=True)

    # --------------------------------------------------
    # 4. Metadados + Hash
    # --------------------------------------------------
    def extrair_nome_arquivo(self):
        """Retorna o nome do arquivo (ex: 'arquivo.txt')."""
        return os.path.basename(self.normalizar())

    def extrair_extensao(self):
        """Retorna a extensão (ex: '.txt')."""
        nome = self.extrair_nome_arquivo()
        return os.path.splitext(nome)[1]

    def gerar_hash(self, algoritmo="md5"):
        """Gera hash do conteúdo do arquivo (se existir)."""
        if not self.eh_arquivo():
            return None

        with open(self.obter_caminho_real(), "rb") as f:
            conteudo = f.read()
            return hashlib.md5(conteudo).hexdigest()

    # --------------------------------------------------
    # 5. Segurança Avançada
    # --------------------------------------------------
    def validar_permissões(self):
        """Verifica permissões de leitura/escrita."""
        caminho = self.obter_caminho_real()
        if not os.path.exists(caminho):
            return False
        return os.access(caminho, os.R_OK | os.W_OK)

    # --------------------------------------------------
    # Métodos Auxiliares
    # --------------------------------------------------
    def obter_caminho_real(self):
        """Retorna o caminho absoluto e normalizado."""
        caminho = self.normalizar()
        if os.path.isabs(caminho):
            return caminho
        return os.path.abspath(caminho)

    def eh_existente(self):
        """Verifica se o caminho existe no sistema de arquivos."""
        return os.path.exists(self.obter_caminho_real())

    def comparar(self, outro_validador):
        """Compara dois caminhos (considerando normalização)."""
        return self.obter_caminho_real() == outro_validador.obter_caminho_real()


# **Exemplo de Uso**
# Validação + Normalização
validador = ValidadorCaminho("C:\\Users\\../file.txt")
if validador.eh_valido():
    print(f"Caminho normalizado: {validador.normalizar()}")  # /mnt/c/file.txt (Linux)
else:
    print(f"Erro: {validador.get_motivo_invalidez()}")

# Sugestões para caminhos inexistentes
sugestoes = ValidadorCaminho("/home/user/documntos").sugerir_alternativas()
print(f"Você quis dizer? {sugestoes}")  # ['documentos']
