#!/usr/bin/env python3
"""13GN: separate PDF-rendered pixels from the original embedded JPEG grid."""
import argparse
import hashlib
import io
import json
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
E = ROOT/'docs/research/TIANWEN-13GN-NCL03130-EMBEDDED-IMAGE-GRADE-ERRATUM-R1.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def check(e, pdf_path=None):
    assert e['grade'] == 'DIRECT_EMBEDDED_JPEG_AND_EXACT_PRIOR_RENDER_REPLAY_NO_NEW_GLYPH'
    assert e['old_images_reclassified_as'] == 'PDF_RENDER_MATRIX_3_1_NOT_EMBEDDED_NATIVE_GRID'
    assert e['old_records_preserved'] is True
    assert e['source']['sha256'] == '3c2a5621fb3f4eabc593020bcde12a38f6ecdae2842940dec12d5a3a56afd32e'
    assert e['source']['bytes'] == 50735589
    assert e['new_physical_witnesses'] == e['new_original_glyphs'] == 0
    assert all(v is None for v in e['unresolved'].values())
    assert e['historical_guards'] == {'d5':'〇/五_UNRESOLVED','g893_six':'OPEN','legacy_13ei':'RETRACTED','algorithm_reopens':0,'candidate_collapses':0}
    assert not e['transmission_impact']['edges_supported']
    assert [r['page'] for r in e['pages']] == [74,75,76]
    gd=json.loads((ROOT/e['prior_gd']).read_text(encoding='utf-8'))
    fv=json.loads((ROOT/e['prior_fv']).read_text(encoding='utf-8'))
    for row in e['pages']:
        page=row['page'];raw=row['embedded'];old=row['previous_render']
        assert raw['size'] == [1754,{74:1173,75:1179,76:1175}[page]]
        assert raw['xref'] == {74:291,75:295,76:299}[page]
        assert old['matrix'] == [3.1,3.1]
        assert old['size'] == [1305,{74:873,75:878,76:875}[page]]
        prior=next((p for p in gd['source']['original_page_images'] if p['page']==page),None)
        if prior:
            assert old['png_sha256'] == prior['png_sha256']
            assert old['rgb_sha256'] == prior['rgb_sha256']
        else:
            assert old['png_sha256'] == fv['source']['png_sha256']
            assert old['rgb_sha256'] == fv['source']['native_rgb_sha256']
        assert row['old_roi_coordinates_cannot_be_reused_directly'] is True
        for roi in row['review_rois']:
            assert roi['complete_original_literal'] is None
            assert roi['coordinate_grid'] == 'EMBEDDED_JPEG_PIXELS'
            b=(ROOT/roi['file']).read_bytes();im=Image.open(io.BytesIO(b)).convert('RGB')
            box=roi['xyxy'];assert im.size==(box[2]-box[0],box[3]-box[1])
            assert sha(b)==roi['png_sha256'] and sha(im.tobytes())==roi['rgb_sha256']
    if pdf_path:
        import fitz
        b=Path(pdf_path).read_bytes();assert len(b)==e['source']['bytes'] and sha(b)==e['source']['sha256']
        with fitz.open(stream=b,filetype='pdf') as pdf:
            assert len(pdf)==189
            for row in e['pages']:
                page=pdf[row['page']-1];info=page.get_images(full=True)
                assert len(info)==1 and info[0][0]==row['embedded']['xref']
                original=pdf.extract_image(info[0][0])['image']
                assert len(original)==row['embedded']['jpeg_bytes'] and sha(original)==row['embedded']['jpeg_sha256']
                im=Image.open(io.BytesIO(original)).convert('RGB')
                assert list(im.size)==row['embedded']['size'] and sha(im.tobytes())==row['embedded']['rgb_sha256']
                rendered=page.get_pixmap(matrix=fitz.Matrix(3.1,3.1),alpha=False)
                assert sha(rendered.samples)==row['previous_render']['rgb_sha256']
                assert sha(rendered.tobytes('png'))==row['previous_render']['png_sha256']
                for roi in row['review_rois']:
                    assert sha(im.crop(roi['xyxy']).tobytes())==roi['rgb_sha256']
    return True
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-pdf',type=Path);a=p.parse_args()
    check(json.loads(E.read_text(encoding='utf-8')),a.source_pdf)
    print('13GN_PASS_'+('EMBEDDED_AND_PRIOR_RENDER_SOURCE_REPLAY' if a.source_pdf else 'SEALED_ROI_AND_GRADE_FIREWALL'))
