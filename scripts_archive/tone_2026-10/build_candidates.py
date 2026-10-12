"""Turn the reviewed findings into candidate edit pairs, following the author's choices.

Rules (decided 10 Oct 2026):
  - every high-severity and factual item is applied (wording from Parts 2 and 3 of the review);
  - findings whose only problem is a death/war/hype/contest metaphor (tag MET alone) are skipped,
    except where OVERRIDES applies a non-metaphor part;
  - findings the review marked as not to apply, or as a judgement on technical meaning, are skipped;
  - everything else is applied with the reviewer's wording unless OVERRIDES gives other text.

Writes candidates.json (one entry per edit: id, line, sev, old, new, why) and candidates_context.md, which
shows each edit inside its line so it can be read in context.

Usage: python build_candidates.py <report.md> <main_rows.json> <overrides.py>
"""
import json
import re
import sys
from pathlib import Path

report = Path(sys.argv[1]).read_text(encoding="utf-8")
lines = report.split("\n")
rows = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
ns = {}
exec(Path(sys.argv[3]).read_text(encoding="utf-8"), ns)
OVERRIDES, SKIP_NOTES, EXTRA = ns["OVERRIDES"], ns["SKIP_NOTES"], ns["EXTRA"]


def match_override(r):
    for (ln, prefix), v in OVERRIDES.items():
        if (ln == r["key"] or ln in r["lines"]) and r["quote"].startswith(prefix):
            return v
    return None


cands, skipped = [], []
for i, r in enumerate(rows):
    ov = match_override(r)
    note = r.get("note", "")
    if ov is not None:
        if ov == "skip":
            skipped.append((r, "override: skip"))
            continue
        pairs = ov  # list of (old, new)
    elif any(s in note for s in SKIP_NOTES):
        skipped.append((r, "note: " + note[:60]))
        continue
    elif r["tags"] == ["MET"]:
        skipped.append((r, "metaphor only"))
        continue
    else:
        pairs = [(r["quote"], r["repl"])]
    for k, (old, new) in enumerate(pairs):
        cands.append(dict(id=f"T{r['key']:05d}_{i}_{k}", line=r["key"], sev=r["sev"], tags=r["tags"],
                          old=old, new=new, why=r["why"][:160]))
for e in EXTRA:
    cands.append(dict(id=e["id"], line=e["line"], sev=e.get("sev", "extra"), tags=["EXTRA"], old=e["old"],
                      new=e["new"], why=e.get("why", ""), expect=e.get("count", 1)))

# Check: each old must occur in the report (count reported); show the edit in context.
out = []
problems = []
for c in sorted(cands, key=lambda c: (c["line"], c["id"])):
    n = report.count(c["old"])
    c["count"] = n
    c.setdefault("expect", 1)
    if n != c["expect"]:
        problems.append(f'{c["id"]} L{c["line"]}: old occurs {n}× | {c["old"][:90]}')
    ln_no = next((j for j, ln in enumerate(lines, 1) if c["old"] in ln), None)
    if ln_no is None:
        ctx_b = ctx_a = "(old spans lines or not found)"
    else:
        ln = lines[ln_no - 1]
        k = ln.find(c["old"])
        a, b = max(0, k - 160), min(len(ln), k + len(c["old"]) + 160)
        ctx_b = ln[a:b]
        ctx_a = ln[a:k] + "⟦" + c["new"] + "⟧" + ln[k + len(c["old"]):b]
    out.append(f'### {c["id"]} (line {ln_no}, {c["sev"]}, {" ".join(c["tags"])})\n- before: {ctx_b}\n- after:  {ctx_a}\n')

Path("candidates.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
Path("candidates_context.md").write_text("\n".join(out), encoding="utf-8")
Path("candidates_skipped.md").write_text("\n".join(f'- L{r["key"]} [{r["sev"]}] {why}: {r["quote"][:120]}'
                                                  for r, why in skipped), encoding="utf-8")
print(len(cands), "candidate edits;", len(skipped), "skipped")
print("\n".join(problems) or "all olds unique")
