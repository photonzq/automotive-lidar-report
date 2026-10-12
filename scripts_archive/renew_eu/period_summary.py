"""Summarize the classified lidar projects by framework period and programme type, and apply
the manual corrections of the 2023-2026 review (role, flags, exclusions) to give a corrected
variant of the recent-year hardware series.

Usage:
    python period_summary.py <results_dir>
Reads <results_dir>/lidar_projects_classified.csv and corpus_totals_by_year.csv; writes
period_summary.csv, programme_shares_by_period.csv and hw_2023_2026_corrected.csv.
"""
import os
import sys

import pandas as pd

# manual review of 2023-2026 relevant projects (title + objective read; [E])
EXCLUDE = {'190122948': 'camera-only 3D perception (Tripleye), lidar named as the alternative',
           '101165759': 'radar antenna (ACTIVATING), not lidar'}
SET = {  # id: {field: value}
    '101194170': dict(role='HW', coherent=True, pic=True),   # STARLight: 300 mm SiPh pilot incl. Steerlight FMCW lidar
    '101135529': dict(coherent=True, pic=True),              # RETINA: FMCW lidar on an InP PIC
    '101125625': dict(role='HW', app='other_fundamental'),   # HIGHRES: dual-comb ranging (ERC)
    '101213805': dict(role='HW', app='other_fundamental'),   # ELASTIC: tunable microcomb chip (ERC PoC)
    '101291179': dict(role='HW', app='other_fundamental'),   # PI-MOLL: integrated mode-locked laser (EIC)
    '101189447': dict(role='HW', app='other_fundamental'),   # IRQUAL: SWIR QD lasers (ERC PoC)
    '101312043': dict(role='HW'),                            # BlueOcean: photonic instruments incl. lidar (MSCA DN)
    '101212897': dict(role='USE'),                           # FLORA: uses lidar data (ERC PoC)
    '101155484': dict(role='USE'),                           # PHOENIX-UASL: UAS lidar survey of heritage sites
    '101186678': dict(app='space_atmosphere'),               # ATLAS: lasers in space (CSA)
}


def period(y):
    if y <= 2013:
        return '2007-2013'
    if y <= 2020:
        return '2014-2020'
    return '2021-2026'


def main(rd):
    L = pd.read_csv(os.path.join(rd, 'lidar_projects_classified.csv'), dtype={'id': str})
    L = L[(L.year >= 2007) & (L.year <= 2026)]
    tot = pd.read_csv(os.path.join(rd, 'corpus_totals_by_year.csv'))
    tot['period'] = tot.year.apply(period)
    R = L[L.relevance.isin(['core', 'significant'])].copy()
    R['period'] = R.year.apply(period)
    rows = []
    for p, g in R.groupby('period'):
        t = tot[tot.period == p]
        hw = g[g.role == 'HW']
        rows.append(dict(period=p, all_projects=int(t.all_n.sum()), all_eur_m=round(t.all_eur_m.sum(), 0),
                         relevant_n=len(g), relevant_eur_m=round(g.ecMax.sum() / 1e6, 2),
                         relevant_per_1000=round(1000 * len(g) / t.all_n.sum(), 2),
                         hw_n=len(hw), hw_eur_m=round(hw.ecMax.sum() / 1e6, 2),
                         hw_per_1000=round(1000 * len(hw) / t.all_n.sum(), 2),
                         coherent_n=int(g.coherent.sum()), coherent_eur_m=round(g[g.coherent].ecMax.sum() / 1e6, 2),
                         pic_n=int(g.pic.sum()), pic_eur_m=round(g[g.pic].ecMax.sum() / 1e6, 2),
                         spad_n=int(g.spad.sum()), spad_eur_m=round(g[g.spad].ecMax.sum() / 1e6, 2)))
    ps = pd.DataFrame(rows)
    ps.to_csv(os.path.join(rd, 'period_summary.csv'), index=False)
    print(ps.to_string())
    sh = []
    for p, g in R.groupby('period'):
        for prog, h in g.groupby('prog'):
            sh.append(dict(period=p, programme=prog, n=len(h), n_share_pct=round(100 * len(h) / len(g), 1),
                           eur_m=round(h.ecMax.sum() / 1e6, 2), eur_share_pct=round(100 * h.ecMax.sum() / g.ecMax.sum(), 1),
                           hw_n=int((h.role == 'HW').sum()), hw_eur_m=round(h[h.role == 'HW'].ecMax.sum() / 1e6, 2)))
    sh = pd.DataFrame(sh)
    sh.to_csv(os.path.join(rd, 'programme_shares_by_period.csv'), index=False)
    print(sh.to_string())
    # corrected 2023-2026 variant
    C = R[R.year >= 2023].copy()
    C = C[~C.id.isin(EXCLUDE)]
    for pid, ch in SET.items():
        for k, v in ch.items():
            C.loc[C.id == pid, k] = v
    C.to_csv(os.path.join(rd, 'relevant_2023_2026_corrected.csv'), index=False, encoding='utf-8')
    out = []
    for y in range(2023, 2027):
        g = C[C.year == y]
        hw = g[g.role == 'HW']
        out.append(dict(year=y, relevant_n=len(g), relevant_eur_m=round(g.ecMax.sum() / 1e6, 2), hw_n=len(hw),
                        hw_eur_m=round(hw.ecMax.sum() / 1e6, 2), coherent_n=int(g.coherent.astype(bool).sum()),
                        coherent_eur_m=round(g[g.coherent.astype(bool)].ecMax.sum() / 1e6, 2),
                        pic_n=int(g.pic.astype(bool).sum()), pic_eur_m=round(g[g.pic.astype(bool)].ecMax.sum() / 1e6, 2)))
    o = pd.DataFrame(out)
    o.to_csv(os.path.join(rd, 'hw_2023_2026_corrected.csv'), index=False)
    print(o.to_string())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
