# Local libraries
from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger, Integer
from sqlalchemy import Float, Double
from sqlalchemy import Text, String
from sqlalchemy import Date, DateTime
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
import pytz
# Batteries included libraries
from datetime import date

class datasets(baseSQL):
    __tablename__ = "p2f_datasets"
    pk_datasets: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    doi: Mapped[str] = mapped_column(Text, index=True)
    title: Mapped[str] = mapped_column(Text, index=True)
    publication_date: Mapped[date] = mapped_column(DateTime(timezone=pytz.utc))

class dataset_datacite(baseSQL):
    __tablename__ = "p2f_dataset_datacite"
    pk_datacite_metadata: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    datacite_json: Mapped[str] = mapped_column(JSON, nullable=True)
    datacite_xml: Mapped[str] = mapped_column(Text, nullable=True)