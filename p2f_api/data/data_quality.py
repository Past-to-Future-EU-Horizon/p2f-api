# Local libraries
from p2f_api.apilogs import logger, fa
from .datasets import datasets
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy import func
# Batteries included libraries
from datetime import date
from uuid import UUID
import enum

logger.debug(f"{fa.data} {__name__}")

class dq_comment(baseSQL):
    __tablename__ = "p2f_dq_comment"
    pk_dq_comment: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    comment_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False, default=func.gen_random_uuid())
    email: Mapped[str] = mapped_column(Text, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.{datasets.dataset_identifier}"))

class dq_rating(baseSQL):
    __tablename__ = "p2f_dq_rating"
    pk_dq_rating: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[int] = mapped_column(Integer)
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey(f"{datasets.__tablename__}.{datasets.dataset_identifier}"))

# Below needs to be discussed with the consortium
# class classification_enum(enum.Enum):


# class dq_classification(baseSQL):
#     __tablename__ = "p2f_dq_classification"
