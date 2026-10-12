"""Find lidar-relevant FP7, Horizon 2020 and Horizon Europe projects in the normalized CORDIS
corpus, classify them by rule, and tabulate trends by start year (2007-2026).

Input: the pickle written by build_corpus.py (one row per project, de-duplicated by id).
Text searched: title + objective + keywords (case-insensitive).

Rules (all scripted; see the regexes below):
  terms      lidar/ladar/laser radar; airborne/terrestrial/mobile laser scanning, laser
             altimetry, ceilometers; ToF cameras/sensors, depth or 3D sensing and cameras
             (only with an active-ranging word: ToF, lidar, SPAD, single-photon, ranging,
             rangefinder, distance measurement; and not in mass-spectrometry, neutron, PET,
             SIMS, electron or ultrasound texts unless lidar is named); laser ranging,
             rangefinders, optical ranging, absolute distance and comb-based ranging.
  relevance  score = 3 x (lidar term in title) + 2 x (in keywords) + (number of lidar-term
             mentions in the objective, capped at 5). core: score >= 3; significant: 2;
             mention: 1. "Lidar-relevant" in the trend tables means core + significant.
  role       HW  = a sentence with a lidar term also has a hardware/component word and a
                   development verb (lidar hardware, component or instrument development);
             USE = otherwise (lidar data or lidar sensors used, integrated or analysed).
  application  the category with the most keyword hits (ties: fixed priority order).
  flags      coherent: FMCW, coherent/heterodyne lidar or comb ranging;
             pic: photonic-integrated (OPA, PIC, silicon/SiN photonics, photonic chip) in a
                  project that also names lidar/ranging;
             spad: SPAD, single-photon or photon-counting detection with lidar/ranging.
  programme  ERC, MSCA, EIC/SME/FET, Chips JU/KDT/ECSEL (incl. ENIAC/ARTEMIS), other JU
             (Clean Sky/Aviation, SESAR, Shift2Rail/Europe's Rail), collaborative (the rest).

Outputs (CSV, in <out_dir>): lidar_projects_classified.csv, trend_<subset>.csv for the
subsets all/hw/coherent/pic/spad, trend_programme_shares.csv, corpus_totals_by_year.csv,
notable_hw_2023_2026.csv.

Usage:
    python classify_trends.py <corpus_pickle> <out_dir>
"""
import os
import re
import sys

import pandas as pd

LID = r'(?<![a-z])(?:lidars?|ladars?)(?![a-z])|laser[- ]radars?'
ALS = (r'(?:airborne|terrestrial|mobile|aerial|uav|drone|3d)[- ]laser[- ]scann\w*'
       r'|laser[- ]scann\w* (?:data|survey|point)|laser altimet\w*|ceilometers?')
TOFD = (r'time[- ]of[- ]flight (?:cameras?|sensors?|imag\w*|depth|rang\w*|3d|lidar)'
        r'|\btof (?:cameras?|sensors?|depth)|depth[- ]sensing|depth cameras?|3d (?:sensing|cameras?)|flash lidar')
RNG = (r'laser rang(?:ing|efinders?|e[- ]finders?)|rangefinders?|range[- ]finders?|optical ranging'
       r'|absolute distance measurement|dual[- ]comb (?:rang\w*|distance)|comb[- ]based (?:rang\w*|distance)')
ANY = '|'.join([LID, ALS, TOFD, RNG])
# ToF/depth terms are ignored in texts about other time-of-flight techniques (mass spectrometry,
# neutrons, PET, SIMS, electron spectroscopy, ultrasound) unless a lidar word is present.
# Word boundaries keep "electronic(s)" from matching "electron".
TOF_EXCL = (r'mass spectrom|neutron|positron|\bpet\b|\bsims\b|tof-sims|ion mobility|\belectrons?\b|secondary ion'
            r'|ultrasound|ultrasonic|time[- ]of[- ]flight (?:mass|spectrom|diffraction|neutron|ion|electron|pet)')
# ToF/depth terms count only with an active optical-ranging context, so that stereo or
# structured-light "3D cameras" and "depth sensing" without ranging are not counted as lidar.
ACTIVE = (r'time[- ]of[- ]flight|\btof\b|lidar|ladar|\bspads?\b|single[- ]photon|photon[- ]counting'
          r'|(?<!wide-)(?<!wide )(?<!far-)(?<!far )\branging\b|range[- ]?finder|distance measurement')

COH = (r'fmcw|frequency[- ]modulated continuous[- ]wave|coherent (?:lidar|ladar|laser radar|rang\w*|detection|doppler)'
       r'|heterodyne|dual[- ]comb|frequency[- ]comb\w* (?:\w+ ){0,4}(?:rang\w*|distance)|microcomb\w* (?:\w+ ){0,4}(?:rang\w*|distance|lidar)')
PIC = (r'optical phased[- ]arrays?|photonic integrated circuits?|integrated photonic\w*|silicon photonic\w*'
       r'|silicon[- ]nitride|photonic chips?|chip[- ]scale|on[- ]chip|focal[- ]plane switch\w*|solid[- ]state beam[- ]steering')
SPAD = r'\bspads?\b|single[- ]photon|photon[- ]counting'
HWW = (r'laser|detector|receiver|transmitter|scanner|steering|photonic|chip|spad|vcsel|mems|optic|prototype|instrument'
       r'|sensor|module|wavelength|fmcw|coherent|component|source|hardware|system|device|technology|camera')
DEV = r'develop|design|build|fabricat|demonstrat|prototyp|novel|integrat|miniatur|engineer|innovat|improv|advanc|realis|realiz|new'
DATAW = r'data|point clouds?|surveys?|mapping|maps?|remote sensing|observ|measurements?|retriev|campaign|products|imagery|monitor|network'

APPS = [
    ('space_atmosphere', r'atmospher|aerosol|clouds?\b|wind (?:lidar|profil|energy|turbine|farm|resource)|doppler wind|ozone|water vapou?r|greenhouse|methane|\bco2\b|\bdial\b|differential absorption|spaceborne|space[- ]?borne|satellite|orbit|planetar|\bmars\b|lunar|\bmoon\b|earth observation|ceilometer|meteorolog|boundary layer|volcan|turbulence|wake vortex|weather'),
    ('automotive_mobility', r'automotive|autonomous (?:driving|vehicles?|cars?)|self[- ]driving|\badas\b|vehicles?\b|\bcars?\b|road|traffic|trucks?|railway|rail\b|trains?\b|aviation|airport|aircraft|helicopter|maritime|ships?\b|vessels?|mobility|navigation|parking'),
    ('robotics_industrial_consumer', r'robot|industrial|industry|manufactur|factory|logistic|warehouse|smartphone|consumer|gesture|augmented reality|virtual reality|\bxr\b|machine vision|inspection|metrology|agv|automation'),
    ('defence_security', r'defen[cs]e|military|security|surveillance|border|counter[- ]?(?:drone|uav|uas)|threat|intrusion|police|crisis|rescue|first responders|mine detection|cbrn'),
    ('mapping_forestry_heritage_agri', r'forest|trees?\b|canopy|biomass|vegetation|agricultur|crops?\b|farm|vineyard|orchard|heritage|archaeolog|cultural|landscape|topograph|geomorph|glacier|coast|bathymetr|rivers?\b|flood|landslide|urban|buildings?|\bbim\b|ecolog|biodiversity|habitat|geolog|mining|terrain'),
]


def year_of(r):
    for k in ('startDate', 'ecSignatureDate'):
        v = str(r.get(k, '') or '')
        if re.match(r'\d{4}', v):
            return int(v[:4])
    return None


def programme(r):
    fs = str(r['fundingScheme']).upper()
    mc = (str(r['masterCall']) + ' ' + str(r['subCall']) + ' ' + str(r['topic'])).upper()
    lb = str(r['legalBasis']).upper()
    if fs.startswith('ERC') or 'HORIZON-ERC' in fs or 'ERC-' in mc[:12] or lb.startswith('FP7-IDEAS') or 'H2020-EU.1.1.' in lb or 'HORIZON.1.1' in lb:
        return 'ERC'
    if fs.startswith('MSCA') or fs.startswith('MC-') or 'MSCA' in fs or 'MSCA' in mc or lb.startswith('FP7-PEOPLE') or 'H2020-EU.1.3' in lb or 'HORIZON.1.2' in lb:
        return 'MSCA'
    if any(k in fs + ' ' + mc for k in ('ECSEL', 'KDT', 'CHIPS', 'ENIAC', 'ARTEMIS')):
        return 'ChipsJU_KDT_ECSEL'
    if any(k in fs + ' ' + mc for k in ('SME-1', 'SME-2', 'SMEINST', 'EIC', 'FETOPEN', 'FETPROACT', 'FETFLAG', 'FET-')) or fs in ('SME-1', 'SME-2') or 'H2020-EU.1.2' in lb or 'HORIZON.3.1' in lb:
        return 'EIC_SME_FET'
    if any(k in fs + ' ' + mc for k in ('CS2', 'JTI-CS', 'CLEAN-AVIATION', 'SESAR', 'S2R', 'SHIFT2RAIL', 'ER-JU', 'EU-RAIL', 'CLEANSKY')):
        return 'other_JU'
    return 'collaborative'


def sentences(text):
    return re.split(r'(?<=[.!?;])\s+', text)


def classify(r):
    title = str(r['title']).lower()
    kw = str(r['keywords']).lower()
    obj = str(r['objective']).lower()
    full = ' '.join([title, kw, obj])
    tof_ok = (bool(re.search(TOFD, full)) and bool(re.search(ACTIVE, full))
              and not (re.search(TOF_EXCL, full) and not re.search(LID, full)))
    terms = ANY if tof_ok else '|'.join([LID, ALS, RNG])
    n_t = len(re.findall(terms, title))
    n_k = len(re.findall(terms, kw))
    n_o = min(len(re.findall(terms, obj)), 5)
    score = 3 * (n_t > 0) + 2 * (n_k > 0) + n_o
    if score == 0:
        return None
    rel = 'core' if score >= 3 else ('significant' if score == 2 else 'mention')
    hw = False
    data_use = False
    for s in sentences(title + '. ' + obj):
        if re.search(terms, s):
            if re.search(HWW, s) and re.search(DEV, s):
                hw = True
            if re.search(DATAW, s):
                data_use = True
    if re.search(r'(?:lidar|ladar|laser radar)[- ](?:data|point|derived|survey)', full) and not re.search(r'(?:develop|design|build)\w* (?:\w+ ){0,4}(?:lidar|ladar)', full):
        hw = hw and bool(re.search(r'(?:lidar|ladar) (?:system|sensor|instrument|transmitter|receiver|prototype)s?', full))
    role = 'HW' if hw else 'USE'
    coh = bool(re.search(COH, full)) and bool(re.search(LID + '|' + RNG + '|rang|distance', full))
    pic = bool(re.search(PIC, full)) and bool(re.search(LID + '|' + RNG + '|beam[- ]steering|3d sensing|depth', full))
    spad = bool(re.search(SPAD, full)) and bool(re.search(LID + '|' + RNG + '|time[- ]of[- ]flight|3d imaging|depth', full))
    scores = {name: len(re.findall(p, full)) for name, p in APPS}
    best = max(scores.values())
    app = 'other_fundamental' if best == 0 else [n for n, _ in APPS if scores[n] == best][0]
    return dict(score=score, relevance=rel, role=role, app=app, coherent=coh, pic=pic, spad=spad,
                n_title=n_t, n_kw=n_k, n_obj=n_o, data_words=data_use)


def trend(df, years, label):
    g = df.groupby('year').agg(n=('id', 'count'), eur=('ecMax', 'sum'))
    g = g.reindex(years, fill_value=0)
    g['eur_m'] = (g['eur'] / 1e6).round(2)
    g = g.drop(columns='eur')
    g.columns = [f'{label}_n', f'{label}_eur_m']
    return g


def main(corpus, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    c = pd.read_pickle(corpus)
    c['year'] = c.apply(year_of, axis=1)
    c['prog'] = c.apply(programme, axis=1)
    years = list(range(2007, 2027))
    tot = c.groupby('year').agg(all_n=('id', 'count'), all_eur=('ecMax', 'sum')).reindex(years, fill_value=0)
    tot['all_eur_m'] = (tot['all_eur'] / 1e6).round(1)
    tot.drop(columns='all_eur').to_csv(os.path.join(out_dir, 'corpus_totals_by_year.csv'))
    out = []
    for _, r in c.iterrows():
        k = classify(r)
        if k:
            d = r[['fp', 'id', 'acronym', 'title', 'year', 'startDate', 'endDate', 'ecMax', 'totalCost', 'prog',
                   'fundingScheme', 'masterCall', 'topic', 'coordName', 'coordCountry', 'coordType', 'coordSME', 'nPart']].to_dict()
            d.update(k)
            d['objective_head'] = str(r['objective'])[:400].replace('\n', ' ')
            out.append(d)
    L = pd.DataFrame(out)
    L.to_csv(os.path.join(out_dir, 'lidar_projects_classified.csv'), index=False, encoding='utf-8')
    R = L[L.relevance.isin(['core', 'significant'])]
    subsets = {'all_incl_mentions': L, 'relevant': R, 'hw': R[R.role == 'HW'], 'coherent': R[R.coherent],
               'pic': R[R.pic], 'spad': R[R.spad]}
    tabs = [tot[['all_n', 'all_eur_m']]]
    for name, sdf in subsets.items():
        t = trend(sdf, years, name)
        t.to_csv(os.path.join(out_dir, f'trend_{name}.csv'))
        tabs.append(t)
    big = pd.concat(tabs, axis=1)
    big['relevant_per_1000'] = (1000 * big['relevant_n'] / big['all_n']).round(2)
    big['hw_per_1000'] = (1000 * big['hw_n'] / big['all_n']).round(2)
    big['relevant_eur_share_pct'] = (100 * big['relevant_eur_m'] / big['all_eur_m']).round(2)
    big['hw_eur_share_pct'] = (100 * big['hw_eur_m'] / big['all_eur_m']).round(3)
    big.to_csv(os.path.join(out_dir, 'trend_summary.csv'))
    ps = R.pivot_table(index='year', columns='prog', values='id', aggfunc='count', fill_value=0).reindex(years, fill_value=0)
    pe = R.pivot_table(index='year', columns='prog', values='ecMax', aggfunc='sum', fill_value=0).reindex(years, fill_value=0) / 1e6
    ps.to_csv(os.path.join(out_dir, 'trend_programme_counts.csv'))
    pe.round(2).to_csv(os.path.join(out_dir, 'trend_programme_eur_m.csv'))
    app = R.pivot_table(index='year', columns='app', values='id', aggfunc='count', fill_value=0).reindex(years, fill_value=0)
    app.to_csv(os.path.join(out_dir, 'trend_application_counts.csv'))
    hwapp = R[R.role == 'HW'].pivot_table(index='year', columns='app', values='id', aggfunc='count', fill_value=0).reindex(years, fill_value=0)
    hwapp.to_csv(os.path.join(out_dir, 'trend_application_counts_hw.csv'))
    nb = R[(R.role == 'HW') & (R.year >= 2023)].sort_values(['year', 'ecMax'], ascending=[True, False])
    nb.to_csv(os.path.join(out_dir, 'notable_hw_2023_2026.csv'), index=False, encoding='utf-8')
    pd.set_option('display.width', 250)
    print(big.to_string())
    print('\nprogramme counts (relevant)\n', ps.to_string())
    print('\napplication counts (relevant)\n', app.to_string())
    print('\nrelevance', L.relevance.value_counts().to_dict(), 'role(relevant)', R.role.value_counts().to_dict())


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
