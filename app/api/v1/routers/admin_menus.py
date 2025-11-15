from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security_deps import get_current_admin_user
from app.db.schemas.menu import MenuCreate, MenuUpdate, MenuRead, MenuDetail
from app.crud import menu as crud

router = APIRouter(prefix="/admin/menus", tags=["admin-menus"])

@router.get("/", response_model=list[MenuRead], summary="Listar todos los menus predeterminados")
def list_menus(
    activo_only: bool = True,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    "Solo administradores pueden ver todos los menus"
    menus = crud.list_menus(db, activo_only=activo_only)
    # Convertir cada menu al formato correcto
    formatted_menus = []
    for menu in menus:
        formatted_menus.append(crud.get_menu_with_alimentos_formatted(db, menu.id))
    return formatted_menus

@router.get("/{menu_id}", response_model=MenuDetail, summary="Obtener detalle de un menu")
def get_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    "Obtiene detalle completo de un menu con nutrición"
    menu_detail = crud.get_menu_detail(db, menu_id)
    if not menu_detail:
        raise HTTPException(status_code=404, detail="Menu no encontrado")
    return menu_detail

@router.post("/", response_model=MenuRead, status_code=status.HTTP_201_CREATED, summary="Crear nuevo menu predeterminado")
def create_menu(
    payload: MenuCreate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    "Crea un nuevo menu predeterminado (solo admin)"
    try:
        menu = crud.create_menu(db, payload, admin_user.id)
        # Devolver el menu formateado correctamente
        return crud.get_menu_with_alimentos_formatted(db, menu.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{menu_id}", response_model=MenuRead, summary="Actualizar menu")
def update_menu(
    menu_id: int,
    payload: MenuUpdate,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    "Actualiza un menu existente (solo admin)"
    try:
        menu = crud.update_menu(db, menu_id, payload)
        return crud.get_menu_with_alimentos_formatted(db, menu.id)
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Desactivar menu")
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    admin_user = Depends(get_current_admin_user)
):
    "Desactiva un menu (soft delete)"
    try:
        crud.delete_menu(db, menu_id)
        return
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
