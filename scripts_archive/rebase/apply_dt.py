"""Apply the self-consistent re-baseline (edits.py) to the report, hash-guarded.

  python apply_rebase.py --dry                 # apply to the live report in memory, write result to a scratch folder
  python apply_rebase.py --target <file> --dry # validate anchors against another file (e.g. the snapshot)
  python apply_rebase.py                       # write the live report (aborts if it changed meanwhile)

Edits are written against the 12:04 snapshot's equation numbers; they are mapped to the target's
numbers by matching equation bodies, then everything is renumbered in order of appearance.
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from edits_dt import E  # noqa: E402

RP = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SNAP = HERE / "report_after_fix2.md"
DRY = "--dry" in sys.argv
TARGET = Path(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else RP

raw = TARGET.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text0 = raw.decode("utf-8")
assert "\r\n" not in text0, "CRLF in target"
snap = SNAP.read_text(encoding="utf-8")
print(f"target {TARGET.name}: {len(raw)} bytes, sha {h0[:12]}")

EQ = re.compile(r"\$\$(.+?)\\tag\{(\d+)\}\s*\$\$", re.S)
TAG = re.compile(r"\\tag\{(\d+)\}")
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")


def bodies(t):
    out = {}
    for m in EQ.finditer(t):
        out.setdefault(re.sub(r"\s+", " ", m.group(1)).strip(), []).append(int(m.group(2)))
    return out


# ---------------------------------------------------------------- snapshot -> target equation map
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
print(f"equation map: {n_snap} snapshot tags, {len(shift)} renumbered in the target"
      + (f" (e.g. {list(shift.items())[:4]})" if shift else ""))


def remap(s):
    def tag(m):
        n = int(m.group(1))
        return m.group(0) if n >= 9000 else "\\tag{%d}" % M[n]

    def ref(m):
        return re.sub(r"\((\d+)\)", lambda q: "(%d)" % (int(q.group(1)) if int(q.group(1)) >= 9000
                                                         else M[int(q.group(1))]), m.group(0))
    return REF.sub(ref, TAG.sub(tag, s))


# ---------------------------------------------------------------- apply edits
text = text0
problems = []


def find(lines, pred, what):
    hits = [i for i, l in enumerate(lines) if pred(l)]
    if len(hits) != 1:
        problems.append((what[:90], len(hits)))
        return None
    return hits[0]


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
                nl = new.split("\n")
                if new.endswith("\n"):
                    nl = nl[:-1]
                lines[i:j] = nl
    else:
        raise ValueError(kind)
    text = "\n".join(lines)

if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  ", p)
    sys.exit(1)
print(f"applied {len(E)} edits")

# ---------------------------------------------------------------- global renumbering
tags = [int(x) for x in TAG.findall(text)]
assert len(tags) == len(set(tags)), "duplicate tags"
new_tags = [t for t in tags if t >= 9000]
assert new_tags == [], new_tags
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

# ---------------------------------------------------------------- hygiene
assert "\t" not in text
old_lines, new_lines = set(text0.split("\n")), text.split("\n")
changed = [l for l in new_lines if l not in old_lines]
for l in changed:
    if len(re.findall(r"(?<!\\)\$", l)) % 2:
        print("ODD $ in:", l[:120])
for w in ["corrected", "updated", "revised", "added"]:
    if text0.count(w) != text.count(w):
        print(f"WORD COUNT CHANGE {w!r}: {text0.count(w)} -> {text.count(w)}")


def tables(t):
    out, cur = [], []
    for i, l in enumerate(t.split("\n")):
        if l.startswith("|"):
            cur.append((i, l))
        elif cur:
            out.append(cur)
            cur = []
    return out


def pipes(l):
    return len(re.findall(r"(?<!\\)\|", l))


bad_tables = 0
for tb in tables(text):
    n0 = pipes(tb[0][1])
    for i, l in tb:
        if pipes(l) != n0:
            bad_tables += 1
            print(f"TABLE ROW MISMATCH at line {i + 1}: {pipes(l)} vs {n0}: {l[:100]}")
print(f"changed lines: {len(changed)}; table mismatches: {bad_tables}")
for s in ["b=2.2$", "b = 2.2", "n_{\\rm th}=13$", "4,430", "4{,}430", "4,455", "0.56 µJ", "2.6 µJ", "≈6×",
          "45–130", "≈46 W", "≈41 W", "≈245 mW", "generous", "10–20 mW", "5–10%"]:
    hits = [i + 1 for i, l in enumerate(new_lines) if s in l]
    if hits:
        print(f"remaining {s!r}: lines {hits[:12]}")

out = text.encode("utf-8")
if DRY:
    (HERE / "report_dt_dry.md").write_bytes(out)
    print("dry run written:", HERE / "report_dt_dry.md", len(out), "bytes")
    sys.exit(0)
now = RP.read_bytes()
if hashlib.sha256(now).hexdigest() != h0:
    print("ABORT: report changed during processing")
    sys.exit(2)
RP.write_bytes(out)
(HERE / "report_after_dt.md").write_bytes(out)
print("written", len(raw), "->", len(out), "bytes")
