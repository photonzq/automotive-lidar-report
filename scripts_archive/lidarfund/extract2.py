import re,html,sys,os
for fn in sys.argv[1:]:
    t=open(fn,encoding='utf-8',errors='replace').read()
    meta={}
    for k in ['article:published_time','article:modified_time','og:title']:
        m=re.search(r'<meta[^>]+property="%s"[^>]+content="([^"]*)"'%re.escape(k),t)
        if m: meta[k]=m.group(1)
    m=re.search(r'<article(.*?)</article>',t,re.S)
    seg=m.group(1) if m else t
    seg=re.sub(r'<script.*?</script>|<style.*?</style>','',seg,flags=re.S)
    imgs=re.findall(r'<img[^>]+>',seg)
    alts=[ (re.search(r'alt="([^"]*)"',i) or [None,''])[1]+' | '+(re.search(r'src="([^"]*)"',i) or [None,''])[1].split('/')[-1] for i in imgs]
    txt=html.unescape(re.sub(r'<[^>]+>','\n',seg)); txt=re.sub(r'[ \t]+',' ',txt); txt=re.sub(r'\n\s*\n+','\n',txt)
    print('#####',fn,meta); print(txt[:int(os.environ.get('MAXC','4000'))]); print('IMGS:',alts[:12])
