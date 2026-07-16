from fastapi import APIRouter
from app.api.endpoints import inference, simulation, metrics

api_router = APIRouter()

api_router.include_router(inference.router, prefix="/inference", tags=["inference"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
