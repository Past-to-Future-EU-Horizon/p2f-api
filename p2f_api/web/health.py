# Local libraries
from p2f_api.apilogs import logger, fa

# Third Party Libraries
from fastapi import Body, APIRouter, Request
from fastapi.responses import JSONResponse

# Batteries included libraries
from inspect import stack

router = APIRouter(prefix="/health-check", include_in_schema=False)

@router.get("/")
def get_health():
    return JSONResponse(content={"status": "OK"})

# Future function with DB status
# @router.get("/v")
# def get_verbose_health():
#     return verbose_health()