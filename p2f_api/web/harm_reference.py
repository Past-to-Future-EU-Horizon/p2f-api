# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_reference
from p2f_pydantic.harm_reference import harm_reference as Harm_reference
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/harm-reference")

# List 
@router.get("/")
def list_references() -> List[Harm_reference]:
    logger.debug(f"{fa.web}{fa.list} {__name__}")
    return(harm_reference.list_references())

# Get Single
@router.get("/{reference_id}")
def get_reference(doi: Optional[str]=None, 
                  reference_id: Optional[uuid.UUID]=None) -> Harm_reference:
    logger.debug(f"{fa.web}{fa.get} {__name__}")
    return harm_reference.get_reference(doi=doi, reference_id=reference_id)

# Create
@router.post("/")
def create_reference(new_reference: Harm_reference) -> Harm_reference:
    logger.debug(f"{fa.web}{fa.create} {__name__}")
    return harm_reference.create_reference(new_reference=new_reference)

# Delete
@router.delete("/{reference_id}")
def delete_reference(reference_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__}")
    return harm_reference.delete_reference(reference_id=reference_id)

# Assign
def assign_reference(reference_id: uuid.UUID, 
                     record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.assign} {__name__}")
    return harm_reference.assign_reference(reference_id=reference_id,
                                           record_hash=record_hash)

# Remove
def remove_reference(reference_id: uuid.UUID, 
                     record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.remove} {__name__}")
    return harm_reference.remove_reference(reference_id=reference_id,
                                           record_hash=record_hash)