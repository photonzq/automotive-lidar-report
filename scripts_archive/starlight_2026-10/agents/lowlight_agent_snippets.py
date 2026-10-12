"""
Helper snippets used during the low-light / night-vision literature check
(consolidated from one-off inline commands; run with the Anaconda interpreter).

Functions:
  render_pages(pdf, pages, dpi, prefix)   -> PNG renders of selected PDF pages (PyMuPDF)
  find_pages(pdf, keywords)               -> page indices whose text contains keywords (locating only)
  openalex_abstract(doi)                  -> abstract text rebuilt from OpenAlex inverted index
  crossref_meta(doi)                      -> title / container / date / authors from Crossref
  europepmc_fulltext(doi, out_xml)        -> PMC full-text XML via Europe PMC REST
  sony_security_lineup(csv_path)          -> prints Sony security-sensor lineup (pixel size, SNR1s)

No personal identifiers are sent to any API; a generic User-Agent is used.
"""
import csv
import io
import json
import re
import urllib.parse
import urllib.request

import pymupdf

UA = {"User-Agent": "research-script/1.0"}


def _get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def render_pages(pdf, pages, dpi=160, prefix="page"):
    d = pymupdf.open(pdf)
    for i in pages:  # 0-based indices
        d[i].get_pixmap(dpi=dpi).save(f"{prefix}_p{i + 1}.png")


def find_pages(pdf, keywords):
    d = pymupdf.open(pdf)
    hits = []
    for i, p in enumerate(d):
        t = p.get_text()
        if any(k.lower() in t.lower() for k in keywords):
            hits.append(i)
    return hits


def openalex_abstract(doi):
    m = json.loads(_get("https://api.openalex.org/works/https://doi.org/" + doi))
    inv = m.get("abstract_inverted_index") or {}
    pos = {p: w for w, ps in inv.items() for p in ps}
    return m.get("title"), " ".join(pos[i] for i in sorted(pos))


def crossref_meta(doi):
    m = json.loads(_get("https://api.crossref.org/works/" + doi))["message"]
    return (m.get("title"), m.get("container-title"),
            m.get("published", {}).get("date-parts"),
            [(a.get("given"), a.get("family")) for a in m.get("author", [])])


def europepmc_fulltext(doi, out_xml):
    q = urllib.parse.quote("DOI:" + doi)
    r = json.loads(_get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={q}&format=json"))
    pmcid = r["resultList"]["result"][0]["pmcid"]
    xml = _get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
    open(out_xml, "wb").write(xml)
    return pmcid


def sony_security_lineup(csv_path):
    # CSV published by Sony at https://www.sony-semicon.com/files/62/csv/security_data.csv
    s = open(csv_path, encoding="utf-8-sig").read()
    for row in csv.DictReader(io.StringIO(s)):
        print(row["Brand"], row["Model_Name"], row["Resolution"], row["Image_Size"],
              row["Pixel_Size"], row["SNR1s"], row["Color_Mono"], row["NIR_Enhanced"], sep=" | ")


if __name__ == "__main__":
    print(openalex_abstract("10.1117/12.2193738")[1][:300])
