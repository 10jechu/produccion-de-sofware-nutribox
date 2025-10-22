from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Restriccions")
def listar_restriccions():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Restriccions")
def crear_restriccions(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Restriccions creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Restriccions")
def obtener_restriccions(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Restriccions no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Restriccions")
def eliminar_restriccions(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Restriccions eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Restriccions no encontrado")
