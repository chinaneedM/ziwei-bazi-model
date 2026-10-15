#!/usr/bin/env python3
"""12WK: four dated textual signatures on ONE source image, not print-date votes."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WK-FOUR-ERA-PARATEXT-ORIGINAL-IMAGE-COLLATION-R1.json"
WJ="docs/research/MING-DATONG-YEHUOBIAN-12WJ-CADAL02096900-DIRECT-1869-REVISION-PARATEXT-AND-1700-PREFACE-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12WJ-CADAL02096900-PARATEXT-DIRECT-IMAGE-SOURCE-SHARD-R1.json"
VZ="docs/research/MING-DATONG-YEHUOBIAN-12VZ-CADAL02112262-DIRECT-PRINTED-GLYPH-AND-DIGITAL-IDENTITY-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
REGISTRY="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
ORIGINAL="711dc16b17d139612fbe852dc99869bb709b85c161440dfc7618ee1dbd6f38fa"
PAGES={5:"c0af056aac05c2fe5a57bfc0c86aef8215dbd8bca01c3f07cd925369bc1d4576",7:"3f82e51414c5b25bf59612e1cee139cf4146cc1ee128eee705e76e5707b4b957",10:"dbc1b4f2dc1af981840dff2fa05eb3513bd22ab5146bcede8944bd1d55df1ebf"}
EXPECTED={
 "W1606":(1606,"丙午",7,"萬曆三十四年丙午仲冬日沈德符題"),
 "W1700":(1700,"庚辰",10,"康熙庚辰八月桐鄉錢枋識"),
 "W1827":(1827,"丁亥",5,"道光七年歲次丁亥春三月"),
 "W1869":(1869,"己巳",5,"同治八年己巳春月重校刊補")
}
STEMS="甲乙丙丁戊己庚辛壬癸"
BRANCHES="子丑寅卯辰巳午未申酉戌亥"
def fail(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def validate(r,w,sh,vz,st,manifest):
 fail(r["schema"]=="TIANWEN-12WK-CADAL02096900-FOUR-ERA-PARATEXT-ORIGINAL-IMAGE-COLLATION-R1","schema")
 s=r["source"]
 fail(s["source_id"]==w["witness"]["source_id"]==sh["sources"][0]["source_id"] and s["preexisting_registry_entry"] is True,"same preexisting registered source")
 fail(s["original_djvu_sha256"]==ORIGINAL==w["witness"]["source_sha256"]==sh["sources"][0]["direct_image_attestation"]["source_sha256"],"same original SHA")
 fail((s["original_djvu_bytes"],s["pages"])==(2833699,115),"original metrics")
 fail(s["artifact_id"]==w["source_capture"]["artifact_id"]==11968140368 and s["github_run_id"]==38724642123,"artifact identity")
 fail(s["verified_artifact_zip_sha256"]==w["source_capture"]["artifact_zip_sha256_locally_recomputed"] and s["direct_original_source_locally_rehashed"] is True and s["no_ocr"] is True,"actual independently rechecked source no OCR")
 fail(s["selected_jpeg_pages_locally_rehashed"]==[5,7,10],"direct three selected pages")
 rows=r["dated_layers"]
 fail(len(rows)==4 and {x["id"] for x in rows}==set(EXPECTED),"four independent date signatures")
 for row in rows:
  y,cy,p,g=EXPECTED[row["id"]]
  fail((row["year"],row["year_cycle"],row["page"],row["glyph"])==(y,cy,p,g),"date glyph/page label "+row["id"])
  fail(row["page_sha256"]==PAGES[p],"source jpeg SHA "+row["id"])
  fail(STEMS[(y-4)%10]+BRANCHES[(y-4)%12]==cy,"sexagenary year coherence "+row["id"])
  fail(any(marker in row["scope"].lower() for marker in ("not proof","not established","neither original","not a copy-date proof")),"textual witness scope "+row["id"])
 fail(w["witness"]["manually_collated_pages"][0]["sha256"]==PAGES[5] and w["witness"]["manually_collated_pages"][1]["sha256"]==PAGES[10],"old manual reading control")
 fail(sh["sources"][0]["direct_image_attestation"]["page_sha256"]=={"5":PAGES[5],"10":PAGES[10]},"preserve previous registered source readings")
 cross=r["cross_fascicle"]
 fail(cross["other_fascicle"]=="CADAL02096915" and cross["alternative_fascicle"]=="CADAL02112262","other digital source identities")
 srcfiles=vz["exact_source_capture"]["source_files"]
 fail(cross["other_fascicle_original_sha256"]==next(x["sha256"] for x in srcfiles if x["id"]=="CADAL02096915"),"other source digest")
 fail(cross["alternative_fascicle_original_sha256"]==next(x["sha256"] for x in srcfiles if x["id"]=="CADAL02112262"),"alternative source digest")
 fail(cross["independently_authenticated_same_physical_paper_copy"] is False and cross["documented_physical_shelfmark_for_this_source"] is None and cross["edition_impression_year_bound"] is None,"physical print cross-fascicle firewall")
 fail(all(cross[k] is False for k in ("printed_target_folio_read_from_this_first_fascicle","original_1827_unrepaired_juan20_leaf_obtained","original_1869_corrected_juan20_leaf_obtained")),"no original target folio")
 f=r["inference_firewalls"]
 fail(all(v is True for v in f.values()),"chronology inference firewalls")
 c=r["counters"]
 fail(c["new_registered_external_sources"]==c["historical_print_independence_votes"]==c["juan20_new_target_glyph_readings"]==c["algorithm_reopens"]==0,"zero manufactured evidence/algorithm")
 fail(c["source_registry_union"]==705 and manifest["combined_source_count"]==st["historical_audit"]["external_source_registry_total_unique_count"]>=c["source_registry_union"],"no source double count")
 fail(c["historical_matrix_rows"]==st["historical_audit"]["row_count"]==222 and c["historical_matrix_audited"]==st["historical_audit"]["audited_row_count"]==222,"matrix intact")
 fail(c["provenance_repairs"]==st["historical_audit"]["repaired_provenance_metadata_defect_count"]==45 and c["formal_batches"]==len(st["historical_audit"]["completed_batches"])==487,"batch/defect invariants")
 fail(c["genealogy_nodes"]==252 and c["genealogy_edges"]==238 and st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED","genealogy/product invariant")
 fail(r["transmission_impact"]["edges_supported"]==[] and r["transmission_impact"]["nodes_added_or_strengthened"]==[],"no unsupported lineage")
 fail(r["provenance"]["new_readings"]==["W1606","W1827"] and r["provenance"]["old_direct_readings_reconfirmed"]==["W1700","W1869"],"forward-only new reading split")
 return {"status":"PASS","date_layers":[1606,1700,1827,1869],"newly_read_image_loci":2,"independent_1827_1869_print_votes":0}
def verify():return validate(*(load(x) for x in [REC,WJ,SHARD,VZ,STATE,REGISTRY]))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
