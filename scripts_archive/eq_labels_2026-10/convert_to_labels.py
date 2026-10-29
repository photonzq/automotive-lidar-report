"""Convert the report from numbered equations to labels: every \\tag{N} becomes \\label{eq:name} and every reference
"Eq. (N)", "Eqs. (N)–(M)" or "Eqs. (N), (M) and (K)" cites \\eqref{eq:name} instead of (N).

Usage: python convert_to_labels.py <report.md> <label_names.json> <work.md> <expected sha256 prefix of the report>
label_names.json maps each equation number at the time of conversion to its label. The script checks the report's
hash, that its tags run 1..n in document order and that the names cover exactly those tags, are unique and well
formed. After converting, it checks the result with build/eqlabels.py and confirms that resolving the labels gives back
the original file byte for byte. It writes only the work copy; installing it is a separate, hash-guarded step.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

report, names_path, work, want = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
sys.path.insert(0, str(report.resolve().parent / "build"))
import eqlabels  # noqa: E402

raw = report.read_bytes()
h = hashlib.sha256(raw).hexdigest()
assert h.startswith(want), f"report changed: {h[:12]}"
text = raw.decode("utf-8")
assert "\r" not in text
names = {int(k): v for k, v in json.loads(names_path.read_text(encoding="utf-8")).items()}

TAG = re.compile(r"\\tag\{(\d+)\}")
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
NUM = re.compile(r"\((\d+)\)")
tags = [int(x) for x in TAG.findall(text)]
assert tags == list(range(1, len(tags) + 1)), "tags are not 1..n in document order"
assert sorted(names) == tags, "the names file does not cover exactly the tags"
assert len(set(names.values())) == len(names), "duplicate label names"
assert all(re.fullmatch(r"eq:[a-z0-9-]+", v) for v in names.values()), "malformed label name"

n_refs = sum(len(NUM.findall(m.group(0))) for m in REF.finditer(text))
out = TAG.sub(lambda m: "\\label{%s}" % names[int(m.group(1))], text)
out = REF.sub(lambda m: NUM.sub(lambda n: "\\eqref{%s}" % names[int(n.group(1))], m.group(0)), out)
errs = eqlabels.problems(out)
assert not errs, errs[:5]
assert eqlabels.resolve(out) == text, "resolving the labels does not reproduce the original"
work.write_bytes(out.encode("utf-8"))
print(f"{len(tags)} tags and {n_refs} references in {len(REF.findall(text))} phrases converted; "
      f"round trip exact; work copy sha256 {hashlib.sha256(out.encode('utf-8')).hexdigest()[:12]}")
