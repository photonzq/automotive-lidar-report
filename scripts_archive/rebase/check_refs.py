"""Read-only consistency check of equation tags and references in the report."""
import re
from pathlib import Path

t = Path(r"<report folder>\automotive_perception_report_2026-09-27.md").read_text(encoding="utf-8")
tags = [int(x) for x in re.findall(r"\\tag\{(\d+)\}", t)]
print("tags", len(tags), "sequential", tags == list(range(1, len(tags) + 1)))
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
refs = [int(x) for m in REF.finditer(t) for x in re.findall(r"\((\d+)\)", m.group(0))]
print("refs", len(refs), "dangling", sorted({r for r in refs if r < 1 or r > len(tags)}))
m = re.search(r"underbrace\{N_\{\\rm ch\}N_LP_\{\\rm an\}\}_\{\\rm analog\}.*?\\tag\{(\d+)\}", t)
print("P_elec equation tag:", m.group(1) if m else None)
i = t.find("**Gated transmitter:** Eq. (")
print(t[i:i + 60])
print("10.9 heading present:", "#### 10.9 What the model leaves out" in t,
      "| eye-safety pointer present:", "puts numbers on it for the two designs of §C7a" in t,
      # items 2(h)-(i) of §C7b became subsection 3a, items (a)-(b), in the readability Round 3 (2026-10-05)
      "| §C7b 3a(b) present:", "**(b) What the 1,550 nm eye-safety allowance buys" in t)
