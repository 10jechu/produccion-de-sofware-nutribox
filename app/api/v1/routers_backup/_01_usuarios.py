from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.db.session import engine
from app.db.models.usuario import Usuario, UsuarioCreate, UsuarioRead

router = APIRouter(prefix="/api/v1/usuarios", tags=["01 - Usuarios"])

@router.post("/", response_model=UsuarioRead)
def create_usuario(usuario: UsuarioCreate):
    with Session(engine) as session:
        # Verificar si el correo ya existe
        existing_user = session.exec(select(Usuario).where(Usuario.correo == usuario.correo)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        # Crear nuevo usuario sin intentar mapear relaciones no inicializadas
        db_usuario = Usuario(nombre=usuario.nombre, correo=usuario.correo, contrasena=usuario.contrasena)
        session.add(db_usuario)
        try:
            session.commit()
            session.refresh(db_usuario)
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error al guardar el usuario: {str(e)}")
        return db_usuario

@router.get("/", response_model=list[UsuarioRead])
def list_usuarios():
    with Session(engine) as session:
        return session.exec(select(Usuario)).all()

@router.get("/{id}", response_model=UsuarioRead)
def get_usuario(id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

@router.delete("/{id}")
def delete_usuario(id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        session.delete(usuario)
        session.commit()
        return {"message": "Usuario eliminado"}
