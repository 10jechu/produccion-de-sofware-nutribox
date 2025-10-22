from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Init__")
def listar_init__():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Init__")
def crear_init__(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Init__ creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Init__")
def obtener_init__(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Init__ no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Init__")
def eliminar_init__(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Init__ eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Init__ no encontrado")
