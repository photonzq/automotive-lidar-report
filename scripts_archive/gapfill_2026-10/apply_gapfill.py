"""Apply the October 2026 gap-filling edits (edits_gapfill.py, then edits_gapfill2.py) to the report, hash-guarded.

Usage (from this folder):
  python apply_gapfill.py --snapshot <snapshot.md> --out-dir <dir> --dry   # dry run: write the result to <dir>
  python apply_gapfill.py --snapshot <snapshot.md> --out-dir <dir>         # write the live report
  add --edits edits_gapfill2 for the second batch

The edits are written against <snapshot.md> (a copy of the report taken before the research round).
Equation numbers in the edits are snapshot numbers; they are mapped to the live file by matching
equation bodies, so a renumbering in the meantime is harmless.  New equations, if any, use
placeholder tags >= 9000 and are numbered in order of appearance at the end.

Edit kinds (see edits_gapfill.py):
  ("L", prefix, new)            replace the unique line starting with prefix
  ("X", exact, new)             replace the unique line equal to exact
  ("S", prefix, old, new)       replace old (once) inside the unique line starting with prefix
  ("B", start, end, text)       replace lines [start, end) (end line kept)
  ("I", prefix, text)           insert text before the unique line starting with prefix
  ("A", prefix, text)           insert text after the unique line starting with prefix
"""
import argparse
import hashlib
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

RP = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
ap = argparse.ArgumentParser()
ap.add_argument("--snapshot", required=True)
ap.add_argument("--out-dir", required=True)
ap.add_argument("--dry", action="store_true")
ap.add_argument("--target", default=None)
ap.add_argument("--edits", default="edits_gapfill", help="edit-list module (edits_gapfill or edits_gapfill2)")
args = ap.parse_args()
os.environ["GAPFILL_SNAPSHOT"] = args.snapshot  # read by edits modules that derive edits from the snapshot
E = __import__(args.edits).E
OUT = Path(args.out_dir)
TARGET = Path(args.target) if args.target else RP

raw = TARGET.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text0 = raw.decode("utf-8")
assert "\r\n" not in text0, "CRLF in target"
snap = Path(args.snapshot).read_text(encoding="utf-8")
print(f"target {TARGET.name}: {len(raw)} bytes, sha {h0[:12]}")

EQ = re.compile(r"\$\$(.+?)\\tag\{(\d+)\}\s*\$\$", re.S)
TAG = re.compile(r"\\tag\{(\d+)\}")
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")


def bodies(t):
    out = {}
    for m in EQ.finditer(t):
        out.setdefault(re.sub(r"\s+", " ", m.group(1)).strip(), []).append(int(m.group(2)))
    return out


bs, bt = bodies(snap), bodies(text0)
M, missing = {}, []
for body, tags in bs.items():
    if body in bt and len(bt[body]) == len(tags):
        M.update(dict(zip(tags, bt[body])))
    else:
        missing.extend(tags)
n_snap = len(TAG.findall(snap))
assert not missing, ("snapshot equations not found in target", sorted(missing))
assert len(M) == n_snap, (len(M), n_snap)
shift = {k: v for k, v in M.items() if k != v}
print(f"equation map: {n_snap} snapshot tags, {len(shift)} renumbered in the target")


def remap(s):
    def tag(m):
        n = int(m.group(1))
        return m.group(0) if n >= 9000 else "\\tag{%d}" % M[n]

    def ref(m):
        return re.sub(r"\((\d+)\)", lambda q: "(%d)" % (int(q.group(1)) if int(q.group(1)) >= 9000
                                                         else M[int(q.group(1))]), m.group(0))
    return REF.sub(ref, TAG.sub(tag, s))


text = text0
problems = []


def find(lines, pred, what):
    hits = [i for i, line in enumerate(lines) if pred(line)]
    if len(hits) != 1:
        problems.append((what[:90], len(hits)))
        return None
    return hits[0]


def as_lines(new):
    nl = new.split("\n")
    if new.endswith("\n"):
        nl = nl[:-1]
    return nl


for k, e in enumerate(E):
    lines = text.split("\n")
    kind = e[0]
    if kind == "L":
        pre, new = remap(e[1]), remap(e[2])
        i = find(lines, lambda l: l.startswith(pre), f"#{k} L {pre}")
        if i is not None:
            lines[i] = new
    elif kind == "X":
        old, new = remap(e[1]), remap(e[2])
        i = find(lines, lambda l: l == old, f"#{k} X {old}")
        if i is not None:
            lines[i] = new
    elif kind == "S":
        pre, old, new = remap(e[1]), remap(e[2]), remap(e[3])
        i = find(lines, lambda l: l.startswith(pre), f"#{k} S {pre}")
        if i is not None:
            if lines[i].count(old) != 1:
                problems.append((f"#{k} S sub {old[:70]}", lines[i].count(old)))
            else:
                lines[i] = lines[i].replace(old, new)
    elif kind == "B":
        a, b, new = remap(e[1]), remap(e[2]), remap(e[3])
        i = find(lines, lambda l: l.startswith(a), f"#{k} B start {a}")
        j = find(lines, lambda l: l.startswith(b), f"#{k} B end {b}")
        if i is not None and j is not None:
            if not i < j:
                problems.append((f"#{k} B order", i, j))
            else:
                lines[i:j] = as_lines(new)
    elif kind in ("I", "A"):
        pre, new = remap(e[1]), remap(e[2])
        i = find(lines, lambda l: l.startswith(pre), f"#{k} {kind} {pre}")
        if i is not None:
            at = i if kind == "I" else i + 1
            lines[at:at] = as_lines(new)
    else:
        raise ValueError(kind)
    text = "\n".join(lines)

if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  ", p)
    sys.exit(1)
print(f"applied {len(E)} edits")

# global renumbering (only does something if placeholder tags >= 9000 were inserted)
tags = [int(x) for x in TAG.findall(text)]
assert len(tags) == len(set(tags)), "duplicate tags"
mapping = {t: k + 1 for k, t in enumerate(tags)}
refs_before = [int(x) for m in REF.finditer(text) for x in re.findall(r"\((\d+)\)", m.group(0))]
bad = sorted({n for n in refs_before if n not in mapping})
assert not bad, ("dangling refs", bad)
text = TAG.sub(lambda m: "\\tag{%d}" % mapping[int(m.group(1))], text)
text = REF.sub(lambda m: re.sub(r"\((\d+)\)", lambda q: "(%d)" % mapping[int(q.group(1))], m.group(0)), text)
tags2 = [int(x) for x in TAG.findall(text)]
assert tags2 == list(range(1, len(tags2) + 1))
refs_after = [int(x) for m in REF.finditer(text) for x in re.findall(r"\((\d+)\)", m.group(0))]
assert len(refs_after) == len(refs_before) and all(1 <= n <= len(tags2) for n in refs_after)
print(f"tags {len(tags)} -> sequential 1..{len(tags2)}; refs {len(refs_after)}")

# hygiene
assert "\t" not in text
old_lines, new_lines = set(text0.split("\n")), text.split("\n")
changed = [l for l in new_lines if l not in old_lines]
for l in changed:
    if len(re.findall(r"(?<!\\)\$", l)) % 2:
        print("ODD $ in:", l[:120])
for w in ["corrected", "updated", "revised", "added", "now confirmed"]:
    if text0.lower().count(w.lower()) != text.lower().count(w.lower()):
        print(f"WORD COUNT CHANGE {w!r}: {text0.lower().count(w.lower())} -> {text.lower().count(w.lower())}")


def tables(t):
    out, cur = [], []
    for i, line in enumerate(t.split("\n")):
        if line.startswith("|"):
            cur.append((i, line))
        elif cur:
            out.append(cur)
            cur = []
    return out


def pipes(line):
    return len(re.findall(r"(?<!\\)\|", line))


bad_tables = 0
for tb in tables(text):
    n0 = pipes(tb[0][1])
    for i, line in tb:
        if pipes(line) != n0:
            bad_tables += 1
            print(f"TABLE ROW MISMATCH at line {i + 1}: {pipes(line)} vs {n0}: {line[:100]}")
print(f"changed lines: {len(changed)}; table mismatches: {bad_tables}")

out = text.encode("utf-8")
OUT.mkdir(parents=True, exist_ok=True)
if args.dry:
    (OUT / "report_gapfill_dry.md").write_bytes(out)
    print("dry run written:", OUT / "report_gapfill_dry.md", len(out), "bytes")
    sys.exit(0)
if hashlib.sha256(RP.read_bytes()).hexdigest() != h0:
    print("ABORT: report changed during processing")
    sys.exit(2)
RP.write_bytes(out)
(OUT / "report_after_gapfill.md").write_bytes(out)
print("written", len(raw), "->", len(out), "bytes")
