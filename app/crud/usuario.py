from sqlmodel import Session, select
from app.db.models.usuario import Usuario

def get_usuarios(session: Session):
    return session.exec(select(Usuario)).all()

def get_usuario(session: Session, user_id: int):
    return session.get(Usuario, user_id)

def create_usuario(session: Session, usuario: Usuario):
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

def delete_usuario(session: Session, user_id: int):
    usuario = session.get(Usuario, user_id)
    if usuario:
        session.delete(usuario)
        session.commit()
    return usuario
