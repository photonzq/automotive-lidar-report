All four cross-reference checks are finished. Locate items by their quotes if the line numbers shift.

**What each check found**

1. **§C8.2 pointer (digitizer):** It resolves, but only to "a 100–400 MHz digitizer (§C7)". §C8.2 gives no converter numbers of its own, and its figure is on a different basis from §C10.2 and §C7a (finding 2).
2. **§E11.2:** The content matches what §C10.6(d) relies on: depth carried as an extra image channel, and "tokenizer" defined. But §E11.2 hedges the claim and tags it [E], while §C10.6(d) states it as fact (finding 9).
3. **§C6's staring-array text:** It exists under "The physics behind it: receive étendue and silicon area" and "What could break this". §C10 paraphrases it with a different formula, puts it more strongly than §C6 does, and in two places departs from §C6's sunlight and pixel-pitch text (findings 5–8, 10).
4. **§C7a's ToF inputs:** The 520 macro-pixels (IMX479: 520 lines × 0.05° = 26°, §C6), the 25 mm aperture and the 30 µm macro-pixel all match. The efficiency inputs do not. §C7a uses PDE 0.37 *at 940 nm* with a 0.784 live fraction (η = 0.145) and FMCW η = 0.25. §C10.3–C10.3b model ToF at 905 nm, and §C10.3a item 7 uses PDE 0.35 with no live fraction and FMCW at 0.504 (findings 1, 3, 4).

## New findings (most severe first)

**1. Line 6349 (and 6356; repeated in §C10.3b "What the exact computation shows")** — B — **high**
- **Quote:** "≈85 mm² for 25 mm (optics ≈0.5 × PDE ≈0.35)"
- **Problem:** Item 7's efficiencies are on a different basis from the model the report builds in §C7a:
  - **ToF:** item 7 uses 0.5 × 0.35 = 0.175. §C7a uses "$\eta=0.5\times0.37\times0.784=0.145$ (optics transmission × PDE × live fraction)" in bright sun, or 0.185 at night. §C10.3 itself uses 0.15 "about the §C7a value".
  - **FMCW:** item 7 uses QE 0.8 × 1 dB each way = 0.504. §C7a's η = 0.25 also includes "heterodyne mixing efficiency", and the measured chains reach only 0.06–0.17.
  - **Effect:** on §C7a's efficiencies, ToF is 491 × 0.145 = 71 mm² and one FMCW look is (28.8–82.0) × 0.25 = 7.2–20.5 mm². That makes the ratio ≈3.5–10×, not the "2–6×" stated here and repeated in §C10.3b. §C7a's four-look design reaches 4 × 63.7 × 0.25 = 64 mm² at 200 m, about 1.1× below ToF.
- **Proposed rewrite:**
  - ToF cell: "≈70 mm² in bright sun, ≈90 mm² at night, for 25 mm (optics 0.5 × PDE 0.37 at 940 nm × live fraction 0.784, §C7a)".
  - FMCW cell: "≈7–20 mm² per look for 20 mm at 100–300 m, using §C7a's $\eta=0.25$ (optics, QE and heterodyne mixing; measured chains 0.06–0.17)".
  - Lead sentence: "On the §C7a efficiencies, a 25 mm scanned ToF receiver keeps about 3.5–10× the efficiency-weighted aperture of one mirror-scanned FMCW look, and about 1.1× that of §C7a's four looks at 200 m."
  - Update the "2–6×" in §C10.3b to match.

**2. Line 6556** — A/B — medium
- **Quote:** "a balanced detector and a digitizer (an analog-to-digital converter, ADC; §C8.2)"
- **Problem:** The pointer lands on §C8.2 item 4, "a 100–400 MHz digitizer (§C7)". That sends the reader on to §C7 and gives a figure that is ambiguous: it is a beat *bandwidth* (§C7: "100–400 MHz ADC path"), not a sample rate. Elsewhere §C10 relies on different digitizer figures:
  - §C10.2 item 7: "0.2–1 GHz beat at 300 m, i.e. 0.4–2 GS/s", using the 2× Nyquist rule and no Doppler;
  - §C7a(c): "$f_s\approx1.2$ GS/s" for 5 µs chirps, using the 2.5 × ($f_b+f_D$) rule.

  Also, the §C7a design needs four receivers per channel (one per look), each with its own balanced detector and GS/s ADC; this sentence implies one per pixel.
- **Proposed rewrite:** "Each *simultaneously* active coherent receiver needs local-oscillator (LO) power, a balanced detector and a GS/s-class analog-to-digital converter (ADC): ≈1.2 GS/s for 5 µs chirps to 300 m (§C7a(c)), or 0.4–2 GS/s for 10–2 µs chirps (§C10.2, item 7). The four-look design of §C7a needs four such receivers per channel." Separately, in §C8.2: "a digitizer for 100–400 MHz of beat signal (≈0.5–1.2 GS/s with Doppler and the 2.5× sampling rule of §C7a(c))".

**3. Line 6039 (§C10.3; also 6159, 6178, 6409 in §§C10.3a–b)** — B — medium
- **Quote:** "$\eta=0.15$ [E: about the §C7a value, 0.145]"
- **Problem:** §§C10.3–C10.3b model ToF at **905 nm** (E_ph = 2.19×10⁻¹⁹ J; $N_{\rm sp}\approx460$ at 0.905 µm) but take their efficiency from §C7a's **940 nm** IMX479 model (PDE 0.37, live fraction 0.784). The report's own 905 nm PDE data are lower: §C6 reports "22–24% at 905 nm (2021), 37% at 940 nm (2025)". §C6(d) also gives a 77% dead fraction at 905 nm behind a 20 nm filter in full sun, against 22–39% at 940 nm/10 nm. Item 7's "PDE ≈0.35" has the same mismatch.
- **Proposed rewrite (preferred):** move the ToF model to 940 nm: "for ToF: 940 nm (the wavelength of §C7a's PDE 0.37 and live fraction), 25 mm aperture, $N_{\rm req}=20$ and $\eta=0.15$ [E: about the §C7a value, 0.145]". Then use $E_{\rm ph}=2.11\times10^{-19}$ J in §C10.3, in item 1's ToF example and in item 5. Mode counts become $N_{\rm sp}\approx420$ at 0.05° (from 456) and $P_{\rm ToF}$ about 4% lower.
- **Alternative:** keep 905 nm and use a 905 nm PDE of 0.22–0.24 with §C6(d)'s 905 nm dead fraction. This raises $P_{\rm ToF}$ by roughly 1.5× or more in sun.

**4. Line 6300** — B — low
- **Quote:** "ToF: 25 mm aperture, 520 SPAD macro-pixels × ≈460 modes, 2,400 scan columns"
- **Problem:** The 520 count matches §C7a's 520-line, IMX479-based sensor (§C6: "520 lines × 0.05°"). But the ≈460 modes and §C10.3b's ToF model ("field of view equals one mesh cell") assume a 0.05° × 0.05° pixel. §C6(d)'s background model, which §C7a and §C0 subsection 10.3 (b = 2.87) build on, assumes "a 0.1°×0.05° field per macro-pixel":
  - If the 0.1° × 0.05° field is right, each pixel accepts ≈850–910 modes and adjacent columns overlap.
  - If 0.05° is right, the §C7a/§C0 background is 2× too high.

  Separately, 520 × 0.05° spans 26°, not the 25° field; this 4% excess is what makes "available" 5.7×10⁸ slightly exceed "required" 5.5×10⁸.
- **Proposed rewrite:** add a note to the derivation: "Each macro-pixel views 0.05° × 0.05° (IMX479 geometry, 520 × 0.05° = 26°, §C6), giving ≈460 modes at 905 nm (≈420 at 940 nm). §C6(d)'s background assumes a 0.1° × 0.05° field, which would double both the mode count and the background; the two should be reconciled." The fix itself (state the horizontal pixel field and why) belongs in §C6(d) and §C7a.

**5. Line 6321** — A — medium
- **Quote:** "has a finite étendue: detector area × NA², where NA is the numerical aperture of the receive optics. This is the §C6 staring-array penalty"
- **Problem:**
  - §C6 does not use this formula or the term "staring-array penalty". It frames the cost as a short focal length forced onto a fixed-size sensor: "staring over 120° … $D\approx3.8$ mm", against 28.5 mm for a 26° scanned column, i.e. "about **1.8% of the collecting area**" and "roughly **7.5× less range**". Those §C6 numbers are what the reader needs.
  - The étendue formula drops a factor π (≈ π × area × NA²).
  - "which ToF solves by scanning one axis" is firmer than §C6's "A mechanical one-axis scanner appears to be the cheapest proven optical multiplexer at current automotive volumes."
- **Proposed rewrite:** "A staring array (…) has a fixed étendue, about $\pi A_{\rm det}{\rm NA}^2$ for detector area $A_{\rm det}$ and receive numerical aperture NA, which a wide field spreads over many directions. §C6 ('The physics behind it: receive étendue and silicon area') quantifies it: IMX479's 15.8 mm array at f/1.2 gets a ≈28.5 mm aperture as a 26° scanned column but ≈3.8 mm staring over 120°, 1.8% of the collecting area and about 7.5× less range. A one-axis scanner avoids this by sharing a small detector across many time slots; §C6 judges it the cheapest proven way at current volumes."

**6. Line 6613** — A — medium
- **Quote:** "**Steering the receive path through a large aperture is exactly the solid-state capability that §C6 found missing**"
- **Problem:** This overstates §C6, which says: "This is **one attractive missing capability**, not the only route". §C6's alternatives are tiling, smaller SPAD pitch and coherent detection.
- **Proposed rewrite:** "**Steering the receive path through a large aperture is one attractive capability that §C6 found missing ('What could break this', item 3), not the only route**, and the LCM is the most mature candidate for it."

**7. Line 6361** — A — medium
- **Quote:** "signal and solar background both grow with aperture, so the signal-to-noise ratio (SNR) scales approximately as $\sqrt{A_{\rm rx}}$"
- **Problem:** §C6(d), which the report's ToF model uses, says the opposite about the mechanism: "In a bright sunlit scene, SNR (signal-to-noise ratio) per bin is not the problem. **Dead time and pile-up** are". In §C7a sunlight enters through the 0.784 live fraction and a higher Poisson threshold, not through √A scaling. As written, the caveat points the reader to a mechanism the report's numbers do not use.
- **Proposed rewrite:** "For SPAD ToF, bright sun mainly costs dead time and pile-up rather than per-bin SNR (§C6(d)): at 940 nm behind a 10 nm filter it cuts effective PDE by about a third in a fully sunlit scene (live fraction 0.784 in §C7a's central case), and a larger aperture collects proportionally more background. Only for a purely background-limited detector does SNR scale as $\sqrt{A_{\rm rx}}$. A narrowband LO receiver strongly rejects broadband sunlight (≈10³ photons/s in one mode, §C6(d′)), …"

**8. Line 6697** — A — medium
- **Quote:** "So **for small objects, more vertical lines cost silicon, not photons.**"
- **Problem:** This holds only if the receive aperture is kept, which the line does not say. Two passages show the alternatives:
  - §C10.3a item 7: with fixed 30 µm macro-pixels at f/1.2, 0.025° needs a ≈57 mm aperture, "which does not fit".
  - §C6: "smaller pixels do not preserve the photon budget automatically": at a fixed line pitch, shrinking the pixels shrinks the aperture "from about **28.5 to 11.5 mm**".

  The sentence carries §C10.6's explanation of the line race, yet reads as a contradiction of item 7's "erodes ToF's photon advantage".
- **Proposed rewrite:** "So **for small objects, more vertical lines cost silicon rather than photons, provided the receive aperture is kept**: the macro-pixel must shrink in step with the line pitch (smaller SPADs, §C6) or the optics must get faster. With fixed 30 µm macro-pixels at f/1.2, 0.025° would need ≈57 mm (§C10.3a, item 7). Extended-target range does fall, because energy per pixel drops (§C6(b))."

**9. Line 6701** — E/A — low
- **Quote:** "This is a genuine architectural motive, independent of detection range."
- **Problem:** §E11.2 hedges the same point and tags it as an estimate: "it may be one of the real motives behind "camera-like" lidar resolution (§C10.6) [E]". It also describes the mechanism more accurately: depth makes lidar "look like an extra image channel". A patch tokenizer pretrained on RGB has no weights for a depth channel, so "let lidar enter image-pretrained tokenizers" overstates.
- **Proposed rewrite:** "…simplify calibration and fusion, and present depth as an extra channel on the camera's pixel grid, a practical way to feed lidar into image-pretrained networks (§E11.2; a tokenizer is the input stage that cuts an image into patches, or 'tokens'). This is plausibly one real motive for camera-like resolution, independent of detection range [E]."

**10. Line 6352** — B — low
- **Quote:** "| Solid-state flash ToF | ≈3–5 mm | Staring étendue (bite c) | Small |"
- **Problem:** Every other row gives a number. §C6 supplies the input: ≈3.8 mm at f/1.2 for a 120° staring field.
- **Proposed rewrite:** "≈1.6 mm² ($\pi(1.9\ {\rm mm})^2\times0.145$; §C6: 1.8% of the 28.5 mm scanned-column aperture's area)".

## New consistency flags

1. **§C6(d) pixel field** (line 4294, "0.1°×0.05° field per macro-pixel") against the 0.05° grids of §C7a (520 × 2,400) and §§C10.3a–b. §C0 subsection 10.3's b = 2.87 inherits the 0.1° field (see finding 4).
2. **Digitizer figures are on four different bases:**
   - §C8.2 (line 5569): "100–400 MHz digitizer (§C7)";
   - §C7 (line 4561): "100–400 MHz ADC path";
   - §C10.2 item 7 (line 5908): "0.4–2 GS/s" (2× rule, no Doppler);
   - §C7a(c) and §C7b: 2.5 × ($f_b+f_D$), ≈1.2 GS/s.
3. **Useful aperture per address:** §C8.2 item 2 (line 5553) says "about 0.9 mm at 0.1° and 1550 nm" ($\lambda/\theta$). §C10.3b's area-matched equivalent collecting diameter at 0.1° is ≈0.65 mm (0.33 mm², with $t^2/2$). Both are fine, but the bases differ and are not labelled.
4. **ToF wavelength:** 905 nm in §§C10.3–C10.3b; 940 nm in §C7a, §C0 subsection 10.3 and §C6(d)'s model case (see finding 3).
5. **Scanner wording:** §C6's own term is "the cheapest proven optical multiplexer" (line 4440). This refines earlier finding 36: §C10.4's "(§C6: the mechanical axis as a silicon-area multiplier)" should cite §C8.3, line 5581, or use §C6's wording.