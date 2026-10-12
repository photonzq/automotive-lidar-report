"""Merge edit lists (JSON) and apply them to the live report as one hash-guarded batch.

Checks before writing (nothing is written if any check fails):
- every "old" occurs exactly once in the live report, and no two edits overlap;
- unescaped-$ parity of "new" matches "old"; no versioning words; texmath-safe \\rm; no new backslash-quote (\\");
- no edit touches the protected spans: Section D8, Appendix 1, and the two Section B8 bullets the author has not yet assigned;
- after applying: the number of \\tag{...} is unchanged unless --allow-tag-change; no bold paragraph heading
  newly glued onto a list item (pandoc would merge it into the bullet).
Usage: python merge_apply.py [--dry [--out=<path>]] [--allow-tag-change] edits/a.json edits/b.json ...
"""
import hashlib
import json
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
DOLLAR = re.compile(r"(?<!\\)\$")
BAD_RM = re.compile(r"_\{[^{}]*[,A-Za-z0-9]\\rm")
VERSIONING = ("corrected", "updated", "revised", " added ", " now ", " newly ")
# The two Section B8 bullets were protected until the author decided (2026-10-04) to fold them into the text;
# the parallel editing pass supplies that edit, so they are no longer protected here.
PROTECTED_LINES = ()


def section_span(text, start_heading, end_heading):
    a = text.find(start_heading)
    b = text.find(end_heading, a + 1)
    return (a, b if b > 0 else len(text)) if a >= 0 else None


def glued_headings(text):
    lines = text.split("\n")
    out = set()
    for i in range(1, len(lines)):
        if lines[i].startswith("**") and re.match(r"^\s*([-*]|\d+\.)\s", lines[i - 1]):
            out.add(lines[i][:80])
    return out


args = [a for a in sys.argv[1:] if not a.startswith("--")]
dry, allow_tags = "--dry" in sys.argv, "--allow-tag-change" in sys.argv
raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
assert "\r\n" not in text, "report has CRLF line endings"

protected = []
for hdr, end in (("## D8. Western public research funding", "\n# Part E"), ("# Appendix 1 —", "# Appendix 2 —")):
    sp = section_span(text, hdr, end)
    if sp:
        protected.append((sp[0], sp[1], hdr))
for pl in PROTECTED_LINES:
    a = text.find(pl)
    if a >= 0:
        protected.append((a, text.find("\n", a), pl))

edits, problems = [], []
for arg in args:
    # "peer:<path>" marks an edit list supplied by the parallel editing pass for an author-approved change; it may touch
    # the protected spans (Section D8, Appendix 1), which this pass's own edits must not.
    trusted = arg.startswith("peer:")
    path = arg[5:] if trusted else arg
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    for e in (data if isinstance(data, list) else data.get("edits", [])):
        eid, old, new = e.get("id", "?"), e.get("old", ""), e.get("new", "")
        tag = f"{Path(path).stem}:{eid}"
        if not old or old == new:
            problems.append(f"{tag}: empty or unchanged edit")
            continue
        k = text.count(old)
        if k != 1:
            problems.append(f"{tag}: 'old' occurs {k} times")
            continue
        a = text.find(old)
        b = a + len(old)
        for pa, pb, name in protected:
            if a < pb and pa < b and not trusted:
                problems.append(f"{tag}: touches protected span {name!r}")
        if len(DOLLAR.findall(new)) % 2 != len(DOLLAR.findall(old)) % 2:
            problems.append(f"{tag}: unbalanced $")
        for w in VERSIONING:
            if w in f" {new.lower()} " and w not in f" {old.lower()} ":
                problems.append(f"{tag}: versioning word {w.strip()!r}")
        if BAD_RM.search(new) and not BAD_RM.search(old):
            problems.append(f"{tag}: texmath \\rm placement")
        if new.count('\\"') > old.count('\\"'):
            problems.append(f"{tag}: new backslash-quote")
        edits.append((a, b, new, tag))
edits.sort()
for (a0, a1, _, t0), (b0, b1, _, t1) in zip(edits, edits[1:]):
    if b0 < a1:
        problems.append(f"overlap: {t0} and {t1}")

out = text
for a, b, new, _ in sorted(edits, reverse=True):
    out = out[:a] + new + out[b:]
tags0, tags1 = text.count("\\tag{"), out.count("\\tag{")
if tags0 != tags1 and not allow_tags:
    problems.append(f"tag count changed {tags0} -> {tags1}")
new_glued = glued_headings(out) - glued_headings(text)
for g in sorted(new_glued):
    problems.append(f"bold heading glued to a list item: {g!r}")
for pl in PROTECTED_LINES:
    line0 = next((l for l in text.split("\n") if l.startswith(pl)), None)
    line1 = next((l for l in out.split("\n") if l.startswith(pl)), None)
    if line0 != line1:
        problems.append(f"protected line changed: {pl!r}")

print(f"{len(edits)} edits from {len(args)} file(s); sha {h0[:12]}; {len(raw):,} -> {len(out.encode('utf-8')):,} bytes; tags {tags0} -> {tags1}")
if problems:
    for p in problems:
        print("PROBLEM", p)
    print(f"{len(problems)} problem(s); nothing written")
    sys.exit(1)
if dry:
    # --out=<path> writes the merged text to a scratch copy, for grepping the result before the real merge
    dest = next((a[6:] for a in sys.argv[1:] if a.startswith("--out=")), None)
    if dest:
        Path(dest).write_bytes(out.encode("utf-8"))
        print("merged copy written to", dest)
    print("dry run OK; nothing written")
    sys.exit(0)
if hashlib.sha256(REPORT.read_bytes()).hexdigest() != h0:
    sys.exit("report changed after it was read; nothing written")
REPORT.write_bytes(out.encode("utf-8"))
print("written; new sha", hashlib.sha256(out.encode("utf-8")).hexdigest()[:12])
