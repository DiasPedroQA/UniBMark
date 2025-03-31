# import os
import stat
from pathlib import Path


class PathValidator:
    def __init__(self, path: str = ""):
        self.path = Path(path) if path else None

    def set_path(self, path: str) -> "PathValidator":
        self.path = Path(path)
        return self

    def is_valid(self) -> bool:
        try:
            _ = self.path.resolve() if self.path else None
            return True
        except OSError:
            return False

    def exists(self) -> bool:
        return self.path.exists() if self.path else False

    def is_absolute(self) -> bool:
        return self.path.is_absolute() if self.path else False

    def get_type(self) -> str:
        if self.path and self.path.is_file():
            return "file"
        elif self.path and self.path.is_dir():
            return "dir"
        return "none"

    def get_size(self) -> int:
        return (
            self.path.stat().st_size
            if self.path and self.path.exists() and self.path.is_file()
            else 0
        )

    def get_permissions(self) -> dict:
        if not self.path or not self.path.exists():
            return {"read": False, "write": False, "execute": False}
        mode = self.path.stat().st_mode if self.path else 0
        return {
            "read": bool(mode & stat.S_IRUSR),
            "write": bool(mode & stat.S_IWUSR),
            "execute": bool(mode & stat.S_IXUSR),
        }
