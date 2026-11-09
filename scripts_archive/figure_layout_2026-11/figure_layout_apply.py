"""Figure layout of the report's PDF and web page: a tall figure at 60 % of the text width, small single-panel
figures beside the text or centred at 65 %, all other figures at full width.

The classes come from figure_classify.py (drawn sizes from the PNG files, 600 dpi):
- Figure C3a, drawn 7.12 x 8.02 in (height/width 1.13), is tall: its image line gets {.tall};
- Figures C0.2 and E11.1, single panels drawn 4.72 and 4.32 in wide, are followed by 3,469 and 2,504 characters of
  text before the next heading, table, display equation, image or caption, more than the 839 and 693 needed for a
  float at 52 % of the text width: each goes into a fenced div "side";
- Figure A7.1, a single panel drawn 4.32 in wide, is followed by a heading after 216 characters and has no second
  small figure next to it: it goes into a div "narrow", centred at 65 %.
Each div holds the image and the whole caption block, the "*Figure ...*" label line with the list that follows it,
and a blank line comes before the closing fence so that pandoc keeps the caption a paragraph. The style block at the
end of the report defines the classes and keeps headings, tables, display equations and full-width figures clear of
a float. "![" and "*Figure" stay at the start of their lines.

Usage: figure_layout_apply.py <report.md> <expected sha256 prefix> [--write]
The starting hash must match and every listed figure must be found once; the report keeps its LF line endings.
"""
import hashlib
import re
import sys
from pathlib import Path

LAYOUT = {"C3a": "tall", "C0.2": "side", "E11.1": "side", "A7.1": "narrow"}
STYLE = """
<style>
img.tall { width: 60%; }
div.side { float: right; width: 52%; margin: 0.15em 0 0.8em 1.4em; break-inside: avoid; }
div.side img, div.half img, div.narrow img { width: 100%; margin: 0 0 0.3em 0; }
div.side p, div.half p, div.narrow p { margin: 0.2em 0; }
div.pair { display: flex; justify-content: space-between; align-items: flex-start; break-inside: avoid; }
div.half { width: 48%; }
div.narrow { width: 65%; margin: 0.6em auto; break-inside: avoid; }
img, table, .eqn, h1, h2, h3, h4, div.pair, div.narrow { clear: both; }
</style>
"""
IMG = re.compile(r"^!\[[^\]]*\]\([^)\s]+\.png\)$")
LABEL = re.compile(r"^\*Figure ([A-Z]\d+[a-z]?(?:\.\d+)?)\.\*")

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text and "<style>" not in text, "CR line endings or layout already applied"

lines = text.split("\n")
out, done, i = [], {}, 0
while i < len(lines):
    line = lines[i]
    if IMG.match(line):
        j = i + 1
        while lines[j] == "":
            j += 1
        m = LABEL.match(lines[j])
        kind = LAYOUT.get(m.group(1)) if m else None
        if kind == "tall":
            out.append(line + "{.tall}")
            done[m.group(1)] = kind
            i += 1
            continue
        if kind in ("side", "narrow"):
            assert out and out[-1] == "", f"Figure {m.group(1)}: no blank line before the image"
            k = j
            while k < len(lines) and lines[k] != "":  # the caption block ends at the first blank line
                k += 1
            out += [f"::: {kind}", line] + lines[i + 1:k] + ["", ":::"]
            done[m.group(1)] = kind
            i = k  # the blank line after the caption block is kept and separates the fence from the text
            continue
    out.append(line)
    i += 1
assert done == LAYOUT, f"found {done}, expected {LAYOUT}"

new = ("\n".join(out).rstrip("\n") + "\n" + STYLE).encode("utf-8")
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
for label, kind in LAYOUT.items():
    print(f"Figure {label}: {kind}")
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
