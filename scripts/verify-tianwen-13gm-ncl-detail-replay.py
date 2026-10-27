#!/usr/bin/env python3
"""Offline source-byte replay of public NCL detail metadata, never a glyph oracle."""
import gzip
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/research/TIANWEN-13GM-NCL03130-DETAIL-BYTE-REPLAY-R1.json'

class DetailParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.cells = []; self.rows = []; self.cell = None; self.controls = {}
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'tr': self.cells = []
        if tag in ('th', 'td'): self.cell = []
        if a.get('id') in ('AddRead', 'AddUse'):
            assert a['id'] not in self.controls, 'duplicate application identity'
            self.controls[a['id']] = a
    def handle_data(self, data):
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag in ('th', 'td') and self.cell is not None:
            self.cells.append(' '.join(''.join(self.cell).split())); self.cell = None
        if tag == 'tr' and len(self.cells) == 2: self.rows.append(tuple(self.cells))

def parse(raw):
    p = DetailParser(); p.feed(raw.decode('utf-8')); p.close()
    fields = {}
    for k, v in p.rows:
        assert k not in fields, 'duplicate metadata field'
        fields[k] = v
    return fields, p.controls

def check(e, raw):
    assert e['grade'] == 'FIRSTPARTY_CATALOG_HTML_BYTES_NOT_ORIGINAL_FOLIO'
    assert len(raw) == e['source']['bytes']
    assert hashlib.sha256(raw).hexdigest() == e['source']['sha256']
    fields, controls = parse(raw)
    prior = json.loads((ROOT/e['prior_evidence']).read_text(encoding='utf-8'))
    assert e['metadata'] == prior['firstparty_item_metadata']
    for k, v in e['metadata'].items():
        if k != 'provider_record_id': assert fields[k] == v, k
    assert e['metadata']['provider_record_id'] == '52884'
    for name in ('AddRead', 'AddUse'):
        assert controls[name]['data-id'] == '52884'
        assert controls[name]['data-number'] == '03130'
        assert controls[name]['data-title'] == '高麗史'
    assert controls['AddRead']['data-quantity'] == '40冊'
    assert '缺卷朱記于首' in fields['題跋釋文']
    assert '光緒甲辰' in fields['題跋釋文'] and '錢塘丁君' in fields['題跋釋文']
    assert e['catalog_colophon'] == fields['題跋釋文']
    assert all(v is None for v in e['unresolved'].values())
    assert e['historical_guards'] == prior['historical_guards']
    assert all(v is False for v in e['external_actions'].values())
    assert not e['transmission_impact']['edges_supported']
    assert e['new_original_glyphs'] == e['new_physical_witnesses'] == 0
    return True

if __name__ == '__main__':
    e = json.loads(EVIDENCE.read_text(encoding='utf-8'))
    check(e, gzip.decompress((ROOT/e['source']['archive']).read_bytes()))
    print('13GM_PASS_SOURCE_HTML_METADATA_REPLAY_NO_FOLIO_UPGRADE')
