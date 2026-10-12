"""Record of the one-off helper snippets run inline during the SPAD research task.

Run from inside the agents_spadimaging folder. Each function reproduces one inline
command that was executed with `python -c` during the search; nothing here sends
personal identifiers to any API (OpenAlex / Europe PMC are queried anonymously).

    python inline_snippets.py render  <file.pdf> <tag>      # PNG pages at 160 dpi + text dump
    python inline_snippets.py grep    <file.pdf> <regex>    # locate pages containing a pattern
    python inline_snippets.py openalex <doi>                # title + abstract (inverted index)
    python inline_snippets.py epmc    <doi> <out_prefix>    # Europe PMC full-text XML -> .txt
"""
import html
import json
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")


def render(pdf, tag, dpi=160):
    import pymupdf
    d = pymupdf.open(pdf)
    for i in range(d.page_count):
        d[i].get_pixmap(dpi=dpi).save(f"{tag}_p{i + 1}.png")
        print(f"--- page {i + 1}")
        print(d[i].get_text())


def grep(pdf, pattern, span=600):
    import pymupdf
    d = pymupdf.open(pdf)
    for i in range(d.page_count):
        t = d[i].get_text()
        for m in re.finditer(pattern, t, re.I):
            s, e = max(0, m.start() - span), min(len(t), m.end() + span)
            print(f"=== page {i + 1}: " + t[s:e].replace("\n", " "))
            break


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace")


def openalex(doi):
    w = json.loads(_get(f"https://api.openalex.org/works/doi:{doi}"))
    print(w.get("title"), w.get("publication_year"))
    ai = w.get("abstract_inverted_index") or {}
    pos = {p: k for k, v in ai.items() for p in v}
    print(" ".join(pos[i] for i in sorted(pos)) if pos else "no abstract")


def epmc(doi, out_prefix):
    q = json.loads(_get("https://www.ebi.ac.uk/europepmc/webservices/rest/search?"
                        f"query=DOI:{doi}&format=json&resultType=lite"))
    res = q["resultList"]["result"]
    if not res or not res[0].get("pmcid"):
        print("no PMC id")
        return
    pmcid = res[0]["pmcid"]
    x = _get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
    open(f"{out_prefix}_{pmcid}.xml", "w", encoding="utf-8").write(x)
    t = re.sub(r"<[^>]+>", " ", x)
    t = re.sub(r"\s+", " ", html.unescape(t))
    open(f"{out_prefix}.txt", "w", encoding="utf-8").write(t)
    print(pmcid, len(t), "chars")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"render": render, "grep": grep, "openalex": openalex, "epmc": epmc}[cmd](*args)
