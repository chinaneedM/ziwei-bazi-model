#!/usr/bin/env python3
"""Join prior sample evidence without expanding its historical scope."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = 'docs/research/MING-DATONG-YEHUOBIAN-12VM-BERLIN-PRIOR-SAMPLE-RECONCILIATION-R1.json'

def validate(record, latest, route, closure):
    def require(condition, message):
        if not condition:
            raise ValueError(message)
    ppn = record['object']['ppn']
    berlin = next(x for x in route['printed_copy_routes'] if x['item_id'] == 'BERLIN_1827_SAMPLES')
    require(ppn == latest['objects'][1]['ppn'] == berlin['ppn'] == closure['object'], 'object identity mismatch')
    require(record['object']['manifest_url'] == closure['manifest'] == berlin['standard_iiif_manifest_pattern'], 'manifest mismatch')
    require(record['object']['ddb_item'] == berlin['ddb_item'], 'DDB object mismatch')
    require(latest['objects'][0]['shelfmark'] == record['object']['shelfmark'], 'shelfmark mismatch')
    images = closure['all_original_jpegs_source_sha256']
    n = closure['manifest_canvas_count']
    require(n == 38 and closure['source_original_images_human_reviewed'] == n and len(images) == n, 'incomplete sample review')
    require({x['manifest_index'] for x in images} == set(range(1, n+1)), 'canvas coverage mismatch')
    require(len({x['sha256'] for x in images}) == n, 'duplicate image digest')
    require(record['historical_observation']['manifest_canvases'] == record['historical_observation']['images_reviewed'] == record['historical_observation']['source_image_hashes'] == n, 'historical counts mismatch')
    old = closure['bounded_target_adjudication']
    require(old['reviewed_all_38_public_sample_canvases'] is True and old['kaizao_louke_heading_identified_in_any_38'] is False, 'prior sample finding mismatch')
    require(record['historical_observation']['target_present_in_reviewed_samples'] is False, 'invented target finding')
    require(record['historical_observation']['scope'] == '38_PUBLIC_SAMPLE_CANVASES_ONLY', 'nonhit scope broadened')
    require(record['historical_observation']['full_1827_juan20_negative_claim_allowed'] is False and old['entire_1827_print_negative_claim_allowed'] is False, 'full print absence forbidden')
    require(record['current_session']['new_images_reviewed'] == 0 and record['current_session']['archive_bytes_redownloaded'] is False, 'new review not attested')
    arts = record['artifact_metadata_rechecked']
    require([(x['run_id'], x['artifact_id'], x['source_image_count']) for x in arts] == [(x['run_id'], x['artifact_id'], x['source_original_jpg_count']) for x in closure['runs']], 'artifact join mismatch')
    require(sum(x['source_image_count'] for x in arts) == n, 'artifact coverage mismatch')
    require(all(record['accounting'][k] == 0 for k in ['new_sources','new_images','new_target_glyph_votes','new_graph_nodes','new_graph_edges','algorithm_reopens']), 'unauthorized evidence promotion')
    return {'historical_samples_reviewed': n, 'new_target_glyph_votes': 0}

def verify(root=ROOT):
    record = json.loads((root/RECORD).read_text())
    docs = []
    for entry in record['prior_records']:
        raw = (root/entry['path']).read_bytes()
        sha = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if sha != entry['git_blob_sha']:
            raise ValueError('prior evidence changed; forward correction required')
        docs.append(json.loads(raw))
    return validate(record, *docs)

if __name__ == '__main__':
    print(json.dumps(verify()))
