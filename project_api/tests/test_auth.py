import pytest

def test_register_and_login_ok(client_auth):
    # NO seguir redirecciones aquí
    r = client_auth.post("/register", data={"username": "ana", "password": "1234"}, follow_redirects=False)
    assert r.status_code in (303, 307)

    # Login ok
    r2 = client_auth.post("/login", data={"username": "ana", "password": "1234"}, follow_redirects=False)
    assert r2.status_code in (303, 307)
    assert "session_user=ana" in r2.headers.get("set-cookie", "")


def test_register_duplicate_username(client_auth):
    client_auth.post("/register", data={"username": "ana", "password": "1234"})
    r = client_auth.post("/register", data={"username": "ana", "password": "abcd"})
    assert r.status_code == 400
    assert "Usuario ya existe" in r.text

@pytest.mark.parametrize(
    "username,password",
    [
        ("", "1234"),            # username vacío
        ("pepe", ""),            # password vacío
        ("pepe", "123"),         # password corto
    ],
)
def test_register_validation_errors(client_auth, username, password):
    r = client_auth.post("/register", data={"username": username, "password": password})
    assert r.status_code == 400

@pytest.mark.parametrize(
    "username,password",
    [
        ("noexiste", "1234"),
        ("ana", "mala"),  # usuario real pero pass incorrecta
    ],
)
def test_login_invalid(client_auth, username, password):
    # Creamos un usuario válido
    client_auth.post("/register", data={"username": "ana", "password": "1234"})

    r = client_auth.post("/login", data={"username": username, "password": password})
    assert r.status_code == 400
    assert "Credenciales inválidas" in r.text

def test_repo_mock_error_on_add(client_no_raise, monkeypatch):
    from app.main import get_user_repo, app
    repo = get_user_repo()

    def boom(*args, **kwargs):
        raise IOError("fallo IO simulado")

    # Parcheamos el método del repo
    monkeypatch.setattr(repo, "add_user", boom)
    # Inyectamos ese repo parcheado en la dependencia
    app.dependency_overrides[get_user_repo] = lambda: repo

    r = client_no_raise.post("/register", data={"username": "x", "password": "1234"})
    assert r.status_code == 500

    app.dependency_overrides.pop(get_user_repo, None)
