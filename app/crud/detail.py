from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from datetime import datetime, timedelta
from app.db.models.core_models import Usuario, Rol, Membresia, Hijo
from app.db.models.address import Direccion
from app.db.models.lunchbox import Lonchera, LoncheraAlimento
from app.db.models.restriction import Restriccion
from app.db.models.alimento import Alimento

def get_user_detail(db: Session, user_id: int) -> dict | None:
    user = db.get(Usuario, user_id)
    if not user: return None
    
    rol = db.get(Rol, user.rol_id)
    membresia = db.get(Membresia, user.membresia_id)
    
    hijos = db.scalars(select(Hijo).where(Hijo.usuario_id == user_id)).all()
    hijos_data = []
    for hijo in hijos:
        rest_count = db.scalar(select(func.count()).select_from(Restriccion).where(Restriccion.hijo_id == hijo.id))
        lonch_activas = db.scalar(select(func.count()).select_from(Lonchera).where(
            Lonchera.hijo_id == hijo.id,
            Lonchera.estado.in_(["Borrador", "Confirmada"])
        ))
        hijos_data.append({
            "id": hijo.id,
            "nombre": hijo.nombre,
            "restricciones_count": rest_count or 0,
            "loncheras_activas": lonch_activas or 0
        })
    
    direcciones = db.scalars(select(Direccion).where(Direccion.usuario_id == user_id)).all()
    dirs_data = [{"id": d.id, "etiqueta": d.etiqueta, "direccion": d.direccion, "ciudad": d.ciudad} for d in direcciones]
    
    total_loncheras = db.scalar(
        select(func.count()).select_from(Lonchera).join(Hijo).where(Hijo.usuario_id == user_id)
    )
    
    primer_dia_mes = datetime.now().replace(day=1)
    loncheras_mes = db.scalar(
        select(func.count()).select_from(Lonchera).join(Hijo).where(
            Hijo.usuario_id == user_id,
            Lonchera.fecha >= primer_dia_mes
        )
    )
    
    # --- INICIO DE MODIFICACIÓN: Lógica de Estadísticas Básicas ---
    hijo_ids = [h.id for h in hijos]
    
    # Inicializa los valores en 0
    avg_kcal = 0.0
    avg_prot = 0.0
    avg_carbs = 0.0

    # SOLO calcular si el usuario TIENE hijos
    if len(hijo_ids) > 0:
        total_nutrition_stats = (
            db.query(
                func.sum(Alimento.kcal * LoncheraAlimento.cantidad).label('total_kcal'),
                func.sum(Alimento.proteinas * LoncheraAlimento.cantidad).label('total_proteinas'),
                func.sum(Alimento.carbos * LoncheraAlimento.cantidad).label('total_carbos')
            )
            .join(LoncheraAlimento, Alimento.id == LoncheraAlimento.alimento_id)
            .join(Lonchera, Lonchera.id == LoncheraAlimento.lonchera_id)
            .where(
                Lonchera.hijo_id.in_(hijo_ids),
                Lonchera.estado.in_(['Confirmada', 'Archivada'])
            )
            .first()
        )

        total_loncheras_confirmadas = db.scalar(
             select(func.count(Lonchera.id))
            .where(
                Lonchera.hijo_id.in_(hijo_ids),
                Lonchera.estado.in_(['Confirmada', 'Archivada'])
            )
        ) or 0

        # Prevenir división por cero
        if total_loncheras_confirmadas > 0:
            avg_kcal = (total_nutrition_stats.total_kcal or 0) / total_loncheras_confirmadas
            avg_prot = (total_nutrition_stats.total_proteinas or 0) / total_loncheras_confirmadas
            avg_carbs = (total_nutrition_stats.total_carbos or 0) / total_loncheras_confirmadas
    # --- FIN DE MODIFICACIÓN ---

    return {
        "id": user.id,
        "nombre": user.nombre,
        "email": user.email,
        "rol": {"id": rol.id, "nombre": rol.nombre},
        "membresia": {"id": membresia.id, "tipo": membresia.tipo, "max_direcciones": membresia.max_direcciones},
        "hijos": hijos_data,
        "direcciones": dirs_data,
        "resumen": {
            "total_hijos": len(hijos),
            "total_direcciones": len(direcciones),
            "total_loncheras": total_loncheras or 0,
            "loncheras_este_mes": loncheras_mes or 0,
            "avg_kcal": round(avg_kcal, 1),
            "avg_proteinas": round(avg_prot, 1),
            "avg_carbos": round(avg_carbs, 1)
        }
    }

def get_child_detail(db: Session, child_id: int) -> dict | None:
    hijo = db.get(Hijo, child_id)
    if not hijo: return None
    
    padre = db.get(Usuario, hijo.usuario_id)
    
    restricciones = db.scalars(select(Restriccion).where(Restriccion.hijo_id == child_id)).all()
    rest_data = []
    for r in restricciones:
        alimento_nombre = None
        if r.alimento_id:
            alimento = db.get(Alimento, r.alimento_id)
            alimento_nombre = alimento.nombre if alimento else None
        rest_data.append({
            "id": r.id,
            "tipo": r.tipo,
            "alimento_nombre": alimento_nombre,
            "texto": r.texto
        })
    
    loncheras = db.scalars(
        select(Lonchera).where(Lonchera.hijo_id == child_id).order_by(Lonchera.fecha.desc()).limit(5)
    ).all()
    lonch_data = []
    for l in loncheras:
        items_count = db.scalar(select(func.count()).select_from(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == l.id))
        lonch_data.append({
            "id": l.id,
            "fecha": l.fecha,
            "estado": l.estado,
            "items_count": items_count or 0
        })
    
    total_loncheras = db.scalar(select(func.count()).select_from(Lonchera).where(Lonchera.hijo_id == child_id))
    
    items_all = db.execute(
        select(Alimento.kcal, LoncheraAlimento.cantidad)
        .join(LoncheraAlimento, Alimento.id == LoncheraAlimento.alimento_id)
        .join(Lonchera, Lonchera.id == LoncheraAlimento.lonchera_id)
        .where(Lonchera.hijo_id == child_id)
    ).all()
    
    total_cal = sum(item[0] * item[1] for item in items_all)
    promedio_cal = total_cal / total_loncheras if total_loncheras else 0
    
    return {
        "id": hijo.id,
        "nombre": hijo.nombre,
        "usuario_id": hijo.usuario_id,
        "padre": {"id": padre.id, "nombre": padre.nombre},
        "restricciones": rest_data,
        "loncheras_recientes": lonch_data,
        "estadisticas": {
            "total_loncheras": total_loncheras or 0,
            "promedio_calorias": round(promedio_cal, 2)
        }
    }

def get_lunchbox_detail_full(db: Session, lunchbox_id: int) -> dict | None:
    lonchera = db.get(Lonchera, lunchbox_id)
    if not lonchera: return None
    
    hijo = db.get(Hijo, lonchera.hijo_id)
    
    items = db.execute(
        select(
            LoncheraAlimento.alimento_id, # 0
            Alimento.nombre,             # 1
            LoncheraAlimento.cantidad,   # 2
            Alimento.kcal,               # 3
            Alimento.proteinas,          # 4
            Alimento.carbos,             # 5
            Alimento.costo               # 6
        )
        .join(Alimento, Alimento.id == LoncheraAlimento.alimento_id)
        .where(LoncheraAlimento.lonchera_id == lunchbox_id)
    ).all()
    
    items_data = [
        {
            "alimento_id": i[0],
            "nombre": i[1],
            "cantidad": i[2],
            "kcal": i[3],
            "proteinas": i[4],
            "carbos": i[5],
            "costo": i[6]
        }
        for i in items
    ]
    
    total_cal = sum(i[3] * i[2] for i in items)
    total_prot = sum(i[4] * i[2] for i in items)
    total_carb = sum(i[5] * i[2] for i in items)
    total_cost = sum(i[6] * i[2] for i in items)
    
    direccion_data = None
    if lonchera.direccion_id:
        direccion = db.get(Direccion, lonchera.direccion_id)
        if direccion:
            direccion_data = {
                "id": direccion.id,
                "etiqueta": direccion.etiqueta,
                "direccion": direccion.direccion,
                "ciudad": direccion.ciudad
            }
    
    alertas = []
    if total_cal > 500:
        alertas.append("⚠️ Esta lonchera supera las 500 calorías recomendadas")
    if total_prot < 5:
        alertas.append("⚠️ Bajo contenido proteico (menos de 5g)")
    
    rest_count = db.scalar(select(func.count()).select_from(Restriccion).where(Restriccion.hijo_id == lonchera.hijo_id))
    
    return {
        "id": lonchera.id,
        "hijo": {
            "id": hijo.id,
            "nombre": hijo.nombre,
            "restricciones_count": rest_count or 0,
            "loncheras_activas": 0
        },
        "fecha": lonchera.fecha,
        "estado": lonchera.estado,
        "items": items_data,
        "direccion": direccion_data,
        "nutricion_total": {
            "calorias": round(total_cal, 2),
            "proteinas": round(total_prot, 2),
            "carbohidratos": round(total_carb, 2),
            "costo_total": round(total_cost, 2)
        },
        "alertas": alertas
    }

def get_advanced_statistics(db: Session, hijo_id: int) -> dict:
    hijo = db.get(Hijo, hijo_id)
    if not hijo:
        raise ValueError("Hijo no encontrado")
        
    fecha_limite = datetime.utcnow().date() - timedelta(days=30)

    stmt = (
        select(
            Lonchera.fecha,
            func.sum(Alimento.kcal * LoncheraAlimento.cantidad).label('total_kcal'),
            func.sum(Alimento.proteinas * LoncheraAlimento.cantidad).label('total_proteinas'),
            func.sum(Alimento.carbos * LoncheraAlimento.cantidad).label('total_carbos'),
            func.sum(Alimento.costo * LoncheraAlimento.cantidad).label('total_costo')
        )
        .join(LoncheraAlimento, Alimento.id == LoncheraAlimento.alimento_id)
        .join(Lonchera, Lonchera.id == LoncheraAlimento.lonchera_id)
        .where(
            Lonchera.hijo_id == hijo_id,
            Lonchera.estado.in_(['Confirmada', 'Archivada']),
            Lonchera.fecha >= fecha_limite
        )
        .group_by(Lonchera.fecha)
        .order_by(Lonchera.fecha.asc())
    )
    
    consumo_diario_result = db.execute(stmt).all()
    
    consumo_diario = [
        {
            "fecha": row.fecha.isoformat(),
            "calorias": round(row.total_kcal or 0, 1),
            "proteinas": round(row.total_proteinas or 0, 1),
            "carbos": round(row.total_carbos or 0, 1),
            "costo": round(row.total_costo or 0, 2)
        }
        for row in consumo_diario_result
    ]

    total_proteinas = sum(item['proteinas'] for item in consumo_diario)
    total_carbos = sum(item['carbos'] for item in consumo_diario)
    
    total_macros = total_proteinas + total_carbos
    
    macro_porcentajes = {
        "proteinas_pct": round((total_proteinas / total_macros) * 100, 1) if total_macros > 0 else 0,
        "carbos_pct": round((total_carbos / total_macros) * 100, 1) if total_macros > 0 else 0,
    }

    return {
        "hijo_id": hijo_id,
        "hijo_nombre": hijo.nombre,
        "consumo_diario": consumo_diario,
        "macro_porcentajes": macro_porcentajes
    }
