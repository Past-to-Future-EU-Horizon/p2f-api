# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import keywords
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.keywords import Keywords, KeywordDictionary
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/keywords")

# List
@router.get("/dataset/{dataset_id}")
def list_keywords(auth: api_token_annotation,
                  dataset_id: Optional[str]=None,
                  contains: Optional[str]=None) -> List[Keywords]:
    return keywords.list_keywords(dataset_id=dataset_id, 
                                  contains=contains)

@router.get("/dictionary")
def list_dictionary_keywords(taxon: str) -> List[Keywords]:
    pass

# Create
@router.post("/dataset/{dataset_id}")
def add_keyword(auth: api_token_annotation,
                dataset_id: uuid.UUID, 
                keyword: str, 
                taxon: Optional[str]=None) -> List[Keywords]:
    return keywords.add_keyword(dataset_id=dataset_id,
                                keyword=keyword,
                                taxon=taxon)

# Delete
@router.delete("/dataset/{dataset_id}")
def delete_keyword(auth: api_token_annotation,
                   dataset_id: uuid.UUID, 
                   keyword: str, 
                   taxon: Optional[str]=None) -> List[Keywords]:
    return keywords.delete_keyword(dataset_id=dataset_id,
                                   keyword=keyword, 
                                   taxon=taxon)