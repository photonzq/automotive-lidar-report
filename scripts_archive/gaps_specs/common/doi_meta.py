"""Look up public metadata for DOIs via the Crossref and OpenAlex REST APIs.

No contact details (no e-mail, no mailto parameter) are sent; a generic
User-Agent is used. OpenAlex abstracts arrive as an inverted index and are
rebuilt into plain text here. The open-access status and any OA URL that
OpenAlex knows are printed, which is how open full texts were looked for.

Usage : python doi_meta.py <doi> [<doi> ...]
Output: prints title, venue, date, authors with affiliations, OA status and
        abstract; writes doi_<sanitized>.json to GAPS_SPECS_RAW (default ".").
"""
import json
import os
import re
import sys

import requests

OUT = os.environ.get("GAPS_SPECS_RAW", ".")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-script/1.0"}


def openalex(doi):
    r = requests.get(f"https://api.openalex.org/works/https://doi.org/{doi}", headers=UA, timeout=60)
    return r.json() if r.status_code == 200 else None


def crossref(doi):
    r = requests.get(f"https://api.crossref.org/works/{doi}", headers=UA, timeout=60)
    return r.json().get("message") if r.status_code == 200 else None


def abstract_from_index(inv):
    if not inv:
        return None
    pos = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos))


def main(dois):
    for doi in dois:
        print("=" * 30, doi)
        oa, cr = openalex(doi), crossref(doi)
        safe = re.sub(r"[^A-Za-z0-9]+", "_", doi)
        with open(os.path.join(OUT, f"doi_{safe}.json"), "w", encoding="utf-8") as fh:
            json.dump({"openalex": oa, "crossref": cr}, fh, ensure_ascii=False, indent=1)
        if cr:
            print("title:", (cr.get("title") or [""])[0])
            print("venue:", (cr.get("container-title") or [""])[0], cr.get("volume"), cr.get("issue"), cr.get("page"))
            print("issued:", cr.get("issued", {}).get("date-parts"))
            for a in cr.get("author", []):
                aff = "; ".join(x.get("name", "") for x in a.get("affiliation", []))
                print("  author:", a.get("given"), a.get("family"), "|", aff)
            if cr.get("abstract"):
                print("crossref abstract:", re.sub(r"<[^>]+>", "", cr["abstract"]))
        if oa:
            print("openalex OA:", oa.get("open_access"))
            for loc in oa.get("locations", []) or []:
                if loc.get("pdf_url") or loc.get("is_oa"):
                    print("  location:", loc.get("landing_page_url"), loc.get("pdf_url"), loc.get("is_oa"))
            ab = abstract_from_index(oa.get("abstract_inverted_index"))
            if ab:
                print("openalex abstract:", ab)
            for au in oa.get("authorships", []):
                insts = "; ".join(i.get("display_name", "") for i in au.get("institutions", []))
                print("  oa-author:", au.get("author", {}).get("display_name"), "|", insts)


if __name__ == "__main__":
    main(sys.argv[1:])
