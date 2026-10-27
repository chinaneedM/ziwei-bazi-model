#!/usr/bin/env python3
"""Forward erratum: GK5553 copy-to-juan attribution and concurrent HEAD recovery."""
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH="docs/research/TIANWEN-13IO-GK5553-CROSSWALK-AND-CONCURRENT-HANDOFF-ERRATUM-R1.json"
def read(path=PATH): return json.loads((ROOT/path).read_text(encoding='utf-8'))
def check(d, with_state=True):
    assert d['schema']=='TIANWEN-13IO-GK5553-CROSSWALK-AND-CONCURRENT-HANDOFF-ERRATUM-R1'
    assert d['issue_id']=='TW-OPEN-0005'
    old=d['historical_erratum']; e=d['snu_firstparty']; paper=d['journal_2020']; c=d['adjudication']
    assert old['prior_batch']=='13IN' and old['prior_asserted_juan']==[81,82,83]
    assert old['new_status']=='RETRACTED_UNBOUND_COPY_TO_JUAN_CROSSWALK' and old['original_13in_file_preserved'] is True
    assert e['supplemental_manuscript_books']==[8,26,29] and e['book_29_juan_81_83_explicitly_bound'] is False
    assert e['work_toc_juan_81_83']=='兵志' and e['work_toc_is_book29_physical_inventory'] is False
    assert e['microfilm_group']=='M/F74-102-17-4' and e['microfilm_books_range']==[25,31]
    assert paper['printed_page']==100 and paper['note']==6 and paper['unused_alternate']=='奎5553'
    assert paper['potential_alternate_juan']==[31,77,78,79,81,82]
    assert paper['book29_mapped_to_juan81_83_by_original_page'] is False and paper['raw_pdf_sha256'] is None
    assert c['retracted_claim']=='13IN_SOURCE_OFFICIAL_BOOK29_CONTAINS_JUAN81_83'
    assert c['physical_copy_material_conflict_between_the_two_proven'] is False
    for k in ['new_original_leaf_images','new_source_registry_records','new_genealogy_nodes','new_genealogy_edges','algorithm_reopen_count']:
        assert c[k]==0
    assert d['invariants']=={'matrix':[222,222],'external_sources':761,'graph':[252,238],'risks':11,'chart':'CLOSED','algorithm_reopens':0,'candidate_collapses':0}
    if with_state:
        s=read('docs/PROJECT-CURRENT-STATE-R1.json'); l=read('docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json')
        old_source=read(old['frozen_evidence_json'])
        assert old_source['snu_firstparty']['book29_juan']==[81,82,83]  # immutable prior evidence, now explicitly retracted
        assert s['schema_version']==s['historical_audit']['research_omission_guard']['reviewed_state_version']==l['binding']['reviewed_state_version']
        assert tuple(map(int,s['schema_version'].split('.'))) >= (1,894,0)
        assert l['binding']['source_focus_count']==len(s['historical_audit']['current_focus'])
        assert any(x.startswith('13IO ') for x in s['historical_audit']['current_focus'])
        assert s['historical_audit']['latest_batch_doc']=='docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-BAZI-MING-DATONG-YEHUOBIAN-SHLIB-FIRSTPARTY-AND-OLD20-ATLAS-QD.md'
        issue=next(x for x in l['issues'] if x['id']=='TW-OPEN-0005')
        assert issue['status']=='OPEN' and PATH in issue['source_refs']
        assert any(x.get('new_action_prefix')=='13IO' for x in issue['history'])
        assert len(l['issues'])==11 and set(l['checkpoint_log'][-1]['reviewed_issue_ids'])=={x['id'] for x in l['issues']}
        root=(ROOT/'docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json').read_bytes()
        manifest=read('docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json')
        digest=hashlib.sha1(b'blob '+str(len(root)).encode('ascii')+b'\0'+root).hexdigest()
        assert digest==manifest['root_registry_blob_sha']
        assert json.loads(root)['access_date']=='2026-10-09'
        assert s['invariants']['deterministic_fusion_chart_product_r1']=='CLOSED'
    return True
if __name__=='__main__':
    assert check(read())
    print('TIANWEN_13IO_SOURCE_SCOPE_AND_CONCURRENT_STATE_RECOVERY_PASS')
