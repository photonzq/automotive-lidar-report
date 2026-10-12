"""Parse the tone-review tables and check each quoted span against the report.

For every finding row it records whether the quote occurs verbatim in the report,
how often, and on which lines.  Quotes that were abbreviated with an ellipsis or
that list several spans separated by '; ' are split and each piece is checked.

Usage: python check_quotes.py <report.md> <tone_review_dir> <out.json>
"""
import json
import re
import sys
from pathlib import Path

report_path, review_dir, out_path = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
lines = Path(report_path).read_text(encoding="utf-8").split("\n")
text = "\n".join(lines)


def where(span):
    """Return the 1-based line numbers on which span occurs (span may not cross lines)."""
    hits = []
    for i, ln in enumerate(lines, 1):
        start = 0
        while True:
            k = ln.find(span, start)
            if k < 0:
                break
            hits.append(i)
            start = k + 1
    return hits


def pieces(quote):
    """Split a quote cell into checkable spans."""
    q = quote.strip()
    q = re.sub(r"^\d{3,5}:\s*", "", q)          # leading "3640: " labels
    parts = re.split(r";\s+(?=\d{3,5}:\s)|\s*…\s*|\s*\(…\)\s*", q)
    out = []
    for p in parts:
        p = re.sub(r"^\d{3,5}:\s*", "", p.strip())
        p = p.strip().strip("`").strip()
        if len(p) >= 8:
            out.append(p)
    return out


rows = []
for md in sorted(review_dir.glob("[0-9][0-9]_*.md")):
    section = md.stem
    header = None
    for raw in md.read_text(encoding="utf-8").split("\n"):
        if not raw.startswith("|") or raw.startswith("|---"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if header is None:
            header = [h.lower() for h in cells]
            continue
        rec = dict(zip(header, cells))
        # two table layouts: (line, quote, replacement, sev, cat) and
        # (line, exact quote, category, why, proposed replacement, severity)
        if "proposed replacement" in header:
            quote = rec.get("exact quote", "")
            repl = rec.get("proposed replacement", "")
            sev = rec.get("severity", "")
            cat = rec.get("category", "") + " — " + rec.get("why", "")
        else:
            quote = rec.get("quote", "")
            repl = rec.get("replacement", "")
            sev = rec.get("sev", "")
            cat = rec.get("cat / why", "")
        found = []
        for p in pieces(quote):
            found.append({"span": p, "lines": where(p)})
        status = "not-found"
        if found and all(f["lines"] for f in found):
            status = "exact"
        elif any(f["lines"] for f in found):
            status = "partial"
        rows.append({
            "section": section,
            "line_cited": rec.get("line", ""),
            "quote": quote,
            "replacement": repl,
            "severity": sev.lower().strip(),
            "category": cat,
            "spans": found,
            "status": status,
        })

Path(out_path).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
print(len(rows), "rows")
print(Counter(r["status"] for r in rows))
print(Counter(r["severity"] for r in rows))
for r in rows:
    if r["status"] != "exact":
        print(f'{r["section"]:>14} L{r["line_cited"]:<22} {r["status"]:<9} {r["quote"][:110]}')
