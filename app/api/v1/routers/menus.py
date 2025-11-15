from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security_deps import get_current_admin_user
from app.db.schemas.lunchbox import LoncheraCreate, LoncheraRead, LoncheraUpdate
from app.crud import lunchbox as crud

router = APIRouter(prefix="/menus", tags=["menus"])

# GET - Listar menús predeterminados (todos pueden ver)
@router.get('/', response_model=list[LoncheraRead], summary='Listar Menus Predeterminados')
def list_menus(db: Session = Depends(get_db)):
    # Menús = Loncheras creadas por el Admin (usuario_id 1)
    return crud.list_(db, usuario_id=1)

# GET - Obtener un menú específico
@router.get('/{menu_id}', response_model=LoncheraRead, summary='Obtener un menú')
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, menu_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    return obj

# POST - Crear nuevo menú base (solo admin)
@router.post('/', response_model=LoncheraRead, status_code=status.HTTP_201_CREATED, summary='Crear menú base (Admin)')
def create_menu(
    payload: LoncheraCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    try:
        return crud.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# PUT - Actualizar menú base (solo admin)  
@router.put('/{menu_id}', response_model=LoncheraRead, summary='Actualizar menú base (Admin)')
def update_menu(
    menu_id: int,
    payload: LoncheraUpdate, 
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    obj = crud.get_by_id(db, menu_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    try:
        return crud.update(db, obj, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE - Eliminar menú base (solo admin)
@router.delete('/{menu_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Eliminar menú base (Admin)')
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    obj = crud.get_by_id(db, menu_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Menú no encontrado")
    try:
        crud.delete(db, menu_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))