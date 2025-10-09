from ..apilogs import logger
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
        tax_kingdom: Optional[str],
        tax_phylum: Optional[str],
        tax_class: Optional[str],
        tax_order: Optional[str],
        tax_family: Optional[str],
        tax_genus: Optional[str],
        tax_species: Optional[str],
        common_name: Optional[str],
        display_species: str
    ) -> List[Harm_data_species]:
    with Session(engine) as session:
        stmt = select(harm_data_species)
        if tax_kingdom:
            stmt = stmt.where(harm_data_species.tax_kingdom == tax_kingdom)
        if tax_phylum:
            stmt = stmt.where(harm_data_species.tax_phylum == tax_phylum)
        if tax_class:
            stmt = stmt.where(harm_data_species.tax_class == tax_class)
        if tax_order:
            stmt = stmt.where(harm_data_species.tax_order == tax_order)
        if tax_family:
            stmt = stmt.where(harm_data_species.tax_family == tax_family)
        if tax_genus:
            stmt = stmt.where(harm_data_species.tax_genus == tax_genus)
        if tax_species:
            stmt = stmt.where(harm_data_species.tax_species == tax_species)
        if common_name:
            stmt = stmt.where(harm_data_species.common_name == common_name)
        if display_species:
            stmt = stmt.where(harm_data_species.display_species == display_species)
        results = session.execute(stmt).all()
    return [Harm_data_species(**x[0].tuple()) for x in results]

def get_harm_metadata_species(species_id: UUID):
    with Session(engine) as session:
        stmt = select(harm_data_species)
        stmt = stmt.where(harm_data_species.species_identifier == species_id)
        result = session.execute(stmt)
    return Harm_data_species(**result[0].tuple())

def create_harm_metadata_species(new_species: Harm_data_species) -> Harm_data_species:
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
