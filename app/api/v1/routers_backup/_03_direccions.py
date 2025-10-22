from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Direccions")
def listar_direccions():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Direccions")
def crear_direccions(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Direccions creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Direccions")
def obtener_direccions(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Direccions no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Direccions")
def eliminar_direccions(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Direccions eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Direccions no encontrado")
