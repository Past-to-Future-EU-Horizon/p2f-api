# Local libraries
from ..apilogs import logger
from ..data.db_connection import engine
from ..data.harm_age import harm_data_age
from p2f_pydantic.harm_age import harm_data_age as Harm_data_age
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional
from uuid import UUID

def list_harm_ages(recent_year_search: Optional[int]=None, 
                   older_year_search: Optional[int]=None) -> List[Harm_data_age]:
    with Session(engine) as session:
        stmt = select(harm_data_age)
        if recent_year_search:
            stmt = stmt.where(harm_data_age.age_mean >= recent_year_search)
        if older_year_search:
            stmt = stmt.where(harm_data_age.age_mean <= older_year_search)
        results = session.execute(harm_data_age).all()
    return [Harm_data_age(**x[0].__dict__) for x in results]

def get_harm_age(
    record_hash: Optional[str]=None, 
    pk_age: Optional[int]=None
    ) -> Harm_data_age:
    with Session(engine) as session:
        stmt = select(harm_data_age)
        if record_hash:
            stmt = stmt.where(harm_data_age.fk_record_hash == record_hash)
        if pk_age:
            stmt = stmt.where(harm_data_age.pk_harm_age == pk_age)
        result = session.execute(stmt)
    return Harm_data_age(**result.tuple()[0].__dict__)

def create_new_harm_data_age(
    new_harm_age: Harm_data_age
    ) -> Harm_data_age:
    with Session(engine) as session:
        stmt = insert(harm_data_age)
        stmt = stmt.values(**new_harm_age)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_age(pk_age=commit.inserted_primary_key[0])

def update_age(update_harm_age: Harm_data_age) -> Harm_data_age:
    with Session(engine) as session:
        stmt = update(harm_data_age)
        stmt = stmt.where(harm_data_age.fk_record_hash == update_harm_age.fk_record_hash)
        stmt = stmt.values(**update_harm_age)
        execute = session.execute(stmt)
        commit = session.commit(stmt)
    return get_harm_age(record_hash=update_harm_age.fk_record_hash)

def delete_age(record_hash: str) -> None:
    with Session(engine) as session:
        stmt = delete(harm_data_age)
        stmt = stmt.where(harm_data_age.fk_record_hash == record_hash)
        execute = session.execute(stmt)
        commit = session.commit()