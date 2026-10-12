## Check of §C0's "Used in" pointers to §C3b, §C4b, §C5 and §E12 (new findings only)

**What I read:**
- the current §C0 tables in subsections 1–3;
- §C3b, §C4b, §C5 and §E12 in full;
- the §E11.3 passage that holds Eq. (169).

**What I searched** across the file: every use of $c\,\tau_p/2$, $\sigma_t/\sqrt{N_s}$ and $1/R^4$, and every "§C0" back-reference. Vendor figures were not checked.

Lines in Part E moved by +6 during the review, so find each item by its quote; the line numbers below are the later ones.

### 1. Overall assessment
Five pointers in the "Used in" column of §C0 subsections 1–3 point at these four sections. Only two of them hold up:
- **§C3b uses points per frame** as Eq. (61).
- **§E12 uses the footprint $R\theta$** in Eqs. (179) and (180).

In both, the numbers agree with §C0 (the AT128 grid; 0.35 m and 0.175 m at 200 m). The notation differs, though, and neither section refers back to §C0. In fact none of the four sections ever cites §C0.

Three pointers are wrong:
- **§C3b never uses two-target resolution.**
- **§C4b never uses the single-target precision relation.**
- **§C5 only states the 297 ps bin width** and never converts it to range.

The $1/R^4$ law for small targets is credited to §E12 in three places, but it is derived in §E11.3, Eq. (169). §C3b's Eq. (62) restates §C0 Eq. (23) without citing it, and within one equation its $N_s$ means first the photons detected, then the photons a detection needs. §C4b's $\bar n$ is the quantity §C0 calls $N_s$.

### 2. Findings (most severe first)

**1. Line 3119–3123 (§C3b, Eq. (62)) — A — medium**
- **Quote:** "where $N_s$ is the number of signal photoelectrons a point needs to be detected"
- **Problem:** Eq. (62) re-derives §C0 Eq. (23) without citing it. §C6's Eq. (80), by contrast, says it "is §C0 Eq. (23) with $T_{\rm atm}=1$". Eq. (62) also changes symbols:
  - PDE becomes $\eta_{\rm det}$.
  - $N_s$ is introduced as "detected per point", then redefined after the ⟹ as the number a detection *needs*. §C0 subsection 10 calls that $n_{\rm req}$.
- **Proposed rewrite:** Replace the sentence that runs from "If the sensor emits average optical power $P$…" through the "where" list with:

  "This is §C0 Eq. (23) with the energy per point, $P/\dot N$ for an average optical power $P$ shared among $\dot N$ points per second, in place of the pulse energy, and clear air. A point then yields $N_s=\frac{P}{\dot N E_{\rm ph}}\frac{\rho A_{\rm rx}}{\pi R^2}\eta_{\rm opt}\,\text{PDE}$ detected photoelectrons. Setting $N_s$ equal to the number a detection needs, $n_{\rm req}$ (§C0 subsection 10), gives
  $$\dot N R^2=\frac{P\,\rho\,A_{\rm rx}\,\eta_{\rm opt}\,\text{PDE}}{\pi\,E_{\rm ph}\,n_{\rm req}} \tag{62}$$
  where $n_{\rm req}$ is the number of signal photoelectrons a point needs to be detected, … and PDE the detector's photon detection efficiency."

**2. Line 1558 (also 2492 and 3125) — A — medium**
- **Quote:** "A target smaller than the beam (debris, a tyre) intercepts a fraction of it that falls as $1/R^2$, so its return falls as $1/R^4$ (§E12)."
- **Problem:** §E12 never mentions $1/R^4$ or how the signal from a small target falls with range. Its small-debris item (point 5 of subsection 3) counts pixels and lidar points only. The derivation is in §E11.3, Eq. (169): "$R\propto E_{\rm point}^{1/4}$ (target smaller than the footprint)". The same wrong pointer appears in §C0 10.9 ("(subsection 1; §E12)") and in §C3b ("so the return falls as $1/R^4$ (§E12)").
- **Proposed rewrite:**
  - Change "(§E12)" to "(§E11.3, Eq. (169))" in all three places.
  - Optionally, so that §E12 also earns the pointer, append to its point 5: "Each such point is also weak: an object of size $s$ smaller than the beam footprint $R\theta_b$ returns about $(s/R\theta_b)^2$ of an extended target's signal, so its return falls as $1/R^4$ (§C0 subsection 1; Eq. (169))."

**3. Line 1525 (row), with §C4b line 3377 — A — medium**
- **Quote:** "Single-target precision | $\sigma_R\approx(c/2)\,\sigma_t/\sqrt{N_s}$: timing spread $\sigma_t$ (pulse, detector jitter, TDC) averaged over $N_s$ detected signal photons"
- **Problem:** §C4b never uses this relation; its only precision statement is "Ranging precision is cm-class in both". No section outside §C0 (subsections 1 and 9) applies it. §C4b does, however, show why the $\sqrt{N_s}$ gain needs care. A 3×3 macro-pixel fires only ≈8 of its 9 cells for 20 photons (Eq. (64)), so the 20 photons of §C0's example cannot all be time-stamped in one shot.
- **Proposed rewrite:**
  - Change the row's "Used in" to "subsection 9; measured precisions in §C5a".
  - After "…reduces their scatter by that factor." add: "The gain assumes every detected photon is time-stamped independently. A 3×3 SPAD macro-pixel registers at most nine photons per shot, and only ≈8 of 20 (§C4b, Eq. (64)), so $N_s=20$ must be accumulated over several shots."
  - In §C4b's Timing row write: "Ranging precision is cm-class in both, against the ideal ≈0.3 cm of $\sigma_R\approx(c/2)\sigma_t/\sqrt{N_s}$ for 100 ps and 20 photons (§C0 subsection 1)".

**4. Line 1523 — A — medium**
- **Quote:** "Two-target range resolution | $\Delta R\approx c\,\tau_p/2$ for pulse length $\tau_p$ | 5 ns → 0.75 m; 1 ns → 15 cm | §C3b"
- **Problem:** §C3b never mentions pulse length or two-target separation, and no section outside §C0 applies $c\,\tau_p/2$. The only analogue is the acoustic $c_{\rm s}\tau/2$ in §B7.1. The relation would naturally belong in §C3b's dual-return discussion.
- **Proposed rewrite:** Either set "Used in" to "—", or make the pointer true. To do that, add after §C3b's "dual-return rates (two echoes reported per laser shot, which doubles the point count without more shots)": "A second echo is reported separately only if it lies at least about $c\,\tau_p/2$ behind the first, 0.75 m for a 5 ns pulse (§C0 subsection 1)."

**5. Line 1524, with §C5 line 3891 — A — medium**
- **Quote:** "Histogram quantization | $c\,\Delta t_{\rm bin}/2$ | 297 ps bins (Adaps ADS6311) → 4.5 cm | §C5"
- **Problem:** §C5 only defines "297 ps bins" as "the width of the timing histogram's bins" and never converts it to range. The dependency runs the other way: §C0 borrows §C5's number. §C5 tags that number [P]; the §C0 row carries no tag. §C5 also has a second applicable case it never converts: the IMX479's 3 GHz equivalent-time sampling.
- **Proposed rewrite:**
  - §C0 row: "| Histogram quantization | $c\,\Delta t_{\rm bin}/2$ | 297 ps bins (Adaps ADS6311 [P]) → 4.5 cm; 3 GHz equivalent-time sampling (Sony IMX479) → 333 ps → 5.0 cm | examples from §C5 |".
  - §C5: "…and "297 ps bins" is the width of the timing histogram's bins, $c\,\Delta t_{\rm bin}/2=4.5$ cm of range per bin (§C0 subsection 1)."

**6. Line 3343–3349 (§C4b, Eq. (64)) — A — medium**
- **Quote:** "Example [E] of Eq. (64), with $\bar n=20$ detected photons in a pulse:"
- **Problem:** §C4b's $\bar n$ (photons detected per pulse per channel, after PDE) is §C0's $N_s$ of Eq. (23). Meanwhile §C0 10.1 uses $\bar n$ for photoelectrons per *point*, summed over shots. The example's 20 photons is essentially §C0's ≈22-photon worked case, but the link is not made.
- **Proposed rewrite:** In §C4b write "$\bar n_1$ the mean number of photons the channel would detect in one pulse if no cell were already fired (photons after PDE; the $N_s$ of §C0 Eq. (23))". Then: "Example [E] of Eq. (64), with $\bar n_1=20$ detected photons in a pulse, close to the ≈22 that §C0 Eq. (23) gives for a 10% target at 200 m with a 25 mm lens and 100 nJ:" Use $\bar n_1$ throughout the saturation passage.

**7. Line 1506 — C — medium**
- **Quote:** "Later sections apply them without re-deriving them; the "Used in" column of each table points to those sections."
- **Problem:** Two of the pointed-to sections re-derive the relation with their own equation numbers: §C3b in Eqs. (61) and (62), §E12 in Eqs. (172), (179) and (180). None of §C3b, §C4b, §C5 or §E12 cites §C0, so the links run one way only.
- **Proposed rewrite:**
  - Change the §C0 sentence to: "Later sections apply them, some restating them in their own notation and numbering; the "Used in" column points to those sections."
  - Add back-references:
    - §C3b after Eq. (61): "(the points-per-frame relation of §C0 subsection 3, times the frame rate)";
    - §C3b at Eq. (62): see finding 1;
    - §E12 after Eqs. (179) and (180): "(the relation $R\theta$ of §C0 subsection 3)";
    - §C4b and §C5: see findings 3 and 5.

**8. Line 3047 (§C3b, Eq. (61)) — D — medium**
- **Quote:** "$$\dot N=N_{\rm col}\,N_{\rm row}\,f_{\rm frame}=\frac{\Theta_H}{\delta\theta_H}\cdot\frac{\Theta_V}{\delta\theta_V}\cdot f_{\rm frame} \tag{61}$$"
- **Problem:** The angular point spacing has four notations: §C0 uses $\Theta_h$ and $\Delta\theta_h$ with no units; §C3b uses $\Theta_H$ and $\delta\theta_H$ in degrees; §E12 uses $\theta_{\rm step}$ in Eq. (179); §E11.3 uses $\Delta\theta$. The §C0 row is unnumbered, while §C3b numbers the same relation.
- **Proposed rewrite:** Adopt §C3b's numbered notation in §C0 subsection 3:
  - Symbol list: "$\Theta_H$, $\Theta_V$ are the horizontal and vertical fields of view, and $\delta\theta_H$, $\delta\theta_V$ the angular spacing of points along each (degrees)".
  - Table row: "| Points per frame | $(\Theta_H/\delta\theta_H)(\Theta_V/\delta\theta_V)$; times $f_{\rm frame}$ this is the point rate, Eq. (61) | … | §C3b (Eq. (61)) |".
  - Use $\delta\theta$ for $\theta_{\rm step}$ in §E12 and for $\Delta\theta$ in §E11.3.

**9. Line 1626 — D/A — low**
- **Quote:** "Footprint at range | $R\,\theta$ | 0.1° at 200 m → 35 cm; 0.05° → 17 cm | §E12"
- **Problem:** §E12 applies $R\theta$ to a lidar's angular grid step ("places points $R\,\theta_{\rm step}$ apart", Eq. (179)) and to a radar's cross-range cell (Eq. (180)), not to a beam footprint. §E11.3 uses it for point spacing too. The numbers match: 0.35 m and 0.175 m at 200 m in §E12's debris item.
- **Proposed rewrite:** "| Footprint or point spacing at range | $R\,\theta$, for a beam, a pixel or an angular step $\theta$ | 0.1° at 200 m → 35 cm; 0.05° → 17 cm | §E11.3, §E12 (Eqs. (179), (180)) |". Extend the symbol line to "…covers at range $R$, or the spacing of points for an angular step $\theta$".

**10. Line 1627 — B — low**
- **Quote:** "120°/0.1° × 25°/0.2° = 150,000; at 10 Hz, 1.5 Mpts/s"
- **Problem:** This looks like the AT128 but does not match §C3b's AT128 entry: 120° × 25.4°, $1{,}200\times128\times10=1.536$ M. Subsection 1's point-rate row uses the exact 1.536 M. A reader following the pointer finds 153,600 points per frame, not 150,000.
- **Proposed rewrite:** "1,200 × 128 = 153,600 points per frame (the Hesai AT128 grid, 0.1° × ≈0.2° over 120° × 25.4°, §C3b); at 10 Hz, 1.536 Mpts/s, the point rate of subsection 1". Update the derivation to match.

**11. Line 3118 (§C3b) — A — low**
- **Quote:** "since at fixed energy per frame $N_{\rm points}R^2$ is roughly constant (§C5a)"
- **Problem:** This scaling is the "Scaling" bullet of §C0 subsection 1 ($R\propto\sqrt{E_pA_{\rm rx}\rho}$). The same applies to the $A_{\rm rx}^{1/4}$ statement in the next bullet, also credited to §C5a. §C5a applies these relations; it does not derive them.
- **Proposed rewrite:** "(§C0 subsection 1; §C5a applies it to the AS-DT1)" in both places.

**12. Line 1702 — A — low**
- **Quote:** "InnovizOne's range table uses 90% true positives and a 5% false-alarm rate *per pixel* at 20 klx"
- **Problem:** Subsection 7 sends the reader to §C3b for detection definitions, but §C3b documents InnovizTwo's terms: "90% true / 1% false positives per pixel at 100 klx". InnovizOne's figures appear nowhere else in the report.
- **Proposed rewrite:** "InnovizOne's range table uses 90% true positives and a 5% false-alarm rate *per pixel* at 20 klx [P], and InnovizTwo's datasheet 90% true and 1% false positives per pixel at 100 klx (§C3b); Seyond's Falcon K1 uses >90% detection probability at 100 klx [P]."

**13. Line 3358 (§C4b) — E — low**
- **Quote:** "$$f_{\rm dead}=1-e^{-r\,\tau_d} \tag{65}$$"
- **Problem:** The same paralyzable dead fraction appears again as §C6 Eq. (82), so the two dead-time sections behind §C0's pointer "(§C4b, §C6)" number one relation twice.
- **Proposed rewrite:** Keep Eq. (65), which avoids renumbering. Introduce §C6's Eq. (82) as: "The paralyzable form repeats Eq. (65) of §C4b; the non-paralyzable form is new:"

### 3. Consistency flags to check elsewhere
- **Assumed lidar range precision differs by section:**
  - §C0 subsection 1: ≈0.3 cm (ideal);
  - §C0 subsection 4: 3 cm;
  - §C4b: "cm-class";
  - §E12: "range noise ≈5 cm";
  - §C5a: AS-DT1 at 20–40 mm outdoors, and IMX459 at "15 cm precision in 6×6 mode".

  State which value each section assumes and why.
- **Energy per point has five symbols:**
  - $E_p$, per pulse (§C0 Eq. (23));
  - $E_{\rm tx}$ (§C0 10.1);
  - $E_{\rm pt}$ (§C6 Eq. (80));
  - $E_{\rm point}$ (§E11.3 Eq. (169) and §C0 subsection 9);
  - $P/\dot N$ (§C3b Eq. (62)).
- **The PDE symbol differs:** PDE in §C0 and §C6, $\eta_{\rm det}$ in §C3b.
- **$\tau$ has several meanings:**
  - round-trip delay: $\Delta t$ in §C0 subsection 1, but $\tau$ in §C0 subsection 2 and in §B8's "$R=c\,\tau/2$";
  - pulse length: $\tau_p$ (§C0 subsection 1);
  - time to contact: $\tau$ (§E12 Eq. (173)).
- **The Lambertian collection argument ("a fraction $\rho A_{\rm rx}/(\pi R^2)$") is written out four times:** Part A Eq. (5), §C0 subsection 1, §C3b ("Why the weight is $R^2$") and §C0 10.2. Only 10.2 and §C6 cite Eq. (23).
- **§C3b's AT128 entry is internally slightly off:** 128 rows × 0.2° = 25.6° against the stated 25.4° field.