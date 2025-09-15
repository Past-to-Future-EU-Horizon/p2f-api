# Local libraries
from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger, Integer
from sqlalchemy import Float, Double
from sqlalchemy import Text, String
from sqlalchemy import Date, DateTime
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
import pytz
# Batteries included libraries
from datetime import date
from uuid import UUID

class harm_locations(baseSQL):
    __tablename__ = "p2f_harm_locations"
    pk_harm_location: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    # fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    # fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    location_identifier: Mapped[UUID] = mapped_column(Uuid, default=func.gen_random_uuid(), unique=True)
    latitude: Mapped[float] = mapped_column(Double)
    longitude: Mapped[float] = mapped_column(Double)
    location_age: Mapped[int] = mapped_column(BigInteger)

class harm_location_to_record(baseSQL):
    __tablename__ = "p2f_harm_location_to_record"
    pk_harm_location_to_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_harm_location: Mapped[int] = mapped_column(ForeignKey("p2f_harm_location_to_record.location_identifier"))
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))

class harm_data_species(baseSQL):
    __tablename__ = "p2f_harm_species"
    pk_harm_species: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    # fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    genus_species: Mapped[str] = mapped_column(Text, index=True)