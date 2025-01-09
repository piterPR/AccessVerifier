import logging
from fastapi import APIRouter
from fastapi.responses import JSONResponse


logger = logging.getLogger("health_router")
health_router = APIRouter()

@health_router.get("", response_class=JSONResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint to verify if the application is running.
    Returns a plain text "OK" with a 200 status code.
    """
    return JSONResponse(content="Service is healthy", status_code=200)
