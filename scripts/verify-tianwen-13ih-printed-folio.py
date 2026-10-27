#!/usr/bin/env python3
"""Replay GK3467 source-pixel folio anchors without promoting them to leaf loss."""
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'docs/research/TIANWEN-13IH-GK3467-PRINTED-FOLIO-DISCONTINUITY-R1.json'
SOURCE_PAGES = {
    4: '4d7ef0761513491099a236c39452ec5cea8ea42ca29b5e4d80a778383f55fa21',
    6: '260f2bbdba9b2eaade4b879e6a3643ef1e5b23cd7c7d5cd04e8c970e31eb99a8',
    7: 'aca88a6462829209de2a1f1f2aecdb2a39ec8970f9135db0f708e462bc8ac9c1',
}


def load(path=EVIDENCE):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def check(d, with_state=True):
    assert d['schema'] == 'TIANWEN-13IH-GK3467-SOURCE-PRINTED-FOLIO-DISCONTINUITY-R1'
    assert d['issue_id'] == 'TW-OPEN-0005'
    assert d['source']['pdf_sha256'] == 'b75009805dae9ccc22797c005bd5f32c7870a192945b503f6b3af3fbf14e1386'
    assert d['source']['exact_impression_year'] is None
    for dep in d['dependencies']:
        raw = (ROOT / dep['path']).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == dep['git_blob_sha']
    images = {}
    assert [p['pdf_page'] for p in d['native_pages']] == [4, 6, 7]
    for p in d['native_pages']:
        raw = (ROOT / p['path']).read_bytes()
        assert len(raw) == p['bytes']
        assert hashlib.sha256(raw).hexdigest() == p['sha256'] == SOURCE_PAGES[p['pdf_page']]
        im = Image.open(ROOT / p['path']).convert('RGB')
        assert list(im.size) == p['size']
        assert hashlib.sha256(im.tobytes()).hexdigest() == p['rgb_sha256']
        images[p['pdf_page']] = im
    rois = {r['key']: r for r in d['rois']}
    assert len(rois) == len(d['rois']) == 6
    for r in rois.values():
        im = images[r['pdf_page']]
        w, h = im.size
        expected = [w - 125, 1180, w - 20, 1510] if r['key'].endswith('FOLIO_NUMERAL') else [w - 125, 650, w - 20, 1570]
        assert r['bbox'] == expected
        assert hashlib.sha256(im.crop(r['bbox']).tobytes()).hexdigest() == r['rgb_sha256']
    rows = d['direct_folio_readings']
    assert [(r['pdf_page'], r['spread_side'], r['literal'], r['printed_number']) for r in rows] == [
        (4, 'RIGHT', '二', 2), (6, 'RIGHT', '十', 10), (7, 'RIGHT', '十一', 11)]
    for row in rows:
        assert row['context_roi'] == f"P{row['pdf_page']}_BANXIN_CONTEXT"
        assert row['numeral_roi'] == f"P{row['pdf_page']}_FOLIO_NUMERAL"
        assert rois[row['numeral_roi']]['literal'] == row['literal']
    page_steps = [b['pdf_page'] - a['pdf_page'] for a, b in zip(rows, rows[1:])]
    folio_steps = [b['printed_number'] - a['printed_number'] for a, b in zip(rows, rows[1:])]
    c = d['comparison']
    assert c['pdf_page_advances'] == page_steps == [2, 1]
    assert c['printed_folio_advances'] == folio_steps == [8, 1]
    assert c['one_folio_per_spread_model_residuals'] == [f - p for f, p in zip(folio_steps, page_steps)] == [6, 0]
    assert c['residual_units'] == 'PRINTED_NUMBER_MINUS_PDF_SPREAD_ADVANCE_NOT_CERTIFIED_LOST_LEAVES'
    assert c['p4_left_and_p5_right_folio_numerals'] is None
    assert c['p4_left_and_p5_right_numerals_inferred_from_neighbors'] is False
    assert c['point_of_loss_or_omission'] is None
    a = d['adjudication']
    assert a['local_printed_number_sequence_discontinuity_observed'] is True
    for k in ('physical_leaf_loss_proven', 'microfilm_omission_proven', 'digital_omission_proven',
              'binding_or_printed_misnumbering_excluded', 'table_title_or_initial_day_leaf_recovered',
              'all_53_pages_linewise_reviewed', 'prior_13IE_13IF_13IG_snapshots_overwritten'):
        assert a[k] is False, k
    assert a['physical_missing_leaf_count'] is a['ancient_units_or_G893_equivalence'] is None
    assert a['own_winter_field_identity'] == 'PROVISIONAL_PENDING_OWN_TITLE_RUBRIC'
    inv = d['invariants']
    assert inv['matrix'] == [222, 222] and inv['sources'] == 761 and inv['graph'] == [252, 238]
    assert inv['open_issues'] == 11 and inv['product'] == 'CLOSED'
    for k in ('new_physical_witnesses', 'new_registered_sources', 'new_graph_nodes', 'new_graph_edges', 'algorithm_reopens', 'candidate_collapses'):
        assert inv[k] == 0, k
    if with_state:
        state = load('docs/PROJECT-CURRENT-STATE-R1.json')
        ledger = load('docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json')
        assert tuple(map(int, state['schema_version'].split('.'))) >= (1, 887, 0)
        assert state['schema_version'] == ledger['binding']['reviewed_state_version']
        assert any(x.startswith('13IH ') for x in state['historical_audit']['current_focus'])
        issue = next(x for x in ledger['issues'] if x['id'] == d['issue_id'])
        assert issue['status'] == 'OPEN' and EVIDENCE in issue['source_refs']
        assert any(x.get('new_action_prefix') == '13IH' for x in issue['history'])
    return True


if __name__ == '__main__':
    check(load())
    print('TIANWEN_13IH_SOURCE_PRINTED_FOLIO_DISCONTINUITY_PASS')
