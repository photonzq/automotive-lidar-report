"""Plan of the restructured §C0, part C: 5 (range, limits, robustness), 6 (testing the model) and the closing table."""
from c0_lib import NEW, COPY

PLAN_C = [
    NEW(r"""
### 5. Range, its limits and its robustness

Subsections 3.1–4.3 give, for each receiver, how much light comes back and how much is needed. Setting the two equal gives the maximum range (subsection 5.1) and how it scales with energy, aperture, background and reflectance (5.2). Eye safety caps the energy (5.3). The shape of the link-loss curve then decides how much range survives a darker target, a dirty window or bad weather (5.4), and how strong the strongest returns become (5.5).

#### 5.1 Detection level and maximum range
"""),
    COPY("This step turns the photoelectron requirement of 10.3",
         subs=[("This step turns the photoelectron requirement of 10.3 into a level on the link-loss axis of Figure C0.10a. The maximum range can then be read off the figure as the range where a loss curve crosses that level.",
                "The photoelectron requirement of subsection 4.3 becomes a level on the link-loss axis of Figure C0.10a, and the maximum range is the range at which a loss curve crosses that level.")]),
    COPY("**The detection level.** Setting the mean signal", "- **At 200 m, the 20–25 mm apertures of §C7a are close to the optimum**",
         subs=[("Setting the mean signal $\\bar n$ equal to the required $n_{\\rm req}$ in Eq. (37) gives",
                "Setting the mean signal $\\bar n$ of Eq. (37) equal to $n_{\\rm req}$, the mean number of signal photoelectrons per point that the required detection probability demands (subsection 4.3), gives"),
               ("modelled as paralyzable, 10.3)", "modelled as paralyzable, subsection 4.2)"),
               ("over the ideal 15.0 counts (10.3);", "over the ideal 15.0 counts (subsection 4.3);"),
               ("The four-look receiver needs 120 in total (10.3),", "The four-look receiver needs 120 in total (subsection 4.3),"),
               ("is 10.2× the SPAD's (10.5)", "is 10.2× the SPAD's (subsection 5.2)"),
               ("- 10.6 follows this sensitivity to its practical consequences", "- Subsection 5.4 follows this sensitivity to its practical consequences")]),

    NEW(r"""
#### 5.2 How range scales: energy, aperture, background and reflectance
"""),
    COPY("Solve $\\mathcal{L}(R_{\\max})=\\mathcal{L}_{\\rm det}(E_{\\rm pt})$",
         subs=[("set the link loss of 10.2 equal to", "set the link loss of subsections 3.1–3.2 equal to"),
               ("the 30 photoelectrons of one look (10.4):", "the 30 photoelectrons of one look (subsection 5.1):")]),
    COPY("- **Direct detection:** from Eqs. (38) and (49),", "  At fixed average optical power $P_{\\rm opt}$ (W)",
         subs=[("the ideal counter of 10.3 needs", "the ideal counter of subsection 4.3 needs")]),
    COPY("- **Scaling.** Signal-limited range goes as", tight=True,
         subs=[("- **Scaling.** Signal-limited range goes as", "- **Background-limited detection.** Eq. (50) is the signal-limited law: range goes as"),
               ("the SNR above becomes", "the SNR of subsection 4.2 becomes"),
               ("(§C0 subsection 10.8).", "(subsection 6.1).")]),
    COPY("- **Coherent, fixed collimated aperture:**", "- **Linear APD against SPAD with the same lens:**", tight=True,
         subs=[("at the optimum, 10.2)", "at the optimum, subsection 3.2)"),
               ("$A_{\\rm mode}=t^2(0.45)^2A_{\\rm rx}$ from 10.2;", "$A_{\\rm mode}=t^2(0.45)^2A_{\\rm rx}$ from subsection 3.2;"),
               ("can pay for at low point rates (§C4c).", "can pay for at low point rates (subsection 5.3, §C4c).")]),
    COPY("![Maximum range versus transmitted energy per point", "- The dotted lines mark 200 and 300 m.",
         subs=[("for the detection levels of 10.4.", "for the detection levels of subsection 5.1.")]),
    COPY("**Reading Figure C0.10c** [E]:", "- **Against the 25 mm SPAD reference** the FMCW energy gap closes",
         subs=[("10.2 times the SPAD's energy (10.5),", "10.2 times the SPAD's energy (above),"),
               ("closes as $1/R$ (10.5),", "closes as $1/R$ (above),")]),

    NEW(r"""
#### 5.3 The cap on energy: eye safety

Every scaling law of subsection 5.2 assumes that more energy per point can be spent. Eye safety caps it. Automotive lidars are designed to Class 1 of IEC 60825-1:2014, the laser-safety standard of the International Electrotechnical Commission (IEC); Class 1 is its least hazardous class, defined by limits on the emission accessible under the standard's measurement conditions.
"""),
    COPY("- **Class 1 (IEC 60825-1:2014).**",
         subs=[("- **Class 1 (IEC 60825-1:2014).** IEC 60825-1 is the laser-safety standard of the International Electrotechnical Commission (IEC), and Class 1 is its least hazardous class, defined by limits on the emission accessible under the standard's measurement conditions; automotive lidars are designed to it. ", "")]),
    NEW(r"""
The limits act on the energy of each pulse and on the average power that can reach an eye, so they bound the energy per point a lidar can spend in one direction per unit time. In Figure C0.10c they would appear as a wavelength-dependent vertical limit on the energy axis; §C7b subsection 3a(b) puts numbers on them for the two designs of §C7a. Like the solar background of subsection 4.2, the limits depend on wavelength, which is why the choice between 905/940 nm and 1,550 nm runs through the whole report. The tenfold higher long-exposure limit at 1,550 nm is what lets a linear InGaAs APD receiver, which needs about ten times the energy per point of the SPAD design (subsection 5.2), pay for that energy at low point rates, and what leaves room for the energy of the robust small-aperture FMCW designs of subsection 5.4 (§C4c).
"""),

    NEW(r"""
#### 5.4 Margin at short range: dark targets, windows, fog and rain
"""),
    COPY("The crossings of 10.4 say how far a sensor sees",
         subs=[("The crossings of 10.4 say how far", "The crossings of subsection 5.1 say how far"),
               ("This part asks what that factor costs in range. The answer depends on the *shape* of the loss curve (10.2).",
                "What that factor costs in range depends on the *shape* of the loss curve (subsections 3.1–3.2).")]),
    COPY("**The designs compared.**", "The margins at 10 m in the table differ slightly",
         subs=[("from the table in 10.4.", "from the table in subsection 5.1."),
               ("the 0.1 µJ of 10.4, which", "the 0.1 µJ of subsection 5.1, which"),
               ("$303\\times12.67/10=384$ nJ (10.1).", "$303\\times12.67/10=384$ nJ (subsection 3.1)."),
               ("and collect less (10.2).", "and collect less (subsection 3.2)."),
               ("- **A water film on the window,** crossed on the way out and again on the way back. Liquid water costs 9.4 dB per millimetre round trip at 1,550 nm (§C4c), so a 0.2 mm film costs $0.2\\times9.4=1.88\\approx1.9$ dB. At 940 nm water absorbs tens of times more weakly, and the film is neglected.",
                "- **A water film on the window:** 1.9 dB for a 0.2 mm film at 1,550 nm, neglected at 940 nm (subsection 3.3)."),
               ("than the model assumes (10.3).", "than the model assumes (subsection 4.3).")]),
    COPY("**Fog.** Fog multiplies $\\mathcal{L}$ by $e^{-2\\alpha R}$", "- **The kinks** in Figure C0.10d(b)",
         subs=[("the Kim model of subsection 8,", "the Kim model of subsection 3.3,"),
               ("- **For direct detection** this is the condition $R^2e^{2\\alpha R}=R_0^2$ of subsection 8.",
                "- **For direct detection** this is the condition $R^2e^{2\\alpha R}=R_0^2$: the design still detects while $e^{-2\\alpha R}/R^2$ is at least its clear-air value $1/R_0^2$."),
               ("(subsection 8), not from the receivers.", "(subsection 3.3), not from the receivers.")]),
    NEW(r"""
In very thick fog of 20 m visibility ($\alpha=196$ /km), beyond the range of the table, the ToF design still reaches ≈13.7 m.

*How the direct-detection reach is found* [E]:
"""),
    COPY("  - **Reach:** a signal-limited lidar still detects", "  - **Reach / $V$** is that reach divided by the visibility", dedent=2, tight=True),
    COPY("- **Reach relative to visibility rises as fog thickens:**", tight=True),
    COPY("**Rain and a wet window.**", "- **Rain is often not the worst of it.**",
         subs=[("Subsection 8's empirical law gives", "The empirical law of subsection 3.3 gives"),
               ("are not modelled (subsection 8).", "are not modelled (subsection 3.3).")]),
    COPY("**Fog also sends light back: backscatter clutter.**", "- **Multiple scattering.** A single-mode receiver accepts light only",
         subs=[("This is the SPAD saturation noted in subsection 8.", "This is the SPAD saturation noted in subsection 3.3."),
               ("that subsection 8 notes for direct detection.", "that subsection 3.3 notes for direct detection.")]),
    COPY("![Maximum range of designs that all reach 200 m", "- **The wet window remains a 1,550 nm problem at any aperture,**",
         subs=[("(Carbonneau law, subsection 8).", "(Carbonneau law, subsection 3.3).")]),

    NEW(r"""
#### 5.5 Dynamic range: strong returns, blooming and blinding
"""),
    COPY("10.6 asked how much light a design has to spare",
         subs=[("10.6 asked how much light", "Subsection 5.4 asked how much light"),
               ("This part sizes that span for the designs of 10.6, describes the failure modes documented for ToF receivers, and says what coherent detection changes and what it does not.",
                "The span is sized below for the designs of subsection 5.4, followed by the failure modes documented for ToF receivers and by what coherent detection changes and what it does not.")]),
    COPY("**How large the span is.**", "  - The robust small-aperture designs of 10.6 give back",
         subs=[("the short-range margin of 10.6.", "the short-range margin of subsection 5.4."),
               ("for four of the designs of 10.6,", "for four of the designs of subsection 5.4,"),
               ("each design of 10.6 is sized", "each design of subsection 5.4 is sized"),
               ("the four-look receiver of 10.3,", "the four-look receiver of subsection 4.3,"),
               ("(the 120 of 10.3 spread", "(the 120 of subsection 4.3 spread"),
               ("macro-pixel (subsection 5).", "macro-pixel (subsection 4.2)."),
               ("designs of 10.6 give back", "designs of subsection 5.4 give back")]),

    NEW(r"""
### 6. Testing the model

A model that predicts ranges from first principles is only as good as its agreement with measured systems. Subsection 6.1 tests its link loss, its detection statistics and its assumed efficiencies against published coherent and direct-detection sensors; subsection 6.2 lists what the model leaves out.

#### 6.1 Benchmark against published systems
"""),
    COPY("The model of 10.2–10.4 predicts how much light", "- **Reflectance scaling.** Ouster's claims suggest",
         subs=[("The model of 10.2–10.4 predicts", "The model of subsections 3.1–5.1 predicts"),
               ("This part tests those predictions", "Here those predictions are tested"),
               ("- **the efficiencies assumed in 10.4.**", "- **the efficiencies assumed in subsection 5.1.**"),
               ("the 0.25 of 10.4 lies above both measured chains (10.1).", "the 0.25 of subsection 5.1 lies above both measured chains (subsection 3.1)."),
               ("the model's bright-sun count (10.4).", "the model's bright-sun count (subsection 5.1)."),
               ("- **Sony's energy per point is my reading of its timing diagram, which states no shots per point.**",
                "- **Sony's energy per point is read from its timing diagram, which states no shots per point.**"),
               ("(live fraction, 10.3)", "(live fraction, subsection 4.2)"),
               ("the background-limited law of subsection 1.", "the background-limited law of subsection 5.2."),
               ("The model of 10.4 holds the background fixed", "The model of subsection 5.1 holds the background fixed"),
               ("against the 0.25 used in 10.4 (see 10.1).", "against the 0.25 used in subsection 5.1 (see subsection 3.1).")]),

    NEW(r"""
#### 6.2 What the model leaves out
"""),
    COPY("- **Small objects.** An object smaller than the footprint", "- **Background-limited direct detection.**",
         subs=[("(subsection 1; §E11.3, Eq. (170))", "(subsection 3.1; §E11.3, Eq. (170))"),
               ("rather than $A_{\\rm rx}^{1/2}$ (subsection 1).", "rather than $A_{\\rm rx}^{1/2}$ (subsection 5.2).")]),
    NEW(r"""
- **Eye safety** is not part of the model's equations; it caps the energy per point from outside (subsection 5.3).
""", tight=True),
    COPY("- **Focusing.** Focusing a coherent beam", "- **Weather beyond extinction.**", tight=True,
         subs=[("restore short-range margin (10.6),", "restore short-range margin (subsection 5.4),"),
               ("depending on angle (10.1).", "depending on angle (the assumptions of subsection 3)."),
               ("10.6 treats fog and rain as extinction", "Subsection 5.4 treats fog and rain as extinction"),
               ("snow, spray and splash (subsection 8),", "snow, spray and splash (subsection 3.3),")]),

    NEW(r"""
### Where these relations are used

| Relation (subsection) | Applied in |
|---|---|
| Range from delay (1.1) | throughout |
| Two-target range resolution (1.1) | §C3b |
| Histogram quantization (1.1) | §C5, §C5a |
| Single-target precision (1.1) | §C5a (measured precisions); subsection 1.2 |
| Unambiguous range and point rate (1.1) | §C4d |
| FMCW beat frequency, range resolution, Doppler shift and its separation from range (1.3) | §C7, §C7a |
| FMCW range precision, velocity resolution, receiver bandwidth and chirp linearity (1.3) | §C7a |
| Coherence and the coherent share of the beat (1.3) | §C7, §C7b |
| FMCW dwell, point rate and per-channel throughput (1.3) | §C7, §C7a, §C7b |
| Shot-noise-limited SNR (1.3) | §C7, §C10.3a |
| Scanning walk-off and scanner-induced Doppler (1.3) | §C4d, §C7, §C10.3a |
| Beam divergence (2.1) | §C7, §C10 |
| Pixel field of view and aperture (2.1) | §C6 |
| Footprint and point spacing at range (2.1) | §E11.3, §E12 (Eqs. (177), (178)) |
| Points per frame (2.1) | §C3b (Eq. (69)) |
| Mechanical sweep rate (2.1) | §C4d (Eq. (77)) |
| Étendue (2.1) | §C6, §C10.3a |
| Photon budget of one pulse, Eq. (31) (3.1) | §C6 (Eq. (88)) |
| Coherent link equation, Eq. (41) (3.2) | §C7b subsection 1(b), §C10.3b and the report's scripts |
| Solar background per pixel, Eq. (32) (4.2) | §C4c, §C6 (Eq. (89)) |
| Detection efficiency, dead time, pile-up, afterpulsing and crosstalk (4.1, 4.2) | §C4b, §C5a, §C6 |
"""),
    COPY("Sources: https://doi.org/10.1364/AO.5.001588 (Siegman 1966)"),
]
