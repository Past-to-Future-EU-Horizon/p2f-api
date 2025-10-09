# Local libraries
from ..apilogs import logger
from ..service import datasets
from p2f_pydantic.datasets import Datasets
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/datasets")

# List 
@router.get("/")
def list_datasets(
    is_new_p2f: Optional[bool]=None,
    is_sub_dataset: Optional[bool]=None
    ) -> List[Datasets]:
    logger.debug("🕸️📃 web/datasets.py list_datasets()")
    return datasets.list_datasets()

# Get Single
@router.get("/{dataset_id}")
def get_dataset(dataset_id) -> Datasets:
    logger.debug("🕸️🔎 web/datasets.py get_dataset()")
    return datasets.get_dataset(dataset_id=dataset_id)

# Create
@router.post("/")
def create_dataset(dataset: Datasets) -> Datasets:
    logger.debug("🕸️🆕 web/datasets.py create_dataset()")
    return datasets.create_dataset(dataset)

# Update 
@router.put("/")
def update_dataset(dataset_updates: Datasets) -> Datasets:
    logger.debug("🕸️✏️ web/datasets.py update_dataset()")
    return datasets.update_dataset(dataset_updates)

# Delete
@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: str) -> None:
    logger.debug("🕸️🗑️ web/datasets.py delete_dataset()")
    if type(dataset_id) == str:
        return datasets.delete_dataset(dataset_id)
    elif type(dataset_id) == Datasets:
        return datasets.delete_dataset(dataset_id.dataset_identifier)