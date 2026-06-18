from p2f_api.service import keywords
from p2f_pydantic.keywords import KeywordDictionary, Keywords
from requests import get
from gzip import GzipFile
from xml.dom import minidom as xdmd

# URLS
## GEMET
url_gemet = "https://www.eionet.europa.eu/gemet/latest/gemet.rdf.gz"    

class gemet:
    def __init__(self):
        self.doc = xdmd.parse(self.get_gemet())
        self.get_rdf_concepts()
    def download_file(self, url):
        r = get(url)
        if r.ok:
            return r.content()
    def get_gemet(self):
        gz = self.download_file(url_gemet)
        gz = GzipFile(gz)
        return gz.read()
    def get_rdf_concepts(self):
        self.concepts = {}
        concepts = self.doc.getElementsByTagName("rdf:Description")
        concepts = [x for x in concepts if x.hasAttribute("rdf:about")]
        concepts = [x for x in concepts if x.getAttribute("rdf:about").startswith("concept/")]
        for concept in concepts:
            concept_id = concept.getAttribute("rdf:about")
            concept_labels = concept.getElementsByTagName("skos:prefLabel")
            concept_labels = [x for x in concept_labels if x.hasAttribute("xml:lang")]
            concept_labels = [x for x in concept_labels if x.getAttribute("xml:lang") == "en"]
            if len(concept_labels) == 1:
                children = [x for x in concept_labels[0].childNodes if x.nodeType == x.TEXT_NODE]
                if len(children) == 1:
                    self.concepts[concept_id] = children[0].nodeValue


                    