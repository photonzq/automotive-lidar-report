"""List "Eq. (N)" citations in the pre-conversion report that look like citations of an outside paper's equation:
inside an evidence tag such as [I, ...] or [P, ...], or within 80 characters after "et al.", "Supplementary",
"SI ", "datasheet" or "paper". Usage: outside_eq_refs.py <old report.md>"""
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
for m in re.finditer(r"Eqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*", text):
    a, b = m.start(), m.end()
    before = text[max(0, a - 80):a]
    # inside an evidence tag: the last '[' before the match is not closed before it
    lb = text.rfind("[", max(0, a - 300), a)
    in_tag = lb != -1 and "]" not in text[lb:a] and re.match(r"\[(I|P|T|S|E|U)\b", text[lb:lb + 3])
    cue = re.search(r"et al\.|Supplementary|\bSI\b|datasheet|paper|their|Table|Fig\.", before)
    if in_tag or cue:
        line = text.count("\n", 0, a) + 1
        print(f"{line}: ...{text[max(0, a - 90):b + 20]!r}")
