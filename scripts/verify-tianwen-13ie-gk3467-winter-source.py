#!/usr/bin/env python3
"""Verify native source pixels and fail-closed GK3467 field/edition claims."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = 'docs/research/TIANWEN-13IE-GK3467-WINTER-D16-ORIGINAL-AND-HEADER-COVERAGE-R1.json'


def load(path=EVIDENCE):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def check(data, with_state=True):
    from PIL import Image

    assert data['schema'] == 'TIANWEN-13IE-GK3467-WINTER-CANDIDATE-D15-D17-DIRECT-PIXELS-R1'
    assert data['issue_id'] == 'TW-OPEN-0005'
    deps = {}
    for item in data['dependencies']:
        raw = (ROOT / item['path']).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == item['git_blob_sha']
        deps[item['key']] = json.loads(raw)
    source = data['source']
    prior = next(x for x in deps['FQ']['acquisition']['records'] if x['book_cd'] == 'GK03467_04')
    assert source['pdf_sha256'] == prior['sha256']
    assert source['pdf_bytes'] == prior['bytes'] and source['pdf_pages'] == prior['pdf_pages']
    assert (source['catalog'], source['digital_volume'], source['physical_book_number'], source['work_juan']) == ('GK03467_04', '0001', 6, 52)
    assert source['physical_impression_year'] is None and source['independent_early_edition_proven'] is False
    pages = {}
    for page in data['native_pages']:
        raw = (ROOT / page['path']).read_bytes()
        assert len(raw) == page['bytes'] and hashlib.sha256(raw).hexdigest() == page['raw_sha256']
        im = Image.open(ROOT / page['path']).convert('RGB')
        assert list(im.size) == page['size'] == [2432, 2064]
        assert hashlib.sha256(im.tobytes()).hexdigest() == page['rgb_sha256']
        pages[page['page_1based']] = im
    assert set(pages) == {3, 4, 5}
    rois = {r['key']: r for r in data['rois']}
    assert len(rois) == 8
    for roi in rois.values():
        im = pages[roi['page_1based']]
        x0, y0, x1, y1 = roi['bbox']
        assert 0 <= x0 < x1 <= im.width and 0 <= y0 < y1 <= im.height
        assert hashlib.sha256(im.crop((x0, y0, x1, y1)).tobytes()).hexdigest() == roi['rgb_sha256']
    expected = [(15, '十五日', '五分二一七六', 52176), (16, '十六日', '五分一三六二', 51362), (17, '十七日', '五分二五四八', 52548)]
    for row, (day, heading, literal, number) in zip(data['direct_rows'], expected, strict=True):
        assert row['printed_day'] == day and row['literal'] == literal and row['local_integer'] == number
        assert row['header_key'] == f'D{day}_HEADER' and row['numeric_key'] == f'D{day}_A'
        assert rois[row['header_key']]['literal'] == heading and rois[row['numeric_key']]['literal'] == literal
    nums = [row['local_integer'] for row in data['direct_rows']]
    arithmetic = data['local_arithmetic']
    assert [nums[1] - nums[0], nums[2] - nums[1]] == arithmetic['observed_neighbor_deltas'] == [-814, 1186]
    assert (nums[0] + nums[2]) // 2 == arithmetic['equal_186_step_counterfactual_integer'] == 52362
    assert arithmetic['counterfactual_attested_in_this_source'] is False
    assert arithmetic['unit'] == 'ENCODED_LOCAL_DIGIT_GRID_ONLY_NOT_CERTIFIED_HISTORICAL_UNIT'
    field = data['field_identity']
    assert field['winter_table_title_on_inspected_pages'] is None
    assert field['technical_A_rubric_on_inspected_pages'] is None
    assert field['original_G893_same_field_or_unit'] is None
    assert field['cross_source_field_equivalence'] == 'PROVISIONAL_PENDING_THIS_COPY_TABLE_START'
    coverage = data['source_coverage']
    assert coverage['start_title_and_days_0_to_7'] == 'NOT_LOCATED_IN_REVIEWED_ADJACENT_TRANSITION'
    assert coverage['p3_left'] == coverage['p4_right'] == 'PLANETARY_TABLE'
    assert coverage['p4_left_first_visible_day'] == '八日'
    for key in ('full_53_pages_linewise_reviewed', 'digital_omission_proven', 'physical_leaf_loss_proven'):
        assert coverage[key] is False
    assert coverage['missing_number_of_leaves'] is None
    assert data['comparison']['four_independent_editions_or_stemmatic_votes'] is False
    assert data['comparison']['13ID_source_specific_layout_judgments_revised'] is False
    firewalls = data['firewalls']
    for key in ('new_physical_witnesses', 'new_registered_sources', 'new_graph_nodes', 'new_graph_edges', 'algorithm_reopens', 'candidate_collapses'):
        assert firewalls[key] == 0
    assert firewalls['product'] == 'CLOSED' and firewalls['G893_six'] == 'OPEN'
    assert firewalls['NCL03130_summer_D14'] is None and firewalls['D5_zero_five'] == 'OPEN'
    if with_state:
        state = load('docs/PROJECT-CURRENT-STATE-R1.json')
        ledger = load('docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json')
        assert tuple(map(int, state['schema_version'].split('.'))) >= (1, 884, 0)
        assert state['schema_version'] == ledger['binding']['reviewed_state_version']
        assert any(x.startswith('13IE ') for x in state['historical_audit']['current_focus'])
        issue = next(x for x in ledger['issues'] if x['id'] == 'TW-OPEN-0005')
        assert issue['status'] == 'OPEN' and EVIDENCE in issue['source_refs']
        assert any(h.get("revision_id", "").startswith("TW-OPEN-0005-13IE-") and "next_action" in h.get("changed_fields", []) for h in issue["history"])
        assert any(x.get('revision_id', '').startswith('TW-OPEN-0005-13IE-') for x in issue['history'])
    return True


def check_pdf(data, path):
    import fitz

    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == data['source']['pdf_sha256']
    pdf = fitz.open(path)
    assert len(pdf) == data['source']['pdf_pages']
    for page in data['native_pages']:
        xref = page['xref']
        assert xref in [x[0] for x in pdf[page['page_1based'] - 1].get_images(full=True)]
        assert pdf.xref_stream_raw(xref) == (ROOT / page['path']).read_bytes()
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-pdf', type=Path)
    args = parser.parse_args()
    data = load()
    assert check(data)
    if args.source_pdf:
        assert check_pdf(data, args.source_pdf)
    print('TIANWEN_13IE_GK3467_DIRECT_PIXELS_AND_HEADER_COVERAGE_PASS')
