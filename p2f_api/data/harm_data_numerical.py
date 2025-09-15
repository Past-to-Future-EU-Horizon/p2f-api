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

class harmonized_int_confidence(baseSQL):
    __tablename__ = "p2f_harm_integer_confidence"
    pk_harm_int_conf: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    value: Mapped[int] = mapped_column(BigInteger)
    upper_conf_interval: Mapped[float] = mapped_column(float)
    lower_conf_interval: Mapped[float] = mapped_column(float)
    upper_conf_value: Mapped[int] = mapped_column(int)
    lower_conf_value: Mapped[int] = mapped_column(int)
    # fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    # fk_data_type: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_type: Mapped[int] = mapped_column(ForeignKey("p2f_harm_data_types.pk_harm_data_type"))

class harmonized_int(baseSQL):
    __tablename__ = "p2f_harm_integer"
    pk_harm_int: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    value: Mapped[int] = mapped_column(BigInteger)
    # fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    # fk_data_type: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_type: Mapped[int] = mapped_column(ForeignKey("p2f_harm_data_types.pk_harm_data_type"))

class harmonized_float_confidence(baseSQL):
    __tablename__ = "p2f_harm_float_confidence"
    pk_harm_float_conf: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    value: Mapped[float] = mapped_column(Double)
    upper_conf_interval: Mapped[float] = mapped_column(float)
    lower_conf_interval: Mapped[float] = mapped_column(float)
    upper_conf_value: Mapped[float] = mapped_column(Double)
    lower_conf_value: Mapped[float] = mapped_column(Double)
    # fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    # fk_data_type: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_type: Mapped[int] = mapped_column(ForeignKey("p2f_harm_data_types.pk_harm_data_type"))

class harmonized_float_confidence(baseSQL):
    __tablename__ = "p2f_harm_float"
    pk_harm_float: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    value: Mapped[float] = mapped_column(Double)
    # fk_data_record: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    # fk_data_type: Mapped[int] = mapped_column(BigInteger, index=True)
    fk_data_type: Mapped[int] = mapped_column(ForeignKey("p2f_harm_data_types.pk_harm_data_type"))
