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

class harm_data_record(baseSQL):
    pk_harm_data_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_dataset: Mapped[int] = mapped_column(BigInteger, index=True)