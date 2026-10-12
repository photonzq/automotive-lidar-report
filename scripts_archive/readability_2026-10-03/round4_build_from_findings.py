"""Round 4: turn a research agent's sources/<group>_findings.md into an edit list for the merge tools.

Parses each "## <item id>" section for its proposed edits (a "`old`:" fenced block followed by a "`new`:" fenced
block, in order) and its Appendix 2 lines ("- `- …`" under "**Appendix 2 entry:**", with the group named in
"under *Group*"). Writes edits/round4/R4_<group>.json with:
  - one edit per old/new pair (id R4_<group>-<item number><letter>), skipping ids listed with --skip;
  - one edit per Appendix 2 group, appending that group's new lines after its last list line, without lines whose
    URL Appendix 2 already holds.
My amendments after the read-through are applied from the AMEND table of round4_amendments.py if it exists:
AMEND[edit id] is a list of (exact substring of the agent's new text, replacement). The report is only read.
Usage: python round4_build_from_findings.py sources/<group>_findings.md [--skip=ID,ID]
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
# --report=<copy> builds against another copy (to regenerate the archived list of a batch already applied)
REPORT = next((Path(a[9:]) for a in sys.argv[1:] if a.startswith("--report=")), REPORT)
T = REPORT.read_text(encoding="utf-8")
src = Path(sys.argv[1])
group = src.name.replace("_findings.md", "")
skip = set()
for a in sys.argv[2:]:
    if a.startswith("--skip="):
        skip |= {x.strip() for x in a[7:].split(",") if x.strip()}
amend, appx_groups = {}, {}
am = HERE / "round4_amendments.py"
if am.exists():
    spec = importlib.util.spec_from_file_location("round4_amendments", am)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    amend = mod.AMEND
    # APPX_GROUPS[item id] names the Appendix 2 group for an item whose findings name none
    appx_groups = getattr(mod, "APPX_GROUPS", {})

text = src.read_text(encoding="utf-8")
sections = re.split(r"(?m)^## ", text)[1:]
# a fence may be indented (inside a list item); its content then carries the same indent, which is removed
# "`old`:" may carry a location note before its colon, e.g. "`old` (§C0 table, L1690):"
FENCE = re.compile(r"`(old|new)`(?:[ \t]*\([^\n]*?\))?:[ \t]*\n([ \t]*)```[a-z]*\n(.*?)\n\2```", re.S)


def dedent(body, indent):
    return "\n".join(l[len(indent):] if l.startswith(indent) else l for l in body.split("\n"))
# an Appendix 2 line is any backticked "- …" in the entry block; its group is named after it on the same line
# ("(group: *X*)"), or else once for the block ("under *X*", "(group *X*)"), in italics or bold
ENTRY = re.compile(r"`(- [^`]+)`")
GROUPREF = re.compile(r"(?:under|group:?)\s*\*{1,2}([^*]+?)\*{1,2}")

app_start = T.index("# Appendix 2 — Selected sources")
appendix = T[app_start:]
# groups are the bold headings and the italic subheadings of Appendix 2
groups = {}
for m in re.finditer(r"(?m)^\*\*([^*]+)\*\*\s*$|^\*([^*]+)\*\s*$", appendix):
    groups[(m.group(1) or m.group(2)).strip()] = app_start + m.start()
edits, by_group, problems = [], {}, []
for sec in sections:
    sid = sec.split("\n", 1)[0].strip()
    if not re.match(r"R\d", sid):
        continue
    num = sid.rsplit("-", 1)[-1]
    blocks = [(k, dedent(body, ind)) for k, ind, body in FENCE.findall(sec)]
    pairs = []
    for i in range(0, len(blocks) - 1, 2):
        (k1, v1), (k2, v2) = blocks[i], blocks[i + 1]
        if k1 == "old" and k2 == "new":
            pairs.append((v1, v2))
        else:
            problems.append(f"{sid}: unpaired old/new blocks")
    for j, (old, new) in enumerate(pairs):
        eid = f"R4_{group}-{num}{'abcdefghij'[j] if len(pairs) > 1 else ''}"
        if eid in skip:
            continue
        for sub, rep in amend.get(eid, []):
            assert new.count(sub) == 1, (eid, sub[:60], new.count(sub))
            new = new.replace(sub, rep)
        if T.count(old) != 1:
            problems.append(f"{eid}: old occurs {T.count(old)} times: {old[:70]!r}")
        edits.append({"id": eid, "finding": f"Round 4 source research, {sid}", "old": old, "new": new,
                      "why": f"Source found by the {group} research agent; see sources/{src.name}, {sid}."})
    m = re.search(r"\*\*Appendix 2 entr(?:y|ies):\*\*(.*?)(?:\n---|\Z)", sec, re.S)
    if not m or m.group(1).strip().lower().startswith("none"):
        continue
    block = m.group(1)
    dm = GROUPREF.search(block)
    default = dm.group(1).strip() if dm else appx_groups.get(sid)
    for bline in block.split("\n"):
        for em in ENTRY.finditer(bline):
            # a bare "US$" in a source label would open math mode: the report writes currency as \$
            line = re.sub(r"(?<!\\)US\$", r"US\\$", em.group(1))
            gm = GROUPREF.search(bline, em.end())
            gname = gm.group(1).strip() if gm else default
            url = re.findall(r"https?://\S+", line)
            if url and url[-1].rstrip(").,;") in appendix:
                continue
            if gname not in groups:
                problems.append(f"{sid}: Appendix 2 group {gname!r} not found")
                continue
            by_group.setdefault(gname, []).append(line)

for gname, lines in by_group.items():
    a = groups[gname]
    nxt = min((p for p in groups.values() if p > a), default=len(T))
    body = T[a:nxt]
    last = [l for l in body.split("\n") if l.startswith("- ")][-1]
    if T.count(last) != 1:
        problems.append(f"Appendix 2 {gname}: last line not unique")
        continue
    new_lines = list(dict.fromkeys(l for l in lines if l not in body))  # once each, in order
    edits.append({"id": f"R4_{group}-A2-{len(edits):02d}", "finding": f"Round 4 source research, Appendix 2 ({gname})",
                  "old": last, "new": last + "\n" + "\n".join(new_lines),
                  "why": f"Sources read by the {group} research agent, added to the group '{gname}'."})

out = HERE / "edits" / "round4" / f"R4_{group}.json"
out.parent.mkdir(parents=True, exist_ok=True)
# an applied list is the archive record of its merge: never overwrite one by accident
assert not out.exists() or "--force" in sys.argv, f"{out.name} exists; pass --force to rebuild it"
out.write_text(json.dumps({"block": f"R4_{group}", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(f"{len(edits)} edits ({sum(len(v) for v in by_group.values())} Appendix 2 lines in {len(by_group)} groups) -> {out.name}")
for p in problems:
    print("PROBLEM", p)
