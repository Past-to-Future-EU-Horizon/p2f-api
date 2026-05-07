# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .harm_data_record import harm_data_record
from .datasets import datasets

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Double
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo


logger.debug(f"{fa.data} {__name__}")

class harm_species(baseSQL):
    __tablename__ = "p2f_harm_species"
    pk_harm_species: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    species_id: Mapped[UUID] = mapped_column(
        Uuid, default=func.gen_random_uuid(), unique=True
    )
    display_species: Mapped[str] = mapped_column(Text, index=True)
    common_name: Mapped[str] = mapped_column(Text, nullable=True)
    tax_domain: Mapped[str] = mapped_column(Text, nullable=True)
    tax_kingdom: Mapped[str] = mapped_column(Text, nullable=True)
    tax_subkingdom: Mapped[str] = mapped_column(Text, nullable=True)
    tax_infrakingdom: Mapped[str] = mapped_column(Text, nullable=True)
    tax_phylum: Mapped[str] = mapped_column(Text, nullable=True)
    tax_class: Mapped[str] = mapped_column(Text, nullable=True)
    tax_subclass: Mapped[str] = mapped_column(Text, nullable=True)
    tax_order: Mapped[str] = mapped_column(Text, nullable=True)
    tax_suborder: Mapped[str] = mapped_column(Text, nullable=True)
    tax_superfamily: Mapped[str] = mapped_column(Text, nullable=True)
    tax_family: Mapped[str] = mapped_column(Text, nullable=True)
    tax_subfamily: Mapped[str] = mapped_column(Text, nullable=True)
    tax_genus: Mapped[str] = mapped_column(Text, nullable=True)
    tax_species: Mapped[str] = mapped_column(Text, nullable=True)
    tax_subspecies: Mapped[str] = mapped_column(Text, nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_species_to_record(baseSQL):
    __tablename__ = "p2f_harm_species_to_rec"
    pk_harm_species_to_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_species_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{harm_species.__tablename__}.species_id")
    )
    fk_data_record: Mapped[str] = mapped_column(
        ForeignKey(f"{harm_data_record.__tablename__}.record_hash")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_species_to_ds(baseSQL):
    __tablename__ = "p2f_harm_species_to_ds"
    pk_harm_species_to_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_species_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{harm_species.__tablename__}.species_id")
    )
    fk_data_record: Mapped[str] = mapped_column(
        ForeignKey(f"{datasets.__tablename__}.dataset_id")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )