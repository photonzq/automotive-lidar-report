import hashlib, re, sys
from pathlib import Path

here = Path(__file__).parent
rp = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
DRY = "--dry" in sys.argv

raw = rp.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
s = raw.decode("utf-8")
assert "\r\n" not in s
print("read", len(raw), "bytes, sha", h0[:12])
lines = s.split("\n")
problems = []


def idx(prefix, exact=False):
    hits = [i for i, l in enumerate(lines) if (l == prefix if exact else l.startswith(prefix))]
    if len(hits) != 1:
        problems.append(("idx", prefix[:70], len(hits)))
        return None
    return hits[0]


def sub_line(prefix, old, new):
    i = idx(prefix)
    if i is None:
        return
    if lines[i].count(old) != 1:
        problems.append(("sub", prefix[:50], old[:50], lines[i].count(old)))
        return
    lines[i] = lines[i].replace(old, new)


# ---------------------------------------------------------------- 1. §C7b subsection 2 (d)-(summary)
i_d = idx("**(d) The laser's chirp speed and linearity: a cost, not the floor.**")
i_3 = idx("### 3. The channel tax: channels, power and receivers", exact=True)
if i_d is not None and i_3 is not None:
    old_block = "\n".join(lines[i_d:i_3])
    assert old_block.count("\\tag{99}") == 1 and old_block.count("\\tag{100}") == 1, "old block tags"
    assert "**(e) Laser linewidth caps the *useful* chirp length from above.**" in old_block
    assert "- In practice, then, one coherent channel at 200 m delivers at most" in old_block
    new_block = (here / "c7b_block.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
    nb = "\n".join(new_block)
    assert nb.count("\\tag{99}") == 1 and nb.count("\\tag{100}") == 1
    lines[i_d:i_3] = new_block + [""]

# ---------------------------------------------------------------- 2. §C7b subsection 2 intro sentence
sub_line("This subsection asks how long one FMCW channel must stay on each point (its dwell)",
         "Readout electronics, chirp linearity, laser linewidth and scanning speed each constrain the chirp length further.",
         "The ADC rate and the laser's chirp rate and tuning range set further lower bounds on the chirp length, scanning sets an upper bound, and laser linewidth multiplies the energy each point needs (items (c)–(h)).")

# ---------------------------------------------------------------- 3. §C7b subsection 1 item (e): lead and coherence bullet
sub_line("**(e) What CW light does cost FMCW in photons.**",
         "Two things, both modest at today's channel powers.",
         "Two things: a round-trip dead time, modest at today's channel powers, and a coherence loss set by the laser's linewidth and the range.")
i = idx("- **Coherence cap.** A ramp can integrate coherently for at most")
if i is not None:
    assert lines[i + 1].startswith("  - At 30 mW and 100 kHz linewidth that is")
    assert lines[i + 2].startswith("  - At the 16 mW silicon limit")
    lines[i:i + 3] = [
        r"- **Coherence loss.** Laser phase noise does not cap how long a ramp can integrate. It removes a range-dependent share of the beat power from the coherent FFT peak and leaves $\eta_{\rm coh}=e^{-2\pi\Delta\nu\,\tau}$ in it (subsection 2(e), Eq. (99)), where $\Delta\nu$ is the laser's linewidth, the spread of its optical frequency caused by phase noise.",
        r"  - The energies of this subsection leave the loss out, so they hold for a laser narrow enough that $\eta_{\rm coh}\approx1$: ≲27 kHz for a 1 dB loss at 200 m (Eq. (9005)).",
        r"  - Otherwise the requirement becomes $E_{\rm opt}/\eta_{\rm coh}$. A 100 kHz laser at 200 m keeps $\eta_{\rm coh}=e^{-2\pi\times10^{5}\times1.33\times10^{-6}}=e^{-0.84}=0.43$, so the central 0.30 µJ becomes 0.70 µJ. At 300 m it keeps 0.28, a 3.5× penalty.",
    ]

# ---------------------------------------------------------------- 4. §C7b short answer: two bullets after the steering bullet
i = idx("  - No steerer changes the single-mode collection rule that fixes FMCW's photons per point.", exact=True)
if i is not None:
    lines[i + 1:i + 1] = [
        r"- **A faster or wider-tuning laser does not help either, at realistic channel powers** (subsection 2(g)). Each ramp's useful window is the longest of four floors: photons, ADC rate, laser chirp rate and laser tuning range.",
        r"  - At 300 m with ≤30 mW per channel, photons set a 7.5–14 µs window. That needs only a 1.1–1.3 GHz sweep at ≈$10^{14}$ Hz/s, so a faster laser shortens nothing.",
        r"  - The ADC floor binds next, above ≈35 mW per channel with 1 GS/s converters. The laser binds only in photon-rich channels (≳100 mW each at 300 m).",
        r"- **At the sensor level, most of the power is the light itself** (subsection 2(h)). For 10 Mpts/s at 300 m, ≈30 of ≈46 W is the useful optical energy per point divided by the CW laser's wall-plug efficiency, $\dot NE_{\rm opt}/(\eta_{\rm coh}\eta_{\rm WPE})$.",
        r"  - No split of the light among channels can reduce that term. The levers are fewer photons per point (collection, speckle, coherence) and more efficient lasers, not more power per channel.",
        r"  - Laser linewidth enters through $\eta_{\rm coh}=e^{-2\pi\Delta\nu\cdot2R/c}$: with a 100 kHz laser the same sensor needs ≈130 W.",
    ]

# ---------------------------------------------------------------- 5. §C7a(f)
i = idx("**(f) Coherence and chirp: solved as components, not yet as integrated automotive parts.**")
if i is not None:
    assert lines[i + 1].startswith("- Linewidth ≲60–120 kHz for 250 m [P, Waymo].")
    assert lines[i + 2].startswith("- Integrated alternatives: SiN self-injection-locked lasers")
    assert lines[i + 3].startswith("- **Very fast chirps buy little:**")
    very_fast = lines[i + 3]
    lines[i:i + 4] = [
        r"**(f) Coherence and chirp: solved as components, not yet as integrated automotive parts.** The laser must have a narrow linewidth and a linear chirp; parts exist that do both, but not yet as integrated, qualified automotive components. §C7b subsection 2(d)–(h) derives the requirements; for 15 cm resolution at 300 m they are:",
        r"- **Linewidth.** Laser phase noise leaves a fraction $\eta_{\rm coh}=e^{-2\pi\Delta\nu\cdot2R/c}$ of the beat power in the coherent FFT peak (Eq. (99)); the rest is lost to detection. It does not limit how long a chirp can be (§C7b subsection 2(e)).",
        r"  - A 1 dB loss allows $\Delta\nu\lesssim18$ kHz at 300 m (27 kHz at 200 m), and 3 dB allows 55 kHz (83 kHz) (Eq. (9005)). Waymo's ≲60–120 kHz for 250 m [P] corresponds to a 2.7–5.5 dB loss [E].",
        r"  - Commercial distributed-feedback lasers (DFBs) reach tens of kHz. At 300 m the SiN self-injection-locked laser below (42 kHz) loses 2.3 dB and the TFLN E-DBR laser (378 kHz) 21 dB [E].",
        r"- **Chirp.** The laser must sweep ≈1.1–1.9 GHz continuously and without mode hops, in ramps of ≈4–16 µs repeated as a 30–120 kHz triangle. Its residual frequency error must stay below ≈$c/(16R)=62.5$ kHz (Eq. (9003)), i.e. a chirp-rate error below $\Delta R/R=5\times10^{-4}$.",
        r"  - The ramp length is set by the photon budget, not by the laser. The implied chirp rate, $0.7$–$4.4\times10^{14}$ Hz/s, is modest, and a faster laser does not raise the point rate at ≤30 mW per channel (§C7b subsection 2(g)).",
        r"- **Parts.** Waymo's thermally chirped DFB with pre-distortion holds <100 kHz error over 1 GHz (nonlinearity $<10^{-4}$) [P]: enough at 200–250 m, marginal at 300 m by Eq. (9003) [E].",
        r"  - Integrated alternatives: SiN self-injection-locked lasers (42 kHz, 0.65% nonlinearity) and thin-film lithium niobate (TFLN) E-DBR lasers (378 kHz, 1.5%) [P, Bianconi et al. 2025]. Read as fractional chirp-rate errors, those nonlinearities are 13–30× above the $5\times10^{-4}$ that 15 cm at 300 m tolerates, so they need pre-distortion or resampling [E].",
        r"  - Snigirev et al.'s 12 PHz/s ($1.2\times10^{16}$ Hz/s) TFLN laser (500 MHz excursion; ranging with an EDFA at 4 mW to 3 m) is [R]. Its 500 MHz excursion alone limits the resolution to ≈0.3–0.4 m (§C7b subsection 2(g)).",
        very_fast,
        r"- **What is missing** is not a part that does this on a bench but an integrated source, qualified at 105 °C, that does it while feeding watts of amplified CW light to hundreds of channels. At 10 Mpts/s and 300 m the light alone is ≈30 of ≈46 W of sensor power (§C7b subsection 2(h)).",
    ]

# ---------------------------------------------------------------- 6. §C7 coherence paragraph
i = idx("**Coherence.** A laser with a Lorentzian line of full width $\\Delta\\nu$ (Hz) has a coherence length")
if i is not None:
    assert "order-of-magnitude design heuristic" in lines[i]
    lines[i] = (r"**Coherence.** A laser with a Lorentzian line of full width $\Delta\nu$ (Hz) has a coherence length, the path difference over which its phase stays correlated, of roughly $L_c=c/(\pi\Delta\nu)$, with $c$ the speed of light. "
                r"Requiring $L_c$ to exceed the 600 m round trip to a 300 m target gives $\Delta\nu\lesssim c/(\pi\times600\ {\rm m})=3\times10^{8}/1{,}885\approx160$ kHz. "
                r"That condition marks where detection becomes marginal, not a design point. At the round-trip delay $\tau=2R/c$, only a fraction $e^{-2\pi\Delta\nu\tau}$ of the beat power stays in the coherent FFT peak, so $L_c=2R$ keeps $e^{-2}\approx14\%$, an 8.7 dB loss. "
                r"Holding the loss to 1–3 dB needs ≈18–55 kHz at 300 m (§C7b subsection 2(e)). Practical FMCW sensitivity also depends on chirp linearity, dwell time and processing.")

# ---------------------------------------------------------------- 7. §C0 subsection 2 table row and derivation bullet
i = idx("| Coherence | Lorentzian coherence length $L_c=c/(\\pi\\Delta\\nu)$, to exceed the round trip |")
if i is not None:
    old = lines[i]
    assert old.count("|") == 5
    lines[i] = r"| Coherence | Coherent share of the beat power $\eta_{\rm coh}=e^{-2\pi\Delta\nu\cdot2R/c}$; Lorentzian coherence length $L_c=c/(\pi\Delta\nu)$ | 100 kHz: $L_c\approx950$ m, yet only 28% of the beat stays coherent at 300 m (43% at 200 m) | §C7, §C7b |"
sub_line("  - **Coherence length:** $L_c=c/(\\pi\\Delta\\nu)=3.0\\times10^8/(\\pi\\times10^5)\\approx955$ m",
         "shown as ≈950 m.",
         r"shown as ≈950 m. **Coherent share:** $2\pi\times10^{5}\times2.0\times10^{-6}=1.26$, so $e^{-1.26}=0.28$ at 300 m; $2\pi\times10^{5}\times1.33\times10^{-6}=0.84$, so $e^{-0.84}=0.43$ at 200 m (§C7b subsection 2(e)).")

# ---------------------------------------------------------------- 8. wavelength-steered laser bullet
sub_line("- The laser must therefore be **widely tunable, narrow-linewidth",
         "($\\lesssim$ 60–160 kHz, from §C7's 300 m heuristic and Waymo's 250 m design, §C10.3)",
         "(≲20–55 kHz at 300 m for a 1–3 dB coherent loss, §C7b subsection 2(e); Waymo designs to ≲60–120 kHz at 250 m, §C10.3)")

# ---------------------------------------------------------------- 9. research leverage points around Eq. (165)
sub_line("- **Integrated narrow-linewidth, linear-chirp lasers with SOAs**",
         "Coherence needs about $\\Delta\\nu\\lesssim160$ kHz at 300 m, from the condition that the coherence length exceed the round trip:",
         "The coherence-length rule of thumb gives about $\\Delta\\nu\\lesssim160$ kHz at 300 m, from the condition that the coherence length exceed the round trip:")
sub_line("  Here $L_c$ is the coherence length (m), $c$ the speed of light, $\\Delta\\nu$ the laser linewidth (full width at half maximum, Hz), assuming a Lorentzian line shape",
         "(§C0 subsection 2). Chirp linearity drives range precision.",
         "(§C0 subsection 2). That condition still leaves only $e^{-2}\\approx14\\%$ of the beat in the coherent FFT peak, an 8.7 dB loss; a 1–3 dB design point needs ≈18–55 kHz at 300 m (§C7b subsection 2(e)). Chirp linearity drives range precision.")

if problems:
    print("PROBLEMS:")
    for p in problems:
        print("  ", p)
    sys.exit(1)

text = "\n".join(lines)

# ---------------------------------------------------------------- 10. global renumbering
TAG = re.compile(r"\\tag\{(\d+)\}")
REF = re.compile(r"\bEqs?\.\s*\(\d+\)(?:\s*(?:,|and|–|-|to|or)\s*\(\d+\))*")
tags = [int(m.group(1)) for m in TAG.finditer(text)]
assert len(tags) == len(set(tags)), "duplicate tags"
olds = [t for t in tags if t < 9000]
assert olds == list(range(1, len(olds) + 1)), "old tags not sequential"
news = [t for t in tags if t >= 9000]
assert news == list(range(9001, 9010)), news
mapping = {t: k + 1 for k, t in enumerate(tags)}
refs_before = [int(x) for m in REF.finditer(text) for x in re.findall(r"\((\d+)\)", m.group(0))]
bad = sorted({n for n in refs_before if n not in mapping})
assert not bad, ("dangling refs", bad)
text = TAG.sub(lambda m: "\\tag{%d}" % mapping[int(m.group(1))], text)


def fix(m):
    return re.sub(r"\((\d+)\)", lambda mm: "(%d)" % mapping[int(mm.group(1))], m.group(0))


text = REF.sub(fix, text)
tags2 = [int(m.group(1)) for m in TAG.finditer(text)]
assert tags2 == list(range(1, len(tags2) + 1))
refs_after = [int(x) for m in REF.finditer(text) for x in re.findall(r"\((\d+)\)", m.group(0))]
assert len(refs_after) == len(refs_before) and all(1 <= n <= len(tags2) for n in refs_after)
print("tags", len(olds), "->", len(tags2), "; refs", len(refs_after), "; old 99 ->", mapping[99], "; old 165 ->", mapping[165])
print("new eq numbers:", {k: mapping[k] for k in news})

# ---------------------------------------------------------------- 11. hygiene checks
assert "\t" not in text
for w in ["corrected", "updated", "revised"]:
    c_old, c_new = s.count(w), text.count(w)
    if c_new != c_old:
        print("WORD COUNT CHANGE", w, c_old, "->", c_new)
print("'added' count", s.count("added"), "->", text.count("added"))

if DRY:
    (here / "report_dry.md").write_text(text, encoding="utf-8")
    print("dry run written to the scratch folder")
    sys.exit(0)

now = rp.read_bytes()
if hashlib.sha256(now).hexdigest() != h0:
    print("ABORT: report changed during processing")
    sys.exit(2)
rp.write_bytes(text.encode("utf-8"))
(here / "report_after_fmcw.md").write_bytes(text.encode("utf-8"))
print("written", len(raw), "->", len(text.encode("utf-8")))
