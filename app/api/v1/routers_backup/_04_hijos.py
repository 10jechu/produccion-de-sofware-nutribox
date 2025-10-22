from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Hijos")
def listar_hijos():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Hijos")
def crear_hijos(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Hijos creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Hijos")
def obtener_hijos(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Hijos no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Hijos")
def eliminar_hijos(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Hijos eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Hijos no encontrado")
