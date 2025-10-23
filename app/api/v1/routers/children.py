from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.schemas.child import HijoCreate, HijoRead, HijoUpdate
from app.crud import child as crud

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
