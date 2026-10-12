"""Renumber the report's display-equation tags sequentially and remap every equation reference.

Run after duplicated displays have been replaced by references, so that some tags are missing. Every remaining
\\tag{N} gets its position in document order; every reference "Eq. (N)", "Eqs. (N)–(M)", "Eqs. (N), (M) and (K)"
(the pattern of scripts_archive/rebase/check_refs.py) is remapped. A reference to a removed tag must be redirected
with --redirect OLD=KEPT (both old numbers), for example 162=11.
Checks before writing: every reference resolves; the new tags are 1..n; the report hash is unchanged since reading.
--allow-reorder accepts tags that are no longer in increasing order (after a move of numbered material); each tag
still gets its position in document order. --file=<path> reads another copy instead of the report (dry runs only).
Usage: python renumber_equations.py [--dry] [--allow-reorder] [--file=<copy.md>] [--redirect 162=11,170=11,...]
"""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
TAG = re.compile(r"\\tag\{(\d+)\}")
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
NUM = re.compile(r"\((\d+)\)")

dry = "--dry" in sys.argv
redirect = {}
for arg in sys.argv[1:]:
    if arg.startswith("--redirect"):
        spec = arg.split("=", 1)[1] if arg.startswith("--redirect=") else sys.argv[sys.argv.index(arg) + 1]
        for pair in spec.split(","):
            a, b = pair.split("=")
            redirect[int(a)] = int(b)

reorder = "--allow-reorder" in sys.argv
copy = next((a[7:] for a in sys.argv[1:] if a.startswith("--file=")), None)
if copy:
    assert dry, "--file= is for dry runs only"
    REPORT = Path(copy)
raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
old_tags = [int(m.group(1)) for m in TAG.finditer(text)]
assert len(old_tags) == len(set(old_tags)), "duplicate tag numbers"
if old_tags != sorted(old_tags):
    moved = [(a, b) for a, b in zip(old_tags, old_tags[1:]) if b < a]
    assert reorder, f"tags not in increasing order (first descents {moved[:5]}); use --allow-reorder after a move"
    print("tags out of order at", ", ".join(f"{a}->{b}" for a, b in moved), "(allowed)")
new_of = {old: i + 1 for i, old in enumerate(old_tags)}
for a, b in redirect.items():
    assert a not in new_of, f"redirected tag {a} still exists"
    assert b in new_of, f"redirect target {b} does not exist"
    new_of[a] = new_of[b]

problems = []


def remap_ref(m):
    s = m.group(0)

    def one(n):
        k = int(n.group(1))
        if k not in new_of:
            problems.append(f"reference to missing tag {k}: {s!r}")
            return n.group(0)
        return f"({new_of[k]})"
    return NUM.sub(one, s)


out = REF.sub(remap_ref, text)
out = TAG.sub(lambda m: f"\\tag{{{new_of[int(m.group(1))]}}}", out)
tags1 = [int(x) for x in TAG.findall(out)]
if tags1 != list(range(1, len(tags1) + 1)):
    problems.append("new tags are not sequential")
changed = sorted({(o, n) for o, n in new_of.items() if o != n})
print(f"{len(old_tags)} tags -> {len(tags1)}; {len(changed)} numbers change; redirects {redirect}")
print("map (old -> new) for changed numbers:", ", ".join(f"{o}->{n}" for o, n in changed[:400]))
if problems:
    for p in problems:
        print("PROBLEM", p)
    sys.exit(1)
if dry:
    print("dry run OK; nothing written")
    sys.exit(0)
if hashlib.sha256(REPORT.read_bytes()).hexdigest() != h0:
    sys.exit("report changed after it was read; nothing written")
REPORT.write_bytes(out.encode("utf-8"))
print("written; new sha", hashlib.sha256(out.encode("utf-8")).hexdigest()[:12])
