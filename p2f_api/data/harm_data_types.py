from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger, Integer
from sqlalchemy import Float, Double
from sqlalchemy import Text, String
from sqlalchemy import Date, DateTime
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
import pytz
# Batteries included libraries
from datetime import date

class harm_data_type(baseSQL):
    __tablname__ = "p2f_harm_data_types"
    pk_harm_data_type: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    measure: Mapped[str] = mapped_column(Text, index=True)
    unit_of_measurement: Mapped[str] = mapped_column(Text)
    method: Mapped[str] = mapped_column(Text, index=True, nullable=True)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)