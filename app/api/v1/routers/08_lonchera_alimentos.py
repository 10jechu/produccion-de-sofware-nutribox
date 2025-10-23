from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.deps import get_db, get_current_user
from app.db.models.lonchera import Lonchera
from app.db.models.lonchera_alimento import LoncheraAlimento
from app.db.models.alimento import Alimento
from app.db.models.usuario import Usuario
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/loncheras", tags=["08 - Lonchera Alimentos"])

# Schemas
class LoncheraAlimentoCreate(BaseModel):
    alimento_id: int
    cantidad: float = Field(gt=0, default=1.0)

class LoncheraAlimentoUpdate(BaseModel):
    cantidad: float = Field(gt=0)

class LoncheraAlimentoRead(BaseModel):
    id: int
    alimento_id: int
    cantidad: float
    nombre_alimento: str | None = None
    calorias_totales: float | None = None
    model_config = ConfigDict(from_attributes=True)

class ResumenNutricional(BaseModel):
    total_calorias: float
    total_proteinas: float
    total_grasas: float
    total_carbohidratos: float

@router.post("/{lonchera_id}/alimentos", status_code=status.HTTP_201_CREATED, summary="Agregar alimento a lonchera")
def add_alimento_to_lonchera(
    lonchera_id: int,
    payload: LoncheraAlimentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Agregar un alimento a una lonchera"""
    # Verificar que la lonchera exista y pertenezca al usuario
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes modificar esta lonchera")
    
    # Verificar que el alimento exista
    alimento = db.get(Alimento, payload.alimento_id)
    if not alimento:
        raise HTTPException(status_code=404, detail="Alimento no encontrado")
    if not alimento.activo:
        raise HTTPException(status_code=400, detail="El alimento no está activo")
    
    # Verificar si ya existe (unique constraint)
    existe = db.query(LoncheraAlimento).filter_by(
        lonchera_id=lonchera_id,
        alimento_id=payload.alimento_id
    ).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="El alimento ya está en la lonchera")
    
    # Crear relación
    item = LoncheraAlimento(
        lonchera_id=lonchera_id,
        alimento_id=payload.alimento_id,
        cantidad=payload.cantidad
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return {
        "message": f"Alimento '{alimento.nombre}' agregado a la lonchera",
        "item": {
            "id": item.id,
            "alimento_id": item.alimento_id,
            "cantidad": item.cantidad
        }
    }

@router.get("/{lonchera_id}/alimentos", response_model=List[dict], summary="Ver alimentos de lonchera")
def list_alimentos_in_lonchera(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Listar todos los alimentos de una lonchera"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta lonchera")
    
    items = db.query(LoncheraAlimento).filter_by(lonchera_id=lonchera_id).all()
    
    result = []
    for item in items:
        alimento = db.get(Alimento, item.alimento_id)
        result.append({
            "id": item.id,
            "alimento_id": item.alimento_id,
            "nombre": alimento.nombre if alimento else "Desconocido",
            "cantidad": item.cantidad,
            "unidad": alimento.unidad if alimento else "",
            "calorias_unitarias": alimento.calorias if alimento else 0,
            "calorias_totales": (alimento.calorias * item.cantidad) if alimento else 0,
            "proteinas_totales": (alimento.proteinas * item.cantidad) if alimento else 0,
            "grasas_totales": (alimento.grasas * item.cantidad) if alimento else 0,
            "carbohidratos_totales": (alimento.carbohidratos * item.cantidad) if alimento else 0,
        })
    
    return result

@router.patch("/{lonchera_id}/alimentos/{alimento_id}", summary="Actualizar cantidad de alimento")
def update_alimento_cantidad(
    lonchera_id: int,
    alimento_id: int,
    payload: LoncheraAlimentoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Actualizar la cantidad de un alimento en la lonchera"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes modificar esta lonchera")
    
    item = db.query(LoncheraAlimento).filter_by(
        lonchera_id=lonchera_id,
        alimento_id=alimento_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="El alimento no está en esta lonchera")
    
    item.cantidad = payload.cantidad
    db.commit()
    db.refresh(item)
    
    return {"message": "Cantidad actualizada", "nueva_cantidad": item.cantidad}

@router.delete("/{lonchera_id}/alimentos/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Quitar alimento de lonchera")
def remove_alimento_from_lonchera(
    lonchera_id: int,
    alimento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Quitar un alimento de una lonchera"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes modificar esta lonchera")
    
    item = db.query(LoncheraAlimento).filter_by(
        lonchera_id=lonchera_id,
        alimento_id=alimento_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="El alimento no está en esta lonchera")
    
    db.delete(item)
    db.commit()
    return None

@router.get("/{lonchera_id}/resumen", response_model=ResumenNutricional, summary="Resumen nutricional de lonchera")
def get_resumen_nutricional(
    lonchera_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Calcular el resumen nutricional total de una lonchera"""
    lonchera = db.get(Lonchera, lonchera_id)
    if not lonchera:
        raise HTTPException(status_code=404, detail="Lonchera no encontrada")
    if lonchera.hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes acceso a esta lonchera")
    
    items = db.query(LoncheraAlimento).filter_by(lonchera_id=lonchera_id).all()
    
    total_calorias = 0.0
    total_proteinas = 0.0
    total_grasas = 0.0
    total_carbohidratos = 0.0
    
    for item in items:
        alimento = db.get(Alimento, item.alimento_id)
        if alimento:
            total_calorias += alimento.calorias * item.cantidad
            total_proteinas += alimento.proteinas * item.cantidad
            total_grasas += alimento.grasas * item.cantidad
            total_carbohidratos += alimento.carbohidratos * item.cantidad
    
    return {
        "total_calorias": round(total_calorias, 2),
        "total_proteinas": round(total_proteinas, 2),
        "total_grasas": round(total_grasas, 2),
        "total_carbohidratos": round(total_carbohidratos, 2)
    }
