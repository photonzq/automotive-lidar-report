"""Print a word-level diff of every edit in one or more edit lists, for a human read-through before merging.

Unchanged runs longer than 12 words are shortened to their first and last 4 words. Deleted words are shown as
[-...-], inserted words as {+...+}. The finding and the reason given by the agent are printed above each diff.
Usage: python show_edit_diffs.py edits/a.json [more.json ...] > out.txt
"""
import difflib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
TOKEN = re.compile(r"\s+|[^\s]+")


def words(s):
    return TOKEN.findall(s)


def shorten(toks):
    w = [t for t in toks if not t.isspace()]
    if len(w) <= 12:
        return "".join(toks)
    return " ".join(w[:4]) + " … " + " ".join(w[-4:])


for path in sys.argv[1:]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    edits = data if isinstance(data, list) else data.get("edits", [])
    print(f"=================== {Path(path).name}: {len(edits)} edits")
    for e in edits:
        a, b = words(e["old"]), words(e["new"])
        out = []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op == "equal":
                out.append(shorten(a[i1:i2]))
            if op in ("replace", "delete"):
                out.append("[-" + "".join(a[i1:i2]).strip() + "-]")
            if op in ("replace", "insert"):
                out.append("{+" + "".join(b[j1:j2]).strip() + "+}")
        print(f"\n--- {e.get('id', '?')} | {e.get('finding', '')}")
        if e.get("why"):
            print(f"    why: {e['why']}")
        print("    " + "".join(out).replace("\n", "\n    "))
    skipped = [] if isinstance(data, list) else data.get("skipped", [])
    if skipped:
        print(f"\n=== skipped ({len(skipped)})")
        for s in skipped:
            print(f"  [{s.get('kind')}] {s.get('finding')} @ {s.get('location')}: {s.get('detail')}")
