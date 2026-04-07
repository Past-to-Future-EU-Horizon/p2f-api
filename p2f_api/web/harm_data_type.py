from p2f_api.apilogs import logger, fa
from ..service import harm_data_types
from .temp_accounts import combined_auth
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-data-types")


@router.get("/")
def list_harm_data_types(
    auth: Annotated[Temp_Account, Depends(combined_auth)],
    measure: Optional[str] = None,
    unit_of_measure: Optional[str] = None,
    method: Optional[str] = None,
    dataset_id: Optional[uuid.UUID] = None,
) -> List[Harm_data_type]:
    logger.debug(
        f"{fa.web}{fa.list} {__name__} {stack()[0][3]}({measure}, {unit_of_measure}, {method}, {dataset_id})"
    )
    return harm_data_types.list_harm_data_types(
        measure=measure,
        unit_of_measure=unit_of_measure,
        method=method,
        dataset_id=dataset_id,
    )


@router.get("/{datatype_id}")
def get_harm_data_type(
    auth: Annotated[Temp_Account, Depends(combined_auth)],
    datatype_id: uuid.UUID) -> Harm_data_type:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}({datatype_id})")
    return harm_data_types.get_harm_data_type(datatype_id=datatype_id)


@router.post("/")
def insert_harm_data_type(auth: Annotated[Temp_Account, Depends(combined_auth)],
                          new_harm_data_type: Harm_data_type) -> Harm_data_type:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_data_types.create_harm_data_type(new_harm_data_type=new_harm_data_type)


# @router.put("/")
# def update_harm_data_type(
#         update_harm_data_type: Harm_data_type
#     ) -> Harm_data_type:
#     logger.debug(f"🕸️✏️ {__name__}/update_harm_data_type()")
#     return harm_data_types.update_harm_data_type(update_harm_data_type=update_harm_data_type)


@router.delete("/{datatype_id}")
def delete_harm_data_record(auth: Annotated[Temp_Account, Depends(combined_auth)],
                            datatype_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}({datatype_id})")
    return harm_data_types.delete_harm_data_type(datatype_id=datatype_id)
