from fastapi import APIRouter

from app.api.v1.routes import categories, dashboard, health, items

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(categories.router)
api_router.include_router(items.router)
api_router.include_router(dashboard.router)
