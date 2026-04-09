from fastapi import APIRouter

from app.api.v1.routes import auth, categories, dashboard, health, items, settings

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(categories.router)
api_router.include_router(items.router)
api_router.include_router(dashboard.router)
api_router.include_router(settings.router)
