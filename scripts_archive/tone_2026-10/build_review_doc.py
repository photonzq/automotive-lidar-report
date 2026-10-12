"""Assemble the consolidated tone review from the per-part tables.

Reads the per-part review tables (NN_*.md), re-locates every quoted span in the report to get
current line numbers, tags each finding with the recurring pattern(s) it belongs to, and writes
the full listing after a hand-written header.

Usage: python build_review_doc.py <report.md> <tone_review_dir> <header.md> <notes.json> <out.md>
  notes.json: {"<line>|<quote prefix>": "reviewer's note to show in the Note column"}
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

report_path, review_dir, header_path, notes_path, out_path = sys.argv[1:6]
review_dir = Path(review_dir)
lines = Path(report_path).read_text(encoding="utf-8").split("\n")
notes = json.loads(Path(notes_path).read_text(encoding="utf-8"))

PARTS = [  # (first line, label) of the main report's parts, in order
    (1, "Front matter and §0 summary"), (218, "Part A (night vision)"), (823, "Part B (markets and programmes)"),
    (1783, "§C0–§C3 (physics and architectures)"), (2854, "§C3a–§C3c (companies)"), (3595, "§C4–§C6 (wavelength, receivers, scanning)"),
    (4797, "§C7–§C9 (FMCW, interference)"), (6136, "§C10 (OPA and resolution)"), (7248, "Part D (supply chain and geopolitics)"),
    (7987, "Part E (sensor debate)"), (9067, "Part F (outlook)"), (9436, "Part G (press hypotheses)"), (9780, "Appendices"),
]

PATTERNS = [  # tag, label, regex on the quoted text
    ("NAT", "nationality and geopolitics", r"Chinese|China|Beijing|Western|\bWest\b|American|\bUS\b|US-|adversar|truce|trade war|weapon|lever|chokepoint|sovereign|indigen|domestic|Japanese|European|blacklist|War Department|protected market|state support"),
    ("MET", "death, war, hype and contest metaphors", r"\bdead\b|died|\bdie\b|death|casualt|surviv|killed|fatal|hype|\bbust|\bboom|retreat|refuge|foothold|attrition|alive|collaps|cliff|brutal|attack|threat|\bwon\b|\bwin\b|winning|winner|\brace\b|\bbeat\b|\bbets?\b|staked|channel tax|handicap|rescue|harvest|feud|exotic|fire sales|hostage|fall off|hits FMCW|eating"),
    ("QUO", "scare quotes, 'really', 'actually', 'own', rhetorical questions", r"[\"“”]|\breally\b|\bactually\b|\bown\b|\?|silence"),
    ("PRO", "promise framing and 'claims' for vendor figures", r"promis|claim|pitch|\btell\b|track record|record on|billed"),
    ("INV", "investment and analyst vocabulary", r"tailwind|rally|narrative|fundamental|pure-play|balance sheet|valuation|\bcall\b|beneficiar|upside|catalyst|resilien|stories"),
    ("SPEC", "pejoratives for spec sheets and marketing", r"fine print|headline|spec-sheet|marketing|reality check|\btraps?\b|\bclean\b|garnish|\blines\b\"|more laser lines"),
    ("CERT", "certainty: unhedged forecasts, universal negatives, verdicts", r"obvious|certainly|\bnever\b|\bnone\b|nobody|no announced|\bwill\b|decisive|cannot|\bonly\b|every|failed|\bis the\b|verdict|years away|restart comes"),
]


def norm(s):
    """Fold curly quotes and drop bold markers, so a reviewer's plain quote still matches."""
    return s.replace("“", '"').replace("”", '"').replace("’", "'").replace("**", "")


norm_lines = [norm(ln) for ln in lines]


def where(span):
    span = norm(span)
    return [i for i, ln in enumerate(norm_lines, 1) if span in ln]


def pieces(quote):
    q = re.sub(r"^\d{3,5}:\s*", "", quote.strip())
    parts = re.split(r";\s+(?=\d{3,5}:\s)|\s*…\s*|\s*\(…\)\s*|\s+/\s+|;\s+", q)
    res = []
    for p in parts:
        p = re.sub(r"^\d{3,5}:\s*", "", p.strip()).strip("`").strip()
        p = re.sub(r"\s*\((bold|unbolded)[^)]*\)\s*$", "", p)
        if len(p) >= 8:
            res.append(p)
    return res


def part_of(line_no):
    label = PARTS[0][1]
    for start, lab in PARTS:
        if line_no >= start:
            label = lab
    return label


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ")


rows = []
for md in sorted(review_dir.glob("[0-9][0-9]_*.md")):
    doc = "main"
    header = None
    for raw in md.read_text(encoding="utf-8").split("\n"):
        if raw.startswith("## "):
            low = raw.lower()
            doc = "addendum" if "addendum" in low else "preaudit" if "pre-audit" in low else "main"
            header = None
            continue
        if not raw.startswith("|") or raw.startswith("|---"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if header is None:
            header = [h.lower() for h in cells]
            continue
        rec = dict(zip(header, cells))
        if "proposed replacement" in header:
            quote, repl = rec.get("exact quote", ""), rec.get("proposed replacement", "")
            sev, why = rec.get("severity", ""), rec.get("category", "") + "; " + rec.get("why", "")
        else:
            quote, repl = rec.get("quote", ""), rec.get("replacement", "")
            sev, why = rec.get("sev", ""), rec.get("cat / why", "")
        cited = rec.get("line", "")
        this_doc = "reading list" if cited.startswith("reading list") else doc
        found = sorted({n for p in pieces(quote) for n in where(p)}) if this_doc == "main" else []
        tags = [t for t, _, rx in PATTERNS if re.search(rx, quote, re.I)]
        key_line = found[0] if found else int(re.search(r"\d+", cited).group(0)) if re.search(r"\d+", cited) else 0
        note = ""
        for k, v in notes.items():
            kl, kq = k.split("|", 1)
            if (str(key_line) == kl or kl in cited) and quote.startswith(kq):
                note = v
        rows.append(dict(doc=this_doc, cited=cited, lines=found, key=key_line, quote=quote, repl=repl,
                         sev=sev.lower().strip(), why=why, tags=tags, note=note))

out = [Path(header_path).read_text(encoding="utf-8").rstrip(), ""]

main_rows = [r for r in rows if r["doc"] == "main"]
sev_count = Counter(r["sev"] for r in main_rows)
out.append("## 4. Every finding in the main report, in report order\n")
out.append(f"{len(main_rows)} findings: {sev_count['high']} high, {sev_count['medium']} medium, {sev_count['low']} low. "
           "Line numbers are the current ones, from re-locating each quote in the report; where a phrase recurs, "
           "all its lines are given. In the last column, ★H marks an item also in Part 3 and ★F one also in Part 2. "
           "Where two reviewers proposed different wording for the same phrase (for example the §C3a title, which recurs "
           "at 27, 48, 144 and 2854), one wording is used throughout, and the final edit list is reviewed before "
           "anything is applied. Tags: " + "; ".join(f"**{t}** {lab}" for t, lab, _ in PATTERNS) + ".\n")
tag_count = Counter(t for r in main_rows for t in r["tags"])
out.append("| Pattern | Findings | of which high | medium | low |")
out.append("|---|---|---|---|---|")
for t, lab, _ in PATTERNS:
    sub = [r for r in main_rows if t in r["tags"]]
    c = Counter(r["sev"] for r in sub)
    out.append(f"| **{t}** {lab} | {len(sub)} | {c['high']} | {c['medium']} | {c['low']} |")
untagged = [r for r in main_rows if not r["tags"]]
c = Counter(r["sev"] for r in untagged)
out.append(f"| other | {len(untagged)} | {c['high']} | {c['medium']} | {c['low']} |\n")

by_part = defaultdict(list)
for r in main_rows:
    by_part[part_of(r["key"])].append(r)
order = {"high": 0, "medium": 1, "low": 2}
for _, lab in PARTS:
    sub = sorted(by_part.get(lab, []), key=lambda r: (r["key"], order.get(r["sev"], 3)))
    if not sub:
        continue
    out.append(f"### {lab}\n")
    out.append("| Line | Sev | Tags | Current text | Proposed text | Why (reviewer) | Note |")
    out.append("|---|---|---|---|---|---|---|")
    for r in sub:
        ln = ", ".join(str(x) for x in r["lines"]) or r["cited"]
        out.append(f"| {ln} | {r['sev']} | {' '.join(r['tags'])} | {esc(r['quote'])} | {esc(r['repl'])} | {esc(r['why'])} | {esc(r['note'])} |")
    out.append("")

for doc, title in [("reading list", "## 5. Reading list"), ("addendum", "## 6. Addendum"),
                   ("preaudit", "## 7. Pre-audit draft")]:
    sub = [r for r in rows if r["doc"] == doc]
    if not sub:
        continue
    c = Counter(r["sev"] for r in sub)
    out.append(f"{title}\n\n{len(sub)} findings: {c['high']} high, {c['medium']} medium, {c['low']} low. Line numbers are the file's own.\n")
    out.append("| Line | Sev | Current text | Proposed text | Why (reviewer) | Note |")
    out.append("|---|---|---|---|---|---|")
    for r in sub:
        out.append(f"| {esc(r['cited'])} | {r['sev']} | {esc(r['quote'])} | {esc(r['repl'])} | {esc(r['why'])} | {esc(r['note'])} |")
    out.append("")

Path(out_path).write_text("\n".join(out) + "\n", encoding="utf-8")
print("rows:", Counter(r["doc"] for r in rows), "main sev:", dict(sev_count))
print("main rows without a located line:", [r["cited"] for r in main_rows if not r["lines"]])
print("tags:", dict(tag_count), "untagged:", len(untagged))
