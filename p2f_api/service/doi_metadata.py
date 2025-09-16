import requests
import furl

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