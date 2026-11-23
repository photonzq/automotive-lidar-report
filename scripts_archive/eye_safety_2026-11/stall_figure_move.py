"""Move Figure C4c.1 (a right-floating `::: side` block) from after the last stall-time bullet of §C4c subsection 1a
to just before the stall-time bullets, so that the derivations wrap beside it.

A side figure may not break across pages. When it does not fit below the last bullet, the browser carries it to the
next page and fills the rest of the current page with the text that follows; the heading of subsection 2 then clears
the float, which leaves the figure alone beside an empty half page. Placed before the bullets, the figure has
several inches of the subsection's own text after it wherever the page breaks. The block itself is unchanged.

Usage: stall_figure_move.py <report.md> <expected sha256 prefix> [--write]
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

START = "::: side\n![Time for a stalled beam to reach the Class 1 limit"
END = "- *Script:* `build/figures/stall_time_to_limit.py` [E].\n\n:::\n"
assert text.count(START) == 1 and text.count(END) == 1
i = text.index(START)
j = text.index(END, i) + len(END)
block = text[i:j]

BEFORE = "and a few milliseconds for FMCW.\n\n"
AFTER = "\n**What the safeguard has to cover**"
assert text[i - len(BEFORE):i] == BEFORE, "block is not where expected"
assert text[j:j + len(AFTER)] == AFTER, "block is not followed by the safeguard paragraph"
new = text[:i] + text[j + 1:]  # drop the block and the blank line after it

INTRO = ("the budget for detecting the stall and cutting the laser.\n- **1,550 nm.**")
assert new.count(INTRO) == 1, f"intro anchor found {new.count(INTRO)} times"
new = new.replace(INTRO, INTRO.replace("laser.\n- ", "laser.\n\n" + block + "\n- "), 1)
assert "\r" not in new and new.count(START) == 1
assert len(new) == len(text) + 1  # one blank line moved, one added before the block
print(f"block of {len(block)} characters moved; sha256 before {sha[:12]}, "
      f"after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
