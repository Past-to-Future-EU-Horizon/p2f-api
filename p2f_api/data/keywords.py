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

class keywords(baseSQL):
    __tablename__ = "p2f_keywords"
    pk_keywords: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    taxon: Mapped[str] = mapped_column(String(127), nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class keyword_dictionary(baseSQL):
    __tablename__ = "p2f_keyword_dictionary"
    pk_keyword_dictionary: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    taxon: Mapped[str] = mapped_column(String(127), nullable=True)
    usage: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )