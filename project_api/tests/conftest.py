import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from pathlib import Path

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

# Importamos la app de forma perezosa dentro del fixture
@pytest.fixture()
def client_auth(tmp_path: Path):
    # Preparamos un archivo de usuarios temporal por test
    users_file = tmp_path / "users.txt"

    # Monkeypatch por entorno para que main lo lea
    # Alternativa: podrías exponer la dependencia y overridearla (aquí lo haremos con override).
    from app.main import app, get_user_repo
    from app.repositories import FileUserRepo

    def _override_repo():
        return FileUserRepo(users_file)

    app.dependency_overrides[get_user_repo] = _override_repo
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture()
def client(tmp_path: Path):
    from app.main import app, get_user_repo
    from app.repositories import FileUserRepo

    users_file = tmp_path / "users.txt"

    def _override_repo():
        return FileUserRepo(users_file)

    app.dependency_overrides[get_user_repo] = _override_repo
    # Comportamiento por defecto: re-lanza (bueno para la mayoría de tests)
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture()
def client_no_raise(tmp_path: Path):
    from app.main import app, get_user_repo
    from app.repositories import FileUserRepo

    users_file = tmp_path / "users.txt"

    def _override_repo():
        return FileUserRepo(users_file)

    app.dependency_overrides[get_user_repo] = _override_repo
    # Aquí NO re-lanza: así podemos asertar un 500
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()