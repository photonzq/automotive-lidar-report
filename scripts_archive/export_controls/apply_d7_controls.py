"""Section D7 "Policy and controls": catalogue any-one-of caveat, 6A008.j.2 wording, and a laser-emitter bullet. Hash-guarded.

  python apply_d7_controls.py --dry   # check anchors and print the new block; nothing is written
  python apply_d7_controls.py         # write the live report (aborts if it changed after being read)
"""
import hashlib
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")

INTRO_OLD = ("China's lidar export controls miss automotive units, because their thresholds sit far beyond automotive "
             "specifications. No national FMCW programme or FMCW-specific test was found.")
INTRO_NEW = ("China's lidar export controls miss most automotive units: five of their six thresholds sit far beyond "
             "automotive specifications, and only the pulse-width criterion could catch a short-pulse time-of-flight "
             "design. US and Wassenaar laser controls miss automotive emitters by large margins. No national FMCW "
             "programme or FMCW-specific test was found.")

HEAD_OLD = ("- **China's Dec 2023 export catalogue** (item 73, lidar systems) restricts the export of lidar technology for "
            "systems with any of the following [P, MOST PDF, page read]:")
HEAD_NEW = ("- **China's Dec 2023 export catalogue** (item 73, lidar systems) restricts the export of lidar technology for "
            "systems meeting any one of the following (\u201c\u7b26\u5408\u4ee5\u4e0b\u4efb\u4e00\u6761\u4ef6\u201d) "
            "[P, MOST PDF, p. 25]:")

PARA_OLD = ("  Automotive units fall far outside it. Taking 0.1° as a representative automotive angular resolution "
            "(LightIC's Lark, above, quotes 0.1° × 0.08°), it converts as $0.1^\\circ=0.1\\times\\pi/180$ rad "
            "$\\approx1{,}745$ µrad, about 87 times the 20 µrad line ($1{,}745/20\\approx87$). The **2 mm ranging-accuracy "
            "threshold could catch industrial FMCW metrology** (挚感 claims µm-level ranging) [E]. The 20 µrad criterion "
            "mirrors US/Wassenaar ECCN 6A008.j.2, which controls coherent-detection lidar below that angular resolution "
            "[P, partially verified]. An ECCN (Export Control Classification Number) is the code under which an item "
            "appears on the US Commerce Control List; the Wassenaar Arrangement is the multilateral export-control regime "
            "whose lists the US and its allies implement.")

PARA_NEW = [
    ("  Automotive units fall far outside it on angular resolution. Taking 0.1° as a representative automotive angular "
     "resolution (LightIC's Lark, above, quotes 0.1° × 0.08°), it converts as $0.1^\\circ=0.1\\times\\pi/180$ rad "
     "$\\approx1{,}745$ µrad, about 87 times the 20 µrad line ($1{,}745/20\\approx87$). Range, peak power and angular "
     "accuracy also clear their lines comfortably [E]. **Pulse width is the exception.** Because any one criterion "
     "suffices, a time-of-flight design with pulses shorter than 1 ns would meet the item on that criterion alone; "
     "automotive pulsed lasers typically run pulses of a few nanoseconds, so the margin is small [E]. The item restricts "
     "technology exports from China, not shipments of lidar units. The **2 mm ranging-accuracy threshold could catch "
     "industrial FMCW metrology** (挚感 claims µm-level ranging) [E]. The 20 µrad criterion mirrors US/Wassenaar ECCN "
     "6A008.j.2, which controls lidar that both uses coherent (heterodyne or homodyne) detection and has an angular "
     "resolution finer than 20 µrad [P]. An ECCN (Export Control Classification Number) is the code under which an item "
     "appears on the US Commerce Control List; the Wassenaar Arrangement is the multilateral export-control regime whose "
     "lists the US and its allies implement."),
    ("- **Laser emitters under US and Wassenaar rules** [P: 15 CFR part 774, supplement no. 1, as of 24 Sep 2026; "
     "Wassenaar 2025 list]. Lasers fall under ECCN 6A005, a national-security control: a licence is needed for exports "
     "to China but not to Japan, South Korea or EU states. Its thresholds are set on average or CW (continuous-wave) "
     "power, or on pulse energy together with peak power, never on peak power alone, so lidar's high-peak, "
     "low-duty-cycle pulses stay far below them."),
    ("  - A 905 nm multi-junction pulsed diode at peak power $P_{\\rm pk}=100$ W, pulse width $\\tau=5$ ns and "
     "repetition rate $f=100$ kHz averages $\\bar P=P_{\\rm pk}\\,\\tau f=100\\times(5\\times10^{-9})\\times10^{5}=0.05$ W, "
     "500 times below the 25 W line for a multimode diode (6A005.d.1.b.1) [E]. Such diodes are not on the control list "
     "at all (EAR99); ams OSRAM's SPL PL90 is listed as EAR99 [S]."),
    ("  - At 1,550 nm, every single-mode diode, and any non-tunable laser averaging more than 1 W, falls under ECCN "
     "6A995. This US-only entry carries anti-terrorism controls only: a licence is needed only for embargoed "
     "destinations, Russia and Belarus, military end users in China and a few other countries, and listed parties. A "
     "pulsed fiber source with pulse energy $E_p=2$ µJ at $f=1$ MHz averages $\\bar P=E_p f=2$ W, $20/2=10$ times below "
     "the 20 W single-mode line (6A005.b.7.a.2). The 3.0–11.4 W FMCW transmit budgets of §C7b 2(i) sit "
     "$50/11.4\\approx4.4$ to $50/3.0\\approx17$ times below the 50 W single-mode CW line (6A005.a.7.a) [E]."),
    ("  - Two wavelength edges matter for design. Above 1,555 nm the fiber and solid-state lines fall to 1 W "
     "(6A005.a.8 and b.8), so the same 2 W source at 1,560 nm would need a licence for China. Above 1,570 nm the "
     "single-mode diode line falls from 2.0 W to 0.5 W (6A005.d.1.a) [P]."),
    ("  - A widely swept source boosted above 1 W by an erbium fiber amplifier may count as a \"tunable\" laser, which "
     "6A005.c.3 controls above 1 W beyond 1,400 nm; that reading is unsettled [E]. An FMCW chirp of "
     "$\\Delta\\nu=1$–10 GHz spans only $\\Delta\\lambda=\\lambda^2\\Delta\\nu/c\\approx8$–80 pm at 1,550 nm, within one "
     "laser transition, so it is not tunable in this sense."),
    ("  - A complete automotive lidar matches no listed entry, since 6A008.j.2 (above) needs both coherent detection and "
     "a resolution finer than 20 µrad; it is most likely EAR99 [E]."),
]

raw = REPORT.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
text = raw.decode("utf-8")
assert "\r\n" not in text, "report has CRLF line endings"
lines = text.split("\n")


def find(line):
    hits = [i for i, x in enumerate(lines) if x == line]
    if len(hits) != 1:
        sys.exit(f"anchor found {len(hits)} times; nothing written: {line[:70]}")
    return hits[0]


i_intro, i_head, i_para = find(INTRO_OLD), find(HEAD_OLD), find(PARA_OLD)
assert i_intro < i_head < i_para, "anchors out of order"
new_text = "\n".join([INTRO_NEW, HEAD_NEW] + PARA_NEW)
for word in ("corrected", "updated", "revised", "added", " now ", " new "):
    assert word not in new_text.lower(), f"versioning word in new text: {word!r}"
for chunk in [INTRO_NEW, HEAD_NEW] + PARA_NEW:
    assert chunk.count("$") % 2 == 0, f"unbalanced $ in: {chunk[:60]}"

lines[i_para:i_para + 1] = PARA_NEW
lines[i_head] = HEAD_NEW
lines[i_intro] = INTRO_NEW
out = "\n".join(lines).encode("utf-8")
print(f"anchors at lines {i_intro + 1}, {i_head + 1}, {i_para + 1}; sha {h0[:12]}; size {len(raw)} -> {len(out)} bytes")
if "--dry" in sys.argv:
    print("dry run; nothing written\n")
    print(new_text)
    sys.exit(0)
if hashlib.sha256(REPORT.read_bytes()).hexdigest() != h0:
    sys.exit("report changed after it was read; nothing written")
REPORT.write_bytes(out)
print("written; new sha", hashlib.sha256(out).hexdigest()[:12])
