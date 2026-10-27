#!/usr/bin/env python3
"""Read only page IDs and image URLs actually emitted by the GK3467 viewer."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
import hashlib
from html import unescape
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kyudb.snu.ac.kr'
BOOK = 'GK03467_04'
SOURCE = ROOT / 'docs/research/evidence/13fq/GK03467_04-renderer.html.gz'
SOURCE_SHA = 'd18eda904b621ffa309ee6ec299d43714c3346f9561d831b251ad1a8e5e25f3d'


def listed_pages(html):
    ids = re.findall(r"fn_goPageJumpWithMokIdxClear\('([^']+)'\)", html)
    if not ids or len(ids) > 200 or len(set(ids)) != len(ids):
        raise ValueError('Missing, excessive or duplicate provider page list')
    if any(not re.fullmatch(r'\d{3}[ab]', x) for x in ids):
        raise ValueError('Unrecognized provider page ID')
    return ids


def image_urls(html, requested_page):
    # Read only source-emitted download links, never synthesize an image path.
    links = re.findall(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", html)
    out = []
    for link in links:
        u = urljoin(BASE, unescape(link))
        parsed = urlparse(u)
        if parsed.scheme != 'https' or parsed.netloc != 'kyudb.snu.ac.kr' or parsed.path != '/ImageDown.do':
            continue
        fields = parse_qs(parsed.query)
        names = fields.get('imgFileNm', [])
        paths = fields.get('path', [])
        if len(names) != 1 or len(paths) != 1:
            continue
        name = names[0]
        if not re.fullmatch(BOOK + r'_[A-Z]+_0001_' + requested_page + r'\.jpg', name):
            continue
        expected_prefix = '/data01/stream/STH/IMG/' + BOOK + '/' + BOOK + '_0001/'
        if paths[0] != expected_prefix + name:
            continue
        if u not in out:
            out.append(u)
    return out


def select_pages(all_ids, requested=None):
    selected = requested if requested is not None else all_ids[:20]
    if not selected or len(selected) > 20 or len(set(selected)) != len(selected):
        raise ValueError('Invalid bounded page selection')
    if any(page not in all_ids for page in selected):
        raise ValueError('Page was not emitted in the provider list')
    return selected


def fetch(url, body=None, limit=25 * 1024 * 1024):
    request = Request(url, data=urlencode(body).encode() if body is not None else None)
    try:
        with urlopen(request, timeout=35) as response:
            data = response.read(limit + 1)
            if len(data) > limit:
                raise ValueError('Bounded response size exceeded')
            return data, response.status, response.headers.get('content-type'), None
    except HTTPError as error:
        return error.read(256 * 1024), error.code, error.headers.get('content-type'), str(error)
    except Exception as error:
        return b'', None, None, type(error).__name__ + ': ' + str(error)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--pages', nargs='+', help='Optional bounded subset of provider-listed IDs')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    raw = gzip.decompress(SOURCE.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    html = raw.decode('utf-8')
    all_ids = listed_pages(html)
    selected = select_pages(all_ids, args.pages)
    # These actions and form field names are published in this archived viewer.
    assert '/pf01/rendererImg.do' in html and 'name="page_no"' in html
    (args.output / 'seed-renderer.html').write_bytes(raw)

    def acquire(page):
        body = {'item_cd': 'STH', 'book_cd': BOOK, 'vol_no': '0001', 'page_no': page, 'add_page_no': ''}
        url = BASE + '/pf01/rendererImg.do'
        data, status, content_type, error = fetch(url, body, 2 * 1024 * 1024)
        name = 'renderer-' + page + '.html'
        (args.output / name).write_bytes(data)
        entry = {'page_id': page, 'request': {'url': url, 'body': body}, 'status': status,
                 'content_type': content_type, 'error': error, 'renderer_file': name,
                 'renderer_sha256': hashlib.sha256(data).hexdigest(), 'images': []}
        if status != 200:
            return entry
        for index, image_url in enumerate(image_urls(data.decode('utf-8', errors='replace'), page)):
            img, image_status, image_type, image_error = fetch(image_url)
            filename = 'source-' + page + '-' + str(index) + '.jpg'
            (args.output / filename).write_bytes(img)
            item = {'url': image_url, 'status': image_status, 'content_type': image_type,
                    'error': image_error, 'filename': filename, 'bytes': len(img),
                    'sha256': hashlib.sha256(img).hexdigest(), 'is_image': False}
            if image_status == 200:
                try:
                    from PIL import Image
                    im = Image.open(args.output / filename).convert('RGB')
                    item.update(is_image=True, size=list(im.size), rgb_sha256=hashlib.sha256(im.tobytes()).hexdigest())
                except Exception as decode_error:
                    item['decode_error'] = str(decode_error)
            entry['images'].append(item)
        return entry

    with ThreadPoolExecutor(max_workers=3) as executor:
        records = list(executor.map(acquire, selected))
    result = {'schema': 'TIANWEN-13IF-SOURCE-LISTED-COLOR-ACQUISITION-R1',
              'catalog': BOOK, 'volume': '0001', 'seed_renderer_sha256': SOURCE_SHA,
              'all_provider_listed_page_ids': all_ids, 'selected_page_ids': selected,
              'records': records, 'source_original_images': sum(x['is_image'] for r in records for x in r['images']),
              'glyph_adjudication': 'NOT_PERFORMED_BY_ACQUISITION_SCRIPT',
              'physical_leaf_loss_or_edition_inference': False}
    (args.output / 'acquisition.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'selected_pages': len(selected), 'decoded_source_images': result['source_original_images']}))


if __name__ == '__main__':
    main()
