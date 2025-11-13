from pathlib import Path
from typing import Optional, Dict, Iterable

class FileUserRepo:
    """
    Repo muy simple que guarda usuarios en un txt (formato: username|password_hash).
    NO es para producción, es solo para demo.
    """
    def __init__(self, filepath: Path):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.filepath.touch()

    def _iter_records(self) -> Iterable[Dict[str, str]]:
        with self.filepath.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                username, password_hash = line.split("|", 1)
                yield {"username": username, "password_hash": password_hash}

    def get_user(self, username: str) -> Optional[Dict[str, str]]:
        for rec in self._iter_records():
            if rec["username"] == username:
                return rec
        return None

    def add_user(self, username: str, password_hash: str) -> None:
        if self.get_user(username) is not None:
            raise ValueError("Usuario ya existe")
        with self.filepath.open("a", encoding="utf-8") as f:
            f.write(f"{username}|{password_hash}\n")

    def verify(self, username: str, password_hash: str) -> bool:
        user = self.get_user(username)
        return bool(user and user["password_hash"] == password_hash)
