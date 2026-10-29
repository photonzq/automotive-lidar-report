"""Addition of 2026-10-29 to the camera-damage block (§C4c subsection 1): "Remedies", replacing the one-sentence remedy
at the end of the Verdict. The filter specification (optical density from the worst case of the estimate, the band
from the off-axis shift of an interference coating, the fluence on the filter itself), what a filter does not fix,
and the lidar-side measures (a global cut to 905-class pulses against a pulse energy adapted to range).
Writes edits_remedies.json. The report is only read. Usage: python add_remedies.py [--force]
"""
import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
REPORT = HERE.parent.parent / "automotive_perception_report_2026-09-27.md"
T = REPORT.read_text(encoding="utf-8")
WHY = "Whether a filter or the lidar can prevent camera damage (2026-10-29)."

# the numbers quoted in the text
F_TH = 0.026                                         # J/cm^2, cumulative threshold used in the estimate
A20, A10 = math.pi * (20e-4) ** 2 / 4, math.pi * (10e-4) ** 2 / 4
worst = 10e-6 / A10
central = 2e-6 / A20
shift = 1550 * (1 - math.sqrt(1 - math.sin(math.radians(30)) ** 2 / 1.8 ** 2))
a_filter = math.pi * (0.05 / 2.8) ** 2 / 4           # beam 0.5 mm / 2.8 wide, in cm
print(f"worst F = {worst:.2f} J/cm^2 = {worst/F_TH:.0f} x F_th, OD {math.log10(worst/F_TH):.2f}; "
      f"central F = {central:.3f} J/cm^2, OD {math.log10(central/F_TH):.2f}")
print(f"off-axis shift at 30 deg, n_eff 1.8: {shift:.0f} nm; 1,565 + shift = {1565 + shift:.0f} nm")
print(f"beam at the filter {0.5/2.8:.3f} mm; fluence 2 uJ {2e-6/a_filter*1e3:.1f}, 10 uJ {10e-6/a_filter*1e3:.1f} mJ/cm^2")
print(f"clip-on 75% reflection: close-up {0.25*central:.3f} J/cm^2 = {0.25*central/F_TH:.1f} x F_th; ranges x {math.sqrt(0.25):.2f}")
print(f"global cut: E_p <= {F_TH*A20*1e9:.0f} nJ; adaptive 20 nJ: {20e-9/A20*1e3:.1f} mJ/cm^2 = {20e-9/A20/F_TH:.2f} x F_th")


def edit(eid, old, new):
    assert T.count(old) == 1, (eid, T.count(old), old[:70])
    return {"id": eid, "finding": "Remedies for lidar damage to cameras", "old": old, "new": new, "why": WHY}


REMEDIES = [
    r"",
    r"",
    r"**Remedies** [P/T/E]. A filter in the camera protects new silicon cameras at no cost in image signal, but not the cameras already in use; on the lidar side, only a pulse energy adapted to range keeps the range that justifies 1,550 nm.",
    r"",
    r"- **A 1,550 nm block in front of the sensor.**",
    r"  - The worst case considered above, a whole 10 µJ pulse in a 10 µm spot, gives $F=10^{-5}\ {\rm J}/7.85\times10^{-7}\ {\rm cm^2}=12.7\ {\rm J\,cm^{-2}}$, 490 times the cumulative threshold. A transmission below 1/490, i.e. an optical density (OD) of $\log_{10}490=2.7$, therefore keeps every case in the table below the cumulative threshold, even for a camera fixed in front of the lidar; the central case (2 µJ in a 20 µm spot) needs only $\log_{10}(0.64/0.026)=1.4$.",
    r"  - Silicon does not respond beyond about 1,100 nm, so a block from 1,100 to 1,700 nm costs no image signal, and cameras that use 850 or 940 nm illumination keep that band.",
    r"  - An interference coating's stopband moves to shorter wavelengths for light arriving off axis, by $\Delta\lambda\approx\lambda[1-\sqrt{1-\sin^2\theta/n_{\rm eff}^2}]$ for an angle of incidence $\theta$ and an effective index $n_{\rm eff}$: $1{,}550\ {\rm nm}\times[1-\sqrt{1-0.25/1.8^2}]=61$ nm at $\theta=30°$ and $n_{\rm eff}=1.8$. To block the 1,530–1,565 nm band of erbium-fibre lidars at every angle, the coating should therefore block about 1,500–1,650 nm at normal incidence.",
    r"  - Colour cameras already carry an infrared-cut coating, OD 2.5 from 700 to 1,200 nm in Théberge et al.'s camera (p. 2474), whose stopband could be extended to cover this band.",
    r"  - The filter receives far less than the sensor. At, for example, 0.5 mm in front of the sensor at f/2.8, the converging beam is still $0.5\ {\rm mm}/2.8=0.18$ mm wide, so a 2–10 µJ pulse spreads to $2$–$10\ \mu{\rm J}/(\pi(0.018\ {\rm cm})^2/4)=8$–$40\ {\rm mJ\,cm^{-2}}$, against 0.64–12.7 J cm⁻² at the focal spot.",
    r"  - Bi et al. propose such a filter (p. 4718), and Volvo recommends filters or protective covers on the lens [T, The Drive].",
    r"- **What a filter does not fix.**",
    r"  - Cameras already in use cannot be recoated. A clip-on filter helps only if its optical density at 1,550 nm is known and high enough: one that reflects 75% of the light (OD 0.6), for example, still leaves a close-up at $0.25\times0.64=0.16\ {\rm J\,cm^{-2}}$, six times the cumulative threshold, and only halves the cumulative ranges, which scale as the square root of the transmission.",
    r"  - Day/night security cameras swing their infrared-cut filter out at night to use 850 or 940 nm illumination, so the 1,550 nm block would have to sit on a fixed element; a short-pass edge near 1,100 nm leaves those bands open.",
    r"  - Short-wave infrared (SWIR) cameras, such as those built on TriEye's sensor, which is sensitive from 700 to 1,650 nm (§A7.5), detect 1,550 nm themselves. They can only notch out the lidar band, and for them the light is absorbed in the photodiodes; no damage thresholds were found for them.",
    r"  - No standard requires either side to act: IEC 60825-1 classifies lidars for the eye only, and no camera-safety requirement for lidars was found.",
    r"- **On the lidar side.**",
    r"  - Cutting every pulse is not an option. Keeping a whole pulse in a 20 µm spot below the cumulative threshold needs $E_{\rm p}\le26\ {\rm mJ\,cm^{-2}}\times3.14\times10^{-6}\ {\rm cm^2}=82$ nJ, the pulse energy of a 905 nm lidar (subsection 1 above), which gives up the range that justifies 1,550 nm.",
    r"  - A pulse energy adapted to range costs little range [E]. A scanning lidar knows each direction's range from the previous frame, and the echo of a target that fills the beam scales as $E_{\rm p}/R^2$ (§C0 subsection 3.1). Cutting the pulse energy 100-fold toward anything within 20 m therefore keeps its echo as strong as a full pulse returns from 200 m, since $(200/20)^2=100$. A camera filming from close up would then receive $20\ {\rm nJ}/3.14\times10^{-6}\ {\rm cm^2}=6.4\ {\rm mJ\,cm^{-2}}$ per pulse, a quarter of the cumulative threshold. The first frame after the camera appears, and large lenses tens of metres away, remain exposed. HiEV suggested a low-energy mode for close range or a stationary car [T, HiEV via 36Kr]; no lidar with such a mode was found.",
]

OLD = (" The remedies are a filter that blocks 1,550 nm in front of the sensor, which Bi et al. propose (p. 4718), and, "
       "on the lidar side, lower pulse energy at the cost of range.")
edits = [edit("R1-C4c-remedies", OLD, "\n".join(REMEDIES))]

out = HERE / "edits_remedies.json"
assert not out.exists() or "--force" in sys.argv, f"{out.name} exists; pass --force"
data = json.dumps({"block": "camera_damage_2026-10/remedies", "edits": edits, "skipped": []}, ensure_ascii=False,
                  indent=1)
out.write_bytes((data + "\n").encode("utf-8"))
print(out.name, len(edits), "edits")
