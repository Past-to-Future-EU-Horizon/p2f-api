# Local libraries
from ..apilogs import logger
from ..service.harm_numerical import list_numerics
from ..data.db_connection import engine
from ..data.harm_data_types import harm_data_type
from p2f_pydantic.harm_data_types import harm_data_type as Harm_data_type
# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update
# Batteries included libraries
from typing import List, Optional

def list_harm_data_types(
        measure: Optional[str]=None, 
        unit_of_measure: Optional[str]=None,
        method: Optional[str]=None
    ) -> List[Harm_data_type]:
    with Session(engine) as session:
        stmt = select(harm_data_type)
        if measure:
            stmt = stmt.where(harm_data_type.measure == measure)
        if unit_of_measure:
            stmt = stmt.where(harm_data_type.unit_of_measurement == unit_of_measure)
        if method:
            stmt = stmt.where(harm_data_type.method == method)
        results = session.execute(stmt).all()
    return [Harm_data_type(**x[0].__dict__) for x in results]

def get_harm_data_type(
        pk_harm_data_type: int
    ) -> Harm_data_type:
    with Session(engine) as session:
        stmt = select(harm_data_type)
        stmt = stmt.where(harm_data_type.pk_harm_data_type == pk_harm_data_type)
        result = session.execute(stmt).first()
    return Harm_data_type(**result.tuple()[0].__dict__)

def create_harm_data_type(
        new_harm_data_type: Harm_data_type    
    ) -> Harm_data_type:
    with Session(engine) as session:
        stmt = insert(harm_data_type)
        stmt = stmt.values(**new_harm_data_type.model_dump(exclude_unset=True))
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_type(pk_harm_data_type=execute.inserted_primary_key[0])

def update_harm_data_type(
        update_harm_data_type: Harm_data_type
    ) -> Harm_data_type:
    with Session(engine) as session:
        stmt = update(harm_data_type)
        stmt = stmt.where(harm_data_type.pk_harm_data_type == update_harm_data_type.pk_harm_data_type)
        stmt = stmt.values(update_harm_data_type)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_harm_data_type(pk_harm_data_type=update_harm_data_type.pk_harm_data_type)

def delete_harm_data_type(
        pk_harm_data_type: int
    ) -> None:
    with Session(engine) as session:
        stmt = delete(harm_data_type)
        stmt = stmt.where(harm_data_type.pk_harm_data_type == pk_harm_data_type)
        execute = session.execute(stmt)
        commit = session.commit()
    return None