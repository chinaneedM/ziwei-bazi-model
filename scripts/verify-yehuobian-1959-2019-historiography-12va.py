#!/usr/bin/env python3
"""12VA: secondary debates about Ming-printed editions are not source-page glyph evidence."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12VA-1959-2019-MING-PRINT-HISTORIOGRAPHY-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12VA-PANG1959-SCHOLARLY-SOURCE-SHARD-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
GRAPH="docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"
OLD="docs/research/MING-DATONG-YEHUOBIAN-12TE-MING-PRINT-SCHOLARLY-SOURCE-SHARD-R1.json"
PANG="EXT-SCU-PANGSHIZHOU1959-WANLI-YEHUOBIAN-MING-PRINT-UNRESOLVED-12VA"
DU="EXT-PKU-CHINESE-CLASSICS-CULTURE-DU2019-YEHUOBIAN-MING-PRINT-QUESTION"
GUARDS=(
"1959_unresolved_discussion_is_not_ming_print_existence_proof",
"2019_negative_hypothesis_is_scholarly_not_physical_nonexistence_proof",
"journals_1959_and_2019_are_two_scholarship_positions_not_two_ancient_glyph_votes",
"ncl02260_old_manuscript_not_a_printed_ming_edition",
"qing_npm_jinxiang_is_not_proven_pre1827_or_1869_same_plates",
"work_1619_arrangement_not_later_themed_30volume_juan20",
"1827_publisher_preface_is_not_proven_unrepaired_target_impression",
"1869_publisher_collation_does_not_prove_four_locus_change",
"exact_1827_and_1869_original_target_leaves_not_obtained",
"scholarship_does_not_authorize_clock_rule_or_algorithm_reopen",
"full_1959_article_not_downloaded_or_page_verified",
"full_2019_article_not_downloaded_or_page_verified")
def validate(r,shard,manifest,state,graph,old):
 if r.get("schema")!="TIANWEN-12VA-YEHUOBIAN-MING-PRINT-1959-2019-HISTORIOGRAPHY-CONTROL-R1":
  raise ValueError("schema")
 scholars=r.get("scholarly_witnesses",[])
 if len(scholars)!=3 or scholars[0].get("source_id")!=PANG or scholars[1].get("source_id")!=DU:
  raise ValueError("1959/2019 witness binding")
 if scholars[0].get("url")!="https://journal.scu.edu.cn/info/1109/11943.htm" or scholars[0].get("issue")!="1959(04)" or scholars[0].get("pages")!="161–170 (provider renders -161-170)":
  raise ValueError("publication locator")
 if scholars[1].get("issue")!="2019(02)" or scholars[1].get("pages")!="25–29":
  raise ValueError("2019 comparison locator")
 if any(x.get("full_article_inspected") is not False for x in scholars[:2]):
  raise ValueError("full article falsely obtained")
 if DU not in {x.get("source_id") for x in old["sources"]}:
  raise ValueError("prior source missing")
 if any(r.get("claim_boundaries",{}).get(k) is not True for k in GUARDS):
  raise ValueError("historical source uncertainty promoted")
 hs=r.get("historical_state",{})
 if hs.get("early_ming_print_status")!="UNRESOLVED_NO_PHYSICAL_MING_PRINT_PROVEN_FROM_REVIEWED_1959_OR_2019_METADATA" or hs.get("earliest_surviving_confirmed_print_date")!="NOT_ADJUDICATED":
  raise ValueError("Ming-print claim unearned")
 if any(hs.get(k) is not False for k in ("physical_ming_print_obtained","original_1827_target_image","original_1869_target_image","algorithm_reopen_authorized")):
  raise ValueError("historical target or reopen falsely obtained")
 if hs.get("source_glyph_votes_new")!=0 or hs.get("transmission_edges_added")!=0:
  raise ValueError("scholarship voted as physical evidence")
 entries=shard.get("sources",[])
 if len(entries)!=1 or entries[0].get("source_id")!=PANG or entries[0].get("physical_glyph_authority") is not False or entries[0].get("verification_status")!="BIBLIOGRAPHIC_METADATA_ONLY" or entries[0].get("evidence")!=REC:
  raise ValueError("source shard")
 if not any(x.get("path")==SHARD and x.get("source_count")==1 and x.get("schema")==shard["schema"] for x in manifest["shards"]):
  raise ValueError("manifest linkage")
 if (manifest.get("root_source_count")!=647 or manifest.get("extension_source_count",0)<43 or
     manifest.get("combined_source_count")!=manifest.get("root_source_count")+manifest.get("extension_source_count")):
  raise ValueError("manifest current count")
 delta=r.get("source_delta",{})
 if (delta.get("extension_before"),delta.get("extension_after"),delta.get("unique_source_count_increment"))!=(42,43,1):
  raise ValueError("historical delta")
 a=state["historical_audit"]
 if (a.get("row_count"),a.get("audited_row_count"),a.get("external_source_registry_total_unique_count"))!=(222,222,manifest["combined_source_count"]):

  raise ValueError("state inconsistency")
 if tuple(map(int,state["schema_version"].split(".")))<(1,557,0) or not any(x.startswith("12VA ") for x in a["current_focus"]):
  raise ValueError("state advance")
 if len(graph["nodes"])<252 or len(graph["edges"])<238:
  raise ValueError("graph unexpectedly changed")
 return {"status":"PASS","new_scholarly_sources":1,"new_primary_early_prints":0,"target_glyph_votes":0,"schema":state["schema_version"]}
def verify(root=ROOT):
 def load(p):return json.loads((root/p).read_text(encoding="utf-8"))
 return validate(*(load(p) for p in (REC,SHARD,MAN,STATE,GRAPH,OLD)))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
