from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.keywords import keywords, taxonomic_keyword, taxonomic_dict
from p2f_pydantic.keywords import Keywords, TaxonomicDict

# Third Party Libraries
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update

# Batteries included libraries
import uuid
from typing import List, Optional
from inspect import stack

# List
def list_keywords(dataset_id: Optional[str]=None,
                  contains: Optional[str]=None) -> List[Keywords]:
    with Session(engine) as session:
        stmt = select(keywords)
        if dataset_id is not None:
            stmt = stmt.where(keywords.dataset_id == dataset_id)
        if contains is not None:
            stmt = stmt.where(keywords.keyword.contains(contains))
        results = session.execute(stmt).all()
    return [Keywords(x) for x in results]

def list_taxonomic_dictionary(taxonomy: Optional[str]=None,
                              contains: Optional[str]=None) -> List[TaxonomicDict]:
    with Session(engine) as session:
        stmt = select(taxonomic_dict)
        if taxonomy is not None:
            stmt = stmt.where(taxonomic_dict.taxonomy == taxonomy)
        if contains is not None:
            stmt = stmt.where(taxonomic_dict.keyword.contains(contains))
        results = session.execute(stmt).all()
    return [TaxonomicDict(x) for x in results]

# Get
def get_keyword_from_dictionary(taxdict_id: Optional[str]=None, 
                                pk_kd: Optional[int]=None):
    with Session(engine) as session:
        stmt = select(taxonomic_dict)
        if pk_kd is not None:
            stmt = stmt.where(taxonomic_dict.pk_taxdict == pk_kd)
        if taxdict_id is not None:
            stmt = stmt.where(taxonomic_dict.taxdict_id == taxdict_id)
        result = session.execute(stmt).first()
    return TaxonomicDict.model_validate(result)

# Create
def add_general_keyword(dataset_id: uuid.UUID, 
                        keyword: str) -> List[Keywords]:
    insert_dict = {"dataset_id": dataset_id,
                   "keyword": keyword}
    insert_dict = {x: y for x, y in insert_dict.items() if y is not None}
    with Session(engine) as session:
        stmt = insert(keywords)
        stmt = stmt.values(**insert_dict)
        session.execute(stmt)
        session.commit()
    return list_keywords(dataset_id=dataset_id)

def create_dictionary_keyword(keyword: str, 
                              taxon: str,
                              taxonomic_id: Optional[str]=None, 
                              parent_keyword: Optional[str]=None):
    insert_dict = {"keyword": keyword,
                   "taxon": taxon,
                   "taxonomic_id": taxonomic_id, 
                   "parent_keyword": parent_keyword}
    insert_dict = {x:y for x, y in insert_dict.items() if y is not None}
    with Session(engine) as session:
        stmt = insert(taxonomic_dict)
        stmt = stmt.values(**insert_dict)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_keyword_from_dictionary(pk_kd=execute.inserted_primary_key[0])

# Delete
def delete_general_keyword(dataset_id: uuid.UUID, 
                   keyword: str) -> List[Keywords]:
    with Session(engine) as session:
        stmt = delete(keywords)
        stmt = stmt.where(keywords.dataset_id == dataset_id)
        stmt = stmt.where(keywords.keyword == keyword)
        session.execute(stmt)
        session.commit()
    return list_keywords(dataset_id=dataset_id)

# Assign
def assign_taxon_to_dataset(taxdict_id: str, dataset_id: uuid):
    with Session(engine) as session:
        stmt = insert(taxonomic_keyword)
        stmt = stmt.values(fk_dataset_id=dataset_id, 
                           fk_taxdict_id=taxdict_id)
        session.execute(stmt)
        session.commit()

def remove_taxon_from_datase(taxdict_id: str, dataset_id: uuid):
    with Session(engine) as session:
        stmt = delete(taxonomic_keyword)
        stmt = stmt.where(taxonomic_keyword.fk_dataset_id == dataset_id)
        stmt = stmt.where(taxonomic_keyword.fk_taxdict_id == taxdict_id)
        session.execute(stmt)
        session.commit()