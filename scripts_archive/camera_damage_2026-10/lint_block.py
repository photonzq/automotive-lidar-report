"""Lint the new text of an edit list: per-line $ parity, doubled spaces, first/second-person pronouns, and print it."""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
DOLLAR = re.compile(r"(?<!\\)\$")
for path in sys.argv[1:]:
    d = json.load(open(path, encoding="utf-8"))
    for e in d["edits"]:
        new = e["new"]
        print("=====", e["id"], "lines", len(new.split("\n")), "chars", len(new))
        for i, l in enumerate(new.split("\n"), 1):
            flags = []
            if len(DOLLAR.findall(l)) % 2:
                flags.append("ODD$")
            if "  " in l.strip():
                flags.append("double-space")
            if re.search(r"\b(I|we|We|you|You|my|our)\b", l):
                flags.append("pronoun")
            if flags:
                print("  FLAG", i, flags, l[:100])
        if "--print" in sys.argv:
            print(new)
