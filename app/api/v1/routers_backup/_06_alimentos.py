from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Alimentos")
def listar_alimentos():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Alimentos")
def crear_alimentos(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Alimentos creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Alimentos")
def obtener_alimentos(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Alimentos no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Alimentos")
def eliminar_alimentos(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Alimentos eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Alimentos no encontrado")
