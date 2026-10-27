#!/usr/bin/env python3
"""13FC: capture only HTML-emitted first-party NIKH viewer JavaScript.

Do not invent image modes, infer original glyphs, or cross physical-copy identities.
"""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import urllib.parse
import urllib.request
import urllib.error

ARTICLE_ID = 'kr_052_0010_0010_0020_0020'
FIRST_IMAGE_ID = 'kr_052_1055'
BASE = 'https://db.history.go.kr'
VIEWER_URL = BASE + '/common/imageViewer.do?' + urllib.parse.urlencode({'levelId': ARTICLE_ID, 'begin': FIRST_IMAGE_ID})
EXACT_VIEWER_SHA = '25ecd6a4672bdaa29d188409c6c10e1c7050cc7481b54c6f9cf3fb1417f28342'
ALLOWED_JS_PATHS = ('/resources/imageViewer/js/html5_viewer.config.js', '/resources/imageViewer/js/html5_viewer.js')
PATTERN = re.compile(r'imageProxy|mode\s*[=:]|download|save_btn|filePath|viewerLoader|addFile|imageSrc|imageUrl|imgUrl|imgPath', re.I)
OUT = Path(os.environ.get('TIANWEN_PROBE_OUT', '/tmp/tianwen-13fc-probe'))

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.src = []
    def handle_starttag(self, tag, attrs):
        if tag.lower() == 'script':
            d = dict(attrs)
            if d.get('src'):
                self.src.append(d['src'])

def permitted_urls(html):
    p = Scripts()
    p.feed(html)
    out = []
    for src in p.src:
        absolute = urllib.parse.urljoin(VIEWER_URL, src)
        u = urllib.parse.urlsplit(absolute)
        if (u.scheme != 'https' or u.hostname != 'db.history.go.kr' or
            u.port is not None or u.username is not None or
            u.path not in ALLOWED_JS_PATHS or
            u.query != 'ver=2.0' or u.fragment):
            continue
        if absolute not in out:
            out.append(absolute)
    return out

def fetch(url, limit=1_300_000):
    record = {'url': url, 'http': None, 'bytes': 0, 'sha256': None, 'status': None}
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Tianwen-Historical-Provenance-13FC/1.0',
            'Accept': 'text/html,application/javascript,text/javascript,*/*;q=0.8'})
        with urllib.request.urlopen(req, timeout=22) as r:
            record['http'] = r.status
            if urllib.parse.urlsplit(r.geturl()).hostname != 'db.history.go.kr':
                record['status'] = 'REDIRECT_OUTSIDE_FIRST_PARTY'
                return record, None
            data = r.read(limit + 1)
            record['bytes'] = len(data)
            if len(data) > limit:
                record['status'] = 'OVER_BYTE_CAP'
                return record, None
            record['sha256'] = hashlib.sha256(data).hexdigest()
            record['status'] = 'PUBLIC_SOURCE_CAPTURED' if r.status == 200 else 'HTTP_NON_200'
            return record, data if r.status == 200 else None
    except urllib.error.HTTPError as e:
        record['http'] = e.code
        record['status'] = 'HTTP_ERROR'
    except Exception as e:
        record['status'] = 'TRANSPORT_ERROR'
        record['error_type'] = type(e).__name__
    return record, None

def contexts(js, cap=18, flank=170):
    found = []
    for m in PATTERN.finditer(js):
        if len(found) >= cap:
            break
        found.append({
            'token': m.group(0), 'character_offset': m.start(),
            'context': js[max(0, m.start()-flank):min(len(js), m.end()+flank)]})
    return found

def run():
    OUT.mkdir(parents=True, exist_ok=True)
    v, raw = fetch(VIEWER_URL)
    result = {
        'schema': 'TIANWEN-13FC-NIKH-JUAN52-SOURCE-EMITTED-VIEWER-SCRIPT-PROBE-R1',
        'date': '2026-10-24', 'issue_id': 'TW-OPEN-0005',
        'viewer': v, 'expected_previous_sha256': EXACT_VIEWER_SHA,
        'same_viewer_sha_as_13fb': bool(raw and v['sha256'] == EXACT_VIEWER_SHA),
        'scripts_declared_by_source': [], 'script_reads': [],
        'high_resolution_original_image_acquired': False,
        'physical_copy_and_folio_bound': False,
        'source_original_target_glyph_adjudicated': False,
        'non_source_emitted_endpoint_requests': 0,
        'numerical_fields_unresolved': ['D5','D30','winter_D16','G893_six_controls']}
    if raw:
        urls = permitted_urls(raw.decode('utf-8', 'replace'))
        result['scripts_declared_by_source'] = urls
        (OUT / 'exact-viewer.html').write_bytes(raw)
        for i, url in enumerate(urls[:2]):
            meta, data = fetch(url)
            if data is not None:
                (OUT / f'official-viewer-script-{i+1:02d}.js').write_bytes(data)
                meta['source_code_contexts'] = contexts(data.decode('utf-8', 'replace'))
            result['script_reads'].append(meta)
    (OUT / 'probe-result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'script_reads'}, ensure_ascii=False))
    for x in result['script_reads']:
        print('SOURCE_SCRIPT', x['url'], x['status'], x['sha256'], 'contexts=', len(x.get('source_code_contexts', [])))
    assert result['non_source_emitted_endpoint_requests'] == 0

if __name__ == '__main__':
    run()
