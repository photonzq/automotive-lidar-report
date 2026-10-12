# -*- coding: utf-8 -*-
"""
Arithmetic check for the Fastree3D SA capital history (Vaud commercial
register / SOGC texts) and for the CHF translation of the Hesai FY2023 20-F
cash-flow figure. Pure arithmetic, no network access.

Inputs are typed in from the primary sources:
  - SOGC notices 974895 (2013) ... 1004974438 (2020): share steps, claims set off
  - Fed H.10 daily rates (CHF per USD, CNY per USD) for 15 and 29 Dec 2023
  - Hesai FY2023 20-F cash-flow line: RMB 54,454 k net outflow, RMB 571 k cash
    acquired, US$ 7,670 k convenience translation at RMB 7.0999 per US$
"""

# (label, shares before, shares after, claims set off in CHF or None, how)
steps = [
    ("2013-07 founding", 0, 100_000, None, "cash at founding (no in-kind/set-off published)"),
    ("2014-10 conditional", 100_000, 132_170, None, "conditional capital (option/conversion rights)"),
    ("2014-10 ordinary, set-off", 132_170, 166_170, 170_000, "set-off of claims"),
    ("2015-03 ordinary", 166_170, 209_633, None, "no set-off stated"),
    ("2015-11 ordinary, set-off", 209_633, 226_033, 82_000, "set-off of claims"),
    ("2016-11 authorised, set-off", 226_033, 240_851, 400_086, "set-off of claims"),
    ("2016-11 authorised", 240_851, 266_351, None, "no set-off stated"),
    ("2016-11 conditional", 266_351, 277_540, None, "conditional capital"),
    ("2018-04 authorised, set-off", 277_540, 297_431, 875_204, "set-off of claims"),
    ("2018-06 conditional", 297_431, 315_757, None, "conditional capital"),
    ("2018-06 authorised", 315_757, 326_174, None, "no set-off stated"),
    ("2019-08 ordinary, set-off", 326_174, 340_702, 697_344, "set-off of a claim"),
    ("2020-08 authorised, set-off", 340_702, 382_152, 1_236_202, "set-off of claims"),
    ("2020-08 conditional", 382_152, 391_631, None, "conditional capital"),
    ("2020-08 authorised", 391_631, 429_444, None, "no set-off stated"),
]

tot = {"set-off": 0, "conditional": 0, "other": 0}
claims = 0
for lab, a, b, c, how in steps:
    n = b - a
    if c:
        print(f"{lab:30s} +{n:7d} sh  claims CHF {c:>9,d}  price = {c}/{n} = {c / n:.4f}")
        tot["set-off"] += n
        claims += c
    else:
        key = "conditional" if "conditional" in lab else "other"
        if a:
            tot[key] += n
        print(f"{lab:30s} +{n:7d} sh  ({how})")
print("shares by set-off      :", tot["set-off"])
print("shares conditional cap :", tot["conditional"])
print("shares other increases :", tot["other"])
print("founding               :", 100_000)
print("sum                    :", 100_000 + sum(tot.values()))
print("claims set off, total  : CHF", f"{claims:,d}")
print("register 'montant libere' sum (34'000 for 2014):",
      f"{34_000 + 82_000 + 400_086 + 875_204 + 697_344 + 1_236_202:,d}")

# FX
usd_k = 7_670          # US$ thousand, 20-F convenience translation
rmb_net_k = 54_454     # RMB thousand, net of cash acquired
rmb_cash_k = 571       # RMB thousand, cash acquired
chf_usd_1215, chf_usd_1229 = 0.8688, 0.8405   # H.10, CHF per USD
cny_usd_1215, cny_usd_1229 = 7.1179, 7.0999   # H.10, CNY per USD
shares = 429_444
print()
print("check 20-F: 54,454 / 7.0999 =", round(rmb_net_k / cny_usd_1229, 2), "kUSD")
a = usd_k * chf_usd_1215
b = usd_k * chf_usd_1229
c = rmb_net_k / cny_usd_1215 * chf_usd_1215
d = (rmb_net_k + rmb_cash_k) / cny_usd_1215 * chf_usd_1215
for lab, v in (("USD 7,670k x 0.8688 (15 Dec)", a),
               ("USD 7,670k x 0.8405 (29 Dec)", b),
               ("RMB 54,454k / 7.1179 x 0.8688", c),
               ("RMB 55,025k / 7.1179 x 0.8688 (gross of cash)", d)):
    print(f"{lab:48s} = CHF {v:,.1f}k ; per share CHF {v * 1000 / shares:.3f}")
print("USD per share: 7,670,000 / 429,444 =", round(7_670_000 / shares, 3))
