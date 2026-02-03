# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Double, Float
from sqlalchemy import Uuid
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
# Batteries included libraries
from uuid import UUID

logger.debug(f"{fa.data} {__name__}")

class harmonized_int_confidence(baseSQL):
    __tablename__ = "p2f_harm_integer_confidence"
    pk_harm_num: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=func.gen_random_uuid())
    value: Mapped[int] = mapped_column(BigInteger)
    upper_conf_interval: Mapped[float] = mapped_column(Float)
    lower_conf_interval: Mapped[float] = mapped_column(Float)
    upper_conf_value: Mapped[int] = mapped_column(BigInteger)
    lower_conf_value: Mapped[int] = mapped_column(BigInteger)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    fk_data_type: Mapped[UUID] = mapped_column(ForeignKey("p2f_harm_data_types.datatype_id"))

class harmonized_int(baseSQL):
    __tablename__ = "p2f_harm_integer"
    pk_harm_num: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=func.gen_random_uuid())
    value: Mapped[int] = mapped_column(BigInteger)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    fk_data_type: Mapped[UUID] = mapped_column(ForeignKey("p2f_harm_data_types.datatype_id"))

class harmonized_float_confidence(baseSQL):
    __tablename__ = "p2f_harm_float_confidence"
    pk_harm_num: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=func.gen_random_uuid())
    value: Mapped[float] = mapped_column(Double)
    upper_conf_interval: Mapped[float] = mapped_column(Float)
    lower_conf_interval: Mapped[float] = mapped_column(Float)
    upper_conf_value: Mapped[float] = mapped_column(Double)
    lower_conf_value: Mapped[float] = mapped_column(Double)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    fk_data_type: Mapped[UUID] = mapped_column(ForeignKey("p2f_harm_data_types.datatype_id"))

class harmonized_float(baseSQL):
    __tablename__ = "p2f_harm_float"
    pk_harm_num: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=func.gen_random_uuid())
    value: Mapped[float] = mapped_column(Double)
    fk_data_record: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    fk_data_type: Mapped[UUID] = mapped_column(ForeignKey("p2f_harm_data_types.datatype_id"))

class harmonized_numeric_id_map(baseSQL):
    __tablename__ = "p2f_harm_id_map"
    pk_harm_numeric_id_map: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_harm_num: Mapped[UUID] = mapped_column(Uuid, index=True, unique=True, nullable=False)
    table_class: Mapped[str] = mapped_column(Text) # TODO Make this a ENUM