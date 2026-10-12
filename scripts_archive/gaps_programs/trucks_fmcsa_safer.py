"""Query FMCSA SAFER company snapshots by carrier name and print power units and MCS-150 dates.

Purpose: size the truck fleets of autonomous-trucking operators (Gatik, Aurora, Kodiak, Bot Auto,
Waabi, PlusAI) from their self-reported USDOT registrations (Appendix 1, trucking items).
Power units are self-reported on Form MCS-150 and may be stale; they count all trucks
registered to the carrier, with or without automation hardware.
Usage:   python trucks_fmcsa_safer.py [OUTDIR] [NAME ...]   (default OUTDIR ./safer)
Inputs:  public SAFER pages at https://safer.fmcsa.dot.gov (no key needed).
Outputs: HTML saved per query in OUTDIR; printed legal name, USDOT number, power units,
         drivers, operating status and MCS-150 form date for each matching carrier.
Date:    2026-10-03
"""
import os
import re
import sys
from html import unescape

import requests

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
URL = "https://safer.fmcsa.dot.gov/query.asp"
DEFAULT = ["GATIK", "AURORA OPERATIONS", "KODIAK ROBOTICS", "BOT AUTO", "WAABI", "PLUSAI", "PLUS AUTOMATION"]


def text(html):
    t = re.sub(r"(?is)<(script|style).*?</\1>", " ", html)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", t)))


LABELS = ["Entity Type", "USDOT Status", "Out of Service Date", "USDOT Number", "State Carrier ID Number",
          "MCS-150 Form Date", "MCS-150 Mileage (Year)", "OPERATING AUTHORITY INFORMATION",
          "Operating Authority Status", "MC/MX/FF Number(s)", "COMPANY INFORMATION", "Legal Name",
          "DBA Name", "Physical Address", "Phone", "Mailing Address", "DUNS Number", "Power Units",
          "Non-CMV Units", "Drivers", "Operation Classification"]


def field(t, label, n=80):
    """Return the value after 'label:' up to the next known label."""
    m = re.search(re.escape(label) + r"\s*:\s*(.{0,%d})" % n, t)
    if not m:
        return ""
    val = m.group(1)
    cut = min([val.find(x) for x in LABELS if x != label and val.find(x) >= 0] + [len(val)])
    return val[:cut].strip()


def snapshot(session, outdir, param, value):
    p = {"searchtype": "ANY", "query_type": "queryCarrierSnapshot", "query_param": param, "query_string": value}
    r = session.get(URL, params=p, headers={"User-Agent": UA}, timeout=60)
    fn = os.path.join(outdir, re.sub(r"\W+", "_", f"{param}_{value}") + ".html")
    open(fn, "w", encoding="utf-8").write(r.text)
    return r.text


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "safer"
    names = sys.argv[2:] or DEFAULT
    os.makedirs(outdir, exist_ok=True)
    s = requests.Session()
    for name in names:
        html = snapshot(s, outdir, "NAME", name)
        # A name query returns either a list of matches or a single snapshot.
        dots = sorted(set(re.findall(r"query_param=USDOT&(?:amp;)?(?:original_query_param=NAME&(?:amp;)?)?query_string=(\d+)", html)))
        if not dots and "USDOT Number" in html:
            dots = [None]
        print(f"===== {name}: {len(dots)} match(es)")
        for dot in dots[:12]:
            h = html if dot is None else snapshot(s, outdir, "USDOT", dot)
            t = text(h)
            print("  legal name:", field(t, "Legal Name", 60), "| USDOT:", field(t, "USDOT Number", 12),
                  "| power units:", field(t, "Power Units", 8), "| drivers:", field(t, "Drivers", 8),
                  "| status:", field(t, "USDOT Status", 25), "| MCS-150 date:", field(t, "MCS-150 Form Date", 12),
                  "| op:", field(t, "Operating Authority Status", 40))


if __name__ == "__main__":
    main()
