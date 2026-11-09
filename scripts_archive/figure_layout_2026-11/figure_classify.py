"""Read-only classification of a note's figures for the PDF/web layout (tall, side, pair, narrow, full width).

Rules: a figure drawn about 6.5 in wide with height/width >= 0.9 is "tall" (60 % of the text width);
one drawn at most about 4.5 in wide is small: it floats ("side", 52 %) if the plain text after it, up to the next
heading, table, display equation, image or caption, fills at least 80 % of its height, estimated as
0.52 x 6.7 in x (h/w) + 0.9 in at about 300 characters per inch; two small figures with nothing between them pair
("half", 48 % each); the rest are "narrow" (65 %). Wider-than-tall figures about 6.5 in wide stay at full width.

It reads the report's caption blocks: the "*Figure ...*" label line plus the list lines that follow it without a
blank line. It also prints a caption-aware height (caption characters at about 330 per inch in the
52 % column) because these captions are much longer than the 0.9 in the rule allows, and the scale at which the
figure's lettering would print (displayed width over drawn width).
Run it on the report before the layout is applied: afterwards the closing fences end the text it measures.
Usage: figure_classify.py <note.md> [text width in inches, default 7.25]
"""
import re
import sys
from pathlib import Path

from PIL import Image

note = Path(sys.argv[1])
TEXT_W = float(sys.argv[2]) if len(sys.argv) > 2 else 7.25
lines = note.read_text(encoding="utf-8").split("\n")
IMG = re.compile(r"^!\[[^\]]*\]\(([^)\s]+\.png)\)")


def clearing(s):
    t = s.lstrip()
    return t.startswith(("#", "|", "$$", "![", ":::", "*Table", "*Figure"))


rows = []
for i, line in enumerate(lines):
    m = IMG.match(line)
    if not m:
        continue
    im = Image.open(note.parent / m.group(1))
    dpi = im.info.get("dpi", (600, 600))[0]
    w_in, h_in = im.size[0] / dpi, im.size[1] / dpi
    r = im.size[1] / im.size[0]
    j = i + 1
    while lines[j] == "":
        j += 1
    assert lines[j].startswith("*Figure"), f"line {i + 1}: no caption"
    k = j
    while k < len(lines) and lines[k] != "":
        k += 1
    cap = lines[j:k]
    label = re.match(r"^\*Figure([^*:]*)", cap[0]).group(1).strip(" .") or "(unnumbered)"
    cap_chars = sum(len(x) for x in cap)
    t, chars, bold_heads = k, 0, 0
    while t < len(lines) and not clearing(lines[t]):
        chars += len(lines[t])
        if re.match(r"^\*\*[^*]+\*\*\s*$", lines[t].strip()):
            bold_heads += 1
        t += 1
    stop = lines[t].strip()[:28] if t < len(lines) else "end of file"
    next_is_fig = t < len(lines) and lines[t].startswith("![") and all(x == "" for x in lines[k:t])
    need_rule = 300 * (0.52 * 6.7 * r + 0.9)
    cap_h = 0.15 + cap_chars / 330
    need_cap = 300 * (0.52 * 6.7 * r + cap_h)
    rows.append(dict(line=i + 1, label=label, file=Path(m.group(1)).name, px=im.size, dpi=dpi, w=w_in, h=h_in, r=r,
                     cap_lines=len(cap), cap_chars=cap_chars, cap_h=cap_h, chars=chars, need_rule=need_rule,
                     need_cap=need_cap, stop=stop, next_is_fig=next_is_fig, bold_heads=bold_heads))

print(f"text width {TEXT_W} in; scale = displayed width / drawn width (lettering drawn at 8 pt prints at 8 x scale)")
for d in rows:
    size = "small" if d["w"] <= 4.5 else ("tall" if d["r"] >= 0.9 else "wide")
    disp = {"small": 0.52, "tall": 0.60, "wide": 1.0}[size] * TEXT_W
    print(f"{d['label']:>12} line {d['line']:>5} {d['file']:<42} {d['px'][0]:>5}x{d['px'][1]:<5} {d['dpi']:>5.0f} dpi "
          f"{d['w']:4.2f} x {d['h']:4.2f} in r={d['r']:.2f} -> {size:5s} scale(full) {TEXT_W / d['w']:.2f} "
          f"scale({size}) {disp / d['w']:.2f}")
    print(f"{'':>14} caption {d['cap_lines']} lines {d['cap_chars']} chars (~{d['cap_h']:.2f} in at 52 %); text after "
          f"{d['chars']} chars until '{d['stop']}'; float needs {0.8 * d['need_rule']:.0f} (rule) / "
          f"{0.8 * d['need_cap']:.0f} (with caption); next is a figure: {d['next_is_fig']}; bold-only lines {d['bold_heads']}")
