#!/usr/bin/env python3
"""12WJ: exact Commons original-image paratext 1869/1700; physical print unbound."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REC="docs/research/MING-DATONG-YEHUOBIAN-12WJ-CADAL02096900-DIRECT-1869-REVISION-PARATEXT-AND-1700-PREFACE-R1.json"
SHARD="docs/research/MING-DATONG-YEHUOBIAN-12WJ-CADAL02096900-PARATEXT-DIRECT-IMAGE-SOURCE-SHARD-R1.json"
MAN="docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json"
STATE="docs/PROJECT-CURRENT-STATE-R1.json"
ID="EXT-CADAL02096900-YEHUOBIAN-FASC1-1869-REVISION-PARATEXT-1700-PREFACE-12WJ"
SHA="711dc16b17d139612fbe852dc99869bb709b85c161440dfc7618ee1dbd6f38fa"
PAGES={"5":"c0af056aac05c2fe5a57bfc0c86aef8215dbd8bca01c3f07cd925369bc1d4576","10":"dbc1b4f2dc1af981840dff2fa05eb3513bd22ab5146bcede8944bd1d55df1ebf"}
def fail(ok,msg):
 if not ok:raise ValueError(msg)
def digest(blob):
 return hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()
def validate(r,sh,m,st):
 fail(r["schema"]=="TIANWEN-12WJ-CADAL02096900-DIRECT-PARATEXT-SOURCE-IMAGE-GLYPHS-R1","schema")
 w=r["witness"]
 fail(w["source_id"]==ID and w["source_sha256"]==SHA,"original source ID and sha")
 fail((w["source_bytes"],w["source_pages"])==(2833699,115),"original actual binary metrics")
 fail(w["edition_impression_date_bound"] is False and w["physical_copy_catalog_identity_bound"] is False and w["exact_original_paper_copy_unbound"] is True,"paper imprint provenance firewall")
 fail(w["target_theoretical_volume20_article_source"] is False and w["historical_independent_print_vote_count"]==0 and w["ocr_used"] is False,"no target or OCR votes")
 loci={str(p["page"]):p["sha256"] for p in w["manually_collated_pages"]}
 fail(loci==PAGES,"photo page identity")
 ph={str(p["page"]):p["visible"] for p in w["manually_collated_pages"]}
 fail("同治八年己巳春月重校刊補" in ph["5"] and "季男德恒謹識" in ph["5"],"1869 printed revision preface")
 fail("康熙庚辰八月桐鄉錢枋識" in ph["10"],"1700 inherited preface")
 c=r["source_capture"]
 fail((c["original_github_run_id"],c["verify_job_id"],c["capture_job_id"],c["artifact_id"])==(38724642123,116387354256,116387522573,11968140368),"exact-head Actions receipt")
 fail(c["capture_head_sha"]=="4cf4d39d6d6515b51bb74eb3b983cb467b59ba98","capture head")
 fail(c["artifact_zip_sha256_locally_recomputed"]==c["artifact_zip_sha256_github_reported"]=="5b3947d258f4722007a8f9901033dbdb896f0c23501776eaf48f2f9d29c78d2d","independently verified artifact")
 fail(c["original_djvu_bytes_locally_rechecked"] is True and c["all_48_page_jpeg_sha256_locally_rechecked"] is True and c["num_selected_pages"]==48,"all source/derived image page digests")
 fail(c["human_original_image_review_no_OCR"] is True and c["imprint_page5_reviewed_in_source_derived_jpeg"] is True and c["preface_page10_reviewed_in_source_derived_jpeg"] is True,"actual human page review")
 t=r["textual_scope"]
 fail(t["firstparty_print_page5_line1"]=="同治八年己巳春月重校刊補" and t["firstparty_print_page10_line1"]=="康熙庚辰八月桐鄉錢枋識","image original reading")
 fail(t["actual_source_printed_paper_impression_year"] is None and t["actual_source_paper_shelfmark"] is None and t["paper_source_copy_to_CADAL02096915_identity"] is None,"not a source-bound physical copy or edition")
 fail(t["actual_j20_gaizao_louke_target_images_in_this_fascicle"] is False and t["no_direct_plate_revision_detected"] is True,"not a 1827/1869 volume20 correction proof")
 sc=r["source_scope"]
 fail(sc["new_original_direct_paratext_image_source_count"]==1 and sc["new_image_scoped_paratext_readings_count"]==2,"one new digital surface/two paratext loci")
 fail(sc["new_independent_historical_print_votes"]==0 and sc["new_target_article_locus_readings"]==0,"no historical 1827/1869 target source vote")
 fail(sc["same_underlying_copy_as_12VZ_unproven"] is True and sc["physical_copy_catalog_bound"] is False,"no CADAL physical linkage")
 fail(sc["algorithm_reopens"]==0 and sc["new_genealogy_edges"]==0,"no algorithm or lineage")
 sources=sh["sources"]
 fail(len(sources)==1 and sources[0]["source_id"]==ID and sources[0]["physical_glyph_authority"] is True,"new source ID")
 src=sources[0]
 fail(src["verification_status"]=="DIRECT_SOURCE_IMAGE_GLYPH_COLLATED_EDITION_UNBOUND","direct image source scope")
 im=src["direct_image_attestation"]
 fail(im["source_sha256"]==w["source_sha256"]==SHA and im["source_url"]==w["source_url"] and im["page_sha256"]==PAGES,"cross-source and page attestation")
 fail(im["source_file_pages"]==115 and im["independent_physical_print_vote"] is False,"no imprint vote")
 fail(m["root_source_count"]==647 and m["extension_source_count"]>=58 and m["combined_source_count"]==m["root_source_count"]+m["extension_source_count"],"registry growth")
 found=[x for x in m["shards"] if x["path"]==SHARD and x["source_count"]==1 and x["schema"]==sh["schema"]]
 fail(len(found)==1,"exact source shard registration")
 fail(st["historical_audit"]["external_source_registry_total_unique_count"]==m["combined_source_count"],"state sync")
 fail(st["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and r["transmission_impact"]["edges_supported"]==[],"product and genealogy")
 return {"status":"PASS","new_direct_printed_paratext_source":1,"source_verified_pages":[5,10],"image_scoped_1869_1700_paratext_loci":2,"independent_1827_1869_original_print_votes":0}
def verify():
 def load(path):return json.loads((ROOT/path).read_text(encoding="utf-8"))
 r,sh,m,st=(load(p) for p in (REC,SHARD,MAN,STATE))
 spec=next(x for x in m["shards"] if x["path"]==SHARD)
 fail(spec["blob_sha"]==digest((ROOT/SHARD).read_bytes()),"source shard Git blob SHA")
 return validate(r,sh,m,st)
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False))
