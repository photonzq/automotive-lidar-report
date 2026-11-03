"""Insert the §A4 blocks "The thermistor: where the NETD comes from", "VOx against a-Si" (signal, noise and smaller
pixels; making them in volume) and "Why not a phase transition" before the vacuum-packaging block, restate the pixel-pitch sentence on 1/f noise, and add the matching Appendix 1 item and Appendix 2 sources.
The numbers come from thermistor_netd.py. Usage: thermistor_block_edit.py <report .md> <expected sha256 prefix> [--write]
Each anchor must match exactly once and the starting hash must match; the inserted text is normalised to the report's
code points (micro sign, U+03A9 omega) and written with LF line endings."""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text


def norm(s):
    s = s.replace("μ", "µ").replace("Ω", "Ω").replace(" ", " ").replace(" ", " ")
    return s


def insert_before(anchor, new):
    global text
    assert text.count(anchor) == 1, f"anchor count {text.count(anchor)}: {anchor[:70]!r}"
    i = text.index(anchor)
    text = text[:i] + norm(new) + text[i:]


def insert_after_line(anchor, new):
    global text
    assert text.count(anchor) == 1, f"anchor count {text.count(anchor)}: {anchor[:70]!r}"
    i = text.index("\n", text.index(anchor)) + 1
    text = text[:i] + norm(new) + text[i:]


def replace(old, new):
    global text
    assert text.count(old) == 1, f"count {text.count(old)}: {old[:70]!r}"
    text = text.replace(old, norm(new))


BLOCK = r"""**The thermistor: where the NETD comes from**

A microbolometer pixel is a membrane suspended on thin legs above the readout circuit. Infrared from the scene warms the membrane, and a thermistor film on it, vanadium oxide (VOx) or amorphous silicon (a-Si) in almost every product, turns the warming into a change of resistance. The noise-equivalent temperature difference (NETD), the change of scene temperature that gives a signal equal to the rms noise, follows from the steps below; the thermistor material enters through its temperature coefficient of resistance (TCR) and its noise [E].
- **From scene to pixel.** A lens of f-number $F$ and transmission $\tau_0$ in front of a pixel of area $A_d$, absorptance $\eta$ and fill factor $\beta$ (the fraction of the pixel area that absorbs) delivers an absorbed power $P$ that changes with the scene temperature $T_{\rm s}$ as

  $$\frac{dP}{dT_{\rm s}}=\frac{\tau_0\,\eta\beta\,A_d}{4F^2+1}\,\frac{dM}{dT_{\rm s}} \label{eq:bolo-scene-power}$$

  where $M$ is the scene's exitance in the 8–14 µm band, the power it radiates per unit area, and $A_d/(4F^2+1)$ is the factor of the pixel-pitch block above. Integrating Planck's law gives $dM/dT_{\rm s}=2.63\ {\rm W\,m^{-2}\,K^{-1}}$ for a 300 K scene [E, `thermistor_netd.py`]. Wang et al. (*Nanomaterials* 15, 1316, 2025, §2.2.4) quote $2.62\times10^{-4}\ {\rm W\,cm^{-2}\,K^{-1}}$ labelled for 295 K, which is the 300 K value; the integral gives $2.51\times10^{-4}$ at 295 K [I; E]. A 12 µm pixel behind an F/1 lens therefore absorbs $7.6\times10^{-11}\,\tau_0\eta\beta$ W more for each kelvin of scene temperature [E].
- **From pixel temperature to signal.** The absorbed power warms the membrane, of heat capacity $C$, against the thermal conductance $G$ of its legs, so the membrane follows changes with the time constant $\tau=C/G$. A bias current $I_b$ through the thermistor resistance $R_b$ turns the warming into a voltage. For power modulated at angular frequency $\omega$ the responsivity, in volts per watt of absorbed power, is

  $$\mathcal{R}_V=\frac{I_bR_b\,|\alpha|}{G\sqrt{1+\omega^2\tau^2}} \label{eq:bolo-responsivity}$$

  where $\alpha=(1/R)\,dR/dT$ is the TCR (Wang et al. 2025, Eq. 12, which counts $\eta\beta$ in the responsivity rather than in the absorbed power) [I].
- **Noise.** Four independent sources add in quadrature:

  $$\langle v_n^2\rangle=4k_BTR_b\,\Delta f+\frac{\alpha_H}{n\,\Omega}\,V_b^2\ln\frac{f_2}{f_1}+\mathcal{R}_V^2\,4k_BT^2G\,\Delta f_{\rm th}+\langle v_{\rm ROIC}^2\rangle \label{eq:bolo-noise}$$

  - The first term is the thermistor's Johnson noise, with $k_B$ Boltzmann's constant, $T$ the pixel temperature and $\Delta f$ the electrical bandwidth of the readout.
  - The second is its 1/f noise in Hooge's form, a spectral density $(\alpha_H/N)V_b^2/f$ integrated over the readout band from $f_1$ to $f_2$. Here $V_b=I_bR_b$ is the bias voltage, $\alpha_H$ the dimensionless Hooge parameter and $N=n\Omega$ the number of free carriers in the film, its carrier density $n$ times its volume $\Omega$ (Wang et al. 2025, Eqs. 17–18) [I].
  - The third is the thermal-fluctuation noise: heat crosses the legs in random portions, a power noise of $4k_BT^2G$ per hertz (Wang et al. 2025, Eq. 19) [I], which the pixel's own thermal low-pass limits to the equivalent bandwidth $\Delta f_{\rm th}=1/(4\tau)$ [E].
  - The last is the noise of the readout integrated circuit (ROIC).
- **The NETD** is the rms noise divided by the signal per kelvin of scene temperature (Wang et al. 2025, Eq. 23, written with $4F^2$, the limit of $4F^2+1$ at large f-number) [I]:

  $$\mathrm{NETD}=\frac{\sqrt{\langle v_n^2\rangle}}{\mathcal{R}_V\,dP/dT_{\rm s}} \label{eq:bolo-netd}$$

- **The thermal-fluctuation floor.** With the third term alone, the bias and the thermistor drop out of Eqs. \eqref{eq:bolo-scene-power}–\eqref{eq:bolo-netd} at low frequency:

  $$\mathrm{NETD}_{\rm th}=\frac{(4F^2+1)\sqrt{k_BT^2G/\tau}}{\tau_0\eta\beta\,A_d\,dM/dT_{\rm s}} \label{eq:bolo-netd-thermal}$$

  For the 12 µm membrane of the vacuum-packaging block below, $C=7\times10^{-11}$ J/K. Time constants of 12 and 7 ms give $G=C/\tau=5.8$ and 10 nW/K, and $\sqrt{k_BT^2G/\tau}=7.8\times10^{-13}$ and $1.3\times10^{-12}$ W at 300 K. Divided by the $7.6\times10^{-11}$ W per kelvin above, the floor at F/1 is 10–18 mK times $1/(\tau_0\eta\beta)$ [E, `thermistor_netd.py`]. The 12 µm detectors quoted in this section sit near 40 mK: the Boson 640 at <40 mK [S], and Raytron's 12 µm detectors and a domestic peer's at 40 mK in Raytron's own comparison (2019 prospectus, p. 186) [P]. The electrical noise of the thermistor and the readout is therefore at least comparable to the floor, and that part depends on the material and the bias scheme [E].
- **The 1/f-limited case.** When the second term dominates, the bias cancels between signal and noise:

  $$\mathrm{NETD}_{1/f}=\frac{(4F^2+1)\,G\sqrt{1+\omega^2\tau^2}}{\tau_0\eta\beta\,A_d\,dM/dT_{\rm s}}\cdot\frac{1}{|\alpha|}\sqrt{\frac{\alpha_H}{n\,\Omega}\ln\frac{f_2}{f_1}} \label{eq:bolo-netd-flicker}$$

  The material then enters only through the ratio $|\alpha|/\sqrt{\alpha_H/n}$: a higher TCR helps only if the film keeps many free carriers and a low Hooge parameter [E].
- **Why a semiconducting film.** In a thermally activated film $R=R_\infty\exp(E_a/k_BT)$, with $E_a$ the activation energy, so

  $$\alpha=\frac{1}{R}\frac{dR}{dT}=-\frac{E_a}{k_BT^2} \label{eq:thermistor-tcr}$$

  Honeywell's 100 nm VOx film follows $\ln R=1.8069+2600.6\ {\rm K}/T$ (US 6,322,670 B2, Fig. 2) [P], so $E_a=k_B\times2600.6\ {\rm K}=0.224$ eV and $\alpha=-2600.6/293.15^2=-3.0$ %/K at 20 °C, the TCR printed beside the fit [E]. A metal whose resistivity is limited by phonon scattering has $\rho\propto T$ and so $\alpha\approx1/T=+0.34$ %/K; Honeywell gives 0.3–0.4 %/K for metals and adds that they reflect the infrared they should absorb (col. 1, ll. 15–21) [P]. An activated film therefore gives about nine times the signal per kelvin. The price is noise: a larger $E_a$ leaves fewer free carriers, a higher resistance and more 1/f noise. Honeywell writes the trade for its VOx as roughly $\mathrm{TCR}=0.03+0.01\log_{10}\rho$, about 1 %/K per decade of resistivity $\rho$ in Ω·cm (col. 2, ll. 13–17) [P].

**VOx against a-Si: signal, noise and smaller pixels**
- **TCR.** At resistivities a readout circuit can handle, both reach 2–3 %/K in magnitude. Moreno et al. (*Bolometers*, InTech, 2012, p. 27, Table 1) list VOx at 0.021 K⁻¹ with $E_a=0.16$ eV and boron-doped hydrogenated a-Si (a-Si:H,B) at 0.028 K⁻¹ with $E_a=0.22$ eV [S]; Eq. \eqref{eq:thermistor-tcr} reproduces both, 2.1 and 2.8 %/K at 300 K [E]. Undoped a-Si:H reaches 10–13 %/K, but at a conductivity of about $10^{-9}$ S/cm its resistance cannot be matched to the readout circuit (same page) [S].
- **Noise.** At a similar TCR, Honeywell's VOx conducts about 470 times better than the doped a-Si of the same table: 0.43 Ω·cm at 3.0 %/K (Fig. 2) [P] against 200 Ω·cm ($5\times10^{-3}$ S/cm) at 2.8 %/K [S; E]. In Hooge's picture a better-conducting film at the same TCR usually holds more free carriers per pixel and so less 1/f noise [E]. The available statements agree on the direction. Honeywell reports 1/f constants $k=\alpha_H/N$ "as low as $10^{-12}$ to $10^{-14}$", which leave its pixels "close to Johnson noise limited" (col. 2, ll. 40–49) [P]. Wang et al. list "elevated 1/f noise" among a-Si's drawbacks (Introduction) [I]. Lynred, whose detectors have used a-Si since ULIS's day, wrote in 2022 that a-Si's "intrinsic bolometric performances (i.e. TCR and 1/f noise) are still lower" than those of the oxide thermistors VOx and TiOx [P, Lynred, SPIE DCS 2022 abstract], although ULIS had claimed in 2003 an a-Si figure of merit of about 2.4 %/K, "superior" to VOx (Tissot, *C. R. Physique* 4, 1083, 2003, p. 1085) [P]. No comparison of the two at the same pixel volume, measured the same way, was found (Appendix 1).
- **Uniformity.** a-Si brings the evenness of silicon processing: across ULIS's 160 × 120 prototype the responsivity varied by 1.4% (one standard deviation), which the authors credit to "l'utilisation d'une technologie silicium", the use of silicon technology (Tissot 2003, p. 1086, Table 3) [P].
- **Smaller pixels.** At a fixed time constant the leg conductance scales with the pixel area (pixel-pitch block), so $G/A_d$ in Eq. \eqref{eq:bolo-netd-flicker} stays fixed while the film volume $\Omega=A_dt_f$, with $t_f$ the film thickness, shrinks with the area. The 1/f-limited NETD therefore grows as $1/\sqrt{A_dt_f}\propto1/d$ for a pixel pitch $d$: a factor of 1.5 from 12 to 8 µm, the same factor as the thermal-fluctuation floor, and more if the film is thinned to cut the heat capacity [E]. Small pixels thus need a better $|\alpha|/\sqrt{\alpha_H/n}$, a faster lens or both. Lynred took the material route: with CEA-Leti it developed new thermistor materials, introduced a 17 µm detector at 25 mK typical (F/1, 300 K, 30 Hz) at the end of 2020, and launched a 12 µm range "with performances equivalent to our current 17µm product range" [P, Lynred 2022].

**VOx against a-Si: making them in volume**
- **a-Si** is deposited by plasma-enhanced chemical vapour deposition (PECVD) below 350 °C, evenly over large areas, and is fully compatible with standard CMOS processes (Wang et al. 2025, Introduction) [I]. CEA-Leti chose it in 1992 for that reason: a monolithic structure and compatibility with silicon were "the two essential characteristics" for producing good uncooled arrays at low cost (Tissot 2003, p. 1085) [P].
- **VOx** is non-stoichiometric, $\mathrm{VO}_x$ with $x$ between 1 and 2.5, and the oxygen level during deposition sets its properties. Honeywell sputters a vanadium target with an argon ion beam and servoes the oxygen flow on the 32-amu signal of a residual-gas analyser, because "the precise location of the operating setpoint determines the resistance and TCR" (US 6,322,670 B2, col. 1, ll. 37–41; col. 4, ll. 13–28) [P]. The process stays at about 80 °C (col. 4, ll. 60–63) [P], so it can coat a finished readout wafer, but vanadium does not belong in a silicon fab: VOx "must be produced on dedicated lines to avoid contamination, thereby increasing the production complexity and cost" (Wang et al. 2025, Introduction) [I].
- **Licences.** VOx was Honeywell's patented technology, developed with the US Department of Defense, classified until 1992 and then licensed in two waves, in the early 1990s and the early 2000s [S, Knowmade, Jul 2015]. NEC, after about five years on its own VOx route, took a Honeywell licence so that it could industrialise without infringing (Tissot 2003, p. 1085) [P]. CEA-Leti's a-Si was its own route [P].
- **Volume.** Despite the dedicated lines, VOx won most of the volume. Maxtech counted 79% of the 46,000 civil uncooled detectors sold in 2004 as Honeywell-licensed technology and 14% as ULIS's [S, Maxtech International, in Dali Technology's 2008 prospectus, p. 1-1-324], and Knowmade put VOx at 79% of the market in 2015 [S]. In China, Raytron, itself a VOx maker, describes two of its three domestic peers as VOx makers, one of which began with a-Si, and the third as an a-Si maker (2019 prospectus, pp. 174 and 186) [P].

**Why not a phase transition**
- **The attraction.** A phase transition gives a far larger TCR than activation. Crystalline vanadium dioxide (VO₂) switches from insulator to metal at 340 K, and its conductivity jumps from $4.6\times10^3$ to $8.0\times10^5$ S/m (Lee et al., *Science* 355, 371, 2017, p. 371 and Fig. 1B inset) [I].
- **Honeywell's four objections.** The latent heat of the transition lowers the sensitivity; each material comes essentially in one form, whose resistance and TCR cannot be adjusted without doping; the transition spans so narrow a range of temperature that the sensor must be held at a tightly controlled temperature; and the films must be crystalline, which needs hot deposition (US 6,322,670 B2, col. 1, ll. 21–33) [P].
- **Hysteresis.** A bolometer made of monoclinic VO₂ "is only usable below the temperature (about 68 °C) at which a hysteresis loop is formed" (KIST and UNIST, US 10,371,571 B2, col. 2, ll. 1–4) [P]. A car's camera faces −40 to +105 °C (vacuum-packaging block), so a transition thermistor would need its focal plane held at one temperature by active control [E].
- **Production VOx avoids the transition by design.** Honeywell's films are amorphous and "exhibit no latent heat effects unlike the phase transition effects in VO2" (col. 2, ll. 35–37) [P], and the film of its Fig. 2 follows one straight Arrhenius line from about 290 to 377 K, through 340 K without a step [P; E].

"""

insert_before("**Vacuum packaging: why every microbolometer needs it, and how it became cheaper**", BLOCK)

replace("The thermistor's 1/f noise, which grows as its volume shrinks, adds to the penalty.",
        "The thermistor's 1/f noise grows by the same factor at a fixed film thickness, and by more if the film is "
        "thinned (next block).")

APPX1 = r"""- **Thermistor materials (§A4).** No source found compares the 1/f noise of VOx and a-Si films of equal volume measured the same way: Honeywell's 1/f constants come without the pixel volume, and the a-Si values found come from research pixels. The thermal-fluctuation floor of §A4 rests on an assumed membrane heat capacity and on time constants from secondary sources, and the absorptance, fill factor and lens transmission of production pixels are not published. The materials behind Lynred's products of 2020–2022 are not disclosed.
"""
insert_after_line("- **Thermal detector packages (§A4).**", APPX1)

APPX2 = r"""- Tissot, J.-L., "La détection infrarouge avec les plans focaux non refroidis : état de l'art", *C. R. Physique* 4, 1083–1088 (2003) (Fig. 1; pp. 1085–1086; Tables 1–3): https://doi.org/10.1016/j.crhy.2003.10.015
- Wang, B. et al., "Convergence of Thermistor Materials and Focal Plane Arrays in Uncooled Microbolometers: Trends and Perspectives", *Nanomaterials* 15, 1316 (2025) (Introduction; §2.2.4; Eqs. 12, 17–19 and 23): https://doi.org/10.3390/nano15171316
- Moreno, M., Torres, A., Ambrosio, R. and Kosarev, A., "Un-Cooled Microbolometers with Amorphous Germanium-Silicon (a-GexSiy:H) Thermo-Sensing Films", in *Bolometers* (InTech, 2012), pp. 26–27, Table 1: https://doi.org/10.5772/32222
- Honeywell (B. E. Cole et al.), US 6,322,670 B2, flexible VOx microbolometer material by controlled ion-beam sputtering (27 Nov 2001; cols. 1–4, Figs. 1–2): https://patents.google.com/patent/US6322670B2
- KIST and UNIST, US 10,371,571 B2, thin-film VO₂ for micro-bolometers (cols. 1–2): https://patents.google.com/patent/US10371571B2
- Lynred, "Recent thermoresistive material evolutions at LYNRED for improving uncooled microbolometer products thermal sensitivity", SPIE DCS 2022 abstract: https://lynred.com/sites/default/files/2022-03/Abstract%20SPIE%20DCS.pdf
- Lee, S. et al., "Anomalously low electronic thermal conductivity in metallic vanadium dioxide", *Science* 355, 371–374 (2017) (Fig. 1B): https://doi.org/10.1126/science.aag0410
- Knowmade, Honeywell microbolometer patent portfolio analysis, flyer (Jul 2015), p. 1: https://www.knowmade.com/wp-content/uploads/2015/07/FLYER_Honeywell_Microbolometer_Patent_Analysis_2015.pdf
- Dali Technology, IPO prospectus (2008), p. 1-1-324 (Maxtech International's 2004 civil market shares): http://static.cninfo.com.cn/finalpage/2008-01-25/37105413.PDF
- Raytron Technology, IPO prospectus (2019), pp. 174 and 186: http://static.cninfo.com.cn/finalpage/2019-07-08/1206430547.PDF
"""
insert_after_line("- Reseller specification listings with NETD by grade: Boson SX8, https://groupgets.com/products/flir-boson-sx8", APPX2)

new = text.encode("utf-8")
odd = sorted({c for c in text if ord(c) > 127} - {c for c in raw.decode("utf-8") if ord(c) > 127})
print("old sha", sha[:12], "new sha", hashlib.sha256(new).hexdigest()[:12], "bytes", len(raw), "->", len(new))
print("non-ASCII characters new to the report:", [f"U+{ord(c):04X}" for c in odd])
if "--write" in sys.argv:
    report.write_bytes(new)
    print("written")
