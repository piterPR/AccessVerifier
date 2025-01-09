import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.ip_checker import IPChecker

logger = logging.getLogger("verify_router")
verify_router = APIRouter()

@verify_router.post("", response_class=JSONResponse)
async def verify_access(request: Request):
    """
    Verify access to resource
    """
    body = await request.body()
    response = IPChecker.check_ip(body)

    if response is True:
        return JSONResponse(content="OK", status_code=200)

    raise HTTPException(status_code=401, detail="Unauthorized")
