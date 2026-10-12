# Rewrite brief: make the report considerate to its readers

You are rewriting ONE chunk of a long technical report on automotive lidar, thermal night vision, radar and cameras. The writing has been judged too terse, too dense and not considerate to readers. An independent audit found:
- symbols that are undefined or reused with different meanings;
- "magic" constants;
- unnumbered equations referenced vaguely ("the first equation");
- unstated assumptions;
- abrupt jumps between market prose and physics.

Your job is to fix these in your chunk **without changing any fact, number, source, evidence tag or conclusion**.

## The reader

Picture a smart, technically literate reader who is **not** a specialist in every field here. It might be a physicist who knows no finance, an investor who knows no optics, or an engineer from another industry. They read your chunk on its own, perhaps jumping in from the table of contents. They do **not** remember definitions from other sections, and they do **not** want to flip back and forth. The owner explicitly rejected a central glossary: "add definitions near the usage, nobody likes jumping back and forth".

## What to do

1. **Open each `##` section (and each long `###` subsection) with 2–4 plain sentences.** Say what question the section answers, what the answer is, and why it matters for the sensor, the car or the market. If a "Short answer" block already exists, keep it but make it readable: full sentences, one idea per bullet, no fragment chains.

2. **Define every symbol where it is used.**
   - Every symbol in an equation is defined in the same paragraph, immediately before or after it ("where $R$ is the range to the target, $\rho$ the target's diffuse reflectance, …"), with units.
   - Do this even if another section defines it. Brief re-definitions are welcome; readers arrive mid-document.
   - Define composite quantities in words as well as by formula. For example, define $A_{\rm mode}$ itself: say what the quantity *is* physically, not only how it is computed.
   - No magic constants. If a number such as 0.45, 2.5, 5, 37 pJ or 1.2 appears in a formula, say where it comes from, or label it as an assumption.
   - Standard mathematical functions get a one-line definition too, e.g. "$\Gamma(k)=(k-1)!$ is the gamma function".

3. **Resolve symbol collisions inside your chunk** using the report-wide conventions below. Rename the minority use; do not rename the conventional one.
   - $c$ is **always** the speed of light. The "nominal footprint fraction" is $f_{\rm fp}$ (never $c$).
   - $E_{\rm ph}=h\nu=hc/\lambda$ is the photon energy. Write $E_{\rm ph}$; do not switch to $h\nu$ mid-report.
   - $A_{\rm rx}$ is the receive-aperture area (not $A_r$, $A_{\rm ap}$ or $A$). $\eta_{\rm opt}$ is the optics transmission (not $T_{\rm opt}$). $T_{\rm atm}$ is atmospheric transmission.
   - $t$ is the Gaussian aperture-truncation (power) factor. §C10.3b wrote $T$; rename it to $t$ there.
   - $B$ is the FMCW chirp bandwidth. A background count rate is $r_{\rm bg}$ (not $B$).
   - $M$ is the APD avalanche gain only.
     - Number of parallel coherent channels: $N_{\rm ch}$.
     - Number of speckles or spatial modes: $N_{\rm sp}$ (speckles per polarization) or $N_{\rm mode}$ (spatial modes accepted).
     - Number of OPA spots: $N_{\rm spot}$.
   - $k$ is the APD ionization-coefficient ratio only. A Poisson count threshold is $n_{\rm th}$ (not $k$ or $n_t$).
   - $F(M)$ is the APD excess-noise factor only. Frame rate is $f_{\rm frame}$ (not $F$). The coherent peak fraction is $\eta_{\rm coh}$ (not $F_{\rm coh}$).
   - Signal photons or photoelectrons are $N_s$ (or $\bar n$ for a mean). ADC samples per point and samples per frame are $N_{\rm samp}$ (never $N_s$).
   - $\kappa$ is the FMCW chirp rate $B/T$ in Hz/s. Define it where used. In §A5, $\kappa$ is the imaginary refractive index of water; define it there.
   - When you rename, rename **every** occurrence of that meaning in your chunk (equations, prose and tables), consistently.

4. **Define abbreviations and jargon at first use in each `##` section**, briefly in parentheses or a short clause. Examples:
   - SOP (start of production); ASP (average selling price); take rate (share of buyers who choose an option); SPAC (special-purpose acquisition company); Tier 1 (a supplier selling directly to carmakers);
   - L2/L3/L4 (SAE driving-automation levels: L2 driver supervises, L3 car drives in a defined domain and the driver takes over on request, L4 no driver needed within the domain); ADAS; NOA (navigate on autopilot);
   - dToF/iToF; SPAD; SiPM; APD; PDE (photon detection efficiency); TDC; VCSEL; EEL; OPA; FPA; LO; PIC; SOA; ADC; ENOB; FFT; ROI; FOV; IFOV;
   - B50L: the headlamp photometric test point that stands for an oncoming driver's eyes 50 m ahead, 0.57° up and 3.43° left of the lamp axis (UN R112/R149).
   Do not over-explain terms that every reader knows (km, GHz, USD).

5. **State assumptions before or alongside the calculation**, as explicit conditions, and say what happens when they fail. Relevant ones (use those that apply to your chunk):
   - Lambertian (perfectly diffuse) target, radiance $\rho/\pi$ × irradiance. Glossy paint and retroreflectors are not Lambertian: they return far more or far less toward the sensor, depending on angle.
   - Speckle statistics behind fading: a single coherent speckle has exponentially distributed intensity (Rayleigh amplitude). Averaging $N_{\rm sp}$ independent speckles narrows it.
   - Coherent receiver operating at the local-oscillator shot-noise limit, i.e. thermal and dark-current noise neglected. At 105–125 °C this holds only approximately; §C4c gives 82–94% of the shot-noise limit for Ge at 125 °C.
   - Ideal TEM00 Gaussian beams ($M^2=1$), perfect mode matching and alignment; no atmospheric turbulence.
   - The factor ½ for a depolarizing target. A retroreflector largely preserves polarization, so the factor then differs.
   - ADC resolution (the §C7a model assumes 8 effective bits, 50 fJ/conversion step) whenever ADC energy is computed.
   - Clear air unless stated; normal incidence; target filling the footprint.

6. **Write in complete, explanatory sentences.** Turn fragment chains ("X → Y; Z ≈ 3×") into sentences that say why. Keep bullets for genuine lists, but make each bullet a complete thought. Prefer "because …", "so …", "which means …". Spell out arrows in prose. Where a long derivation ends, add one sentence on what it means in engineering or market terms.

7. **Bridge the two audiences.**
   - In market or business passages, a physics term gets a short plain gloss.
   - In physics passages, end with the practical consequence.
   - At the start of each Part (`# Part …` heading), add a short orientation paragraph (3–5 sentences) if there is none: what the Part covers, what the reader needs from earlier Parts, and how it connects to the rest.

8. **Equations: label every display equation and refer to it by label.** Global numbers (1)…(N) are assigned automatically after all chunks are merged.
   - Every display equation (`$$ … $$`) must end, inside the `$$`, with `\tag{eq:cNN-SHORTLABEL}`. NN is your two-digit chunk number; SHORTLABEL is unique and descriptive, lower case with hyphens, e.g. `\tag{eq:c04-link-loss-dd}`.
   - Example: `$$\mathcal{L}_{\rm DD}=\frac{\rho D^2}{4R^2}T_{\rm atm}^2 \tag{eq:c04-link-loss-dd}$$`.
   - Wherever text refers to an equation ("the first equation", "the equation above", "item (a)'s formula", "Eq. …"), write `Eq. (eq:SHORTLABEL)`. It becomes "Eq. (17)" after numbering.
   - You may promote an important inline relation to a display equation if the text refers back to it. Do not number trivial inline arithmetic.
   - Keep each display equation on a line of its own, with a blank line or list context around it as it is now.

## What NOT to do (hard rules)

- **Do not change any number, unit, date, name, source, URL, evidence tag ([P] [I] [T] [E] [U] [MR] [S] [D] [NT] [R]), probability, or conclusion.** Do not add new facts or estimates. You may add definitions, explanations, stated assumptions and orientation sentences. If you find an error, do not fix it: list it in your final reply.
- Do not change headings (`#`, `##`, `###` lines). Cross-references depend on them.
- Do not change `Sources:` lines, image links `![…](…)`, or table structure (columns and rows). You may edit text inside table cells, but keep cells short; put explanations below the table.
- Do not delete content. Moving a sentence within a section is fine if it reads better.
- Do not use versioning language ("updated", "corrected", "revised", "added", "now shows", "previous version"). Do not mention an audit, a reviewer or a rewrite.
- Keep the conventions:
  - Inline LaTeX `$…$` and display `$$…$$`; `\$` for currency (never a bare `$` for money).
  - `$` balanced on every line; no `|` inside math in a table row (use `\lvert…\rvert`).
  - A space between a closing `$` and a following digit.
  - `{\rm …}` or `\mathrm{…}` for upright text.
- Match the report's existing spelling and style. Don't pad or repeat: one clear explanation is better than three.

## How to work

- Your working file is `chunkNN.md` in your folder. **Edit it in place, section by section.** Do not rewrite the whole file at once; that risks losing content.
- Read your whole chunk first (about 250 lines at a time), then edit.
- Before finishing, run the checker:
  `"python" "<rewrite folder>/check_chunk.py" <your chunk id>`.
  Fix everything it reports: missing numbers or tags, changed headings, odd `$`, untagged display equations, unresolved `Eq. (eq:…)` references.
  - A number reported "missing" usually means you dropped or reformatted it. Restore it.
  - It is fine if numbers merely moved.
- Final reply (short):
  - what you changed, by kind (openings added, symbols defined, renames, assumptions stated, jargon defined, equations labelled);
  - every rename you made (old → new, with where);
  - any errors or inconsistencies you noticed but did not fix;
  - the checker's final output.
