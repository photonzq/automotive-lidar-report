"""Fetch Google Patents pages for a list of publication numbers and save
metadata, abstract, claims and description as plain text, plus the PDF.

Usage:
    python item5a_gpatents_fetch.py OUTDIR PUBNUM [PUBNUM ...] [--no-pdf]

For each publication number (e.g. US20160299228A1) the script writes
OUTDIR/<pubnum>.html (raw page), OUTDIR/<pubnum>.txt (parsed text) and,
unless --no-pdf is given, OUTDIR/<pubnum>.pdf. The parsed text lists title,
inventors, original and current assignee, priority/filing/publication dates,
legal events (including assignments), family members, cited-by and similar
documents, then abstract, claims and description.
"""
import os
import sys
import time

import requests
from bs4 import BeautifulSoup

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def txt(el):
    return " ".join(el.get_text(" ", strip=True).split()) if el else ""


def parse(html):
    s = BeautifulSoup(html, "lxml")
    out = []
    title = s.find("meta", attrs={"name": "DC.title"})
    out.append("TITLE: " + (title["content"].strip() if title else ""))
    for m in s.find_all("meta", attrs={"name": "DC.contributor"}):
        out.append("CONTRIBUTOR (%s): %s" % (m.get("scheme"), m.get("content")))
    for m in s.find_all("meta", attrs={"name": "DC.date"}):
        out.append("DATE (%s): %s" % (m.get("scheme"), m.get("content")))
    # main bibliographic block only (citation tables use <td>/<tr> or nested spans)
    for prop in ["priorityDate", "filingDate", "publicationDate"]:
        for el in s.find_all(attrs={"itemprop": prop}):
            if el.name != "td" and el.find_parent("tr") is None:
                out.append("%s: %s" % (prop, txt(el)))
    for prop in ["assigneeOriginal", "assigneeCurrent", "inventor"]:
        for el in s.find_all("dd", attrs={"itemprop": prop}):
            out.append("%s: %s" % (prop, txt(el)))
    pdf = s.find("meta", attrs={"name": "citation_pdf_url"})
    out.append("PDF: " + (pdf["content"] if pdf else ""))
    out.append("\n== EVENTS (timeline) ==")
    for ev in s.find_all(attrs={"itemprop": "events"}):
        out.append("  EV: " + txt(ev))
    out.append("\n== LEGAL EVENTS ==")
    for ev in s.find_all(attrs={"itemprop": "legalEvents"}):
        out.append("  " + txt(ev))
    out.append("\n== FAMILY / ALSO PUBLISHED / PRIORITY APPS ==")
    for prop in ["docdbFamily", "priorityApps", "appsClaimingPriority",
                 "afterApplications", "applications"]:
        for el in s.find_all(attrs={"itemprop": prop}):
            if el.name in ("tr", "li", "div", "span", "dd"):
                out.append("  %s: %s" % (prop, txt(el)))
    out.append("\n== CITED BY ==")
    for prop in ["forwardReferencesOrig", "forwardReferencesFamily"]:
        for el in s.find_all("tr", attrs={"itemprop": prop}):
            out.append("  %s: %s" % (prop, txt(el)))
    out.append("\n== BACKWARD CITATIONS ==")
    for prop in ["backwardReferencesOrig", "backwardReferencesFamily"]:
        for el in s.find_all("tr", attrs={"itemprop": prop}):
            out.append("  %s: %s" % (prop, txt(el)))
    out.append("\n== SIMILAR DOCUMENTS ==")
    for el in s.find_all("tr", attrs={"itemprop": "similarDocuments"}):
        out.append("  " + txt(el))
    out.append("\n== ABSTRACT ==")
    out.append(txt(s.find("section", attrs={"itemprop": "abstract"})))
    out.append("\n== CLAIMS ==")
    cl = s.find("section", attrs={"itemprop": "claims"})
    if cl:
        for c in cl.find_all("div", class_="claim"):
            if c.find_parent("div", class_="claim") is None:
                out.append(txt(c))
    out.append("\n== DESCRIPTION ==")
    d = s.find("section", attrs={"itemprop": "description"})
    if d:
        for p in d.find_all(["p", "heading", "li"]):
            t = txt(p)
            if t:
                out.append(t)
    return "\n".join(out), (pdf["content"] if pdf else None)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    want_pdf = "--no-pdf" not in sys.argv
    outdir, nums = args[0], args[1:]
    os.makedirs(outdir, exist_ok=True)
    reparse = "--reparse" in sys.argv
    for n in nums:
        local = os.path.join(outdir, n + ".html")
        if reparse and os.path.exists(local):
            with open(local, encoding="utf-8") as f:
                text, pdf = parse(f.read())
            with open(os.path.join(outdir, n + ".txt"), "w", encoding="utf-8") as f:
                f.write(text)
            print(n, "REPARSED", len(text), "chars")
            continue
        url = "https://patents.google.com/patent/%s/en" % n
        r = None
        for wait in (0, 10, 30, 60):  # simple back-off on rate limiting
            time.sleep(wait)
            try:
                r = requests.get(url, headers=UA, timeout=60)
            except Exception as e:  # network problem: retry
                print(n, "ERROR", e)
                r = None
                continue
            if r.status_code == 200:
                break
        if r is None or r.status_code != 200:
            print(n, "HTTP", None if r is None else r.status_code)
            continue
        with open(os.path.join(outdir, n + ".html"), "w", encoding="utf-8") as f:
            f.write(r.text)
        text, pdf = parse(r.text)
        with open(os.path.join(outdir, n + ".txt"), "w", encoding="utf-8") as f:
            f.write(text)
        print(n, "OK", len(text), "chars")
        if want_pdf and pdf:
            try:
                p = requests.get(pdf, headers=UA, timeout=120)
                with open(os.path.join(outdir, n + ".pdf"), "wb") as f:
                    f.write(p.content)
            except Exception as e:
                print(n, "PDF ERROR", e)
        time.sleep(3.0)


if __name__ == "__main__":
    main()
