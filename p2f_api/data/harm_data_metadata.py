# Local libraries
from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Double
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
# Batteries included libraries
from uuid import UUID

class harm_locations(baseSQL):
    __tablename__ = "p2f_harm_locations"
    pk_harm_location: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    location_identifier: Mapped[UUID] = mapped_column(Uuid, default=func.gen_random_uuid(), unique=True)
    location_name: Mapped[str] = mapped_column(Text, nullable=True)
    location_code: Mapped[str] = mapped_column(Text, nullable=True)
    latitude: Mapped[float] = mapped_column(Double)
    longitude: Mapped[float] = mapped_column(Double)
    elevation: Mapped[float] = mapped_column(Double)
    location_age: Mapped[int] = mapped_column(BigInteger)

class harm_location_to_record(baseSQL):
    __tablename__ = "p2f_harm_location_to_record"
    pk_harm_location_to_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_harm_location: Mapped[UUID] = mapped_column(ForeignKey("p2f_harm_locations.location_identifier"))
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))

class harm_data_species(baseSQL):
    __tablename__ = "p2f_harm_species"
    pk_harm_species: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    species_identifier: Mapped[UUID] = mapped_column(Uuid, default=func.gen_random_uuid(), unique=True)
    display_species: Mapped[str] = mapped_column(Text, index=True)
    common_name: Mapped[str] = mapped_column(Text, nullable=True)
    tax_kingdom: Mapped[str] = mapped_column(Text, nullable=True)
    tax_phylum: Mapped[str] = mapped_column(Text, nullable=True)
    tax_class: Mapped[str] = mapped_column(Text, nullable=True)
    tax_order: Mapped[str] = mapped_column(Text, nullable=True)
    tax_family: Mapped[str] = mapped_column(Text, nullable=True)
    tax_genus: Mapped[str] = mapped_column(Text, nullable=True)
    tax_species: Mapped[str] = mapped_column(Text, nullable=True)

class harm_species_to_record(baseSQL):
    __tablename__ = "p2f_harm_species_to_record"
    pk_harm_species_to_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_species_identifier: Mapped[UUID] = mapped_column(ForeignKey("p2f_harm_species.species_identifier"))
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))