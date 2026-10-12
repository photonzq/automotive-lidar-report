All four cross-references are checked. Line numbers below may be off by a few lines (§E12's heading moved from 8451 to 8459 during the check), so locate by quote.

## Results of the four checks

- **§E12 (item 4).** The pointer is wrong. §E12 never states the $R^{-4}$ small-object law; it is in §E11.3 (Eq. (169)). Finding 1.
- **§C3b (item 1).** Its Eq. (62) is subsection 10's Eq. (42) rearranged ($A_{\rm rx}=\pi D^2/4$, $\eta=\eta_{\rm opt}\eta_{\rm det}$, $N_s=n_{\rm req}$). But §C3b assumes signal-limited detection, and subsection 10 applies the relation in bright sun without that condition. Finding 2.
- **§C5a (item 3).** §C5a presents the paralyzable behaviour as an [E] inference about the development chip, notes a contrary press release, and adds "The product may differ from the development chip." Subsection 10 states it as fact. Finding 3.
- **§C10.3a/§C10.3b (item 2).** Both pointers are supported:
  - §C10.3b uses $t=0.915$ with $w_0=0.45D$ and the same monostatic link equation (63.7 mm² for 20 mm at 200 m; ceiling $\lambda R/4$; far-field loss about 3×, matching 10.2's 0.34).
  - §C10.3a item 3 gives the footprint fraction $2\lambda/(R\theta^2)\propto1/R$.
  - §C10.3a item 3 and §C10.3b Result 4 cover small objects being missed between samples.
  
  Its assumption list matches 10.1. But the two sections conflict with subsection 10 on efficiencies, on what the "optimum diameter" means, and on the symbol $N_{\rm sp}$ (flags a–c).

## New findings

1. **Line** 2492 — **A** — **medium**
   - **Quote:** "so its loss grows as $R^{-4}$ (subsection 1; §E12). A narrow coherent beam is filled by smaller objects, but it must hit them (§C10.3a)."
   - **Problem:** §E12 contains no $R^{-4}$ law. The law and its consequence $R\propto E_{\rm point}^{1/4}$ are in §E11.3 ("For a target smaller than the footprint, it intercepts a share of the beam that also falls as $1/R^2$", Eq. (169)). §E12 (subsection 3, item 5) only counts pixels and points on small debris ("0–1 lidar points on the 0.1° grid … at 200–300 m"). That fits the second sentence, not the first.
   - **Proposed rewrite** (also covers earlier finding 15 on the same sentence): "- **Small objects.** An object smaller than the footprint intercepts a fraction of the light that falls as $1/R^2$, so the fraction it returns falls as $1/R^4$ and range grows only as $E_{\rm tx}^{1/4}$ (subsection 1; §E11.3, Eq. (169)). A narrow coherent beam is filled by smaller objects, but it must hit them (§C10.3a, item 3; §C10.3b, Result 4). At 200–300 m a 15–30 cm object gets at most about one point on a 0.1° grid, whatever the receiver (§E12, subsection 3, item 5)."

2. **Line** 2148 — **A** — **medium**
   - **Quote:** "is constant: this is the range-weighted point-rate figure of merit of §C3b."
   - **Problem:** §C3b's Eq. (62) is constant only under "signal-limited detection (a fixed number of detected signal photons per point suffices, whatever the background)". §C3b adds that the conserved product tends toward $\dot N R^4$ when sunlight limits. Subsection 10 applies the relation with the bright-sun $n_{\rm req}$ and drops that condition. In the 10.3 model the bright-sun requirement depends on how the energy per point is delivered. With 5, 10 and 20 shots per point ($b=1.43$, 2.87 and 5.73), the ideal counter needs 14.0, 17.3 and 22.5 counts. So $\dot N R^2$ moves by about 25% per factor of two in point rate.
   - **Proposed rewrite:** "So $\dot N R_{\max}^2=\rho\,\eta\,D^2P_{\rm opt}/(4n_{\rm req}E_{\rm ph})$ is constant as long as $n_{\rm req}$ is: this is Eq. (62), the range-weighted point-rate figure of merit of §C3b, which assumes signal-limited detection. In bright sun $n_{\rm req}$ grows with the background a point collects. If the energy per point is changed through the number of shots, the ideal counter of 10.3 needs 14.0, 17.3 and 22.5 counts for 5, 10 and 20 shots [E]. $\dot N R^2$ then shifts by about 25% per factor of two in point rate, part of the way toward the $\dot N R^4$ of sunlight-limited detection (§C3b)."

3. **Line** 2026 — **E/A** — **medium**
   - **Quote:** "Sony's passively recharged SPADs behave paralyzably (§C5a): a SPAD is live only if no photon arrived during the last $\tau_d$."
   - **Problem:** §C5a records "The ISSCC abstract says *passive* quenching and recharge; the IMX459 press release says *active* recharge [I/P]". It infers paralyzable behaviour from the 60 Mcps ceiling as [E] and adds "The product may differ from the development chip." Subsection 10 drops all three hedges. The numerical effect is small, but not zero. A non-paralyzable SPAD here would be dead 19.6% rather than 21.6% of the time (live fraction 0.804, $\eta=0.149$). $b$ would rise to 2.94, which lifts the threshold from 15 to 16 counts (18.4 needed instead of 17.3).
   - **Proposed rewrite:** "Eq. (82) gives the dead fraction. The model treats Sony's SPADs as paralyzable [E]: the development chip's measured 60 Mcps ceiling equals the $1/(e\tau_d)$ of a paralyzable counter with passive recharge, although the IMX459 press release says active recharge (§C5a). A paralyzable SPAD is live only if no photon arrived during the last $\tau_d$. Each of the macro-pixel's nine SPADs (a 3×3 group) counts … and $f_{\rm dead}=0.216$. A non-paralyzable SPAD would be dead 19.6% of the time instead, which raises $b$ to 2.94 and the threshold to 16 counts, and changes the energy per point by a few per cent."

4. **Line** 1968 — **A** — **low**
   - **Quote:** "written as an area; the report's scripts use it throughout (§C10.3b)."
   - **Problem:** §C10.3b documents only its own script, `coherent_mode_coverage.py`. It also restates the same relation as Eq. (146), and §C7b restates it as Eq. (101). The pointer neither supports "throughout" nor tells the reader that the later equation numbers are the same relation.
   - **Proposed rewrite:** "This is the monostatic link equation of Piggott et al. (Waymo) [P], written as an area. §C7b (Eq. (101)) and §C10.3b (Eq. (146)) restate it, and the report's scripts use it throughout."

5. **Line** 2157 — **A** — **low** (amends earlier finding 17)
   - **Quote:** "while the footprint's share of a fixed angular cell shrinks as $1/R$ (§C10.3a)."
   - **Problem:** The pointer is correct, but §C10.3a item 3 gives the explicit expression. Citing it makes the sentence self-contained.
   - **Proposed rewrite:** "…while the beam covers a share $\pi w^2/(R\theta)^2=2\lambda/(R\theta^2)$ of a cell of angular pitch $\theta$, which shrinks as $1/R$: 4.1% at 100 m for 0.05° (§C10.3a, item 3)."

## New consistency flags

a. **Efficiencies (substantive).**
   - §C10.3a item 7 (~6350) uses ToF optics 0.5 × PDE 0.35 = 0.175, with no dead-time factor, giving 86 mm².
   - For FMCW it uses QE 0.8 × 1 dB each way ≈ 0.50, giving 14.5, 32 and 41 mm² at 100, 200 and 300 m, and concludes "about 2–6×".
   - Subsection 10 (10.1, 10.4, 10.8) and §C7a use 0.145 and 0.25, and call 0.25 "at the optimistic end" of measured chains (0.057–0.17).
   - With subsection 10's values the per-look ratio is about 3.5–10× (71 mm² against 7.2, 15.9 and 20.5 mm²). §C10.3a's FMCW efficiency is twice the report's own optimistic design value.

b. **"Optimum diameter" means two things.**
   - §C10.3a item 3's table and item 7 ("Confocal optimum (≈14 mm at 100 m, ≈22 mm at 250 m)") give the beam diameter $2w_0$, about 31 mm at 500 m.
   - §C0 10.2/10.4 and §C10.3b give the aperture $D_{\rm opt}=w_0/0.45$: about 16 mm at 100 m, 22 mm at 200 m, 35 mm at 500 m.
   - So "≈22 mm" is the 250 m optimum in one section and the 200 m optimum in the other.

c. **$N_{\rm sp}$ has two meanings.**
   - Subsection 10 (10.1 at ~1905, 10.3 at ~2039) uses it for the number of looks summed.
   - §C10.3a item 2 (~6170, "one coherent mixer uses of order $1/N_{\rm sp}$ of the aperture power") and §C10.3b Result 1 ("6.2 / 3.3" speckles for the matched 20 mm aperture) use it for speckle modes across one aperture.
   - A reader could take "3–6 speckles" as 3–6 looks, which would contradict 10.3's single-look fading. Use a separate symbol in §C10.3a/b, and say that a single-mode receiver still fades like one look.

d. **$t^2$ and the 0.45 ratio.** §C10.3b gives $t^2=0.837$ (~6437) and $t^2=0.84$ (~6453); subsection 10.2 uses 0.838. §C10.3b calls 0.45 "a model choice" (~6388), while §C0 10.2 derives it as the far-field optimum.

e. **One equation, three numbers.** Eq. (33) = Eq. (101) in §C7b = Eq. (146) in §C10.3b. The collimated ceiling $\lambda R/4$ is likewise restated in §C10.3b and as Eq. (103) in §C7b.

f. **Paralyzable claim stated without hedge elsewhere.** §C4b (~3356, "A passively recharged SPAD such as Sony's is paralyzable"), §C6(d) (the Eq. (82) text) and §C7a(a) (~4689, "Its passive recharge behaves paralyzably") all drop §C5a's hedge. Hedge them consistently with §C5a.

g. **The same wrong §E12 pointer appears in two more places.** Subsection 1 (~1558, "its return falls as $1/R^4$ (§E12)") and §C3b (~3125, "so the return falls as $1/R^4$ (§E12)") should point to §E11.3, Eq. (169).

h. **$N_s$ and $\eta$ notation differs across sections.**
   - $N_s$ is "signal photoelectrons a point needs" in §C3b's Eq. (62), "detected photons per pulse" in subsection 1's Eq. (23), and "photons in the LO's mode" in subsection 2.
   - §C3b's $\eta_{\rm opt}\eta_{\rm det}$ (with $\eta_{\rm det}$ = PDE) omits the dead-time live fraction that subsection 10's $\eta$ includes.