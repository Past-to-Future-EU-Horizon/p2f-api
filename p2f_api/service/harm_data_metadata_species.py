from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.harm_data_metadata import harm_species_to_record, harm_data_species
from p2f_pydantic.harm_data_metadata import harm_data_species as Harm_data_species
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID

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
    logger.debug(f"{fa.service}{fa.list} {__name__}")
    with Session(engine) as session:
        stmt = select(harm_data_species)
        tax_values = {x:y for x, y in dict(locals()).items() if x.startswith("tax_") and y != None}
        if tax_domain is not None:
            stmt = stmt.where(harm_data_species.tax_domain == tax_domain)
        if tax_kingdom is not None:
            stmt = stmt.where(harm_data_species.tax_kingdom == tax_kingdom)
        if tax_subkingdom is not None:
            stmt = stmt.where(harm_data_species.tax_kingdom == tax_subkingdom)
        if tax_infrakingdom is not None:
            stmt = stmt.where(harm_data_species.tax_kingdom == tax_infrakingdom)
        if tax_phylum is not None:
            stmt = stmt.where(harm_data_species.tax_phylum == tax_phylum)
        if tax_class is not None:
            stmt = stmt.where(harm_data_species.tax_class == tax_class)
        if tax_subclass is not None:
            stmt = stmt.where(harm_data_species.tax_class == tax_subclass)
        if tax_order is not None:
            stmt = stmt.where(harm_data_species.tax_order == tax_order)
        if tax_suborder is not None:
            stmt = stmt.where(harm_data_species.tax_order == tax_suborder)
        if tax_superfamily is not None:
            stmt = stmt.where(harm_data_species.tax_family == tax_superfamily)
        if tax_family is not None:
            stmt = stmt.where(harm_data_species.tax_family == tax_family)
        if tax_subfamily is not None:
            stmt = stmt.where(harm_data_species.tax_family == tax_subfamily)
        if tax_genus is not None:
            stmt = stmt.where(harm_data_species.tax_genus == tax_genus)
        if tax_species is not None:
            stmt = stmt.where(harm_data_species.tax_species == tax_species)
        if tax_subspecies is not None:
            stmt = stmt.where(harm_data_species.tax_species == tax_subspecies)
        if common_name is not None:
            stmt = stmt.where(harm_data_species.common_name == common_name)
        if display_species is not None:
            stmt = stmt.where(harm_data_species.display_species == display_species)
        results = session.execute(stmt).all()
    return [Harm_data_species(**x[0].tuple()) for x in results]

def get_harm_metadata_species(species_id: UUID):
    logger.debug(f"{fa.service}{fa.get} {__name__}")
    with Session(engine) as session:
        stmt = select(harm_data_species)
        stmt = stmt.where(harm_data_species.species_identifier == species_id)
        result = session.execute(stmt)
    return Harm_data_species(**result[0].tuple())

def create_harm_metadata_species(new_species: Harm_data_species) -> Harm_data_species:
    logger.debug(f"{fa.service}{fa.create} {__name__}")
    with Session(engine) as session:
        stmt = insert(harm_data_species)
        stmt = stmt.values(**new_species)
        execute = session.execute(stmt)
        commit = session.commit(stmt)
    new_pk = execute.inserted_primary_key
    with Session(engine) as session:
        stmt = select(harm_data_species.species_identifier)
        stmt = stmt.where(harm_data_species.pk_harm_species == new_pk)
        result = session.execute(stmt)
    new_species_id = result[0].tuple().species_identifier

def delete_harm_species(species_id: UUID) -> None:
    logger.debug(f"{fa.service}{fa.delete} {__name__}")
    with Session(engine) as session:
        stmt = delete(harm_data_species)
        stmt = stmt.where(harm_data_species.species_identifier==species_id)
        execute = session.execute(stmt)
        commit = session.commit(stmt)

def assign_species_to_record_hash(species_id: UUID, 
                                  record_hash: str):
    logger.debug(f"{fa.service}{fa.assign} {__name__}")
    with Session(engine) as session:
        stmt = insert(harm_species_to_record)
        stmt = stmt.values(fk_species_identifier=species_id, 
                           fk_data_record=record_hash)
        execute = session.execute(stmt)
        commit = session.commit(stmt)

def remove_specied_to_record_assignment(species_id: UUID, 
                                        record_hash: str):
    logger.debug(f"{fa.service}{fa.remove} {__name__}")
    with Session(engine) as session:
        stmt = delete(harm_species_to_record)
        stmt = stmt.where(harm_species_to_record.fk_species_identifier==species_id)
        stmt = stmt.where(harm_species_to_record.fk_data_record==record_hash)
        execute = session.execute(stmt)
        commit = session.commit(stmt)