"""New §B4b: Europe's robotaxis, shuttles and trucks, the laws and approvals that govern them, why Europe is later,
and what it means for lidar; cross-references in the reading guide, §0, §B4, Appendix 1 and Appendix 2.

Every legal statement was read in the instrument itself (EUR-Lex texts through the EU Publications Office
repository, UNECE documents, legislation.gov.uk, gesetze-im-internet.de, Légifrance copies, fedlex/ASTRA,
Narodne novine, gouvernement.lu) or in an official record (KBA lists and FAQ, the Bundestag research service, the
London Assembly, the Commission's "Have your say" records); every operator statement in the operator's own release,
except where tagged [T]. The research records are kept outside the repository.

The German counts (287 testing approvals, 114 at Level 4; 108 Level 4 and 109 Level 3 in force on 5 Nov 2026; 87
Level 4 in force without geographic restriction; holders) come from kba_testing_approvals_count.py, which reads the
KBA's list dated 05.11.2026.

Usage: europe_b4b_edit.py <report.md> <expected sha256 prefix> [--write]
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

U = {
    # EU and UNECE
    "gsr": "http://publications.europa.eu/resource/celex/32019R2144",
    "ta": "http://publications.europa.eu/resource/celex/02018R0858-20260802",
    "ads_ir": "http://publications.europa.eu/resource/celex/02022R1426-20260324",
    "avp_ir": "http://publications.europa.eu/resource/celex/32026R0481",
    "avp_da": "http://publications.europa.eu/resource/celex/32026R1188",
    "kba_eu": ("https://www.kba.de/EN/Themen_en/Typgenehmigung_en/Autonomes_automatisiertes_Fahren_en/"
               "EU_Typgenehmigung_en/eu_typgenehmigung_node_en.html"),
    "wp29_report": "https://documents.un.org/api/symbol/access?s=ECE/TRANS/WP.29/1192&l=en&t=pdf",
    "r185": "https://documents.un.org/api/symbol/access?s=ECE/TRANS/WP.29/2026/137&l=en&t=pdf",
    "gtr": "https://documents.un.org/api/symbol/access?s=ECE/TRANS/WP.29/2026/139&l=en&t=pdf",
    "depositary": "https://treaties.un.org/doc/Publication/CN/2026/CN.288.2026-Eng.pdf",
    "hys_18732": "https://ec.europa.eu/info/law/better-regulation/brpapi/groupInitiatives/18732",
    "hys_18133": "https://ec.europa.eu/info/law/better-regulation/brpapi/groupInitiatives/18133",
    "action_plan": "http://publications.europa.eu/resource/celex/52025DC0095",
    "jdi": ("https://transport.ec.europa.eu/document/download/e6e549b2-916d-4d12-9290-23e76528c49d_en?filename="
            "Joint_Decaration_of_Intent_EU_cross-border_testbed_for_the_deployment_of_automated_vehicles.pdf"),
    "council_testbed": "https://data.consilium.europa.eu/doc/document/ST-9848-2026-INIT/en/pdf",
    "adacities": ("https://digital-strategy.ec.europa.eu/en/news/autonomous-drive-ambition-cities-adacities-"
                  "initiative-bring-autonomous-driving-technology-cities"),
    "pld": "http://publications.europa.eu/resource/celex/32024L2853",
    "ai_act": "http://publications.europa.eu/resource/celex/02024R1689-20260727",
    "rdw": ("https://www.rdw.nl/en/news/2026/rdw-explanation-of-european-type-approval-tesla-with-provisional-"
            "validity-in-the-netherlands"),
    # national
    "stvg_1d": "https://www.gesetze-im-internet.de/stvg/__1d.html",
    "stvg_1e": "https://www.gesetze-im-internet.de/stvg/__1e.html",
    "stvg_1i": "https://www.gesetze-im-internet.de/stvg/__1i.html",
    "afgbv": "https://www.gesetze-im-internet.de/afgbv/BJNR098610022.html",
    "kba_national": ("https://www.kba.de/DE/Themen/Typgenehmigung/Autonomes_automatisiertes_Fahren/"
                     "nationale_Betriebserlaubnis/nationale_betriebserlaubnis_node.html"),
    "kba_list": ("https://www.kba.de/EN/Themen_en/Typgenehmigung_en/Autonomes_automatisiertes_Fahren_en/"
                 "Erprobungsgenehmigung_en/dl_liste_erprobungsgenehmigungen_en.pdf?__blob=publicationFile"),
    "kba_faq": ("https://www.kba.de/EN/Themen_en/Typgenehmigung_en/Autonomes_automatisiertes_Fahren_en/"
                "Erprobungsgenehmigung_en/erprobungsgenehmigung_node_en.html"),
    "bt_wd": "https://www.bundestag.de/resource/blob/1194930/WD-5-038-26-WD-7-022-26.pdf",
    "de_strategy": ("https://web.archive.org/web/20250119133631/https://bmdv.bund.de/SharedDocs/DE/Publikationen/DG/"
                    "die-zukunft-faehrt-autonom.pdf?__blob=publicationFile"),
    "ava": "https://www.legislation.gov.uk/ukpga/2024/10/enacted",
    "si_439": "https://www.legislation.gov.uk/uksi/2026/439/made",
    "dft_2025": ("https://www.gov.uk/government/news/driving-innovation-38000-jobs-on-the-horizon-as-pilots-of-self-"
                 "driving-vehicles-fast-tracked"),
    "ssp": "https://www.gov.uk/government/consultations/automated-vehicles-statement-of-safety-principles",
    "la_report": ("https://www.london.gov.uk/sites/default/files/2026-10/FINAL%20Who%27s%20driving%20the%20future%20"
                  "of%20autonomous%20transport%20in%20London.pdf"),
    "la_15": ("https://www.london.gov.uk/transport-committee-responds-tfl-approval-supervised-robocab-service-"
              "london"),
    "fr_ord": ("https://web.archive.org/web/20210417000058/https://www.legifrance.gouv.fr/jorf/id/"
               "JORFTEXT000043370894"),
    "fr_dec": ("https://web.archive.org/web/20210705012236/https://www.legifrance.gouv.fr/jorf/id/"
               "JORFTEXT000043729532"),
    "ch_vaf": "https://www.astra.admin.ch/dam/de/sd-web/2Nke1yzNHEb2/verordnung-automatisiertes-fahren.pdf",
    "es_dgt": ("https://www.dgt.es/muevete-con-seguridad/vehiculos-seguros/conduccion-automatizada/marco-pruebas-"
               "vehiculos-automatizados/"),
    "hr_law": "https://narodne-novine.nn.hr/clanci/sluzbeni/2024_12_145_2377.html",
    "hr_rules": "https://narodne-novine.nn.hr/clanci/sluzbeni/2024_12_154_2554.html",
    "lu_pony": ("https://gouvernement.lu/fr/actualites/agenda.gouvernement2024+fr+actualites+toutes_actualites+"
                "communiques+2025+04-avril+03-backes-conduite-autonome.html"),
    # operators
    "uber_wayve": "https://www.uber.com/gb/en/newsroom/wayve-on-uber/",
    "waymo_london": "https://waymo.com/blog/2026/09/visionforlondon/",
    "waymo_testing": "https://waymo.com/blog/shorts/autonomous-driving-in-london/",
    "lyft_baidu": "https://www.lyft.com/blog/posts/freenow-by-lyft-and-baidu-start-av-testing-in-london",
    "postauto": ("https://www.postauto.ch/de/ueber-uns-und-aktuelles/aktuelles/2026/meilenstein-fuer-automatisierte-"
                 "mobilitaet-in-der-schweiz"),
    "hesai_baidu": "https://www.hesaitech.com/?p=3291",
    "moia_hamburg": "https://www.moia.io/en/news/moia-launches-passenger-test-operation-in-hamburg",
    "moia_series": ("https://www.moia.io/en/news/moia-unveils-series-production-version-id-buzz-ad-and-turnkey-"
                    "solution-for-fully-autonomous-mobility-services"),
    "innoviz_vw": ("https://www.prnewswire.com/il/news-releases/innoviz-technologies-accelerates-delivery-of-newly-"
                   "designed-lidar-platform-to-volkswagen-autonomous-mobility-to-equip-a-fleet-of-id-buzz-ad-shuttles-"
                   "in-2025-302453790.html"),
    "mobileye_innoviz": ("https://prnewswire.com/il/news-releases/mobileye-to-use-innoviz-lidars-for-its-mobileye-"
                         "drive-av-platform-302328845.html"),
    "hochbahn": "https://www.hochbahn.de/en/projects/autonomous-bus-transport/autonomous-on-demand-shuttles",
    "uber_momenta": "https://www.uber.com/de/de/newsroom/uber-momenta-pilot/",
    "pony_zagreb": "https://www.aap.com.au/aapreleases/cision20260408ae29472",
    "uber_zagreb": ("https://investor.uber.com/news-events/news/press-release-details/2026/Uber-Launches-Autonomous-"
                    "Rides-in-Europe/default.aspx"),
    "pony_verne_driverless": ("https://www.prnewswire.com/news-releases/ponyai-and-verne-kick-off-fully-driverless-"
                              "robotaxi-test-rides-in-zagreb-302874840.html"),
    "afp_zagreb": "https://www.thestar.com.my/tech/tech-news/2026/10/14/croatia-trials-full-driverless-robotaxi-service",
    "hesai_pony": "https://hesaitech.com/?p=7711",
    "stellantis_bolt": ("https://www.media.stellantis.com/em-en/corporate/press/bolt-pony-ai-and-stellantis-to-launch-"
                        "autonomous-mobility-testing-program-in-luxembourg"),
    "zh_furttal": ("https://www.zh.ch/de/news-uebersicht/medienmitteilungen/2026/09/im-furttal-startet-der-"
                   "passagierbetrieb-mit-selbstfahrenden-fahrzeugen.html"),
    "zrh_airport": ("https://newsroom.flughafen-zuerich.ch/en/zurich-airport-automated-shuttle-buses-now-operate-"
                    "without-a-safety-driver-on-board/"),
    "weride_valence": ("https://ir.weride.ai/news-releases/news-release-details/weride-makes-first-european-fully-"
                       "driverless-commercial-robobus"),
    "weride_madrid": ("https://ir.weride.ai/news-releases/news-release-details/weride-uber-and-avomo-receive-spains-"
                      "first-national-operating"),
    "robosense_weride": ("https://en.prnasia.com/releases/global/robosense-empowers-weride-s-next-gen-robotaxi-gxr-"
                         "with-thousand-beam-level-digital-lidar-2-000-factory-installed-units-slated-for-global-"
                         "deployment-524593.shtml"),
    "karsan": "https://www.karsan.com/en/press/current-news/autonomous-e-atak-europes-first-driverless-tunnel-bus",
    "electrive_stavanger": ("https://www.electrive.com/2026/05/04/autonomous-bus-without-safety-driver-hits-road-in-"
                            "norway/"),
    "wayve_series_d": "https://wayve.ai/press/series-d/",
    "waymo_16b": "https://waymo.com/blog/2026/02/waymo-raises-usd16-billion-investment-round/",
    # freight
    "einride_lidl": "https://www.einride.tech/press/3361628",
    "schwarz": "https://gruppe.schwarz/content/story-autonome-filialbelieferung",
    "einride_q3": "https://www.einride.tech/press/3405471",
    "atlas": "https://www.aisec.fraunhofer.de/en/media/press-releases/2025/ATLAS-L4-conclusion.html",
    "man_2024": ("https://press.mantruckandbus.com/corporate/download/ff3d7ad5-07f5-4552-a9d8-3865424c2e73/240418-"
                 "mtb-pi-truck-automation-fahrt-bm-dr-volker-wissing.pdf"),
    "scania": "https://www.scania.com/group/en/home/innovation/autonomous-solutions/hub-to-hub.html",
    "traton_plus": ("https://traton.com/en/newsroom/press-releases/traton-group-and-plusai-expand-global-partnership-"
                    "to-accelerate-autonomous-truck-on-highway-commercialization.html"),
    "iveco_plus": ("https://www.financialcontent.com/article/gnwcq-2026-1-12-iveco-and-plusai-launch-new-level-4-"
                   "autonomous-driving-programme-in-spain"),
    "volvo_bronnoy": ("https://www.volvogroup.com/en/news-and-media/news/2025/may/volvo-achieves-milestone-with-over-"
                      "1-million-tonnes-hauled-autonomously-at-bronnoy-kalk.html"),
    "volvo_3mt": "https://mb.cision.com/Main/39/4400034/4284937.pdf",
    "fernride": ("https://hhla.de/en/media/news/detail-view/hhla-tk-estonia-fernride-begins-transition-to-driverless-"
                 "operations"),
    "felixstowe_2025": "https://www.ajot.com/news/port-of-felixstowe-expands-autonomous-truck-fleet",
    "felixstowe_100": "https://www.ajot.com/news/port-of-felixstowe-expands-autonomous-truck-fleet-to-100-units",
    "hesai_westwell": ("https://www.hesaitech.com/hesai-and-westwell-partner-to-accelerate-global-expansion-in-"
                       "autonomous-driving-for-logistics/"),
}

SECTION = r"""## B4b. Europe: robotaxis, shuttles and trucks, and the rules that govern them

This section asks how far driverless passenger and freight vehicles have got in Europe (the EU, the UK, Switzerland and Norway), which legal instruments let them onto public roads, and why Europe is later than the US and China. It matters for lidar makers because Europe's carmakers and its approval rules decide whether a third large driverless market appears, and whose lidars it buys. §B4 counts the lidars on robotaxis and trucks outside China and §B4a covers China. Here each legal statement cites the article, section or page of the instrument itself, and each operator statement the operator's own release.

**Short answer.**
- **No robotaxi service in Europe runs without a person aboard yet.** On 22 Nov 2026 every robotaxi service open to riders, in London, Zagreb, the Canton of Zurich, Hamburg and Munich, carried a safety driver or operator [P]. Vehicles ran with nobody aboard only in narrower settings: two staff shuttles at Zurich Airport, invited test rides in Zagreb, one Lidl delivery route in Germany under a testing approval, and trucks on private ground: cab-less ones in the Port of Felixstowe and driverless ones in a Norwegian quarry [P].
- **The laws exist, but the approvals so far are for tests.** Germany has provided for driverless operation in approved areas since 2021, France since 2022 and Switzerland since 2025, and the UK has issued permits for automated passenger services since May 2026 [P]. Yet no vehicle in Germany held a Level 4 operating permit in Apr 2026 [I: the Bundestag's research service, citing the KBA], and no UK permit had been granted by Oct 2026 [I: London Assembly].
- **EU type approval of driverless vehicles is capped** at small series of 1,500 vehicles per type per year, except for automated valet parking since Jun 2026 [P]. The UN Regulation on automated driving systems adopted on 24 Jun 2026, which a Commission draft would apply in the EU from 1 Jan 2027, opens the way to unlimited series [P].
- **The driving systems are mostly bought abroad.** The systems on Europe's roads are Chinese (Pony.ai, WeRide, Baidu, Momenta), Mobileye's (Volkswagen's ID. Buzz AD and Holon's shuttle) or Waymo's; Wayve, the British exception, drives without lidar [P]. Europe's truck makers run their driverless programmes in the US (§B4).
- **Lidar:** Europe's driverless and test fleets carry roughly 1–2k lidars [E, subsection 5], mostly Innoviz units on Volkswagen's vans and Hesai or RoboSense units on Chinese systems.

### 1. The rules: what each instrument allows

A driverless vehicle needs two permissions in Europe: approval of the vehicle, and permission to operate it in a given place. Type approval, the certification that a vehicle type meets the rules before it is sold or registered, is harmonised in the EU and largely shared with the UK and Switzerland through UN regulations. Permission to operate stays national, and in practice local. The table lists the instruments in force on 22 Nov 2026.

| Jurisdiction | Instrument | What it allows | Main conditions | Status on 22 Nov 2026 |
|---|---|---|---|---|
| **EU** (vehicle approval) | Regulation (EU) 2019/2144, Art. 3(21)–(22) and Art. 11; Implementing Regulation (EU) 2022/1426, in force 15 Sep 2022; Regulation (EU) 2018/858, Annex V | EU type approval of the automated driving system (ADS) of fully automated M and N vehicles for three uses: passengers or goods in a predefined area, "hub-to-hub" on a predefined route, and automated valet parking (2022/1426, Art. 1) [P] | Small series only: at most 1,500 vehicles per type per year in the EU (2018/858, Annex V, Part A, point 1). The ADS must perform the whole driving task within its operational design domain (ODD), stop at no more than 4 m/s² in a minimal-risk manoeuvre, and be backed by an audited safety management system and in-service reporting (2022/1426, Annexes II–III); a remote intervention operator may not drive (Art. 2(25)) [P] | Unlimited series only for automated valet parking, since 22 Jun 2026 (Delegated Regulation (EU) 2026/1188). Member States still regulate operation on their roads (2022/1426, recital 7) [P] |
| **UNECE** (worldwide) | UN Regulation No 185 on ADS and a UN global technical regulation (GTR) on ADS, adopted on 24 Jun 2026 at WP.29's 199th session; Regulation 185 by 39 votes to none | Type approval of the ADS of M, N, L6 and L7 vehicles, including features with no fallback driver at all ("ADSF-2") (R185, paras. 1.1, 2.6.2) [P] | Safety "at least equivalent to that of a competent and careful human driver"; a safety management system, a safety case, in-service monitoring (R185, introduction) [P] | Adopted unless one-fifth of the contracting parties object within six months of the notice of 30 Jul 2026, so about end-Jan 2027 [P, UN depositary notice C.N.288.2026]. A Commission draft (feedback closed 6 Nov 2026) adds it to the General Safety Regulation from 1 Jan 2027 and lets makers choose it or 2022/1426 [P, initiative 18732] |
| **Germany** | Act on Autonomous Driving of 2021 (Road Traffic Act, StVG §§ 1d–1l, in force 28 Jul 2021); AFGBV ordinance (in force 1 Jul 2022) | Level 4 operation with no driver in a "defined operating area" of public road (StVG § 1d(1)–(2), § 1e) [P] | A KBA operating permit for the vehicle, or an EU type approval, plus approval of the area by the Land authority (§ 1e(1) Nos. 2–3; AFGBV § 7); a technical supervisor who can deactivate the vehicle and release manoeuvres from outside it (§ 1d(3), § 1f). National operating permits are capped at 250 vehicles per type per year [P, KBA]. Testing approvals (§ 1i with AFGBV § 16) are granted vehicle by vehicle, with the supervisor in sight of the vehicle [P, KBA] | No vehicle held a Level 4 operating permit on 27 Apr 2026 [I: Bundestag research service, citing the KBA]; 108 Level 4 testing approvals were in force on 5 Nov 2026 (below) [P/E] |
| **United Kingdom** | Automated Vehicles Act 2024 (Royal Assent 20 May 2024), Part 5 (ss. 82–90); Automated Vehicles (Permits for Automated Passenger Services) Regulations 2026, SI 2026/439, in force 15 May 2026 | Permits for automated passenger services (APS), taxi-, private-hire- or bus-like, for up to five years (s. 82; SI 2026/439, reg. 3) [P] | Granted nationally, through the Driver and Vehicle Standards Agency (DVSA), with the consent of each licensing authority and, in London, of Transport for London (TfL); six weeks of silence count as consent (ss. 85–86). The Act's full authorisation regime needs a statement of safety principles first (s. 2(10)), consulted on until 9 Sep 2026 [P] | No APS permit granted by Oct 2026, and TfL knew of no application on 14 Jul 2026 [I: London Assembly Transport Committee, pp. 12, 19]; the government expects the full Act from the second half of 2027 [P, DfT] |
| **France** | Ordonnance n° 2021-443; Décret n° 2021-873 | Automated road transport systems on predefined routes or zones, for public passenger services (Code des transports L. 3151-1; R. 3151-1) and for goods (L. 3251-1) [P] | A decision of the transport organising authority, a certified safety demonstration and periodic audits; remote intervention only by an authorised person licensed for the vehicle's category, with a training certificate (L. 3151-1, L. 3151-3; R. 3152-3) [P] | In force by 1 Sep 2022. WeRide's Robobus began a service at Valence TGV station on 10 Mar 2025, which WeRide describes as fully driverless [P, WeRide] |
| **Switzerland** | Ordinance on Automated Driving (VAF), in force 1 Mar 2025 | Driverless vehicles in operating areas approved by the canton; a motorway pilot in which drivers may let go of the wheel; automated parking (VAF, Arts. 2(c), 23(2), 25–32, 44) [P] | Each driverless vehicle supervised by an operator, who must work in Switzerland (Art. 34) [P] | Until 1 Mar 2028 applicants have no right to a decision on driverless operating areas (Art. 51). Meanwhile the Federal Roads Office (ASTRA) grants exemptions with safety drivers: WeRide's pilot in the Canton of Zurich (Nov 2025) and PostAuto's with Baidu in eastern Switzerland (Jun 2026) [P] |
| **Spain** | DGT Instruction VEH 2025/07, the ES-AV programme (Jun 2025) | Testing in three phases [P] | Phases 1–2: a safety operator aboard; phase 3: an operator aboard optional, a remote operator required [P, DGT] | Spain's first national L4 permit for passenger vehicles went to WeRide, Uber and AVOMO on 10 Sep 2026: 20 vehicles in Greater Madrid with an in-car specialist [P, WeRide] |
| **Croatia** | Road Traffic Safety Act amendment (Narodne novine 145/2024) and rulebook (NN 154/2024), Dec 2024 | Fully automated vehicles within an approved area; outside it, with the transport ministry's approval (Art. 281.b) [P] | Operators must act from within Croatia (Art. 281.c); while a service is tested, at least one remote operator per ten vehicles, or one operator in each vehicle (rulebook) [P] | Verne runs Pony.ai's robotaxis in Zagreb (subsection 2) |
| **Luxembourg** | An individual ministerial authorisation; no general regime yet | Supervised scientific trials [P] | Trained supervisors aboard and a "scientific trial" sign [P] | Pony.ai authorised in Lenningen from 28 Mar 2025, for one year [P] |

How to read the table. M vehicles carry passengers and N vehicles goods; L6 and L7 are light four-wheelers. An ADS is a system that performs the whole driving task, and its ODD is the set of conditions (roads, speeds, weather, times of day) in which it is designed to work. "Small series" is the EU's capped approval route; an approval in unlimited series has no annual cap. Level 4 is the SAE level at which no driver is needed inside the operating domain. The KBA is Germany's Federal Motor Transport Authority, and a technical supervisor (*Technische Aufsicht*) is the person, usually remote, whom the German law requires. A transport organising authority is the public body that runs local transport in France; ASTRA is Switzerland's Federal Roads Office, and the DGT Spain's traffic directorate.

**Germany's approvals in numbers.** The KBA publishes every testing approval it has granted under StVG § 1i with AFGBV § 16 [P]. Each approval covers one vehicle: the KBA requires a separate application for each vehicle [P, KBA testing FAQ]. On the list dated 5 Nov 2026:
- 287 approvals had been granted, 114 at Level 4 and 173 at Level 3; 108 of the Level 4 approvals and 109 of the Level 3 ones were still in force [P/E: counted from the list].
- Volkswagen held 55 of the Level 4 approvals in force, ZF 10, Holon and Deutsche Bahn's regional bus company 8 each, MAN 4, and Momenta, Motor AI and Munich's municipal utility 3 each; Einride held 1. Mercedes-Benz (51), Audi (36) and Wayve (12) held most of the Level 3 approvals [P/E].
- 87 of the Level 4 approvals in force carry no geographic restriction, which, by the KBA's footnote, makes them valid throughout Germany [P/E]. Momenta's of 8 Jul 2026 underlies its Munich pilot with Uber [P].
- The Bundestag's research service put the approved test vehicles at "about 250" in Apr 2026 and found that no company had yet moved a Level 4 pilot into regular operation [I, Wissenschaftliche Dienste WD 5-3000-038/26, pp. 22, 25]. The federal government's 2024 strategy had aimed to move autonomous driving "seamlessly" from testing into regular operation by 2026 [P, strategy, ch. 3].

**EU policy beyond approval.**
- **The Industrial Action Plan** (5 Mar 2025) promised at least three large-scale cross-border testbeds with regulatory sandboxes, approval in unlimited series for automated parking in 2025 and for "more use cases (e.g. hub-to-hub freight transport) in 2026", harmonised rules for testing on open roads, and a European Connected and Autonomous Vehicle Alliance [P, COM(2025) 95, pp. 2–3]. The alliance held its first forum on 23 Jun 2026 [P].
- **A declaration of 18 Member States** (8 Jun 2026) commits them to common technical requirements in a cross-border testbed, to "seek to facilitate mutual recognition" of approvals and to "ease commercial operations without a safety driver"; companies from outside the EU may join only in partnership with an EU company. It is not a treaty [P, Joint Declaration of Intent, Parts 1, 3 and 5]. The Connecting Europe Facility's 2026 programme sets aside €20 M for digital infrastructure for automated driving [P, Council note ST 9848/26].
- **ADACities** (23 Jun 2026), a Commission initiative, asks participating cities to target fleets of 100 or more autonomous vehicles each by 2030, through partnerships that are "EU-centric, with European OEMs and tech at the core" [P].
- **The Commission's drafts of Oct–Nov 2026** are the steps toward unlimited series: one adds UN Regulation 185 to the General Safety Regulation from 1 Jan 2027, another adapts the large-series safety rules (driver monitoring, speed assistance and similar) to vehicles that cannot be driven by hand [P, initiatives 18732 and 18133]. Neither had been adopted by 22 Nov 2026 [P].
- **Liability and AI rules.** Under the revised Product Liability Directive, software, AI systems included, is a product, for products placed on the market after 9 Dec 2026 [P, Directive (EU) 2024/2853, Arts. 2(1), 4(1)]. The AI Act treats AI safety components of vehicles as high-risk but applies its requirements through the vehicle-approval acts, from 2 Aug 2028 after a 2026 amendment [P, Regulation (EU) 2024/1689, Art. 6(1), Annex I Section B, Arts. 107 and 109; Regulation (EU) 2026/1744].
- **Supervised driver assistance moved faster.** The Dutch approval authority RDW approved Tesla's FSD (Supervised) on 10 Apr 2026, at first valid only in the Netherlands [P, RDW]; §B4 gives Tesla's count of nine EU countries by Oct 2026.

### 2. Passenger services and tests

The table lists the passenger services and tests running in Europe on 22 Nov 2026, with who is aboard, as the operators themselves describe them.

| Place | Operator and partners | What runs, since when | Who is aboard | Fleet | Vehicle and driving system | Lidar |
|---|---|---|---|---|---|---|
| **Zagreb** | Verne with Pony.ai and Uber | A paid public service since 8 Apr 2026, over about 90 km² including the airport, and on Uber's app since 19 Aug 2026; driverless test rides for invited passengers on a 22 km route since 10 Sep 2026 [P] | A licensed operator behind the wheel in the paid service [P]; nobody at the wheel in the test rides [P/T] | About 30 [T, AFP] | BAIC Arcfox Alpha T5 with Pony.ai's Gen-7 system [P] | Four Hesai AT128 per Gen-7 vehicle [P, Hesai] |
| **London** | Uber with Wayve | Supervised rides for Uber customers since 2 Sep 2026 [P] | A TfL-licensed driver [P] | Up to 15, approved by TfL for one year [I, London Assembly] | Ford Mustang Mach-E with the Wayve AI Driver [P] | None named: "surround cameras and radar" [P] |
| **London** | Waymo | Supervised testing since 14 Apr 2026; Waymo will apply for an APS permit [P] | Specialists [P] | Not disclosed | Jaguar I-PACE with the Waymo Driver [P] | Waymo's own (§B4) |
| **London** | Baidu Apollo Go with Lyft's Freenow, and with Uber | Testing in the borough of Brent since 28 Jul 2026; public riders from 2027 [P] | Safety operators [P] | Not disclosed | Apollo RT6 [P] | Four per RT6 [P, PostAuto]; Hesai is Baidu's exclusive long-range supplier [P] |
| **St. Gallen and Appenzell** | PostAuto ("AmiGo") with Baidu | Hands-free testing over about 80 km² since 1 Jun 2026, under an ASTRA exemption; regular service without safety drivers expected from 2027 [P] | Safety drivers [P] | Up to 25 from 2027 [P] | Apollo RT6 [P] | Four per vehicle [P] |
| **Canton of Zurich** (Furttal) | Swiss Transit Lab, SBB and the cantons, with WeRide | A public service since 28 Sep 2026, about 100 stops, at CHF 4.70 plus CHF 0.38 per km [P] | A safety person behind the wheel [P] | Up to 3 [P] | WeRide robotaxi [P] | Not disclosed for these cars |
| **Zurich Airport** | Zurich Airport with WeRide | A staff shuttle with no safety driver since early Sep 2026, monitored from a remote cockpit [P] | Nobody [P] | 2 [P] | WeRide Robobus [P] | Not disclosed |
| **Valence** (France) | beti with WeRide, Renault and Macif | A Robobus service on a 3.3 km route from the TGV station, from 10 Mar 2025; its status in 2026 is not published [P/U] | Nobody, by WeRide's description [P] | "Several" buses [P] | WeRide Robobus [P] | Not disclosed |
| **Madrid** | WeRide with Uber and AVOMO | A national L4 test permit since 10 Sep 2026; commercial service expected by end-2026 [P] | An in-car specialist [P] | 20 [P] | WeRide GXR [P] | RoboSense EM4 main and E1 blind-spot lidars on WeRide's newest GXR [P, RoboSense] |
| **Hamburg** | MOIA (Volkswagen), ALIKE project | Free rides for selected pre-registered residents since 15 Jul 2026 [P] | A trained safety operator [P] | Up to 10 [P] | ID. Buzz AD with Mobileye Drive [P] | Nine Innoviz per van [P] |
| **Hamburg** | HOCHBAHN with Holon, ALIKE project | Testing, with passenger rides planned [P] | A safety driver [P] | Not disclosed | Holon urban shuttle with Mobileye Drive [P] | Probably Innoviz, Mobileye Drive's lidar supplier [P/E]; count not disclosed |
| **Munich** | Uber with Momenta | Free rides for selected Uber users in northern Munich since 18 Nov 2026, under Momenta's KBA testing approvals [P] | A trained safety specialist [P] | Not disclosed | Not disclosed [P] | Not disclosed |
| **Luxembourg** | Pony.ai with Stellantis and Bolt | A pilot announced on 9 Jun 2026, aiming at "driverless readiness" by its end [P] | Not disclosed | Not disclosed | Stellantis midsize van with Pony.ai's Gen-7 [P] | Gen-7: four AT128 [P] |
| **Stavanger** (Norway) | Vy with Karsan and ADASTEC | A scheduled bus without a safety driver on parts of its route since about May 2026 [T] | Reports differ [T] | 1 [T] | Karsan e-ATAK [P] | "many LIDAR sensors" [P, Karsan] |

WeRide's robotaxis and Robobuses began road tests in Slovakia in Q3 2026, and Pony.ai is road-testing in Manchester [P]. The parcel van of Loxo and Planzer in Bern is in §B4a subsection 4.

How to read the table. A safety driver sits at the controls and can take over; a safety operator or specialist may sit elsewhere in the vehicle; a remote cockpit supervises vehicles from outside. Gen-7 is Pony.ai's seventh-generation driving system, and the AT128 Hesai's 128-channel automotive lidar. The RT6 is Baidu's sixth-generation robotaxi, and the ID. Buzz AD the driverless version of Volkswagen's electric van.

**What this shows** [E unless tagged]:
- **Scale.** The fleets with a published size add up to about 80 vehicles carrying passengers or in public trials: up to 15 in London (Wayve), about 30 in Zagreb, up to 10 in Hamburg (MOIA), up to 3 in the Furttal, 2 at Zurich Airport and 20 in Madrid ($15+30+10+3+2+20=80$). Germany's 108 Level 4 test vehicles are the largest pool [P/E]. Waymo runs about 4,000 driverless vehicles (§B4), and Pony.ai had 2,768 robotaxis worldwide on 30 Sep 2026 (§G1).
- **The systems are imported.** Pony.ai's system runs in Zagreb, Luxembourg and Manchester; WeRide's in the Furttal, at Zurich Airport, in Valence and in Madrid; Baidu's in London and eastern Switzerland; Momenta's in Munich; Mobileye's in Hamburg; and Waymo's in London. Wayve is the only European developer with a public service, and its cars carry no lidar [P].
- **The first rides with nobody aboard are on short, fixed routes:** two buses at Zurich Airport, the 3.3 km Valence route, Zagreb's 22 km invited rides and parts of Stavanger's bus route [P/T].

### 3. Freight: route-by-route tests on public roads, driverless operation on private ground

Europe's truck makers run their driverless programmes in Texas (§B4). In Europe, freight without a driver aboard runs on private ground, in ports and quarries, and on one public-road route.

| Operator | What runs in Europe | Who is aboard | Status and next step | Lidar |
|---|---|---|---|---|
| **Einride with Lidl** (Germany) | A cab-less electric truck with 15 pallet places, between Lidl's distribution centre in Edermünde (near Kassel) and a nearby store, up to three runs a day, from Sep 2026 [P] | Nobody; a local operator follows in a separate vehicle, at no more than 25 km/h in the pilot [P, Einride; Schwarz Group] | A Level 4 *testing* approval (StVG § 1i with AFGBV § 16), extended on 14 Sep 2026 to 28 Feb 2027 [P, KBA list]; a multi-stop route at another site is planned [P] | Not disclosed |
| **Einride** elsewhere | Four cab-less trucks on Lorenz Snacks' plant ground in Neunburg vorm Wald (Germany) [P] | Remote and local operators [P] | Permits without a safety driver in four countries and five US states; about 8,500 contracted driverless hours by 13 Nov 2026; highway autonomy targeted from H1 2028 [P, Q3 update] | Not disclosed |
| **MAN** (TRATON) | The ATLAS-L4 research project (Jan 2022–May 2025, €59.1 M, 12 partners): a truck drove at Level 4 on the A9 motorway north of Munich under a KBA testing approval from Apr 2024 [P] | A safety driver on every test drive [P, Fraunhofer AISEC] | Four Level 4 testing approvals in force in Nov 2026 [P, KBA list]; customer hub-to-hub projects promised "from 2025", and series readiness "towards the end of the decade" [P, MAN, Apr 2024] | Not disclosed |
| **Scania** (TRATON) with Plus | Hub-to-hub test trucks on Swedish motorways around Södertälje, under permits since 2021 [P] | A safety driver [P] | Safety drivers stay "until the system is able to handle all situations" [P]; TRATON's Jan 2026 agreement with Plus starts with US routes and prepares European markets [P] | Not disclosed |
| **IVECO** with Plus | Two S-Way trucks for the logistics firm Sesé on the ≈300 km Madrid–Zaragoza corridor, testing from 2026 [P] | A safety operator throughout the trial [P] | Plus targets factory-built trucks commercially in 2027 [P] | Not disclosed |
| **Volvo Autonomous Solutions** | Nine autonomous trucks haul limestone from quarry to crusher over 5 km of tunnels and grades at Brønnøy Kalk (Norway) [P] | No safety driver since 2023 [P] | More than 3 M t hauled at Volvo's European customer sites by Sep 2026 [P] | Not disclosed |
| **FERNRIDE** | Terminal tractors at HHLA's container terminal in Muuga (Estonia), moving to driverless operation from Jul 2025 [P] | No safety driver in the target state; a remote operator can take over [P] | TÜV SÜD certified its safety concept and system design under the EU Machinery Directive [P] | Not disclosed |
| **Westwell** at the Port of Felixstowe (UK) | Cab-less electric container trucks in mixed traffic at Trinity Terminal: 34 in service from early 2025, and a fleet of 100 after a third order in Jul 2026, with battery-swap stations [P] | No cab [P] | The largest European autonomous truck fleet found [E] | A 128-line lidar on each truck [P, port]; Hesai XT32 and AT128 on Westwell's trucks [P, Hesai] |

**What this shows** [E]:
- **On public roads, Europe's driverless freight is one route at 25 km/h** (Edermünde), run under a testing approval; everything else on public roads carries a safety driver. Europe's larger driverless fleets, Felixstowe's 100 trucks and Volvo's quarry trucks, run on private ground.
- **The largest driverless truck fleet in Europe runs a Chinese system on Chinese lidar** (Westwell, Hesai).
- **The unlimited-series approval for hub-to-hub freight** that the Commission promised "in 2026" depends on the drafts above, which had not been adopted by 22 Nov 2026 [P].

### 4. Why Europe is later

[E verdict; facts tagged]
1. **Approval routes are capped or granted vehicle by vehicle.** EU type approval of a driverless vehicle runs in small series of 1,500 per type per year, German national permits at 250 per type per year, and German testing approvals one vehicle at a time with a supervisor in sight [P]. A fleet the size of Waymo's 4,000 would need three EU small-series types to register in one year ($4{,}000/1{,}500\approx2.7$, rounded up). Unlimited series opens only when UN Regulation 185 applies in the EU, planned from 1 Jan 2027 [P].
2. **Permission to operate is national, then local.** Germany's Länder approve operating areas, UK licensing authorities and TfL must consent to each APS permit, Swiss cantons approve operating areas (and need not decide before Mar 2028), and French organising authorities decide on each system [P]. Each new city therefore repeats an approval, as in China's city-by-city pilot zones (§B4a), but under different national laws.
3. **The laws differ, and recognition is still an intention.** The table holds seven national regimes; the 18-state declaration "will seek to facilitate mutual recognition" and is not a treaty [P].
4. **Operators had not yet asked for driverless permission.** TfL knew of no APS application on 14 Jul 2026 [I], and every German Level 4 activity runs under testing approvals [I]; Waymo said in Sep 2026 that it would apply under the APS scheme [P]. In 2026, operators' safety cases held Europe back as much as its laws did.
5. **The money and the driving systems are elsewhere.** Wayve's \$1.2 B Series D of Feb 2026, at an \$8.6 B valuation, with Mercedes-Benz, Nissan and Stellantis among its investors, is the largest European raise for autonomy; Waymo raised \$16 B the same month, at \$126 B [P]. European carmakers buy their robotaxi systems from Mobileye (Volkswagen) or Pony.ai (Stellantis), and Uber's Munich pilot runs Momenta's [P].

### 5. What it means for lidar

[E unless tagged]
- **Installed base.** The lidars on Europe's driverless and test fleets, counted as vehicles × lidars per vehicle:
  - Volkswagen's 55 Level 4 test vehicles in Germany, if all are ID. Buzz ADs with nine Innoviz units each: $55\times9\approx500$;
  - Westwell's 100 Felixstowe trucks at an assumed two to four Hesai units each (Hesai says "multiple"): $100\times(2\text{–}4)=200\text{–}400$;
  - about 30 Zagreb robotaxis with four AT128 each: $30\times4=120$;
  - WeRide's ≈25 vehicles in Madrid and Switzerland at an assumed four to six each: ≈100–150;
  - the fleets without published counts (Waymo's, Baidu's, Momenta's and Holon's tests, and the trucks of MAN, Einride and Volvo), perhaps a few hundred more.
  - In all, ≈1–2k lidars ($500+200+120+100=920$ at the low end; $500+400+120+150=1{,}170$ plus a few hundred at the high end), about 2–7% of the ≈27–40k on robotaxis and trucks outside China (§B4), of which they are a part ($920/40{,}000\approx2\%$; $2{,}000/27{,}000\approx7\%$).
- **Suppliers.** Innoviz on Volkswagen's vans and, through Mobileye Drive, probably on Holon's shuttles; Hesai on Pony.ai's, Baidu's and Westwell's vehicles; RoboSense on WeRide's newest GXR [P]. No European lidar maker supplies any fleet in this section [E, from the suppliers named].
- **What would change it, and when** [dates P]:
  - UN Regulation 185 in EU law, planned from 1 Jan 2027, with the large-series safety rules adapted to vehicles without a driver;
  - the first UK APS permit and Waymo's London service, and the full UK regime from the second half of 2027;
  - MOIA's targeted EU-wide approval of the driverless ID. Buzz AD by 2027 [T, Business Insider, quoting MOIA] and PostAuto's driverless service from 2027;
  - the end of Switzerland's three-year wait on 1 Mar 2028.
  - ADACities is a guide to scale: if ten cities each reach 100 vehicles by 2030 at four to nine lidars per vehicle, they hold $10\times100\times(4\text{–}9)=4\text{–}9\text{k}$ lidars, small next to China's van fleet (§B4a).
- **Origin may matter more than volume.** The 18-state declaration and ADACities favour partnerships with EU companies [P], but no EU measure targets the origin of lidars (§F3), and the fleets in this section run on Israeli and Chinese lidars.

Sources: """

SOURCE_KEYS = ["gsr", "ta", "ads_ir", "avp_ir", "avp_da", "kba_eu", "wp29_report", "r185", "gtr", "depositary",
               "hys_18732", "hys_18133", "action_plan", "jdi", "council_testbed", "adacities", "pld", "ai_act", "rdw",
               "stvg_1d", "stvg_1e", "stvg_1i", "afgbv", "kba_national", "kba_list", "kba_faq", "bt_wd",
               "de_strategy", "ava", "si_439", "dft_2025", "ssp", "la_report", "la_15", "fr_ord", "fr_dec", "ch_vaf",
               "es_dgt", "hr_law", "hr_rules", "lu_pony", "uber_wayve", "waymo_testing", "waymo_london",
               "lyft_baidu", "postauto", "hesai_baidu", "zh_furttal", "zrh_airport", "weride_valence",
               "weride_madrid", "robosense_weride", "moia_hamburg", "moia_series", "innoviz_vw", "mobileye_innoviz",
               "hochbahn", "uber_momenta", "pony_zagreb", "uber_zagreb", "pony_verne_driverless", "afp_zagreb",
               "hesai_pony", "stellantis_bolt", "karsan", "electrive_stavanger", "wayve_series_d", "waymo_16b",
               "einride_lidl", "schwarz", "einride_q3", "atlas", "man_2024", "scania", "traton_plus", "iveco_plus",
               "volvo_bronnoy", "volvo_3mt", "fernride", "felixstowe_2025", "felixstowe_100", "hesai_westwell"]
assert len(SOURCE_KEYS) == len(set(SOURCE_KEYS)) and set(SOURCE_KEYS) <= set(U)
SECTION = SECTION + " ; ".join(U[k] for k in SOURCE_KEYS) + "\n\n"

EXEC_BULLET = (
    "   - **Europe has no robotaxi service without a person aboard yet, and buys its driving systems abroad (§B4b).**\n"
    "     - Every robotaxi service open to riders, in London, Zagreb, Zurich, Hamburg and Munich, carried a safety "
    "driver or operator in Nov 2026; vehicles ran with nobody aboard only on short fixed routes and private ground.\n"
    "     - No vehicle in Germany held a Level 4 operating permit in Apr 2026, no UK permit for an automated "
    "passenger service had been granted by Oct 2026, and EU type approval of driverless vehicles stays capped at "
    "1,500 per type per year until the new UN rules apply (planned from Jan 2027).\n"
    "     - The systems in service are Chinese, Mobileye's or Waymo's, and their lidars Innoviz's or Chinese, about "
    "1–2k units in all.\n")

APPENDIX1_FLEETS = (
    "- **European fleets (§B4b):** lidar counts and suppliers are not published for Momenta's Munich cars, Holon's "
    "shuttle (Innoviz supplies Mobileye Drive [P]), WeRide's Furttal cars and Robobuses, Westwell's Felixstowe trucks "
    "(Hesai says \"multiple\" per truck [P]) or the trucks of Einride, MAN and Volvo. Fleet sizes are unpublished for "
    "Waymo's and Baidu's London tests, Momenta's Munich pilot and Verne's Zagreb fleet (about 30 by AFP's count [T]), "
    "and whether Volkswagen's 55 Level 4 test vehicles are all ID. Buzz ADs is not stated.")

APPENDIX1_RULES = (
    "- **Europe's approvals (§B4b):** UN Regulation No 185 enters into force on adoption, about end-Jan 2027 by the "
    "depositary procedure, while the Commission's draft applies it from 1 Jan 2027 and UN News said \"roughly one "
    "month\"; the UN's notice of adoption will settle the date. Unknown: any German Level 4 operating permit after "
    "27 Apr 2026; any UK APS application after 14 Jul 2026 (no official count is published); the legal basis of the "
    "Stavanger bus's driverless approval, which only the press reports; whether the Valence Robobus still runs; and "
    "when the Commission's promised harmonised rules for testing on open roads will appear.")

APPENDIX2_GROUP = (
    "**Europe: laws, regulators and operators (§B4b)**\n"
    "- Regulation (EU) 2019/2144, General Safety Regulation (Art. 3(21)–(22), Art. 11): " + U["gsr"] + "\n"
    "- Regulation (EU) 2018/858, consolidated 2 Aug 2026 (Annex V small-series limits): " + U["ta"] + "\n"
    "- Implementing Regulation (EU) 2022/1426 on the ADS of fully automated vehicles, consolidated 24 Mar 2026: "
    + U["ads_ir"] + "\n"
    "- Implementing Regulation (EU) 2026/481 and Delegated Regulation (EU) 2026/1188 (automated valet parking): "
    + U["avp_ir"] + " ; " + U["avp_da"] + "\n"
    "- WP.29 199th session report (ECE/TRANS/WP.29/1192; votes on UN Regulation 185 and the GTR, pp. 30, 32): "
    + U["wp29_report"] + "\n"
    "- UN Regulation No 185 on ADS (ECE/TRANS/WP.29/2026/137) and the UN GTR on ADS (ECE/TRANS/WP.29/2026/139): "
    + U["r185"] + " ; " + U["gtr"] + "\n"
    "- UN depositary notification C.N.288.2026 (adoption procedure for UN Regulation 185): " + U["depositary"] + "\n"
    "- Commission initiatives 18732 (UN Regulation 185 in the General Safety Regulation) and 18133 (safety "
    "requirements adapted to fully automated vehicles): " + U["hys_18732"] + " ; " + U["hys_18133"] + "\n"
    "- Industrial Action Plan for the European automotive sector, COM(2025) 95 (pp. 2–3): " + U["action_plan"] + "\n"
    "- Joint Declaration of Intent on a cross-border testbed for automated vehicles (8 Jun 2026): " + U["jdi"] + "\n"
    "- ADACities initiative (23 Jun 2026): " + U["adacities"] + "\n"
    "- Product Liability Directive (EU) 2024/2853; AI Act (EU) 2024/1689, consolidated 27 Jul 2026: " + U["pld"]
    + " ; " + U["ai_act"] + "\n"
    "- Germany: StVG §§ 1d, 1e, 1i and the AFGBV: " + U["stvg_1d"] + " ; " + U["stvg_1e"] + " ; " + U["stvg_1i"]
    + " ; " + U["afgbv"] + "\n"
    "- KBA: list of testing approvals (5 Nov 2026), testing FAQ and national operating permits: " + U["kba_list"]
    + " ; " + U["kba_faq"] + " ; " + U["kba_national"] + "\n"
    "- Bundestag research service, *Autonomes Fahren – Rechtslage und Markteinführung in Deutschland*, "
    "WD 5-3000-038/26 (pp. 22, 25): " + U["bt_wd"] + "\n"
    "- UK: Automated Vehicles Act 2024; SI 2026/439; London Assembly Transport Committee report (Oct 2026, pp. 12, "
    "19): " + U["ava"] + " ; " + U["si_439"] + " ; " + U["la_report"] + "\n"
    "- France: Ordonnance n° 2021-443 and Décret n° 2021-873 (Journal officiel copies): " + U["fr_ord"] + " ; "
    + U["fr_dec"] + "\n"
    "- Switzerland: Ordinance on Automated Driving (VAF; Arts. 34, 44, 51): " + U["ch_vaf"] + "\n"
    "- Spain: DGT framework for automated-vehicle testing (ES-AV): " + U["es_dgt"] + "\n"
    "- Croatia: Narodne novine 145/2024 and 154/2024: " + U["hr_law"] + " ; " + U["hr_rules"] + "\n"
    "- Operators: Uber and Wayve (2 Sep 2026); MOIA Hamburg (15 Jul 2026); Uber and Momenta (18 Nov 2026); Pony.ai "
    "in Zagreb (8 Apr 2026); Zurich Airport (9 Sep 2026); Canton of Zurich (24 Sep 2026); WeRide in Madrid (10 Sep "
    "2026): " + U["uber_wayve"] + " ; " + U["moia_hamburg"] + " ; " + U["uber_momenta"] + " ; " + U["pony_zagreb"]
    + " ; " + U["zrh_airport"] + " ; " + U["zh_furttal"] + " ; " + U["weride_madrid"] + "\n"
    "- Freight: Einride and Lidl (15 Sep 2026); Schwarz Group on the pilot; Port of Felixstowe's fleet of 100: "
    + U["einride_lidl"] + " ; " + U["schwarz"] + " ; " + U["felixstowe_100"] + "\n"
    "\n")

EDITS = [
    # reading guide: scope list and the organisation of Part B
    ("  - China's driverless delivery vans (about 47k in Q1 2026), where Chinese autonomous trucking stands, and "
     "delivery robots and trucks elsewhere (§B4a);\n",
     "  - China's driverless delivery vans (about 47k in Q1 2026), where Chinese autonomous trucking stands, and "
     "delivery robots and trucks elsewhere (§B4a);\n"
     "  - how far driverless vehicles have got in Europe, the laws and approvals that govern them, and why Europe is "
     "later than the US and China (§B4b);\n"),
    ("robotaxis and trucks, China's driverless delivery vans, parking sensing, and markets beyond cars.",
     "robotaxis and trucks, China's driverless delivery vans, Europe's driverless pilots and the rules behind them, "
     "parking sensing, and markets beyond cars."),
    # §0, a bullet after the China vans block
    ("   - **Beyond cars (§B8):**\n", EXEC_BULLET + "   - **Beyond cars (§B8):**\n"),
    # §B4 pointers
    ("China's driverless delivery vans and autonomous trucks, and delivery robots elsewhere, are covered in §B4a.",
     "China's driverless delivery vans and autonomous trucks, and delivery robots elsewhere, are covered in §B4a; "
     "Europe's robotaxis, shuttles and trucks, and the laws that govern them, in §B4b."),
    ("and Japan (Level 2 commercially, Level 4 demonstrations on the Shin-Tomei) are covered in §B4a.",
     "and Japan (Level 2 commercially, Level 4 demonstrations on the Shin-Tomei) are covered in §B4a, and Europe (one "
     "cab-less truck route in Germany under a testing approval, tests with safety drivers, and driverless trucks on "
     "private ground) in §B4b."),
    ("| **Einride / Lidl** (Germany) | First KBA Level 4 permit for a cab-less truck on a German public road "
     "(announced 15 Sep 2026). One vehicle type on one route, reportedly a quarter-mile link [P/T] |",
     "| **Einride / Lidl** (Germany) | A cab-less truck on a German public road with nobody aboard, announced on "
     "15 Sep 2026, under a KBA Level 4 testing approval: one truck on one short route at up to 25 km/h, with a local "
     "operator following in a separate vehicle (§B4b) [P] |"),
    ("Pony.ai began ride-hailing in Zagreb in Apr 2026,",
     "Pony.ai began ride-hailing in Zagreb in Apr 2026 (§B4b lists Europe's services one by one),"),
    # the new section, before §B5
    ("\n## B5. Lidar's share of new cars outside China (estimate)\n",
     "\n" + SECTION + "## B5. Lidar's share of new cars outside China (estimate)\n"),
    # Appendix 2: a European group after the robotaxi-and-trucks group
    ("\n**FMCW and beam steering**\n", "\n" + APPENDIX2_GROUP + "**FMCW and beam steering**\n"),
]

# Appendix 1: items after existing lines (found by a unique line prefix)
AFTER_LINES = [
    ("- **HiRain–Arbe L3 imaging radar (§E2a):**", APPENDIX1_FLEETS),
    ("- **Camera damage by lidar (§C4c subsection 1).**", APPENDIX1_RULES),
]

new = text
for old, rep in EDITS:
    n = new.count(old)
    assert n == 1, f"anchor found {n} times: {old[:90]!r}"
    new = new.replace(old, rep, 1)
lines = new.split("\n")
for prefix, item in AFTER_LINES:
    hits = [i for i, ln in enumerate(lines) if ln.startswith(prefix)]
    assert len(hits) == 1, f"line prefix found {len(hits)} times: {prefix[:80]!r}"
    lines[hits[0]] = lines[hits[0]] + "\n" + item
new = "\n".join(lines)
assert "\r" not in new
print(f"{len(EDITS)} substring edits, {len(AFTER_LINES)} appended items; sha256 before {sha[:12]}, after "
      f"{hashlib.sha256(new.encode('utf-8')).hexdigest()[:12]}")
if "--write" in sys.argv[3:]:
    report.write_bytes(new.encode("utf-8"))
    print("written")
