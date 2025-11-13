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
cd Python_MBIT_API
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