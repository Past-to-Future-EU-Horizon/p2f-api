# Local libraries
from p2f_api.apilogs import logger, fa
from .p2f_decbase import baseSQL
# Third Party Libraries
from sqlalchemy import BigInteger
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Uuid
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy import ForeignKey
# Batteries included libraries
from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

logger.debug(f"{fa.data} {__name__}")

class git_repository(baseSQL):
    __tablename__ = "p2f_git_repositories"
    pk_git_repo: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    git_repo_id: Mapped[UUID] = mapped_column(Uuid, unique=True, nullable=False, default=func.gen_random_uuid())
    git_repo_url: Mapped[str] = mapped_column(Text, nullable=False)
    is_p2f_repo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

class git_repository_to_dataset(baseSQL):
    __tablename__ = "p2f_gitrepo_to_dataset"
    pk_gitrepo_to_dataset: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    fk_git_repository: Mapped[UUID] = mapped_column(ForeignKey("p2f_git_repositories.git_repo_id"))
    fk_dataset_id: Mapped[UUID] = mapped_column(ForeignKey("p2f_datasets.dataset_identifier"))