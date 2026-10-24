#!/usr/bin/env python3
"""Replay public, provider-listed GK3467 child volumes; never infer book ordinals."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE = 'https://kyudb.snu.ac.kr'
CATALOGS = ('GK03467_02', 'GK03467_04')

def listed_volumes(raw, book):
    data = json.loads(raw)
    if data.get('RESULT') != 'SUCCESS':
        raise ValueError('Provider did not return a successful volume list')
    rows = data['volList']
    if not rows or len(rows) > 5:
        raise ValueError('Unexpected bounded child-volume count')
    seen = set()
    for row in rows:
        vol = row['VOL_NO']
        if (row['BOOK_CD'] != book or row['ITEM_CD'] != 'STH'
                or row['IS_PDF'] != 'Y' or len(vol) != 4 or not vol.isdigit()
                or vol in seen):
            raise ValueError('Unbound, duplicate, or unavailable provider volume')
        seen.add(vol)
    return [row['VOL_NO'] for row in rows]

def fetch(url, body=None):
    req = Request(url, data=urlencode(body).encode() if body is not None else None)
    with urlopen(req, timeout=90) as response:
        raw = response.read(64 * 1024 * 1024 + 1)
        if len(raw) > 64 * 1024 * 1024:
            raise ValueError('Response exceeds bounded acquisition size')
        return raw

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    for book in CATALOGS:
        catalog = fetch(BASE + '/book/view.do?' + urlencode({'book_cd': book}))
        if ("fn_mfPdfPopShow('" + book + "')").encode() not in catalog:
            raise ValueError('Missing exact provider microfilm entry point')
        (args.output / (book + '-catalog.html')).write_bytes(catalog)
        # The embedded fn_mfPdfPopShow publishes this POST and field name.
        raw = fetch(BASE + '/ajax/book/mfPdfList.do', {'book_cd': book})
        (args.output / (book + '-volumes.json')).write_bytes(raw)
        for vol in listed_volumes(raw, book):
            url = BASE + '/book/mfPdf.do?' + urlencode({'book_cd': book, 'vol_no': vol})
            pdf = fetch(url)
            if not pdf.startswith(b'%PDF-'):
                raise ValueError('Provider response is not a PDF: ' + book + '/' + vol)
            name = book + '-' + vol + '.pdf'
            (args.output / name).write_bytes(pdf)
            records.append({'book_cd': book, 'vol_no': vol, 'url': url,
                            'filename': name, 'bytes': len(pdf),
                            'sha256': hashlib.sha256(pdf).hexdigest()})
    (args.output / 'acquisition.json').write_text(
        json.dumps({'records': records, 'scope': 'SOURCE_LISTED_DIGITAL_VOLUMES_ONLY',
                    'physical_book_numbers_inferred': False}, ensure_ascii=False, indent=2) + '\n')
    print('Acquired', len(records), 'provider-listed PDF volumes; no original glyph adjudication.')

if __name__ == '__main__':
    main()
