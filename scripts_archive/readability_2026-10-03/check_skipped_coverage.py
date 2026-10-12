"""For every cross_section item that a Round 2 agent skipped, check whether the quoted old text survives the merge.

The agents quote the text they would change as 'Old: '…' New: '…'' or 'Replace '…' with '…''. Each quoted old
string is looked up in the merged copy (merge_apply.py --dry --out=…): if it is gone, another list covered it;
if it is still there, the item is open. Items without a quotable old string are listed for reading by hand.
Usage: python check_skipped_coverage.py <merged copy.md> edits/round2/*.json
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
merged = Path(sys.argv[1]).read_text(encoding="utf-8")
QUOTES = (re.compile(r"(?:Old:|Replace)\s*'(.+?)'\s*(?:New:|with)", re.S),
          re.compile(r"Exact text:\s*«(.+?)»", re.S),
          re.compile(r"Exact text:\s*(?!«)(.+?)\s*→\s*proposed:", re.S),
          re.compile(r"Exact text:\s*'(.+?)'", re.S))
for arg in sys.argv[2:]:
    data = json.loads(Path(arg).read_text(encoding="utf-8"))
    if isinstance(data, list):
        continue
    for s in data.get("skipped", []):
        if "cross" not in s.get("kind", ""):
            continue
        detail = s.get("detail", "")
        olds = [o for q in QUOTES for o in q.findall(detail)]
        where = s.get("location", "")[:90]
        if not olds:
            print(f"[read] {Path(arg).stem} @ {where}\n       {detail[:300]}\n")
            continue
        for o in olds:
            core = o.strip().strip("…").strip()
            # a quote may abbreviate with an ellipsis; test the longest piece
            piece = max(core.split("…"), key=len).strip()
            state = "OPEN" if piece and piece in merged else "covered"
            print(f"[{state}] {Path(arg).stem} @ {where}\n       old: {piece[:200]}\n")
