from fastapi import APIRouter
from app.api.v1.routes import health, settings, categories

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(settings.router)
api_router.include_router(categories.router)
