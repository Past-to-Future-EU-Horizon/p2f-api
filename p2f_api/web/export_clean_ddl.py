###### THIS IS A DEBUG FEATURE, DO NOT INCLUDE IN REAL USE
from p2f_api.apilogs import logger
from service.export_clean_ddl import get_clean_ddl
# Third Party Libraries
from fastapi import Body, APIRouter, Request
from fastapi.responses import PlainTextResponse
# Batteries included libraries

router = APIRouter(prefix="/ddl")

@router.get("/")
def web_get_clean_ddl(request: Request) -> str:
    logger.debug(f"RECEIVED DDL REQUEST FROM {request.client.host}")
    # logger.debug(f"{request.headers.keys()}")
    # logger.debug(dir(request.headers))
    return PlainTextResponse(get_clean_ddl())