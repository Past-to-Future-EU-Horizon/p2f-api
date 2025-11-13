# Local libraries
from ..apilogs import logger
from ..service import harm_data_metadata_species
from p2f_pydantic.harm_data_metadata import harm_data_species as Harm_data_species
# Third Party Libraries
from fastapi import Body, APIRouter, Request
# Batteries included libraries
from uuid import UUID
from typing import Optional, List

router = APIRouter(prefix="/harm-data-species")

# List 
@router.get("/")
def list_harm_metadata_species(
        tax_domain: Optional[str]=None,
        tax_kingdom: Optional[str]=None,
        tax_subkingdom: Optional[str]=None,
        tax_infrakingdom: Optional[str]=None,
        tax_phylum: Optional[str]=None,
        tax_class: Optional[str]=None,
        tax_subclass: Optional[str]=None,
        tax_order: Optional[str]=None,
        tax_suborder: Optional[str]=None,
        tax_superfamily: Optional[str]=None,
        tax_family: Optional[str]=None,
        tax_subfamily: Optional[str]=None,
        tax_genus: Optional[str]=None,
        tax_species: Optional[str]=None,
        tax_subspecies: Optional[str]=None,
        common_name: Optional[str]=None,
        display_species: Optional[str]=None,
    ) -> List[Harm_data_species]:
    return harm_data_metadata_species.list_harm_metadata_species(
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
        display_species=display_species
    )
    

# Get Single
@router.get("/{species_identifier}")
def get_harm_metadata_species(species_identifier: UUID):
    return harm_data_metadata_species.get_harm_metadata_species(species_id=species_identifier)

# Create
@router.post("/")
def create_harm_metadata_species(new_species: Harm_data_species) -> Harm_data_species:
    return harm_data_metadata_species.create_harm_metadata_species(new_species=new_species)
    
# # Update
# @router.put("/")


# Delete
@router.delete("/{species_identifier}")
def delete_harm_species(species_identifier: UUID) -> None:
    return harm_data_metadata_species.delete_harm_species(species_identifier)
    
@router.post("/assign")
def assign_species_to_record_hash(species_id: UUID, 
                                  record_hash: str):
    return harm_data_metadata_species.assign_species_to_record_hash(species_id=species_id,
                                                                    record_hash=record_hash)

@router.delete("/remove")
def remove_specied_to_record_assignment(species_id: UUID, 
                                        record_hash: str):
    return harm_data_metadata_species.remove_specied_to_record_assignment(species_id=species_id,
                                                                          record_hash=record_hash)