# Local libraries
from p2f_api.apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Date
from sqlalchemy import JSON
from sqlalchemy import Boolean
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
import pytz
# Batteries included libraries
from datetime import date
from uuid import UUID

class datasets(baseSQL):
    __tablename__ = "p2f_datasets"
    pk_datasets: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    dataset_identifier: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False, default=func.gen_random_uuid())
    doi: Mapped[str] = mapped_column(Text, index=True, unique=False)
    title: Mapped[str] = mapped_column(Text, index=True)
    sub_dataset_name: Mapped[str] = mapped_column(Text, nullable=True)
    publication_date: Mapped[date] = mapped_column(Date)
    is_new_p2f: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_sub_dataset: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class dataset_datacite(baseSQL):
    __tablename__ = "p2f_dataset_datacite"
    pk_datacite_metadata: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    doi: Mapped[str] = mapped_column(Text, index=True, unique=False)
    datacite_json: Mapped[str] = mapped_column(JSON, nullable=True)
    datacite_xml: Mapped[str] = mapped_column(Text, nullable=True)