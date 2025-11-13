def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    # Ajusta aquí el texto que hayas puesto en <h2> de index.html
    assert "<h2>Transformamos tus ideas en software</h2>" in resp.text

def test_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    # Ajusta este <h2> al de about.html
    assert "<h2>Quiénes somos</h2>" in resp.text
    # Puedes añadir más comprobaciones, ej. que aparece el nombre del equipo
    assert "Somos un equipo dedicado a ayudar a desarrolladores" in resp.text

def test_robots(client):
    resp = client.get("/robots.txt")
    assert resp.status_code == 200
    assert "User-agent: *" in resp.text
    assert "Disallow:" in resp.text

def test_nav_links_on_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    # Verifica que existe el enlace a “Sobre nosotros”
    assert '<a href="/about">' in resp.text
    # Verifica que existe el enlace a “Inicio”
    assert '<a href="/">' in resp.text

def test_nav_links_on_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert '<a href="/about">' in resp.text
    assert '<a href="/">' in resp.text

def test_css_link_present(client):
    resp = client.get("/")
    assert resp.status_code == 200
    # Verifica que el CSS está enlazado
    assert '<link rel="stylesheet" href="/static/style.css">' in resp.text

def test_css_loading_returned(client):
    # Verifica que el archivo CSS es servido correctamente
    resp = client.get("/static/style.css")
    assert resp.status_code == 200
    assert "body" in resp.text  # una clase o selector común del CSS

def test_footer_content(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "&copy; 2025 Mi Empresa" in resp.text