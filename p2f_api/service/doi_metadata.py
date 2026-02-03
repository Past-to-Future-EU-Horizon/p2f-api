# Local libraries
from p2f_api.apilogs import logger, fa
from ..data.db_connection import engine
from ..data.datasets import dataset_datacite
# Third Party Libraries
import requests
import furl
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
# Batteries included libraries

datacite_api_url = "https://api.datacite.org/"
crossref_api_url = "https://api.crossref.org/"

datacite_api_furl = furl.furl(datacite_api_url)
crossref_api_furl = furl.furl(crossref_api_url)

def request_dataset_doi(doi: str) -> str:
    logger.debug(f"{fa.background}{fa.get} {__name__}")
    doi_url = datacite_api_furl / doi
    r = requests.get(doi_url)
    if r.status_code in requests.Response.ok:
        return r.json
    else:
        return None
    
def request_publication_doi(doi: str) -> str:
    logger.debug(f"{fa.background}{fa.get} {__name__}")
    doi_url = crossref_api_furl / "works" / doi
    r = requests.get(doi_url)
    if r.status_code in requests.Response.ok:
        return r.json
    else:
        return None
    
def insert_doi_datacite(doi, json_document):
    with Session(engine) as session:
        logger.debug(f"{fa.background}{fa.create} {__name__}")
        stmt = insert(dataset_datacite)
        stmt = stmt.values(
            doi=doi,
            datacite_json=json_document
        )
        execute = session.execute(stmt)
        commit = session.commit()

def get_doi_datacite(doi):
    with Session(engine) as session:
        logger.debug(f"{fa.service}{fa.create} {__name__}")
        stmt = select(dataset_datacite)
        stmt = stmt.where(dataset_datacite.doi == doi)
        results = session.execute(stmt)
    return [x[0].datacite_json for x in results]