# pylint: disable=protected-access

"""
Módulo Caminho - Manipulação segura de caminhos do sistema de arquivos

Esta classe fornece:
- Validação robusta de caminhos (absolutos e relativos)
- Conversão automática de caminhos relativos para absolutos
- Controle de acesso via getter/setter com validação
- Verificação de permissões
- Identificação do tipo (arquivo, diretório, link)
- Exportação para dict e JSON
- Representações consistentes do objeto

Exemplo de uso:
    >>> caminho = Caminho("../pasta/relativa")  # Aceita caminhos relativos
    >>> print(caminho.to_json())  # Saída formatada em JSON
    >>> dados = caminho.to_dict()  # Dicionário com metadados
"""

import json
import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal, Optional, Union


class PathType(str, Enum):
    """Enumeração de tipos de caminhos do sistema de arquivos."""
    FILE = "arquivo"
    DIR = "diretório"
    SYMLINK = "link simbólico"
    UNKNOWN = "desconhecido"
    INVALID = "inválido"


@dataclass
class PathError:
    """Representa um erro de caminho inválido."""
    type: str
    message: str


@dataclass
class Caminho:
    """Representa um caminho do sistema de arquivos (válido ou inválido)."""

    raw_path: str
    _resolved_path: Optional[Path] = field(default=None, init=False, repr=False)
    _error: Optional[PathError] = field(default=None, init=False, repr=False)
    _state: Literal["valid", "invalid"] = field(default="invalid", init=False, repr=False)

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        """Valida o caminho automaticamente após inicialização."""
        try:
            path: Path = Path(self.raw_path).resolve(strict=True)

            if not os.access(path, os.R_OK | os.W_OK):
                raise PermissionError(f"Sem permissões em: {path}")

            self._resolved_path = path
            self._state = "valid"

        except (TypeError, RuntimeError, OSError) as e:
            self._error = PathError(type=e.__class__.__name__, message=str(e))
            self._state = "invalid"

    @property
    def is_valid(self) -> bool:
        """Retorna True se o caminho for válido."""
        return self._state == "valid"

    @property
    def path(self) -> Optional[Path]:
        """Retorna o objeto Path se válido."""
        return self._resolved_path if self.is_valid else None

    @property
    def type(self) -> PathType:
        """Determina o tipo do caminho."""
        if not self.is_valid:
            return PathType.INVALID

        if self._resolved_path and self._resolved_path.is_dir():
            return PathType.DIR
        if self._resolved_path and self._resolved_path.is_file():
            return PathType.FILE
        if self._resolved_path and self._resolved_path.is_symlink():
            return PathType.SYMLINK

        return PathType.UNKNOWN

    @property
    def error(self) -> Optional[PathError]:
        """Retorna o erro associado ao caminho, se houver."""
        return self._error

    def to_dict(self) -> dict:
        """Converte para dicionário com informações completas."""
        base: dict = {
            "raw_path": self.raw_path,
            "is_valid": self.is_valid,
            "type": self.type.value
        }

        if self.is_valid:
            base.update({
                "resolved_path": str(self._resolved_path),
                "permissions": {
                    "readable": os.access(
                        self._resolved_path, os.R_OK
                    ) if self._resolved_path else False,
                    "writable": os.access(
                        self._resolved_path, os.W_OK
                    ) if self._resolved_path else False
                }
            })
        else:
            base["error"] = {
                "type": self._error.type if self._error else "Unknown",
                "message": self._error.message if self._error else "Erro desconhecido"
            }

        return base

    def __str__(self) -> str:
        return self.raw_path


# Exemplo de uso moderno
if __name__ == "__main__":
    paths_to_test: list[Union[str, int, Path]] = [
        "/caminho/válido/existente",  # Substitua por um caminho real
        "/caminho/inválido",
        Path.home() / "Downloads",
        123  # Tipo inválido
    ]

    for test_path in paths_to_test:
        print(f"\nTesting: {test_path}")
        caminho = Caminho(str(test_path))

        print(f"Valid: {caminho.is_valid}")
        print(f"Type: {caminho.type.value}")
        if caminho.error:
            print(f"Error: {caminho.error.type} - {caminho.error.message}")
        if caminho.is_valid:
            print(f"Resolved: {caminho.path}")
        else:
            if not caminho.is_valid and caminho._error:
                print(f"Error: {caminho._error.type} - {caminho._error.message}")
            else:
                print("No error or path is valid.")

        print("JSON Representation:")
        print(json.dumps(caminho.to_dict(), indent=2, ensure_ascii=False))
