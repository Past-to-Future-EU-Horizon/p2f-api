from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
# Batteries included libraries
from uuid import UUID

class harm_timeslice(baseSQL):
    __tablename__ = "p2f_harm_timeslice"
    pk_harm_timeslice: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    timeslice_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False, default=func.gen_random_uuid())
    timeslice_name: Mapped[str] = mapped_column(Text)
    timeslice_age_mean: Mapped[int] = mapped_column(BigInteger)
    timeslice_age_recent: Mapped[int] = mapped_column(BigInteger, nullable=True)
    timeslice_age_oldest: Mapped[int] = mapped_column(BigInteger, nullable=True)