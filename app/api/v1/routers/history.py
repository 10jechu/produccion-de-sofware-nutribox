from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security_deps import get_current_premium_user
from app.db.schemas.historial import HistorialCreate, HistorialRead, HistorialReadWithAlimento
from app.crud import historial as crud

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=list[HistorialReadWithAlimento], summary="Obtener historial de alimentos (Premium)")
def listar_historial(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    premium_user = Depends(get_current_premium_user)
):
    "Solo usuarios Premium pueden ver el historial de alimentos"
    return crud.listar_historial_completo(db, premium_user.id, skip=skip, limit=limit)

@router.post("/", response_model=HistorialRead, status_code=status.HTTP_201_CREATED, summary="Registrar acción en historial")
def crear_registro_historial(
    payload: HistorialCreate,
    db: Session = Depends(get_db),
    premium_user = Depends(get_current_premium_user)
):
    "Registra una acción en el historial (solo Premium)"
    try:
        return crud.crear_historial(
            db, 
            payload.alimento_id, 
            premium_user.id, 
            payload.accion, 
            payload.motivo
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{historial_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar registro del historial")
def eliminar_registro_historial(
    historial_id: int,
    db: Session = Depends(get_db),
    premium_user = Depends(get_current_premium_user)
):
    "Elimina un registro del historial (solo Premium)"
    try:
        crud.eliminar_historial(db, historial_id)
        return
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
