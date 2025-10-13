from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.db.database import SessionLocal, Base, engine
from sqlalchemy import select, delete
from app.db.models.core_models import Usuario, Rol, Membresia, Hijo
from app.db.models.address import Direccion
from app.db.models.alimento import Alimento
from app.db.models.lunchbox import Lonchera, LoncheraAlimento

router = APIRouter()

# ---------- Seeds / Inspect ----------

@router.post("/seed", summary="Seed de datos demo (DEV)")
def seed():
    db = SessionLocal()
    try:
        rol = db.query(Rol).filter_by(nombre="UsuarioPrincipal").first() or Rol(nombre="UsuarioPrincipal")
        mem = db.query(Membresia).filter_by(tipo="Premium").first() or Membresia(tipo="Premium", max_direcciones=3)
        db.add_all([rol, mem]); db.commit()

        u = db.query(Usuario).filter_by(email="demo@nutribox.com").first()
        if not u:
            u = Usuario(nombre="Demo", email="demo@nutribox.com", hash_password="x", rol_id=rol.id, membresia_id=mem.id)
            db.add(u); db.commit(); db.refresh(u)

        h = db.query(Hijo).filter_by(usuario_id=u.id).first()
        if not h:
            h = Hijo(nombre="Peque", usuario_id=u.id); db.add(h); db.commit(); db.refresh(h)

        d = db.query(Direccion).filter_by(usuario_id=u.id).first()
        if not d:
            d = Direccion(usuario_id=u.id, etiqueta="Casa", direccion="Calle 123 #45-67", barrio="Chapinero", ciudad="Bogotá")
            db.add(d); db.commit(); db.refresh(d)

        a = db.query(Alimento).filter_by(nombre="Manzana").first()
        if not a:
            a = Alimento(nombre="Manzana", kcal=52, proteinas=0.3, carbos=14)
            db.add(a); db.commit(); db.refresh(a)

        res = {"usuario_id": u.id, "hijo_id": h.id, "direccion_id": d.id, "alimento_id": a.id}
        return {"ok": True, "ids": res}
    finally:
        db.close()

@router.get("/inspect", summary="Resumen de datos (DEV)")
def inspect():
    db = SessionLocal()
    try:
        users = [{"id": u.id, "email": u.email} for u in db.query(Usuario).all()]
        hijos = [{"id": h.id, "nombre": h.nombre, "usuario_id": h.usuario_id} for h in db.query(Hijo).all()]
        dirs = [{"id": d.id, "usuario_id": d.usuario_id, "etiqueta": d.etiqueta} for d in db.query(Direccion).all()]
        foods = [{"id": a.id, "nombre": a.nombre} for a in db.query(Alimento).all()]
        lunch = [{"id": l.id, "hijo_id": l.hijo_id, "fecha": str(l.fecha)} for l in db.query(Lonchera).all()]
        return {"usuarios": users, "hijos": hijos, "direcciones": dirs, "alimentos": foods, "loncheras": lunch}
    finally:
        db.close()

# ---------- Crear hijo por BODY JSON (DEV) ----------

class DevChildCreate(BaseModel):
    usuario_id: int
    nombre: str = "Peque 2"

@router.post("/children", summary="Crear Hijo para un usuario (DEV)")
def create_child(payload: DevChildCreate):
    db = SessionLocal()
    try:
        u = db.get(Usuario, payload.usuario_id)
        if not u:
            raise HTTPException(status_code=404, detail="Usuario no existe")
        h = Hijo(nombre=payload.nombre, usuario_id=payload.usuario_id)
        db.add(h); db.commit(); db.refresh(h)
        return {"ok": True, "hijo": {"id": h.id, "nombre": h.nombre, "usuario_id": h.usuario_id}}
    finally:
        db.close()

@router.post("/addresses", summary="Crear Dirección para un usuario (DEV)")
def create_address(usuario_id: int, etiqueta: str = "Colegio", direccion: str = "Carrera 9 #99-99", barrio: str = "Usaquén", ciudad: str = "Bogotá"):
    db = SessionLocal()
    try:
        u = db.get(Usuario, usuario_id)
        if not u: raise HTTPException(404, "Usuario no existe")
        d = Direccion(usuario_id=usuario_id, etiqueta=etiqueta, direccion=direccion, barrio=barrio, ciudad=ciudad)
        db.add(d); db.commit(); db.refresh(d)
        return {"ok": True, "direccion_id": d.id}
    finally:
        db.close()

# ---------- Deletes granulares (DEV) ----------

@router.delete("/children/{child_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Hijo (y sus loncheras/items)")
def delete_child(child_id: int):
    db = SessionLocal()
    try:
        h = db.get(Hijo, child_id)
        if not h: raise HTTPException(404, "Hijo no existe")
        lns = db.scalars(select(Lonchera.id).where(Lonchera.hijo_id == child_id)).all()
        if lns:
            db.execute(delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id.in_(lns)))
            db.execute(delete(Lonchera).where(Lonchera.id.in_(lns)))
        db.delete(h); db.commit(); return
    finally:
        db.close()

@router.delete("/addresses/{address_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Dirección")
def delete_address(address_id: int):
    db = SessionLocal()
    try:
        d = db.get(Direccion, address_id)
        if not d: raise HTTPException(404, "Dirección no existe")
        db.delete(d); db.commit(); return
    finally:
        db.close()

@router.delete("/lunchboxes/{lunchbox_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Lonchera (y sus items)")
def delete_lunchbox(lunchbox_id: int):
    db = SessionLocal()
    try:
        l = db.get(Lonchera, lunchbox_id)
        if not l: raise HTTPException(404, "Lonchera no existe")
        db.execute(delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id == lunchbox_id))
        db.delete(l); db.commit(); return
    finally:
        db.close()

@router.delete("/foods/{food_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Alimento (y sus apariciones en loncheras)")
def delete_food(food_id: int):
    db = SessionLocal()
    try:
        a = db.get(Alimento, food_id)
        if not a: raise HTTPException(404, "Alimento no existe")
        db.execute(delete(LoncheraAlimento).where(LoncheraAlimento.alimento_id == food_id))
        db.delete(a); db.commit(); return
    finally:
        db.close()

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar Usuario DEMO completo (hijos, direcciones, loncheras e items)")
def delete_user(user_id: int):
    db = SessionLocal()
    try:
        u = db.get(Usuario, user_id)
        if not u: raise HTTPException(404, "Usuario no existe")
        child_ids = db.scalars(select(Hijo.id).where(Hijo.usuario_id == user_id)).all()
        if child_ids:
            ln_ids = db.scalars(select(Lonchera.id).where(Lonchera.hijo_id.in_(child_ids))).all()
            if ln_ids:
                db.execute(delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id.in_(ln_ids)))
                db.execute(delete(Lonchera).where(Lonchera.id.in_(ln_ids)))
            db.execute(delete(Hijo).where(Hijo.id.in_(child_ids)))
        db.execute(delete(Direccion).where(Direccion.usuario_id == user_id))
        db.delete(u); db.commit(); return
    finally:
        db.close()

# ---------- Limpiezas globales (DEV) ----------

@router.post("/clear", summary="Limpiar datos de negocio (items, loncheras, hijos, direcciones)")
def clear_business_data():
    db = SessionLocal()
    try:
        ln_ids = db.scalars(select(Lonchera.id)).all()
        if ln_ids:
            db.execute(delete(LoncheraAlimento).where(LoncheraAlimento.lonchera_id.in_(ln_ids)))
            db.execute(delete(Lonchera).where(Lonchera.id.in_(ln_ids)))
        db.execute(delete(Hijo))
        db.execute(delete(Direccion))
        db.commit()
        return {"ok": True}
    finally:
        db.close()

@router.post("/reset-db", summary="Recrear BD desde cero (PELIGRO: borra todo)")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"ok": True, "msg": "Base de datos recreada"}
