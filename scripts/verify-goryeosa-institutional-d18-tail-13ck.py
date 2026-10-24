#!/usr/bin/env python3
"""13CK: typed electronic transcription discordance vs an existing historical original ROI."""
import hashlib,json
from pathlib import Path
from decimal import Decimal
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CK-GORYEOSA-KRDB-D18-TAIL-TRANSCRIPTION-DISCORDANCE-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json";L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
R="docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
OLD="docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json"
KR="八千四百二十四六四〇八三";WK="八千四百二十四六四〇八"
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def shaobj(path):
 raw=(ROOT/path).read_bytes()
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def check(e,s,l,reg,old):
 assert e["schema"]=="TIANWEN-13CK-GORYEOSA-INSTITUTIONAL-D18-RECEIVED-TAIL-GLYPH-R1"
 assert e["issue_id"]=="TW-OPEN-0005"
 assert "LIVE_PUBLIC_HTML_TRANSCRIPTION" in e["evidence_grade"]
 assert [x["source_id"] for x in e["existing_registry_sources"]]==[
  "EXT-KRDB-GORYEOSA-V52-SHOUSHI-LICHENG","EXT-WIKISOURCE-GORYEOSA-V52-SHOUSHI-SOLAR-LICHENG"]
 for row in e["existing_registry_sources"]:
  entry=next(x for x in reg["sources"] if x["source_id"]==row["source_id"])
  assert row["url"]==entry["url"] or row["source_id"].startswith("EXT-KRDB-") and entry["url"]=="https://db.history.go.kr/goryeo/itemLevelKrList.do?parentId=kr_052_0010_0010_0020&types=o"
  assert row["source_role"].endswith("NOT_ORIGINAL_IMPRESSION") or "NOT_INDEPENDENT_PHYSICAL_COPY" in row["source_role"]
 z=e["live_html_snapshot_boundaries"]
 assert z["sha256_of_live_html_download"]==z["provider_binary_snapshot"]=="NOT_CAPTURED"
 assert z["review_date"]=="2026-10-22"
 assert z["institutional_display_header_order"]==["積日","日差加一秒八十六少","盈縮加分","盈縮積","行度"]
 assert z["community_display_header_order"]==["積日","日差加一秒八十六少","盈縮積","盈縮加分","行度"]
 assert z["column_order_is_presentation_difference_not_numeric_field_variant"] is True
 a=e["directly_observed_received_rows"]
 assert [x["printed_day"] for x in a]==[16,17,18,19]
 original=[("五分一三六二","四百二十九六〇七三","七千五百七十〇六六二四"),
           ("五分二五四八","四百二十四三七一一","八千〇〇〇二六九七"),
           ("五分二七三四","四百一十九一一六三",WK),
           ("五分二九二〇","四百一十三八四二九","八千八百四十三七五七一")]
 for row,(richa,long,c) in zip(a,original):
  assert row["institutional"]["richa"]==row["community"]["richa"]==richa
  assert row["institutional"]["yingsuojiafen"]==row["community"]["yingsuojiafen"]==long
  assert row["community"]["yingsuoji"]==c
  assert row["institutional"]["yingsuoji"]==(KR if row["printed_day"]==18 else c)
  assert "NOT_TWO_ORIGINAL" in row["scope"] or "OBSERVED_FINAL_CHARACTER" in row["scope"]
 assert a[2]["institutional"]["yingsuoji"]==a[2]["community"]["yingsuoji"]+"三"
 prev=e["previously_sha_bound_original"]
 assert prev["path"]==OLD and shaobj(OLD)==prev["git_blob_sha"]
 assert prev["image_sha256"]==old["source"]["jpeg_sha256"]
 roi=next(x for x in old["original_numeric_rois"] if x["key"]==prev["roi_key"])
 assert roi["key"]=="P23_D18_C" and roi["day"]==prev["printed_day"]==18
 assert roi["literal"]==prev["original_glyph_literal"]==WK
 assert roi["value"]==prev["previous_original_decimal"]=="8424.6408"
 assert roi["pixel_sha256"]==prev["numeric_roi_sha256"]
 assert roi["bbox"]==prev["roi_bbox"]
 assert prev["current_turn_original_pixels_reopened"] is False
 c=e["scoped_comparison"]
 assert c["institutional_d18_extra_suffix"]=="三"
 assert c["institutional_d18_received_literal"]==KR and c["community_d18_received_literal"]==WK
 assert c["physical_waseda_d18_original_literal"]==WK
 assert c["institutional_equals_community"] is False
 assert c["institutional_equals_original_record"] is False
 assert c["community_equals_original_record"] is True
 assert c["matched_neighboring_received_rows"]==[16,17,19]
 assert Decimal(c["exact_decimal_4place_original"])==Decimal("8424.6408")
 assert Decimal(c["original_local_c18_minus_c17"])==Decimal(c["long_d17"])==Decimal("424.3711")
 assert c["strongest_supported_claim"]=="CURRENT_INSTITUTIONAL_ELECTRONIC_TRANSCRIPTION_HAS_TRAILING_EXTRA_THREE_AGAINST_ANOTHER_ELECTRONIC_TEXT_AND_PREVIOUS_ORIGINAL_IMAGE_ROI"
 for k in ("not_evidence_of_archaeological_variant","cannot_silently_rewrite_institutional_text","cannot_promote_received_text_to_new_physical_witness"):
  assert c[k] is True
 assert c["transcription_cause"]==c["library_edit_history_or_base_impression"]=="UNRESOLVED" or c["transcription_cause"]=="UNRESOLVED" and c["library_edit_history_or_base_impression"]=="NOT_BOUND"
 scope=e["new_evidence_scope"]
 for k in ("source_registry_entries","new_archived_html_sha_objects","new_original_pixel_rois","new_original_jpegs","new_physical_historical_witnesses","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","independent_stemmatic_votes","algorithm_reopens"):
  assert scope[k]==0
 assert scope["open_or_blocked_issues"]==11 and scope["deterministic_product"]=="CLOSED"
 assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and s["invariants"]["algorithm_reopen_count"]==0
 a=s["historical_audit"]
 assert a["row_count"]==a["audited_row_count"]==222 and a["external_source_registry_total_unique_count"]==a["external_source_registry_root_count"]+a["external_source_registry_extension_count"]
 assert any(x.startswith("13CK ") for x in a["current_focus"])
 assert l["binding"]["reviewed_state_version"]==s["schema_version"] and l["binding"]["source_focus_count"]==len(a["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and E in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-KRDB-RECEIVED-D18-13CK" for x in issue["history"])
 assert any(x["id"]=="OMISSIONS-13CK-KRDB-D18-TRANSCRIPTION-20261022" for x in l["checkpoint_log"])
 assert len([x for x in l["issues"] if x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS")])==11
 return True
if __name__=="__main__":
 assert check(load(E),load(S),load(L),load(R),load(OLD))
 print("TIANWEN_13CK_RECEIVED_D18_TRANSCRIPTION_DISCORDANCE=PASS")
