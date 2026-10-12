"""Round 5: edit list for the source items that the Round 2 agents skipped (R2A_C0 skipped item "10.8 Panasonic row").

The Panasonic flash row of §C0 subsection 10.8 quoted 0.13–0.53 photons per pixel per pulse at 100 m without its
inputs, and marked the comparison with the paper as agreeing. Read: Hirose et al., Sensors 18, 3642 (2018), PMC full
text (§2, Fig. 2, Table 2, §4). The inputs that reproduce 0.13–0.53 are the f/1.4 lens sized by a 20° or 10° field over
the 7.71 mm wide array, a 10% target, eta = 1 (photons at the pixel); round5_panasonic_photons.py computes them. The
paper's own Fig. 2 shows about 1.2 photons at 100 m, 2–9 times more, for an aperture it does not state.
Writes edits/round5/R5a_panasonic.json; the report is only read.
Usage: python round5_build_r2_leftovers.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
T = REPORT.read_text(encoding="utf-8")
WHY = ("R2A_C0 skipped item '10.8 Panasonic row' (needs_source): the inputs behind 0.13–0.53 were not stated. "
       "Hirose et al., Sensors 18, 3642 (2018), read in full (PMC6263636): Fig. 2 assumes 1.2 kW, 10 ns, a 20° field "
       "and 10%; the experiments use f/1.4 and a 10° field; 688 × 384 pixels of 11.2 µm. round5_panasonic_photons.py.")
E = [
    ("R5a-001",
     "| Panasonic flash, Hirose et al. (2018) | 940 nm, four 300 W sources, ≈10 ns pulses spread over 688×384 pixels; "
     "f/1.4 lens | 45 pJ per pixel per pulse | — | The model gives 0.13–0.53 photons per pixel per pulse at 100 m; the "
     "paper says below one beyond 100 m ✓ |",
     "| Panasonic flash, Hirose et al. (*Sensors* 2018) | 940 nm, four 300 W sources, ≈10 ns pulses spread over "
     "688×384 pixels of 11.2 µm; f/1.4 lens, 10° field (20° in its photon estimate); 250 m at night | 45 pJ per pixel "
     "per pulse | — | The model gives 0.13 (20° field) to 0.53 (10° field) photons per pixel per pulse at 100 m on 10%. "
     "The paper's own estimate, for an aperture it does not state, is ≈1.2 there, 2–9× more. Both lie below one photon "
     "per pulse at 250 m, which the sensor bridges by accumulating pulses |"),
    ("R5a-002",
     r"Their $\eta A_{\rm rx}$ is 3–5× below the model's 0.81 cm² ($0.81/0.28=2.9$ and $0.81/0.16=5.1$), consistent "
     r"with the lower PDE of 2013–2018 detectors.",
     r"Their $\eta A_{\rm rx}$ is 3–5× below the model's 0.81 cm² ($0.81/0.28=2.9$ and $0.81/0.16=5.1$), consistent "
     r"with the lower PDE of 2013–2018 detectors." "\n"
     r"- **Panasonic's photon count.** Its four sources give $4\times300\ {\rm W}\times10\ {\rm ns}=12\ \mu{\rm J}$ per "
     r"pulse, which, spread evenly over $688\times384=2.64\times10^{5}$ pixels (illumination filling the camera's "
     r"field), is $E_{\rm px}=45$ pJ per pixel. Eq. (55) solved for the count, with $\eta=1$ because the paper counts "
     r"photons arriving at a pixel through the lens, before the PDE, gives $\bar n=\rho E_{\rm px}A_{\rm rx}/(\pi R^2E_{\rm ph})$. "
     r"The aperture of the f/1.4 lens is $D=f/1.4$, and its focal length $f$ follows from the field across the 7.71 mm "
     r"width of the array ($688\times11.2\ \mu{\rm m}$): $f=3.85\ {\rm mm}/\tan10^\circ=21.9$ mm for a 20° field and "
     r"$3.85\ {\rm mm}/\tan5^\circ=44.0$ mm for 10°, i.e. $D=15.6$ and 31.5 mm. At 100 m on 10%, "
     r"$\bar n=0.1\times4.54\times10^{-11}\ {\rm J}\times1.91\times10^{-4}\ {\rm m^2}/(\pi\times(100\ {\rm m})^2\times2.11\times10^{-19}\ {\rm J})=0.13$ "
     r"for the 20° field, and 0.53 with the 31.5 mm lens ($A_{\rm rx}=7.77\times10^{-4}$ m²). The paper's Figure 2, for "
     r"1.2 kW, 10 ns, a 20° field and a 10% target, shows ≈1.2 photons at 100 m and crosses one near 110 m. It gives no "
     r"aperture or losses for that curve, which lies 9× above the model's 0.13 for the same field "
     r"[P, Hirose et al. 2018, §2 and Fig. 2; E]."),
    ("R5a-003",
     r"The model's figures match every published research sensor, given f/1-class lenses of 10–30 mm and overall "
     r"receive efficiencies $\eta$ of 0.05–0.14 (Sony's PDE is 22%; Toshiba and Toyota publish none).",
     r"The model's figures match every published scanning research sensor, given f/1-class lenses of 10–30 mm and "
     r"overall receive efficiencies $\eta$ of 0.05–0.14 (Sony's PDE is 22%; Toshiba and Toyota publish none). "
     r"Panasonic's flash sensor is the exception: its own photon estimate is 2–9× above the model's, for an aperture "
     r"it does not state."),
    ("R5a-004",
     "(Yoshioka et al., Toshiba, ISSCC 2018, with the comparison to Niclass et al. 2013)",
     "(Yoshioka et al., Toshiba, ISSCC 2018, with the comparison to Niclass et al. 2013) ; "
     "https://doi.org/10.3390/s18113642 (Hirose et al., Panasonic, *Sensors* 2018)"),
    ("R5a-005",
     "- Kumagai et al., ISSCC 2021: doi:10.1109/ISSCC42613.2021.9365961",
     "- Kumagai et al., ISSCC 2021: doi:10.1109/ISSCC42613.2021.9365961\n"
     "- Hirose *et al.* (Panasonic), 250 m direct ToF with a 688 × 384 vertical-avalanche-photodiode image sensor, "
     "*Sensors* 18, 3642 (2018): https://doi.org/10.3390/s18113642"),
]
edits = []
for eid, old, new in E:
    assert T.count(old) == 1, (eid, T.count(old))
    edits.append({"id": eid, "finding": "R2A_C0 skipped item: 10.8 Panasonic row (needs_source)", "old": old,
                  "new": new, "why": WHY})
out = HERE / "edits" / "round5" / "R5a_panasonic.json"
out.parent.mkdir(parents=True, exist_ok=True)
assert not out.exists() or "--force" in __import__("sys").argv, f"{out.name} exists; pass --force to rebuild it"
out.write_text(json.dumps({"block": "R5a_panasonic", "edits": edits, "skipped": []}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(len(edits), "edits ->", out.name)
