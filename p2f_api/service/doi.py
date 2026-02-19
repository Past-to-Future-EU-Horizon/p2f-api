# Local libraries
from p2f_api.apilogs import logger, fa
from p2f_api.doi import doi as DOI
from ..data.db_connection import engine
from ..data.doi import doi_metadata
from ..service.datasets import get_dataset

# Third Party Libraries
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
import furl
import requests

# Batteries included libraries
from uuid import UUID
from typing import Optional, Literal
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from base64 import b64decode
from xml.dom import minidom as xdmd
from inspect import stack

datacite_api_url = "https://api.datacite.org/"
crossref_api_url = "https://api.crossref.org/"

datacite_api_furl = furl.furl(datacite_api_url)
crossref_api_furl = furl.furl(crossref_api_url)


def insert_doi_metadata(
    doi: str,
    source: Literal["DATACITE", "CROSSREF", "ZENODO"],
    metadata_json: Optional[str] = None,
    metadata_xml: Optional[str] = None,
    request_time: datetime = datetime.now(tz=ZoneInfo("UTC")),
):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    doi = DOI(doi)
    with Session(engine) as session:
        stmt = insert(doi_metadata)
        stmt = stmt.values(
            doi_str=doi.string,
            metadata_source=source,
            request_time=request_time,
            metadata_json=metadata_json,
            metadata_xml=metadata_xml,
        )
        execute = session.execute(stmt)
        commit = session.commit()


def request_insert_datacite_doi(doi: str) -> str:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    doi_url = datacite_api_furl / "dois" / doi
    r = requests.get(doi_url)
    if r.ok:
        doc_json = r.json()
        if "data" in doc_json.keys():
            doc_data = doc_json["data"]
            if "attributes" in doc_data.keys():
                doc_attrs = doc_data["attributes"]
                if "xml" in doc_attrs.keys():
                    # check for base64 encoded XML in DataCite JSON
                    doc_xml = doc_attrs["xml"]
                    xml_b64 = b64decode(doc_xml)
                    xml_content = xdmd.parseString(xml_b64).toxml()
                    doc_json["data"]["attributes"].pop("xml")
                else:
                    xml_content = None
        insert_doi_metadata(
            doi=doi, source="DATACITE", metadata_xml=xml_content, metadata_json=doc_json
        )
        return doc_json
    else:
        return None


def request_insert_crossref_doi(doi: str) -> str:
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")
    doi_url = crossref_api_furl / "works" / doi
    r = requests.get(doi_url)
    if r.ok:
        insert_doi_metadata(doi=doi, source="CROSSREF", metadata_json=r.json())
        return r.json()
    else:
        return None


def request_insert_zenodo_doi(doi: str) -> str:
    # This is an extra for the future
    pass


def request_insert_doi_metadata(doi: str):
    logger.debug(f"{fa.background}{fa.get} {__name__} {stack()[0][3]}()")


def get_doi(
    dataset_id: Optional[UUID] = None,
    doi_prefix: Optional[str] = None,
    doi_suffix: Optional[str] = None,
):
    logger.debug(f"{fa.service}{fa.get} {__name__} {stack()[0][3]}()")
    # TODO Add protection here for anti-DDOSing our friends at DataCite, Crossref, Zenodo
    # TODO Add check here if DOI within our database
    if dataset_id is not None:
        dataset = get_dataset(dataset_id=dataset_id)
        existing_doi = DOI(dataset.doi)
    if doi_prefix is not None:
        if doi_suffix is not None:
            existing_doi = DOI(f"{doi_prefix}/{doi_suffix}")
        else:
            raise ValueError("DOI prefix and suffix both must be supplied together.")
    with Session(engine) as session:
        logger.debug("Created session")
        stmt = select(doi_metadata)
        stmt = stmt.where(doi_metadata.doi_str == existing_doi.string)
        result = session.execute(stmt).first()
    logger.debug(f"Result: {type(result)}")
    if result is not None:
        if result[0].request_time + timedelta(days=30) > datetime.now(
            tz=ZoneInfo("UTC")
        ):
            logger.debug("Returning existing result")
            return result[0].metadata_json
        else:
            logger.debug("Stale result, refreshing database")
            match result[0].metadata_source:
                case "DATACITE":
                    return request_insert_datacite_doi(existing_doi.string)
                case "CROSSREF":
                    return request_insert_crossref_doi(existing_doi.string)
    else:
        logger.debug("No existing result, collecting from online")
        datacite = request_insert_datacite_doi(existing_doi.string)
        if datacite is None:
            logger.debug("DataCite did not have a record, trying Crossref")
            crossref = request_insert_crossref_doi(existing_doi.string)
            return crossref
        else:
            logger.debug("DataCite had a result, returning document")
            return datacite
