from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security_deps import get_current_user
from app.db.models.core_models import Hijo
from app.db.models.address import Direccion

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}/children-and-addresses", summary="Obtener hijos y direcciones del usuario")
def get_children_and_addresses(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    "Endpoint consolidado para obtener hijos y direcciones (usado en crear lonchera)"
    
    # Verificar que el usuario accede a sus propios datos
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No autorizado")
    
    # Obtener hijos
    hijos = db.query(Hijo).filter(Hijo.usuario_id == user_id).all()
    hijos_data = [{"id": h.id, "nombre": h.nombre} for h in hijos]
    
    # Obtener direcciones
    direcciones = db.query(Direccion).filter(Direccion.usuario_id == user_id).all()
    direcciones_data = [{"id": d.id, "etiqueta": d.etiqueta, "direccion": d.direccion} for d in direcciones]
    
    return {
        "hijos": hijos_data,
        "direcciones": direcciones_data
    }
