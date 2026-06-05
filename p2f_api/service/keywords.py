from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.keywords import keywords, keyword_dictionary
from p2f_pydantic.keywords import Keywords, KeywordDictionary

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

# Get
def get_keyword_from_dictionary(keyword: Optional[str]=None, 
                                taxon: Optional[str]=None, 
                                pk_kd: Optional[int]=None):
    with Session(engine) as session:
        stmt = select(keyword_dictionary)
        if pk_kd is not None:
            stmt = stmt.where(keyword_dictionary.pk_keyword_dictionary == pk_kd)
        else:
            stmt = stmt.where(keyword_dictionary.keyword == keyword)
            if taxon is not None:
                stmt = stmt.where(keyword_dictionary.taxon == taxon)
        result = session.execute(stmt).first()
    return KeywordDictionary.model_validate(result)

# Create
def add_keyword(dataset_id: uuid.UUID, 
                keyword: str, 
                taxon: Optional[str]=None) -> List[Keywords]:
    insert_dict = {"dataset_id": dataset_id,
                   "keyword": keyword,
                   "taxon": taxon}
    insert_dict = {x: y for x, y in insert_dict.items() if y is not None}
    with Session(engine) as session:
        stmt = insert(keywords)
        stmt = stmt.values(**insert_dict)
        session.execute(stmt)
        session.commit()
    return list_keywords(dataset_id=dataset_id)

def create_dictionary_keyword(keyword: str, 
                              taxon: Optional[str]=None):
    with Session(engine) as session:
        stmt = insert(keyword_dictionary)
        stmt = stmt.values(keyword=keyword, 
                           taxon=taxon)
        execute = session.execute(stmt)
        commit = session.commit()
    return get_keyword_from_dictionary(pk_kd=execute.inserted_primary_key[0])

def iterate_keyword_dictionary_stat(keyword: str, 
                                   taxon: Optional[str]=None):
    result = get_keyword_from_dictionary(keyword=keyword, taxon=taxon)
    if result is None:
        result = create_dictionary_keyword(keyword=keyword, taxon=taxon)
    new_value = result.usage + 1
    with Session(engine) as session:
        stmt = update(keyword_dictionary)
        stmt = stmt.where(keyword_dictionary.keyword == keyword)
        if taxon is not None:
            stmt = stmt.where(keyword_dictionary.taxon == taxon)
        stmt = stmt.values(usage = new_value)
        session.execute()
        session.commit()
            

# Delete
def delete_keyword(dataset_id: uuid.UUID, 
                   keyword: str, 
                   taxon: Optional[str]=None) -> List[Keywords]:
    with Session(engine) as session:
        stmt = delete(keywords)
        stmt = stmt.where(keywords.dataset_id == dataset_id)
        stmt = stmt.where(keywords.keyword == keyword)
        if taxon is not None:
            stmt = stmt.where(keywords.taxon == taxon)
        session.execute(stmt)
        session.commit()
    return list_keywords(dataset_id=dataset_id)