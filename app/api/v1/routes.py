from fastapi import APIRouter
import importlib, pkgutil
import app.api.v1.routers as routers_pkg

api_router = APIRouter()

# Incluye solo módulos que empiezan por "_" y exponen "router"
for _, modname, ispkg in pkgutil.iter_modules(routers_pkg.__path__):
    if not modname.startswith("_"):
        continue
    module = importlib.import_module(f"app.api.v1.routers.{modname}")
    router = getattr(module, "router", None)
    if router is not None:
        api_router.include_router(router)
