"""Follow-up write after the parallel 10.7 edit: notation fix, evidence-tag style, and the measured-efficiency
caveat (the author's choice, relayed by the parallel edit) in §C7a and §C7b. Hash-guarded; exact-substring edits."""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
RP = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
DRY = "--dry" in sys.argv
raw = RP.read_bytes()
h0 = hashlib.sha256(raw).hexdigest()
t0 = raw.decode("utf-8")
assert "\r\n" not in t0
t = t0
print("read", len(raw), "bytes, sha", h0[:12])


def rep(old, new, count=1):
    global t
    n = t.count(old)
    assert n == count, (old[:80], n)
    t = t.replace(old, new)


# 1. P_{FA,\rm pt}: texmath needs the \rm inside its own group
rep(r"P_{FA,\rm pt}", r"P_{FA,{\rm pt}}", count=4)

# 2. evidence tags in the FFT paragraph
rep(r"**Is the FFT the limit? Nearly** [E; detection theory I]. For a tone of unknown frequency and phase in white noise, the peak of the FFT power spectrum (the periodogram) is the maximum-likelihood, or generalized likelihood-ratio, detector (S. M. Kay, *Fundamentals of Statistical Signal Processing*, Vol. II, 1998).",
    r"**Is the FFT the limit? Nearly** [E]. For a tone of unknown frequency and phase in white noise, the peak of the FFT power spectrum (the periodogram) is the maximum-likelihood, or generalized likelihood-ratio, detector [I: S. M. Kay, *Fundamentals of Statistical Signal Processing*, Vol. II: Detection Theory (Prentice Hall, 1998)].")

# 3. §C7a short answer
rep(r"This narrows to about **5×** in an optimistic 2032 projection ($1.48/0.286\approx5.2$; totals from the §3 table). Both receivers are held to the same detection rule (§C0 subsection 10.3).",
    r"This narrows to about **5×** in an optimistic 2032 projection ($1.48/0.286\approx5.2$; totals from the §3 table). Both receivers are held to the same detection rule (§C0 subsection 10.3). With the lower FMCW efficiencies measured so far (§2(a)), the 2026 gap is ≈12–15× for a discrete fibre chain and ≈25× for an integrated array.")

# 4. §C7a(a): after the Waymo check
line = next(l for l in t.split("\n") if l.startswith("  - **Check against Waymo.**"))
rep(line, line + "\n" + r"  - **Measured efficiencies are lower.** The FMCW value, 0.25, is a design value at the optimistic end of what has been measured. Waymo's lab chain measured 0.112 end to end, or 0.168 without its Hann window (Piggott et al. 2025, App. A), and Pointcloud's integrated array 0.057 once its amplifier noise is counted (Settembrini et al. 2026) [P; §C0 subsection 10.1]. With those values FMCW needs 1.5–2.2× (discrete fibre chain) or about 4.4× (integrated array) the optical energy per point quoted here: 0.45–0.67 µJ or 1.3 µJ instead of 0.30 µJ. The laser's electrical energy scales in the same way while the receiver electronics do not, so the total per point rises from 4.25 µJ to 5.2–6.7 µJ (12–15× ToF), or to ≈11 µJ (≈25×). The model keeps 0.25 as its central value and carries these as a sensitivity.")

# 5. §C7b 1(c): after the AMCW-row bullet
line = next(l for l in t.split("\n") if l.startswith("- **AMCW row:** an iToF camera integrates sunlight over its whole exposure"))
rep(line, line + "\n" + r"- **The FMCW efficiency is a design value.** The FMCW value, 0.25, is at the optimistic end of what has been measured: Waymo's lab chain measured 0.112 end to end, or 0.168 without its Hann window, and Pointcloud's integrated array 0.057 (§C0 subsection 10.1, §C7a(a)). With those values the FMCW rows need 1.5–2.2× or about 4.4× the energy shown, so FMCW buys 6–9× (discrete fibre chain) or ≈18× (integrated array) fewer points per optical joule than SPAD ToF, instead of ≈4×.")

# 6. §C7b subsection 5: after the "Reaching 0.15 uJ" paragraph
line = next(l for l in t.split("\n") if l.startswith(r"**Reaching $E_{\rm opt}\approx0.15$ µJ**"))
rep(line, line + "\n\n" + r"**The efficiency is also the least certain input.** The FMCW value, 0.25, is a design value at the optimistic end of what has been measured: Waymo's lab chain measured 0.112 end to end, or 0.168 without its Hann window, and Pointcloud's integrated array 0.057 (§C0 subsection 10.1). With those values FMCW needs 1.5–2.2× (discrete fibre chain) or about 4.4× (integrated array) the energy per point quoted in this report, and the 2026 central case rises from ≈67 W at 15 Mpts/s to ≈82–104 W, or to ≈170 W. Parity's $\eta\approx0.5$ is therefore 3–9× above the chains measured so far.")

# hygiene
for l in t.split("\n"):
    if l not in t0 and len(re.findall(r"(?<!\\)\$", l)) % 2:
        print("ODD $:", l[:100])
for w in ["corrected", "updated", "revised", "added"]:
    if t0.count(w) != t.count(w):
        print("WORD COUNT CHANGE", w, t0.count(w), "->", t.count(w))
assert len(re.findall(r"\\tag\{\d+\}", t)) == len(re.findall(r"\\tag\{\d+\}", t0))
out = t.encode("utf-8")
if DRY:
    (HERE / "report_fix2_dry.md").write_bytes(out)
    print("dry ok", len(out))
    sys.exit(0)
if hashlib.sha256(RP.read_bytes()).hexdigest() != h0:
    print("ABORT: report changed")
    sys.exit(2)
RP.write_bytes(out)
(HERE / "report_after_fix2.md").write_bytes(out)
print("written", len(raw), "->", len(out))
