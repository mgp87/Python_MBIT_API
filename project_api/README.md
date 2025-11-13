# Pasos para la instalación y ejecución del proyecto
## Instalación de uv

- [Docs oficial](https://docs.astral.sh/uv/getting-started/installation/)

- en macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- en Windows (PowerShell)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- Verificar:
```bash
uv --version
```

## Clonar repo e ir al proyecto

```bash
git clone https://github.com/mgp87/Python_MBIT_API.git
cd project_api
```

## Sincronizar deps

```bash
uv sync
```

## Verificación

```bash
uv run python --version
uv run pip list
```

## Ejecutar API
```bash
uv run uvicorn app.main:app --reload
```

## Ejecutar los tests
```bash
uv run pytest --cov=app
```

## Comprobaciones adicionales
Abre en el navegador: http://localhost:8000/ y http://localhost:8000/about para asegurarte de que las páginas cargan correctamente.

```bash
pytest # todos los tests

pytest -q # Salida compacta

pytest -v # verbose - útil si algo falla

pytest tests/test_auth.py # ejecutar archivo específico

pytest tests/test_auth.py::test_register_and_login_ok # ejecutar función específica

pytest tests/test_auth.py::TestAuth::test_register_and_login_ok # ejecutar función dentro de una clase de test (cuando las hay)

pytest -s -v # repetir ejecución con salida detallada

pytest -k "login" # ejecutar tests que contengan la palabra login

pytest -k "login and not invalid" # ejecutar tests que contengan la palabra login pero no invalid

pytest --cov=app # ejecutar con informe de cobertura

pytest --cov=app --cov-report=term-missing

# Todos los tests
pytest -v --disable-warnings

# Solo los de auth
pytest tests/test_auth.py -v

# Solo una función
pytest tests/test_auth.py::test_register_and_login_ok -v

# Con cobertura
pytest --cov=app --cov-report=term-missing -v

```

| Opción               | Descripción                                            |
| -------------------- | ------------------------------------------------------ |
| `-x`                 | Detiene al primer fallo                                |
| `--maxfail=3`        | Para tras 3 fallos                                     |
| `--disable-warnings` | Oculta los warnings (útil con Jinja2)                  |
| `--lf`               | Solo re-ejecuta los tests que fallaron la última vez   |
| `--ff`               | Ejecuta primero los tests que fallaron la vez anterior |


```bash

# Todos los tests
uv run pytest

# Salida detallada
uv run pytest -v

# Silenciar warnings (útil por los de Jinja/Starlette)
uv run pytest -v --disable-warnings

# Un archivo concreto
uv run pytest tests/test_auth.py -v

# Un test concreto
uv run pytest tests/test_auth.py::test_register_and_login_ok -v

# Filtrar por nombre
uv run pytest -k "login and not invalid" -v

# Con cobertura
uv run pytest --cov=app --cov-report=term-missing -v

```