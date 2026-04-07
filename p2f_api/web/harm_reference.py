# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_reference
from .temp_accounts import combined_auth
from p2f_pydantic.harm_reference import HARM_Reference
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-reference")


# List
@router.get("/")
def list_references(auth: Annotated[Temp_Account, Depends(combined_auth)]) -> List[HARM_Reference]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_reference.list_references()


# Get Single
@router.get("/{reference_id}")
def get_reference(
    auth: Annotated[Temp_Account, Depends(combined_auth)],
    doi: Optional[str] = None,
    reference_id: Optional[uuid.UUID] = None
) -> HARM_Reference:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_reference.get_reference(doi=doi, reference_id=reference_id)


# Create
@router.post("/")
def create_reference(
    auth: Annotated[Temp_Account, Depends(combined_auth)],
    new_reference: HARM_Reference) -> HARM_Reference:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    logger.debug(f"• new_reference: {new_reference.model_dump(exclude_unset=True)}")
    return harm_reference.create_reference(new_reference=new_reference)


# Delete
@router.delete("/{reference_id}")
def delete_reference(auth: Annotated[Temp_Account, Depends(combined_auth)],
                     reference_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_reference.delete_reference(reference_id=reference_id)


# Assign
def assign_reference(auth: Annotated[Temp_Account, Depends(combined_auth)],
                     reference_id: uuid.UUID,
                     record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.assign} {__name__} {stack()[0][3]}()")
    return harm_reference.assign_reference(
        reference_id=reference_id,
        record_hash=record_hash
    )


# Remove
def remove_reference(auth: Annotated[Temp_Account, Depends(combined_auth)],
                     reference_id: uuid.UUID,
                     record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.remove} {__name__} {stack()[0][3]}()")
    return harm_reference.remove_reference(
        reference_id=reference_id, record_hash=record_hash
    )
