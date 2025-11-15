from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.core.security_deps import get_current_user, get_current_premium_user
from app.db.models.core_models import Hijo, Lonchera, LoncheraAlimento
from app.db.models.alimento import Alimento
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/{hijo_id}", summary="Obtener estadísticas de un hijo")
def get_child_stats(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    "Obtiene estadísticas nutricionales de un hijo específico"
    
    # Verificar que el hijo pertenece al usuario
    hijo = db.get(Hijo, hijo_id)
    if not hijo or hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    # Estadísticas básicas
    total_loncheras = db.scalar(
        select(func.count()).select_from(Lonchera).where(Lonchera.hijo_id == hijo_id)
    ) or 0
    
    # Calcular promedios nutricionales
    stats_query = db.execute(
        select(
            func.avg(Alimento.kcal * LoncheraAlimento.cantidad).label('avg_calorias'),
            func.avg(Alimento.proteinas * LoncheraAlimento.cantidad).label('avg_proteinas'),
            func.avg(Alimento.carbos * LoncheraAlimento.cantidad).label('avg_carbos'),
            func.sum(Alimento.costo * LoncheraAlimento.cantidad).label('total_costo')
        )
        .select_from(LoncheraAlimento)
        .join(Alimento, Alimento.id == LoncheraAlimento.alimento_id)
        .join(Lonchera, Lonchera.id == LoncheraAlimento.lonchera_id)
        .where(Lonchera.hijo_id == hijo_id)
    ).first()
    
    # Estadísticas del último mes
    last_month = datetime.now() - timedelta(days=30)
    loncheras_mes = db.scalar(
        select(func.count())
        .select_from(Lonchera)
        .where(and_(
            Lonchera.hijo_id == hijo_id,
            Lonchera.fecha >= last_month
        ))
    ) or 0
    
    return {
        "hijo_id": hijo_id,
        "hijo_nombre": hijo.nombre,
        "estadisticas": {
            "total_loncheras": total_loncheras,
            "loncheras_este_mes": loncheras_mes,
            "promedio_calorias": round(stats_query.avg_calorias or 0, 2),
            "promedio_proteinas": round(stats_query.avg_proteinas or 0, 2),
            "promedio_carbohidratos": round(stats_query.avg_carbos or 0, 2),
            "costo_total": round(stats_query.total_costo or 0, 2)
        }
    }

@router.get("/{hijo_id}/advanced", summary="Estadísticas avanzadas (Premium)")
def get_child_stats_advanced(
    hijo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_premium_user)
):
    "Estadísticas avanzadas solo para usuarios Premium"
    
    # Verificar que el hijo pertenece al usuario
    hijo = db.get(Hijo, hijo_id)
    if not hijo or hijo.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Hijo no encontrado")
    
    # Alimentos más usados
    top_alimentos = db.execute(
        select(
            Alimento.nombre,
            func.sum(LoncheraAlimento.cantidad).label('total_cantidad'),
            func.count(LoncheraAlimento.lonchera_id).label('veces_usado')
        )
        .select_from(LoncheraAlimento)
        .join(Alimento, Alimento.id == LoncheraAlimento.alimento_id)
        .join(Lonchera, Lonchera.id == LoncheraAlimento.lonchera_id)
        .where(Lonchera.hijo_id == hijo_id)
        .group_by(Alimento.id, Alimento.nombre)
        .order_by(func.sum(LoncheraAlimento.cantidad).desc())
        .limit(5)
    ).all()
    
    return {
        "hijo_id": hijo_id,
        "hijo_nombre": hijo.nombre,
        "estadisticas_avanzadas": {
            "top_alimentos": [
                {
                    "nombre": alimento.nombre,
                    "total_cantidad": alimento.total_cantidad,
                    "veces_usado": alimento.veces_usado
                }
                for alimento in top_alimentos
            ]
        }
    }
