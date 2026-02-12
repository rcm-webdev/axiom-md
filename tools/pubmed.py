import json
import os

from Bio import Entrez
from langchain.tools import tool

Entrez.email = os.getenv("ENTREZ_EMAIL", "user@example.com")

_RETMAX = 5


@tool
def search_pubmed(query: str) -> str:
    """Search PubMed for abstracts relevant to a clinical query.

    Returns a JSON array of objects with pmid, title, and abstract fields.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=_RETMAX)
    record = Entrez.read(handle)
    handle.close()

    pmids = record["IdList"]
    if not pmids:
        return json.dumps([])

    handle = Entrez.efetch(db="pubmed", id=pmids, rettype="xml", retmode="xml")
    records = Entrez.read(handle)
    handle.close()

    results = []
    for article in records["PubmedArticle"]:
        medline = article["MedlineCitation"]
        pmid = str(medline["PMID"])
        title = str(medline["Article"]["ArticleTitle"])

        abstract_data = medline["Article"].get("Abstract", {})
        abstract = " ".join(
            str(t) for t in abstract_data.get("AbstractText", [])
        )

        results.append({"pmid": pmid, "title": title, "abstract": abstract})

    return json.dumps(results)
