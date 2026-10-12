"""Round 2, agent R2E_C10: build the edit list for sections C10-C10.7 (decisions 6 and 7 of round2_spec.md).

Reads the live report (read only), cuts every "old" span from it by anchors so that the text is exact, applies the
replacements, checks that each "old" occurs exactly once, and writes edits/round2/R2E_C10.json.
The numbers come from R2E_C10_numbers.py, round2_c10_3_power_table.py and coherent_mode_coverage.py.
Usage: python R2E_C10_build_edits.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]          # <report folder>
REPORT = ROOT / "automotive_perception_report_2026-09-27.md"
OUT = ROOT / "scripts_archive" / "readability_2026-10-03" / "edits" / "round2" / "R2E_C10.json"
text = REPORT.read_text(encoding="utf-8")
lo, hi = text.index("## C10. Can optical phased arrays"), text.index("# Part D")
edits, skipped = [], []


def span(start, end):
    assert text.count(start) == 1, ("start", start[:60], text.count(start))
    i = text.index(start)
    j = text.index(end, i) + len(end)
    return text[i:j]


def rep(old, pairs):
    new = old
    for a, b in pairs:
        assert new.count(a) == 1, ("rep", a[:70], new.count(a))
        new = new.replace(a, b)
    return new


def add(finding, old, new, why):
    assert text.count(old) == 1, ("old", old[:70], text.count(old))
    i = text.index(old)
    assert lo <= i and i + len(old) <= hi, ("outside C10", old[:60])
    edits.append({"id": f"R2E_C10-{len(edits) + 1:03d}", "finding": finding, "old": old, "new": new, "why": why})


D6 = "decision 6 (eta convention)"
D7 = "decision 7 (ToF at 940 nm, n_req 21.7, eta 0.164)"

# ---------------------------------------------------------------- C10 summary of verdicts
old = r"Ideal full-coverage coherent power does not grow as $1/\Omega_{\rm cell}$ (§C10.3; §C10.3a, item 4)."
add("summary of verdicts; decisions 6-7", old,
    old + r""" The gap does not close at camera-like pitch, however: at the 0.0125° of "2,000+ line" claims, ideal full-coverage coherent detection still needs 4.2–13× ToF's power (§C10.3).""",
    "States the conclusion the recomputed §C10.3 table supports (4.2-13x at 0.0125 deg).")

# ---------------------------------------------------------------- C10.2 item 5
add(f"round1 model_round2 [09_C10_part1] report #3; {D6}",
    r"$A_{\rm mode}$ the mode-equivalent collecting area (the effective area with which a single-mode receiver collects light scattered by a diffuse target), $\eta$ the detection efficiency and $\eta_{\rm OPA}$ the OPA's one-way power transmission.",
    r"$A_{\rm mode}$ the mode-equivalent collecting area (the effective area with which a single-mode receiver collects light scattered by a diffuse target, including its single-polarization and truncation factors), $\eta$ the end-to-end efficiency of the rest of the chain (optics × detector × mixing, without polarization or mode shape, which sit in $A_{\rm mode}$) and $\eta_{\rm OPA}$ the OPA's one-way power transmission.",
    "Defines eta on the report-wide convention.")

old = span(r"an ideal mode-equivalent collecting area $A_{\rm mode}=\lambda^2/\Omega_{\rm cell}=", r"The polarization factor of 0.5 assumes")
add(f"round1 model_round2 [09_C10_part1] report #3; {D6}", old,
    r"that beam's mode-equivalent collecting area $A_{\rm mode}=\tfrac{t^2}{2}\lambda^2/\Omega_{\rm cell}=0.419\times(1.55\ \mu{\rm m})^2/(8.73\times10^{-4}\ {\rm rad})^2=0.419\times3.15\ {\rm mm^2}=1.32$ mm², where $\Omega_{\rm cell}$ is the solid angle of one 0.05° cell ($8.73\times10^{-4}$ rad on a side) and $t^2/2=0.419$ is the Gaussian model's round-trip truncation factor $t^2=0.838$ times the single-polarization factor ½ (§C10.3b, Result 2), with $t$ the fraction of a Gaussian beam's power that the finite aperture passes one way; 1 W for 5 µs; and $\eta=0.8$, the detector's quantum efficiency with ideal mixing: the OPA's optical loss is counted separately in $\eta_{\rm OPA}$, so the design value 0.25 of §C0 subsection 10.1, which already contains a free-space chain's optics loss, would count it twice. The polarization factor ½ assumes",
    "Polarization and truncation move into A_mode (t^2/2 = 0.419); eta = 0.25.")

old = span(r"and a Lambertian return delivers the fraction $\rho A_{\rm mode}/(\pi R^2)=0.1\times3.15", r"would lower the results below by a further ≈16%.")
add(f"round1 model_round2 [09_C10_part1] report #3; {D6}", old,
    r"and a Lambertian return delivers the fraction $\rho A_{\rm mode}/(\pi R^2)=0.1\times1.32\ {\rm mm^2}/(\pi\times(200\ {\rm m})^2)=1.05\times10^{-12}$ of them to the mode. That gives about **41 photons in the mode before the efficiency and the OPA's loss** ($3.9\times10^{13}\times1.05\times10^{-12}=41$), and $41\times0.8=32.8$ after the efficiency.",
    "Recomputed on A_mode = 1.32 mm^2 and eta = 0.25; the truncation note is now inside A_mode.")

old = span(r"After one-way OPA losses of 1, 3 and 7 dB, about **25, 10 and 1.6 photons**", r"$39\times0.040=1.6$.")
add(f"round1 model_round2 [09_C10_part1] report #3; {D6}", old,
    r"After one-way OPA losses of 1, 3 and 7 dB, about **21, 8.2 and 1.3 photons** are detected. The monostatic path applies each loss twice, so the factors $\eta_{\rm OPA}^2$ are $10^{-0.2}$, $10^{-0.6}$ and $10^{-1.4}$: $32.8\times0.631=20.7$, $32.8\times0.251=8.23$ and $32.8\times0.0398=1.31$.",
    "Detected photons after OPA loss on the new convention.")

old = span(r"about 9–26 W per beam at 5 µs dwell and 3 dB one-way loss [E]", r"$60\times26.4\approx1{,}590$ W;")
add(f"round1 model_round2 [09_C10_part1] report #3; {D6}; decision 1 (dwell T_int + 2 tau)", old,
    r"about 11–31 W per beam at 5 µs of chirp and 3 dB one-way loss [E], if the looks share one receive mode (wavelength or time diversity): ≈11 W for four-look and ≈31 W for single-look detection, or ≈1.0–2.9 kW for 92 beams at 12 Mpts/s. With polarization or spatial diversity each look adds a receive mode, which cuts the four-look figure about 4×, to ≈2.7 W per beam (≈250 W for 92 beams). At 3 dB one-way loss, 1 W for 5 µs yields 8.23 detected photons, so 88.5 photons need $88.5/8.23=10.8$ W and 259 need $259/8.23=31.5$ W. Each beam emits that power for its whole dwell, the 5 µs of chirp plus the round trips, $T_{\rm dwell}=5\ \mu{\rm s}+2.67\ \mu{\rm s}=7.67$ µs at 200 m (§C7b, Eq. (107); item 7 below), so 12 Mpts/s needs $12\times10^{6}\ {\rm s^{-1}}\times7.67\ \mu{\rm s}=92$ beams, hence $92\times10.8\approx990$ W to $92\times31.5\approx2{,}900$ W, and $92\times10.8/4\approx250$ W with one receive mode per look;",
    "Per-beam powers on eta = 0.8 with t^2/2 in A_mode; beam count from the dwell 5 us + 2 tau = 7.67 us (decision 1): 92 beams, 1.0-2.9 kW.")

add(f"{D6} (power per beam)",
    r"a waveguide platform that carries watts: Si trunks (the input waveguides that carry the full power before it is split among elements) are limited by two-photon absorption, a nonlinear loss that grows with intensity (§C8.2), whereas SiN handles watts;",
    r"a waveguide platform that carries ≈3–31 W per beam: Si trunks (the input waveguides that carry the full power before it is split among elements) are limited by two-photon absorption, a nonlinear loss that grows with intensity (§C8.2), whereas SiN handles watts (the Si–SiN chip of §C10.2b takes 20 W in, against the 11–31 W per beam of looks that share one receive mode);",
    "The per-beam power the platform must carry follows from the recomputed first bullet.")

add(f"{D6} (full-field OPA power); decision 1 (dwell T_int + 2 tau)",
    r"In practical terms, full-field coverage by a long-range OPA would need 0.5–1.6 kW of optical power,",
    r"In practical terms, full-field coverage by a long-range OPA would need about 1.0–2.9 kW of optical power at 3 dB one-way loss (≈0.25 kW if every look has its own receive mode),",
    "Conclusion restated from the recomputed 990-2,900 W (92 beams at the 7.67 us dwell).")

# ---------------------------------------------------------------- C10.2b finding 7
old = span(r"That sits at the low end of the cell-filling link budget", r"$5\ \mu{\rm J}\times259/9.8=132\ \mu{\rm J}$).")
add(f"{D6} (quotes §C10.2 item 5)", old,
    r"That sits at or just below the low end of the cell-filling link budget of §C10.2, item 5, Eq. (134): 54–157 µJ for 88.5–259 photons at 3 dB one-way loss (5 µJ yields 8.23 detected photons there, so $5\ \mu{\rm J}\times88.5/8.23=54\ \mu{\rm J}$ and $5\ \mu{\rm J}\times259/8.23=157\ \mu{\rm J}$). The 8,192-element array's 0.01° × 0.039° beam is much narrower than a 0.05° cell, so each of its samples collects more photons than a cell-filling one would, at the price of sparse coverage (§C10.3a, item 4).",
    "The measured energies no longer sit at the low end of the recomputed cell-filling budget; says so and why.")

# ---------------------------------------------------------------- C10.3 headline and assumptions
old = span(r"For a 10% target at 200 m and 10 Hz, gap-free single-mode coherent coverage", r"the gap closes only as ToF cells approach the diffraction limit.")
add(f"round1 model_round2 [09_C10_part1] follow-up section 4 (headline); {D6}; {D7}", old,
    r"""For a 10% target at 200 m and 10 Hz, gap-free single-mode coherent coverage of 120° × 25° needs 58.5–175.5 W at a non-fading threshold of 10–30 detected photons, and about 518–1,515 W once speckle fading is counted under the report's per-point rule, or ≈130 W if each of four looks has its own receive mode (caveat 4; §C10.2, item 5); ToF needs 0.215–13.8 W at 0.1° to 0.0125° sampling. Coherent designs therefore sample sparsely with narrow beams. The gap closes only as ToF cells approach the diffraction limit: at the 0.0125° pitch of "2,000+ line" claims, coherent coverage still needs 4.2–13× ToF's power.""",
    "Headline on the recomputed Eq. (139) values, with the multi-mode speckle case.")

add(f"round1 model_round2 [09_C10_part1] report #3; {D6}",
    r"The values of $\eta$ below are assumed to include whatever polarization loss applies.",
    r"That factor ½ is not part of $\eta$: with the round-trip truncation $t^2=0.838$ it forms the factor $t^2/2=0.419$ of the mode-equivalent area (Eq. (138) below), as in §C0 subsection 10.1 and §C10.3b.",
    "eta convention of §C0 subsection 10.1.")

add(f"round1 model_round2 [09_C10_part1] consistency flag (ToF model); {D7}",
    r"- *Sunlight.* For ToF, $N_{\rm req}=20$ already corresponds to bright sun (§C0 subsection 10.3: 17.3 counts for an ideal counter, 25 in the §C7a model); at night ≈5 counts suffice.",
    r"- *Sunlight.* For ToF, $N_{\rm req}=21.7$ already corresponds to bright sun: an ideal counter needs 15.0 counts there (§C0 subsection 10.3), and the §C7a model applies its ×1.45 implementation margin, $1.45\times15.0\approx21.7$. The dead time that sunlight causes is in $\eta$, through the SPAD live fraction 0.885. At night ≈5 counts suffice.",
    "ToF requirement of the 940 nm model with the 0.05 x 0.05 deg background.")

add(f"{D6}",
    r"- $\eta$, the end-to-end detection efficiency: the fraction of photons arriving at the aperture that are detected, including optics transmission and quantum efficiency;",
    r"- $\eta$, the end-to-end efficiency from photons arriving at the aperture to signal photoelectrons: optics × detector, and for the coherent receiver also × mixing (§C0 subsection 10.1). It excludes the coherent receiver's polarization and mode-shape factors, which sit in $A_{\rm mode}$, and for SPAD ToF it includes the live fraction that sunlight-induced dead time leaves;",
    "Symbol definition on the report-wide convention.")

old = span(r"  $$n_{\rm coh}=\frac{\eta\rho E_{\rm pt}}{E_{\rm ph}}\frac{A_{\rm mode}}{\pi R^2},\qquad A_{\rm mode}\sim", r"subject to polarization, beam shape, truncation and receive-mode overlap.")
add(f"{D6} (Eq. (138) rewritten in place)", old,
    r"""  $$n_{\rm coh}=\frac{\eta\rho E_{\rm pt}}{E_{\rm ph}}\frac{A_{\rm mode}}{\pi R^2},\qquad A_{\rm mode}\simeq\frac{t^2}{2}\,\frac{\lambda^2}{\Omega_{\rm cell}} \tag{138}$$

  If the received mode is widened until its Gaussian 1/e² spot fills one angular cell, the Gaussian model of §C10.3b gives the second relation (its Eq. (147) with a footprint fraction of one), where $t^2/2=0.419$ is the round-trip truncation $t^2=0.838$ times the single-polarization factor ½; at 0.05° it is 1.32 mm². The two cell-angle factors (in $E_{\rm pt}$ and in $A_{\rm mode}$) then cancel. That is the ideal full-coverage scaling used below, subject to beam shape and receive-mode overlap at the cell corners.""",
    "The cell-filling mode area carries t^2/2, as in §C10.3b; tag kept.")

add(f"{D6} (Eq. (139) rewritten in place)",
    r"\Omega_{\rm FOV}}{\rho\,\lambda^2\,\eta},\\",
    r"\Omega_{\rm FOV}}{\rho\,\tfrac{t^2}{2}\lambda^2\,\eta},\\",
    "P_coh with the single-polarization and truncation factor; tag kept.")

old = span(r"$N_{\rm req}$ is the number of detected photons required per sample. The assumed inputs are", r"which is why §C10.2b and the product comparison below rank by $R^2\Omega$.")
add(f"round1 model_round2 [09_C10_part1] consistency flag (ToF model) and [10_C10_part2] follow-up #3; {D6}; {D7}", old,
    r"""$N_{\rm req}$ is the number of detected photons (photoelectrons) required per sample, the $n_{\rm req}$ of §C0 subsection 10.1. The ToF inputs are those of the 940 nm SPAD model of §C0 subsection 10.3 and §C7a: a 25 mm aperture, $N_{\rm req}=21.7$ [E: the bright-sun requirement with the model's ×1.45 margin] and $\eta=0.5\times0.37\times0.885=0.164$ [E: optics × PDE × the bright-sun live fraction]. They belong to the model's 0.05° × 0.05° macro-pixel and are held fixed across the grids below, although a coarser pixel collects more sunlight and a finer one less. Single-mode coherent: 1550 nm, $N_{\rm req}$ 10–30 and $\eta=0.25$, the design value of §C0 subsection 10.1, needing **58.5–175.5 W** on every grid, because $\Omega_{\rm cell}$ does not appear in $P_{\rm coh}$; Waymo's measured chain efficiency of 0.112 (§C0 subsection 10.1) would raise this 2.23-fold. Both powers grow as $R^2\Omega_{\rm FOV}$, which is why §C10.2b and the product comparison below rank by $R^2\Omega$.""",
    "Inputs of decisions 6-7 replace 905 nm, N_req 20, eta 0.15 and eta 0.3-0.1.")

add(f"{D6}; {D7}",
    r"and the ratio of the coherent power, which is 20–184 W on every grid, to it.",
    r"and the ratio of the coherent power, which is 58.5–175.5 W on every grid, to it.",
    "Recomputed coherent power.")

old = span(r"| 0.1° × 0.1° | 0.23 W | 87–800× |", r"| 0.0125° × 0.0125° | 14.4 W | 1.4–13× |")
add(f"round1 model_round2 [09_C10_part1] report #31 (0.1° row); {D6}; {D7}", old,
    rep(old, [("| 0.23 W | 87–800× |", "| 0.215 W | 272–816× |"), ("| 0.45 W | 45–410× |", "| 0.43 W | 136–408× |"),
              ("| 0.9 W | 23–200× |", "| 0.86 W | 68–204× |"), ("| 3.6 W | 6–51× |", "| 3.44 W | 17–51× |"),
              ("| 14.4 W | 1.4–13× |", "| 13.8 W | 4.2–13× |")]),
    "Table from Eq. (139) on the new inputs; every ratio from the unrounded P_ToF.")

old = span(r"- Common inputs: $\Omega_{\rm FOV}=(120^\circ\times25^\circ)(\pi/180)^2=0.914$ sr (small-angle approximation", r"$184/0.90=204\approx200$.")
add(f"{D6}; {D7}", old,
    r"""- Common inputs: $\Omega_{\rm FOV}=(120^\circ\times25^\circ)(\pi/180)^2=0.914$ sr (small-angle approximation: the product of the two field angles in radians), $R=200$ m, $f_{\rm frame}=10$ Hz and $\rho=0.1$, so $\pi R^2f_{\rm frame}\,\Omega_{\rm FOV}/\rho=1.148\times10^{7}\ {\rm m^2\,s^{-1}\,sr}$.
- Coherent: $E_{\rm ph}=hc/\lambda=1.282\times10^{-19}$ J and $\lambda^2=2.403\times10^{-12}$ m² at 1550 nm, and $t^2/2=0.419$. With $N_{\rm req}=10$ and $\eta=0.25$, $P_{\rm coh}=10\times1.282\times10^{-19}\times1.148\times10^{7}/(0.419\times2.403\times10^{-12}\times0.25)=58.5$ W, i.e. 5.85 W per detected photon per sample; $N_{\rm req}=30$ triples it, to 175.5 W. With the measured efficiency 0.112 instead of 0.25, both rise $0.25/0.112=2.23$-fold, to 131 and 392 W.
- ToF: $E_{\rm ph}=2.113\times10^{-19}$ J at 940 nm and $A_{\rm rx}=\pi(12.5\ {\rm mm})^2=4.909\times10^{-4}$ m² for the 25 mm aperture. At 0.1° × 0.1°, $\Omega_{\rm cell}=(1.745\times10^{-3})^2=3.046\times10^{-6}$ sr, so $P_{\rm ToF}=21.7\times2.113\times10^{-19}\times1.148\times10^{7}/(4.909\times10^{-4}\times3.046\times10^{-6}\times0.164)=0.215$ W. Halving one cell side doubles $P_{\rm ToF}$, and halving both quadruples it.
- Ratio: $P_{\rm coh}/P_{\rm ToF}$ falls in proportion to $\Omega_{\rm cell}$. At 0.1° × 0.1°, $58.5/0.215=272$ and $175.5/0.215=816$; at 0.05° × 0.05°, $58.5/0.860=68$ and $175.5/0.860=204$.""",
    "Substitutions for the recomputed table.")

add(f"round1 model_round2 [09_C10_part1] report #3; {D6}",
    r"- It assumes a realizable cell-filling single mode with $A_{\rm mode}=\lambda^2/\Omega_{\rm cell}$ and no polarization or mode-shape penalty beyond the stated $\eta$.",
    r"- It assumes a realizable cell-filling single mode with $A_{\rm mode}=\tfrac{t^2}{2}\lambda^2/\Omega_{\rm cell}$ (1.32 mm² at 0.05°), which carries the single-polarization and truncation factors, and no further mode-shape penalty in $\eta$.",
    "Caveat on the new convention.")

old = span(r"- The numerical Gaussian model in §C10.3b applies a further factor $t^2/2\simeq0.42$", r"and ½ is the single-polarization factor for a depolarizing target.")
add(f"round1 model_round2 [09_C10_part1] report #3; {D6}", old,
    r"- The factor $t^2/2=0.419$ in Eq. (139) is that of the numerical Gaussian model in §C10.3b, on the convention of §C0 subsection 10.1, in which $\eta$ excludes truncation and polarization. Here $t=0.915$ is the Gaussian aperture-truncation (power) factor, the fraction of a Gaussian beam's power that passes the finite aperture, counted on transmit and on receive ($t^2=0.838$), and ½ is the single-polarization factor for a depolarizing target.",
    "The factor is applied in Eq. (139) rather than left as a further caveat.")

add(f"{D6}; {D7}",
    r"to 200 m needs 20–184 W, even before speckle fading (caveat 4).**",
    r"to 200 m needs 58.5–175.5 W, even before speckle fading (caveat 4).**",
    "Recomputed coherent power.")

old = span(r"Power parity arrives only near **0.004–0.01°**", r'That is beyond even "camera-like" resolution.')
add(f"round1 model_round2 [09_C10_part1] report #31 (item 2); {D6}; {D7}", old,
    rep(old, [("**0.004–0.01°**", "**0.0035–0.006°**"),
              (r"$\theta_{\rm cell}=0.1^\circ/\sqrt{87}=0.011^\circ$ to $0.1^\circ/\sqrt{800}=0.0035^\circ$",
               r"$\theta_{\rm cell}=0.1^\circ/\sqrt{272}=0.0061^\circ$ to $0.1^\circ/\sqrt{816}=0.0035^\circ$"),
              (r"=0.905\ \mu{\rm m}/22\ {\rm mm}=4.1\times10^{-5}$ rad $=0.0023^\circ$",
               r"=0.940\ \mu{\rm m}/22.2\ {\rm mm}=4.2\times10^{-5}$ rad $=0.0024^\circ$"),
              ('That is beyond even "camera-like" resolution.',
               'That is beyond even "camera-like" resolution, and finer than the 0.0125° of "2,000+ line" claims, at which full-coverage coherent detection still needs 4.2–13× ToF\'s power.')]),
    "Parity cells and diffraction limit at 940 nm; states that 0.0125 deg leaves a 4.2-13x gap.")

old = span(r"Sunlight is already included in the ToF $N_{\rm req}$, which corresponds to bright sun", r"background model in §C6(d)).")
add(f"{D7} (full-sun case)", old,
    r"Sunlight is already included in the ToF inputs: $N_{\rm req}=21.7$ is the bright-sun requirement, and $\eta=0.164$ contains the bright-sun live fraction 0.885. A fully sunlit scene of reflectance 0.9 doubles the background to $3.66\times10^{8}$ counts/s per macro-pixel, which lowers the live fraction to $e^{-0.244}=0.784$ (each of the nine SPADs has $r\tau_d=3.66\times10^{8}/9\times6\ {\rm ns}=0.244$) and raises the ideal requirement only to 17.3 counts ($b=3.66\times10^{8}\ {\rm s^{-1}}\times1\ {\rm ns}\times10\times0.784=2.87$ background counts per bin, threshold 15; §C0 subsection 10.3; background model in §C6(d)). $P_{\rm ToF}$ then rises by $(17.3/15.0)\times(0.885/0.784)=1.30$.",
    "Full-sun case on the 0.05 x 0.05 deg background (was 'only to ≈20').")

old = span(r"   - The choices of $N_{\rm req}$ and $\eta$ move the numbers by a few times but do not change the scaling.", r"which brings the four-look case back to ≈45 W at $\eta=0.3$.")
add(f"round1 model_round2 [09_C10_part1] report #15; {D6}", old,
    rep(old, [("move the numbers by a few times but do not change the scaling.",
               r"move the numbers but do not change the scaling with $\Omega_{\rm cell}$. The measured chain efficiency of 0.112 in place of the design value 0.25 raises the coherent powers 2.23×, and speckle raises the coherent $N_{\rm req}$ to 88.5–259, 3–26× the 10–30 of the table (next bullet)."),
              (r"that raises the coherent requirement to about **180–1,590 W** ($P_{\rm coh}\propto N_{\rm req}/\eta$ from Eq. (139): 88.5 photons at $\eta=0.3$ give $20.4\times88.5/10=181$ W, and 259 photons at $\eta=0.1$ give $20.4\times(259/10)\times3=1{,}590$ W).",
               r"that raises the coherent requirement to about **518–1,515 W**: at fixed $\eta$, Eq. (139) gives $P_{\rm coh}\propto N_{\rm req}$, 5.85 W per detected photon, so 88.5 photons need $58.5\times88.5/10=518$ W and 259 need $58.5\times259/10=1{,}515$ W, while the non-fading per-point 39.1 needs $58.5\times3.91=229$ W."),
              (r"which brings the four-look case back to ≈45 W at $\eta=0.3$.",
               r"which brings the four-look case back to ≈130 W ($518/4$).")]),
    "Speckle and fading cases recomputed from their own N_req at eta = 0.25.")

add(f"{D6}; {D7}",
    r"The ideal full-coverage example (20–184 W)",
    r"The ideal full-coverage example (58.5–175.5 W)",
    "Recomputed coherent power.")

# ---------------------------------------------------------------- C10.3a item 1
old = span(r"Per sample, the number of photoelectrons this yields after the shared efficiency $\eta_{\rm common}$ (defined below) is", r"$$n_{\rm aperture}=\frac{\eta_{\rm common}\,\rho}{E_{\rm ph}}")
add(f"round1 model_round2 [10_C10_part2] report #1 (one efficiency symbol); symbol scheme; {D6}", old,
    rep(old, [(r"after the shared efficiency $\eta_{\rm common}$ (defined below)", r"after the efficiency $\eta$ (defined below)"),
              (r"\frac{\eta_{\rm common}\,\rho}", r"\frac{\eta\,\rho}")]),
    "One shared-efficiency symbol, eta, as the symbol scheme sets; Eq. (142) rewritten in place.")

add(f"round1 model_round2 [10_C10_part2] report #1; {D6}",
    r"- $\eta_{\rm common}$ is the efficiency both receiver types share: common transmission and photoconversion losses. It excludes coherent mode selection and polarization loss, which are counted separately below.",
    r"- $\eta$ is the end-to-end efficiency of §C10.3 and §C0 subsection 10.1, from photons at the aperture to photoelectrons: optics × detector, and for the coherent receiver also × mixing. It excludes coherent mode selection and polarization loss, which are counted separately below, in $A_{\rm mode}$.",
    "Same definition as §C10.3.")

old = span(r"Example: 1 W, 1.2 M samples per frame, 10 Hz, 200 m, 10% reflectivity, $\eta_{\rm common}=0.1$.", r"a well-matched multimode pixel can use nearly all of these after the common losses.")
add(f"round1 model_round2 [10_C10_part2] follow-up #3 (item 1 example); {D7}", old,
    rep(old, [(r"10% reflectivity, $\eta_{\rm common}=0.1$.",
               r"10% reflectivity and an illustrative $\eta=0.1$ for both receivers, so that only the apertures and wavelengths differ (§C10.3 uses the model values, 0.25 for coherent and 0.164 for ToF)."),
              (r"(photons at the aperture times $\eta_{\rm common}$)", r"(photons at the aperture times $\eta$)"),
              (r"times $\eta_{\rm common}\rho=0.01$", r"times $\eta\rho=0.01$"),
              (r"ToF aperture at 905 nm has about **15** [E: $83\ {\rm nJ}/2.19\times10^{-19}\ {\rm J}=3.8\times10^{11}$ photons",
               r"ToF aperture at 940 nm has about **15** [E: $83\ {\rm nJ}/2.11\times10^{-19}\ {\rm J}=3.9\times10^{11}$ photons")]),
    "ToF example at 940 nm; one efficiency symbol.")

add(f"round1 model_round2 [10_C10_part2] follow-up #3; {D7}",
    r"more photons per joule at 1550 nm ($1550/905=1.71$)",
    r"more photons per joule at 1550 nm ($1550/940=1.65$)",
    "Photon-per-joule ratio against 940 nm.")

add(f"round1 model_round2 [10_C10_part2] report #1; symbol scheme",
    r"under this example's shared $\eta_{\rm common}=0.1$",
    r"under this example's common $\eta=0.1$",
    "One efficiency symbol.")

# ---------------------------------------------------------------- C10.3a item 2
add(f"round1 model_round2 [10_C10_part2] follow-up #3 (item 2 table); {D7}",
    "| ToF, 25 mm aperture, 0.05° cell, 905 nm | ≈22 cm | ≈1 mm | ≈460 (485) | All (incoherent sum) |",
    "| ToF, 25 mm aperture, 0.05° cell, 940 nm | ≈22 cm | ≈1.1 mm | ≈420 (451) | All (incoherent sum) |",
    "ToF speckle size and count at 940 nm (coherent_mode_coverage.py).")

add(f"round1 model_round2 [10_C10_part2] follow-up #3; {D7}",
    r"$0.905\ \mu{\rm m}\times250\ {\rm m}/22\ {\rm cm}=1.0$ mm (ToF)",
    r"$0.940\ \mu{\rm m}\times250\ {\rm m}/22\ {\rm cm}=1.1$ mm (ToF)",
    "940 nm.")

add(f"round1 model_round2 [10_C10_part2] follow-up #3; {D7}",
    r"ToF: $491\ {\rm mm^2}\times(8.73\times10^{-4})^2/(0.905\ \mu{\rm m})^2=456\approx460$, against 485 from Goodman's formula.",
    r"ToF: $491\ {\rm mm^2}\times(8.73\times10^{-4})^2/(0.940\ \mu{\rm m})^2=423\approx420$, against 451 from Goodman's formula.",
    "940 nm mode counts.")

# ---------------------------------------------------------------- C10.3a item 4
add(f"round1 model_round2 [10_C10_part2] report #1; {D6} (Eq. (144) rewritten in place)",
    r"\;=\; K \;=\; \frac{\eta\,\rho\,P\,\lambda^2}{\pi R^2\,f_{\rm frame}\,\Omega_{\rm FOV}\,E_{\rm ph}} \tag{144}$$",
    r"\;=\; K \;=\; \frac{t^2}{2}\,\frac{\eta\,\rho\,P\,\lambda^2}{\pi R^2\,f_{\rm frame}\,\Omega_{\rm FOV}\,E_{\rm ph}} \tag{144}$$",
    "K carries t^2/2, consistent with Eq. (147); tag kept.")

add(f"round1 model_round2 [10_C10_part2] report #1; {D6}",
    r"- $\eta$ is the end-to-end efficiency, playing the role of $\eta_{\rm common}$ in item 1 (it excludes truncation and polarization);",
    r"- $\eta$ is the end-to-end efficiency of Eq. (142), which excludes truncation and polarization; these enter through $t^2/2=0.419$, the round-trip truncation $t^2=0.838$ times the single-polarization factor ½ of the Gaussian model (§C10.3b);",
    "One efficiency symbol and the factor it excludes.")

add(f"round1 model_round2 [10_C10_part2] report #1; {D6}",
    r"combined with the antenna theorem for an ideal single mode, $A_{\rm mode}\,\Omega_{\rm footprint}\approx\lambda^2$.",
    r"combined with the antenna theorem in the form the Gaussian model gives it, $A_{\rm mode}\,\Omega_{\rm footprint}=\tfrac{t^2}{2}\lambda^2$ (Eq. (147) of §C10.3b, since one sample's footprint fraction is $\Omega_{\rm footprint}/\Omega_{\rm cell}$); an ideal single mode without truncation or polarization loss would have $\lambda^2$.",
    "Derivation of the t^2/2 in Eq. (144).")

old = span(r"For 200 m, 10% reflectivity, a 120° × 25° field ($\Omega_{\rm FOV}=0.914$ sr), 10 Hz and $\eta=0.1$ at 1550 nm", r"=0.163\ {\rm W^{-1}}$].")
add(f"round1 model_round2 [10_C10_part2] report #1 (0.068 per-watt bullet); {D6}", old,
    r"For 200 m, 10% reflectivity, a 120° × 25° field ($\Omega_{\rm FOV}=0.914$ sr), 10 Hz, the coherent design efficiency $\eta=0.25$ of §C10.3 and $t^2/2=0.419$ at 1550 nm ($\lambda^2=2.40\times10^{-12}$ m²), the per-watt budget constant $K/P$ is about **0.17 photoelectrons per watt** [E: $K/P=0.419\times0.25\times0.1\times2.40\times10^{-12}\ {\rm m^2}/(1.26\times10^{5}\ {\rm m^2}\times10\ {\rm s^{-1}}\times0.914\ {\rm sr}\times1.28\times10^{-19}\ {\rm J})=0.171\ {\rm W^{-1}}$].",
    "Budget constant on eta = 0.25 with t^2/2.")

old = span("| 1 W | 0.5% | 0.06% |", "| ≈200 W | 100% | 13% |")
add(f"{D6}", old,
    rep(old, [("| 1 W | 0.5% | 0.06% |", "| 1 W | 0.6% | 0.07% |"), ("| 5 W | 2.7% | 0.3% |", "| 5 W | 2.8% | 0.3% |"),
              ("| 100 W | 54% | 6.3% |", "| 100 W | 57% | 6.6% |"), ("| ≈200 W | 100% | 13% |", "| ≈175 W | 100% | 12% |")]),
    "Bounds from K/P = 0.171 per watt (the 20 W row is unchanged).")

old = span(r"the bound is $f_{\rm fp}=K/n_{\rm mode}=(K/P)\,P/n_{\rm mode}$, capped at one, with $K/P=0.163$", r"$0.163\times200/259=13\%$.")
add(f"{D6}", old,
    r"the bound is $f_{\rm fp}=K/n_{\rm mode}=(K/P)\,P/n_{\rm mode}$, capped at one, with $K/P=0.171$ W⁻¹ from above. For 20 W, $0.171\times20/30=11\%$ at 30 photoelectrons and $0.171\times20/259=1.3\%$ at 259. Full coverage at 30 photoelectrons needs $P=30/0.171=175$ W, the ≈175 W row, where 259 photoelectrons give $0.171\times175/259=12\%$. The 175 W is the $P_{\rm coh}$ of Eq. (139) for $N_{\rm req}=30$, as it must be, since both rest on the same cell-filling mode.",
    "Substitutions for the recomputed bounds; cross-check with Eq. (139).")

old = span(r"- The table is a bound for the stipulated $\eta=0.1$ **before**", r"not 54%.")
add(f"round1 model_round2 [10_C10_part2] report #1 (0.068 per-watt bullet); {D6}", old,
    r"- The table already contains the Gaussian model's single-polarization and truncation factor $t^2/2=0.419$ (the round-trip truncation factor $t^2=0.838$ times the single-polarization factor ½) and uses the design efficiency $\eta=0.25$. With the measured chain efficiency of 0.112 (§C0 subsection 10.1), $K/P$ falls to **0.077 photoelectrons per watt** ($0.171\times0.112/0.25$), and 100 W then yields about **26%** nominal footprint fraction at 30 photoelectrons ($0.077\times100/30$), not 57%.",
    "The t^2/2 factor is inside K; the remaining sensitivity is the measured efficiency.")

add(f"{D6}",
    r"cover only 0.5–11% of the scene with its nominal footprints at 30 photoelectrons per mode.",
    r"cover only 0.6–11% of the scene with its nominal footprints at 30 photoelectrons per mode.",
    "From the recomputed table.")

add(f"round1 model_round2 [10_C10_part2] follow-up #3 (item 4 ToF bullet); {D7}",
    r"in this 0.05° example sums of order 460 spatial speckles per polarization in one intensity detector, i.e. $N_{\rm mode}\sim N_{\rm spk}\approx460$",
    r"in this 0.05° example at 940 nm sums of order 420 spatial speckles per polarization in one intensity detector, i.e. $N_{\rm mode}\sim N_{\rm spk}\approx420$",
    "940 nm mode count.")

# ---------------------------------------------------------------- C10.3a item 5
add(f"round1 model_round2 [10_C10_part2] follow-up #3 (item 5 table); {D7}",
    "| ToF: 25 mm aperture, 520 SPAD macro-pixels × ≈460 modes, 2,400 scan columns | 5.5×10⁸ | 5.7×10⁸ | ≈100% |",
    "| ToF at 940 nm: 25 mm aperture, 520 SPAD macro-pixels × ≈420 modes, 2,400 scan columns | 5.1×10⁸ | 5.3×10⁸ | ≈100% |",
    "Mode-time slots at 940 nm.")

add(f"round1 model_round2 [10_C10_part2] follow-up #3; {D7}",
    r"ToF $491\ {\rm mm^2}\times0.914\ {\rm sr}/(0.905\ \mu{\rm m})^2=5.5\times10^{8}$",
    r"ToF $491\ {\rm mm^2}\times0.914\ {\rm sr}/(0.940\ \mu{\rm m})^2=5.1\times10^{8}$",
    "940 nm.")

add(f"round1 model_round2 [10_C10_part2] follow-up #3; {D7}",
    r"ToF $520\times460\times2{,}400=5.7\times10^{8}$",
    r"ToF $520\times423\times2{,}400=5.3\times10^{8}$",
    "940 nm.")

# ---------------------------------------------------------------- C10.3a item 7
old = span(r"The *efficiency-weighted aperture* is the collecting area", r"of a mirror-scanned FMCW unit.")
add(f"round1 model_round2 [10_C10_part2] follow-up #1 and [03_C0_part10] follow-up flag a; {D6}; {D7}", old,
    r"The *efficiency-weighted aperture* is the collecting area (the hard area for direct detection, $A_{\rm mode}$ for a coherent receiver) multiplied by the efficiency $\eta$ of §C10.3 (optics × detector, × mixing for a coherent receiver, and for SPAD ToF also the bright-sun live fraction). It is the area of a lossless, perfectly efficient detector that would yield the same signal photoelectrons. On the report's efficiencies, 0.164 for ToF and 0.25 for coherent, a 25 mm scanned ToF receiver keeps about **4–11×** the efficiency-weighted aperture of one mirror-scanned FMCW receiver at 100–300 m. The four receivers per point of §C7a narrow the gap to about 1.3× at 200 m.",
    "Ratio on the report-wide efficiencies (4-11x per receiver, 1.3x with four).")

old = span("| Long-range scanned ToF | ≈15–30 mm |", "| Solid-state flash ToF | ≈3–5 mm | Staring étendue (bite c) | Small |")
add(f"round1 model_round2 [10_C10_part2] follow-up #1, report #6, report #7, follow-up #10; {D6}; {D7}", old,
    rep(old, [("| ≈85 mm² for 25 mm (optics ≈0.5 × PDE ≈0.35) |",
               r"| ≈80 mm² for 25 mm ($\eta=0.5\times0.37\times0.885=0.164$: optics × PDE × bright-sun live fraction) |"),
              ("| ≈15–40 mm² for 20 mm at 100–300 m, including §C10.3b's near-field, polarization and mode-shape losses, quantum efficiency (QE) ≈0.8 and ≈1 dB loss each way; a far-field-only estimate of ≈80 mm² is optimistic |",
               r"| ≈7–21 mm² per receiver for 20 mm at 100–300 m: §C10.3b's mode-equivalent areas, which include its near-field, polarization and mode-shape losses, times $\eta=0.25$; a far-field-only estimate of ≈27 mm² is optimistic |"),
              ("| ≈25 mm² down to below 1 mm², with 3–10 dB on-chip loss each way |",
               "| ≈4 mm² (8 mm) down to ≈0.07 mm² (1 mm) before on-chip loss, and 4–100× less after 3–10 dB of it each way |"),
              ("| Staring étendue (bite c) | Small |", "| Staring étendue (bite c) | ≈1–3 mm² |")]),
    "Efficiency-weighted apertures on eta 0.164 (ToF) and 0.25 (coherent).")

old = span(r"- Long-range ToF: $\pi(12.5\ {\rm mm})^2\times0.5\times0.35=491\times0.175=86$ mm².", r"and 0.4 mm² for 1 mm.")
add(f"round1 model_round2 [10_C10_part2] follow-up #1, report #6, report #7, follow-up #10; {D6}; {D7}", old,
    r"""- Long-range ToF: $\pi(12.5\ {\rm mm})^2\times0.164=491\times0.164=80$ mm². In a fully sunlit scene the live fraction falls to 0.784, and the area to $491\times0.5\times0.37\times0.784=71$ mm².
- Mirror-scanned FMCW, per receiver: the mode-equivalent areas of §C10.3b, Result 2 (28.8, 63.7 and 82.0 mm² at 100, 200 and 300 m), times $\eta=0.25$ (optics × detector × mixing; polarization and mode shape are already in $A_{\rm mode}$): $28.8\times0.25=7.2$ mm² at 100 m, 15.9 mm² at 200 m and 20.5 mm² at 300 m. ToF's 80 mm² is $80/20.5=3.9$ to $80/7.2=11$ times larger; the four receivers per point of §C7a collect $4\times15.9\approx64$ mm² at 200 m, $80/64\approx1.3$ times less than ToF. The far-field-only figure takes the far-field limit of item 2, $A_{\rm mode}\to t^2\pi w_0^2/2=0.838\times\pi(9\ {\rm mm})^2/2=107$ mm² (the hard area divided by 2.9), times the same $\eta$: $107\times0.25=27$ mm².
- OPA or FPA chip: the far-field $A_{\rm mode}$ of the hard aperture (its area divided by 2.9, item 2) times $\eta=0.25$, before on-chip loss: $\pi(8\ {\rm mm})^2/4/2.9\times0.25=4.3$ mm² for 8 mm and $0.785\ {\rm mm^2}/2.9\times0.25=0.07$ mm² for 1 mm. An on-chip loss of 3–10 dB each way multiplies these by $10^{-0.6}=0.25$ to $10^{-2}=0.01$.
- Solid-state flash ToF: a 3–5 mm staring aperture times the same $\eta$, $\pi(1.5\ {\rm mm})^2\times0.164=1.2$ mm² to $\pi(2.5\ {\rm mm})^2\times0.164=3.2$ mm². IMX479 staring over 120° gets a ≈3.8 mm aperture, 1.8% of the 28.5 mm scanned column's area (item 5, bite (c)), i.e. $\pi(1.9\ {\rm mm})^2\times0.164=1.9$ mm².""",
    "Substitutions for the item 7 table.")

add(f"{D7}",
    r"against ≈5 counts for SPAD ToF at night and ≈17 in bright sun (§C0 subsection 10.3)",
    r"against ≈5 counts for SPAD ToF at night and ≈15 in bright sun (§C0 subsection 10.3)",
    "Bright-sun ideal requirement with the 0.05 x 0.05 deg background.")

old = span(r"In a fully sunlit scene this cuts the effective PDE by about a third", r"§C7a's central case uses a live fraction of 0.784)")
add(f"{D7} (dead fractions at the 0.05° × 0.05° macro-pixel)", old,
    r"In a fully sunlit scene of reflectance 0.9 this cuts the effective PDE by about a sixth at 940 nm behind a 10 nm filter, and by about a half to three-quarters at 905 nm behind 20–40 nm filters (§C6(d): at PDE 0.3 and the 0.05° × 0.05° macro-pixel, Eq. (82) with $r\tau_d=2.97\times10^{8}/9\times6\ {\rm ns}=0.20$ gives a dead fraction of 16.5–18% at 940 nm, and 42–77% at 905 nm; §C7a's central case uses a live fraction of 0.885)",
    "Dead fractions halve with the background; live fraction of the model's central case.")

add(f"{D6}",
    r"0.5–11% for item 4's bounds at 1–20 W",
    r"0.6–11% for item 4's bounds at 1–20 W",
    "From the recomputed item 4 table.")

# ---------------------------------------------------------------- C10.3b
add(f"round1 model_round2 [10_C10_part2] follow-up #3 (Result 1); {D7}",
    r"- **ToF model:** a hard 25 mm aperture with a polarization-insensitive multimode pixel whose field of view equals one mesh cell.",
    r"- **ToF model:** a hard 25 mm aperture at 940 nm, the wavelength of the SPAD model of §C0 subsection 10 and §C7a, with a polarization-insensitive multimode pixel whose field of view equals one mesh cell.",
    "States the ToF wavelength of the model.")

old = span("| ToF, 25 mm, 905 nm, 0.1° pixel | 1,888 | 1,826 |", "| ToF, 25 mm, 905 nm, 0.025° pixel | 127 | 114 |")
add(f"round1 model_round2 [10_C10_part2] follow-up #3 (Result 1); {D7}", old,
    rep(old, [("| ToF, 25 mm, 905 nm, 0.1° pixel | 1,888 | 1,826 |", "| ToF, 25 mm, 940 nm, 0.1° pixel | 1,752 | 1,692 |"),
              ("| ToF, 25 mm, 905 nm, 0.05° pixel | 485 | 456 |", "| ToF, 25 mm, 940 nm, 0.05° pixel | 451 | 423 |"),
              ("| ToF, 25 mm, 905 nm, 0.025° pixel | 127 | 114 |", "| ToF, 25 mm, 940 nm, 0.025° pixel | 118 | 106 |")]),
    "Goodman and simple counts at 940 nm (coherent_mode_coverage.py).")

add(f"{D7}",
    r"e.g. $491\ {\rm mm^2}\times(8.73\times10^{-4})^2/(0.905\ \mu{\rm m})^2=456$ at 0.05°",
    r"e.g. $491\ {\rm mm^2}\times(8.73\times10^{-4})^2/(0.940\ \mu{\rm m})^2=423$ at 0.05°",
    "940 nm.")

add(f"{D7}",
    r"The resolution race cuts ToF's mode count from about 1,900 to about 130, still far above one.",
    r"The resolution race cuts ToF's mode count from about 1,750 to about 120, still far above one.",
    "From the 940 nm Result 1 rows.")

old = span(r"- A 20 mm monostatic aperture at 100–200 m sees about 3–6 speckles and keeps about 1/5 to 1/11", r"where $\Omega_{\rm cell}=\theta_{\rm cell}^2$ is the solid angle of one mesh cell.")
add(f"round1 model_round2 [10_C10_part2] report #18 and follow-up #1; {D6}; {D7}", old,
    r"""- A mirror-scanned coherent receiver's efficiency-weighted aperture is about **7–21 mm² at 100–300 m** (Result 2's $A_{\rm mode}$ times $\eta=0.25$), not the ≈27 mm² of the far-field formula alone (both are worked in §C10.3a, item 7). A 25 mm ToF unit's ≈80 mm² is about 4–11× larger ($80/20.5=3.9$ to $80/7.2=11$), and the four receivers per point of §C7a narrow this to 1.3× at 200 m. ToF's $\eta=0.164$ already contains the bright-sun live fraction (≈71 mm² in a fully sunlit scene); sunlight's other cost, a higher detection threshold, sits in the photon requirement (§C10.3a, item 7, caveats).
- With truncation and single polarization included, the *area-matched* coherent mode-equivalent collecting area at 0.05° is 1.3 mm². It is 1.6 mm² without the truncation factor $t^2=0.84$, and 3.2 mm² without the single-polarization factor ½ as well; that last value is the ideal $\lambda^2/\Omega_{\rm cell}$, where $\Omega_{\rm cell}=\theta_{\rm cell}^2$ is the solid angle of one mesh cell. The cell-filling estimates of §C10.2, item 5 and §C10.3 use the 1.3 mm².""",
    "Repeated bullet 1 cut; efficiency-weighted apertures and ratio on the report-wide efficiencies.")

# ---------------------------------------------------------------- C10.4, C10.6, C10.7
add(f"round1 model_round2 [10_C10_part2] report #1 (§C10.4 check); {D6}",
    r"(ideally 20–184 W at 200 m)",
    r"(ideally 58.5–175.5 W at 200 m)",
    "Recomputed §C10.3 power.")

add(f"{D6}; {D7}",
    r"coherent detection needs 1.4–800× the power of the ToF example",
    r"coherent detection needs 4.2–816× the power of the ToF example",
    "From the recomputed §C10.3 table.")

old = span("| 0.1° | 87–800× |", "| 0.0125° | 1.4–13× |")
add(f"{D6}; {D7}", old,
    rep(old, [("| 0.1° | 87–800× |", "| 0.1° | 272–816× |"), ("| 0.05° | 23–200× |", "| 0.05° | 68–204× |"),
              ("| 0.025° | 6–51× |", "| 0.025° | 17–51× |"), ("| 0.0125° | 1.4–13× |", "| 0.0125° | 4.2–13× |")]),
    "Same ratios as the §C10.3 table.")

add(f"{D6} (requirement 3 restates §C10.2 item 5)",
    r"| 3 | At most about 3 dB one-way loss at watt-class power |",
    r"| 3 | At most about 3 dB one-way loss while carrying ≈3–31 W per beam (§C10.2, item 5) |",
    "Power per beam from the recomputed §C10.2 item 5.")

# ---------------------------------------------------------------- skipped
# (Decision 1, the FMCW dwell, is implemented in §C10.2 item 5 above and, for the rest of §C10, in the second list,
#  edits/round2/R2E2_C10_dwell.json, built by R2E2_C10_dwell_build_edits.py.)
skipped.append({
    "finding": "decision 7 (ToF at 940 nm): companion tables file",
    "kind": "cross_section",
    "location": "automotive_perception_report_figures/coherent_mode_coverage_tables.txt (dated 27 Sep), cited in §C10.3b 'What was computed'",
    "detail": "The file still prints the 905 nm ToF rows ('ToF 25 mm, 905 nm, pixel 0.1 deg: M_Goodman = 1888 (simple ... = 1826)', 485/456, 127/114), while §C10.3b Result 1 quotes the 940 nm output of the installed script (1,752/1,692, 451/423, 118/106). Regenerate it from build/figures/coherent_mode_coverage.py (its print_tables output); no report text outside §C10 quotes these numbers."})

for e in edits:
    assert e["old"] != e["new"], e["id"]
spans = sorted((text.index(e["old"]), text.index(e["old"]) + len(e["old"]), e["id"]) for e in edits)
for (a0, a1, ai), (b0, b1, bi) in zip(spans, spans[1:]):
    assert b0 >= a1, ("overlap", ai, bi)
OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump({"block": "R2E_C10", "edits": edits, "skipped": skipped}, f, ensure_ascii=False, indent=1)
print(f"{len(edits)} edits, {len(skipped)} skipped -> {OUT.name}")
