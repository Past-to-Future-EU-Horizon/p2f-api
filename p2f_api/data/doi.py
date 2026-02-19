# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL

# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

# Batteries included libraries
from datetime import datetime
from uuid import UUID
from zoneinfo import ZoneInfo


class doi_metadata(baseSQL):
    __tablename__ = "doi_metadata"
    pk_doi_metadata: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    doi_str: Mapped[str] = mapped_column(Text, index=True)
    metadata_source: Mapped[str] = mapped_column(String(31))
    request_time: Mapped[datetime] = mapped_column(DateTime(timezone=ZoneInfo("UTC")))
    metadata_json: Mapped[dict] = mapped_column(JSONB, nullable=True)
    metadata_xml: Mapped[str] = mapped_column(Text, nullable=True)
