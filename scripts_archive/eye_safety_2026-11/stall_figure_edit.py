"""Figure C4c.1 in §C4c subsection 1a: time for a stalled beam to reach the Class 1 limit against its average power,
drawn by build/figures/stall_time_to_limit.py. The Ge-receiver figure of §C4c subsection 4, until now "Figure C4c",
becomes Figure C4c.2, since the new figure comes first in the section.

Usage: stall_figure_edit.py <report.md> <expected sha256 prefix> [--write]
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

BUDGET = (r"- **The budget therefore scales as $1/(\eta P)$:** a few hundred milliseconds at 905 nm, 10–80 ms for "
          r"1,550 nm pulsed lidars, and a few milliseconds for FMCW." + "\n")

BUDGET_WITH_FIGURE = (
    r"- **The budget therefore scales as $1/(\eta P)$** (Figure C4c.1): a few hundred milliseconds at 905 nm, 10–80 ms "
    r"for 1,550 nm pulsed lidars, and a few milliseconds for FMCW." + "\n"
    "\n"
    "::: side\n"
    "![Time for a stalled beam to reach the Class 1 limit against its average power]"
    "(automotive_perception_report_figures/stall_time_to_limit.png)\n"
    "\n"
    r"*Figure C4c.1.* Time for a stalled beam to reach the Class 1 limit, $t_{\rm stall}$, against the beam's average "
    r"power $P$, from the limits of subsection 1." + "\n"
    r"- *Solid lines:* the whole beam enters the measuring aperture, 7 mm at 905 nm. At 1,550 nm the aperture is 1 mm "
    r"for exposures under 0.35 s and widens to 3.5 mm at 10 s, which bends the line at about 20 mW." + "\n"
    r"- *Dashed line:* a 1,550 nm Gaussian beam 3 mm across ($1/e^2$ diameter), about 20% of which enters the 1 mm "
    r"aperture." + "\n"
    r"- *Markers:* Velodyne's 2 mW per beam, the 0.64 W of Luminar's patent example and the 3.8 W of the FMCW model "
    r"of §C7a, on both 1,550 nm lines; the grey line marks a check made every 100 ms." + "\n"
    r"- *Where the lines end:* below about 1 mW at 905 nm and 10 mW at 1,550 nm a stalled beam never reaches the limit. "
    r"At 905 nm the pulse-train rule can bind sooner (text)." + "\n"
    r"- *Script:* `build/figures/stall_time_to_limit.py` [E]." + "\n"
    "\n"
    ":::\n")

EDITS = [
    (BUDGET, BUDGET_WITH_FIGURE),
    ("\n*Figure C4c.* (a) Shot-noise efficiency", "\n*Figure C4c.2.* (a) Shot-noise efficiency"),
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
