# Local libraries
from p2f_api.apilogs import logger, fa

# Third Party Libraries
from fastapi import Body, APIRouter, Request
from fastapi.responses import JSONResponse

# Batteries included libraries
from inspect import stack
from pprint import pprint

router = APIRouter(prefix="/health-check", include_in_schema=False)

@router.get("/")
def get_health():
    return JSONResponse(content={"status": "OK"})

# Future function with DB status
# @router.get("/v")
# def get_verbose_health():
#     return verbose_health()

# @router.get("/2", include_in_schema=False, operation_id="healthcheck2-eclectic-boogaloo")
# def eclectic_boogaloo(request: Request) -> str:
#     pprint(request.scope["fastapi"]["effective_route_context"].operation_id)
#     return JSONResponse(content={"status": "OK"})