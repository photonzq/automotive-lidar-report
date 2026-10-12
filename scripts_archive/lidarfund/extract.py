import re,html,sys,os
def extract(fn):
    t=open(fn,encoding='utf-8',errors='replace').read()
    meta={}
    for k in ['article:published_time','article:modified_time','og:title']:
        m=re.search(r'<meta[^>]+property="%s"[^>]+content="([^"]*)"'%re.escape(k),t)
        if m: meta[k]=m.group(1)
    body=re.sub(r'<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>','',t,flags=re.S)
    # try to isolate main post content
    m=re.search(r'<div class="the_content_wrapper[^"]*">(.*?)(?:<div class="section section-post-footer|<section class="section section-post-related|Related\s*</?)',body,re.S)
    seg=m.group(1) if m else body
    txt=html.unescape(re.sub(r'<[^>]+>','\n',seg))
    txt=re.sub(r'[ \t]+',' ',txt)
    txt=re.sub(r'\n\s*\n+','\n',txt)
    return meta,txt
if __name__=='__main__':
    for fn in sys.argv[1:]:
        meta,txt=extract(fn)
        print('#####',fn,meta)
        print(txt[:int(os.environ.get('MAXC','6000'))])
