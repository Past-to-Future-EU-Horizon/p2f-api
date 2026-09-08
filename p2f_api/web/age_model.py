# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import age_model
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.age_model import Age_Model
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/age-models", tags=["Age Model"])

# List

@router.get("/", operation_id="agemodel-list")
def list_age_models(auth: api_token_annotation,) -> List[Age_Model]:
    """List the available age models on the API. 

    Args:
        auth (api_token_annotation): email address and token

    Returns:
        List[Age_Model]: A list of all age models.
    """
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return age_model.list_age_models()

# Get
@router.get("/{age_model_id}", operation_id="agemodel-get")
def get_age_model(auth: api_token_annotation,
                  age_model_id: Optional[uuid.UUID]=None) -> Age_Model:
    """Get a single age model from the API

    Args:
        auth (api_token_annotation): email address and token
        age_model_id (Optional[uuid.UUID], optional): Unique age model identifier. Defaults to None.

    Returns:
        Age_Model: A single age model
    """
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return age_model.get_age_model(age_model_id=age_model_id)

# Create
@router.post("/", operation_id="agemodel-create")
def create_age_model(auth: api_token_annotation,
                     new_age_model: Age_Model) -> Age_Model:
    """Create a new age model

    Args:
        auth (api_token_annotation): _description_
        new_age_model (Age_Model): age model to be created from the p2f-pydantic library

    Returns:
        Age_Model: The single new age model resulting as it was ingested into the API
    """
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return age_model.create_age_model(new_age_model=new_age_model)

# Delete
@router.delete("/{age_model_id}", operation_id="agemodel-delete")
def delete_age_model(auth: api_token_annotation,
                     age_model_id: uuid.UUID) -> None:
    """Delete a specific age model from the API. 

    Args:
        auth (api_token_annotation): _description_
        age_model_id (uuid.UUID): The unique identifier of the age model
    """
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return age_model.delete_age_model(age_model_id=age_model_id)

# Assign
@router.post("/assign-dataset", operation_id="agemodel_dataset-assign")
def assign_age_model_to_dataset(auth: api_token_annotation,
                                age_model_id: uuid.UUID, 
                                dataset_id: uuid.UUID) -> None:
    """Assign an age model to a dataset

    Args:
        auth (api_token_annotation): _description_
        age_model_id (uuid.UUID): The unique identifier of the age model
        dataset_id (uuid.UUID): The unique identifier of the dataset
    """
    logger.debug(f"{fa.web}{fa.assign} {__name__} {stack()[0][3]}()")
    return age_model.assign_age_model_to_dataset(age_model_id=age_model_id, 
                                                 dataset_id=dataset_id)
    
@router.post("/assign-record", operation_id="agemodel_recordhash-assign")
def assign_age_model_to_record(auth: api_token_annotation,
                               age_model_id: uuid.UUID, 
                               record_hash: str) -> None:
    """Assign an age model to a specific record within a dataset. 

    Args:
        auth (api_token_annotation): _description_
        age_model_id (uuid.UUID): The unique identifier of the age model
        record_hash (str): The record hash calculated for the row in the dataset
    """
    logger.debug(f"{fa.web}{fa.assign} {__name__} {stack()[0][3]}()")
    return age_model.assign_age_model_to_record(age_model_id=age_model_id,
                                                record_hash=record_hash)

# Remove
@router.delete("/remove-dataset", operation_id="agemodel_dataset-remove")
def remove_age_model_to_dataset(auth: api_token_annotation,
                                age_model_id: uuid.UUID, 
                                dataset_id: uuid.UUID) -> None:
    """Remove the association of an age model from a dataset

    Args:
        auth (api_token_annotation): _description_
        age_model_id (uuid.UUID): Unique identifier of an age model
        dataset_id (uuid.UUID): Unique identifier of a dataset
    """
    logger.debug(f"{fa.web}{fa.remove} {__name__} {stack()[0][3]}()")
    return age_model.remove_age_model_to_dataset(age_model_id=age_model_id,
                                                 dataset_id=dataset_id)

@router.delete("/remove-record", operation_id="agemodel_recordhash-remove")
def remove_age_model_to_record(auth: api_token_annotation,
                               age_model_id: uuid.UUID, 
                               record_hash: str) -> None:
    """Remove the association of an age model from a record. 

    Args:
        auth (api_token_annotation): _description_
        age_model_id (uuid.UUID): Unique identifier of an age model
        record_hash (str): The record hash calculated for the row in the dataset
    """
    logger.debug(f"{fa.web}{fa.remove} {__name__} {stack()[0][3]}()")
    return age_model.remove_age_model_to_record(age_model_id=age_model_id,
                                                record_hash=record_hash)