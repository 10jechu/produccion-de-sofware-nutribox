from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.user import UserRead, UserUpdate
from app.db.schemas.detail import UserDetail
from app.crud import user as crud
from app.crud import detail as detail_crud

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead], summary="Listar todos los usuarios")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista todos los usuarios (admin)."""
    return crud.list_all(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserRead, summary="Obtener un usuario por ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj

@router.get("/{user_id}/detail", response_model=UserDetail, summary="Detalle completo del usuario")
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    """Retorna información completa: hijos, direcciones, loncheras, estadísticas."""
    data = detail_crud.get_user_detail(db, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return data

@router.patch("/{user_id}", response_model=UserRead, summary="Actualizar usuario")
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    obj = crud.get_by_id(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    try:
        return crud.update(db, obj, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desactivar usuario")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """Desactiva un usuario (soft delete)."""
    obj = crud.get_by_id(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    crud.deactivate(db, obj)
    return
