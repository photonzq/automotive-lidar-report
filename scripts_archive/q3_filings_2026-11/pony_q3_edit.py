"""Pony.ai's Q3 2026 results and the driverless launch of its Toyota bZ4X robotaxi (§B4, §B4a, §G1, Appendix 2).

Sources, read in full: the Q3 2026 results release (6-K of 18 Nov 2026, Exhibit 99.1) and the Pony.ai and Toyota
release of 16 Nov 2026 (PR Newswire). Facts used: robotaxi fleet 2,768 at 30 Sep 2026, target 3,500 in 20 cities by
year-end; all three seventh-generation models (built with BAIC, GAC and Toyota) in fully driverless commercial
operation; the bZ4X robotaxi joined the driverless commercial fleet in Guangzhou, about 1,000 planned across major
Chinese cities, first mass-produced unit Feb 2026; Zagreb ride-hailing from Apr 2026, Europe's first fully driverless
test rides with invited passengers from Sep 2026, over 200,000 km and several thousand trips to 31 Oct 2026; road
testing in Manchester, London to follow; over 4,000 robotaxis under agreements in negotiation abroad; memorandum with
inDrive and NVIDIA for Kazakhstan; Gen-4 Robotruck in mass production, a new Gen-4 heavy-duty model with GAC
Commercial Vehicle, deployments at Jiangmen Port and Shenzhen Mawan Port, fully driverless light-duty trucks in
production; robotruck revenue $18.0 M (+76.3%), mainly freight with Sinotrans. Hesai's release of 24 Apr 2025 (already
cited in §C4d): four AT128 on each vehicle of all three seventh-generation models.

Usage: pony_q3_edit.py <report.md> <expected sha256 prefix> [--write]
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

Q3 = "https://www.sec.gov/Archives/edgar/data/1969302/000110465926129308/tm2629888d1_ex99-1.htm"
BZ4X = ("https://www.prnewswire.com/apac/news-releases/ponyai-and-toyota-launch-fully-driverless-commercial-services-"
        "with-gen-7-bz4x-robotaxi-302939914.html")

EDITS = [
    # ---- §B4: Chinese operators abroad
    ("- **Chinese operators abroad** (WeRide about 400 in the Middle East; Pony and Baidu in Doha, Zagreb, Dubai and "
     "Switzerland) use Hesai or RoboSense lidars.\n",
     "- **Chinese operators abroad** (WeRide about 400 in the Middle East; Pony and Baidu in Doha, Zagreb, Dubai and "
     "Switzerland) use Hesai or RoboSense lidars. Pony.ai began ride-hailing in Zagreb in Apr 2026, ran Europe's first "
     "fully driverless test rides with invited passengers there from Sep 2026, and had logged more than 200,000 km and "
     "several thousand trips by 31 Oct. It is road-testing in Manchester, with London to follow, counts more than "
     "4,000 robotaxis under agreements in negotiation abroad, and has signed a memorandum with inDrive and NVIDIA on "
     "Kazakhstan [P].\n"),
    # ---- §B4a: the Pony.ai truck row
    ("| **Pony.ai** | Gen-4 heavy truck built with Sany. A \"1+4\" platoon with Sinotrans: a human-driven lead truck "
     "and four autonomous followers. Dozens of Gen-4 trucks are due to enter commercial service at Shenzhen's Mawan "
     "port | About 200 trucks (Nov 2025). Target of 500–1,000 Gen-4 trucks within two to three years (Aug 2026). The "
     "Gen-4 driving hardware is about 70% cheaper than the previous generation [T, CnEVPost; trans.info] |",
     "| **Pony.ai** | Gen-4 heavy truck built with Sany, and a second Gen-4 heavy-duty model with GAC Commercial "
     "Vehicle. A \"1+4\" platoon with Sinotrans: a human-driven lead truck and four autonomous followers. Robotrucks "
     "are being deployed at Jiangmen Port and Shenzhen's Mawan Port, with regular commercial operation planned, and "
     "fully driverless light-duty trucks have entered production, with first deployments for logistics clients in "
     "tier-one cities [P] | About 200 trucks (Nov 2025). Target of 500–1,000 Gen-4 trucks within two to three years "
     "(Aug 2026); the Gen-4 entered mass production on schedule in Q3 2026 [P]. The Gen-4 driving hardware is about "
     "70% cheaper than the previous generation [T, CnEVPost; trans.info]. Robotruck revenue was \\$18.0 M in Q3 2026, "
     "up 76.3%, mainly from freight services with Sinotrans [P] |"),
    # ---- §B4a Sources line: add the Q3 release
    ("https://www.electrive.com/2025/05/20/china-launches-worlds-largest-fleet-of-autonomous-electric-mining-trucks/\n",
     "https://www.electrive.com/2025/05/20/china-launches-worlds-largest-fleet-of-autonomous-electric-mining-trucks/ ; "
     + Q3 + " (Pony.ai Q3 2026 results)\n"),
    # ---- §G1: customers
    ("Baidu, Pony (4 AT128 per car), DiDi and Momenta. There is also a \\$40 M sole-supplier order from an unnamed "
     "\"leading U.S. robotaxi company\".\n",
     "Baidu, Pony (4 AT128 per car, below), DiDi and Momenta. There is also a \\$40 M sole-supplier order from an "
     "unnamed \"leading U.S. robotaxi company\".\n"
     "  - **Pony.ai** fits four AT128 to every vehicle of its three seventh-generation robotaxi models [P, Hesai] "
     "(§C4d). All three, built with BAIC, GAC and Toyota, were in fully driverless commercial operation by Nov 2026, "
     "and its robotaxi fleet numbered 2,768 at 30 Sep 2026, against a target of 3,500 in 20 cities by year-end [P]. "
     "The Toyota bZ4X model joined the driverless commercial fleet in Guangzhou on 16 Nov 2026, with about 1,000 "
     "planned across major Chinese cities [P], which at four per car is $1{,}000\\times4=4{,}000$ AT128 [E].\n"),
    # ---- Appendix 2: robotaxi group
    ("- Zoox paid service: https://techcrunch.com/2026/07/30/zoox-clears-final-federal-hurdle-to-launch-paid-robotaxi-"
     "service/\n",
     "- Zoox paid service: https://techcrunch.com/2026/07/30/zoox-clears-final-federal-hurdle-to-launch-paid-robotaxi-"
     "service/\n"
     "- Pony.ai Q3 2026 results (6-K of 18 Nov 2026, Exhibit 99.1; robotaxi fleet, seventh-generation driverless "
     "operation, Zagreb, Manchester and London, Robotruck): " + Q3 + "\n"
     "- Pony.ai and Toyota, fully driverless commercial service with the bZ4X robotaxi in Guangzhou (16 Nov 2026): "
     + BZ4X + "\n"),
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
