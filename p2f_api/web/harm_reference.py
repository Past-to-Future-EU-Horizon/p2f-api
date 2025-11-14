# Local libraries
from ..apilogs import logger
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
    return(harm_reference.list_references())

# Get Single
@router.get("/{reference_id}")
def get_reference(doi: Optional[str]=None, 
                  reference_id: Optional[str]=None) -> Harm_reference:
    return harm_reference.get_reference(doi=doi, reference_id=reference_id)

# Create
@router.post("/")
def create_reference(new_reference: Harm_reference) -> Harm_reference:
    return harm_reference.create_reference(new_reference=new_reference)

# Delete
@router.delete("/{record_hash}")

# Assign

# Remove