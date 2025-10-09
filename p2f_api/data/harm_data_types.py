from ..apilogs import logger
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
# Batteries included libraries

class harm_data_type(baseSQL):
    __tablename__ = "p2f_harm_data_types"
    pk_harm_data_type: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    measure: Mapped[str] = mapped_column(Text, index=True)
    unit_of_measurement: Mapped[str] = mapped_column(Text)
    method: Mapped[str] = mapped_column(Text, index=True, nullable=True)
    is_proxy: Mapped[bool] = mapped_column(Boolean, default=False)