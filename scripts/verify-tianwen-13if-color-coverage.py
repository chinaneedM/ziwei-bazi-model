#!/usr/bin/env python3
"""Bind first-party color source bytes to bounded coverage claims."""
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'docs/research/TIANWEN-13IF-GK3467-COLOR-PAGES-AND-TABLE-START-COVERAGE-R1.json'


def load(path=EVIDENCE):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def check(data, with_state=True):
    from PIL import Image

    assert data['schema'] == 'TIANWEN-13IF-GK3467-PROVIDER-COLOR-ADJACENCY-AND-COVERAGE-R1'
    assert data['issue_id'] == 'TW-OPEN-0005' and data['catalog'] == 'GK03467_04'
    for dependency in data['dependencies']:
        raw = (ROOT / dependency['path']).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == dependency['git_blob_sha']
    spec = importlib.util.spec_from_file_location('source_acquirer_13if', ROOT / 'scripts/acquire-gk3467-listed-color-pages-13if.py')
    acquirer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(acquirer)
    contract = data['source_contract']
    seed = gzip.decompress((ROOT / contract['seed_html']).read_bytes())
    assert hashlib.sha256(seed).hexdigest() == contract['seed_uncompressed_sha256']
    page_ids = acquirer.listed_pages(seed.decode())
    assert len(page_ids) == contract['provider_listed_page_count'] == 104
    records = {}
    for source in data['acquisition_records']:
        raw = (ROOT / source['path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == source['sha256']
        entry = json.loads(raw)
        assert entry['all_provider_listed_page_ids'] == page_ids
        assert source['selected_pages'] == len(entry['selected_page_ids'])
        assert source['decoded_images'] == entry['source_original_images'] == sum(i['is_image'] for r in entry['records'] for i in r['images'])
        records[source['stage']] = entry
    initial, retry = records['initial'], records['retry']
    assert initial['selected_page_ids'] == page_ids[:20]
    failed = [r['page_id'] for r in initial['records'] if not any(i['is_image'] for i in r['images'])]
    assert failed == contract['failed_page_ids'] == retry['selected_page_ids'] == ['000a', '000b', '001a']
    assert contract['selected_initial_page_count'] == 20 and contract['decoded_initial_color_images'] == 17
    assert initial['source_original_images'] == 17 and retry['source_original_images'] == contract['retry_decoded_images'] == 0
    assert contract['failed_page_retry_count'] == 1
    for r in retry['records']:
        assert r['status'] is None and 'Connection reset by peer' in r['error'] and r['images'] == []
    pics = {}
    for image in data['images']:
        raw = (ROOT / image['image_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == image['jpeg_sha256']
        im = Image.open(ROOT / image['image_path']).convert('RGB')
        assert list(im.size) == image['size']
        assert hashlib.sha256(im.tobytes()).hexdigest() == image['rgb_sha256']
        renderer = gzip.decompress((ROOT / image['renderer_path']).read_bytes())
        assert hashlib.sha256(renderer).hexdigest() == image['renderer_uncompressed_sha256']
        assert acquirer.image_urls(renderer.decode(), image['page_id']) == [image['source_url']]
        source = next(r for r in initial['records'] if r['page_id'] == image['page_id'])
        assert source['images'][0]['sha256'] == image['jpeg_sha256']
        assert source['images'][0]['url'] == image['source_url']
        pics[image['page_id']] = im
    assert set(pics) == {'002b', '003a', '003b'}
    for roi in data['direct_context_rois']:
        im = pics[roi['page_id']]
        assert hashlib.sha256(im.crop(roi['bbox']).tobytes()).hexdigest() == roi['rgb_sha256']
    assert [(r['page_id'], r['literal']) for r in data['direct_context_rois']] == [('002b', '火星'), ('003a', '八日'), ('003b', '十六日')]
    transition = data['navigation_transition']
    assert (transition['before'], transition['after']) == ('002b', '003a')
    assert page_ids.index('003a') == page_ids.index('002b') + 1
    assert transition['adjacent_in_provider_page_list'] is True
    for key in ('all_104_pages_acquired', 'all_104_pages_linewise_collated', 'physical_folio_numbers_bound'):
        assert transition[key] is False
    scope = data['catalog_scope']
    catalog = gzip.decompress((ROOT / scope['source_path']).read_bytes())
    assert hashlib.sha256(catalog).hexdigest() == scope['uncompressed_sha256']
    for term in ('乙亥字', '[刊年未詳]', '1冊外缺'):
        assert term in catalog.decode()
    assert scope['note_scope'] == 'ONE_EXTANT_BOOK_OUTSIDE_WHICH_REST_OF_SET_MISSING_NOT_TARGET_LEAF_CONDITION'
    assert scope['exact_impression_year'] is None and scope['missing_leaves_within_book_proven'] is False
    adjudication = data['adjudication']
    for key in ('color_route_has_recovered_table_start', 'shared_upstream_digitization_omission_excluded', 'physical_leaf_loss_proven', 'source_page_images_prove_whole_work_absence', 'transport_failure_is_nonexistence_proof', 'prior_13ID_day_column_judgments_revised'):
        assert adjudication[key] is False
    grade = data['review_grade']
    assert grade['new_D16_numeric_adjudications'] == 0 and grade['title_rubric_and_initial_D7_recovered'] is False
    assert grade['this_copy_winter_field_identity'] == 'PROVISIONAL_PENDING_OWN_TITLE_AND_RUBRIC'
    assert grade['ancient_units_or_G893_field_equivalence'] is None
    invariants = data['invariants']
    for key in ('new_physical_witnesses', 'new_registered_sources', 'new_graph_nodes', 'new_graph_edges', 'algorithm_reopens', 'candidate_collapses'):
        assert invariants[key] == 0
    assert invariants['product'] == 'CLOSED' and invariants['G893_six'] == 'OPEN'
    if with_state:
        state = load('docs/PROJECT-CURRENT-STATE-R1.json')
        ledger = load('docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json')
        assert tuple(map(int, state['schema_version'].split('.'))) >= (1, 885, 0)
        assert state['schema_version'] == ledger['binding']['reviewed_state_version']
        assert any(x.startswith('13IF ') for x in state['historical_audit']['current_focus'])
        issue = next(x for x in ledger['issues'] if x['id'] == 'TW-OPEN-0005')
        assert issue['status'] == 'OPEN' and EVIDENCE in issue['source_refs']
        assert issue['next_action'].startswith('13IF CURRENT ACTION:') or 'ARCHIVED 13IF PRIOR ACTION:' in issue['next_action']
    return True


if __name__ == '__main__':
    assert check(load())
    print('TIANWEN_13IF_SOURCE_COLOR_NAVIGATION_AND_COVERAGE_PASS')
