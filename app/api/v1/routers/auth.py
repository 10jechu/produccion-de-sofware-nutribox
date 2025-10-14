from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.deps import get_db
from app.db.schemas.user import UserRegister, UserRead, Token
from app.crud.user import create as create_user, authenticate
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        u = create_user(db, nombre=payload.nombre, email=payload.email, password=payload.password)
        return u
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# OAuth2PasswordRequestForm: recibe form-data (username, password)
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = authenticate(db, form_data.username, form_data.password)
    if not u:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(u.id)})
    return {"access_token": token, "token_type": "bearer"}
