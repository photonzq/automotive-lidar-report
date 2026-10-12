import json, sys, subprocess, urllib.parse, os, time
sys.stdout.reconfigure(encoding='utf-8')
def fetch(q, tag):
    allhits = []
    p = 1
    while True:
        url = 'https://cordis.europa.eu/search/en?q=' + urllib.parse.quote(q) + f'&format=json&p={p}&num=50'
        fn = f'raw_{tag}_p{p}.json'
        if not os.path.exists(fn) or os.path.getsize(fn) < 300:
            subprocess.run(['curl','-s','-m','180',url,'-o',fn])
        try:
            d = json.load(open(fn, encoding='utf-8'))
        except Exception as e:
            print('ERR', tag, p, e); break
        h = d['result']['header']
        hits = d.get('hits',{}).get('hit',[])
        if isinstance(hits, dict): hits=[hits]
        allhits += hits
        tot = int(h['totalHits'])
        print(tag, 'page', p, 'records', h['records'], 'total', tot, file=sys.stderr)
        if len(allhits) >= tot or not hits: break
        p += 1
    return allhits, tot
if __name__ == '__main__':
    tag = sys.argv[1]; q = sys.argv[2]
    hits, tot = fetch(q, tag)
    json.dump([x.get('project', x) for x in hits], open(f'hits_{tag}.json','w',encoding='utf-8'))
    print(tag, 'total', tot, 'got', len(hits))
