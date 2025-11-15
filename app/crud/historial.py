from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.historial import HistorialAlimento
from app.db.models.alimento import Alimento

def crear_historial(db: Session, alimento_id: int, usuario_id: int, accion: str, motivo: str = None) -> HistorialAlimento:
    historial = HistorialAlimento(
        alimento_id=alimento_id,
        usuario_id=usuario_id,
        accion=accion,
        motivo=motivo
    )
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial

def listar_historial_usuario(db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> list[HistorialAlimento]:
    stmt = (
        select(HistorialAlimento)
        .where(HistorialAlimento.usuario_id == usuario_id)
        .order_by(HistorialAlimento.fecha.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()

def listar_historial_completo(db: Session, usuario_id: int, skip: int = 0, limit: int = 100) -> list:
    stmt = (
        select(
            HistorialAlimento.id,
            HistorialAlimento.alimento_id,
            Alimento.nombre.label('alimento_nombre'),
            Alimento.kcal.label('alimento_kcal'),
            Alimento.proteinas.label('alimento_proteinas'),
            Alimento.carbos.label('alimento_carbos'),
            HistorialAlimento.usuario_id,
            HistorialAlimento.accion,
            HistorialAlimento.fecha,
            HistorialAlimento.motivo
        )
        .join(Alimento, Alimento.id == HistorialAlimento.alimento_id)
        .where(HistorialAlimento.usuario_id == usuario_id)
        .order_by(HistorialAlimento.fecha.desc())
        .offset(skip)
        .limit(limit)
    )
    return db.execute(stmt).all()

def obtener_historial_por_id(db: Session, historial_id: int) -> HistorialAlimento:
    return db.get(HistorialAlimento, historial_id)

def eliminar_historial(db: Session, historial_id: int) -> None:
    historial = db.get(HistorialAlimento, historial_id)
    if historial:
        db.delete(historial)
        db.commit()
