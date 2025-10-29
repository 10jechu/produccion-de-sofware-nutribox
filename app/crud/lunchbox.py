from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.lunchbox import Lonchera, LoncheraAlimento
from app.db.models.core_models import Hijo
from app.db.models.alimento import Alimento
from app.db.models.address import Direccion
from sqlalchemy import delete as sqlalchemy_delete
from datetime import date

# Función de list_ corregida (ya incluida)
def list_(db: Session, hijo_id: int | None = None, usuario_id: int | None = None) -> list[Lonchera]:
    stmt = select(Lonchera)
    if hijo_id:
        stmt = stmt.where(Lonchera.hijo_id == hijo_id)
    elif usuario_id:
        stmt = stmt.join(Hijo).where(Hijo.usuario_id == usuario_id)
    return db.scalars(stmt).all()

# --- NUEVA FUNCIÓN: COPIA DE LONCHERA ---
def copy_lunchbox(db: Session, original_lunchbox_id: int, target_hijo_id: int) -> Lonchera:
    original = db.get(Lonchera, original_lunchbox_id)
    if not original:
        raise LookupError("Menú original no encontrado")

    target_hijo = db.get(Hijo, target_hijo_id)
    if not target_hijo:
        raise ValueError("Hijo de destino no encontrado")

    # 1. Crear nueva Lonchera (Borrador)
    new_lunchbox = Lonchera(
        hijo_id=target_hijo_id,
        fecha=date.today(),
        estado="Borrador", # Siempre como borrador
        direccion_id=None
    )
    db.add(new_lunchbox)
    db.flush() # Obtener ID antes del commit

    # 2. Copiar Ítems (LoncheraAlimento)
    original_items = db.scalars(
        select(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == original_lunchbox_id)
    ).all()

    new_items = []
    for item in original_items:
        new_items.append(
            LoncheraAlimento(
                lonchera_id=new_lunchbox.id,
                alimento_id=item.alimento_id,
                cantidad=item.cantidad
            )
        )
    
    if new_items:
        db.add_all(new_items)
        
    db.commit()
    db.refresh(new_lunchbox)
    return new_lunchbox
# --- FIN NUEVA FUNCIÓN ---

def get_by_id(db: Session, lonchera_id: int) -> Lonchera | None:
    return db.get(Lonchera, lonchera_id)

def create(db: Session, payload) -> Lonchera:
    hijo = db.get(Hijo, payload.hijo_id)
    if not hijo:
        raise ValueError("Hijo no encontrado")
    
    if payload.direccion_id:
        direccion = db.get(Direccion, payload.direccion_id)
        if not direccion:
            raise ValueError("Dirección no encontrada")
    
    obj = Lonchera(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, obj: Lonchera, payload) -> Lonchera:
    data = payload.model_dump(exclude_none=True)
    
    if "direccion_id" in data and data["direccion_id"]:
        direccion = db.get(Direccion, data["direccion_id"])
        if not direccion:
            raise ValueError("Dirección no encontrada")
    
    for k, v in data.items():
        setattr(obj, k, v)
    
    db.commit()
    db.refresh(obj)
    return obj

def list_items(db: Session, lonchera_id: int) -> list[LoncheraAlimento]:
    return db.scalars(
        select(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == lonchera_id)
    ).all()

def add_item(db: Session, lonchera_id: int, item) -> None:
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise LookupError("Lonchera no encontrada")
    
    alimento = db.get(Alimento, item.alimento_id)
    if not alimento:
        raise ValueError("Alimento no encontrado")
    
    existing = db.scalar(
        select(LoncheraAlimento).where(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == item.alimento_id
        )
    )
    
    if existing:
        raise ValueError("Este alimento ya está en la lonchera")
    
    obj = LoncheraAlimento(
        lonchera_id=lonchera_id,
        alimento_id=item.alimento_id,
        cantidad=item.cantidad
    )
    db.add(obj)
    db.commit()

def update_item(db: Session, lonchera_id: int, alimento_id: int, payload) -> None:
    item = db.scalar(
        select(LoncheraAlimento).where(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == alimento_id
        )
    )
    
    if not item:
        raise LookupError("Item no encontrado en esta lonchera")
    
    item.cantidad = payload.cantidad
    db.commit()

def remove_item(db: Session, lonchera_id: int, alimento_id: int) -> None:
    item = db.scalar(
        select(LoncheraAlimento).where(
            LoncheraAlimento.lonchera_id == lonchera_id,
            LoncheraAlimento.alimento_id == alimento_id
        )
    )
    
    if not item:
        raise LookupError("Item no encontrado")
    
    db.delete(item)
    db.commit()

def delete(db: Session, lonchera_id: int) -> None:
    """Elimina una lonchera y todos sus LoncheraAlimento asociados."""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise LookupError("Lonchera no encontrada")

    # Eliminar primero los items asociados (LoncheraAlimento)
    db.execute(
        sqlalchemy_delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == lonchera_id)
    )

    # Luego eliminar la lonchera
    db.delete(lonchera)
    db.commit()
