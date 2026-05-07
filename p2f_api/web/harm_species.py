# Local libraries
from p2f_api.apilogs import logger, fa
from .temp_accounts import combined_auth, api_token_annotation
from ..service import harm_species
from p2f_pydantic.harm_species import HARM_Species
from p2f_pydantic.temp_accounts import Temp_Account

# Third Party Libraries
from fastapi import Body, APIRouter, Depends

# Batteries included libraries
from uuid import UUID
from typing import Optional, List, Annotated
from inspect import stack

router = APIRouter(prefix="/harm-data-species")


# List
@router.get("/")
def list_harm_metadata_species(
    auth: api_token_annotation,
    tax_domain: Optional[str] = None,
    tax_kingdom: Optional[str] = None,
    tax_subkingdom: Optional[str] = None,
    tax_infrakingdom: Optional[str] = None,
    tax_phylum: Optional[str] = None,
    tax_class: Optional[str] = None,
    tax_subclass: Optional[str] = None,
    tax_order: Optional[str] = None,
    tax_suborder: Optional[str] = None,
    tax_superfamily: Optional[str] = None,
    tax_family: Optional[str] = None,
    tax_subfamily: Optional[str] = None,
    tax_genus: Optional[str] = None,
    tax_species: Optional[str] = None,
    tax_subspecies: Optional[str] = None,
    common_name: Optional[str] = None,
    display_species: Optional[str] = None,
) -> List[HARM_Species]:
    logger.debug(f"{fa.web}{fa.list} {__name__} {stack()[0][3]}()")
    return harm_species.list_harm_metadata_species(
        tax_domain=tax_domain,
        tax_kingdom=tax_kingdom,
        tax_subkingdom=tax_subkingdom,
        tax_infrakingdom=tax_infrakingdom,
        tax_phylum=tax_phylum,
        tax_class=tax_class,
        tax_subclass=tax_subclass,
        tax_order=tax_order,
        tax_suborder=tax_suborder,
        tax_superfamily=tax_superfamily,
        tax_family=tax_family,
        tax_subfamily=tax_subfamily,
        tax_genus=tax_genus,
        tax_species=tax_species,
        tax_subspecies=tax_subspecies,
        common_name=common_name,
        display_species=display_species,
    )


# Get Single
@router.get("/{species_id}")
def get_harm_metadata_species(auth: api_token_annotation,
                              species_id: UUID):
    logger.debug(f"{fa.web}{fa.get} {__name__} {stack()[0][3]}()")
    return harm_species.get_harm_metadata_species(
        species_id=species_id
    )


# Create
@router.post("/")
def create_harm_metadata_species(auth: api_token_annotation,
                                 new_species: HARM_Species) -> HARM_Species:
    logger.debug(f"{fa.web}{fa.create} {__name__} {stack()[0][3]}()")
    return harm_species.create_harm_metadata_species(
        new_species=new_species
    )


# # Update
# @router.put("/")


# Delete
@router.delete("/{species_id}", include_in_schema=False)
def delete_harm_species(auth: api_token_annotation,
                        species_id: UUID) -> None:
    logger.debug(f"{fa.web}{fa.delete} {__name__} {stack()[0][3]}()")
    return harm_species.delete_harm_species(species_id)


@router.post("/assign")
def assign_species_to_record_hash(auth: api_token_annotation,
                                  species_id: UUID, 
                                  record_hash: str):
    logger.debug(f"{fa.web}{fa.assign} {__name__} {stack()[0][3]}()")
    return harm_species.assign_species_to_record_hash(
        species_id=species_id, record_hash=record_hash
    )


@router.delete("/remove")
def remove_species_to_record_assignment(auth: api_token_annotation,
                                        species_id: UUID, 
                                        record_hash: str):
    logger.debug(f"{fa.web}{fa.remove} {__name__} {stack()[0][3]}()")
    return harm_species.remove_specied_to_record_assignment(
        species_id=species_id, record_hash=record_hash
    )
