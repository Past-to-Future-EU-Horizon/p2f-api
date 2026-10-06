from uuid import UUID
from datetime import datetime
from zoneinfo import ZoneInfo

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import Uuid
from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import ForeignKey

from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .db_connection import engine
from .harm_locations import harm_locations

class core(baseSQL):
    __tablename__ = "p2f_harm_core"
    pk_harm_core: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    core_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False, default=func.gen_random_uuid())
    core_name: Mapped[str] = mapped_column(String(127))
    core_notes: Mapped[str] = mapped_column(Text, nullable=True)
    core_type: Mapped[str] = mapped_column(Text, nullable=False, default="other")
    total_length: Mapped[float] = mapped_column(Float, nullable=True)
    fk_location: Mapped[UUID] = mapped_column(ForeignKey(f"{harm_locations.__tablename__}.location_id"))
    creation_timestamp: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), default=func.now()
        )
    update_timestamp: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), default=func.now(), onupdate=func.now()
        )

class coreSegment(baseSQL):
    __tablename__ = "p2f_harm_core_segment"
    pk_harm_core_segment: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_core_id: Mapped[UUID] = mapped_column(ForeignKey(f"{core.__tablename__}.core_id"))
    core_segment_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False, default=func.gen_random_uuid())
    segment_name: Mapped[str] = mapped_column(String(127))
    segment_notes: Mapped[str] = mapped_column(Text, nullable=True)
    segment_center: Mapped[float] = mapped_column(Float, nullable=True)
    segment_start: Mapped[float] = mapped_column(Float, nullable=True)
    segment_end: Mapped[float] = mapped_column(Float, nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), default=func.now()
            )
    update_timestamp: Mapped[datetime] = mapped_column(
                DateTime(timezone=True), default=func.now(), onupdate=func.now()
            )