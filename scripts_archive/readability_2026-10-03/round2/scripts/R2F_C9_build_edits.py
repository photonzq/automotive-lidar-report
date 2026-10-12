"""Round 2, agent R2F_C9: writes edits/round2/R2F_C9.json for sections C9 and C9a (interference model).

Each "old" text is cut from the live report (whole lines checked against their start, or exact fragments) and
checked to occur once, to lie between "## C9." and "## C10.", and not to overlap another edit.
The numbers in the "new" texts come from R2F_C9_interference_model.py (same folder).
Reads the report only; writes only the JSON. Run from any folder with the Anaconda interpreter.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                      # report folder
REPORT = ROOT / "automotive_perception_report_2026-09-27.md"
OUT = HERE.parents[1] / "edits" / "round2" / "R2F_C9.json"
text = REPORT.read_text(encoding="utf-8")
lines = text.split("\n")
sec0, sec1 = text.index("## C9. Lidar-to-lidar"), text.index("## C10. Can optical")


def block(first, last, start):
    """Lines first..last (1-based, inclusive), checked against the start of the first line."""
    s = "\n".join(lines[first - 1:last])
    assert s.startswith(start), (first, s[:80])
    return s


edits = []


def add(eid, finding, old, new, why):
    edits.append({"id": f"R2F_C9-{eid:03d}", "finding": finding, "old": old, "new": new, "why": why})


# ---------------------------------------------------------------- C9, units within 100 m
add(1, "report #6",
    "from a few to perhaps 15 lidars today, depending on city and location; dozens later, as the fleet turns over.",
    "from about 3 to about 16 lidars today, depending on city and location, and dozens later as the fleet turns over; "
    "the estimate below takes 10–30 for that later case.",
    "States the derived 3–16 of the same bullet and links the later case to the n = 10–30 used in the Result.")

# ---------------------------------------------------------------- C9, direct interference chain
old2 = block(5662, 5663, "   - Aligned hits, where my active pixel")
new2 = "\n".join([
    r"   - Aligned hits, in which my active pixel looks at the foreign unit while its beam crosses my aperture, are rare [E]. Take two facing §C6-class units more than about 30 m apart, each scanning 2,400 columns of 20.8 µs per 50 ms frame. Each unit's 0.05° column is then at least as wide as the other's 25 mm aperture ($8.73\times10^{-4}\ {\rm rad}\times30\ {\rm m}=26$ mm), so the foreign beam lights my aperture during one or two of its column periods per frame, and my pixel that images the foreign aperture listens during one or two of mine. With unsynchronized scans the two intervals overlap in $2/2{,}400=0.8\times10^{-3}$ to $4/2{,}400=1.7\times10^{-3}$ of frames, and each overlap saturates one to four points. Aligned hits therefore occur in about one frame in a thousand, a few points at a time.",
    r"   - Stray light is the larger risk. If lens flare or window scatter delivers even $10^{-5}$ of the directly received power to each of the other active pixels, each gets about 100 times the return of a 10% Lambertian target at the same range ($10^{-5}\times10^{7}=10^{2}$). How many points each crossing of the foreign beam over my aperture costs then depends on how far that light spreads [E]:",
    r"     - In the *localized* case it spreads over about 2.5° around the foreign unit, the order of Popko's direct-interference extent (§C9a item 5), and it reaches my active column only while my scan is within those 50 columns ($2.5^\circ/0.05^\circ$), in $(50+2)/2{,}400=2.2\%$ of frames. It then hits about 50 pixels in each of one or two columns: 50–100 points, or $4\times10^{-5}$ to $8\times10^{-5}$ of a 1.25 Mpt frame ($50/(1.25\times10^{6})$ and $100/(1.25\times10^{6})$). Averaged over all frames, that is at most $0.022\times100/(1.25\times10^{6})=1.7\times10^{-6}$ of points.",
    r"     - In the *column-wide* case it reaches the whole active column at every crossing, and each frame loses $520\times1=520$ to $520\times2=1{,}040$ points, $4\times10^{-4}$ to $8\times10^{-4}$ of the frame. That is the order $10^{-3}$ of points per frame, and the upper end of this chain.",
])
add(2, "report #2", old2, new2,
    "Gives the facing-scanner claim an [E] chain, per frame and per event: aligned hits in ~1e-3 of frames; "
    "1e-6 (localized) to 4–8e-4 (column-wide) of points per frame.")

# ---------------------------------------------------------------- C9, chain: visits
add(3, "report #1 (visit structure)",
    r"so $r_{\rm f}=2.5\times10^{8}\ {\rm s^{-1}}\times0.0025/3{,}120\approx200$ s⁻¹.",
    r"so $r_{\rm f}=2.5\times10^{8}\ {\rm s^{-1}}\times0.0025/3{,}120\approx200$ s⁻¹. They arrive as one ten-shot "
    r"column per 50 ms frame ($10\times20\ {\rm s^{-1}}=200\ {\rm s^{-1}}$), which sets the ghost rate after "
    r"rejection (§C9a item 3).",
    "States the arrival structure that the rebuilt Eq. (128) uses.")

# ---------------------------------------------------------------- C9, Result
old4 = block(5682, 5682, "- **Result:** with $n=$ 10–30 such lidars")
new4 = (r"- **Result:** with today's 3–16 such lidars within 100 m (above), if all of them overlapped fully, "
        r"**about 1.2–6.5% of points would carry at least one foreign shot in their histogram window** (the set of time "
        r"bins in which the receiver accumulates counts for one point), and the later 10–30 would give about 4–12%. "
        r"From Eq. (127) with the unrounded $p_1=4.17\times10^{-3}$ ($200.3\ {\rm s^{-1}}\times20.83\ \mu{\rm s}$), "
        r"$1-(1-p_1)^{n}$ is 1.2% for $n=3$, 6.5% for $n=16$, 4.1% for $n=10$ and 11.8% for $n=30$. §C9a item 2 "
        r"scales these down for partial overlap and wavelength. A smaller foreign unit (2 Mpts/s, 0.1° pixel) gives "
        r"about a third of this: at 10 shots per point it fires $2\times10^{7}$ shots/s, each lighting 0.01 deg² "
        r"(larger than my pixel, so $\Omega_{\rm hit}\approx0.01$ deg²), so $2\times10^{7}\times0.01/3{,}120\approx64$ "
        r"shots/s land on my pixel, $64\times20.8\ \mu{\rm s}=1.3\times10^{-3}$ per point, and 3–16 such units give "
        r"0.4–2.1% while 10–30 give 1.3–3.9%.")
add(4, "report #6", old4, new4,
    "Gives the rates for today's 3–16 units and the later 10–30, with the substitution.")

# ---------------------------------------------------------------- C9, dither bullet
add(5, "report #1 (link to C9a)",
    "and each pair shares a bin with probability 1/1,800.",
    "and each pair shares a bin with probability 1/1,800. Five is the mean number of shots that one foreign unit's "
    "ten-shot column puts into my point when the two overlap; §C9a item 3 turns this into a ghost rate per point.",
    "Ties the §C9 dither example to the visit term of Eq. (128).")

# ---------------------------------------------------------------- C9, count threshold bullet
add(6, "report #1 (rule strength)",
    r"Robust rejection therefore needs a consistency test (a peak present in at least $m$ of the $N_{\rm shots}$ "
    r"shots of a point) or code matching.",
    r"Robust rejection therefore needs a consistency test (a peak present in at least $m$ of the $N_{\rm shots}$ "
    r"shots of a point), with $m\ge3$ if random ghosts are to be negligible in dense traffic (§C9a item 3), or code "
    r"matching.",
    "States the rule strength that the rebuilt estimate supports.")

# ---------------------------------------------------------------- C9a, Popko table cell
add(7, "report #8 (method comparison)",
    "Replicating Kim's setup gave ≈300× Kim's rate, so method matters",
    "Replicating Kim's arrangements gave 1.4–2.4× Kim's rate where only scattered light could interfere and up to "
    "≈350× where direct view was possible (thesis Table 8), so geometry and method matter",
    "Popko's Table 8: 1.36–2.36x in side-by-side #2 (scattered only), 298–351x side by side #1, 9–240x face to face.")

# ---------------------------------------------------------------- C9a, item 1
old8 = block(5737, 5738, "   - Applying the §C9 flux × window structure")
new8 = "\n".join([
    r"   - *Kim's geometry* [P, Kim et al. 2017, Table 1]. Each SICK LMS-511 fires 36 kHz pulses, one per 0.25° step at 25 rotations per second ($36{,}000/25=1{,}440$ steps per 360°). Its beam diverges by 11 mrad (0.63°), it ranges to 80 m, and each point is one shot. SICK's LMS511 datasheet gives a 0.2–80 m working range and, for its PRO variant, 11.9 mrad [P].",
    r"   - *Prediction.* The rate of foreign shots into one footprint of the victim scanner is the shot rate times the hit width over the field, $r_{\rm f}=36{,}000\ {\rm s^{-1}}\times\theta_{\rm hit}/360^\circ$. The hit width $\theta_{\rm hit}$ lies between one beam width (0.63°, the larger-of-the-two rule of Eq. (127)) and two (1.26°, counting any partial overlap of two 0.63° spots), so $r_{\rm f}=63$–126 s⁻¹. The receiver listens for the round trip to its 80 m maximum range, $T_{\rm listen}=2\times80\ {\rm m}/c=0.534$ µs. Eq. (127) then gives $p_1=63\ {\rm s^{-1}}\times0.534\ \mu{\rm s}=3.4\times10^{-5}$ to $126\ {\rm s^{-1}}\times0.534\ \mu{\rm s}=6.7\times10^{-5}$ per point, with a central value of $5.0\times10^{-5}$. This is the model's prediction for Kim's geometry, not a measurement.",
    r"   - *Measurement.* Kim measured $6\times10^{-6}$–$1.7\times10^{-4}$ over all four arrangements, as in the table above. Interfered points, summed over the burst lengths of the 2017 paper's Table 4 and divided by the points scanned per arrangement in its Table 3, give $35{,}867/(1.38\times10^{9})=2.6\times10^{-5}$ face to face, $42{,}292/(1.38\times10^{9})=3.1\times10^{-5}$ and $230{,}916/(1.38\times10^{9})=1.7\times10^{-4}$ side by side, and $4{,}691/(7.8\times10^{8})=6.0\times10^{-6}$ back to back. Back to back, the two fields do not overlap, so a foreign pulse must scatter more than once to arrive. The three arrangements with overlapping fields, the case Eq. (127) describes, give $2.6\times10^{-5}$–$1.7\times10^{-4}$; the prediction lies inside that range, within a factor of 2.5 of either end. Popko measured 2–3×10⁻⁴ scattered-only, and his repeat of the Kim arrangement in which only scattered light could interfere gave 1.4–2.4× Kim's rate.",
    r"   - *Rescaling.* Our flux × window, $p_1=4.17\times10^{-3}$, is $4.17\times10^{-3}/(5.0\times10^{-5})\approx83$ times the central prediction for Kim's geometry. Multiplying the measured $2.6\times10^{-5}$ (Kim, face to face) to $3\times10^{-4}$ (Popko) by 83 gives $2.2\times10^{-3}$–$2.5\times10^{-2}$, which brackets §C9's $4.2\times10^{-3}$ per fully overlapping foreign lidar.",
])
add(8, "report #7, report #8, consistency flag #4", old8, new8,
    "Derives 63–126 shots/s from Kim's Table 1 (36 kHz, 0.25°, 11 mrad) and the 80 m window; labels the prediction; "
    "reconciles 6e-6–1.7e-4 (all arrangements) with 2.6e-5–1.7e-4 (overlapping fields).")

# ---------------------------------------------------------------- C9a, item 2
old9 = block(5739, 5739, "2. **4–12% is a worst case.**")
new9 = "\n".join([
    r"2. **The fully overlapping rates are worst cases, today's 1.2–6.5% as much as the later 4–12%.** In traffic, three factors reduce the rate of foreign shots into my footprints; each is an estimate [E]:",
    r"   - *Scene overlap* $f_{\rm ov}$, the share of a foreign unit's shots that land inside my field: 0.25–0.6. The low end is Popko's typical ≈¼ beam-intersection fraction for two coplanar scanners (Models, above); the high end is a car ahead facing the same way, most of whose 120° field lies inside mine.",
    r"   - *In-band share* $f_{\rm band}$, the share of foreign units that my receive filter passes: 0.5–0.9. 9xx-nm units are ≈94–96% of Chinese installations (§C2), but this report does not quantify their 905/940 nm split, so the range assumes my band holds half to most of them.",
    r"   - *Spot density* $f_{\rm sd}\approx(R/R_{\rm f})^2$, where $R$ and $R_{\rm f}$ are my range and the foreign unit's range to the surfaces I see: 0.5–1. It is 1 at equal range, as Eq. (127) assumes, and 0.5 when the foreign unit is 1.4 times farther ($1/1.4^2=0.5$), because the light of its spots on those surfaces falls as the square of its range. A unit closer to them than I am gives more than 1, so this factor is the least certain.",
    r"   - The product is $F=f_{\rm ov}f_{\rm band}f_{\rm sd}=0.25\times0.5\times0.5=0.0625$ to $0.6\times0.9\times1=0.54$, and Popko's ≈¼ overlap alone sits inside that range. With $F\,p_1$ in place of $p_1$ in Eq. (127), $1-(1-F\,p_1)^{n}$ gives **about 0.08–3.5% of points carrying at least one foreign shot before rejection today** ($n=3$ with $F=0.0625$, $n=16$ with $F=0.54$) and 0.26–6.5% later ($n=10$ and 30). Counting only single-scatter paths is right (Kim's power analysis).",
])
add(9, "report #9", old9, new9,
    "Gives each reduction factor a range and tag before multiplying, and the reduced rates for today and later, in shots.")

# ---------------------------------------------------------------- C9a, item 3 (ghost model, Eq. (128))
old10 = block(5740, 5746, "3. **After consistency checks, random ghosts are rare.**")
new10 = "\n".join([
    r"3. **Random ghosts: a 3-of-10 consistency test makes them negligible by day and night; 2-of-10 is marginal.**",
    r"   - Ghosts are built from foreign *shots*, not counts. One foreign shot can fill a bin with up to nine counts (§C9), so a count threshold does not reject it; what rejects it is that it does not recur. The receiver is taken to apply an $m$-of-10 shot-recurrence rule: a peak is accepted only if a significant per-shot event, for example a coincidence-gated one (§C6(d′)), recurs in the same bin on at least $m$ of the ten shots of a point, so a single foreign shot never passes. Background is treated in the sunlight bullet below.",
    r"   - The mean number of foreign shots per point is $\bar k=n\,p_1$ (Eq. (127)): 0.0125–0.0667 for today's 3–16 units and 0.0417–0.125 for the later 10–30 ($3\times4.17\times10^{-3}=0.0125$, $16\times4.17\times10^{-3}=0.0667$, $10\times4.17\times10^{-3}=0.0417$ and $30\times4.17\times10^{-3}=0.125$). The bins are $\Delta t_{\rm bin}=0.333$ ns wide (the 5 cm bins of §C9), each shot's histogram spans $T_{\rm w}=2$ µs (the round trip to 300 m, $T_{\rm w}/\Delta t_{\rm bin}=6{,}000$ bins), and dither spreads a foreign shot over $T_{\rm dith}=0.6$ µs ($T_{\rm dith}/\Delta t_{\rm bin}=1{,}800$ bins, §C9). Returns are taken to fall in one bin; a pulse spread over several bins widens the effective coincidence window, and the ghost rates below grow in proportion.",
    r"   - Shots from one foreign unit arrive together. A §C6-class unit fires one 20.8 µs column of ten shots at my footprint per 50 ms frame (a *visit*). A visit overlaps a given point with probability $2\times20.8\ \mu{\rm s}/50\ {\rm ms}=8.3\times10^{-4}$, and its offset from my point's window is then uniform, so it puts $k=0$ to 10 of its shots into the point: over the 20 equally likely offsets of one shot period each, all 10 once, 1 to 9 twice each and none once. That is 5 shots on average, which reproduces $p_1=8.3\times10^{-4}\times5=4.2\times10^{-3}$, and the number of pairs $\binom{k}{2}$ averages $(2\sum_{k=2}^{9}\binom{k}{2}+\binom{10}{2})/20=(240+45)/20=14.25$, i.e. $q_2=14.25/5=2.85$ pairs per foreign shot. A unit with my shot period puts its shots at the same offset in each of my shots apart from the dither, so a pair shares a bin with probability $\Delta t_{\rm bin}/T_{\rm dith}=1/1{,}800$; a unit with another shot period spreads its shots further and coincides no more often.",
    r"   - Shots from two different units are independent. A point holds $\binom{n}{2}p_1^2\approx\bar k^2/2$ such pairs on average, and each shares a bin with probability $\Delta t_{\rm bin}/T_{\rm w}=1/6{,}000$; this slightly overstates them, since the rule also needs the two on different shots. Under the 2-of-10 rule the ghost probability per point is therefore",
    r"",
    r"     $$p_{\rm ghost}\approx q_2\,\bar k\,\frac{\Delta t_{\rm bin}}{T_{\rm dith}}+\frac{\bar k^{2}}{2}\,\frac{\Delta t_{\rm bin}}{T_{\rm w}} \tag{128}$$",
    r"",
    r"   - The first term dominates. Today it is $2.85\times0.0125/1{,}800=2.0\times10^{-5}$ to $2.85\times0.0667/1{,}800=1.06\times10^{-4}$, against at most $0.0667^2/2/6{,}000=3.7\times10^{-7}$ for the second; later it is $6.6\times10^{-5}$ to $2.85\times0.125/1{,}800=2.0\times10^{-4}$, against at most $0.125^2/2/6{,}000=1.3\times10^{-6}$. A simulation of $10^{7}$ dithered visits gives the same $14.25/1{,}800=0.79\%$ ghost chance per overlapping visit [E].",
    r"   - A 1.25 Mpt frame (2,400 × 520 points at 20 fps, §C6) therefore carries about 25–130 random ghosts today ($2.0\times10^{-5}\times1.25\times10^{6}=25$ to $1.06\times10^{-4}\times1.25\times10^{6}=132$) and about 80–250 later ($6.6\times10^{-5}\times1.25\times10^{6}=83$ to $2.0\times10^{-4}\times1.25\times10^{6}=250$), i.e. about 500–2,600 and 1,700–5,000 per second at 20 frames per second. At night that is up to a fifth of the $10^{-3}$ false points per point that the detection rule of §C0 subsection 10.3 allows ($2.0\times10^{-4}/10^{-3}=0.2$): tolerable, but not negligible. The traffic factor $F=0.0625$–0.54 of item 2 scales all of these down in proportion.",
    r"   - A 3-of-10 rule makes them negligible. Three shots of one visit must then share a bin, with probability $(\Delta t_{\rm bin}/T_{\rm dith})^2=1/1{,}800^2$ per triple, and the number of triples $\binom{k}{3}$ averages $(2\sum_{k=3}^{9}\binom{k}{3}+\binom{10}{3})/20=(420+120)/20=27$ per overlapping visit, i.e. $q_3=27/5=5.4$ per foreign shot. So $p\approx q_3\,\bar k/1{,}800^2$, at most $5.4\times0.125/(3.24\times10^{6})=2.1\times10^{-7}$ per point: 0.26 ghosts per frame ($2.1\times10^{-7}\times1.25\times10^{6}$), or about 5 per second. The rule costs a weak far return little, since a 200 m, 10% return gives 2.1–3.3 detected photons per shot (§C6(c)) and so registers on most of its ten shots.",
    r"   - These rates assume that background never supplies a recurrence, as at night. In bright sun it can: the rate and live fraction of §C0 subsection 10.3 put $1.83\times10^{8}\ {\rm s^{-1}}\times0.333\ {\rm ns}\times0.885=0.054$ background counts into a bin per shot, so a lone foreign burst would find a count in its bin on one of the other nine shots with probability $1-e^{-9\times0.054}=0.39$. A per-shot event must then need two or more counts, which background supplies with probability $1-e^{-0.054}(1+0.054)=1.4\times10^{-3}$ per shot. Under 3-of-10 that adds $\binom{9}{2}(1.4\times10^{-3})^2\,\bar k=7.1\times10^{-5}\,\bar k$ for lone bursts and $8\times1.4\times10^{-3}=1.1\%$ of the visit term for visit pairs, together $1.1\times10^{-5}$ per point at $\bar k=0.125$ (14 per frame), while a 200 m, 10% return of 2.1–3.3 photons per shot (§C6(c)) still clears two counts on three or more of its ten shots in over 99% of points, if it falls in one bin. Under 2-of-10 the same test leaks $9\times1.4\times10^{-3}\,\bar k=1.6\times10^{-3}$ per point at $\bar k=0.125$, above the false-point budget, and a three-count test that avoids this loses up to 9% of those weak returns. In bright sun, then, the 3-of-10 rule is the one that works.",
    r"   - Without dither, every pair of a visit shares a bin. The $8.3\times10^{-4}\times0.85=7.1\times10^{-4}$ of points per foreign unit that receive two or more of its shots then all become ghosts, where 0.85 ($17/20$) is the share of overlapping visits that put at least two shots into the point. That is $n\times7.1\times10^{-4}$, i.e. 0.2–1.1% of points for today's 3–16 units and 0.7–2.1% for the later 10–30, the identical-unit failure of §C9.",
    r"   - Published post-rejection false-alarm rates, from $10^{-5}$ (Hwang & Lee, a preset value) to $1.1\times10^{-3}$ (Liang et al., with 200 interferers), both from simulations of other receivers, span the 2-of-10 rate derived here and lie at or above the 3-of-10 rate ($2\times10^{-7}$ at night, $1\times10^{-5}$ in bright sun). They are not a test of this model.",
])
add(10, "report #1, report #3, report #4, consistency flag #5", old10, new10,
    "Counts foreign shots; 2-of-10 rule with kbar = n p1; 0.333 ns bins; 1.25 Mpt frames; ghosts per frame and per "
    "second for 3–16 and 10–30 units; adds the one-unit visit term that the §C9 dither example implies.")

# ---------------------------------------------------------------- C9a, item 5
old11 = block(5751, 5753, "5. **Direct view: §C9's ≈10⁻³ of points per frame")
new11 = "\n".join([
    r"5. **Direct view: the measurements fit the localized case of the §C9 chain.**",
    r"   - Popko found direct interference 10–100× more frequent than scattered in coplanar 2-D scanners, but only at scan angles that view the other scanner or lie at most ≈2.5° beyond its angular extent; face to face, 90% of the direct events fell inside the other scanner's angular extent. Popko attributes the spread to beam divergence and the receiver's field of view [P, thesis §7.2]. That is the localized case of §C9, not stray light across the whole field.",
    r"   - Robinson 2025 found 98–652 interference points per cloud with two MEMS units face to face at 1–3 m. A §C6-class pair at that spacing would lose up to about 500–1,500 points per crossing in the localized case, the same order: the interferer's column then takes $1+25\ {\rm mm}/(8.73\times10^{-4}\times3\ {\rm m})=10.5$ to $1+25\ {\rm mm}/(8.73\times10^{-4}\times1\ {\rm m})=29.6$ column periods to cross a 25 mm aperture, and $50\times10.5=525$, $50\times29.6=1{,}480$.",
    r"   - Neither measured a 3-D one-axis unit at road distance, where the chain gives at most $1.7\times10^{-6}$ of points per frame in the localized case and $4\times10^{-4}$ to $8\times10^{-4}$ if stray light reaches the whole active column.",
])
add(11, "report #2 (§C9a item 5)", old11, new11,
    "Restates item 5 from the §C9 chain and Popko's source (localized direct coupling, thesis §7.2).")

# ---------------------------------------------------------------- C9a, GB/T
old12 = block(5796, 5796, "  - It is a direct-view test only:")
new12 = (r"  - It is a direct-view test only: no scattered paths, multiple interferers or synchronized-unit case. For direct "
         r"view, though, it is not a lenient bar [E]. At its 0.5–2 m spacing the interferer's 0.05° column takes at least "
         r"$1+25\ {\rm mm}/(8.73\times10^{-4}\times2\ {\rm m})=15$ to $1+25\ {\rm mm}/(8.73\times10^{-4}\times0.5\ {\rm m})=58$ "
         r"column periods to cross a 25 mm aperture, against one or two at road distance (§C9). A §C6-class unit without "
         r"dither or coding, whose foreign bursts then build consistent peaks, would put false points into "
         r"$520\times15/(1.25\times10^{6})=0.6\%$ to $520\times58/(1.25\times10^{6})=2.4\%$ of its points in every frame "
         r"if stray light reaches its whole active column, and fail the ≤0.1% limit. If the light stays within about 2.5° "
         r"(50 pixels), at most $50\times15/(1.25\times10^{6})=0.06\%$ to $50\times58/(1.25\times10^{6})=0.23\%$ are hit, "
         r"and only in frames where the two scans meet: near the limit, which such a unit can exceed at 1 m "
         r"($50\times29.6/(1.25\times10^{6})=0.12\%$) and 0.5 m. At road distance even the column-wide case stays below "
         r"the limit, at $4\times10^{-4}$ to $8\times10^{-4}$ (§C9).")
add(12, "report #2 (GB/T comparison)", old12, new12,
    "Says whether an unmitigated unit passes ≤0.1%, from the §C9 chain at the test's 0.5–2 m spacing.")

# ---------------------------------------------------------------- C9a, net effect
old13 = block(5807, 5809, "- Post-rejection random ghosts are rare")
new13 = "\n".join([
    r"- Post-rejection random ghosts become negligible with dither plus a consistency test that needs a peak on three of the ten shots (at most $1.1\times10^{-5}$ of points in bright sun and dense, fully overlapping traffic); a two-of-ten test is marginal.",
    lines[5807],   # residual-risks line, unchanged
    r"- The Chinese national test checks only one of these, direct view by a same-model unit at 0.5–2 m, which column-wide stray light would fail.",
])
assert lines[5807].startswith("- The residual risks are synchronized identical units")
add(13, "report #1, report #2 (conclusions)", old13, new13,
    "Keeps the net-effect bullets true to the rebuilt item 3 and the GB/T analysis.")

# ---------------------------------------------------------------- C9a, sources
add(14, "report #7 (source)",
    "https://doi.org/10.14372/IEMEK.2017.12.1.43 ;",
    "https://doi.org/10.14372/IEMEK.2017.12.1.43 ; "
    "https://www.sick.com/media/pdf/1/41/941/dataSheet_LMS511-10100-PRO_1046135_en.pdf ;",
    "Source for the LMS511 working range and divergence cited in item 1.")

# ---------------------------------------------------------------- checks
spans = []
for e in edits:
    k = text.count(e["old"])
    assert k == 1, (e["id"], k)
    a = text.index(e["old"])
    assert sec0 <= a < sec1, e["id"]
    spans.append((a, a + len(e["old"]), e["id"]))
spans.sort()
for (a0, a1, i0), (b0, b1, i1) in zip(spans, spans[1:]):
    assert b0 >= a1, (i0, i1)

skipped = [
    {"finding": "report #1 (model form, for the author)", "kind": "needs_decision",
     "location": "§C9a, Check item 3, Eq. (128)",
     "detail": ("Eq. (128) as decided, (kbar^2/2)(Dt_bin/T_w) with kbar = n p1, treats foreign shots as independent. "
                "A C6-class unit, however, lights a footprint with one 20.8 us column of ten shots per 50 ms frame "
                "(the 200 shots/s of §C9 are 10 x 20), and §C9's own dither example ('about five foreign shots overlap "
                "one point ... C(5,2)/1800') uses that structure. The edit therefore writes Eq. (128) with two terms: "
                "q2 kbar Dt_bin/T_dith (pairs within one unit's visit, q2 = 2.85, T_dith/Dt_bin = 1,800) plus "
                "(kbar^2/2) Dt_bin/T_w (pairs from two units). The first dominates by 150-1,500x: 25-130 ghosts per "
                "1.25 Mpt frame today, 80-250 later, under 2-of-10; 0.03-0.26 per frame under 3-of-10. A Monte Carlo "
                "of 1e7 visits reproduces 0.79% per overlapping visit (R2F_C9_interference_model.py). A further bullet "
                "adds what the decided model leaves out in sunlight: background can supply a recurrence (0.054 counts "
                "per 0.333 ns bin per shot at the bright-sun rate of §C0 10.3), so a two-count per-shot test is needed; "
                "with it 3-of-10 gives 1.1e-5 per point at kbar = 0.125 while 2-of-10 leaks 1.6e-3, above the 1e-3 "
                "false-point budget. Item 3's heading ('3-of-10 makes them negligible by day and night; 2-of-10 is "
                "marginal'), the C9 consistency-test sentence (m >= 3) and the net-effect bullet follow from these. If "
                "the author prefers the independent-shot form only, drop the visit and sunlight bullets and the first "
                "term; the decided form then gives 1.3e-8-3.7e-7 per point today and 1.4e-7-1.3e-6 later, i.e. "
                "0.016-0.46 and 0.18-1.6 ghosts per frame (0.3-9 and 3.6-33 per second), and item 3's heading can stay "
                "'random ghosts are rare'.")},
    {"finding": "report #9 (in-band share)", "kind": "needs_source",
     "location": "§C9a, Check item 2, 'In-band share f_band ... 0.5–0.9'",
     "detail": ("The 905 nm / 940 nm split of Chinese installations (2025 or H1 2026) would replace the assumed "
                "0.5–0.9; §C2 gives only the 1,550 nm share (about 6% in 2025, 4–5% in H1 2026).")},
    {"finding": "report #1 (cross-section)", "kind": "cross_section",
     "location": "§0 executive summary, item 5 interference bullet: 'now ships and makes random ghosts rare.'",
     "detail": ("Exact text: 'Randomized firing (jittered pulse timing, so that foreign pulses do not line up from shot "
                "to shot) now ships and makes random ghosts rare.' Proposed: 'Randomized firing (jittered pulse timing, "
                "so that foreign pulses do not line up from shot to shot) now ships. Combined with a test that a peak "
                "recurs on three of a point's ten shots, it makes random ghosts negligible by day and night; a "
                "two-of-ten test is marginal in dense traffic (§C9a).'")},
    {"finding": "report #7, report #2 (cross-section, sources)", "kind": "cross_section",
     "location": "Appendix 2, group 'Chip-size limits, interference and fusion (§C8, §C9, §E10)'",
     "detail": ("Add after the SPIE 11005 entry: '- Kim, Eom, Choi & Park, \"Mutual interference on mobile pulsed "
                "scanning LIDAR\", IEMEK J. Embed. Sys. Appl. 12(1), 43–62 (2017), Tables 1, 3 and 4: "
                "https://doi.org/10.14372/IEMEK.2017.12.1.43' ; '- SICK LMS511-10100 PRO data sheet (190° field, "
                "0.2–80 m working range, 11.9 mrad): https://www.sick.com/media/pdf/1/41/941/dataSheet_LMS511-10100-PRO_1046135_en.pdf' ; "
                "'- Popko, \"Signal interactions between lidar scanners\", PhD thesis, Georgia Tech (2019), Table 8 and "
                "§7.2: http://hdl.handle.net/1853/62690'.")},
]

OUT.write_text(json.dumps({"block": "R2F_C9", "edits": edits, "skipped": skipped}, ensure_ascii=False, indent=1),
               encoding="utf-8")
print(f"wrote {OUT.name}: {len(edits)} edits, {len(skipped)} skipped")
