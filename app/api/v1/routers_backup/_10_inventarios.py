from fastapi import APIRouter, HTTPException

router = APIRouter()

fake_db = []

# --- LISTAR ---
@router.get("/", summary="Listar Inventarios")
def listar_inventarios():
    return fake_db

# --- CREAR ---
@router.post("/", summary="Crear Inventarios")
def crear_inventarios(item: dict):
    item["id"] = len(fake_db) + 1
    fake_db.append(item)
    return {"message": "Inventarios creado correctamente", "data": item}

# --- OBTENER POR ID ---
@router.get("/{id}", summary="Obtener Inventarios")
def obtener_inventarios(id: int):
    for item in fake_db:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Inventarios no encontrado")

# --- ELIMINAR POR ID ---
@router.delete("/{id}", summary="Eliminar Inventarios")
def eliminar_inventarios(id: int):
    for i, item in enumerate(fake_db):
        if item["id"] == id:
            fake_db.pop(i)
            return {"message": "Inventarios eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Inventarios no encontrado")
