# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_data_record
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_data_record import HARM_Data_Record
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-data-records", tags=["HARM Data Records"])

# List
@router.get("/", operation_id="record-list")
def list_harm_data_records(
    auth: api_token_annotation,
    dataset: Optional[str] = None,
    # data_type: Optional[int]=None, ### Disabled for now, see note in service
) -> List[HARM_Data_Record]:
    """List the records within a dataset

    Args:
        auth (api_token_annotation): _description_
        dataset (Optional[str], optional): Unique identifier of the dataset. Defaults to None.

    Returns:
        List[HARM_Data_Record]: List of p2f-pydantic HARM_Data_Records from search. 
    """
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_data_record.list_harm_data_record(dataset=dataset)


# Get Single
@router.get("/{record_hash}", operation_id="record-get")
def get_harm_data_record(auth: api_token_annotation,
                         record_hash: str) -> HARM_Data_Record:
    """Get a single record hash object from the API

    Args:
        auth (api_token_annotation): _description_
        record_hash (str): The record hash of the desired record

    Returns:
        HARM_Data_Record: The p2f-pydantic HARM_Data_Record
    """
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_data_record.get_harm_data_record(record_hash=record_hash)


# Create
@router.post("/", operation_id="record-create")
def create_record(auth: api_token_annotation,
                   new_data_record: HARM_Data_Record) -> HARM_Data_Record:
    """Create a new record for a row within a dataset. Records are an individual row
        or set of data within a dataset. The P2F project uses a relational model for 
        records within a dataset so numerical and metadata can be brought together 
        in a way with a unique identifier. 

        The record hash can be created with the p2f-client-py library. The method
            for creating the hash is to create a hashing object (sha256 at time of writing), 
            add the dataset identifier to the hash, digest, add the row identifier, digest.
            The record hash is the resulting hex digestion of the hash object. 

    Args:
        auth (api_token_annotation): _description_
        new_data_record (HARM_Data_Record): New p2f-pydantic HARM_Data_Record object with dataset_id and record_hash

    Returns:
        HARM_Data_Record: New p2f-pydantic HARM_Data_Record as processed by the API
    """
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
@router.delete("/{record_hash}", include_in_schema=False, operation_id="record-delete")
def delete_dataset(auth: api_token_annotation,
                   record_hash: str) -> None:
    """Delete a record from the API by record hash

    Args:
        auth (api_token_annotation): _description_
        record_hash (str): The records hash
    """
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    if type(record_hash) == str:
        return harm_data_record.delete_harm_data_record(record_hash)
