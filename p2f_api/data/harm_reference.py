from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text, String
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey

# Batteries included libraries
from uuid import UUID

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


class harm_reference_to_record(baseSQL):
    __tablename__ = "p2f_harm_reference_to_record"
    pk_harm_reference_to_record: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )
    fk_harm_reference: Mapped[UUID] = mapped_column(
        ForeignKey("p2f_harm_reference.reference_id")
    )
    fk_record_hash: Mapped[str] = mapped_column(
        ForeignKey("p2f_harm_data_record.record_hash")
    )
