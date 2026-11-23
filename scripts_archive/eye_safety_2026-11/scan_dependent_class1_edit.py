"""§C4c subsection 1a: lidars whose Class 1 rating depends on the scan, what the rules require when the scan fails,
how fast a stalled scanner must switch its laser off, and what the safeguard has to cover; pointers in §0, §C0,
§C4c subsection 1 and §C4d(f); Appendix 1 and Appendix 2 entries.

Sources, read at source:
- 21 CFR 1040.10 (eCFR, current): (f)(9) "Scanning safeguard"; (e)(3)(i) scanned radiation measured with the
  acceptance direction moving "with an angular speed of up to 5 radians/second"; (e)(2)(i) tests include "start-up,
  stabilized emission, and shut-down".
- FDA, Laser Notice No. 56 (issued 8 May 2019, reissued 21 Feb 2023), printed pp. 3-4: FDA does not intend to
  enforce 1040.10(f)(9), among other sections, for products that conform to the comparable clauses of IEC 60825-1
  Ed. 3; p. 4, note to (f)(2) "Safety interlocks": the IEC standard requires redundancy or safe failure of interlocks
  indirectly, through the reasonably foreseeable single-fault sub-clause of its classification rules (4.3). The
  wording inserted below was restated afterwards by ln56_citation_fix.py.
- FARO knowledge base, safety information for the Focus scanners: Class 1 "Due to permanent rotation of the
  deflecting mirror"; Focus3D X 1,550 nm "below 500mW", Class 1 (IEC 60825-1:2007); Focus3D 905 nm, average power
  at most 20 mW, Class 3R.
- Laser Focus World (J. Hecht, 25 Sep 2019): Velodyne's 905 nm lidars are Class 1 "because the two milliwatt beams
  are scanning continually"; 9xx nm pump light in fibre lasers can pose a retinal risk.
- Luminar, US 9,874,635 B1 (Google Patents text): 0.1 µJ-1 mJ pulses, 100 kHz-5 MHz, 640 kHz example; an interlock
  line shuts the laser down or reduces its power on a fault, including "a failure of scanner 120".
- Lumentum, US 11,757,533 B2 (Google Patents text): hardware shutdown when a diffuser or cover is damaged or
  detached, because software "may be slow to react".

The arithmetic (pass time, duty factor, stall times at 1,550 and 905 nm, pulse-train bound) is written out in the
text; the limits are those of §C4c subsection 1.

Usage: scan_dependent_class1_edit.py <report.md> <expected sha256 prefix> [--write]
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

CFR = "https://www.ecfr.gov/current/title-21/chapter-I/subchapter-J/part-1040/section-1040.10"
LN56 = "https://www.fda.gov/media/110120/download"
FARO = "https://knowledge.faro.com/Hardware/Focus/Focus/Safety_Information_for_the_FARO_Laser_Scanner"
LFW = "https://www.laserfocusworld.com/blogs/article/14040682/safety-questions-raised-about-1550-nm-lidar"
LUMINAR = "https://patents.google.com/patent/US9874635B1/en"
LUMENTUM = "https://patents.google.com/patent/US11757533B2/en"

SUBSECTION = r"""### 1a. When the Class 1 rating depends on the scan

Subsection 1 showed that a scanned beam may carry far more energy than a stationary one; this subsection asks what happens when the scan stops. Many scanned lidars are Class 1 only because the beam keeps moving: a moving beam crosses an eye for about a millisecond per pass, while a stalled one sends its whole power into the same pupil. The rules treat a stall as a foreseeable fault, so such a product must switch its laser off or down before the limit is reached, and the wavelength and the power set how fast it must do so. In short, a stalled beam reaches the limit after a few hundred milliseconds at 905 nm, after 10–80 ms for a pulsed 1,550 nm fibre laser, and after a few milliseconds for an FMCW beam of watts [E, derived below].

**What the rules require** [P].
- **The class must survive a single fault.** IEC 60825-1:2014 assigns the class under reasonably foreseeable single-fault conditions (clause 4.3, the classification rules) [P, via FDA Laser Notice No. 56; §C4d(f)]. A scanner that stops or slows is such a fault, so a product that is Class 1 only while scanning must stay within Class 1 during a stall as well, which in practice means a safeguard that cuts or lowers the emission in time [E].
- **The US rule names the case.** Laser products "that emit accessible scanned laser radiation shall not, as a result of any failure causing a change in either scan velocity or amplitude, permit human access to laser radiation in excess of" the limits of their class [P, 21 CFR 1040.10(f)(9), "Scanning safeguard"]. FDA accepts conformance with IEC 60825-1 Ed. 3 in place of this paragraph, because the IEC single-fault rule supplies the same safe-failure requirement [P, Laser Notice No. 56, issued 2019 and reissued 21 Feb 2023, p. 4].
- **Two measurement rules matter for scanners.** For scanned radiation the measuring aperture's direction "shall change as needed to maximize detectable radiation, with an angular speed of up to 5 radians/second" [P, 21 CFR 1040.10(e)(3)(i)], which allows for an eye that follows a slow beam. Tests must also cover "start-up, stabilized emission, and shut-down" [P, 1040.10(e)(2)(i)], so a scanner that is spinning up or coasting down is part of the assessment [E].

**Why a moving beam is so much safer** [E]. A beam of diameter $d_{\rm b}$ swept at angular speed $\omega$ (rad/s) past an aperture of diameter $D_{\rm a}$ at distance $R$ overlaps it for $t_{\rm pass}=(D_{\rm a}+d_{\rm b})/(\omega R)$ per pass.
- A head spinning at 10 Hz sweeps $\omega=2\pi\times10=62.8$ rad/s, about 13 times the 5 rad/s that the measurement rule lets the aperture follow.
- At the 100 mm evaluation distance of subsection 1, with the 7 mm aperture and a 3 mm beam, $t_{\rm pass}=(7+3)\ {\rm mm}/(62.8\ {\rm rad\,s^{-1}}\times100\ {\rm mm})=1.6$ ms, consistent with the "about a millisecond" that Velodyne cites (table below).
- One pass per revolution exposes the aperture for $1.6\ {\rm ms}\times10\ {\rm Hz}=1.6\%$ of the time, so it receives about 1/63 of the beam's average power; a raster spreads the pulses further (subsection 1's table). A stall removes this factor, and the whole beam stays on the aperture.

**Who says or shows that the rating depends on the scan.** The makers below state it, or their own documents show the safeguard. The fourth column compares the stalled beam with the stationary Class 1 limits of subsection 1, 9.6 mW at 1,550 nm and 1.00 mW at 905 nm [E].

| Product or source | Light | What the maker says or shows | Stalled beam against the stationary limit [E] | Source |
|---|---|---|---|---|
| FARO Focus Premium, Core, M and S (survey scanners) | 1,550 nm | Class 1 "due to permanent rotation of the deflecting mirror": the eye "is exposed to the IR laser for only very short periods of time per revolution" [P] | Power not stated | FARO's safety page |
| FARO Focus3D X | 1,550 nm, "below 500mW" | Class 1 under IEC 60825-1:2007 [P] | Up to $500/9.6\approx52$ times | FARO's safety page |
| FARO Focus3D, an earlier model | 905 nm, at most 20 mW average | Class 3R, even while scanning [P] | $20/1.00=20$ times | FARO's safety page |
| Velodyne spinning lidars | 905 nm, ≈2 mW per beam | Class 1 "because the two milliwatt beams are scanning continually, so they would sweep across a person's eye in about a millisecond" [T, quoting Velodyne] | ≈2 times, if the whole beam enters the 7 mm aperture | Laser Focus World, 25 Sep 2019 |
| Luminar (patent filed 2017, priority 2015) | 1,550 nm; 0.1 µJ–1 mJ pulses at 100 kHz–5 MHz, 640 kHz in the example | An interlock line from the sensor head tells the laser to "shut down, stop emitting light, or reduce the power or energy of emitted light" on a fault; the faults include "a failure of scanner 120", a receiver failure, and a person or object within a threshold distance of the head [P] | 1 µJ at 640 kHz is 0.64 W, ≈67 times | US 9,874,635 B1 |
| Mirrorcle (MEMS mirrors) | Any | Class 1 on a continuously scanned beam "requires that the scan is reliably monitored" [P] | — | §C4d(f) |
| Lumentum (flash emitter; patent) | Any | A hardware circuit cuts the emitter if its diffuser or cover is damaged or detached, because a software controller "may be slow to react" and "laser radiation levels may exceed safety thresholds" before it acts [P] | The same dependence, on the diffuser rather than the scan | US 11,757,533 B2 |

How to read the table. A survey scanner is a tripod-mounted instrument that maps buildings and terrain. A patent shows a design its owner protected, not necessarily the product it ships. Class 3R allows up to five times the Class 1 limit and calls for care with direct viewing.

**How fast a stalled design must switch off** [E]. The time a stalled beam takes to reach the limit is the budget for detecting the stall and cutting the laser.
- **1,550 nm.** For exposures shorter than 0.35 s the limit is a radiant exposure of $10^{4}\ {\rm J\,m^{-2}}$ over a 1 mm aperture, i.e. 7.85 mJ (subsection 1). A stalled beam of average power $P$, of which a fraction $\eta$ enters that aperture, reaches it after $t_{\rm stall}=7.85\ {\rm mJ}/(\eta P)$. For a Gaussian beam of $1/e^2$ diameter $d_{\rm b}$ centred on the aperture, $\eta=1-\exp[-2(0.5\ {\rm mm})^2/(d_{\rm b}/2)^2]$; a 3 mm beam gives $\eta=1-e^{-0.222}=0.20$.
  - Luminar's example, 0.64 W: $7.85\ {\rm mJ}/0.64\ {\rm W}=12$ ms with the whole beam in the aperture, and $7.85\ {\rm mJ}/(0.20\times0.64\ {\rm W})=61$ ms for a 3 mm beam.
  - FARO's Focus3D X at 0.5 W: 16 ms and 79 ms.
  - The FMCW model of §C7a emits 3.8 W at 10 Mpts/s (subsection 1). If a stall left all of it in one beam, the limit would come after 2.1 ms, or 10 ms for a 3 mm beam; spread over $n$ beams pointing in different directions, each time grows $n$-fold.
  - All these times are well under 0.35 s, so the 1 mm aperture applies.
- **905 nm.** For exposures between about 5 µs and 10 s the limit grows as $7\times10^{-4}\,C_4\,t^{0.75}$ J, with $C_4=2.57$ (Eq. \eqref{eq:c4-correction}); at 10 s it reproduces the 1.00 mW CW limit ($7\times10^{-4}\times2.57\times10^{0.75}\ {\rm J}/10\ {\rm s}=1.01$ mW). A stalled beam of average power $P$, wholly inside the 7 mm aperture, reaches it when $Pt=7\times10^{-4}C_4t^{0.75}$, i.e. after $t_{\rm stall}=(7\times10^{-4}C_4/P)^4$.
  - At Velodyne's 2 mW: $t_{\rm stall}=(1.80\times10^{-3}/2.0\times10^{-3})^4=0.90^4=0.65$ s.
  - The pulse-train rule can bind first. If the beam fires at 20 kHz, each pulse carries $2\ {\rm mW}/20\ {\rm kHz}=100$ nJ, which Eq. \eqref{eq:c5-pulse-train} allows only while $198\ {\rm nJ}\times(N/600)^{-1/4}\ge100$ nJ, i.e. up to $N=600\times(198/100)^4=9{,}200$ pulses, which take 0.46 s.
  - A beam wider than the aperture lengthens both times.
- **The budget therefore scales as $1/(\eta P)$:** a few hundred milliseconds at 905 nm, 10–80 ms for 1,550 nm pulsed lidars, and a few milliseconds for FMCW.

**What the safeguard has to cover** [E unless tagged].
- **Detecting the stall.** A spinning head or polygon reports its speed through the motor drive or an encoder, and a MEMS mirror or galvanometer through its drive or position-sense signal. An optical check, a photodiode at the edge of the scan that must see the beam at the expected rate, tests the scan itself rather than the motor. Luminar's patent adds a receiver failure and an object close to the head as triggers [P].
- **Acting in time.** The detection must cut the drive current, or lower the pulse energy, within $t_{\rm stall}$. At 1,550 nm a firmware loop that checked the motor speed every 100 ms would be too slow, which is the case Lumentum makes for a hardware shutdown path [P].
- **Starting and stopping.** The laser must not fire before the scanner is at speed and must stop as it coasts down, since the tests cover start-up and shut-down [P, 21 CFR 1040.10(e)(2)(i)].
- **Other single faults.** A laser driver stuck on, a damaged or detached diffuser or window [P, Lumentum], and, in fibre lasers, leaking 9xx nm pump light, which, unlike 1,550 nm light, reaches the retina [T, Laser Focus World, 2019].
- **In a car** the safeguard is a safety function under ISO 26262, the automotive functional-safety standard; the Fraunhofer system of §C4d(f) monitors its mirror with an automotive safety microcontroller [P].

**What this means for the choice of wavelength** [E].
- **1,550 nm's headroom belongs to the moving beam.** Its 10²–10³-fold advantage in pulse energy (subsection 1's table) holds only while the beam moves; with the scan stopped it shrinks to about 10× in power, the CW ratio. The eye safety of a 1,550 nm lidar therefore rests on its scanner and its safeguard as much as on its wavelength.
- **FMCW is the extreme case:** a CW beam of watts must be switched off within milliseconds of a stall.
- **905 nm designs already sit near the stationary limit** (≈10–100 nJ per pulse, subsection 1), so a stall over-exposes by a small factor and leaves hundreds of milliseconds to react. Flash designs have no scanner; they are rated as stationary sources and depend instead on their diffusers.

Sources: """ + " ; ".join([CFR, LN56, FARO, LFW, LUMINAR, LUMENTUM]) + "\n\n"

APPENDIX1_ITEM = (
    "- **Scan-dependent Class 1 (§C4c subsection 1a).** No lidar maker publishes how fast its scan-failure "
    "safeguard acts, what it monitors, or the class its product would have with the scan stopped, and certification "
    "reports are not public. Whether the ratings of Hesai's, Ouster's and Livox's scanning units depend on the scan "
    "is not stated in the documents found. The stall times of subsection 1a assume a Gaussian beam of 3 mm, or the "
    "whole beam in the aperture, and use the 1 mm aperture of the standard for exposures under 0.35 s.")

APPENDIX2_GROUP = (
    "**Eye safety when the scan stops (§C4c subsection 1a)**\n"
    "- 21 CFR 1040.10, eCFR ((f)(9) scanning safeguard; (e)(3)(i) scanned measurement at up to 5 rad/s; (e)(2)(i) "
    "start-up and shut-down): " + CFR + "\n"
    "- FDA, Laser Notice No. 56 (2019, reissued 21 Feb 2023; p. 4, (f)(9) and the IEC single-fault rule): " + LN56
    + "\n"
    "- FARO, safety information for the Focus laser scanners (Class 1 by mirror rotation; Focus3D X below 500 mW; "
    "Focus3D Class 3R): " + FARO + "\n"
    "- Laser Focus World, \"Safety questions raised about 1550 nm lidar\" (25 Sep 2019; Velodyne's scanning "
    "argument, pump leakage): " + LFW + "\n"
    "- Luminar, US 9,874,635 B1 (interlock line, scanner failure, pulse parameters): " + LUMINAR + "\n"
    "- Lumentum, US 11,757,533 B2 (hardware shutdown when a diffuser or cover fails): " + LUMENTUM + "\n"
    "\n")

EDITS = [
    # the new subsection, after the camera-damage blocks of subsection 1
    ("\n### 2. Sunlight: 940 nm, not 1,550 nm, has the lowest photon background\n",
     "\n" + SUBSECTION + "### 2. Sunlight: 940 nm, not 1,550 nm, has the lowest photon background\n"),
    # §C4c subsection 1, the architecture bullet
    ("Condition 1 (50 mm at 2 m) and the platform-motion allowance of TS 60825-19.\n",
     "Condition 1 (50 mm at 2 m) and the platform-motion allowance of TS 60825-19. Subsection 1a works out what a "
     "stalled scanner requires.\n"),
    # §C4d(f)
    ("Their larger exit apertures spread each pulse over more area, so less of it can enter a 7 mm pupil [E].\n",
     "Their larger exit apertures spread each pulse over more area, so less of it can enter a 7 mm pupil [E]. "
     "§C4c subsection 1a names products whose rating depends on the scan and estimates how fast each must switch "
     "off after a stall.\n"),
    # §C0
    ("The classification must hold under reasonably foreseeable single faults, including a stalled scanner (§C4d).",
     "The classification must hold under reasonably foreseeable single faults, including a stalled scanner "
     "(§C4c subsection 1a; §C4d)."),
    # §0
    ("Because each 1,550 nm photon carries less energy, that 10× in power is ≈17× more photons.\n",
     "Because each 1,550 nm photon carries less energy, that 10× in power is ≈17× more photons. The scanned "
     "allowance holds only while the beam moves, so a stalled 1,550 nm scanner must cut its laser within tens of "
     "milliseconds, and an FMCW one within a few (§C4c subsection 1a).\n"),
    # Appendix 2, after the camera-damage group
    ("\n**Glare and dirty glass (§E4.1)**\n", "\n" + APPENDIX2_GROUP + "**Glare and dirty glass (§E4.1)**\n"),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
lines = new.split("\n")
hits = [i for i, ln in enumerate(lines) if ln.startswith("- **Camera damage by lidar (§C4c subsection 1).**")]
assert len(hits) == 1, f"Appendix 1 camera-damage line found {len(hits)} times"
lines[hits[0]] = lines[hits[0]] + "\n" + APPENDIX1_ITEM
new = "\n".join(lines)
assert "\r" not in new
print(f"{len(EDITS)} substring edits, 1 appended item; sha256 before {sha[:12]}, after "
      f"{hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
