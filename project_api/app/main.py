from pathlib import Path
from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status

from .repositories import FileUserRepo
from .auth import hash_password, ensure_strongish

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ---- Dependency: repositorio de usuarios ----
USERS_FILE = Path("app/data/users.txt")

def get_user_repo() -> FileUserRepo:
    return FileUserRepo(USERS_FILE)

# ---- Páginas existentes ----
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return PlainTextResponse("User-agent: *\nDisallow:")

# ---- Register ----
@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

@app.post("/register")
async def register_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    repo: FileUserRepo = Depends(get_user_repo)
):
    ensure_strongish(username, password)
    try:
        repo.add_user(username, hash_password(password))
    except ValueError as e:
        # Usuario ya existe
        return templates.TemplateResponse("register.html", {"request": request, "error": str(e)}, status_code=400)
    # Redirige a login para el ejemplo
    response = RedirectResponse(url="/login?registered=1", status_code=status.HTTP_303_SEE_OTHER)
    return response

# ---- Login ----
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, registered: int | None = None):
    msg = "Registro correcto, inicia sesión" if registered else None
    return templates.TemplateResponse("login.html", {"request": request, "error": None, "message": msg})

@app.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    repo: FileUserRepo = Depends(get_user_repo)
):
    ok = repo.verify(username, hash_password(password))
    if not ok:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas", "message": None}, status_code=400)

    # Para el ejemplo, “marcamos” sesión con una cookie simple (NO seguro)
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie("session_user", username, httponly=True)
    return response
