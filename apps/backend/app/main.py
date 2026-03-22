from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI(title="BFS Life API")

app.include_router(api_router, prefix="/api/v1")