"""Check that the Round 2 edits survive in the current report, and attribute every change since to a later list.

For each edit of edits/round2/*.json and of R3a (merged together with Round 2), the applied "new" text is renumbered
with the Round 3 map (edits/round3/round3_renumber_map.txt) and looked up in the report:
  - intact: the whole renumbered text is present;
  - changed: some of its segments (sentences, table cells) are gone. Each missing segment is attributed to the
    Round 3 or Round 4 edit whose "old" text overlaps it by at least 40 characters, or is reported UNEXPLAINED with
    the report text where it used to be.
The report and the lists are only read.
Usage: python check_round2_survival.py [--all]   (--all also prints the attributed segments)
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
T = REPORT.read_text(encoding="utf-8")
show_all = "--all" in sys.argv

# Round 3 map: old tag -> new tag (only numbers that changed are listed)
mtxt = (HERE / "edits" / "round3" / "round3_renumber_map.txt").read_text(encoding="utf-8")
mtxt = mtxt[mtxt.index("Map (old -> new)"):mtxt.index("Equation numbers quoted outside")]
MAP = {int(a): int(b) for a, b in re.findall(r"(\d+)->(\d+)", mtxt)}
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
TAG = re.compile(r"\\tag\{(\d+)\}")


def renumber(s):
    s = REF.sub(lambda m: re.sub(r"\((\d+)\)", lambda n: f"({MAP.get(int(n.group(1)), int(n.group(1)))})", m.group(0)), s)
    return TAG.sub(lambda m: f"\\tag{{{MAP.get(int(m.group(1)), int(m.group(1)))}}}", s)


def segments(s):
    """Sentences and table cells of a text, without the very short ones."""
    out = []
    for line in s.split("\n"):
        parts = line.split(" | ") if line.lstrip().startswith("|") else re.split(r"(?<=[.;])\s+(?=[A-Z(*\[$])", line)
        out += [p.strip(" |") for p in parts if len(p.strip(" |")) >= 25]
    return out


K = 40
later = []  # (list name, edit id, old text)
for sub in ("round3", "round4"):
    for p in sorted((HERE / "edits" / sub).glob("*.json")):
        if p.stem == "R3a_E2a_E12":
            continue
        for e in json.loads(p.read_text(encoding="utf-8")).get("edits", []):
            later.append((p.stem, e["id"], e["old"]))
shingle = {}
for i, (lst, eid, old) in enumerate(later):
    for form in {old, renumber(old)}:
        for j in range(0, max(1, len(form) - K + 1)):
            shingle.setdefault(form[j:j + K], set()).add(i)


def attribute(seg):
    hits = set()
    for j in range(0, max(1, len(seg) - K + 1)):
        hits |= shingle.get(seg[j:j + K], set())
    return sorted(hits)


def where_now(seg):
    """The report line holding the longest surviving prefix or suffix of a lost segment."""
    for n in range(min(len(seg), 80), 19, -5):
        for piece in (seg[:n], seg[-n:]):
            k = T.find(piece)
            if k >= 0 and T.count(piece) == 1:
                a, b = T.rfind("\n", 0, k) + 1, T.find("\n", k)
                return T.count("\n", 0, k) + 1, T[a:b]
    return None, None


lists = sorted((HERE / "edits" / "round2").glob("*.json")) + [HERE / "edits" / "round3" / "R3a_E2a_E12.json"]
tot = {"intact": 0, "changed, explained": 0, "changed, UNEXPLAINED": 0, "deletion": 0}
unexplained = []
for p in lists:
    for e in json.loads(p.read_text(encoding="utf-8")).get("edits", []):
        new = renumber(e["new"])
        if new.strip() == "" or (len(new) < len(e["old"]) and new in renumber(e["old"]) and new not in T):
            tot["deletion"] += 1
            continue
        if new in T:
            tot["intact"] += 1
            continue
        lost = [s for s in segments(new) if s not in T]
        if not lost:
            tot["intact"] += 1  # all segments present; only joins between them changed
            continue
        expl = {s: attribute(s) for s in lost}
        if all(expl.values()):
            tot["changed, explained"] += 1
            if show_all:
                print(f"[explained] {p.stem} {e['id']}")
                for s, h in expl.items():
                    print(f"    - {s[:110]!r}  <- {', '.join(f'{later[i][0]}:{later[i][1]}' for i in h[:4])}")
            continue
        tot["changed, UNEXPLAINED"] += 1
        unexplained.append((p.stem, e["id"], [s for s, h in expl.items() if not h]))

for lst, eid, segs in unexplained:
    print(f"[UNEXPLAINED] {lst} {eid}")
    for s in segs:
        ln, now = where_now(s)
        print(f"    lost: {s[:240]!r}")
        print(f"    now : L{ln}: {now[:400]!r}" if ln else "    now : (no surviving prefix or suffix found)")
print(tot)
