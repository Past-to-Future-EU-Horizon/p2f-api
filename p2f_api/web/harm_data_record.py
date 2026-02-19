# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_data_record
from p2f_pydantic.harm_data_record import harm_data_record as Harm_data_record

# Third Party Libraries
from fastapi import Body, APIRouter, Request

# Batteries included libraries
import uuid
from typing import Optional, List
from inspect import stack

router = APIRouter(prefix="/harm-data-records")


# List
@router.get("/")
def list_harm_data_records(
    dataset: Optional[str] = None,
    # data_type: Optional[int]=None, ### Disabled for now, see note in service
) -> List[Harm_data_record]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_data_record.list_harm_data_record(dataset=dataset)


# Get Single
@router.get("/{record_hash}")
def get_harm_data_record(record_hash: str) -> Harm_data_record:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_data_record.get_harm_data_record(record_hash=record_hash)


# Create
@router.post("/")
def create_dataset(new_data_record: Harm_data_record) -> Harm_data_record:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_data_record.create_harm_data_record(new_data_record)


# Update
## Discussion, should this method exist?
##   If the hash changes we should delete the old hash and re-enter
##   the row data as new records in their respective tables.
# @router.put("/{record_hash}")
# def update_dataset(record_hash: str,
#                    update_data_record: Harm_data_record) -> Harm_data_record:
#     logger.debug("🕸️✏️ web/harm_data_record.py update_harm_data_record()")
#     return harm_data_record.update_harm_data_record(update_data_record)


# Delete
@router.delete("/{record_hash}")
def delete_dataset(record_hash: str) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    if type(record_hash) == str:
        return harm_data_record.delete_harm_data_record(record_hash)
