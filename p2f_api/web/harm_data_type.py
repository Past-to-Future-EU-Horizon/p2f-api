from ..apilogs import logger
from ..service import harm_data_types
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List

router = APIRouter(prefix="/harm-data-types")

router.get("/")
def list_harm_data_types(
        measure: Optional[str]=None, 
        unit_of_measure: Optional[str]=None,
        method: Optional[str]=None
    ) -> List[Harm_data_type]:
    return harm_data_types.list_harm_data_types(measure=measure,
                                                unit_of_measure=unit_of_measure,
                                                method=method)

router.get("/{data_type_id}")
def get_harm_data_type(
        data_type_id: int
    ) -> Harm_data_type:
    return harm_data_types.get_harm_data_type(pk_harm_data_type=data_type_id)

router.post("/")
def insert_harm_data_type(
        new_harm_data_type: Harm_data_type
    ) -> Harm_data_type:
    return harm_data_types.create_harm_data_type(new_harm_data_type=new_harm_data_type)

router.put("/")
def update_harm_data_type(
        update_harm_data_type: Harm_data_type
    ) -> Harm_data_type:
    return harm_data_types.update_harm_data_type(update_harm_data_type=update_harm_data_type)

router.delete("/{data_type_id}")
def delete_harm_data_record(
        data_type_id: int
    ) -> None:
    return harm_data_types.delete_harm_data_type(pk_harm_data_type=data_type_id)