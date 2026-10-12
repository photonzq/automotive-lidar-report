"""Verified cross-chunk fixes after the readability rewrite (edits chunk working files in place)."""
from pathlib import Path

HERE = Path(__file__).resolve().parent
missing = []


def edit(cid, old, new, count=1, section=None):
    p = HERE / f"chunk{cid}" / f"chunk{cid}.md"
    t = p.read_text(encoding="utf-8")
    if section:
        a = t.index(section[0])
        b = t.index(section[1], a) if section[1] else len(t)
        seg = t[a:b]
        n = seg.count(old)
        if n != count:
            missing.append((cid, n, old[:70]))
            return
        t = t[:a] + seg.replace(old, new) + t[b:]
    else:
        n = t.count(old)
        if n != count:
            missing.append((cid, n, old[:70]))
            return
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8")


# --- chunk 01: scope pointers; §A6.3 opening made consistent with its own evidence
edit("01", "print in one exposure; lidar-to-lidar interference, with a literature review (§C9a);",
     "print in one exposure (§C8); lidar-to-lidar interference, with a literature review (§C9, §C9a);")
edit("01", "High-beam reach comfortably exceeds stopping distance at highway speeds, but drivers rarely use high beams.",
     "On paper, the high beam's photometric reach (§A6.1) far exceeds highway stopping distance, about 98 m at 100 km/h. "
     "In measured tests, though, switching to high beam raised pedestrian recognition distance only to about 94 m (below), "
     "and drivers rarely use high beams.")

# --- chunk 02: wrong direction pointer; Aurora mileage dates; Valeo average range
edit("02", "Nasdaq listing Jun 2026 (above)", "Nasdaq listing Jun 2026 (below)")
edit("02", "more than 500k driverless miles; 200 trucks",
     "more than 500k driverless miles by the late-September release (the Q2 letter gave ≈440k at end-June, table below); 200 trucks")
edit("02", "Valeo's historic average of about 20k per year is a cross-check.",
     "Valeo's historic average of about 20–24k per year (derived below) is a cross-check.")

# --- chunk 03: Gatik runs middle-mile trucks, not sidewalk robots
edit("03", "plus the much smaller fleets of Avride and Gatik.",
     "plus the much smaller fleets of Avride's sidewalk robots and Gatik's middle-mile trucks "
     "(Gatik's are road trucks, not sidewalk robots, but they are counted here as delivery lidars outside China).")

# --- chunk 04: étendue statement was reversed
edit("04", r"$A\,\Omega$ is conserved through passive optics, so a smaller pixel angle at a fixed f-number means a smaller aperture",
     r"$A\,\Omega$ is conserved through passive optics. At a fixed f-number, a smaller pixel pitch at the same pixel angle "
     r"therefore means a smaller aperture, while a smaller pixel angle at the same pitch means a larger one")

# --- chunk 05: grant total basis; Mobileye source matches the linked filing; Aeva price date
edit("05", "≈€3.0 M of grants, ≈5% of >€60 M invested, plus the EIB loan [E]",
     "≈€3.0 M of grants (excluding the ≈€0.70 M of COVID aid), ≈5% of >€60 M invested, plus the EIB loan [E]")
edit("05", "(≈90 affected staff, per its 2024 10-K)", "(≈90 affected staff, per its Q3 2024 10-Q)")
edit("05", "≈90 affected in the 2024 10-K (§C3)", "≈90 affected in the Q3 2024 10-Q (§C3)")
edit("05", r"≈\$1.0 B market cap in Sep 2026 (68.7 M shares × \$14.78)",
     r"≈\$1.0 B market cap in Sep 2026 (68.7 M shares × \$14.78, a September price; the latest weekly close in subsection 5 is \$15.35)")

# --- chunk 06: §C10.6 now uses the AT128's 210 m figure
edit("06", r"Against the AT128's 200 m rating (§C10.6) this is $(41.04/1.536)\times(300/200)^2=26.7\times2.25\approx60$; "
           r"against its 210 m product-page figure it is $26.7\times(300/210)^2\approx55$.",
     r"Against the AT128's 210 m product-page figure, which §C10.6 uses, it is $26.7\times(300/210)^2\approx55$; "
     r"an older 200 m rating would give $(41.04/1.536)\times(300/200)^2=26.7\times2.25\approx60$.")

# --- chunk 07: InP multiple matches its derivation; IMX459 geometry precise; C4d scan rate -> Omega
edit("07", "and processed InP is 1–3 orders of magnitude dearer, depending on volume.",
     "and processed InP is about 1.4–3.4 orders of magnitude (24× to 2,400×) dearer than 28 nm silicon, depending on volume (derived below).")
edit("07", "SPAD array **189×600**, the IMX459 geometry;",
     "SPAD array **189×600**, the physical array of Sony's ISSCC 2021 design behind the IMX459 (597 × 168 effective SPADs, §C5a);")
edit("07", r"\omega_{\max}", r"\Omega_{\max}", count=1, section=("## C4d.", "## C5."))
edit("07", r"\omega", r"\Omega", count=9, section=("## C4d.", "## C5."))

# --- chunk 08: SiPM cell count consistent with Layer 5
edit("08", "up to the SiPM limit of hundreds of cells (§C4b)", "up to the SiPM limit of hundreds to about a thousand cells (§C4b)")

# --- chunk 09: receiver-energy range matches its low and high cases
edit("09", "This gives **≈0.56 µJ per point** (0.3–0.9):", "This gives **≈0.56 µJ per point** (0.3–0.95):")

# --- chunk 10: ratio range at 0.30 µJ
edit("10", "is 3.5–7.0 at 0.30 µJ and 1.9–3.5 at 0.15 µJ", "is 3.7–7.0 at 0.30 µJ and 1.9–3.5 at 0.15 µJ")

# --- chunk 11: listening time is the column time; C10 keeps omega for scan rate (Omega is solid angle there)
edit("11", r"My pixel listens for about 2 µs per shot × 10 shots, giving $T_{\rm listen}\approx$ 20.8 µs per point (§C6).",
     r"My pixel listens for the whole 20.8 µs column time per point, about 10 shots of ≈2 µs each (§C6), so $T_{\rm listen}\approx20.8$ µs.")
edit("11", r"where $R$ is the range, $\omega$ the angular scan rate (rad/s),",
     r"where $R$ is the range, $\omega$ the angular scan rate of the beam (rad/s; §C0, §C4d and §C7 write it $\Omega$, "
     r"but §C10 keeps $\Omega$ for solid angles),")

# --- chunk 12: rounding; scan-rate symbol note
edit("12", r"about 2.5 fps ($1{,}000/410=2.4$ fps)", r"about 2.4 fps ($1{,}000/410=2.4$ fps)")
edit("12", r"where $\omega$ is the optical scan rate in rad/s and $D$",
     r"where $\omega$ is the optical scan rate in rad/s (written $\Omega$ in §C0, §C4d and §C7) and $D$")

# --- chunk 14: Xpeng uses radar; rounding shown with the unrounded factors
edit("14", "Only Tesla (and Xpeng) ship camera-only driving with no lidar tier.",
     "Only Tesla ships camera-only driving; Xpeng ships cameras plus radar, with no lidar tier.")
edit("14", r"$4.1\times2.1\approx8.9$ angular cells", r"$4.13\times2.15\approx8.9$ angular cells")

# --- chunk 15: preprint year vs venue year
edit("15", "Yu et al. reached the same qualitative conclusion in 2022:",
     "Yu et al. reached the same qualitative conclusion in a 2022 preprint (published at a CVPR workshop in 2023):")

# --- chunk 16: marker that no item carries; lidar cost share quantified; fleet counts dated
edit("16", " Items marked *(not yet researched)* have not been investigated.", "")
edit("16", "under 1% of today's cost and a few per cent at maturity.",
     r"under 1% of today's cost and about 1–6% at maturity (about 1% for four \$1,000 lidars, about 6% for a \$20k sensor suite).")
edit("16", "The active unsupervised fleet is only about 85–200 per trackers, with Austin's",
     "The active unsupervised fleet was only about 85–200 per trackers in late Aug 2026 (≈300 across Texas and Florida by late Sep, Appendix 1), with Austin's")

print("missing:", missing)
