# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .datasets import datasets

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

logger.debug(f"{fa.data} {__name__}")

class harm_ds_timecoverage(baseSQL):
    __tablename__ = "p2f_harm_ds_timecoverage"
    pk_ds_timecov: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_ds_frequency(baseSQL):
    __tablename__ = "p2f_harm_ds_frequency"
    pk_ds_frequency: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )