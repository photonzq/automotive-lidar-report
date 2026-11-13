"""§E4.1 after reading the built pages: the substitutions behind the quoted numbers, and two wording fixes.

- The common-cause sentence now refers to §E5's beta-factor model (a cause that takes out two channels at once)
  instead of implying that §E5 counts the camera and the driver as its two redundant channels.
- Substitutions are added for the veil 10 deg from the sun, the zone's width along the horizon, the night contrast
  of road and target, the lidar zone through a dirty window, the dead-time factor and the 1 deg case, the halogen
  counts per bin, the window's scattered fraction and loss, and the coherent design's range with the window.
- The LED-at-905-nm statement is marked as an extrapolation of the datasheet's tail [E].
Every number is printed by build/figures/glare_veil.py.

Usage: glare_veil_fix.py <report.md> <expected sha256 prefix> [--write]
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
    (r"In the low-sun case below, the veil through an average windshield is 8.4 times the difference between "
     r"pedestrian and road, so an unevenness of 12% across the glass is as large as the pedestrian's whole contrast.",
     r"In the low-sun case below, the veil through an average windshield 10° from the sun, "
     r"$38{,}000\times0.0663=2{,}520$ cd/m², is 8.4 times the 301 cd/m² between road and pedestrian, so an "
     r"unevenness of 12% across the glass is as large as the pedestrian's whole contrast."),
    (r"For a sun 10° high that zone meets the road up to 19° (average) or 24° (dirty) to either side of the sun's "
     r"direction, a sector 39–49° wide.",
     r"For a sun 10° high that zone meets the road up to 19° (average) or 24° (dirty) to either side of the sun's "
     r"direction, a sector 39–49° wide: on the horizon the azimuth difference $\Delta\phi$ from the sun follows "
     r"$\cos\Delta\phi=\cos21.6^\circ/\cos10^\circ$, so $\Delta\phi=19^\circ$ for the average windshield."),
    (r"At night the glare source is a pair of oncoming headlamps, and the targets are about 2,000 times darker than "
     r"by day [E]:",
     r"At night the glare source is a pair of oncoming headlamps, and the targets are about 2,000 times darker than "
     r"by day (a road of 0.16 cd/m² against 339) [E]:"),
    (r"In a supervised (L2) system the driver is the fallback for the situations the camera handles badly, so in "
     r"glare the two channels that §E5 counts as redundant fail together.",
     r"In a supervised (L2) system the driver is the fallback for the situations the camera handles badly, so glare "
     r"is a common cause in the sense of §E5's β-factor model: it takes out the camera and its human fallback at "
     r"once."),
    (r"That happens within 0.3° of the sun through new glass, 0.8° through cleaned glass, 2.6° through an average "
     r"window and 3.5° through a dirty one;",
     r"That happens within 0.3° of the sun through new glass, 0.8° through cleaned glass, 2.6° through an average "
     r"window and 3.5° through a dirty one, where $6.6\,\theta^{-1.73}=0.75$ gives "
     r"$\theta=(6.6/0.75)^{1/1.73}=3.5^\circ$;"),
    (r"Paralyzable dead time, with the high case's $x_0=0.244$ (live fraction 0.784, §C0 subsection 4.2), lowers "
     r"these to 0.62 and 0.71. At 1° from the sun the range falls to 0.57–0.58, or 0.33–0.36 with dead time.",
     r"Paralyzable dead time, with the high case's $x_0=2\times0.122=0.244$ (live fraction $e^{-0.244}=0.784$, §C0 "
     r"subsections 4.2 and 4.3), multiplies the range factor by $e^{-(m-1)x_0/4}$ (§C5b with $a=1$), which gives "
     r"$(e^{-2.6\times0.244}/3.6)^{1/4}=0.62$ and 0.71. At 1° from the sun the veil alone is "
     r"$\pi\times6.6\times38{,}000/90{,}000=8.8$ times the specification's background, and the range falls to "
     r"0.57–0.58, or 0.33–0.36 with dead time."),
    (r"falls to about 1% of its peak at 750 nm and ends near 780 nm (KW H2L531.TE datasheet, p. 9) [P], so it adds "
     r"no background at 905, 940 or 1,550 nm.",
     r"falls to about 1% of its peak at 750 nm and ends near 780 nm (KW H2L531.TE datasheet, p. 9) [P]; "
     r"extrapolating that steep tail, it adds no measurable background at 905, 940 or 1,550 nm [E]."),
    (r"treated as a 3,200 K blackbody, 12 lx of its light carries $12\times2.67\times10^{-5}=3.2\times10^{-4}$ W m⁻² "
     r"nm⁻¹ at 940 nm. Through a dirty window this adds at most 0.0064 counts per 1 ns bin to the night background "
     r"of 0.01 (§C0 subsection 4.3).",
     r"treated as a 3,200 K blackbody (Planck's law per lux of photopic illuminance), 12 lx of its light carries "
     r"$12\times2.67\times10^{-5}=3.2\times10^{-4}$ W m⁻² nm⁻¹ at 940 nm. Through a dirty window ($f=0.781$ sr⁻¹ at "
     r"3.43°) its veil is $\pi\times0.781\times3.2\times10^{-4}/(0.9\times0.39)=2.24\times10^{-3}$ of a sunlit white "
     r"scene at 940 nm, where full sun gives 0.39 W m⁻² nm⁻¹ (§C0 subsection 4.2). The high case counts 2.87 "
     r"background photons per 1 ns bin, summed over a point's ten shots (§C0 subsection 4.3), so the veil adds at "
     r"most $2.24\times10^{-3}\times2.87=0.0064$ counts per bin to the night background of 0.01."),
    (r"(Table II summed over 1–110°: $g=0.043$ average and 0.071 dirty), the two-way loss is $X=-20\log_{10}(1-g)$: "
     r"0.39 dB for an average window and 0.64 dB for a dirty one.",
     r"(Table II summed over 1–110°: $g=0.035+0.0058+0.0026=0.0434$ average and $0.057+0.0097+0.0045=0.0712$ "
     r"dirty), the two-way loss is $X=-20\log_{10}(1-g)$: $-20\log_{10}(1-0.0434)=0.39$ dB for an average window and "
     r"0.64 dB for a dirty one."),
    (r"The coherent 25 mm design of §C0 subsection 5.4, which reaches 200 m in clear air, reaches 177 m and 160 m "
     r"(12% and 20% less, with clear-air extinction included as in that subsection).",
     r"The coherent 25 mm design of §C0 subsection 5.4 ($z_R=257$ m), sized to reach 200 m in clear air, has a "
     r"budget of $10\log_{10}[1+(200/257)^2]$ plus the two-way clear-air loss over 200 m, 2.13 dB in all. With the "
     r"window it reaches the range $R$ at which $10\log_{10}[1+(R/257\ {\rm m})^2]$ plus the clear-air loss "
     r"(0.382 dB/km, both ways) equals $2.13\ {\rm dB}-X$: 177 m for 0.39 dB and 160 m for 0.64 dB, 12% and 20% "
     r"less."),
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
