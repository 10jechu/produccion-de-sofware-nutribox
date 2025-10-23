from fastapi import APIRouter

api_router = APIRouter()

# Importar routers existentes
try:
    from app.api.v1.routers import auth
    api_router.include_router(auth.router, tags=["auth"])
except ImportError as e:
    print(f"Warning: No se pudo importar auth - {e}")

try:
    from app.api.v1.routers._01_usuarios import router as usuarios_router
    api_router.include_router(usuarios_router, tags=["usuarios"])
except ImportError:
    pass

try:
    from app.api.v1.routers._04_hijos import router as hijos_router
    api_router.include_router(hijos_router, tags=["hijos"])
except ImportError:
    pass

try:
    from app.api.v1.routers._05_loncheras import router as loncheras_router
    api_router.include_router(loncheras_router, tags=["loncheras"])
except ImportError:
    pass

try:
    from app.api.v1.routers._06_alimentos import router as alimentos_router
    api_router.include_router(alimentos_router, tags=["alimentos"])
except ImportError:
    pass

try:
    from app.api.v1.routers._03_direccions import router as direcciones_router
    api_router.include_router(direcciones_router, tags=["direcciones"])
except ImportError:
    pass

try:
    from app.api.v1.routers._08_restriccions import router as restricciones_router
    api_router.include_router(restricciones_router, tags=["restricciones"])
except ImportError:
    pass
