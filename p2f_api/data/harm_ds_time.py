from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .datasets import datasets

from sqlalchemy import BigInteger
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

logger.debug(f"{fa.data} {__name__}")

class harm_ds_timecoverage(baseSQL):
    __tablename__ = "p2f_harm_ds_timecoverage"
    pk_ds_timecov: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    oldest: Mapped[int] = mapped_column(BigInteger)
    youngest: Mapped[int] = mapped_column(BigInteger)
    reference_zero: Mapped[int] = mapped_column(BigInteger)
    oldest_older_conf: Mapped[int] = mapped_column(Integer, nullable=True)
    oldest_younger_conf: Mapped[int] = mapped_column(Integer, nullable=True)
    younger_older_conf: Mapped[int] = mapped_column(Integer, nullable=True)
    younger_youngest_conf: Mapped[int] = mapped_column(Integer, nullable=True)
    older_conf_interval: Mapped[float] = mapped_column(Float, nullable=True)
    younger_conf_interval: Mapped[float] = mapped_column(Float, nullable=True)
    assigned_by_human: Mapped[bool] = mapped_column(Boolean, default=False)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_ds_seasonality(baseSQL):
    __tablename__ = "p2f_harm_ds_seasonality"
    pk_ds_seasonality: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    has_seasonality: Mapped[bool] = mapped_column(Boolean, default=False)
    seasonailty_type: Mapped[str] = mapped_column(String(63), nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_ds_frequency(baseSQL):
    __tablename__ = "p2f_harm_ds_frequency"
    pk_ds_frequency: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    mean_frequency: Mapped[int] = mapped_column(BigInteger, nullable=True)
    shortest_frequency: Mapped[int] = mapped_column(BigInteger, nullable=True)
    longest_frequency: Mapped[int] = mapped_column(BigInteger, nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )