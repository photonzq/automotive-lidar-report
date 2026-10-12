"""Builds edits/round2/R2C_C7-C7a.json (Round 2, executive summary, C7, C7a, D7, F6).

Every "old" is cut from the live report (read only) with unique anchors, and every "new" is either written
out or made from "old" by replacements that must each match exactly once. Numbers come from
r2c_c7a_numbers.py (the installed fmcw_tof_system_budget.py model).
Run from the report folder:  python scripts_archive/readability_2026-10-03/round2/scripts/r2c_build_edits.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT_DIR = HERE.parents[3]
REPORT = REPORT_DIR / "automotive_perception_report_2026-09-27.md"
OUT = HERE.parents[1] / "edits" / "round2" / "R2C_C7-C7a.json"
LABEL = "R2C_C7-C7a"

text = REPORT.read_text(encoding="utf-8")
edits, skipped = [], []


def uniq(s):
    k = text.count(s)
    assert k == 1, f"occurs {k} times: {s[:90]!r}"
    return s


def span(start, end):
    """Unique text from `start` through the first `end` after it."""
    uniq(start)
    i = text.index(start)
    j = text.index(end, i)
    assert j + len(end) >= i + len(start), "end found inside start"
    return uniq(text[i:j + len(end)])


def rep(old, pairs):
    new = old
    for a, b in pairs:
        k = new.count(a)
        assert k == 1, f"replacement source occurs {k} times: {a[:90]!r}"
        new = new.replace(a, b)
    return new


def add(finding, old, new, why):
    uniq(old)
    new = new.replace("μ", "µ")
    assert new != old
    edits.append({"id": f"{LABEL}-{len(edits)+1:03d}", "finding": finding, "old": old, "new": new, "why": why})


def skip(finding, kind, location, detail):
    skipped.append({"finding": finding, "kind": kind, "location": location, "detail": detail})


D1 = "round2 decision 1 (ungated dwell T_int+2tau)"
D2 = "round2 decision 2 (ToF pixel 0.05 x 0.05 deg)"
D3 = "round2 decision 3 (ToF n_req 21.7)"
D5 = "round2 decision 5 (parity follows C7b subsection 5)"
MODEL = "round2 model outputs (fmcw_tof_system_budget tables)"

# ---------------------------------------------------------------- section 0
add("round2 model outputs (C4c count-rate headroom)",
    "InGaAs SPADs would run ≈700× over their count-rate ceiling in sunlight, i.e. background photons would saturate them.",
    r"InGaAs SPADs would run ≈340× over their count-rate ceiling in sunlight ($3.4\times10^{8}$ background counts/s in a 0.05° × 0.05° pixel against the ≈$10^{6}$ counts/s that a 1 µs hold-off allows, §C4c subsection 3), i.e. background photons would saturate them.",
    "The 0.05° pixel halves the 1,550 nm background (6.77e8 to 3.38e8 counts/s), so 677× becomes 338×; derivation shown.")

add(f"{MODEL}; {D1}; {D2}",
    r"At 200 m and 10% reflectivity, the modelled electrical energy per point is ≈4.3 µJ for FMCW against ≈0.54 µJ for 940 nm SPAD ToF, whose SPADs lose ≈22% of the signal to their 6 ns dead time in bright sun. That is ≈8×, since $4.25/0.536\approx7.9$ (≈4× in an optimistic 2032 case).",
    r"At 200 m and 10% reflectivity, the modelled electrical energy per point is ≈4.9 µJ for FMCW against ≈0.42 µJ for 940 nm SPAD ToF, whose SPADs lose ≈11.5% of the signal to their 6 ns dead time in bright sun. That is ≈12×, since $4.90/0.415\approx11.8$ (≈6× in an optimistic 2032 case, $1.74/0.280\approx6.2$). The FMCW figure counts all the light its continuous-wave laser emits during its dwell on a point, including the light sent during the round trips, whose echoes fall in discarded windows.",
    "Model totals 4.899 / 0.415 µJ (2026) and 1.738 / 0.280 µJ (2032); dead fraction 11.5% at the 0.05° pixel; the ungated emission is stated.")

add(f"{D3}",
    "against ≈17 counts for SPAD ToF in bright sun (the model uses 120 and 25)",
    "against ≈15 counts for SPAD ToF in bright sun (the model uses 120 and 21.7)",
    "Ideal ToF requirement 14.98 counts at b = 1.62; model n_req = 21.7.")

add(f"{D1}",
    "At 10 Mpts/s (million points per second) that means ≈100 channels with 400 receivers and ≈4.9 Tb/s of raw ADC data.",
    "At 10 Mpts/s (million points per second), with each channel spending 12.7 µs on a point, that means ≈127 channels with 507 receivers and ≈4.9 Tb/s of raw ADC data.",
    "N_ch = 10^7 × 12.67 µs = 127 (507 receivers); raw data counts the useful windows and is unchanged.")

add(f"{D1}; {D5}",
    "Parity would need three things together: a coherent receiver chip with ≥150 channels of four receivers each, at ≈2–3 mW per receiver, a CW light source with ≥30% wall-plug efficiency at 105 °C, and ≈0.15 µJ of optical energy per point.",
    "Parity, defined as ≥15 Mpts/s in ≤15 W at 200 m on a 10% target (§C7b subsection 5), would need three things together: a coherent receiver chip with 115–190 channels of four receivers each, at ≈2–3 mW per receiver, a CW light source with ≥30% wall-plug efficiency at 105 °C, and ≈0.15 µJ of optical energy per point. Even then a sensor whose laser stays on through the round trips draws ≈14 W at 15 Mpts/s, about 1.8× the electrical energy per point of the 2026 SPAD ToF model, which needs 9.2 W (§C7a subsection 5).",
    "With the dwell E_pt/P_ch + 2τ, §C7b subsection 5 gives 115 (30 mW) to 190 (15 mW) channels at parity; ungated parity is 0.733 µJ per point, 14.0 W, 1.8× ToF's 0.415 µJ.")

# ---------------------------------------------------------------- C7
add(f"{D1}",
    r"- Each point needs a dwell $T_{\rm dwell}\approx T_{\rm up}+T_{\rm down}$ (several µs to tens of µs), the durations of the up-chirp and the down-chirp that separate range from Doppler.",
    r"- Each point needs a dwell $T_{\rm dwell}=T_{\rm int}+2\tau$ (several µs to tens of µs; §C7b, Eq. (107)). Here $T_{\rm int}$ is the useful integration time of an up-chirp and a down-chirp, which together separate range from Doppler, and $\tau=2R/c$ is the round trip that each of the two ramps loses before its echo arrives.",
    "One report-wide dwell definition (Eq. (107)).")

add(f"{D1}",
    r"A 10 µs dwell is a 5 µs up-chirp plus a 5 µs down-chirp, whose beat at 300 m is 400 MHz rather than the 200 MHz of the 10 µs example above. At that dwell, $N_{\rm ch}=\dot N\,T_{\rm dwell}=2\times10^{6}\ {\rm s^{-1}}\times10\times10^{-6}\ {\rm s}=20$ channels, and 40 for 4 Mpts/s.",
    r"The §C7a model integrates a 5 µs up-chirp plus a 5 µs down-chirp, whose beat at 300 m is 400 MHz rather than the 200 MHz of the 10 µs example above. At its 200 m design range the two round trips add $2\tau=2\times2\times200\ {\rm m}/(3\times10^{8}\ {\rm m\,s^{-1}})=2.67$ µs, so $T_{\rm dwell}=10+2.67=12.67$ µs. At that dwell, $N_{\rm ch}=\dot N\,T_{\rm dwell}=2\times10^{6}\ {\rm s^{-1}}\times12.67\times10^{-6}\ {\rm s}=25$ channels, and 51 for 4 Mpts/s.",
    "Channel counts at the 12.67 µs dwell: 25.3 and 50.7.")

add(f"{D1}",
    r"- Shorter chirps reduce the channel count but raise the beat frequency, $f_b\propto1/T$ by Eq. (85), and with it the ADC rate.",
    r"- Shorter chirps reduce the channel count, though never below the round-trip share $2\tau\dot N$, but raise the beat frequency, $f_b\propto1/T$ by Eq. (85), and with it the ADC rate.",
    "The round trips set a floor that shorter chirps cannot remove (§C7b Eq. (121)).")

# ---------------------------------------------------------------- C7a short answer and figure
add(f"{MODEL}; {D1}",
    r"The model below gives about **8×** more electrical energy per point than 940 nm SPAD ToF in 2026 ($4.25/0.536\approx7.9$). This narrows to about **4×** in an optimistic 2032 projection ($1.48/0.368\approx4.0$; totals from the subsection 3 table). Both receivers are held to the same detection rule (§C0 subsection 10.3). With the lower FMCW efficiencies measured so far (subsection 2(a) below), the 2026 gap is ≈10–13× for a discrete fibre chain and ≈21× for an integrated array.",
    r"The model below gives about **12×** more electrical energy per point than 940 nm SPAD ToF in 2026 ($4.90/0.415\approx11.8$), counting the light the FMCW laser emits for its whole dwell on a point, round trips included. This narrows to about **6×** in an optimistic 2032 projection ($1.74/0.280\approx6.2$; totals from the subsection 3 table). Both receivers are held to the same detection rule (§C0 subsection 10.3). With the lower FMCW efficiencies measured so far (subsection 2(a) below), the 2026 gap is ≈15–19× for a discrete fibre chain and ≈33× for an integrated array.",
    "Model ratios 11.8 (2026) and 6.2 (2032); measured-efficiency totals 6.15, 8.06 and 13.6 µJ against 0.415 µJ.")

add(f"{MODEL}; {D1}",
    "- *(b)* Electrical energy per point in the central case, for ToF and FMCW in 2026 and 2032, split into the emitted optical energy, the loss in the laser, semiconductor optical amplifier (SOA) and driver, and the receiver electronics.",
    r"- *(b)* Electrical energy per point in the central case, for ToF and FMCW in 2026 and 2032, split into the emitted optical energy, the loss in the laser, semiconductor optical amplifier (SOA) and driver, and the receiver electronics. The totals are 0.42, 0.28, 4.90 and 1.74 µJ. FMCW's emitted energy includes the light its transmitter sends while it stays on through the round trips (an ungated transmitter), $T_{\rm dwell}/T_{\rm int}=12.67/10=1.27$ times its useful energy (subsection 2(d)).",
    "Caption matches the rebuilt panel (b), which plots the emitted energy.")

add(f"{D1}",
    r"- *(c)* Parallel coherent channels (transmit beams) needed ($\dot N\times T_{\rm dwell}$, point rate times dwell per point) and the raw ADC data they produce at 10 bits per sample, counting the four receivers of each channel.",
    r"- *(c)* Parallel coherent channels (transmit beams) needed ($\dot N\times T_{\rm dwell}$, point rate times dwell per point) for 4, 10 and 20 µs of integration plus the two round trips at 200 m, $2\tau=2.67$ µs, i.e. dwells of 6.7, 12.7 and 22.7 µs. The note gives the raw ADC data at 10 bits per sample over the useful windows, counting the four receivers of each channel: at the model's 12.7 µs dwell, 2, 10 and 25 Mpts/s need 25, 127 and 317 channels and produce 0.98, 4.9 and 12 Tb/s (subsection 2(d)).",
    "Caption matches the rebuilt panel (c): three dwell curves and the 12.7 µs note.")

# ---------------------------------------------------------------- C7a subsection 2 intro and (a)
add(f"{D1}",
    "raise the optical energy, continuous-wave (CW) amplification limits wall-plug efficiency (electrical-to-optical conversion efficiency), and dense digitization",
    "raise the optical energy, a continuous-wave (CW) laser that stays on through the round trips emits 27% more light than it uses ($T_{\\rm dwell}/T_{\\rm int}=12.67/10$), CW amplification limits wall-plug efficiency (electrical-to-optical conversion efficiency), and dense digitization",
    "Names the ungated emission among the FMCW costs.")

add(f"{MODEL}; {D2}; {D3}",
    "**(a) Optical energy per point: ≈93 nJ for ToF against ≈300 nJ (0.30 µJ) for FMCW.**",
    "**(a) Optical energy per point: ≈72 nJ for ToF against ≈300 nJ (0.30 µJ) for FMCW.**",
    "ToF central E_pt = 71.7 nJ.")

add(f"{D2}",
    r"""In the model's central "bright sun" case, half the background of a fully sunlit scene of reflectance 0.9 (the model's high case; §C0 subsection 10.3), each of the nine SPADs of a macro-pixel counts $r=3.66\times10^{8}/9=4.06\times10^{7}$ s⁻¹, so $r\tau_d=0.244$ and each SPAD is dead a fraction $1-e^{-0.244}=21.6\%$ of the time (Eq. (82)). A SPAD that is dead when the echo arrives misses it, so the live fraction 0.784 multiplies the signal efficiency as well as the background.""",
    r"""Each macro-pixel sees a 0.05° × 0.05° field, one cell of the IMX479 grid (2,400 × 520 cells over 120° × 26°), i.e. a solid angle $\Omega_{\rm pix}=(0.05^\circ\times\pi/180)^2=(8.727\times10^{-4})^2=7.615\times10^{-7}$ sr. In the model's central "bright sun" case, half the background of a fully sunlit scene of reflectance 0.9 (the model's high case; §C0 subsection 10.3), the macro-pixel counts $r_{\rm bg}=1.83\times10^{8}$ s⁻¹ (subsection 2(c)), so each of its nine SPADs counts $r=1.83\times10^{8}/9=2.03\times10^{7}$ s⁻¹, $r\tau_d=0.122$, and each SPAD is dead a fraction $1-e^{-0.122}=11.5\%$ of the time (Eq. (82)). A SPAD that is dead when the echo arrives misses it, so the live fraction 0.885 multiplies the signal efficiency as well as the background. In the fully sunlit high case the rate doubles, $r\tau_d=0.244$, and the dead fraction is $1-e^{-0.244}=21.6\%$ (live fraction 0.784).""",
    "States the pixel field and recomputes the dead and live fractions (0.122, 11.5%, 0.885; high case 0.244, 21.6%).")

add(f"{MODEL}; {D3}",
    "- $E_{\\rm pt}$ is the optical energy the transmitter must emit per point (J);",
    "- $E_{\\rm pt}$ is the useful optical energy per point (J), the light whose echo the receiver integrates: all of a ToF point's light, whereas an ungated FMCW laser emits $T_{\\rm dwell}/T_{\\rm int}$ times more, because it stays on through the round trips (subsection 2(d));",
    "With the ungated dwell the FMCW transmitter emits more than E_pt; the definition says which energy Eq. (93) gives.")

old = span("- **ToF:** $A_{\\rm eff}=A_{\\rm rx}$ is the whole 25 mm receive aperture (491 mm²)", "(35 counts, live fraction 0.614, $\\eta=0.114$): 167 nJ.")
add(f"{MODEL}; {D2}; {D3}", old,
    r"- **ToF:** $A_{\rm eff}=A_{\rm rx}$ is the whole 25 mm receive aperture (491 mm²), and the pixel sums hundreds of speckle modes. An ideal counter needs 15.0 counts in the model's bright sun (14.98; §C0 subsection 10.3); the model applies a ×1.45 implementation margin to it [E], $n_{\rm req}=1.448\times14.98=21.7$ counts, and its low and high cases apply ×1.16 and ×2.03 (17.4 and 30.4 counts). At 940 nm, 37% PDE (photon detection efficiency of the SPAD) and the bright-sun live fraction of 0.885 the result is **≈72 nJ** (51–113). With $n_{\rm req}=21.7$ (central), $E_{\rm ph}=2.11\times10^{-19}$ J, $\pi R^2=\pi\times200^2=1.26\times10^{5}$ m², $\rho=0.1$ and $\eta=0.5\times0.37\times0.885=0.164$ (optics transmission × PDE × live fraction): $E_{\rm pt}=21.7\times2.11\times10^{-19}\times1.26\times10^{5}/(0.1\times4.91\times10^{-4}\times0.164)=5.77\times10^{-13}/(8.05\times10^{-6})\approx7.2\times10^{-8}$ J. The low case is night (17.4 counts, no dead time, $\eta=0.185$): 51 nJ. The high case is the fully sunlit scene (30.4 counts, live fraction 0.784, $\eta=0.145$): 113 nJ.",
    "n_req 17.4/21.7/30.4 (×1.16/×1.45/×2.03 over the ideal 15.0); η 0.164; E_pt 51/72/113 nJ, with the substitution.")

add(f"{D3}",
    "a ×1.36 implementation margin, close to the ×1.45 that takes ToF from 17.3 to 25 counts.",
    "a ×1.36 implementation margin, close to the ×1.45 that takes ToF from 15.0 to 21.7 counts.",
    "ToF ideal and model requirements at b = 1.62.")

old = span("With those values FMCW needs 1.5–2.2× (discrete fibre chain) or about 4.4× (integrated array) the optical energy per point quoted here:", "or to ≈11 µJ (≈21×).")
add(f"{MODEL}; {D1}", old,
    r"With those values FMCW needs $0.25/0.168=1.5$ to $0.25/0.112=2.2$ times (discrete fibre chain) or $0.25/0.057=4.4$ times (integrated array) the optical energy per point quoted here: 0.45–0.68 µJ or 1.3 µJ instead of 0.30 µJ. The laser's electrical energy (2.56 µJ, subsection 3) scales in the same way while the receiver electronics (2.34 µJ) do not, so the total per point rises from 4.90 µJ to $2.563\times1.488+2.337=6.15$ µJ and $2.563\times2.232+2.337=8.06$ µJ (15–19× ToF's 0.415 µJ), or to $2.563\times4.386+2.337=13.6$ µJ (≈33×).",
    "Sensitivity recomputed on the ungated model totals, with the substitution.")

old = span("FMCW therefore needs ≈3.2× more optical energy per point than ToF (0.30 µJ against 93 nJ).", "- efficiency (0.58×), ToF's 0.145, which includes the SPADs' dead time in bright sun, against FMCW's 0.25.")
new = rep(old, [
    ("FMCW therefore needs ≈3.2× more optical energy per point than ToF (0.30 µJ against 93 nJ). The ≈3.2× ratio splits into four factors:",
     r"FMCW therefore needs ≈4.2× more useful optical energy per point than ToF ($0.303\ \mu{\rm J}/72\ {\rm nJ}=4.2$), and its ungated transmitter emits ≈5.3× more ($0.384\ \mu{\rm J}/72\ {\rm nJ}=5.3$), because it also emits during the round trips (subsection 2(d)). The ≈4.2× ratio is the product of four factors, $1.93\times5.53\times0.607\times0.655=4.2$:"),
    ("- detection statistics (4.8×), 120 required photoelectrons against 25 counts:", "- detection statistics (5.5×), 120 required photoelectrons against 21.7 counts:"),
    ("- efficiency (0.58×), ToF's 0.145,", "- efficiency (0.66×), ToF's 0.164,"),
])
add(f"{MODEL}; {D3}", old, new, "Useful ratio 0.303/0.072 = 4.2 and emitted ratio 0.384/0.072 = 5.3; detection 120/21.7 = 5.53 and efficiency 0.164/0.25 = 0.655.")

# ---------------------------------------------------------------- C7a (b)
add(f"{D1}",
    "so the laser's electrical energy per point is $E_{\\rm pt}/\\eta_{\\rm wp}$ and everything not emitted becomes heat.",
    "so the laser's electrical energy per point is the light it emits per point divided by $\\eta_{\\rm wp}$: $E_{\\rm pt}/\\eta_{\\rm wp}$ for a pulsed ToF laser and $E_{\\rm pt}T_{\\rm dwell}/(T_{\\rm int}\\eta_{\\rm wp})$ for the ungated FMCW laser (subsection 2(d)). Everything not emitted becomes heat.",
    "The FMCW laser is charged for the light it emits through the whole dwell.")

add(f"{D1}",
    "Eye safety allows ≈9 W of scanned light over a 120° × 25° field at 1,550 nm, which FMCW's 3.0–7.6 W at 10–25 Mpts/s and 200 m fits within if its transmitter is gated during the round trips; ungated, it emits 3.5–9.6 W and can reach the allowance at 25 Mpts/s (§C7b subsection 2(i)).",
    r"Eye safety allows ≈9.1 W of scanned light over a 120° × 25° field at 1,550 nm (§C7b subsection 2(i)). FMCW's useful light at 200 m, 3.0 W at 10 Mpts/s and 7.6 W at 25 Mpts/s, fits within it if the transmitter is gated during the round trips. The model's transmitter is ungated and emits $T_{\rm dwell}/T_{\rm int}=12.67/10=1.27$ times as much, 3.8 W and 9.6 W, so at 25 Mpts/s it exceeds the allowance unless it is gated.",
    "The central model is ungated; at 25 Mpts/s its 9.6 W exceeds the 9.1 W allowance, a changed conclusion stated plainly.")

add(f"{D1}; {D5}",
    "so channels carrying ≈100 mW need silicon-nitride (SiN) or III-V (compound-semiconductor) paths.",
    "so the model's 30 mW channels (subsection 2(e)), and brighter ones, need silicon-nitride (SiN) or III-V (compound-semiconductor) paths.",
    "Ties the waveguide limit to the model's channel power instead of the dropped 100 mW condition.")

old = span("- At 10 Mpts/s that means ≈3 W optical and ≈17 W of heat in the laser/SOA stage alone;", "where $5.67=1/0.15-1$.")
add(f"{MODEL}; {D1}", old,
    r"- At 10 Mpts/s that means ≈3.0 W of useful light, ≈3.8 W emitted and ≈22 W of heat in the laser/SOA stage alone; at 25 Mpts/s, ≈7.6 W useful, ≈9.6 W emitted and ≈54 W of heat. The useful optical power is the point rate $\dot N$ times the optical energy per point, $P_{\rm opt}=\dot N E_{\rm pt}=10^{7}\ {\rm s^{-1}}\times0.303\ \mu{\rm J}=3.03$ W. The ungated laser emits for the whole dwell, $P_{\rm opt}T_{\rm dwell}/T_{\rm int}=3.03\times12.67/10=3.84$ W (subsection 2(d)). The heat is the electrical input minus the light out, $3.84\times(1/\eta_{\rm wp}-1)=3.84\times(1/0.15-1)=21.8$ W; at 25 Mpts/s, $7.59\times1.267\times5.67=54.5$ W, where $5.67=1/0.15-1$.",
    "Emitted 3.84 / 9.61 W and heat 21.8 / 54.5 W at 10 / 25 Mpts/s.")

# ---------------------------------------------------------------- C7a (c)
add(f"{D1}",
    "An FMCW receiver must sample its beat signal densely over the whole chirp and Fourier-transform it,",
    "An FMCW receiver must sample its beat signal densely over the useful window of every chirp ramp and Fourier-transform it,",
    "Only the useful windows are digitized.")

add(f"{D1}; 08_C7b report #1 (which window is digitized)",
    "The beat frequency is $f_b=2BR/(cT)$ (Eq. (85)), with $B$ the chirp bandwidth, $R$ the range and $T$ the duration of one chirp.",
    r"The beat frequency is $f_b=2BR/(cT)$ (Eq. (85)), with $R$ the range, $T$ the useful window of one chirp ramp and $B$ the bandwidth swept in it. The useful window is the part of the ramp after the round trip $\tau=2R/c$, once the echo beats with the LO; the ramp itself lasts $T+\tau$, with $\tau$ taken at the 200 m design range (§C7b, Eq. (106)), so the laser sweeps $1\ {\rm GHz}\times(5+1.33)/5=1.27$ GHz per ramp (§C7b, Eq. (110)). An echo from beyond 200 m arrives later and beats for less of the window, 4.33 µs instead of 5 µs at 300 m, which the model ignores because its design target sits at 200 m.",
    "Defines T as the useful window, consistent with §C7b Eqs. (106)–(109).")

add(f"07 report §3 flag (Eq. (94) chirp length); {D1}",
    "Over an up-plus-down chirp of total duration $2T$, the number of ADC samples per point is $N_{\\rm samp}=f_s\\times2T$, which gives",
    "Only the two useful windows, $T_{\\rm int}=2T$ in all, are digitized, so the number of ADC samples per point is $N_{\\rm samp}=f_s\\times2T$, which gives",
    "Eq. (94) counts the useful windows, as the model does.")

add("08_C7b consistency flag (Eq. (109) vs Eq. (94))",
    r"The first term follows because $f_bT=2BR_{\max}/c=R_{\max}/\Delta R$ at maximum range.",
    r"The first term follows because $f_bT=2BR_{\max}/c=R_{\max}/\Delta R$ at maximum range. Eq. (94) is Eq. (109) of §C7b with $R=R_{\max}$ and $T_u=T$.",
    "With T the useful window the two equations are the same; cross-reference added as the flag asked.")

add(f"{D1}",
    "- For 300 m, 15 cm resolution (2,000 range bins) and 5 µs chirps:",
    "- For 300 m, 15 cm resolution (2,000 range bins) and 5 µs useful windows:",
    "Same quantity as T above.")

old = span("where $E_{\\rm rx}$ is the receiver electronics energy per point, $N_L$ the number of receivers (looks) per point,", "+20\\ {\\rm mW}\\times10\\ \\mu{\\rm s})=3.8$ µJ.")
add(f"{D1}; 07 report §3 flag (round-trip dead time); 08_C7b report #1 (§C7a part)", old,
    r"where $E_{\rm rx}$ is the receiver electronics energy per point, $N_L$ the number of receivers (looks) per point, $P_{\rm an}$ the analog power per receiver and $T_{\rm dwell}$ the dwell per point. The dwell is the two useful windows plus the two round trips, $T_{\rm dwell}=2T+2\tau=10+2.67=12.67$ µs at the 200 m design range (§C7b, Eq. (107)). The ADC samples only the useful windows, but the analog front end stays on for the whole dwell. This gives **≈2.3 µJ per point** (1.3–4.0): $E_{\rm rx}=4\times(12{,}300\times37.3\ {\rm pJ}+10\ {\rm mW}\times12.67\ \mu{\rm s})=4\times(0.459+0.127)=2.34$ µJ. The low and high cases are $4\times(12{,}300\times22\ {\rm pJ}+5\ {\rm mW}\times12.67\ \mu{\rm s})=1.3$ µJ and $4\times(12{,}300\times61\ {\rm pJ}+20\ {\rm mW}\times12.67\ \mu{\rm s})=4.0$ µJ.",
    "Analog power runs for the 12.67 µs dwell: E_rx 1.32 / 2.34 / 3.99 µJ.")

old = span("  - *Result:* **≈70 nJ per point** (20–126)", "in the fully sunlit scene (live fraction 0.614).")
new = rep(old, [
    ("**≈70 nJ per point** (20–126)", "**≈57 nJ per point** (20–102)"),
    (r"=3.66\times10^{8}\ {\rm s^{-1}}\times20.8\ \mu{\rm s}\times0.784+25\approx5{,}990$ events per point in bright sun.",
     r"=1.83\times10^{8}\ {\rm s^{-1}}\times20.8\ \mu{\rm s}\times0.885+21.7\approx3{,}369+22\approx3{,}390$ events per point in bright sun."),
    (r"    - the background count rate $r_{\rm bg}=3.66\times10^{8}$ s⁻¹ per macro-pixel, half the fully sunlit 940 nm case of §C6(d) (Eq. (81)) evaluated at the model's PDE of 0.37, i.e. a sunlit scene",
     r"    - the background count rate $r_{\rm bg}=1.83\times10^{8}$ s⁻¹ per 0.05° × 0.05° macro-pixel, half the fully sunlit 940 nm, 10 nm-filter case of §C6(d) (Eq. (81)) evaluated at the model's PDE of 0.37. §C6(d) gives $2.965\times10^{8}$ s⁻¹ at PDE 0.3, so $r_{\rm bg}=0.5\times2.965\times10^{8}\times0.37/0.3=1.83\times10^{8}$ s⁻¹, i.e. a sunlit scene"),
    (r"    - the live fraction 0.784 that the paralyzable form of Eq. (82) gives at the per-SPAD rate $r=r_{\rm bg}/9=4.06\times10^{7}$ s⁻¹ (nine SPADs per 3×3 macro-pixel; subsection 2(a)): $e^{-r\tau_d}=e^{-0.244}=0.784$, so each SPAD is blind 21.6% of the time;",
     r"    - the live fraction 0.885 that the paralyzable form of Eq. (82) gives at the per-SPAD rate $r=r_{\rm bg}/9=2.03\times10^{7}$ s⁻¹ (nine SPADs per 3×3 macro-pixel; subsection 2(a)): $e^{-r\tau_d}=e^{-0.122}=0.885$, so each SPAD is blind 11.5% of the time;"),
    (r"    - $n_{\rm req}=25$ signal counts.", r"    - $n_{\rm req}=21.7$ signal counts (subsection 2(a))."),
    (r"=3.66\times10^{8}\ {\rm s^{-1}}\times1\ {\rm ns}\times10\times0.784=2.87$", r"=1.83\times10^{8}\ {\rm s^{-1}}\times1\ {\rm ns}\times10\times0.885=1.62$"),
    (r"$E=40\ {\rm nJ}+5{,}990\times5\ {\rm pJ}=70$ nJ.", r"$E=40\ {\rm nJ}+3{,}390\times5\ {\rm pJ}=57$ nJ."),
    ("the 70 nJ total sits inside", "the 57 nJ total sits inside"),
    (r"$60\ {\rm nJ}+(7.31\times10^{8}\times20.8\ \mu{\rm s}\times0.614+35)\times7\ {\rm pJ}=126$ nJ in the fully sunlit scene (live fraction 0.614).",
     r"$60\ {\rm nJ}+(3.66\times10^{8}\times20.8\ \mu{\rm s}\times0.784+30.4)\times7\ {\rm pJ}=102$ nJ in the fully sunlit scene (live fraction 0.784)."),
])
add(f"{MODEL}; {D2}; {D3}", old, new, "Background 1.83e8 per 0.05° pixel, live 0.885, 3,390 events, b = 1.62, 57 nJ (20–102).")

# ---------------------------------------------------------------- C7a (d)
old = span("- The 10 µs dwell is the 5 µs up-chirp plus the 5 µs down-chirp of (c).", "rather than through more samples.")
add(f"{D1}; 07 report §3 flag (round-trip dead time); 08_C7b report #1 (4 µs case)", old,
    r"- The dwell is the 10 µs of useful integration of (c), the 5 µs up-chirp plus the 5 µs down-chirp, plus the round trip that each of the two ramps loses, $2\tau=2.67$ µs at 200 m: $T_{\rm dwell}=12.67$ µs (Eq. (96); §C7b, Eq. (107)). At that dwell, 2 Mpts/s needs $N_{\rm ch}=2\times10^{6}\ {\rm s^{-1}}\times12.67\times10^{-6}\ {\rm s}=25$ channels, 10 Mpts/s needs **127**, and 25 Mpts/s needs 317. With four receivers per channel these are 101, 507 and 1,267 receivers. Integrating for 4 µs instead (2 µs useful windows) shortens the dwell only to $4+2.67=6.67$ µs, a factor of 1.9 rather than 2.5, because the round trips stay: 13, 67 and 167 channels (53, 267 and 667 receivers). Meanwhile $f_s$ and ADC energy rise: 2 µs chirps give $f_b=1.0$ GHz and $f_s=2.5\times(1{,}000+90)\ {\rm MHz}\approx2.7$ GS/s. The samples per point stay near $5R_{\max}/\Delta R$ ($2.7\times10^{9}\times4\times10^{-6}\approx10{,}900$), so the energy per point rises through the poorer figure of merit of faster converters rather than through more samples." "\n"
    r"- The central design is ungated: its laser stays on through the round trips, so it emits $E_{\rm pt}T_{\rm dwell}/T_{\rm int}=0.303\ \mu{\rm J}\times12.67/10=0.38$ µJ per point (0.19–1.12 µJ across the cases), and the laser's electrical energy is counted on that emitted light (subsections 2(b) and 3). A transmitter switched off during the last $\tau$ of each ramp, whose echo would land in the next ramp's discarded window, would save that extra light, $2\tau/T_{\rm dwell}=2.67/12.67=21\%$ of what the ungated laser emits (§C7b subsection 2(i)).",
    "Channels 25/127/317 (receivers 101/507/1,267); 4 µs integration gives 6.67 µs and 13/67/167; emitted energy 0.38 µJ.")

old = span("- Raw ADC output at 10 bits per sample is **0.98, 4.9 and 12 Tb/s** respectively:", "=4.9\\times10^{12}$ b/s at 10 Mpts/s.")
add(f"{D1}", old,
    r"- Raw ADC output at 10 bits per sample is **0.98, 4.9 and 12 Tb/s** respectively: $N_L\dot N N_{\rm samp}\times10$ bits with $N_L=4$ receivers per channel, e.g. $4\times10^{7}\ {\rm s^{-1}}\times12{,}300\times10=4.9\times10^{12}$ b/s at 10 Mpts/s. This counts the useful windows only, as the ADC energy of (c) does; converters left running through the round trips would stream $T_{\rm dwell}/T_{\rm int}=1.27$ times more, 6.2 Tb/s.",
    "Raw data counts the useful windows (decision 1), so it is written per point rather than per channel.")

old = span("A 10 Mpts/s sensor would need roughly **120 such devices** [E].", "is far too slow per receiver.")
new = rep(old, [
    ("roughly **120 such devices** [E]", "roughly **120–130 such devices** [E]"),
    ("Counting one ADC per receiver gives $400/4=100$, but each 1 GS/s converter is then below the 1.23 GS/s a receiver needs, and the 8 × 500 MS/s mode (50 devices)",
     "Counting one ADC per receiver gives $507/4\\approx127$, but each 1 GS/s converter is then below the 1.23 GS/s a receiver needs during its useful windows, and the 8 × 500 MS/s mode (≈63 devices)"),
])
add(f"{D1}", old, new, "507 receivers at the 12.67 µs dwell: 127 four-ADC devices, or 63 in the 8 × 500 MS/s mode.")

add(f"{D1}",
    r"- **Physics bounds the minimum dwell:** one round trip, $\tau=2R/c=2\times250\ {\rm m}/(3\times10^{8}\ {\rm m\,s^{-1}})=1.67$ µs at 250 m.",
    r"- **Physics bounds the minimum dwell:** each of the two ramps loses one round trip, $\tau=2R/c=2\times250\ {\rm m}/(3\times10^{8}\ {\rm m\,s^{-1}})=1.67$ µs at 250 m, so even unlimited light leaves a dwell of at least $2\tau=3.33$ µs (2.67 µs at 200 m; §C7b subsection 2(a)).",
    "Minimum dwell under the report-wide definition is 2τ.")

add(f"{D1}",
    "For any wider beam the minimum dwell already exceeds the maximum, so no chirp length works without digital compensation",
    "For any wider beam even the shortest ramp, one round trip long, outlasts the crossing time, so no chirp length works without digital compensation",
    "The scan limit applies per ramp (Eq. (116)); the minimum dwell is two ramps.")

# ---------------------------------------------------------------- C7a (e)
old = span("plus its own CW optical power: **≈30 mW per channel** in the central model at 200 m", "Lines beyond the channel count come from stepping the beam, which costs dwell.")
add("round2 task: C7a(e) per-channel light; 08_C7b consistency flag (range scaling of coherent energy); " + D1, old,
    r"plus its own CW optical power. Lines beyond the channel count come from stepping the beam, which costs dwell." "\n"
    r"  - *Light per channel:* **≈30 mW** in the central model at 200 m, the useful energy over the integration time, $P_{\rm ch}=E_{\rm pt}/T_{\rm int}=0.303\ \mu{\rm J}/10\ \mu{\rm s}=30$ mW. The channel emits it for the whole 12.67 µs dwell, 0.38 µJ per point (subsection 2(d)). The high-energy case needs $0.885\ \mu{\rm J}/10\ \mu{\rm s}=88$ mW." "\n"
    r"  - *With range:* the power grows with the energy, $E_{\rm pt}\propto R^2/A_{\rm mode}$ (Eq. (93)). For the model's fixed 20 mm aperture, $A_{\rm mode}$ is 63.7 mm² at 200 m, 74.5 mm² at 250 m (subsection 2(a)) and ≈82 mm² at 300 m, where $w=9\ {\rm mm}\times\sqrt{1+(300/164)^2}\approx18.8$ mm and $A_{\rm mode}=0.84\times(1.55\times10^{-6})^2\times300^2/(2\pi\times0.0188^2)\approx82$ mm² (§C0 Eq. (33)). A channel therefore needs $30.3\times(250/200)^2\times63.7/74.5=40$ mW at 250 m and $30.3\times(300/200)^2\times63.7/82=53$ mW at 300 m. An aperture re-optimized at each range holds the growth to $\propto R$ (§C7b subsection 1(f)): $30.3\times250/200=38$ mW and $30.3\times300/200=45$ mW.",
    "P_ch = E_pt/T_int = 30 mW over the whole dwell; range scaling R^2/A_mode for the fixed 20 mm aperture (40 and 53 mW), and R for a re-optimized one (38 and 45 mW).")

old = span("- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m (12.5 Mpts/s)", "\\times0.536\\ \\mu{\\rm J}\\approx9.7$ W.")
add(f"{MODEL}; {D1}", old,
    r"- **Worked example:** a 520-line, 10 Hz, 2,400-column FMCW image at 200 m (12.5 Mpts/s) implies ≈158 channels (≈630 receivers) at the 12.67 µs dwell, ≈3.8 W of useful light (4.8 W emitted), ≈27 W of laser heat and ≈29 W of receiver electronics under the central 2026 assumptions. That is about **64 W** in total, against ≈8 W for a 520-line ToF unit in the same model, and each FMCW sample still covers only ≈2% of its cell (§C10.3b, Result 2). The arithmetic: $\dot N=520\times2{,}400\times10\ {\rm Hz}=1.25\times10^{7}$ pts/s; $N_{\rm ch}=1.25\times10^{7}\times12.67\ \mu{\rm s}=158$; useful optical power $1.25\times10^{7}\times0.303\ \mu{\rm J}=3.8$ W, emitted $1.25\times10^{7}\times0.384\ \mu{\rm J}=4.8$ W; laser heat, the laser's electrical energy per point minus the light it emits, $1.25\times10^{7}\times(2.56-0.38)\ \mu{\rm J}=27$ W; receivers $1.25\times10^{7}\times2.34\ \mu{\rm J}=29.2$ W. With the 3 W overhead, the total is $3\ {\rm W}+1.25\times10^{7}\times4.90\ \mu{\rm J}\approx64$ W. The ToF unit is $3\ {\rm W}+1.25\times10^{7}\times0.415\ \mu{\rm J}\approx8.2$ W.",
    "Worked example on the ungated model: 158 channels, 64 W against 8.2 W.")

# ---------------------------------------------------------------- C7a subsection 3
add(f"{MODEL}",
    "FMCW needs about 8× ToF's electrical energy per point in 2026 and about 4× in the optimistic 2032 case, but measures velocity on every point.",
    "FMCW needs about 12× ToF's electrical energy per point in 2026 and about 6× in the optimistic 2032 case, but measures velocity on every point.",
    "Ratios 11.8 and 6.2.")

old = span("| Counts or photoelectrons needed per point (ideal; model) | 17.3; 25 |", "| Sensor power at 25 Mpts/s | 16 W | 109 W | 12 W | 40 W |")
add(f"{MODEL}; {D1}; {D3}", old,
    "| Counts or photoelectrons needed per point (ideal; model) | 15.0; 21.7 | 88.5; 120 (four looks) | 15.9; 22.0 | 88.5; 120 |\n"
    "| Useful optical energy per point | 0.072 µJ | 0.30 µJ | 0.061 µJ | 0.19 µJ |\n"
    "| Emitted optical energy per point | 0.072 µJ (pulsed) | 0.38 µJ (ungated, 12.67 µs dwell) | 0.061 µJ | 0.24 µJ |\n"
    "| Laser/SOA electrical energy | 0.36 µJ | 2.56 µJ | 0.25 µJ | 1.09 µJ |\n"
    "| Receiver electronics | 0.057 µJ | 2.34 µJ (four receivers) | 0.034 µJ | 0.65 µJ |\n"
    "| **Total per point** | **0.415 µJ** | **4.90 µJ** | **0.280 µJ** | **1.74 µJ** |\n"
    "| Sensor power at 10 Mpts/s (incl. 3 W overhead) | 7.2 W | 52.0 W | 5.8 W | 20.4 W |\n"
    "| Sensor power at 25 Mpts/s | 13.4 W | 125.5 W | 10.0 W | 46.5 W |",
    "Central values of the installed model, with an emitted-energy row for the ungated dwell.")

old = span("- All entries are the central cases of the companion script. **Optical energy** uses", "1.45× (ToF 2026) and 1.36× (FMCW) higher.")
add(f"{MODEL}; {D1}; {D3}", old,
    r"- All entries are the central cases of the companion script. **Useful optical energy** uses $E_{\rm pt}=n_{\rm req}E_{\rm ph}\pi R^2/(\rho A_{\rm eff}\eta)$, Eq. (93) of subsection 2(a): $n_{\rm req}$ required counts or photoelectrons, $E_{\rm ph}$ photon energy, $R$ range, $\rho$ reflectance, $A_{\rm eff}$ effective collecting area and $\eta$ receive efficiency. ToF 2026 is 72 nJ and FMCW 2026 0.30 µJ (worked in subsection 2(a)). ToF 2032 raises PDE from 0.37 to 0.45, which also raises the sunlight counted, the dead fraction (13.8%, live fraction 0.862) and the background to 1.92 counts per bin. For that background the ideal requirement of §C0 subsection 10.3 is 15.9 counts (threshold 13 counts, whose Poisson tail is $1.3\times10^{-7}$ per bin against the $5\times10^{-7}$ allowed), and the model's is 22.0 (margin ×1.39). That gives $71.7\times(22.0/21.7)\times(0.37\times0.885)/(0.45\times0.862)=61$ nJ. FMCW 2032 keeps the four looks and the 120 photoelectrons, since detection statistics do not improve with technology, and raises $\eta$ to 0.40, giving $0.30\times0.25/0.40=0.19$ µJ. The counts row gives the ideal requirement of §C0 subsection 10.3 and the model's value, 1.45× (ToF 2026), 1.39× (ToF 2032) and 1.36× (FMCW) higher." "\n"
    r"- **Emitted optical energy** equals the useful energy for the pulsed ToF laser, which is dark between shots. The ungated FMCW laser emits the useful energy times $T_{\rm dwell}/T_{\rm int}=12.67/10$: $0.303\times1.267=0.38$ µJ in 2026 and $0.190\times1.267=0.24$ µJ in 2032.",
    "2032 ToF on the new background (13.8% dead, b = 1.92, n_req 22.0); emitted-energy row explained.")

old = span("- **Laser/SOA electrical energy** is $E_{\\rm pt}/\\eta_{\\rm wp}$,", "$0.19\\ \\mu{\\rm J}/0.22=0.86$ µJ.")
add(f"{MODEL}; {D1}", old,
    r"- **Laser/SOA electrical energy** is the emitted optical energy divided by $\eta_{\rm wp}$, the wall-plug efficiency, using central wall-plug efficiencies of 20% (ToF 2026), 15% (FMCW 2026), 25% (ToF 2032) and 22% (FMCW 2032): $71.7\ {\rm nJ}/0.20=0.36$ µJ, $0.384\ \mu{\rm J}/0.15=2.56$ µJ, $61.5\ {\rm nJ}/0.25=0.25$ µJ and $0.240\ \mu{\rm J}/0.22=1.09$ µJ.",
    "The laser is charged for the light it emits, round trips included.")

old = span("- **Receiver electronics:** ToF is a fixed 40 nJ (2026) or 20 nJ (2032) plus ≈5,990 or ≈6,900 events", "=4\\times(0.12+0.03)=0.61$ µJ.")
add(f"{MODEL}; {D1}; 08_C7b report #29 (2032 receiver energy)", old,
    r"- **Receiver electronics:** ToF is a fixed 40 nJ (2026) or 20 nJ (2032) plus ≈3,390 or ≈4,010 events at 5 or 3.5 pJ, giving 57 and 34 nJ (subsection 2(c)); the 2032 sensor counts more events because its higher PDE also detects more sunlight (Eq. (81)): $2.224\times10^{8}\ {\rm s^{-1}}\times20.8\ \mu{\rm s}\times0.862+22.0\approx4{,}010$. FMCW is $N_L(N_{\rm samp}e_s+P_{\rm an}T_{\rm dwell})$ (Eq. (96)): $N_L=4$ receivers, each with $N_{\rm samp}$ samples per point times energy per sample $e_s$, plus analog power per receiver $P_{\rm an}$ times the dwell $T_{\rm dwell}=12.67$ µs. That is 2.34 µJ in 2026 (subsection 2(c)). In 2032 the model keeps 8 effective bits (ENOB = 8) at a FOM of 12 fJ/step and 70 DSP operations at 0.1 pJ each, so Eq. (95) gives $e_s=12\ {\rm fJ}\times2^{8}+70\times0.1\ {\rm pJ}=3.07+7=10.07$ pJ, and $4\times(12{,}300\times10.07\ {\rm pJ}+3\ {\rm mW}\times12.67\ \mu{\rm s})=4\times(0.124+0.038)=0.65$ µJ.",
    "ToF 57 / 34 nJ; FMCW 2.34 / 0.65 µJ with the analog power over 12.67 µs (fixes the 0.61/0.62 rounding).")

add(f"{MODEL}",
    "- **Total per point** is the laser row plus the receiver row, e.g. FMCW 2026: $2.02+2.23=4.25$ µJ.",
    "- **Total per point** is the laser row plus the receiver row, e.g. FMCW 2026: $2.56+2.34=4.90$ µJ, and ToF 2026: $0.358+0.057=0.415$ µJ.",
    "Model totals.")

old = span("e.g. FMCW 2026 at 10 Mpts/s: $3+10^{7}\\times4.25\\times10^{-6}=45.5\\approx46$ W,", "\\times0.536\\times10^{-6}=8.4$ W.")
add(f"{MODEL}", old,
    r"e.g. FMCW 2026 at 10 Mpts/s: $3+10^{7}\times4.90\times10^{-6}=52.0$ W, and at 25 Mpts/s $3+2.5\times10^{7}\times4.90\times10^{-6}=125.5$ W; ToF 2026 at 10 Mpts/s: $3+10^{7}\times0.415\times10^{-6}=7.2$ W.",
    "Sensor power on the model totals.")

old = span("The 2032 FMCW column assumes efficiency $\\eta=0.4$ and 22% wall-plug;", "and dense digitization in four receivers per point.")
add(f"{MODEL}; {D1}", old,
    r"The 2032 FMCW column assumes efficiency $\eta=0.4$ and 22% wall-plug; ADCs at 12 fJ/step (still at 8 ENOB), FFTs at 0.1 pJ/op and 3 mW of analog per receiver; and the same four looks, 120 photoelectrons and ungated 12.67 µs dwell as in 2026. These are optimistic but not exotic. The residual ≈6× gap ($1.74/0.280=6.2$) comes from detection statistics and single-mode collection, SOA wall-plug efficiency, the light emitted during the round trips, and dense digitization in four receivers per point.",
    "2032 ratio 6.2; the ungated dwell is part of the 2032 case.")

# ---------------------------------------------------------------- C7a subsections 5 and 6
old = span("### 5. What would have to be true for parity at 10–25 Mpts/s and 200–300 m", "5. Volume: a program in the hundreds of thousands per year to run the cost curve.")
add("07 report #2; 07 report §3 flag (parity conditions); 07 report #16; 08_C7b consistency flag (parity conditions); " + D5, old,
    "### 5. What parity would need: the three conditions of §C7b subsection 5\n\n"
    r"This subsection summarizes the parity arithmetic of §C7b subsection 5. Parity means ≥15 Mpts/s in ≤15 W at 200 m on a 10% target, which leaves 0.8 µJ of electricity per point after the 3 W overhead (Eq. (123)); the 2026 SPAD ToF model meets it with $3+15\times0.415=9.2$ W. The central 2026 FMCW model needs 4.90 µJ per point, i.e. $3+15\times4.90=76.5$ W at 15 Mpts/s. Three conditions must land together; any two of them alone leave a 15 Mpts/s sensor at ≈23.5 W or more (§C7b subsection 5 table)." "\n\n"
    r"1. **A low-power coherent receiver chip**, with the electronics and photonics stacked or monolithic: ≈2–3 mW per receiver including ≈1 GS/s ADCs and FFT, i.e. ≈0.10 µJ of receiver energy per point against the model's 2.34 µJ, for 115–190 channels of four receivers each." "\n"
    r"2. **CW lasers and amplifiers at ≥30% wall-plug efficiency at 105 °C**, twice the model's 15%." "\n"
    r"3. **≈0.15 µJ of optical energy per point** at 200 m, half the model's 0.30 µJ, which needs a receive efficiency $\eta$ near 0.5, or more looks per point, each with its own receiver." "\n\n"
    r"With all three and the model's ungated dwell (10 µs of integration, so 15 mW per channel and 190 channels), a point costs $0.150\times1.267/0.30+0.10=0.73$ µJ, and a 15 Mpts/s sensor draws $3+15\times0.73=14.0$ W: just inside the target, yet still 1.8× the electrical energy per point of the SPAD ToF model ($0.73/0.415$). Brighter channels stay inside 15 W only with a gated transmitter: at 30 mW per channel the sensor draws 16 W ungated and 12 W gated (§C7b subsection 5). More power per channel is not a lever: it trades receivers against light wasted during the round trips, and the optimum is already ≈30–40 mW per channel (§C7b subsection 2(h)). The energies also assume a laser narrow enough to lose little to phase noise: ≲27 kHz for a 1 dB coherent loss at 200 m, or ≲55 kHz for 3 dB at 300 m (Eq. (115); table in §C7b subsection 2(e)), with its residual chirp error inside Eq. (112), all qualified to automotive grade. Two gaps lie outside this per-watt definition: each sample covers only ≈2% of its cell (§C10.3b, Result 2), which more modes per sample would close at the price of more receivers (§C7b subsection 6, item 3), and the cost curve needs programs of hundreds of thousands of units a year (subsection 4).",
    "Parity follows §C7b subsection 5 (three conditions at 200 m); the ≥100 mW condition is dropped; linewidth restated from Eq. (115).")

add(D5,
    "| FMCW matching 2026 SPAD ToF on point rate per watt (≥15 Mpts/s in ≤15 W at 200–300 m, 10%) | 2032 | ≈3–7% |",
    "| FMCW matching 2026 SPAD ToF on point rate per watt (≥15 Mpts/s in ≤15 W at 200 m on a 10% target, the three conditions of subsection 5) | 2032 | ≈3–7% |",
    "Same parity definition as §C7b subsection 5.")

# ---------------------------------------------------------------- D7
add(f"{MODEL}; 07 report #14 (consistency)",
    "   - §C7a shows that FMCW costs ≈8× the electrical energy per point. Each extra simultaneous line also costs coherent receiver chains (four in the §C7a design; each a mixer with the local laser copy, a balanced detector and a fast ADC, the analog-to-digital converter) plus ≈30 mW of light per channel at 200 m, more at longer range (§C7a subsection 2(e)).",
    r"   - §C7a shows that FMCW costs ≈12× the electrical energy per point ($4.90/0.415\approx11.8$ at 200 m on a 10% target). Each extra simultaneous line also costs coherent receiver chains (four in the §C7a design; each a mixer with the local laser copy, a balanced detector and a fast ADC, the analog-to-digital converter) plus ≈30 mW of light per channel at 200 m, emitted for the whole dwell, and ≈40–53 mW at 250–300 m (§C7a subsection 2(e)).",
    "Ratio 11.8 and the per-channel light of §C7a(e).")

# ---------------------------------------------------------------- F6
add(f"{MODEL}; {D1}; {D3}",
    "Long range is not free: at 200 m FMCW needs ≈3.2× more optical energy per point than 940 nm time-of-flight (ToF) lidar with single-photon avalanche diode (SPAD) receivers, a gap that narrows with distance because its energy grows only in proportion to range when the aperture is matched to it.",
    r"Long range is not free: at 200 m FMCW needs ≈4.2× more useful optical energy per point than 940 nm time-of-flight (ToF) lidar with single-photon avalanche diode (SPAD) receivers ($0.303\ \mu{\rm J}/72\ {\rm nJ}$), and its laser, left on through the round trips, emits ≈5.3× more ($0.384\ \mu{\rm J}/72\ {\rm nJ}$; §C7a subsection 2(a)). The gap narrows with distance because FMCW's energy grows only in proportion to range when the aperture is matched to it.",
    "Useful 4.2× and emitted 5.3× (0.303 and 0.384 µJ against 72 nJ).")

add("07 report #19; " + D1,
    r"and $T_{\rm dwell}$ the time one channel must stay on a point (about one chirp). Tens of parallel LO-matched channels on one PIC (Voyant's Helium direction) would remove the dwell-time penalty.",
    r"and $T_{\rm dwell}$ the time one channel must stay on a point: an up-chirp and a down-chirp plus the round trip that each loses, $T_{\rm dwell}=T_{\rm int}+2\tau=12.67$ µs in the §C7a model at 200 m. At that dwell 10–25 Mpts/s needs $N_{\rm ch}=\dot N T_{\rm dwell}=127$–317 channels, i.e. 507–1,267 receivers (§C7a subsection 2(d)). Hundreds of parallel LO-matched channels on one PIC (Voyant's Helium direction) would offset the dwell-time penalty.",
    "Report-wide dwell and the channel counts it gives.")

add("07 report #20 (numbers); " + D1,
    "so ADC (analog-to-digital converter) and DSP (digital signal processing) energy per channel sets how many channels fit in a 10–15 W sensor power envelope.",
    r"so ADC (analog-to-digital converter) and DSP (digital signal processing) energy per channel sets how many channels fit in a 10–15 W sensor power envelope. In the §C7a central 2026 model one channel's four receivers draw ≈0.18 W ($E_{\rm rx}/T_{\rm dwell}=2.34\ \mu{\rm J}/12.67\ \mu{\rm s}$). After the 3 W overhead a 10–15 W sensor therefore holds ≈38–65 channels even if its light were free ($(10-3)/0.184$ to $(15-3)/0.184$), i.e. 3.0–5.1 Mpts/s, and supports only 1.4–2.4 Mpts/s once the light is paid for ($7\ {\rm W}/4.90\ \mu{\rm J}$ to $12\ {\rm W}/4.90\ \mu{\rm J}$) [E].",
    "Sizes the channels in the envelope from E_rx and the 12.67 µs dwell.")

# ---------------------------------------------------------------- skipped: cross-section quotes of changed numbers
skip("cross_section (C4c count-rate headroom quoted in §0)", "cross_section",
     "§C3a table (d), Princeton Lightwave row: 'InGaAs SPADs would run ≈700× over their count-rate ceiling in sunlight (§C4c)'",
     "No Round 2 agent covers §C3a. Replace 'InGaAs SPADs would run ≈700× over their count-rate ceiling in sunlight (§C4c)' with 'InGaAs SPADs would run ≈340× over their count-rate ceiling in sunlight (§C4c; 3.38×10⁸ counts/s per 0.05° pixel against ≈10⁶ at a 1 µs hold-off)'.")
skip("cross_section (C7a totals)", "cross_section",
     "§C3a, Mobileye row: '(FMCW ≈4.3 µJ vs ToF ≈0.53 µJ per point at 200 m, §C7a)'",
     "No Round 2 agent covers §C3a. Replace '(FMCW ≈4.3 µJ vs ToF ≈0.53 µJ per point at 200 m, §C7a)' with '(FMCW ≈4.9 µJ vs ToF ≈0.42 µJ per point at 200 m, §C7a)'.")
skip("cross_section (C7a(e) light per channel)", "cross_section",
     "§C3a, list of what FMCW needs: 'powerful (≈50–100 mW per simultaneous line, §C7a(e));'",
     "No Round 2 agent covers §C3a. Replace 'powerful (≈50–100 mW per simultaneous line, §C7a(e));' with 'powerful (≈30 mW per simultaneous line at 200 m, emitted for the whole dwell; ≈40–53 mW at 250–300 m and 88 mW in the high-energy case, §C7a(e));'.")

# ---------------------------------------------------------------- skipped: block-07 items the decisions do not settle
skip("07 report §3 flag (power envelopes)", "needs_decision",
     "§F6 '10–15 W sensor power envelope'; Figure C7a '8–25 W typical'; §C6(c) '8–13 W electrical envelopes'; §C7a subsection 6 '≤15 W'",
     "Not settled by the Round 2 decisions. The §F6 channel sizing added in this round uses the 10–15 W it states.")
skip("07 report §3 flag (N_samp)", "needs_decision",
     "§C7a Eqs. (94), (96) (ADC samples per point) against §C10.3a Eqs. (142), (144) (samples per frame)",
     "Not settled by the Round 2 decisions.")
skip("07 report §3 flag (T vs T_c)", "needs_decision",
     "§C7 Eq. (85) ($T$) and Eq. (87) ($T_c$); §C7a Eq. (94) ($T$); §C7b ($T_c$, $T_u$)",
     "Not settled. In §C7a(c) this round defines $T$ as the useful window of a ramp and states that Eq. (94) is Eq. (109) with $T_u=T$; one symbol report-wide is still the author's choice.")
skip("07 report #24 (Moore Photonics)", "needs_decision",
     "§C7 Commercial status, China: '**Moore Photonics** has published claims but no product data.'",
     "Not settled by the Round 2 decisions.")
skip("07 report #1 (table row status)", "needs_decision",
     "§C7a subsection 1 table, row 'Analog Photonics FS-4S': 'No production award found (§C7 Commercial status)'",
     "Not settled by the Round 2 decisions (deployability tag).")
skip("round2 decision 5 (parity probability)", "needs_decision",
     "§C7a subsection 6 table, parity row: '≈3–7%'",
     "The probability is kept. It was judged when the all-three parity case drew 12 W; on the ungated dwell it draws 14.0 W (1 W of margin) and stays inside 15 W only with channels of ≤22.5 mW or a gated transmitter, still at 1.8× the ToF energy per point. Revisit if wanted (the same note applies to §C7b subsection 7).")
skip("figure check (Figure C7a panel b)", "needs_decision",
     "build/figures/fmcw_tof_system_budget.py, panel (b)",
     "In the rebuilt figure the '4.90 µJ' total label over the FMCW 2026 bar overlaps the legend; moving the legend (e.g. loc='upper right') or raising ylim from 6200 to about 6800 and rebuilding would clear it.")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({"block": LABEL, "edits": edits, "skipped": skipped}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(edits)} edits, {len(skipped)} skipped -> {OUT.name}")
