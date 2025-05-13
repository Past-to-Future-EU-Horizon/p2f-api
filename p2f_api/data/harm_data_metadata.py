# Local libraries
from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger, Integer
from sqlalchemy import Float, Double
from sqlalchemy import Text, String
from sqlalchemy import Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
import pytz
# Batteries included libraries
from datetime import date

class harm_location(baseSQL):
    pk_harm_location: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    latitude: Mapped[float] = mapped_column(Double)
    longitude: Mapped[float] = mapped_column(Double)
    location_age: Mapped[int] = mapped_column(BigInteger)
    
class harm_data_species(baseSQL):
    pk_harm_species: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    genus_species: Mapped[str] = mapped_column(Text, index=True)