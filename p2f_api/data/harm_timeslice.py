from p2f_api.apilogs import logger, fa
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

logger.debug(f"{fa.data} {__name__}")


class harm_timeslice(baseSQL):
    __tablename__ = "p2f_harm_timeslice"
    pk_harm_timeslice: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    timeslice_id: Mapped[UUID] = mapped_column(
        Uuid, unique=True, nullable=False, default=func.gen_random_uuid()
    )
    timeslice_name: Mapped[str] = mapped_column(Text)
    timeslice_age_mean: Mapped[int] = mapped_column(BigInteger)
    timeslice_age_recent: Mapped[int] = mapped_column(BigInteger, nullable=True)
    timeslice_age_oldest: Mapped[int] = mapped_column(BigInteger, nullable=True)


class harm_timeslice_to_record(baseSQL):
    __tablename__ = "p2f_harm_timeslice_to_record"
    pk_timeslice_to_record: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_timeslice_id: Mapped[UUID] = mapped_column(
        ForeignKey("p2f_harm_timeslice.pk_harm_timeslice")
    )
    fk_record_hash: Mapped[str] = mapped_column(
        ForeignKey("p2f_harm_data_record.record_hash")
    )
