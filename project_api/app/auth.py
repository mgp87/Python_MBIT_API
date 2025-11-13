import hashlib
from fastapi import HTTPException, status

def hash_password(raw: str) -> str:
    # Hash simple para el ejemplo (NO usar en producción)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def ensure_strongish(username: str, password: str):
    if not username or not password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username y password son requeridos")
    if len(password) < 4:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password demasiado corto (>=4)")
