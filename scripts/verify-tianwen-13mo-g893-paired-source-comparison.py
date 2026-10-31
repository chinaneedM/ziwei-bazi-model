#!/usr/bin/env python3
"""13MO original paired-column regression; never promote mere numerical equality to lineage."""
from pathlib import Path
from decimal import Decimal
import json,re
R=Path(__file__).resolve().parents[1]
E=R/"docs/research/TIANWEN-13MO-G893-ZHOU1569-PAIRED-LANE-SOURCE-COMPARISON-R1.json"
S=R/"docs/PROJECT-CURRENT-STATE-R1.json"
L=R/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def check(e,s,l):
    assert e["schema"]=="TIANWEN-13MO-G893-ZHOU1569-PAIRED-LANE-SOURCE-COMPARISON-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    a=e["archive"]
    assert a["run_id"]==41144025711 and a["artifact_id"]==13019278183
    assert a["zip_sha256"]=="1d8f10da7c27411bf38ad635494a1b9f4e700fb76cb37b2a7541c075a0ca9835"
    assert a["new_physical_copy"] is False and a["ocr"] is False
    g=e["g893"]
    assert g["jpeg_sha256"]=="f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"
    assert g["header_minor_unit_glyph"]=="少"
    assert g["observed_header_terms"]==["積日","日差","盈縮加分","盈縮積度"]
    assert len(g["bounded_native_rgb_crops"])==3 and len(e["zhou1569"]["bounded_native_rgb_crops"])==2
    for c in g["bounded_native_rgb_crops"]+e["zhou1569"]["bounded_native_rgb_crops"]:
        assert re.fullmatch("[0-9a-f]{64}",c["rgb_sha256"])
        assert len(c["box"])==4 and c["box"][2]>c["box"][0] and c["box"][3]>c["box"][1]
    assert e["zhou1569"]["pdf_sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
    rows=e["paired_column_transcriptions"]
    assert [(r["day"],r["short"],r["long"]) for r in rows]==[(15,"5.2176","434.8249"),(16,"5.2362","429.6073"),(17,"5.2548","424.3711")]
    sh=[Decimal(r["short"]) for r in rows];lg=[Decimal(r["long"]) for r in rows]
    assert sh[1]-sh[0]==sh[2]-sh[1]==Decimal("0.0186")
    assert lg[0]-sh[0]==lg[1] and lg[1]-sh[1]==lg[2]
    p=e["limits"]
    for k in ("zhous_1569_physical_impression_catalog_independence_bound","full_field_header_unit_radix_day_anchor_identity_bound","direct_copying_or_same_archetype_proved"):
        assert p[k] is False
    for k in ("historical_cross_original_six_target_winners","registered_sources_added","new_copies_added","matrix_rows_changed","graph_nodes_changed","graph_edges_changed","algorithm_reopens"):
        assert p[k]==0
    assert p["deterministic_product"]=="CLOSED"
    assert tuple(map(int,s["schema_version"].split(".")))>=(1,977,0)
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    focus=s["historical_audit"]["current_focus"]
    assert any(x.startswith("13MO ") for x in focus)
    assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
    assert l["binding"]["source_focus_count"]==len(focus)
    i=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
    assert i["priority"]=="P0" and i["status"]=="OPEN"
    assert "docs/research/TIANWEN-13MO-G893-ZHOU1569-PAIRED-LANE-SOURCE-COMPARISON-R1.json" in i["source_refs"]
    assert any(x["revision_id"]=="TW-OPEN-0005-13MO-PAIRED-SOURCE-COMPARISON-20261031" for x in i["history"])
    assert any(x["id"]=="OMISSIONS-13MO-G893-PAIRED-SOURCE-COMPARISON-20261031" for x in l["checkpoint_log"])
    assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    return {"status":"PASS","days":[15,16,17],"source_scope":"PAIRED_NUMERIC_IMAGE_CONGRUENCE_ONLY","six_winners":0}
if __name__=="__main__":
    print(json.dumps(check(json.loads(E.read_text(encoding="utf-8")),json.loads(S.read_text(encoding="utf-8")),json.loads(L.read_text(encoding="utf-8"))),ensure_ascii=False))
