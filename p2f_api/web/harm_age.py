from p2f_api.apilogs import logger, fa
from ..service import harm_age
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.harm_age import HARM_Rec_Age

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-data-age", tags=["HARM Age"])

@router.get("/", operation_id="age-list")
def list_harm_ages(
    auth: api_token_annotation,
    recent_year_search: Optional[int] = None,
    older_year_search: Optional[int] = None
) -> List[HARM_Rec_Age]:
    """List the records within an age range. 

    Args:
        auth (api_token_annotation): _description_
        recent_year_search (Optional[int], optional): The higher year limit. Defaults to None.
        older_year_search (Optional[int], optional): The lower year limit. Defaults to None.

    Returns:
        List[HARM_Rec_Age]: List of ages with the records
    """
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_age.list_harm_ages(
        recent_year_search=recent_year_search,
        older_year_search=older_year_search
    )


@router.get("/{record_hash}", operation_id="age-get")
def get_harm_age(auth: api_token_annotation,
                 record_hash: Optional[str] = None) -> HARM_Rec_Age:
    """Get an individual HARM age for a record hash

    Args:
        auth (api_token_annotation): _description_
        record_hash (Optional[str], optional): Record hash calculated for a row within a dataset. Defaults to None.

    Returns:
        HARM_Rec_Age: The p2f-pydantic HARM_Rec_Age as returned by the API
    """
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_age.get_harm_age(record_hash=record_hash)


@router.post("/", operation_id="age-create")
def create_new_HARM_Data_Age(auth: api_token_annotation,
                             new_harm_age: HARM_Rec_Age) -> HARM_Rec_Age:
    """Create a new p2f-pydantic HARM_Rec_Age object to associate with a record.

    Args:
        auth (api_token_annotation): _description_
        new_harm_age (HARM_Rec_Age): New p2f-pydantic HARM_Rec_Age object

    Returns:
        HARM_Rec_Age: Processed p2f-pydantic HARM_Rec_Age object
    """
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_age.create_new_harm_data_age(new_harm_age=new_harm_age)


@router.put("/", include_in_schema=False, operation_id="age-update")
def update_age(auth: api_token_annotation,
               update_harm_age: HARM_Rec_Age) -> HARM_Rec_Age:
    """Update the age object of a record

    Args:
        auth (api_token_annotation): _description_
        update_harm_age (HARM_Rec_Age): Updated p2f-pydantic HARM_Rec_Age object

    Returns:
        HARM_Rec_Age: Processed updated p2f-pydantic HARM_Rec_Age object
    """ 
    logger.debug(f"{fa.web}{fa.update} {__name__} {stack()[0][3]}()")
    return harm_age.update_age(update_harm_age=update_harm_age)


@router.delete("/{record_hash}", include_in_schema=False, operation_id="age-delete")
def delete_age(auth: api_token_annotation,
               record_hash: str) -> None:
    """Delete a p2f-pydantic HARM_Rec_Age from a record by its record_hash. 

    Args:
        auth (api_token_annotation): _description_
        record_hash (str): Record hash calculate for a row in a dataset
    """
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_age.delete_age(record_hash=record_hash)
