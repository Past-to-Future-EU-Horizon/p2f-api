from p2f_api.service import keywords
from p2f_pydantic.keywords import KeywordDictionary, Keywords
from requests import get
from gzip import GzipFile
from xml.dom import minidom as xdmd

# URLS
## GEMET
url_gemet = "https://www.eionet.europa.eu/gemet/latest/gemet.rdf.gz"

def download_file(url):
    r = get(url)
    if r.ok:
        return r.content()
    
def get_gemet():
    gz = download_file(url_gemet)
    gz = GzipFile(gz)
    return gz.read()

class gemet:
    def __init__(self, rdf_doc):
        self.doc = xdmd.parse(rdf_doc)
    