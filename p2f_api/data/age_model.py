# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .datasets import datasets
from .harm_data_record import harm_data_record

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Uuid
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

logger.debug(f"{fa.data} {__name__}")

class age_model(baseSQL):
    __tablename__ = "p2f_age_model"
    pk_age_model: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    age_model_id: Mapped[UUID] = mapped_column(
        Uuid, unique=True, nullable=False, default=func.gen_random_uuid()
    )
    age_model_name: Mapped[str] = mapped_column(Text, nullable=False)
    age_model_description: Mapped[str] = mapped_column(Text, nullable=True)  
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class age_model_to_dataset(baseSQL):
    __tablename__ = "p2f_age_model_to_dataset"
    pk_am2d: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_age_model_id: Mapped[UUID] = mapped_column(ForeignKey(f"{age_model.__tablename__}.age_model_id"))
    fk_dataset_id: Mapped[UUID] = mapped_column(
        ForeignKey(f"{datasets.__tablename__}.dataset_id")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class age_model_to_record(baseSQL):
    __tablename__ = "p2f_age_model_to_record"
    pk_am2r: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_age_model_id: Mapped[UUID] = mapped_column(ForeignKey(f"{age_model.__tablename__}.age_model_id"))
    fk_record_hash: Mapped[str] = mapped_column(ForeignKey(f"{harm_data_record.__tablename__}.record_hash"))
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )