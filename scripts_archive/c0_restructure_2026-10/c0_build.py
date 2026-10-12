"""Build a working copy of the report with §C0 restructured (equations not yet renumbered).

1. Assemble the new §C0 from the plan (c0_plan_a/b/c) and the old section; list old lines not carried over.
2. Remap the references to §C0 subsections in the rest of the report (old -> new numbering, with per-line overrides).
3. Rename Figures C0.10a-d to C0.1-C0.4 everywhere.
4. Report every "subsection" reference inside the new §C0 and any left-over old-style reference.
Usage: python c0_build.py <report.md> <expected sha256 prefix> <working copy out> <new_c0 out>
"""
import hashlib
import re
import sys
from pathlib import Path

from c0_lib import assemble
from c0_plan_a import PLAN_A
from c0_plan_b import PLAN_B
from c0_plan_c import PLAN_C

src, expect, out_work, out_c0 = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
raw = src.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expect), f"report sha {sha[:12]} is not {expect}"
crlf = b"\r\n" in raw
text = raw.decode("utf-8").replace("\r\n", "\n")
lines = text.split("\n")
c0 = next(i for i, l in enumerate(lines) if l.startswith("## C0. Physics primer"))
c1 = next(i for i, l in enumerate(lines) if l.startswith("## C1. Taxonomy"))
old = lines[c0:c1]

# ---- 1. assemble
new_c0, used = assemble(PLAN_A + PLAN_B + PLAN_C, old)
covered = set()
for a, b in used:
    covered.update(range(a, b + 1))
dropped = [(i, l) for i, l in enumerate(old) if l.strip() and i not in covered]
print(f"old §C0: {len(old)} lines; new §C0: {len(new_c0.splitlines())} lines; old non-blank lines not copied: {len(dropped)}")
for i, l in dropped:
    print(f"   not copied, report line {c0 + i + 1}: {l[:150]}")

# ---- 2. remap references to §C0 subsections outside §C0 (report line numbers are 1-based, before splicing)
DEFAULT = {"1": "1.1", "2": "1.3", "3": "2.1", "4": "1.4", "5": "4.2", "6": "4.1", "7": "4.3", "8": "3.3", "9": "1.2",
           "10.1": "3.1", "10.2": "3.2", "10.3": "4.3", "10.4": "5.1", "10.5": "5.2", "10.6": "5.4", "10.7": "5.5",
           "10.8": "6.1", "10.9": "6.2"}
# (line, old number) -> new number for every occurrence on that line; (line, old number, k) for the k-th occurrence only
OVERRIDE = {(356, "1"): "3.1", (358, "1"): "3.1", (3441, "1"): "5.2", (3449, "1"): "5.2",
            (8286, "8"): "5.4", (8292, "8"): "5.4",
            (3442, "10"): "4.3", (6793, "10"): "5.1",
            (6399, "10.1"): "3.2", (6431, "10.1", 0): "4.3",
            (3446, "10.3"): "4.2", (4666, "10.3"): "4.2", (5037, "10.3"): "4.2", (5112, "10.3"): "4.2",
            (5116, "10.3"): "4.2", (6065, "10.3"): "4.2"}
REF = re.compile(r"§C0 subsection (\d+(?:\.\d+)?)(?![\d.]*\d)")
changes = []
for idx in list(range(0, c0)) + list(range(c1, len(lines))):
    n = idx + 1
    seen = {}

    def repl(m, n=n, seen=seen):
        num = m.group(1)
        k = seen.get(num, 0)
        seen[num] = k + 1
        new = OVERRIDE.get((n, num, k)) or OVERRIDE.get((n, num)) or DEFAULT.get(num)
        if new is None:
            raise SystemExit(f"line {n}: no mapping for §C0 subsection {num}")
        changes.append((n, num, new))
        return f"§C0 subsection {new}"
    lines[idx] = REF.sub(repl, lines[idx])
used_overrides = {(n, num) for n, num, _ in changes}
for key in OVERRIDE:
    assert (key[0], key[1]) in used_overrides, f"override {key} matched nothing"
print(f"outside §C0: {len(changes)} subsection references remapped")
from collections import Counter
print("   ", dict(Counter(f"{a}->{b}" for _, a, b in changes)))

# ---- the reader's guide describes §C0's contents: bring it in line with the new order
FRONT_OLD = ("  - a physics primer (§C0). It gives the time-of-flight (ToF), frequency-modulated continuous-wave (FMCW), beam and "
             "scanning relations, detector noise, detection statistics and weather attenuation used throughout, with worked numbers. "
             "ToF lidar times the round trip of a light pulse; FMCW lidar sweeps (chirps) the laser frequency and reads range from "
             "the beat frequency between the echo and the outgoing light. The primer also covers phase-based ranging (AMCW, "
             "amplitude-modulated continuous-wave) in ToF cameras and surveying instruments, and what counts as lidar;")
FRONT_NEW = ("  - a physics primer (§C0). It develops, in order, the three ranging principles (pulsed time of flight (ToF), phase "
             "ranging with amplitude-modulated continuous-wave (AMCW) light, as in ToF cameras and surveying instruments, and "
             "frequency-modulated continuous-wave (FMCW) ranging), beam and scanning geometry, the link loss of direct and coherent "
             "detection with the losses of weather and wet windows, detector noise and detection statistics, and the range, margin "
             "and dynamic range that follow, with worked numbers and a benchmark against published systems. ToF lidar times the "
             "round trip of a light pulse; FMCW lidar sweeps (chirps) the laser frequency and reads range from the beat frequency "
             "between the echo and the outgoing light;")
hits = [i for i in range(c0) if lines[i] == FRONT_OLD]
assert len(hits) == 1, f"reader's-guide line found {len(hits)}x"
lines[hits[0]] = FRONT_NEW
print("reader's guide: §C0 description updated at line", hits[0] + 1)

# ---- splice and rename figures
work = "\n".join(lines[:c0]) + "\n" + new_c0 + "\n\n" + "\n".join(lines[c1:])
FIG = {"C0.10a": "C0.1", "C0.10b": "C0.2", "C0.10c": "C0.3", "C0.10d": "C0.4"}
for a, b in FIG.items():
    work = work.replace(a, b)
assert "C0.10" not in work, "a C0.10 figure name is left"

# ---- 4. internal references in the new §C0
c0_text = work[work.index("## C0. Physics of lidar ranging"):work.index("## C1. Taxonomy")]
heads = set(re.findall(r"^#{3,4} (\d+(?:\.\d+)?)\.? ", c0_text, flags=re.M))
print("new §C0 headings:", sorted(heads, key=lambda s: [int(x) for x in s.split(".")]))
bad = []
for m in re.finditer(r"(§C\w+ )?subsections? (\d+(?:\.\d+)?)(?:–(\d+(?:\.\d+)?))?", c0_text, flags=re.I):
    if m.group(1):
        continue  # a reference to another section's subsection
    for num in filter(None, (m.group(2), m.group(3))):
        if num not in heads:
            bad.append(c0_text[max(0, m.start() - 60):m.end() + 30].replace("\n", " "))
print(f"internal subsection references that match no new heading: {len(bad)}")
for b in bad:
    print("   ", b)
left = [c0_text[max(0, m.start() - 50):m.end() + 30].replace("\n", " ")
        for m in re.finditer(r"\(10\.\d\)|\b10\.\d (?:asks|turns|follows|treats|reads|derives|explains|states)|§C0 subsection|\bsubsection 10\b", c0_text)]
print(f"left-over old-style references: {len(left)}")
for l in left:
    print("   ", l)
outside = work.replace(c0_text, "")
print("outside §C0, references to subsections that do not exist:",
      sorted({m.group(1) for m in re.finditer(r"§C0 subsection (\d+(?:\.\d+)?)", outside) if m.group(1) not in heads}))

out_c0.write_text(c0_text, encoding="utf-8", newline="\n")
data = work.replace("\n", "\r\n") if crlf else work
out_work.write_bytes(data.encode("utf-8"))
print(f"working copy written ({'CRLF' if crlf else 'LF'}): {len(data.encode('utf-8'))} bytes")
