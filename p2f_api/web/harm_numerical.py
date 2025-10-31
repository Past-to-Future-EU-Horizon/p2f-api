# Local libraries
from ..apilogs import logger
from ..service import harm_numerical
from p2f_pydantic.harm_data_numerical import harmonized_int_confidence as Harmonized_int_confidence
from p2f_pydantic.harm_data_numerical import harmonized_float_confidence as Harmonized_float_confidence
from p2f_pydantic.harm_data_numerical import harmonized_int as Harmonized_int
from p2f_pydantic.harm_data_numerical import harmonized_float as Harmonized_float
from p2f_pydantic.harm_data_numerical import insert_harm_numerical as Insert_harm_numerical
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
import uuid
from typing import Optional, List, Union, Literal

router = APIRouter(prefix="/harm-numerical")

Harm_numerical_union = Union[Harmonized_float_confidence, 
                             Harmonized_float,
                             Harmonized_int_confidence,
                             Harmonized_int]

# List 
@router.get("/")
def list_harm_numerical(
    record_hash: Optional[str]=None,
    numeric_type: Optional[Literal["float_confidence", 
                                               "float", 
                                               "int_confidence", 
                                               "int"]]=None, 
    data_type: Optional[int]=None
    ) -> List[Harm_numerical_union]:
    logger.debug("🕸️📃 web/harm_numerical.py list_harm_numerical()")
    return harm_numerical.list_numerics(record_hash=record_hash, data_type=data_type)

# Get Single
@router.get("/{numeric_id}")
def get_harm_numerical(numeric_id: uuid.UUID) -> Harm_numerical_union:
    logger.debug("🕸️🔎 web/harm_numerical.py get_harm_numerical()")
    return harm_numerical.get_numeric(numeric_id=numeric_id)

# Create
@router.post("/")
def create_harm_numerical(new_numeric: Insert_harm_numerical) -> Harm_numerical_union:
    logger.debug("🕸️🆕 web/harm_numerical.py create_harm_numerical()")
    return harm_numerical.create_numeric(new_numeric=new_numeric)

# Update 
@router.put("/")
def update_harm_numerical(numerical_updates: Harm_numerical_union) -> Harm_numerical_union:
    logger.debug("🕸️✏️ web/harm_numerical.py update_harm_numerical()")
    return harm_numerical.update_numeric(numerical_updates)

# Delete
@router.delete("/{numeric_id}")
def delete_harm_numerical(numeric_id: uuid.UUID) -> None:
    logger.debug("🕸️🗑️ web/harm_numerical.py delete_harm_numerical()")
    return harm_numerical.delete_numeric(numeric_id=numeric_id)