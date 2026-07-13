from p2f_api.apilogs import logger, fa
from .db_connection import engine, baseSQL
from sqlalchemy import text
from sqlalchemy import BigInteger
from sqlalchemy import String, Text
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import select, insert, update
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session
from datetime import datetime
from zoneinfo import ZoneInfo

class migration_history(baseSQL):
    __tablename__ = "p2f_migration_history"
    pk_mig_hist: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    mig_name: Mapped[str] = mapped_column(String(255))
    mig_table: Mapped[str] = mapped_column(String(255))
    mig_status: Mapped[bool] = mapped_column(Boolean, default=False)
    creation_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now()
    )
    update_timestamp: Mapped[datetime] = mapped_column(
        DateTime(ZoneInfo("UTC")), default=func.now(), onupdate=func.now()
    )

def add_migration(name, table):
    with Session(engine) as session:
        stmt = insert(migration_history)
        stmt = stmt.values(
            mig_name=name,
            mig_table=table
        )
        execute = session.execute(stmt)
        commit = session.commit()

def get_migration(name, table):
    with Session(engine) as session:
        stmt = select(migration_history)
        stmt = stmt.where(migration_history.mig_name == name)
        stmt = stmt.where(migration_history.mig_table == table)
        result = session.execute(stmt)
    return result

def update_migration_status(name, table, status=True):
    with Session(engine) as session:
        stmt = update(migration_history)
        stmt = stmt.where(migration_history.mig_name == name)
        stmt = stmt.where(migration_history.mig_table == table)
        stmt = stmt.values(mig_status=status)
        session.execute(stmt)
        session.commit()

def migration(name, table, action):
    exists = get_migration(name=name, table=table)
    if len(exists) == 0:
        add_migration(name=name, table=table)
        mig_status = False
    else:
        if len(exists) > 1:
            raise IndexError("Multiple records were found for name and table")
        else:
            mig_status = exists[0].mig_status
    if mig_status == False:
        with Session(engine) as session:
            try:
                session.execute(action)
                update_migration_status(name=name, 
                                        table=table, 
                                        status=True)
            except Exception as e:
                logger.debug("#"*50)
                logger.debug(f"MIGRATION {name} experienced an error")
                logger.debug(f"EXCEPTION:\n e")
                logger.debug("#"*50)
