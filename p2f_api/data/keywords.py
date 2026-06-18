# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
from .datasets import datasets

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Uuid
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
    fk_dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class taxonomic_dict(baseSQL):
    __tablename__ = "p2f_taxonomy_dict"
    pk_taxdict: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    taxdict_id: Mapped[UUID] = mapped_column(
        Uuid, unique=True, nullable=False, default=func.gen_random_uuid()
    )
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    taxonomy: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_keyword: Mapped[str] = mapped_column(String(255), nullable=True)
    taxonomy_id: Mapped[str] = mapped_column(String(255), nullable=True)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

class taxonomic_keyword(baseSQL):
    __tablename__ = "p2f_taxonomic_keywords"
    pk_taxkeywords: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.dataset_id"))
    fk_taxdict_id: Mapped[UUID] = mapped_column(ForeignKey(f"{taxonomic_dict.__tablename__}.taxdict_id"))
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )
