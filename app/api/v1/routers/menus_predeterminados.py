# app/api/v1/routers/menus_predeterminados.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.deps import get_db, require_admin # Usaremos require_admin para proteger
from app.db.schemas.menu import (
    MenuPredeterminadoCreate, MenuPredeterminadoRead, MenuPredeterminadoUpdate,
    MenuItemCreate, MenuItemRead, MenuPredeterminadoDetail
)
from app.crud import menu as crud
from app.db.models.core_models import Usuario # Para la dependencia require_admin

router = APIRouter(prefix="/menus-predeterminados", tags=["menus_predeterminados"])

# --- Endpoints Públicos (GET) ---

@router.get("/", response_model=list[MenuPredeterminadoDetail], summary="Listar todos los menús predeterminados")
def list_menus_predeterminados(db: Session = Depends(get_db)):
    """Obtiene la lista de menús predeterminados disponibles para los usuarios."""
    menus = crud.list_menus(db)
    # Calculamos la nutrición para cada menú antes de devolverlo
    detailed_menus = []
    for menu in menus:
        nutricion = crud.calculate_menu_nutrition(menu)
        menu_detail = MenuPredeterminadoDetail.model_validate(menu) # Usa model_validate en Pydantic v2
        menu_detail.nutricion_total = nutricion
        menu_detail.costo_total = nutricion.get('costo_total', 0)
        detailed_menus.append(menu_detail)
    return detailed_menus

@router.get("/{menu_id}", response_model=MenuPredeterminadoDetail, summary="Obtener un menú predeterminado por ID")
def get_menu_predeterminado(menu_id: int, db: Session = Depends(get_db)):
    """Obtiene los detalles de un menú predeterminado específico."""
    menu = crud.get_menu_by_id(db, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menú predeterminado no encontrado")
    nutricion = crud.calculate_menu_nutrition(menu)
    menu_detail = MenuPredeterminadoDetail.model_validate(menu)
    menu_detail.nutricion_total = nutricion
    menu_detail.costo_total = nutricion.get('costo_total', 0)
    return menu_detail

# --- Endpoints Protegidos (Solo Admin) ---

@router.post("/", response_model=MenuPredeterminadoRead, status_code=status.HTTP_201_CREATED, summary="Crear un menú predeterminado (Admin Only)")
def create_menu_predeterminado(
    payload: MenuPredeterminadoCreate,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # Protegido
):
    """Crea una nueva plantilla de menú (solo administradores)."""
    try:
        return crud.create_menu(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{menu_id}", response_model=MenuPredeterminadoRead, summary="Actualizar nombre/descripción de menú (Admin Only)")
def update_menu_predeterminado(
    menu_id: int,
    payload: MenuPredeterminadoUpdate,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # Protegido
):
    """Actualiza el nombre o descripción de una plantilla de menú (solo administradores)."""
    try:
        updated_menu = crud.update_menu(db, menu_id, payload)
        if not updated_menu:
            raise HTTPException(status_code=404, detail="Menú predeterminado no encontrado")
        return updated_menu
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un menú predeterminado (Admin Only)")
def delete_menu_predeterminado(
    menu_id: int,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # Protegido
):
    """Elimina una plantilla de menú y sus items asociados (solo administradores)."""
    deleted = crud.delete_menu(db, menu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menú predeterminado no encontrado")
    return # Retorna 204 No Content

# --- Endpoints para Items del Menú (Protegidos) ---

@router.post("/{menu_id}/items", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED, summary="Agregar item a menú predeterminado (Admin Only)")
def add_item_to_menu_predeterminado(
    menu_id: int,
    payload: MenuItemCreate,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # Protegido
):
    """Agrega un alimento a una plantilla de menú existente (solo administradores)."""
    try:
        item = crud.add_item_to_menu(db, menu_id, payload)
        # Recargar el item con el alimento para la respuesta
        db.refresh(item, attribute_names=['alimento'])
        return item
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{menu_id}/items/{alimento_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Quitar item de menú predeterminado (Admin Only)")
def remove_item_from_menu_predeterminado(
    menu_id: int,
    alimento_id: int,
    db: Session = Depends(get_db),
    admin_user: Usuario = Depends(require_admin) # Protegido
):
    """Quita un alimento de una plantilla de menú (solo administradores)."""
    deleted = crud.remove_item_from_menu(db, menu_id, alimento_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item no encontrado en este menú")
    return