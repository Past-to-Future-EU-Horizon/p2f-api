# Local libraries
from p2f_api.apilogs import logger, fa
from ..service import keywords
from .temp_accounts import combined_auth, api_token_annotation
from p2f_pydantic.keywords import Keywords, TaxonomicDict
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
import uuid
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/keywords")

# List
@router.get("/")
def list_keywords(auth: api_token_annotation,
                  dataset_id: Optional[str]=None,
                  contains: Optional[str]=None) -> List[Keywords]:
    return keywords.list_keywords(dataset_id=dataset_id, 
                                  contains=contains)

@router.get("/dictionary")
def list_taxonomic_dictionary(auth: api_token_annotation,
                              taxonomy: Optional[str]=None,
                              contains: Optional[str]=None) -> List[TaxonomicDict]:
    return keywords.list_taxonomic_dictionary(taxonomy=taxonomy, contains=contains)

@router.get("/taxonomies")
def list_taxonomies(auth: api_token_annotation,) -> List[str]:
    return keywords.list_taxonomies()

@router.get("/dictionary/{taxdict_id}")
def get_keyword_from_dictionary(auth: api_token_annotation,
                                taxdict_id: Optional[str]=None) -> TaxonomicDict:
    return keywords.get_keyword_from_dictionary(taxdict_id=taxdict_id)

# Create
@router.post("/dataset/{dataset_id}")
def add_general_keyword(auth: api_token_annotation,
                        dataset_id: uuid.UUID, 
                        keyword: str) -> List[Keywords]:
    return keywords.add_general_keyword(dataset_id=dataset_id,
                                        keyword=keyword)

# Delete
@router.delete("/dataset/{dataset_id}")
def delete_general_keyword(auth: api_token_annotation,
                           dataset_id: uuid.UUID, 
                           keyword: str) -> List[Keywords]:
    return keywords.delete_general_keyword(dataset_id=dataset_id,
                                           keyword=keyword)

# Assign
@router.post("/dictionary/{taxdict_id}")
def assign_taxon_to_dataset(auth: api_token_annotation,
                            taxdict_id: str, 
                            dataset_id: uuid.UUID):
    return keywords.assign_taxon_to_dataset(taxdict_id=taxdict_id, 
                                            dataset_id=dataset_id)

# Remove
@router.delete("/dictionary/{taxdict_id}")
def remove_taxon_from_datase(auth: api_token_annotation,
                             taxdict_id: str, 
                             dataset_id: uuid.UUID):
    return keywords.remove_taxon_from_datase(taxdict_id=taxdict_id, 
                                             dataset_id=dataset_id)