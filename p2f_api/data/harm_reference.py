from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .db_connection import engine
from .harm_data_record import harm_data_record
from .datasets import datasets

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text, String
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


class harm_reference(baseSQL):
    __tablename__ = "p2f_harm_reference"
    pk_harm_reference: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    reference_id: Mapped[UUID] = mapped_column(
        Uuid, unique=True, nullable=False, default=func.gen_random_uuid()
    )
    doi: Mapped[str] = mapped_column(Text, nullable=True)
    other_link: Mapped[str] = mapped_column(Text, nullable=True)
    reference_type: Mapped[str] = mapped_column(String(32), default=None, nullable=True)
    reference_content: Mapped[str] = mapped_column(Text, nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_reference_to_record(baseSQL):
    __tablename__ = "p2f_harm_reference_to_rec"
    pk_harm_reference_to_record: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    fk_harm_reference: Mapped[UUID] = mapped_column(
        ForeignKey(f"{harm_reference.__tablename__}.reference_id")
    )
    fk_record_hash: Mapped[str] = mapped_column(
        ForeignKey(f"{harm_data_record.__tablename__}.record_hash")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class harm_reference_to_dataset(baseSQL):
    __tablename__ = "p2f_harm_reference_to_ds"
    pk_harm_reference_to_dataset: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    fk_harm_reference: Mapped[UUID] = mapped_column(
        ForeignKey(f"{harm_reference.__tablename__}.reference_id")
    )
    fk_dataset_id: Mapped[str] = mapped_column(
        ForeignKey(f"{datasets.__tablename__}.dataset_id")
    )
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )
    
baseSQL.metadata.create_all(engine)