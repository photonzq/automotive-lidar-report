# -*- coding: utf-8 -*-
"""
Fetch the public Vaud commercial-register extract of a company by its UID,
the same way the public web page https://prestations.vd.ch/pub/101266/ does
(open session -> XSRF cookie -> POST to the public JSON API).

Saves, into OUTDIR:
  vd_excerpt_<LANG>.json   full extract as JSON (FR, DE, EN)
  vd_excerpt_<LANG>.pdf    official PDF extract produced by the register
  vd_doc_<kind>_<id>.pdf   any public statutes / journal documents listed

No login, no email, no key; generic browser User-Agent only.
Usage:  python R3_fastree_vd_register_fetch.py <UID> <OUTDIR>
        e.g. CHE-291.330.490  <scratch>/r3/fastree
"""
import json
import os
import sys
import time

import requests

BASE = "https://prestations.vd.ch/pub/101266/"
API = BASE + "api/public/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def new_session():
    s = requests.Session()
    s.headers.update({"User-Agent": UA,
                      "Accept": "application/json, text/plain, */*",
                      "Referer": BASE})
    s.get(BASE, timeout=60)
    s.get(API + "catalog/configuration", timeout=60)
    tok = s.cookies.get("XSRF-TOKEN")
    if tok:
        s.headers["X-XSRF-TOKEN"] = tok
    return s


def post(s, path, body, binary=False):
    r = s.post(API + path, json=body, timeout=120)
    print(path, r.status_code, r.headers.get("Content-Type"), len(r.content))
    r.raise_for_status()
    return r.content if binary else r.json()


def walk(obj, keys, found):
    """Collect every (key, value) for keys of interest anywhere in the JSON."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in keys and v not in (None, ""):
                found.append((k, v, obj))
            walk(v, keys, found)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, keys, found)


def main(uid, outdir):
    os.makedirs(outdir, exist_ok=True)
    s = new_session()
    rcent = ""
    excerpts = {}
    for lang in ("FR", "DE", "EN"):
        body = {"rcentId": rcent, "lng": lang, "rad": True,
                "companyOfsUid": uid, "extraitTravail": False,
                "admOrderDirection": "ASC", "order": "R"}
        js = post(s, "hrcexcerpts/", body)
        excerpts[lang] = js
        with open(os.path.join(outdir, f"vd_excerpt_{lang}.json"), "w",
                  encoding="utf-8") as f:
            json.dump(js, f, ensure_ascii=False, indent=1)
        if not rcent:
            rcent = str(js.get("id") or js.get("hrcentId") or "")
        time.sleep(1)
    # official PDF extracts (with struck-out = historical entries included)
    for lang in ("FR", "DE"):
        body = {"rcentId": rcent, "lng": lang, "rad": True,
                "companyOfsUid": uid, "extraitTravail": False,
                "admOrderDirection": "ASC", "order": "R"}
        try:
            pdf = post(s, "hrcexcerpts/report", body, binary=True)
            with open(os.path.join(outdir, f"vd_excerpt_{lang}.pdf"), "wb") as f:
                f.write(pdf)
        except Exception as e:  # noqa: BLE001
            print("report", lang, "failed:", e)
        time.sleep(1)
    # public documents referenced in the extract (statutes, journal docs)
    found = []
    walk(excerpts["FR"], {"rdfisId", "byLawDocId"}, found)
    seen = set()
    for k, v, ctx in found:
        if v in seen:
            continue
        seen.add(v)
        body = {"hrcentId": rcent, "uid": uid, "rdfisId": v}
        for kind, path in (("bylaw", "hrcexcerpts/by-law"),
                           ("deed", "hrcexcerpts/fundation-deed")):
            try:
                pdf = post(s, path, body, binary=True)
                if pdf[:4] == b"%PDF":
                    fn = f"vd_doc_{kind}_{v}.pdf"
                    with open(os.path.join(outdir, fn), "wb") as f:
                        f.write(pdf)
                    print("saved", fn, "ref", ctx.get("noReference"))
                    break
            except Exception as e:  # noqa: BLE001
                print(kind, v, "failed:", e)
            time.sleep(1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
