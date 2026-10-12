"""Replace section C0 subsection 10 with the restructured 10.1-10.7 text, renumber equations globally,
remap every Eq. reference, and update the cross-references to the old item letters."""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SNAP = Path(r"<scratch>\rewrite\report_after_peer_fmcw.md")
NEW = Path(r"<scratch>\mech\c0_10_restructured.md")
OUT_SNAP = Path(r"<scratch>\rewrite\report_after_c0_10_restructure.md")
DRY = "--dry" in sys.argv

raw = REPORT.read_bytes()
assert hashlib.sha256(raw).hexdigest() == hashlib.sha256(SNAP.read_bytes()).hexdigest(), "report changed since the snapshot"
s = raw.decode("utf-8")
assert "\r" not in s
new_sec = NEW.read_text(encoding="utf-8").rstrip("\n") + "\n"
assert "\r" not in new_sec and "\t" not in new_sec

# ---- 1. splice the section
start = s.index("### 10. Link budget: loss versus range, the detection level, and how range scales\n")
end = s.index("## C1. Taxonomy\n", start)
s = s[:start] + new_sec + "\n" + s[end:]

# ---- 2. cross-references to the old lettered items
subs = [
    ("derived in §C0 subsection 10(a))", "derived in §C0 subsection 10.2)", 2),
    ("§C0 subsection 10(a) derives Eq.", "§C0 subsection 10.2 derives Eq.", 1),
    ("§C0 subsection 10(a) derives it", "§C0 subsection 10.2 derives it", 1),
    ("§C0 subsection 10(a) gives the derivation", "§C0 subsection 10.2 gives the derivation", 1),
    ("a model choice, the same as in §C0 subsection 10.", "a model choice, the same as in §C0 subsection 10.2.", 1),
    ("Subsection 10(c) plots these cases against photon counting (Figure C0.10b).",
     "Subsection 10.3 plots these cases against photon counting (Figure C0.10b).", 1),
]
for old, new, n in subs:
    c = s.count(old)
    assert c == n, (old, c, n)
    s = s.replace(old, new)
left = re.findall(r"subsections? 10\([a-e]\)|item \([a-e]\)", s)
print("leftover lettered refs:", left)

# ---- 3. renumber \tag{N} in order of appearance, remap references
tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", s)]
assert len(tags) == len(set(tags)), "duplicate tag numbers"
mapping = {old: i for i, old in enumerate(tags, 1)}
changed = {o: n for o, n in mapping.items() if o != n}
print("tags:", len(tags), "| renumbered:", len(changed))
print("  sample map:", {k: mapping[k] for k in (29, 35, 36, 37, 40, 41, 44, 901, 902, 903, 904, 905, 906, 45, 90, 177) if k in mapping})
s = re.sub(r"\\tag\{(\d+)\}", lambda m: r"\tag{" + str(mapping[int(m.group(1))]) + "}", s)
EQREF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
n_ref, bad = 0, []


def remap(m):
    global n_ref
    def one(mm):
        global n_ref
        k = int(mm.group(1))
        if k not in mapping:
            bad.append(k)
            return mm.group(0)
        n_ref += 1
        return f"({mapping[k]})"
    return re.sub(r"\((\d+)\)", one, m.group(0))


s = EQREF.sub(remap, s)
print("Eq. references remapped:", n_ref, "| dangling:", sorted(set(bad)))
assert not bad

# ---- 4. checks
tags2 = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", s)]
assert tags2 == list(range(1, len(tags2) + 1)), "tags not contiguous"
odd = [i for i, l in enumerate(s.split("\n"), 1) if l.replace("\\$", "").count("$") % 2]
print("odd-$ lines:", odd[:10])
assert not odd
tbl_pipe = [i for i, l in enumerate(s.split("\n"), 1)
            if l.startswith("|") and any("|" in sp for sp in re.findall(r"\$([^$]+)\$", l.replace("\\$", "")))]
print("tables with | inside math:", tbl_pipe[:5])
print("h4 headings:", [l for l in s.split("\n") if l.startswith("#### ")])
print("bytes:", len(s.encode("utf-8")), "(was", len(raw), ")")
if not DRY:
    REPORT.write_bytes(s.encode("utf-8"))
    OUT_SNAP.write_bytes(s.encode("utf-8"))
    print("written; snapshot", OUT_SNAP.name)
