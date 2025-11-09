from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.db.schemas.child import HijoCreate, HijoRead, HijoUpdate
from app.db.schemas.detail import ChildDetail
from app.crud import child as crud
from app.crud import detail as detail_crud
from app.db.models.core_models import Usuario # Importa Usuario

# --- AÑADIDO: Imports para el nuevo endpoint ---
from app.crud.detail import get_advanced_statistics
from app.db.schemas.detail import AdvancedStatsResponse
from typing import List
# --- FIN DE LO AÑADIDO ---

router = APIRouter(prefix="/children", tags=["children"])

@router.get("/", response_model=list[HijoRead], summary="Listar todos los hijos de un usuario")
def list_children(usuario_id: int, db: Session = Depends(get_db)):
    """Lista todos los hijos asociados a un usuario principal."""
    return crud.list_by_user(db, usuario_id)

@router.get("/{child_id}", response_model=HijoRead, summary="Obtener un hijo por ID")
def get_child(child_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, child_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return obj

@router.get("/{child_id}/detail", response_model=ChildDetail, summary="Detalle completo del hijo")
def get_child_detail(child_id: int, db: Session = Depends(get_db)):
    """Retorna: padre, restricciones, loncheras recientes, estadísticas."""
    data = detail_crud.get_child_detail(db, child_id)
    if not data:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return data

# ### AÑADIDO: Endpoint de Estadísticas Avanzadas ###
@router.get(
    "/{child_id}/statistics", 
    response_model=AdvancedStatsResponse, 
    summary="Obtener estadísticas avanzadas (Premium)"
)
def get_child_statistics(
    child_id: int, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Necesitamos al usuario
):
    """
    Obtiene las estadísticas de consumo de un hijo para los gráficos.
    Requiere plan Premium.
    """
    # Verificación de Seguridad (Plan)
    if not current_user.membresia or current_user.membresia.tipo != 'Premium':
         raise HTTPException(
             status_code=status.HTTP_403_FORBIDDEN,
             detail="Se requiere plan Premium para acceder a esta función."
         )
         
    # Verificación de Seguridad (Propiedad)
    hijo = crud.get_by_id(db, child_id)
    if not hijo or hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Hijo no encontrado o no pertenece al usuario")

    try:
        stats = get_advanced_statistics(db, child_id)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
# ### FIN DE LO AÑADIDO ###

@router.post("/", response_model=HijoRead, status_code=status.HTTP_201_CREATED, summary="Crear un hijo")
def create_child(payload: HijoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{child_id}", response_model=HijoRead, summary="Actualizar información de un hijo")
def update_child(child_id: int, payload: HijoUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, child_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    return crud.update(db, obj, payload)

@router.delete("/{child_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un hijo")
def delete_child(child_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, child_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    crud.delete(db, obj)
    return
