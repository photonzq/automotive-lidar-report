"""§C4c subsection 1a: what the makers' own documents say about a stopped scanner, why slowing down matters far less
than stopping at 1,550 nm, and which stage of a fibre laser the safeguard has to cut. Also the Velodyne and Luminar
rows of the subsection's first table, the safeguard list, the Sources line, the Appendix 1 item and the Appendix 2
group.

Sources, each read at source (pages rendered and read; printed page numbers):
- Velodyne: VLP-16 User Manual 63-9243 Rev D (2018), p. 70 (a speed of 0 "will auto-disable the sensor's lasers") and
  p. 82 ("…the lasers are turned off, as leaving them on with the motor stopped would be an unsafe eye state"; 1-299
  rpm revert to 300); Rev F (2022, marked draft), p. 3 (firmware 3.0.38.0 "IMPROVED: Eye safety laser cutoff time"),
  p. 55 (lasers fire "based on time, not azimuth"), p. 89 (same sentence as Rev D p. 82); HDL-64E S2 manual, firmware
  4.07 (2012), p. 6 (lockout circuit until "approximately 300 RPMs"); HDL-64E S3 Rev J (2017), p. 4 (label "CLASS 1M
  LASER PRODUCT"), p. 8 (lockout until "a preset operational RPM"), p. 53 ("Class 1 - eye safe").
- Ouster: OS1 Hardware User Manual for Rev C sensors (25 Jul 2022), p. 6 (boot with the laser disabled, then spinning,
  then the laser activated; "a multi-layer series of internal safety interlocks"); firmware 4.0 documentation, "Sensor
  States" (ERROR: "Motor and laser output are disabled") and "Alerts and Errors" (0x01000064 "Unit failed to maintain
  target spin rate", Sensor Action "No Action").
- Hesai: OT128 User Manual O01-en-261010, pp. 51-52 (lidar states incl. "Shutdown or Output Untrusted", 5 ms rolling
  counter, Safety Manual via technical support), p. 66 (trigger method), p. 67 (standby); AT128P User Manual
  A02-en-261110, p. 6 (Class 1), p. 63 (standby); Pandar128E3X p. 50 and QT128C2X p. 48 (same lidar states).
- Livox: SDK Communication Protocol V1.3.0 (26 Oct 2020), section 3.5.1 (motor_status 2 "Unable to Work" triggers
  system_status 2, which "Causes the LiDAR to Shut Down and Enter the Error State"); Mid Series User Manual v1.2 (Aug
  2019), p. 17 (standby: "the laser beams are not active"; error: all components but communication powered off).
- RoboSense: RS-Bpearl User Manual rev 2.0.1 (2020, distributor's copy), p. 28 (1,200/600/300 rpm; any other value
  sets the motor speed to 0).
- SICK: LMS5xx Operating Instructions 8013796/ZM63/2017-05-09 (SICK's file in the Internet Archive), p. 12 ("Do not
  open the housing (opening the housing will not switch off the laser)"), p. 98 (IDLE: "the laser is switched off";
  "Motor starts": no error).
- Luminar: US 11,119,198 B2, col. 2, ll. 23-27, col. 41, ll. 38-59, col. 42, ll. 25-41; US 10,451,716 B2, col. 47,
  ll. 6-38; US 9,874,635 B1, col. 13, l. 63 to col. 14, l. 7, and col. 36, ll. 33-40. MicroVision's IRIS data sheet
  (2026-06): Class 1 per IEC/EN 60825-1:2014 at 1550 nm.
- IMRA America: US 7,505,196 B2, col. 2, ll. 27-39, and claims 16-18 (pump-diode current shut off or reduced when the
  seed's repetition rate falls below a threshold or its amplitude leaves a safe range).
The slowdown numbers are checked by slowdown_check.py in this folder.

Usage: makers_manuals_edit.py <report.md> <expected sha256 prefix> [--write]
"""
import hashlib
import sys
from pathlib import Path

report, expected = Path(sys.argv[1]), sys.argv[2]
raw = report.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
assert sha.startswith(expected), f"report changed: sha {sha[:12]} != {expected}"
text = raw.decode("utf-8")
assert "\r" not in text

VLP16_D = "https://web.archive.org/web/20180929163636id_/https://velodynelidar.com/docs/manuals/63-9243%20REV%20D%20MANUAL,USERS,VLP-16.pdf"
VLP16_F = "https://data.ouster.io/downloads/velodyne/user-manual/vlp-16-user-manual-revf.pdf"
HDL64_S2 = ("https://web.archive.org/web/20150910071407id_/http://velodynelidar.com/docs/manuals/"
            "63-HDL64ES2h%20HDL-64E%20S2%20CD%20Users%20Manual.pdf")
HDL64_S3 = ("https://web.archive.org/web/20170329150835id_/http://velodynelidar.com:80/docs/manuals/"
            "63-HDL64ES3%20REV%20J%20MANUAL,USERS%20AND%20PROGRAM%20GUIDE,HDL-64E%20S3.pdf")
OUSTER_HW = "https://data.ouster.io/downloads/hardware-user-manual/hardware-user-manual-revd-os1.pdf"
OUSTER_STATES = "https://docs.ouster.com/sensor-docs/firmware/sensor-states"
OUSTER_ALERTS = "https://docs.ouster.com/sensor-docs/firmware/alerts-and-errors"
HESAI_OT128 = "https://www.hesaitech.com/wp-content/uploads/2026/10/OT128_User_Manual_O01-en-261010.pdf"
HESAI_AT128P = "https://www.hesaitech.com/wp-content/uploads/2026/11/AT128P_User_Manual_A02-en-261110.pdf"
LIVOX_SDK = "https://github.com/Livox-SDK/Livox-SDK/wiki/Livox-SDK-Communication-Protocol"
LIVOX_MID = ("https://www.livoxtech.com/3296f540ecf5458a8829e01cf429798e/downloads/20190827/"
             "Livox%20Mid%20Series%20User%20Manual%20v1.2%2020190827.pdf")
RS_BPEARL = "https://www.generationrobots.com/media/Robosense_Bpearl_User_Guide.pdf"
SICK_LMS5 = ("https://web.archive.org/web/20220617014208id_/https://www.sick.com/media/docs/4/14/514/"
             "Operating_instructions_LMS5xx_LASER_MEASUREMENT_SENSORS_en_IM0037514.PDF")
LUM_198 = "https://patents.google.com/patent/US11119198B2/en"
LUM_716 = "https://patents.google.com/patent/US10451716B2/en"
IMRA_196 = "https://patents.google.com/patent/US7505196B2/en"
IRIS_DS = ("https://cdn.microvision.com/resources/persistent/c2e60a8d9ae946038d7ea051298919b7b5bce81e/"
           "IRIS_Datasheet.pdf")

# ---- 1. the Velodyne and Luminar rows of the first table
VELODYNE_ROW = (
    "| Velodyne spinning lidars | 905 nm, ≈2 mW per beam | Class 1 \"because the two milliwatt beams are scanning "
    "continually, so they would sweep across a person's eye in about a millisecond\" [T, quoting Velodyne] | ≈2 times, "
    "if the whole beam enters the 7 mm aperture | Laser Focus World, 25 Sep 2019 |\n")
VELODYNE_ROW_NEW = (
    "| Velodyne spinning lidars | 905 nm, ≈2 mW per beam | Class 1 \"because the two milliwatt beams are scanning "
    "continually, so they would sweep across a person's eye in about a millisecond\" [T, quoting Velodyne]. Its "
    "manuals turn the lasers off when the motor is set to stop, \"as leaving them on with the motor stopped would be "
    "an unsafe eye state\" [P] | ≈2 times, if the whole beam enters the 7 mm aperture | Laser Focus World, 25 Sep "
    "2019; VLP-16 manual (2018), p. 82 |\n")
LUMINAR_ROW_END = (
    "a receiver failure, and a person or object within a threshold distance of the head [P] | 1 µJ at 640 kHz is "
    "0.64 W, ≈67 times | US 9,874,635 B1 |\n")
LUMINAR_ROW_END_NEW = (
    "a receiver failure, and a person or object within a threshold distance of the head [P]. A later patent runs \"a "
    "laser that is not eye-safe under all operating conditions\" in a way that makes the lidar eye-safe [P]. Iris, the "
    "product, is rated Class 1 under IEC 60825-1:2014 [P] | 1 µJ at 640 kHz is 0.64 W, ≈67 times | US 9,874,635 B1; "
    "US 11,119,198 B2, col. 2; Iris data sheet (MicroVision, 2026) |\n")

# ---- 2. the makers' manuals, after the first table's reading note
READ_NOTE = ("How to read the table. A survey scanner is a tripod-mounted instrument that maps buildings and terrain. "
             "A patent shows a design its owner protected, not necessarily the product it ships. Class 3R allows up "
             "to five times the Class 1 limit and calls for care with direct viewing.\n")
MANUALS_BLOCK = (
    "\n"
    "**What the makers' manuals say about a stopped scanner** [P unless tagged]. The user manuals and interface "
    "documents of six makers, in editions from 2011 to 2026, were read for a stall safeguard: lasers held off until "
    "the scanner is at speed, a cut when it stops or slows, a speed threshold, a fault code, or a response time.\n"
    "\n"
    "| Maker and documents | What they say about the scanner and the laser | Stall safeguard described |\n"
    "|---|---|---|\n"
    "| Velodyne: VLP-16 manual, Rev D (2018) and Rev F (2022), with the same text in the VLP-32C, HDL-32E and VLS-128 "
    "manuals; HDL-64E S2 (2012) and S3 (2017) manuals | The HDL-64E has \"a lockout circuit that prevents its lasers "
    "from firing until it achieves approximately 300 RPMs\" (S2, p. 6). On the VLP-16, a speed setting of 0 stops the "
    "motor and \"the lasers are turned off, as leaving them on with the motor stopped would be an unsafe eye state\"; "
    "settings of 1–299 rpm revert to 300 (Rev D, p. 82). Firmware 3.0.38.0 lists \"IMPROVED: Eye safety laser cutoff "
    "time\" without saying what triggers the cut-off (Rev F, p. 3). The lasers fire \"based on time, not azimuth\" "
    "(Rev F, p. 55). The HDL-64E S3's label reads \"Class 1M\" and its specification \"Class 1\" (S3, pp. 4 and 53) | "
    "A start-up lockout and a commanded stop; a cut-off named in the firmware notes, not described |\n"
    "| Ouster: OS0, OS1 and OS2 hardware manuals (Rev C sensors, 2022); firmware 4.0 documentation | The laser stays "
    "disabled through a boot of about 60 s, after which the optics start spinning and the laser is activated; the "
    "sensors \"are equipped with a multi-layer series of internal safety interlocks to ensure compliance to Class 1 "
    "Laser Eye Safe limits\", which are not described (OS1 manual, p. 6). In the latched error state \"Motor and laser "
    "output are disabled\", while the alert \"Unit failed to maintain target spin rate\" lists \"No Action\" (firmware "
    "4.0, \"Sensor States\" and \"Alerts and Errors\") | Interlocks named, not described |\n"
    "| Hesai: 12 user manuals, 2022–2026: spinning OT128, Pandar64, Pandar128E3X, QT128C2X, JT128, XT32M2X, PandarXT "
    "and PandarQT; mirror-scanned AT128P, AT128E2X and ATX; flash FTX_140 | Class 1 is stated without conditions "
    "(AT128P, p. 6). In standby \"the motor stops running and lasers stop firing\" (OT128, p. 67). The OT128, "
    "Pandar128E3X and QT128C2X report a lidar state every 5 ms, among them \"Shutdown or Output Untrusted\"; the "
    "states and fault codes are described in a Safety Manual for which the user manuals refer to Hesai's technical "
    "support (OT128, pp. 51–52). The OT128 fires its lasers by angle, \"every 0.1° at 10 Hz\", or by time, \"every "
    "27.778 µs\" (p. 66) | Not in the user manuals |\n"
    "| Livox: Mid-40/100, Mid-70, Horizon, Tele-15, Avia, HAP and Mid-360 manuals (2019–2024); SDK communication "
    "protocol V1.3.0 (2020) | A motor in its error state (\"Unable to Work\") raises a system error, which \"Causes the "
    "LiDAR to Shut Down and Enter the Error State\" (protocol, section 3.5.1); in that state all components except the "
    "communication module are powered off, and in standby \"the laser beams are not active\" (Mid Series manual, "
    "p. 17) | A shutdown on a motor error, with no threshold or timing |\n"
    "| RoboSense: Bpearl (2020), Ruby, M1 (2021) and M1P (2022) manuals, distributors' copies | The Bpearl accepts "
    "1,200, 600 or 300 rpm and sets the motor speed to 0 for any other value, without saying what the lasers do "
    "(p. 28) | No |\n"
    "| SICK: LMS5xx operating instructions (2011, 2015 and 2017 editions); LMS1xx, TiM and MRS1000 manuals | \"Do not "
    "open the housing (opening the housing will not switch off the laser)\" (LMS5xx, 2017, p. 12). The display states "
    "include \"Motor starts\", a normal state, and IDLE, in which \"the laser is switched off\"; no code reports a stall "
    "(p. 98) | No |\n"
    "\n"
    "How to read this table. Velodyne's VLP-16 manual is the only one that says outright that the lasers must not run "
    "with the motor stopped. Velodyne's HDL-64E and Ouster document the start-up order, and Livox a shutdown on a "
    "motor error, but no manual says at what speed a running scanner's laser is cut, how fast, or whether the cut is "
    "made in hardware. Those details sit in documents users do not see: Hesai's Safety Manual, the test reports behind "
    "the IEC classification, and the product reports filed with FDA [E].\n"
    "\n"
    "**What Luminar's later patents add** [P].\n"
    "- **The dependence, stated outright.** US 11,119,198 B2 (priority 2017) describes a lidar that \"operates a laser "
    "that is not eye-safe under all operating conditions in a manner that prevents prolonged exposure of a human eye "
    "to the laser, and thereby renders the lidar system eye-safe\" (col. 2, ll. 23–27), through scan rates of "
    "20–60,000°/s and fewer than 10 lines per degree (col. 41, ll. 38–59). Its claimed safeguard stops the light, or "
    "cuts the pulse energy below 0.1 µJ, when a person is closer than a threshold distance (col. 42, ll. 25–41).\n"
    "- **A speed monitor that does not cut the laser.** US 10,451,716 B2 (priority 2017) reads the polygon's speed with "
    "an optical encoder at 160 revolutions per second. Jitter of more than 3 µs per quarter turn means the unit "
    "\"needs to be taken in for repair or replacement immediately\", with autonomous features suspended and an alert "
    "raised (col. 47, ll. 6–38); the text does not switch the laser off for it.\n"
    "- **Which stage the interlock cuts.** US 9,874,635 B1 sends its interlock to the laser module as a whole (table "
    "above) and does not say which stage it cuts, how fast, or how a scanner failure is detected. The only stage it "
    "names is the pump, switched off \"to avoid possible damage to the amplifier\" when too little seed light reaches "
    "it (col. 36, ll. 33–40).\n")

# ---- 3. slowing down against stopping, after the last stall-time bullet
BUDGET_TO_SAFEGUARD = (
    r"- **The budget therefore scales as $1/(\eta P)$** (Figure C4c.1): a few hundred milliseconds at 905 nm, 10–80 ms "
    r"for 1,550 nm pulsed lidars, and a few milliseconds for FMCW." + "\n\n**What the safeguard has to cover**")
SLOWDOWN_BLOCK = (
    "\n"
    r"**Slowing down matters far less than stopping** [E]. The US rule covers any failure that changes the scan's "
    r"speed, but at 1,550 nm a slower scan delivers no more energy until it has almost stopped. For exposures up to "
    r"0.35 s the limit is a fixed energy, 7.85 mJ through the 1 mm aperture, however it is delivered. With the "
    r"symbols above, each pass delivers at most $E_{\rm pass}=\eta P\,t_{\rm pass}=\eta P\,(D_{\rm a}+d_{\rm b})/"
    r"(\omega R)$, where $P$ is the beam's average power and $\eta$ the fraction of it inside the aperture when the "
    r"beam is centred on it; multiplying that fraction by the whole overlap time makes this an upper bound." + "\n"
    r"- **Down to 18 rad/s nothing changes.** While a 0.35 s window holds at least one pass, that is for "
    r"$\omega\ge2\pi/(0.35\ {\rm s})=18$ rad/s, it holds about $0.35\ {\rm s}\times\omega/2\pi$ passes, which together "
    r"deliver $0.35\ {\rm s}\times\eta P\,(D_{\rm a}+d_{\rm b})/(2\pi R)$. The speed cancels: slower passes deliver "
    r"more each, but fewer of them fall in the window. The limits for longer exposures depend on the average power "
    r"entering the aperture, which does not depend on the speed either. A beam that meets the limits at full speed "
    r"therefore still meets them down to 18 rad/s, 29% of a 10 Hz head's 62.8 rad/s." + "\n"
    r"- **Below that, a single pass sets the limit.** A window then holds one pass, which reaches 7.85 mJ once the "
    r"head has slowed to $\omega_{\rm trip}=\eta P\,(D_{\rm a}+d_{\rm b})/(R\times7.85\ {\rm mJ})$." + "\n"
    r"- **Luminar's example.** With 0.64 W in a 3 mm beam ($\eta=0.20$, $D_{\rm a}+d_{\rm b}=4$ mm, $R=100$ mm), "
    r"$\omega_{\rm trip}=0.20\times0.64\ {\rm W}\times4\ {\rm mm}/(100\ {\rm mm}\times7.85\ {\rm mJ})=0.65$ rad/s, "
    r"1.0% of full speed; with the whole beam in the aperture ($\eta=1$, $D_{\rm a}+d_{\rm b}\approx2$ mm) it is "
    r"1.6 rad/s, 2.6%. At full speed a 0.35 s window collects $0.35\ {\rm s}\times0.20\times0.64\ {\rm W}\times4\ "
    r"{\rm mm}/(2\pi\times100\ {\rm mm})=0.29$ mJ, 27 times below the limit, or 0.71 mJ, 11 times below, with the "
    r"whole beam." + "\n"
    r'- **So the trigger can be "nearly stopped".** A speed monitor with any sensible threshold trips long before '
    r"the exposure grows; what the design must get right is the time to act once the scan has stopped, "
    r"$t_{\rm stall}$ above." + "\n")
BUDGET_TO_SAFEGUARD_NEW = BUDGET_TO_SAFEGUARD.replace(
    "\n\n**What the safeguard has to cover**", "\n" + SLOWDOWN_BLOCK + "\n**What the safeguard has to cover**")

# ---- 4. the safeguard list
DETECT_END = ("Luminar's patent adds a receiver failure and an object close to the head as triggers [P].\n")
DETECT_END_NEW = (
    "Luminar's patent adds a receiver failure and an object close to the head as triggers [P]. Luminar's polygon "
    "patent reads the mirror's speed with an optical encoder [P, US 10,451,716 B2]. A head that fires on encoder angle "
    "stops firing when the angle stops advancing, but one that fires on a timer, as the VLP-16 does, keeps firing "
    "unless something cuts it [E]; Hesai's OT128 offers both [P].\n")
ACTING_END = "which is the case Lumentum makes for a hardware shutdown path [P].\n"
ACTING_END_NEW = (
    "which is the case Lumentum makes for a hardware shutdown path [P].\n"
    "- **Cutting the right stage** [E unless tagged]. In a fibre MOPA (a seed laser followed by an erbium fibre "
    "amplifier, §C4), stopping the seed pulses does not stop the light: a pumped amplifier without a seed keeps "
    "emitting amplified spontaneous emission through the same optics, and its gain builds up until stray feedback can "
    "make it pulse on its own. The safeguard therefore has to remove the pump current. Amplifier designs already "
    "include such a cut for their own protection. IMRA America's patent on pulsed fibre amplifiers shuts off or "
    "reduces the pump-diode current when the seed's repetition rate falls below a threshold or the seed pulses' "
    "amplitude leaves a safe range, against \"gain buildup in excess of the damage threshold\" [P, US 7,505,196 B2, "
    "col. 2, ll. 27–39, and claims 16–18], and Luminar's interlock patent switches its pump off when too little seed "
    "light reaches the amplifier [P, US 9,874,635 B1, col. 36, ll. 33–40]. A stall signal can drive the same path.\n")
STARTING = ("- **Starting and stopping.** The laser must not fire before the scanner is at speed and must stop as it "
            "coasts down, since the tests cover start-up and shut-down [P, 21 CFR 1040.10(e)(2)(i)].\n")
STARTING_NEW = STARTING.replace(
    "[P, 21 CFR 1040.10(e)(2)(i)].\n",
    "[P, 21 CFR 1040.10(e)(2)(i)]. Velodyne's HDL-64E keeps its lasers off until the head turns at about 300 rpm, and "
    "Ouster's sensors start spinning before the laser is activated [P, manuals above].\n")

# ---- 5. the subsection's Sources line
SOURCES_END = " ; https://patents.google.com/patent/US9874635B1/en ; https://patents.google.com/patent/US11757533B2/en\n"
SOURCES_END_NEW = (" ; https://patents.google.com/patent/US9874635B1/en ; https://patents.google.com/patent/US11757533B2/en"
                   " ; " + " ; ".join([VLP16_D, HDL64_S2, OUSTER_HW, HESAI_OT128, LIVOX_SDK, SICK_LMS5, LUM_198,
                                       LUM_716, IMRA_196]) + "\n")

# ---- 6. Appendix 1
APPX1_OLD = (
    "- **Scan-dependent Class 1 (§C4c subsection 1a).** No lidar maker publishes how fast its scan-failure safeguard "
    "acts, what it monitors, or the class its product would have with the scan stopped, and certification reports are "
    "not public. Whether the ratings of Hesai's, Ouster's and Livox's scanning units depend on the scan is not stated "
    "in the documents found. The stall times of subsection 1a assume a Gaussian beam of 3 mm, or the whole beam in the "
    "aperture, and use the 1 mm aperture of the standard for exposures under 0.35 s.\n")
APPX1_NEW = (
    "- **Scan-dependent Class 1 (§C4c subsection 1a).** No lidar maker publishes at what speed its scan-failure "
    "safeguard cuts the laser, how fast it acts, whether it works in hardware, or the class its product would have "
    "with the scan stopped. The user manuals of Velodyne, Ouster, Hesai, Livox, RoboSense and SICK do not say; Hesai's "
    "fault codes are in a Safety Manual for which its user manuals refer to technical support, and the test reports "
    "and the product reports filed with FDA are not public. What Velodyne's \"eye safety laser cutoff\" (VLP-16 "
    "firmware 3.0.38.0) responds to is not stated, and the HDL-64E S3's label (Class 1M) and specification (Class 1) "
    "disagree. Whether the ratings of Hesai's, Ouster's and Livox's scanning units depend on the scan is not stated "
    "either. The stall times and the slowdown estimate of subsection 1a assume a Gaussian beam of 3 mm, or the whole "
    "beam in the aperture, use the 1 mm aperture of the standard for exposures under 0.35 s, and take the energy per "
    "pass as an upper bound.\n")

# ---- 7. Appendix 2
APPX2_LUMINAR = ("- Luminar, US 9,874,635 B1 (interlock line, scanner failure, pulse parameters): "
                 "https://patents.google.com/patent/US9874635B1/en\n")
APPX2_LUMINAR_NEW = ("- Luminar, US 9,874,635 B1 (interlock line and scanner failure, col. 13, l. 63 to col. 14, l. 7; pump "
                     "switched off when too little seed light reaches the amplifier, col. 36, ll. 33–40; pulse "
                     "parameters): https://patents.google.com/patent/US9874635B1/en\n")
APPX2_LAST = ("- Lumentum, US 11,757,533 B2 (hardware shutdown when a diffuser or cover fails): "
              "https://patents.google.com/patent/US11757533B2/en\n")
APPX2_ADD = (
    f"- Luminar, US 11,119,198 B2 (a laser not eye-safe under all operating conditions, made eye-safe by the scan, "
    f"col. 2, ll. 23–27, and col. 41, ll. 38–59; shutdown when a person is near, col. 42, ll. 25–41): {LUM_198}\n"
    f"- Luminar, US 10,451,716 B2 (polygon speed read by an optical encoder; jitter thresholds leading to repair and "
    f"an alert, col. 47, ll. 6–38): {LUM_716}\n"
    f"- MicroVision, IRIS data sheet (2026-06; Class 1 per IEC/EN 60825-1:2014, 1,550 nm): {IRIS_DS}\n"
    f"- IMRA America, US 7,505,196 B2 (pump-diode current shut off or reduced when the seed's repetition rate falls "
    f"below a threshold or its amplitude leaves a safe range, col. 2, ll. 27–39, and claims 16–18): {IMRA_196}\n"
    f"- Velodyne, VLP-16 User Manual 63-9243 Rev D (2018; p. 70, a speed of 0 disables the lasers; p. 82, \"unsafe eye "
    f"state\"), the maker's file in the Internet Archive: {VLP16_D}\n"
    f"- Velodyne, VLP-16 User Manual 63-9243 Rev F (2022, marked draft; p. 3, firmware 3.0.38.0 eye-safety laser "
    f"cut-off; p. 55, firing by time; p. 89, \"unsafe eye state\"): {VLP16_F}\n"
    f"- Velodyne, HDL-64E S2 and S2.1 User's Manual, firmware 4.07 (2012; p. 6, lockout circuit until about 300 rpm), "
    f"the maker's file in the Internet Archive: {HDL64_S2}\n"
    f"- Velodyne, HDL-64E S3 User's Manual Rev J (2017; p. 4, label \"Class 1M\"; p. 8, lockout circuit; p. 53, "
    f"\"Class 1\"), the maker's file in the Internet Archive: {HDL64_S3}\n"
    f"- Ouster, OS1 Hardware User Manual for Rev C sensors (25 Jul 2022; p. 6, start-up order and safety interlocks): "
    f"{OUSTER_HW}\n"
    f"- Ouster, sensor documentation for firmware 4.0, \"Sensor States\" (error state: motor and laser output disabled) "
    f"and \"Alerts and Errors\" (0x01000064, no action): {OUSTER_STATES} ; {OUSTER_ALERTS}\n"
    f"- Hesai, OT128 User Manual O01-en-261010 (pp. 51–52, lidar states and Safety Manual; p. 66, trigger method; "
    f"p. 67, standby): {HESAI_OT128}\n"
    f"- Hesai, AT128P User Manual A02-en-261110 (p. 6, Class 1; p. 63, standby): {HESAI_AT128P}\n"
    f"- Livox, SDK Communication Protocol V1.3.0 (26 Oct 2020; section 3.5.1, motor error, system error and "
    f"shutdown): {LIVOX_SDK}\n"
    f"- Livox, Mid Series User Manual v1.2 (Aug 2019; p. 17, working states): {LIVOX_MID}\n"
    f"- RoboSense, RS-Bpearl User Manual rev 2.0.1 (2020; p. 28, motor speed register), a distributor's copy: "
    f"{RS_BPEARL}\n"
    f"- SICK, LMS5xx Operating Instructions 8013796/ZM63/2017-05-09 (p. 12, housing; p. 98, display states), SICK's "
    f"file in the Internet Archive: {SICK_LMS5}\n")

EDITS = [
    (VELODYNE_ROW, VELODYNE_ROW_NEW),
    (LUMINAR_ROW_END, LUMINAR_ROW_END_NEW),
    (READ_NOTE, READ_NOTE + MANUALS_BLOCK),
    (BUDGET_TO_SAFEGUARD, BUDGET_TO_SAFEGUARD_NEW),
    (DETECT_END, DETECT_END_NEW),
    (ACTING_END, ACTING_END_NEW),
    (STARTING, STARTING_NEW),
    (SOURCES_END, SOURCES_END_NEW),
    (APPX1_OLD, APPX1_NEW),
    (APPX2_LUMINAR, APPX2_LUMINAR_NEW),
    (APPX2_LAST, APPX2_LAST + APPX2_ADD),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
assert "\r" not in new
print(f"{len(EDITS)} edits; sha256 before {sha[:12]}, after {hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
