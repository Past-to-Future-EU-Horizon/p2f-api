from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.harm_ds_time import harm_ds_frequency
from p2f_pydantic.harm_ds_time import HARM_DS_Frequency

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

# Get
def get_ds_freq(dataset_id: uuid.UUID) -> HARM_DS_Frequency:
    with Session(engine) as session:
        stmt = select(harm_ds_frequency)
        stmt = stmt.where(harm_ds_frequency.dataset_id == dataset_id)
        result = session.execute(stmt)
    return HARM_DS_Frequency(result)

# Create
def create_ds_freq(new_frequency: HARM_DS_Frequency) -> HARM_DS_Frequency:
    with Session(engine) as session:
        stmt = insert(harm_ds_frequency)
        stmt = stmt.values(
            **new_frequency.model_dump(exclude_unset=True)
        )
        execute = session.execute(stmt)
        commit = session.commit()
    return get_ds_freq(dataset_id=new_frequency.dataset_id)

# Delete
def delete_ds_freq(dataset_id: uuid.UUID) -> None:
    with Session(engine) as session:
        stmt = delete(harm_ds_frequency)
        stmt = stmt.where(harm_ds_frequency.dataset_id == dataset_id)
        session.execute(stmt)
        session.commit(stmt)
