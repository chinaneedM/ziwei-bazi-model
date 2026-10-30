#!/usr/bin/env python3
"""Read public NAJ catalog/viewer links; retain responses, never infer image availability."""
import hashlib, json, re, unicodedata, urllib.error, urllib.parse, urllib.request
from html.parser import HTMLParser
from pathlib import Path

OUT = Path('13lj-naaj-firstparty-output')
HOST = 'www.digital.archives.go.jp'
CATALOGS = [('281-0037', 'https://www.digital.archives.go.jp/file/3602570', '明史10'),
            ('281-0038', 'https://www.digital.archives.go.jp/file/en/3610285', '明史 志第11-13')]

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.scripts=[]; self.current=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a': self.current=[a.get('href',''), '', a]
        if tag=='script' and a.get('src'): self.scripts.append(a['src'])
    def handle_data(self, data):
        if self.current is not None: self.current[1]+=data
    def handle_endtag(self, tag):
        if tag=='a' and self.current is not None:
            self.links.append(self.current); self.current=None

def allowed(url):
    p=urllib.parse.urlsplit(url)
    return p.scheme=='https' and p.netloc==HOST

def fetch(url, name, results):
    assert allowed(url), 'Only observed public same-provider URLs allowed'
    row={'url':url, 'file':name}; results.append(row)
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'TianwenHistoricalAudit/1.0 (public source provenance research)'})
        with urllib.request.urlopen(req, timeout=40) as r:
            body=r.read(8_000_001); assert len(body)<=8_000_000
            row.update(status=r.status, final_url=r.url, content_type=r.headers.get('Content-Type'))
        (OUT/name).write_bytes(body)
        row.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        return body.decode('utf-8','replace')
    except Exception as e:
        row['error']=type(e).__name__+': '+str(e)[:400]
        return ''

def parse(s):
    p=Links();p.feed(s);return p

def norm(s): return ''.join(unicodedata.normalize('NFKC',s).split())

def main():
    OUT.mkdir(exist_ok=True)
    result={'evidence_grade':'PUBLIC_PROVIDER_ROUTE_PROBE_NOT_GLYPH_OR_OPTICAL_ORIGINAL',
            'historical_winners_added':0,'no_ocr':True,'fetches':[], 'holdings':[]}
    for holding,url,target in CATALOGS:
        text=fetch(url, holding+'-catalog.html',result['fetches']); p=parse(text)
        row={'holding':holding,'target_title':target,'matched_catalog_anchors':[], 'viewer_anchors':[]};result['holdings'].append(row)
        matches=[a for a in p.links if norm(a[1])==norm(target)]
        row['matched_catalog_anchors']=matches
        for n,a in enumerate(matches[:2]):
            item=urllib.parse.urljoin(url,a[0])
            if not allowed(item):continue
            s=fetch(item,holding+f'-item{n}.html',result['fetches']); q=parse(s)
            viewers=[a for a in q.links if '/img/' in a[0] or '/DAS/' in a[0] or '/pdf/' in a[0]]
            row['viewer_anchors'].extend(viewers)
            for j,v in enumerate(viewers[:3]):
                vu=urllib.parse.urljoin(item,v[0])
                if not allowed(vu):continue
                vs=fetch(vu,holding+f'-viewer{j}.html',result['fetches']);vp=parse(vs)
                row.setdefault('viewer_scripts',[]).extend(vp.scripts)
                for k,src in enumerate(vp.scripts[:20]):
                    su=urllib.parse.urljoin(vu,src)
                    if allowed(su):fetch(su,holding+f'-viewer{j}-script{k}.js',result['fetches'])
        # Save relevant inline viewer/item identifiers even when the catalog uses JS buttons.
        row['inline_route_lines']=[line[:2500] for line in text.splitlines() if any(t in line for t in ['/img/','openImage','listPhoto','imageId','contentId'])][:35]
        for k,src in enumerate(p.scripts[:15]):
            su=urllib.parse.urljoin(url,src)
            if allowed(su):fetch(su,holding+f'-catalog-script{k}.js',result['fetches'])
    faq=fetch('https://www.digital.archives.go.jp/faq','provider-faq.html',result['fetches'])
    (OUT/'route-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
