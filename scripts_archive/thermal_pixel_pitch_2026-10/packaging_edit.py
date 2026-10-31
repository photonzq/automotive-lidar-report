"""Add the vacuum-packaging block to §A4 (after the pixel-pitch block), an Appendix 1 item and Appendix 2 sources.
Usage: packaging_edit.py <report.md> <packaging_fragments.md> <expected sha256 prefix> [--write]
Every anchor must occur exactly once and the starting hash must match; writes LF line endings. No display equations."""
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
assert "$$" not in frags["A4_PACKAGING"], "no display equations allowed"


def once(t, s):
    n = t.count(s)
    assert n == 1, f"anchor found {n} times: {s[:70]!r}"
    return t.index(s)


# §A4: before the germanium headwind group
i = once(text, "**Headwind: germanium**")
text = text[:i] + frags["A4_PACKAGING"] + "\n\n" + text[i:]
# Appendix 1: directly after the "Thermal pixel pitch (§A4)" item (one line), keeping the list tight
lines = text.split("\n")
hits = [k for k, ln in enumerate(lines) if ln.startswith("- **Thermal pixel pitch (§A4).**")]
assert len(hits) == 1
lines.insert(hits[0] + 1, frags["APP1"])
text = "\n".join(lines)
# Appendix 2: after the Guide investor Q&A line in the thermal group
lines = text.split("\n")
hits = [k for k, ln in enumerate(lines) if ln.startswith("- Guide Infrared investor Q&A on passenger-car design wins")]
assert len(hits) == 1
lines.insert(hits[0] + 1, frags["APP2"])
text = "\n".join(lines)
assert "\n\n\n" not in text
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
