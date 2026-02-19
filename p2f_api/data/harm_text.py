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


class harm_text(baseSQL):
    __tablename__ = "p2f_harm_text"
    pk_harm_text: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_record_hash: Mapped[str] = mapped_column(
        ForeignKey("p2f_harm_data_record.record_hash")
    )
    text_id: Mapped[UUID] = mapped_column(
        Uuid, unique=True, nullable=False, default=func.gen_random_uuid()
    )
    text_content: Mapped[str] = mapped_column(Text, nullable=False)
    text_data_type: Mapped[str] = mapped_column(
        ForeignKey("p2f_harm_text_data_types.text_data_type_id")
    )


class harm_text_types(baseSQL):
    __tablename__ = "p2f_harm_text_data_types"
    pk_harm_text_data_types: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    text_data_type_id: Mapped[str] = mapped_column(
        String(16), nullable=False, unique=True
    )
    text_data_type: Mapped[str] = mapped_column(Text, nullable=False)
    text_data_measure: Mapped[str] = mapped_column(Text, nullable=True)
