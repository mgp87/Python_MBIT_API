# tests/conftest.py
from pathlib import Path
import sys

# --- Garantiza que el proyecto raíz esté en sys.path ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app_module():
    """Carga la app una vez por sesión."""
    from app.main import app
    return app


# Cliente base para test_routes (SIN overrides)
@pytest.fixture(scope="module")
def client(app_module):
    """Rutas públicas (index, about, etc.)."""
    with TestClient(app_module, raise_server_exceptions=True) as c:
        yield c


# Cliente con repo temporal para tests de auth
@pytest.fixture()
def client_auth(tmp_path: Path, app_module):
    """Repo de usuarios apuntando a un fichero temporal."""
    from app.repositories import FileUserRepo
    from app.main import get_user_repo

    users_file = tmp_path / "users.txt"

    def _override_repo():
        return FileUserRepo(users_file)

    app_module.dependency_overrides[get_user_repo] = _override_repo
    try:
        with TestClient(app_module, raise_server_exceptions=True) as c:
            yield c
    finally:
        app_module.dependency_overrides.clear()


# Cliente para testear errores (no relanza excepciones)
@pytest.fixture()
def client_no_raise(tmp_path: Path, app_module):
    """Como client_auth pero sin relanzar excepciones (para asertar 500)."""
    from app.repositories import FileUserRepo
    from app.main import get_user_repo

    users_file = tmp_path / "users.txt"

    def _override_repo():
        return FileUserRepo(users_file)

    app_module.dependency_overrides[get_user_repo] = _override_repo
    try:
        with TestClient(app_module, raise_server_exceptions=False) as c:
            yield c
    finally:
        app_module.dependency_overrides.clear()
