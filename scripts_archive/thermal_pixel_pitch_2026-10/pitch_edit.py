"""Add the thermal pixel-pitch block (Holst and Driggers 2012) to §A4 of the report, with a pointer in §A3, the Boson SX8
in the existing pixel-pitch bullet, an Appendix 1 item and Appendix 2 sources.
Usage: pitch_edit.py <report.md> <fragments.md> <expected sha256 prefix> [--write]
Every anchor must occur exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

report, frag_path, expected = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

frags, key = {}, None
for line in frag_path.read_text(encoding="utf-8").split("\n"):
    if line.startswith("@@@ "):
        key = line[4:].strip()
        if key != "END":
            frags[key] = []
        continue
    if key and key != "END":
        frags[key].append(line)
frags = {k: "\n".join(v).strip("\n") for k, v in frags.items()}


def once(t, s):
    n = t.count(s)
    assert n == 1, f"anchor found {n} times: {s[:70]!r}"
    return t.index(s)


def append_after(t, anchor, add):
    i = once(t, anchor) + len(anchor)
    return t[:i] + add + t[i:]


def insert_before(t, anchor, block, sep="\n\n"):
    i = once(t, anchor)
    return t[:i] + block + sep + t[i:]


def insert_after_line(t, prefix, block):
    lines = t.split("\n")
    hits = [k for k, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(hits) == 1, f"line prefix found {len(hits)} times: {prefix!r}"
    lines[hits[0]:hits[0] + 1] = [lines[hits[0]], block]
    return "\n".join(lines)


text = append_after(text, "In engineering terms, the figures bound what the pixel count alone allows; "
                          "the achieved range is set by those other factors as well.", frags["A3_POINTER"].rstrip())
text = append_after(text, "and Guide shows an 8 µm 640×512 camera core [P].", frags["A4_SX8"].rstrip())
text = insert_before(text, "**Headwind: germanium**", frags["A4_BLOCK"])
# Appendix 1: last item of the "Sensor and chip specifications" group, directly after its last bullet (no blank line,
# so the list stays tight), i.e. before the blank line that precedes the next group heading
i = once(text, "\n\n**Night vision beyond thermal (§A7)**")
text = text[:i] + "\n" + frags["APP1"] + text[i:]
text = insert_after_line(text, "- LightPath BlackDiamond BD6 datasheet", frags["APP2"])
assert "\n\n\n" not in text, "triple newline created"
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
