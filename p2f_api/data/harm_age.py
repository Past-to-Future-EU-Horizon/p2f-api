from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .harm_data_record import harm_data_record

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo


logger.debug(f"{fa.data} {__name__}")


class harm_rec_age(baseSQL):
    __tablename__ = "p2f_harm_age"
    pk_harm_age: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_record_hash: Mapped[str] = mapped_column(
        ForeignKey(f"{harm_data_record.__tablename__}.record_hash")
    )
    age_mean: Mapped[int] = mapped_column(BigInteger)
    age_recent: Mapped[int] = mapped_column(BigInteger, nullable=True)
    age_oldest: Mapped[int] = mapped_column(BigInteger, nullable=True)
    reference_zero: Mapped[int] = mapped_column(BigInteger, nullable=False)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )
