"""Plan of the restructured §C0, part A: opening, 1 (measuring one point) and 2 (from points to images)."""
from c0_lib import NEW, COPY

PLAN_A = [
    NEW(r"""
## C0. Physics of lidar ranging

A lidar measures range by sending light to a target and analysing what comes back. Every number in Part C rests on one chain of physics: how the echo encodes range and velocity, how finely beams and pixels sample the scene, how much of the transmitted light returns, how much a reliable detection needs, and how those two amounts set range, robustness and dynamic range. This chapter follows that chain in order, from the measurement of a single point to a link budget tested against published systems:
1. **Measuring one point** (subsections 1.1–1.4): pulsed time of flight, phase ranging with modulated light, and frequency-modulated coherent ranging, which also measures velocity.
2. **From points to images** (2.1): beam divergence, pixel field of view, scan rates and étendue.
3. **How much light comes back** (3.1–3.3): the link loss of direct and coherent detection, and the losses of air, fog, rain and wet windows.
4. **How much light is needed** (4.1–4.3): detector gain and noise, background light, and detection statistics under one false-alarm rule.
5. **Range, its limits and its robustness** (5.1–5.5): maximum range and how it scales, the eye-safety cap on energy, the margin left for dark targets and bad weather, and the dynamic range of strong returns.
6. **Testing the model** (6.1–6.2): a benchmark against published systems, and what the model leaves out.

Each subsection states its relations, evaluates them for typical automotive numbers with a worked substitution, and says what they mean for the sensor. Numbers are illustrative engineering estimates [E] unless tagged otherwise, and $c=3.0\times10^8$ m/s is the speed of light throughout. Later sections apply these relations, some restating them in their own notation and numbering; the table at the end of the chapter lists where. The script `build/figures/link_budget_scaling.py` draws Figures C0.10a–C0.10d and writes the link-budget numbers of subsections 3.1–6.1 to `link_budget_scaling_tables.txt`. Those numbers are for a Lambertian target that fills the illuminated spot, at normal incidence and in clear air unless stated otherwise.

**Main results** [E]:
"""),
    COPY("- **Direct detection collects a fraction proportional to $D^2/R^2$ at every range** (10.2)",
         "- **The model agrees with published systems** (10.8)",
         subs=[("(10.2)", "(subsections 3.1–3.2)"), ("(10.5)", "(subsection 5.2)", 2), ("(10.1)", "(subsection 3.1)"),
               ("(10.6)", "(subsection 5.4)", 2), ("(10.7)", "(subsection 5.5)"), ("(10.8)", "(subsection 6.1)")],
         tight=True),

    NEW(r"""
### 1. Measuring one point

A lidar can encode range in three ways: in the delay of a pulse, in the phase of an intensity modulation, or in the frequency difference between a swept laser and its echo. The three principles differ in what limits their precision and their unambiguous range, in how they reject ambient light, and in whether they measure velocity directly. Subsections 1.1–1.3 take them in turn, and subsection 1.4 compares the velocity each can deliver.

#### 1.1 Pulsed time of flight (dToF)

A pulsed direct time-of-flight (dToF) lidar fires a short laser pulse and times its echo; the range is half the round-trip delay times the speed of light. The timing relations below set its range resolution, precision, unambiguous range and point rate. How many photons the echo carries, which decides whether it is detected at all, is the subject of subsections 3.1 and 4.3.
"""),
    COPY("**Symbols in the table.**", "- **Point rate:** $\\dot N=128", dropcol=True,
         subs=[("with the same meaning in subsection 9.", "with the same meaning in subsection 1.2."),
               ("(SPADs, subsection 6)", "(SPADs, subsection 4.1)")]),

    NEW(r"""
#### 1.2 Phase ranging with modulated light (AMCW, iToF)

A pulse is not the only way to time light: the delay can also be read from the phase shift of an intensity modulation. That principle runs ToF cameras, surveying rangefinders and phase-based laser scanners, yet it gives millimetre precision at hundreds of metres in a surveying scanner and stops near 10 m in a camera; the difference lies in the photon budget, not in the principle. The products, the chips inside them and where usage draws the boundary of "lidar" are surveyed in §C1a. For cars, phase ranging (indirect ToF, iToF) suits the cabin, while exterior sensing uses pulsed dToF or FMCW.
"""),
    COPY("**Principle.** An amplitude-modulated", "- **The split is the same everywhere.**",
         subs=[("- **FMCW (subsection 2) is the coherent counterpart.**",
                "- **FMCW, the subject of subsection 1.3, is the coherent counterpart.**"),
               ("over noise $\\propto\\sqrt{A_{\\rm rx}}$, as in subsection 1)",
                "over noise $\\propto\\sqrt{A_{\\rm rx}}$; subsection 5.2)"),
               ("Pulsed dToF (subsection 1) gates out", "Pulsed dToF (subsection 1.1) gates out")]),
    COPY("Sources: https://www.ti.com/lit/ug/sbau219d"),

    NEW(r"""
#### 1.3 Frequency-modulated coherent ranging (FMCW)

A frequency-modulated continuous-wave (FMCW) lidar does not time its light at all. It sweeps the laser's optical frequency and measures the frequency difference between the echo and the light being sent at that moment. That difference encodes range, and its Doppler part gives each point's radial velocity directly. The relations below set FMCW's resolution, precision, receiver bandwidth and point rate. Their practical consequence is that each coherent channel must dwell for microseconds per point and digitize hundreds of megahertz, so per-channel throughput is one of the hard limits on FMCW point rates.
"""),
    COPY("**Principle and symbols.**", "In short, FMCW trades the timing electronics", dropcol=True,
         subs=[("subsection 10 uses $\\bar n$ for the total over both ramps of a point",
                "subsection 4.3 uses $\\bar n$ for the total over both ramps of a point"),
               ("counted over both ramps and all looks (§C0 subsection 10.3)",
                "counted over both ramps and all looks (subsection 4.3)"),
               ("the §C7a model and §C0 subsection 10.3 integrate 5 µs in each ramp",
                "the §C7a model and subsection 4.3 integrate 5 µs in each ramp"),
               ("(the antenna theorem, §C7)", "(the antenna theorem, subsection 3.2)"),
               ("that speckle fading removes (§C10.3a)", "that speckle fading removes (subsection 4.3)"),
               ("errors** (§C7, §C10.3a, §C4d). Here", "errors.** Here")]),

    NEW(r"""
#### 1.4 Velocity: measured or differenced
"""),
    COPY("Knowing how fast an object moves", "- **Neither measures the tangential component directly.**",
         subs=[("for a 10 µs ramp (subsection 2), and", "for a 10 µs ramp (subsection 1.3), and"),
               ("ten times the ideal 0.3 cm of subsection 1 to allow", "ten times the ideal 0.3 cm of subsection 1.1 to allow")]),

    NEW(r"""
### 2. From points to images

A single range measurement becomes an image only when the sensor repeats it across a field of view. How finely the scene is sampled, and how fast, is set by geometry: the divergence of the beam, the angle each receiver pixel sees, the number of points per frame and the rate at which a scanner can sweep. The same relations tie the size of the optics to the field of view, which is why resolution, range and scan speed cannot all be improved at once.

#### 2.1 Beams, pixels and sampling
"""),
    COPY("=**Symbols.**", "The practical consequence is that parallel channels relieve the scanner", dropcol=True,
         subs=[("$N_{\\rm par}=N_{\\rm ch}$ of subsection 1 when", "$N_{\\rm par}=N_{\\rm ch}$ of subsection 1.1 when"),
               ("the square root of the energy per point (subsection 1).",
                "the square root of the energy per point (subsection 5.2)."),
               ("the point rate of subsection 1 |", "the point rate of subsection 1.1 |")]),
]
