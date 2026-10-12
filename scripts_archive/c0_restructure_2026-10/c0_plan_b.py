"""Plan of the restructured §C0, part B: 3 (how much light comes back) and 4 (how much light is needed)."""
from c0_lib import NEW, COPY

PLAN_B = [
    NEW(r"""
### 3. How much light comes back

Whether an echo is detected depends on two amounts: how much of the transmitted light the receiver can use, and how much it needs. Subsections 3.1–3.3 derive the first, the link loss, for the two kinds of receiver compared throughout the report: direct detection, which counts every photon its lens collects (ToF), and coherent detection, which responds only to light in the spatial mode of its local oscillator (FMCW). Subsection 3.3 adds the losses of the atmosphere, fog, rain and wet windows. Subsections 4.1–4.3 derive the second amount, and subsection 5.1 sets the two against each other.

**Assumptions.** The link model of subsections 3.1–6.1 rests on the following conditions; subsection 6.2 notes what changes when they fail.
"""),
    COPY("- **Lambertian target.** The target is perfectly diffuse", "- **Clear air and normal incidence.**",
         subs=[("narrows the distribution (10.3).", "narrows the distribution (subsection 4.3)."),
               ("which 10.6 treats as a fixed extra loss.", "which subsection 5.4 treats as a fixed extra loss."),
               ("below the computed value (10.9).", "below the computed value (subsection 6.2)."),
               ("The air is clear, except in 10.6, which adds fog and rain (subsection 8 treats weather for direct detection alone).",
                "The air is clear, except where subsection 3.3 adds fog and rain.")]),

    NEW(r"""
#### 3.1 Direct detection: the Lambertian link

A diffuse target scatters the light it intercepts into the whole hemisphere, so a receiver at range $R$ collects only the small fraction that falls on its lens. That fraction, the link loss, is where every range calculation starts. It is defined below for any receiver, evaluated for direct detection, and finally counted in photons for a single pulse.
"""),
    COPY("**Definition of the link loss.**", "where $E_{\\rm pt}/E_{\\rm ph}$ is the number of photons transmitted per point"),
    NEW(r"""
The photon energy is $E_{\rm ph}=h\nu=hc/\lambda$, with $h=6.63\times10^{-34}$ J s Planck's constant and $\nu$ the optical frequency: $2.20\times10^{-19}$ J at 905 nm, $2.11\times10^{-19}$ J at 940 nm and $1.28\times10^{-19}$ J at 1,550 nm. Two other quantities in Eq. (37) need care:
"""),
    COPY("- $E_{\\rm pt}$: optical energy transmitted toward one point", tight=True,
         subs=[("(FMCW; subsection 2)", "(FMCW; subsection 1.3)")]),
    COPY("- $\\eta$: end-to-end efficiency from photons at the aperture", "  - **The FMCW value, 0.25, is a design value", tight=True,
         subs=[("in the bright sun of 10.3.", "in the bright sun of subsection 4.2.")]),
    NEW(r"""
A Lambertian surface is perfectly diffuse: it scatters the light it intercepts so that its radiance is the same in every direction, and a fraction $\rho/\pi$ of the intercepted power leaves per steradian along its normal, where $\rho$ is its reflectance. The "10% target" of range specifications has $\rho=0.1$. The receiver's aperture has diameter $D$ and area $A_{\rm rx}=\pi D^2/4$: the receive lens of a direct-detection sensor, or the aperture that the monostatic coherent receiver of subsection 3.2 shares with its transmitter.
"""),
    COPY("**Direct detection: the lens collects the whole spot.**", "- **Worked example:** $D=25$ mm and $R=200$ m give",
         subs=[("This is Eq. (31) of subsection 1 written as a fraction, with $A_{\\rm rx}=\\pi D^2/4$.",
                "Here $T_{\\rm atm}$ is the one-way atmospheric transmission (subsection 3.3).")]),
    NEW(r"""
**The photon budget of one pulse.** For a pulsed ToF lidar it is convenient to count the detected photons of a single pulse. Multiplying the link loss of Eq. (38) by the number of photons in the pulse and by the receiver's efficiencies gives
"""),
    COPY("$$N_{s,1}=\\frac{E_{\\rm p}}{E_{\\rm ph}}", "  - *Substitution.* One 905 nm photon carries",
         subs=[("of the precision row; equivalently", "of the precision row of subsection 1.1; equivalently"),
               ("subsection 5 and §C4c)", "subsection 5.3 and §C4c)")]),
    COPY("- **Small targets.** A target smaller than the beam", tight=True),

    NEW(r"""
#### 3.2 Coherent detection: one spatial mode

A coherent receiver is selective: it responds only to light that arrives in the spatial mode and polarization of its local oscillator (LO). Its collecting power is therefore not its lens area but a smaller, range-dependent *mode-equivalent area*, and its link loss behaves quite differently from that of direct detection: flat in the near field and falling as $1/R^2$ beyond the beam's Rayleigh range. Three quantities describe it:
"""),
    COPY("- $P_{\\rm tx}$: transmitted optical power.", "  - **Not a physical area.**", tight=True,
         subs=[("10.2 derives it (Eqs. (39)–(41)).", "The derivation follows (Eqs. (39)–(41)).")]),
    COPY("**Coherent detection: one spatial mode and the mode-equivalent area.**", "$$A_{\\rm mode}=\\lambda^2R^2\\int",
         subs=[("**Coherent detection: one spatial mode and the mode-equivalent area.** A heterodyne receiver responds only to light in the spatial mode (and polarization) of its local oscillator (LO). Three standard results give its effective collecting area.",
                "**Derivation of the mode-equivalent area.** Three standard results give the effective collecting area of a heterodyne receiver.")]),
    NEW(r"""
**The beam.** The transmitter launches a Gaussian beam, described by:
"""),
    COPY("  - $w_0$: the 1/e² intensity radius", "  - $t=1-e^{-2(D/2)^2/w_0^2}", dedent=2, tight=True,
         subs=[("here $w_0=0.45D$ (10.2 explains the choice).", "here $w_0=0.45D$ (the choice is explained below).")]),
    COPY("**Why the beam is launched with $w_0=0.45D$.**"),
    COPY("In a monostatic system (one aperture shared", "- **Physical reading.** The single-mode receiver collects",
         subs=[("written as an area. §C7b (subsection 1(b)) and §C10.3b use it, and so do the report's scripts.",
                "written as an area."),
               ("(see the assumptions in 10.1)", "(see the assumptions at the start of subsection 3)")]),
    COPY("**A collimated beam: flat near field,", "  - At the optimum, $A_{\\rm mode}=t^2\\lambda R/4"),
    COPY("**Worked numbers at 1,550 nm, $D=25$ mm:**", "- **Envelope at 200 m:**"),
    COPY("![Link loss versus range", "- In both panels the dashed horizontal lines",
         subs=[("the detection levels derived in 10.4 (Eq. (49))", "the detection levels derived in subsection 5.1 (Eq. (49))"),
               ("i.e. the maximum ranges. 10.4 reads the crossings.", "i.e. the maximum ranges, which subsection 5.1 reads.")]),
    COPY("**Reading Figure C0.10a: the shapes of the curves**", "- **At 1,310 nm** the 25 mm plateau"),

    NEW(r"""
#### 3.3 Losses on the way: air, fog, rain, snow and water films

Between sensor and target the light crosses air and, in bad weather, fog, rain or snow; on the way out and back it also crosses the sensor's window, which may be wet or dirty. Each multiplies the link loss by a transmission factor below one. Clear air costs a fraction of a decibel at automotive ranges and dense fog tens of decibels, while rain costs less through the air than through water on the window and through spray. Water on the window costs far more at 1,550 nm than at 905 or 940 nm. What these losses do to each receiver's range is the subject of subsection 5.4.
"""),
    COPY("- **Beer–Lambert, both ways.**"),
    COPY("- **Fog.** Kim's model scales", tight=True,
         subs=[('(the "clear air" of subsection 10.1)', "(clear air)"),
               (" A signal-limited lidar with 200 m clear-air range at 10% reflectance reaches the range where $R^2e^{2\\alpha R}$ equals its clear-air value [E]:",
                " The table gives the extinction coefficient and the two-way loss over 50 m for four visibilities [E]:")]),
    COPY("| Visibility $V$ | $\\alpha$ at 905 nm", "| 20 m (very thick fog)", keepcols=3),
    COPY("=- *How the numbers are derived* [E]:", "  - **Two-way loss at 50 m:**"),
    NEW(r"""
- **Clear air.** With the clear-air exponent $q_{\rm K}=1.3$ (visibility 23 km), the Kim model gives $\alpha=0.085$ /km at 940 nm and 0.044 /km at 1,550 nm, so the two-way transmission $T_{\rm atm}^2$ costs only 0.15 and 0.08 dB at 200 m.
"""),
    COPY("- **Clutter and multiple scattering.**", tight=True,
         subs=[("adds clutter and can saturate SPADs.", "adds clutter and can saturate SPADs (quantified in subsection 5.4)."),
               ("beyond this single-scattering estimate.", "beyond the single-scattering estimates of subsection 5.4.")]),
    COPY("- **Rain.** The empirical free-space-optics law", "  - wet roads, which turn specular", tight=True),
    COPY("- **Snow and sleet**", tight=True),
    NEW(r"""
- **Water films and dirt on the window.** Liquid water absorbs strongly at 1,550 nm: a film on the window, crossed on the way out and again on the way back, costs 9.4 dB per millimetre round trip (§C4c), so a 0.2 mm film costs $0.2\times9.4=1.88\approx1.9$ dB. At 940 nm water absorbs tens of times more weakly, and the film can be neglected. Dust, mud, salt and droplets on the window scatter light out of the beam at every wavelength.
""", tight=True),

    NEW(r"""
### 4. How much light is needed

A receiver needs a minimum number of signal photoelectrons per point to detect an echo reliably without reporting points where there are none. That number depends on how the detector turns light into a signal and what noise comes with it (subsection 4.1), on the background light that competes with the echo (4.2), and on the statistics of deciding, among thousands of range or frequency cells, which one holds the target (4.3).

#### 4.1 Detectors: gain, excess noise, Geiger mode and the local oscillator

A single returning photon produces one photoelectron, far too little charge for an amplifier to see. Lidar detectors therefore multiply it: in a controlled avalanche (a linear avalanche photodiode, APD), in a runaway one (a single-photon avalanche diode, SPAD, operated in Geiger mode), or, in a coherent receiver, by mixing it with a strong local oscillator. Linear gain helps only up to a point set by the detector material, which underlies the choice of silicon at 905/940 nm and the difficulty of InGaAs at 1,550 nm.
"""),
    COPY("- **Linear APD.** An APD is a photodiode biased just below breakdown.", "- **Coherent receivers need no avalanche gain.**",
         subs=[("optical crosstalk between cells (§C4b, §C5a, §C6).",
                "optical crosstalk between cells. Dead time and pile-up are treated in subsection 4.2.")]),

    NEW(r"""
#### 4.2 Background light and dead time

A direct-detection receiver counts every photon that reaches it, signal or not. In daylight the sunlit scene in each pixel's view supplies a steady background whose shot noise competes with the echo, and a photon-counting pixel also loses time after each count. Together they set the background counts per bin that the detection statistics of subsection 4.3 must clear. A coherent receiver is almost immune to the background: its local oscillator rejects light outside its single spatial mode and its narrow band of beat frequencies (subsection 1.3).

**Solar background per pixel.** The rate of background counts in one pixel is
"""),
    COPY("  $$r_{\\rm bg}=\\frac{E_\\odot", dedent=2),
    COPY("=  where:", "  - $A_{\\rm rx}$ is the receive-aperture area, $\\eta_{\\rm opt}$ the optics transmission", dedent=2),
    COPY("  Eq. (32) is the relation §C6 uses as Eq. (89).", dedent=2),
    NEW(r"""
**Signal-to-noise ratio.** In the histogram bins that hold the echo, the photon-counting SNR is $\text{SNR}\approx N_s/\sqrt{N_s+N_b}$, with $N_s$ the signal counts and $N_b$ the background counts in the same bins, both summed over the pulses of one point. Both are Poisson-distributed, so the noise is the square root of the total count, and sunlight, through Eq. (32), sets $N_b$.

**Dead time and pile-up.** After each detection a photon-counting pixel is blind for its dead time. At high count rates this biases the histogram toward early photons (pile-up) and removes part of the echo along with the background (§C4b, §C6).

**The background of the model** [E]. The detection statistics of subsection 4.3 and the comparison of §C7a use a bright-sun background of $b=1.62$ counts per 1 ns bin, summed over the ten shots of a point. It follows from Eq. (32) and the dead time:
"""),
    COPY("  - Eq. (89) gives $r_{\\rm bg}=2.97\\times10^{8}$", "  - The dead time blinds the SPADs to signal photons as well", dedent=2,
         subs=[("- Eq. (89) gives $r_{\\rm bg}=2.97\\times10^{8}$", "- Eq. (32), the relation §C6 uses as Eq. (89), gives $r_{\\rm bg}=2.97\\times10^{8}$"),
               ("the IMX479 grid of subsection 5)", "the IMX479 grid of the example above)"),
               ("and the 25 mm aperture Eq. (89) reads", "and the 25 mm aperture Eq. (32) reads"),
               ("with the 21.7 signal counts of 10.4 that is", "with the 21.7 signal counts of subsection 5.1 that is")]),

    NEW(r"""
#### 4.3 Detection statistics under one rule

A return counts as detected when it crosses a threshold set above the noise. The threshold trades the detection probability $P_D$, the chance that a real echo crosses it, against the false-alarm probability $p$ of each range or frequency cell, the chance that noise alone crosses it there. Because noise can cross in any of the cells searched, the chance of a false point grows with their number, and so does the threshold needed for a given false-point rate. A stated range therefore means little without its $P_D$ and its false-alarm definition (§C3b). Both receivers are held below to one rule, first for photon counting and then for coherent detection of a speckled target.
"""),
    COPY("**The detection rule.** A point must be detected", "- **Per-bin probability.**",
         subs=[(" Subsection 7 uses the same per-point budget, but with 1,000 bins (so $10^{-6}$ per bin) and a daylight background of one count per bin, for which an ideal counter needs ≈13 signal counts. The 2,000 bins and the 1.62 background counts per bin of the §C7a model raise this to 15.0 here.", ""),
               ("- **What it allows.** At 10 Mpts/s, $10^{-3}$ per point is $10^{4}$ false points per second before any filtering; products remove most of them with neighbour-consistency checks (subsection 7).",
                "- **What it allows.** At 1.5 Mpts/s (the Hesai AT128) the budget still allows 1,500 false points a second, 150 per 10 Hz frame, and at 10 Mpts/s $10^{4}$ a second, before any filtering [E: $1.5\\times10^6\\ {\\rm s^{-1}}\\times10^{-3}=1{,}500\\ {\\rm s^{-1}}$, and $1{,}500/10=150$]. Products therefore add multi-pulse or neighbour-consistency checks before a point is output.")]),
    COPY("- **Vendors define the terms differently.**", tight=True),
    COPY("*Photon counting (SPAD histogram).*", "- **Bright sun, $b=1.62$:**",
         subs=[("- **Bright sun, $b=1.62$:**", "- **Bright sun, $b=1.62$ (subsection 4.2):**")]),
    NEW(r"""
- **A stricter budget.** At $10^{-6}$ false points per point, i.e. $5\times10^{-10}$ per bin, the thresholds rise to 4 counts at night and 15 in bright sun, and $P_D=0.9$ needs 6.7 and 18.5 signal counts instead of 5.3 and 15.0 [E: $P(N\ge3\mid0.01)=1.7\times10^{-7}$ fails and $P(N\ge4\mid0.01)=4.1\times10^{-10}$ passes; $P(N\ge14\mid1.62)=2.2\times10^{-9}$ fails and $P(N\ge15\mid1.62)=2.3\times10^{-10}$ passes; $P(N\ge4\mid6.68)=0.9$ and $P(N\ge15\mid20.13)=0.9$]. A thousandfold stricter false-point budget costs a photon counter only about a quarter more signal.
""", tight=True),
    COPY("*Coherent detection in one frequency bin", "  where $Q_1(u,v)$ is Marcum's Q function",
         subs=[("equals $\\bar n$ (subsection 2), so", "equals $\\bar n$ (subsection 1.3), so")]),
    NEW(r"""
- **One speckle.** A rough target scatters the coherent light from many randomly phased patches, and their sum at the receiver is a random speckle pattern. In a single speckle the return's amplitude is Rayleigh-distributed, so its intensity is exponentially distributed: deep fades are common. For a single look with square-law detection (the receiver compares the beat power, not its amplitude, with the threshold),
""", tight=True),
    COPY("$$P_D=p^{1/(1+\\bar n)} . \\tag{46}$$", tight=True),
    COPY("  where $p$ is the false-alarm probability of the bin tested", tight=True,
         subs=[("and $\\overline{\\rm SNR}$ the mean signal-to-noise ratio, averaged over the speckle fading.",
                "and $\\bar n$ the mean signal-to-noise ratio, averaged over the speckle fading; in a shot-noise-limited receiver $\\bar n$ is also the mean number of signal photoelectrons (subsection 1.3).")]),
    COPY("  - $P_D=0.9$ at $p=10^{-6}$ then needs a mean SNR", "    - *Steady target:* Albersheim's empirical approximation", tight=True,
         subs=[("  - $P_D=0.9$ at $p=10^{-6}$ then needs a mean SNR", "  - *One bin tested alone.* $P_D=0.9$ at $p=10^{-6}$ needs a mean SNR"),
               ("$1+\\overline{\\rm SNR}=\\ln p/\\ln P_D", "$1+\\bar n=\\ln p/\\ln P_D"),
               ("so $\\overline{\\rm SNR}\\approx130$", "so $\\bar n\\approx130$")]),
    NEW(r"""
  - In a shot-noise-limited receiver the SNR equals the detected photoelectrons, so this single bin needs ≈130 of them. A full FMCW point held to the rule above needs ≈259 with one look, twice the single-bin ≈130, because its peak must be found in both chirp ramps after a search over the whole range; four independent looks bring the total, summed over both ramps and all looks, down to ≈88 (Eq. (48) and the table below). Polarization, wavelength or spatial diversity recovers much of the fading penalty.
""", tight=True),
    COPY("  - The practical consequence is that speckle fading", tight=True),
    COPY("- **$N_{\\rm sp}$ independent speckles summed incoherently**", "$$P_D=Q\\!\\left(N_{\\rm sp},", tight=True),
    COPY("*An FMCW point: both ramps, over the whole range.*", "  - **Reading.** The square is the two ramps' independent noise",
         subs=[("(subsection 2)", "(subsection 1.3)", 2),
               ("round trips at 200 m, subsection 2)", "round trips at 200 m, subsection 1.3)")]),
    COPY("The table gives both receivers' requirements under this rule.", "**What this means for the comparison** [E].",
         subs=[("21.7 for ToF (10.4) and 120 for FMCW (four looks)", "21.7 for ToF (subsection 5.1) and 120 for FMCW (four looks)"),
               ("(the live fraction above, §C7a(a))", "(the live fraction of subsection 4.2, §C7a(a))"),
               ("at Waymo's own $10^{-6}$ per bin (10.8).", "at Waymo's own $10^{-6}$ per bin (subsection 6.1)."),
               ("10.4 turns the model's counts", "Subsection 5.1 turns the model's counts")]),
]
