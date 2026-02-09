# Local libraries
from p2f_api.apilogs import logger, fa
from ..service.doi import get_doi
# Third Party Libraries
from fastapi import Body, APIRouter, Request
from fastapi import HTTPException
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/doi")

@router.get("/")
def get(dataset_id: Optional[uuid.UUID]=None,
        doi_prefix: Optional[str]=None, 
        doi_suffix: Optional[str]=None):
    if doi_prefix is not None:
        if doi_suffix is None:
            return HTTPException(400, "DOI Suffix and Prefix must be supplied together.")
    if doi_suffix is not None:
        if doi_prefix is None:
            return HTTPException(400, "DOI Suffix and Prefix must be supplied together.")
    return get_doi(dataset_id, doi_prefix, doi_suffix)