from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Excepcions")
def listar_excepcions():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Excepcions")
def crear_excepcions(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Excepcions creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Excepcions")
def obtener_excepcions(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Excepcions no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Excepcions")
def eliminar_excepcions(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Excepcions eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Excepcions no encontrado")
