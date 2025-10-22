from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.database import engine
from app.db.models.usuario import Usuario
from app.crud.usuario import get_usuarios, create_usuario, get_usuario, delete_usuario

router = APIRouter(prefix="/usuarios", tags=["01 - Usuarios"])

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Usuario])
def listar_usuarios(session: Session = Depends(get_session)):
    return get_usuarios(session)

@router.get("/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int, session: Session = Depends(get_session)):
    usuario = get_usuario(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=Usuario)
def crear_usuario(usuario: Usuario, session: Session = Depends(get_session)):
    return create_usuario(session, usuario)

@router.delete("/{user_id}", response_model=dict)
def eliminar_usuario(user_id: int, session: Session = Depends(get_session)):
    usuario = delete_usuario(session, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
