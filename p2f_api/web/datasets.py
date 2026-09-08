# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import datasets
from .temp_accounts import combined_auth, api_token_annotation, api_token_annotation
from p2f_pydantic.datasets import Datasets
# from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import APIRouter, Security, Depends
from fastapi import Header, Body

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

tag_name = "Datasets"

router = APIRouter(prefix="/datasets", tags=[tag_name])

tag_metadata = {"name": tag_name,
                "description": 
                """Datasets are one of the core data types within the Past 2 Future API and Portal. 

Datasets are any individual data collections or groups of data collections that are published.
Datasets can also be nested, consider a dataset published on Pangaea that has multiple sub-files. 
The parent dataset object would be the collection of the data files held within. 
Sub datasets are the individual files within that collection. 
In addition to individual files, worksheets within an Excel spreadsheet can be a subdataset. 

Datasets have the following attributes:

* dataset_id : A unqiue identifier of the dataset using the UUID standard. This is set by the API server, do not set this yourself. 
* doi : The url or doi.org link for the dataset. This must be identical across all sub datasets
* title : The title of the dataset or collection of datasets
* sub_dataset_name : A unique name for a sub dataset, such as the filename or worksheet name. 
* publication_date : The date the publication was made available
* is_new_p2f : A boolean for if a dataset is newly created by the Past 2 Future project (True) or a dataset that is being re-used from previous science (False)
* is_sub_dataset : A boolean for if the dataset is part of a larger dataset collection

The dataset_id is one of the most re-used identifiers across the whole API. 
The dataset_id field is used to relate the following objects back to a dataset:

* HARM Data Records
* Keywords
* Git Repositories
* HARM Time Slices
* HARM Age Models
* HARM Data Types
* HARM References
* HARM Locations
* HARM Species"""}

# List
@router.get("/", operation_id="dataset-list")
def list_datasets(
    auth: api_token_annotation,
    is_new_p2f: Optional[bool] = None,
    is_sub_dataset: Optional[bool] = None,
    doi: Optional[str] = None,
) -> List[Datasets]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    # logger.debug(f"Parameters: {is_new_p2f}, {is_sub_dataset}, {doi}")
    return datasets.list_datasets(
        is_new_p2f=is_new_p2f, is_sub_dataset=is_sub_dataset, doi=doi
    )


# Get Single
@router.get("/{dataset_id}", operation_id="dataset-get")
def get_dataset(auth: api_token_annotation,
                dataset_id: uuid.UUID) -> Datasets:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return datasets.get_dataset(dataset_id=dataset_id)


# Create
@router.post("/", operation_id="dataset-create")
def create_dataset(auth: api_token_annotation,
                   dataset: Datasets) -> Datasets:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return datasets.create_dataset(dataset)


# Update
@router.put("/", include_in_schema=False, operation_id="dataset-update")
def update_dataset(auth: api_token_annotation,
                   dataset_updates: Datasets) -> Datasets:
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return datasets.update_dataset(dataset_updates)


# Delete
@router.delete("/{dataset_id}", include_in_schema=False, operation_id="dataset-delete")
def delete_dataset(auth: api_token_annotation,
                   dataset_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    if type(dataset_id) == str:
        return datasets.delete_dataset(dataset_id)
