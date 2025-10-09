from ..data.db_connection import engine
from ..data.datasets import dataset_datacite
import requests
import furl
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

datacite_api_url = "https://api.datacite.org/"
crossref_api_url = "https://api.crossref.org/"

datacite_api_furl = furl.furl(datacite_api_url)
crossref_api_furl = furl.furl(crossref_api_url)

def request_dataset_doi(doi: str) -> str:
    doi_url = datacite_api_furl / doi
    r = requests.get(doi_url)
    if r.status_code in requests.Response.ok:
        return r.json
    else:
        return None
    
def request_publication_doi(doi: str) -> str:
    doi_url = crossref_api_furl / "works" / doi
    r = requests.get(doi_url)
    if r.status_code in requests.Response.ok:
        return r.json
    else:
        return None
    
def insert_doi_datacite(doi, json_document):
    with Session(engine) as session:
        stmt = insert(dataset_datacite)
        stmt = stmt.values(
            doi=doi,
            datacite_json=json_document
        )
        execute = session.execute(stmt)
        commit = session.commit()

def get_doi_datacite(doi):
    with Session(engine) as session:
        stmt = select(dataset_datacite)
        stmt = stmt.where(dataset_datacite.doi == doi)
        results = session.execute(stmt)
    return [x[0].datacite_json for x in results]