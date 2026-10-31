"""Restore two citations of equations in outside papers that the label conversion of 2026-10-29 turned into
references to the report's own equations: Supplementary Eq. 4 of Bianconi et al. 2025 and Eq. 1 of arXiv 2503.15087.
Before the conversion they read "Supplementary Eq. (4)" and "Eq. (1)"; they are now written without parentheses, as
the report cites other papers' equations, so the build neither numbers nor links them.
Usage: outside_eq_fix.py <report.md> <expected sha256 prefix> [--write]
Each (old, new) pair must match exactly once and the starting hash must match; writes LF line endings."""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

PAIRS = [
    ("[I, Bianconi et al. 2025, Supplementary Eq. \\eqref{eq:points-on-pedestrian}]",
     "[I, Bianconi et al. 2025, Supplementary Eq. 4]"),
    ("[I, arXiv 2503.15087, Eq. \\eqref{eq:thermal-ifov}, Tables 7–8]",
     "[I, arXiv 2503.15087, Eq. 1, Tables 7–8]"),
]
for old, new in PAIRS:
    n = text.count(old)
    assert n == 1, f"found {n} times: {old[:80]!r}"
    text = text.replace(old, new)
new = text.encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
