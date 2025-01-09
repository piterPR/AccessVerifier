from fastapi import FastAPI
from app.core.scheduler import DataScheduler
from app.api.routers.verify import verify_router
from app.api.routers.healthcheck import health_router


data_scheduler = DataScheduler()

app = FastAPI(
    title="AccessVerifier",
    description="AccessVerifier for verifying and allowing IP addresses from AWS services",
    version="1.0.0",
)

app.include_router(verify_router, prefix="/verify", tags=["verify"])
app.include_router(health_router, prefix="/health", tags=["health"])
