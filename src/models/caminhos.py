"""
Módulo Caminho

Este módulo fornece a classe `Caminho` para manipulação e validação de caminhos de arquivos,
diretórios e links simbólicos. A classe permite verificar permissões, identificar o tipo do caminho
e converter informações para dicionários e JSON.

Principais funcionalidades:
- Validação de caminhos fornecidos.
- Verificação de permissões de leitura e escrita.
- Identificação do tipo do caminho (arquivo, diretório ou link simbólico).
- Exportação de informações do caminho em formato de dicionário ou JSON.

"""

import json
import os
from pathlib import Path
from typing import Dict, Optional


class Caminho:
    """
    Classe para manipulação de caminhos de arquivos,
    diretórios e links simbólicos.
    """

    def __init__(self, caminho: str) -> None:
        self._caminho: Optional[Path] = None
        self._cache: Dict[Path, bool] = {}  # Cache para permissões de caminhos
        self._tipo_cache: Dict[str, str] = {}  # Cache separado para tipos e outros dados
        self.caminho = Path(caminho).resolve()

    @property
    def caminho(self) -> Optional[Path]:
        """
        Propriedade para acessar o caminho armazenado.
        """
        return self._caminho

    @caminho.setter
    def caminho(
        self, novo_caminho: str | Path
    ) -> None:
        """Valida, normaliza e armazena o caminho se for válido."""
        if not isinstance(novo_caminho, str) or not novo_caminho.strip():
            raise TypeError("O caminho deve ser uma string válida.")

        # Trata caminhos de rede separadamente
        if novo_caminho.startswith(("\\\\", "smb://")):
            caminho_path: Path = Path(novo_caminho)
        else:
            caminho_path = Path(novo_caminho).resolve()

        if not caminho_path.exists():
            raise FileNotFoundError(f"Caminho não encontrado: {novo_caminho}")

        if not self._verificar_permissao(caminho_path):
            raise PermissionError(f"Sem permissão de leitura e escrita: {novo_caminho}")

        self._caminho = caminho_path
        self._cache.clear()

    def _verificar_permissao(self, caminho: Path) -> bool:
        """Verifica se o caminho tem permissão de leitura e escrita."""
        if caminho in self._cache:
            return bool(self._cache[caminho])

        permitido: bool = os.access(caminho, os.R_OK | os.W_OK)
        self._cache[caminho] = permitido
        return permitido

    def _determinar_tipo(self) -> str:
        """Determina se o caminho é um arquivo, diretório ou link simbólico."""
        if "tipo" in self._tipo_cache:
            return self._tipo_cache["tipo"]
        if self._caminho is None:
            return "desconhecido"

        tipo: str = (
            "diretório"
            if self._caminho.is_dir()
            else (
                "arquivo"
                if self._caminho.is_file()
                else "link simbólico" if self._caminho.is_symlink() else "desconhecido"
            )
        )
        self._tipo_cache["tipo"] = tipo
        return tipo

    def to_dict(
        self,
    ) -> Dict[
        str, str | bool | None
    ]:
        """Retorna um dicionário com informações do caminho."""
        return {
            "caminho": str(self._caminho) if self._caminho else "",
            "tipo": self._determinar_tipo(),
            "existe": self._caminho.exists() if self._caminho else False,
            "permissao": (
                self._verificar_permissao(self._caminho) if self._caminho else False
            ),
            "normalizado": str(self._caminho.resolve()) if self._caminho else None,
        }

    def to_json(self) -> str:
        """Retorna um JSON com informações do caminho."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
