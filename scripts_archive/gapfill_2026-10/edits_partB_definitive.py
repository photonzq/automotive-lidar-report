"""Old->new pairs that turn the reviewer-voice hedges of Part B ("not verified", "not confirmed",
"in this review", "verify on the installed vehicle") into definitive statements (5 Oct 2026), plus the
Appendix 1 items that take over what stays unknown. Requested by the author on 5 Oct 2026, after the §B8
note bullets were integrated (see edits_b8_integration.py).

Each pair is anchored on content: the line is found by its unique start, and the whole line is the
"old" text. The pairs are written as JSON to be applied in a separate pass;
a dry-run copy with the pairs applied is written for checking and for a test build. The script does
not write the report.

Usage:
    python edits_partB_definitive.py --report <report.md> --out-dir <dir> --expect <sha256 prefix>
                                     [--texts <module defining EDITS>] [--name <output stem>]
(default texts: partB_definitive_texts; the follow-ups use --texts followups_texts --name followups)
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import importlib

ap = argparse.ArgumentParser()
ap.add_argument("--report", required=True)
ap.add_argument("--out-dir", required=True)
ap.add_argument("--expect", required=True)
ap.add_argument("--texts", default="partB_definitive_texts", help="module that defines EDITS")
ap.add_argument("--name", default="partB_definitive", help="stem of the output JSON and dry-run files")
args = ap.parse_args()
EDITS = importlib.import_module(args.texts).EDITS  # (id, unique line start, change)

RP = Path(args.report)
OUT = Path(args.out_dir)
raw = RP.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
assert h0.startswith(args.expect), h0
text0 = raw.decode("utf-8")
L = text0.split("\n")

pairs = []
for eid, start, new in EDITS:
    hits = [i for i, x in enumerate(L) if x.startswith(start)]
    assert len(hits) == 1, (eid, hits)
    line = L[hits[0]]
    if isinstance(new, dict):  # {"block": k, "text": ...}: replace the line and the k-1 lines after it
        old = "\n".join(L[hits[0]:hits[0] + new["block"]])
        new_line = new["text"]
    elif isinstance(new, tuple):  # ("sub", old_fragment, new_fragment): replace a fragment inside the line
        _, frag_old, frag_new = new
        assert line.count(frag_old) == 1, (eid, "fragment not unique in line")
        new_line = line.replace(frag_old, frag_new)
        old = line
    elif isinstance(new, list):  # ("after", [lines]): keep the line, insert new lines after it
        old = line
        new_line = "\n".join([line] + new)
    else:
        old = line if new is not None else line + "\n"
        new_line = new if new is not None else ""
    assert text0.count(old) == 1, (eid, text0.count(old))
    pairs.append({"id": eid, "old": old, "new": new_line})

spans = sorted((text0.index(p["old"]), text0.index(p["old"]) + len(p["old"]), p["id"]) for p in pairs)
for (a0, a1, ia), (b0, b1, ib) in zip(spans, spans[1:]):
    assert a1 <= b0, ("overlap", ia, ib)

text = text0
for p in pairs:
    assert text.count(p["old"]) == 1, p["id"]
    text = text.replace(p["old"], p["new"], 1)

# hygiene
assert "\t" not in text
assert '\\"' not in "".join(p["new"] for p in pairs), "backslash-quote in new text"
old_lines, new_lines = set(text0.split("\n")), text.split("\n")
changed = [l for l in new_lines if l not in old_lines]
for l in changed:
    if len(re.findall(r"(?<!\\)\$", l)) % 2:
        print("ODD $ in:", l[:120])
for w in ["corrected", "updated", "revised", "added", "now confirmed", "verification", "verified", "in this review"]:
    a, b = text0.lower().count(w.lower()), text.lower().count(w.lower())
    if a != b:
        print(f"WORD COUNT CHANGE {w!r}: {a} -> {b}")
for i, l in enumerate(new_lines[1:], 1):
    prev = new_lines[i - 1]
    if l.startswith("**") and (prev.startswith("- ") or re.match(r"\d+\. ", prev)):
        print("BOLD PARAGRAPH GLUED TO A LIST ITEM at line", i + 1, l[:60])


def pipes(line):
    return len(re.findall(r"(?<!\\)\|", line))


block, bad = [], 0
for i, l in enumerate(new_lines + [""]):
    if l.startswith("|"):
        block.append((i, l))
    elif block:
        n0 = pipes(block[0][1])
        for j, r in block:
            if pipes(r) != n0:
                bad += 1
                print(f"TABLE ROW MISMATCH at line {j + 1}: {pipes(r)} vs {n0}")
        block = []
print(f"pairs {len(pairs)}; changed lines {len(changed)}; table mismatches {bad}")

OUT.mkdir(parents=True, exist_ok=True)
js = json.dumps(pairs, ensure_ascii=False, indent=1)
(OUT / f"{args.name}_edits.json").write_bytes(js.encode("utf-8"))
(OUT / f"report_{args.name}_dry.md").write_bytes(text.encode("utf-8"))
print("source sha", h0[:12], "| dry-run sha", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12],
      "| json sha", hashlib.sha256(js.encode("utf-8")).hexdigest()[:12])
