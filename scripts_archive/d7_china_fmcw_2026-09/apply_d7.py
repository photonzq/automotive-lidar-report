"""Update section D7 (Chinese FMCW): RoboSense/SUSTech papers, long-range Chinese demonstrations, new firms, news."""
import hashlib
import re
import sys
from pathlib import Path

REPORT = Path(r"<report folder>\automotive_perception_report_2026-09-27.md")
SCR = Path(r"<scratch>")
SNAP = SCR / "rewrite" / "report_after_c0_10_8.md"
OUT_SNAP = SCR / "rewrite" / "report_after_d7.md"
DRY = "--dry" in sys.argv

raw = REPORT.read_bytes()
assert hashlib.sha256(raw).digest() == hashlib.sha256(SNAP.read_bytes()).digest(), "report changed since the snapshot"
s = raw.decode("utf-8")
a = s.index("## D7. Chinese FMCW and coherent lidar")
b = s.index("\n## ", a + 10)
d7 = s[a:b]

E = []  # (old, new)
# --- verdict 2: one system test meets the automotive criterion
E.append(("   - Chinese groups publish top-journal results on parallel FMCW (many simultaneous FMCW channels) and chaos lidar (ranging with a noise-like chaotic laser waveform instead of a chirp).\n",
          "   - Chinese groups publish top-journal results on parallel FMCW (many simultaneous FMCW channels) and chaos lidar (ranging with a noise-like chaotic laser waveform instead of a chirp).\n"
          "   - **One system test meets the automotive criterion.** SUSTech with RoboSense ranged a 10% board outdoors to 200 m with a silicon-photonic receiver engine (2025). The other long-range Chinese demonstrations either used mirror-folded paths and 90% targets (to 109 m) or do not state their target (Academic highlights, below).\n"))
# --- company rows
E.append(("Skywell fleet fitment; Hyundai Mobis PoC aiming at 2027 production. Silicon photonics at **Tower** (Israel). The \"custom SoC\" matches **indie Semiconductor's iND83301** (US) | [NT] |",
          "Skywell fleet fitment; Hyundai Mobis PoC aiming at 2027 production. Silicon photonics at **Tower** (Israel). The \"custom SoC\" matches **indie Semiconductor's iND83301** (US). Media report proof-of-concept work with two domestic OEMs and one international OEM (Aug 2025) [T]; a Jan 2026 release claims more than 500 m of \"perception\" for Lark without a reflectivity [P, claim]; FR60 was shown at CES 2026 at 110° × 60°, 100 m and under 15 W [T] | [NT] |"))
E.append(("Raptor uses an \"internationally leading\" III-V/Si platform (foundry unnamed) | [NT] |",
          "Raptor uses an \"internationally leading\" III-V/Si platform (foundry unnamed). B1 first close with Beijing Electronics Holding's photonics fund (Jan 2025) [T]; F-series shown at CIOE 2026 [P] | [NT] |"))
E.append(("| **光勺, 映讯芯光, 镭神 LeiShen (FMCW fibre lidar page, no specs)** | — | Stale or unverified | [NT/U] |",
          "| **光勺, 映讯芯光, 镭神 LeiShen (FMCW fibre lidar page, no specs)** | — | Stale or unverified. 映讯芯光 raised a Pre-A round of about ¥100 M led by Shenzhen Capital Group (Jan 2026) [T] | [NT/U] |\n"
          "| **镭智传感, 灵动芯光, 璇光半导体** (smaller firms) | 镭智传感 (Suzhou, 2018; founder from CAS SINANO): FMCW coherent lidar and narrow-linewidth lasers; Everbright Photonics (长光华芯) holds 31.47% [P, its H1 2025 report]. 灵动芯光 (Shenzhen, 2022; Tsinghua holds an IP stake): FMCW light source in development. 璇光半导体 (Suzhou): FMCW with MEMS mirrors | 镭智: co-author of a 5 kHz external-cavity laser for FMCW (2022). 灵动: Angel++ round of tens of millions of yuan (Apr 2026), mainly for optical interconnect. 璇光: a 2022 round, no later news [T] | [R/NT] |"))
E.append(("\"FMCW products depend on suppliers; whether the underlying technology is mature decides whether the product is\" | No FMCW in any SEC filing | [R] |",
          "\"FMCW products depend on suppliers; whether the underlying technology is mature decides whether the product is\" | No FMCW in any SEC filing. A May 2026 driving-dataset paper with four Hesai co-authors uses a forward-facing 4D FMCW lidar whose vendor is not named: a hint of an in-house unit, not evidence [U] | [R] |"))
E.append(("| **RoboSense** | US patent 12025739B1 (SiPh multi-transceiver FMCW; CEO a co-inventor) | No FMCW in its 2024 annual report. The widely repeated \"RoboSense expects FMCW in 2027–28\" was not found in primary sources | [R] |",
          "| **RoboSense** | US patents 12025739B1 (SiPh multi-transceiver FMCW; CEO a co-inventor), 12196887B1 (Jan 2025) and 12276851B2 (Apr 2025). **Published FMCW hardware with SUSTech:** a three-channel dual-polarization receiver (*Opt. Laser Technol.*, Apr 2025), a 7.56 ns on-chip delay line (*JLT*, 2025) and a four-channel engine that ranged a 10% board to 200 m (*Moore and More*, 2025; Academic highlights) | No FMCW in its 2024 interim or 2025 annual report, and its April 2026 launch was a SPAD-SoC ToF unit. The widely repeated \"RoboSense expects FMCW in 2027–28\" was not found in primary sources | [R] |"))
# --- academic highlights
E.append(("All are lab demonstrations; reported target distances are metre-scale. A *microcomb*",
          "All are research results, in two groups. The first table lists the long-range ranging demonstrations. Only one of them, SUSTech with RoboSense, meets the automotive criterion of a 10% target outdoors at 200 m; the others used mirror-folded paths and 90% targets, or do not state their target. The second table lists sources, combs and short-range demonstrations, whose targets are metre-scale. A 2024 review by IMECAS in 红外与激光工程 tabulates further Chinese OPA-FMCW demonstrations.\n\n"
          "*Long-range ranging demonstrations.*\n\n"
          "| Group | Paper | Range and target | Hardware |\n"
          "|---|---|---|---|\n"
          "| SUSTech (王静) with RoboSense | *Moore and More* 2:12 (2025) | 200 m on a 1.5 m, 10% board outdoors, SNR ≥ 10 dB on all four channels | 130 nm SiPh chip (2.8 × 2.7 mm, hermetic package): four dual-polarization coherent receivers (1.09 A/W Ge photodiodes) and an on-chip 40 cm (5.74 ns) delay line for chirp calibration. External 100 kHz DFB laser, EDFA (power not given), 7 mm collimated beam. §C0 subsection 10.8 finds its fall with range 3–4 dB gentler than the beam model |\n"
          "| RoboSense with SUSTech (王静 et al.) | *Opt. Laser Technol.* 182:112131 (2025) | Beyond 180 m on all three channels (target not verified) | Three-channel dual-polarization balanced receiver, 130 nm SiPh |\n"
          "| Jilin Univ. (宋俊峰) with Peng Cheng Lab | *Photonics Res.* 9:2511 (2021) | 100 m on a 90% scatter plate; beyond 50 m a silver mirror folded the path | 128-channel SiN-on-Si OPA transmitter (26 dBm in; 4 × 3 mm aperture); fibre-collimator receiver; AMF foundry |\n"
          "| Jilin Univ. with CIOMP | *Opt. Express* 30:5008 (2022) | 109 m on a 90% reflector, over a mirror-folded path. A 10% target gave SNR 8.4 dB at 32 dBm into the chip; the 49° edge beam reached 82 m | 64-channel 2-D OPA plus a bulk lens (36 m without it); AMF foundry |\n"
          "| CAS Inst. of Semiconductors (潘教青) | *Opt. Express* 30:28112 (2022) | Echo from 100 m (target and power not verified) | 512-channel Si₃N₄ OPA, 3.16 × 20.5 mm aperture |\n"
          "| SIMIT (武爱民) | *Results Phys.* 57:107327 (2024); SPIE 12757 (2023) | 120 m (journal) and 160 m (SPIE), 0.3 m precision (target not verified) | Coherent receiver chip on 3 µm SOI; transmit power not found |\n"
          "| SiFotonics (希烽光电; US headquarters, Chinese operations) | OFC 2024, paper M4J.1 | 81.9 m (target not given) | Four-channel dual-polarization receiver module, better than −80 dBm sensitivity |\n\n"
          "*Sources, combs and short-range demonstrations.* A *microcomb*"))
E.append(("| SJTU (周林杰) | III-V/Si–SiN external-cavity FMCW source; 256-channel OPA | Device results |",
          "| SJTU (周林杰) | III-V/Si–SiN external-cavity FMCW source (*Laser Photonics Rev.* 2024); 256-channel OPA | Device results: 4.2 cm precision \"at 200 m\" (free space or fibre not stated); the OPA system's 50 m range was emulated with delay fibre |\n"
          "| Tsinghua (陈明华) | *APL Photonics* 9:021302 (2024) and 10:041305 (2025) | III-V/Si₃N₄ external-cavity lasers with 6–9 Hz intrinsic linewidth, as FMCW sources |\n"
          "| Tsinghua (薛晓晓) | *Photonics Res.* 13:31 (2025); *Opt. Lett.* 50:2538 (2025) | Self-injection-locked laser with a 100 GHz sweep; its metre-to-kilometre ranges are fibre-emulated \"equivalent\" distances |\n"
          "| CAS SINANO with 镭智传感 | *IEEE PTL* 34:1123 (2022) | 5 kHz external-cavity laser; SNR above 35 dB through 156 m of delay fibre (≈110 m equivalent) |"))
# --- judgement
E.append(("Hesai and RoboSense already hold FMCW patents and in-house programmes.",
          "Hesai and RoboSense already hold FMCW patents and in-house programmes; RoboSense's is visible in its papers with SUSTech, including the 200 m, 10% system test of 2025."))

for old, new in E:
    c = d7.count(old)
    assert c == 1, (old[:80], c)
    d7 = d7.replace(old, new)

NEW_SOURCES = (
    " ; https://doi.org/10.1007/s44275-025-00030-7 (Wang et al., SUSTech and RoboSense, 2025)"
    " ; https://doi.org/10.1016/j.optlastec.2024.112131 (Wang et al., RoboSense, three-channel receiver, 2025)"
    " ; https://opg.optica.org/jlt/abstract.cfm?uri=jlt-43-15-7016 (RoboSense on-chip delay line, JLT 2025)"
    " ; https://patents.google.com/patent/US12196887B1/en ; https://patents.google.com/patent/US12276851B2/en (RoboSense patents)"
    " ; https://www.researching.cn/ArticlePdf/m00072/2021/9/12/12002511.pdf (Li et al., Jilin, Photonics Res. 2021)"
    " ; http://ir.ciomp.ac.cn/bitstream/181722/67202/1/Two-dimensional%20multi-layered%20SiN-on-SOI%20optical%20phased%20array%20with%20wide-scanning%20and%20long-distance%20ranging.pdf (Zhang et al., Jilin and CIOMP, Opt. Express 2022)"
    " ; https://doi.org/10.1364/OE.464358 (Yu et al., CAS Institute of Semiconductors, 2022)"
    " ; https://doi.org/10.1016/j.rinp.2024.107327 ; https://doi.org/10.1117/12.2690403 (Xu et al., SIMIT)"
    " ; https://opg.optica.org/abstract.cfm?uri=OFC-2024-M4J.1 (Liu et al., SiFotonics, OFC 2024)"
    " ; https://researching.cn/ArticlePdf/m00018/2024/53/8/20240239.pdf (IMECAS review, 红外与激光工程 2024)"
    " ; https://doi.org/10.1002/lpor.202300882 (SJTU, LPR 2024)"
    " ; https://pubs.aip.org/aip/app/article/9/2/021302/3265980/ ; https://pubs.aip.org/aip/app/article/10/4/041305/3344446/ (Tsinghua lasers)"
    " ; https://opg.optica.org/ol/abstract.cfm?uri=ol-50-8-2538 (Tsinghua, Opt. Lett. 2025)"
    " ; https://doi.org/10.1109/LPT.2022.3203063 (SINANO and 镭智传感, PTL 2022)"
    " ; https://arxiv.org/html/2605.18074 (dataset paper with Hesai co-authors)"
    " ; https://www.roboticstomorrow.com/news/2026/01/27/lightic-technologies-announces-new-fmcw-lidar-with-exceptional-cost-and-power-efficiency-for-automotive-and-robotic-applications/26068/ (LightIC, Jan 2026)"
    " ; https://news.qq.com/rain/a/20250807A06CMU00 (LightIC OEM work) ; https://www.eefocus.com/article/1944295.html (LightIC FR60 at CES 2026)"
    " ; https://m.pedaily.cn/news/545068 (LuminWave B1) ; https://exhibitors.cioe.cn/jtycn/cp12914.html (LuminWave at CIOE 2026)"
    " ; https://pub-zhtb.hizh.cn/s/202601/05/AP695b7b03e4b0a0fbdabf1d80.html (映讯芯光 Pre-A)"
    " ; http://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESH_STOCK/2025/2025-8/2025-08-23/11340417.PDF (长光华芯 H1 2025 report, 镭智传感 stake)"
    " ; https://m.chinaventure.com.cn/news/108-20260430-391198.html (灵动芯光) ; https://www.smartautoclub.com/p/36393/ (璇光半导体)"
    " ; https://www.caixinglobal.com/2026-04-24/robosense-unveils-more-accurate-lidar-102437519.html (RoboSense, Apr 2026)"
)
src_lines = [l for l in d7.split("\n") if l.startswith("Sources: ")]
assert len(src_lines) == 1, len(src_lines)
d7 = d7.replace(src_lines[0], src_lines[0].rstrip() + NEW_SOURCES)

s = s[:a] + d7 + s[b:]
tags = re.findall(r"\\tag\{(\d+)\}", s)
assert [int(t) for t in tags] == list(range(1, len(tags) + 1))
odd = [i for i, l in enumerate(s.split("\n"), 1) if l.replace("\\$", "").count("$") % 2]
assert not odd, odd[:5]
pipes = [i for i, l in enumerate(s.split("\n"), 1)
         if l.startswith("|") and any("|" in sp for sp in re.findall(r"\$([^$]+)\$", l.replace("\\$", "")))]
assert not pipes, pipes[:5]
print("tags", len(tags), "| bytes", len(s.encode("utf-8")), "(was", len(raw), ")")
if not DRY:
    REPORT.write_bytes(s.encode("utf-8"))
    OUT_SNAP.write_bytes(s.encode("utf-8"))
    print("written; snapshot", OUT_SNAP.name)
