from fastapi import FastAPI
from app.core.scheduler import DataScheduler
from app.api.routers.verify import verify_router
from app.api.routers.healthcheck import health_router
from app.core.config import BASE_URL, SCHEDULER_INTERVAL_HOURS, DATA_PATH


data_scheduler = DataScheduler(base_url=BASE_URL, data_path=DATA_PATH)
data_scheduler.start(interval=SCHEDULER_INTERVAL_HOURS)

app = FastAPI(
    title="AccessVerifier",
    description="AccessVerifier for verifying and allowing IP addresses from AWS services",
    version="1.0.0",
)

app.include_router(verify_router, prefix="/verify", tags=["verify"])
app.include_router(health_router, prefix="/health", tags=["health"])
