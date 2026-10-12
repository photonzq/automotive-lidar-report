/*
 * Page-console snippets used to read sites that refuse scripted HTTP clients
 * (SEC EDGAR without a contact header, Justia) or run their search in an AJAX panel
 * (ARAMIS). Each snippet was pasted into the page's console, in an ordinary browser
 * tab already showing the site named in its heading; nothing here logs in or submits
 * personal data. Results were copied into the findings by hand.
 */

// 1. SEC EDGAR filing (e.g. Hesai FY2023 20-F, Aeva FY2025 10-K): passages around keywords.
//    Open the filing's .htm page first, then run:
(() => {
  const t = document.body.innerText.replace(/\s+/g, ' ');
  const re = /(Swiss|spatial awareness|Fastree|contingent consideration|earn-out|earnout|asset acquisition|bargain purchase|patent rights|Switzerland|Chachoengsao|European (?:passenger )?(?:OEM|original equipment)|definitive (?:volume )?production agreement|Supplier Award|terminate.{0,40}for convenience)/gi;
  const out = []; const seen = new Set(); let m;
  while ((m = re.exec(t)) !== null) {
    const k = Math.floor(m.index / 600); if (seen.has(k)) continue; seen.add(k);
    out.push('[' + m[0] + '] ' + t.slice(Math.max(0, m.index - 450), m.index + 550));
  }
  return { length: t.length, hits: out };
})();

// 2. ARAMIS project search (https://www.aramis.admin.ch/Projektsuche/?Sprache=en-US):
//    run one term per call; the result list refreshes through an update panel.
(async (q) => {
  const before = document.body.innerText;
  document.querySelector('input[name="ctl00$cphContent$txtSearch"]').value = q;
  document.querySelector('input[name="ctl00$cphContent$cmdSearch"]').click();
  let t = '';
  for (let k = 0; k < 20; k++) { await new Promise(r => setTimeout(r, 700)); t = document.body.innerText; if (t !== before) break; }
  const ids = [...document.querySelectorAll('a')].filter(a => /ProjectID=/.test(a.href))
    .map(a => [a.innerText.trim().slice(0, 70), a.href.match(/ProjectID=(\d+)/)[1]]);
  return { q, count: (t.match(/(\d+) results/) || [])[1], ids };
})('Pointcloud');   // also run: 'Nicolaescu', 'Fastree3D', 'FMCW', 'lidar'

// 3. Justia Patents (https://patents.justia.com/...): an inventor's or a search page's
//    publications with filing date, publication date and assignee.
(async (people) => {
  const out = {};
  await Promise.all(people.map(async p => {
    const ctl = new AbortController(); setTimeout(() => ctl.abort(), 12000);
    const r = await fetch('/inventor/' + p, { signal: ctl.signal });
    const doc = new DOMParser().parseFromString(await r.text(), 'text/html');
    out[p] = [...doc.querySelectorAll('li')].map(li => li.textContent.replace(/\s+/g, ' '))
      .filter(s => /Inventor/.test(s) && /(Patent number|Publication number)/.test(s))
      .map(s => {
        const num = s.match(/(Patent number|Publication number): (\S+)/);
        const f = s.match(/Filed: ([A-Za-z]+ \d+, \d{4})/);
        const d = s.match(/(Date of Patent|Publication date): ([A-Za-z]+ \d+, \d{4})/);
        const a = s.match(/(Assignee|Applicant)s?: (.*?) Inventor/);
        return [num && num[2], f && f[1], d && d[2], a && a[2]].join(' | ');
      });
  }));
  return out;
})(['augusto-ronchini-ximenes', 'preethi-padmanabhan', 'stefan-thomas-keller',
    'lucio-carrara', 'bruno-penlae', 'ting-gong', 'edoardo-charbon']);
