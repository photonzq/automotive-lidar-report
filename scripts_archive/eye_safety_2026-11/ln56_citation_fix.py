"""§C4c subsection 1a: cite FDA Laser Notice No. 56 for what it states.

The notice (issued 8 May 2019, reissued 21 Feb 2023) lists, on its printed pp. 3-4, the sections of 21 CFR 1040 that
FDA does not intend to enforce for products conforming to the comparable clauses of IEC 60825-1 Ed. 3; 1040.10(f)(9),
"Scanning safeguard", is among them. It does not say which IEC clause takes the place of (f)(9). The only place it
names the single-fault rule is its note to 1040.10(f)(2), "Safety interlocks" (p. 4): IEC 60825-1 Ed. 3 requires
redundancy or safe failure of interlocks indirectly, through the reasonably foreseeable single-fault sub-clause of
its classification rules (4.3). The text therefore states the non-enforcement with its pages, gives the note as the
notice's own, and marks the step from that sub-clause to a stalled scanner as an estimate [E]. The Appendix 2 entry
and the citation of clause 4.3 in the first rule bullet get the same page detail.

Usage: ln56_citation_fix.py <report.md> <expected sha256 prefix> [--write]
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

EDITS = [
    ("(clause 4.3, the classification rules) [P, via FDA Laser Notice No. 56; §C4d(f)].",
     "(clause 4.3, the classification rules) [P, via FDA Laser Notice No. 56, p. 4; §C4d(f)]."),
    ("FDA accepts conformance with IEC 60825-1 Ed. 3 in place of this paragraph, because the IEC single-fault rule "
     "supplies the same safe-failure requirement [P, Laser Notice No. 56, issued 2019 and reissued 21 Feb 2023, p. 4].",
     "FDA does not intend to enforce this paragraph for products that conform to the comparable clauses of IEC "
     "60825-1 Ed. 3 [P, Laser Notice No. 56, issued 2019 and reissued 21 Feb 2023, pp. 3–4]. The notice does not "
     "say which IEC clause takes its place. In its note on safety interlocks it traces the IEC standard's "
     "safe-failure requirement to the single-fault sub-clause of the classification rules (4.3) [P, Laser Notice "
     "No. 56, p. 4, note to 1040.10(f)(2)], and a stalled scanner falls under the same sub-clause [E]."),
    ("- FDA, Laser Notice No. 56 (2019, reissued 21 Feb 2023; p. 4, (f)(9) and the IEC single-fault rule): ",
     "- FDA, Laser Notice No. 56 (2019, reissued 21 Feb 2023; pp. 3–4, the sections of 21 CFR 1040 that FDA does not "
     "intend to enforce for products conforming to IEC 60825-1 Ed. 3, (f)(9) among them; p. 4, note to (f)(2), the "
     "single-fault sub-clause 4.3): "),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
