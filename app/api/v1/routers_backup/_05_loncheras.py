from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Loncheras")
def listar_loncheras():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Loncheras")
def crear_loncheras(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Loncheras creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Loncheras")
def obtener_loncheras(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Loncheras no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Loncheras")
def eliminar_loncheras(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Loncheras eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Loncheras no encontrado")
