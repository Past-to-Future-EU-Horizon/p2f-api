# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import harm_numerical
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_data_numerical import HARM_Int, HARM_Int_Confidence
from p2f_pydantic.harm_data_numerical import HARM_Float, HARM_Float_Confidence
from p2f_pydantic.harm_data_numerical import Insert_HARM_Numerical, Return_HARM_Numerical
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, Annotated, Union, Literal
from inspect import stack

router = APIRouter(prefix="/harm-numerical")

Harm_numerical_union = Union[
    HARM_Float_Confidence, HARM_Float, HARM_Int, HARM_Int_Confidence
]


# List
@router.get("/")
def list_harm_numerical(
    auth: api_token_annotation,
    record_hash: Optional[str] = None,
    numeric_type: Optional[
        Literal["float_confidence", "float", "int_confidence", "int"]
    ] = None,
    data_type: Optional[uuid.UUID] = None,
    dataset_id: Optional[uuid.UUID] = None,
) -> Return_HARM_Numerical:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    logger.debug(f"Received params: {locals()}")
    return harm_numerical.list_numerics(
        record_hash=record_hash,
        numeric_type=numeric_type,
        data_type=data_type,
        dataset_id=dataset_id,
    )


# Get Single
@router.get("/{numeric_id}")
def get_harm_numerical(auth: api_token_annotation,
                       numeric_id: uuid.UUID) -> Harm_numerical_union:
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_numerical.get_numeric(numeric_id=numeric_id)


# Create
@router.post("/")
def create_harm_numerical(auth: api_token_annotation,
                          new_numeric: Insert_HARM_Numerical) -> Harm_numerical_union:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_numerical.create_numeric(new_numeric=new_numeric)


# Update
@router.put("/", include_in_schema=False)
def update_harm_numerical(
    auth: api_token_annotation,
    numerical_updates: Harm_numerical_union,
) -> Harm_numerical_union:
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return harm_numerical.update_numeric(numerical_updates)


# Delete
@router.delete("/{numeric_id}", include_in_schema=False)
def delete_harm_numerical(auth: api_token_annotation,
                          numeric_id: uuid.UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_numerical.delete_numeric(numeric_id=numeric_id)
