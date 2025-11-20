from p2f_api.apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
# Batteries included libraries
from uuid import UUID

class harm_data_age(baseSQL):
    __tablename__ = "p2f_harm_data_age"
    pk_harm_age: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_record_hash: Mapped[str] = mapped_column(ForeignKey("p2f_harm_data_record.record_hash"))
    age_mean: Mapped[int] = mapped_column(BigInteger)
    age_recent: Mapped[int] = mapped_column(BigInteger, nullable=True)
    age_oldest: Mapped[int] = mapped_column(BigInteger, nullable=True)