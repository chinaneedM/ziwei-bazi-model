#!/usr/bin/env python3
"""Evidence-scoped, forward-only research omission ledger verifier."""
import argparse
import json
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LEDGER=Path("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
STATE=Path("docs/PROJECT-CURRENT-STATE-R1.json")
PROTOCOL=Path("docs/PROJECT-CONTINUITY-PROTOCOL-R1.md")
MATRIX=Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
MANIFEST=Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json")
ALLOWED={"OPEN","BLOCKED_SOURCE_ACCESS","RESOLVED_WITH_EVIDENCE"}
REQUIRED_AXES={
 "primary_editions_and_physical_copies","region_and_location","school_specific_methods",
 "philology_and_word_sense","historical_time_and_calendar_coordinate",
 "mathematical_replay","contrary_and_negative_evidence","transmission_lineage_and_non_edges"
}
BASELINE_IDS={f"TW-OPEN-{i:04d}" for i in range(1,10)}
def require(p,msg):
 if not p:raise ValueError(msg)
def read(path):
 return json.loads((ROOT/path).read_text(encoding="utf-8"))
def record_statuses(data):
 return {x["id"]:x for x in data["issues"]}
def validate(data,state,protocol,exists_fn=None):
 require(data["schema"]=="TIANWEN-RESEARCH-OMISSION-RISK-LEDGER-R1","schema")
 for issue in data["issues"]:
  if "source_page_coverage" not in issue:
   continue
  ev=issue["source_page_coverage"]
  p=Path(ev["source_doc"])
  require(p.as_posix().startswith("docs/research/") and ".." not in p.parts,"evidence replay path must be stable")
  original=(ROOT/p).read_bytes()
  import hashlib
  blob_hash=hashlib.sha1(b"blob "+str(len(original)).encode("ascii")+b"\0"+original).hexdigest()
  require(blob_hash==ev["source_blob_sha"],"research image-grade source blob mismatch")
  src=json.loads(original)
  g=src["grade_union"];r=src["review"]
  require(ev["total_source_pdf_pages"]==g["whole_holding_source_pdf_pages"],"page-count replay mismatch")
  require(ev["body_source_pages"]==g["whole_body_pages"],"body page replay mismatch")
  require(ev["bounded_native_body_jpeg_pages"]==g["global_native_body_source_pages_after"],"native grade replay mismatch")
  require(ev["linewise_fulltext_pending_body_pages"]==g["whole_body_fulltext_collation_pending"],"full-text pending replay mismatch")
  require(ev["fulltext_linewise_collated_body_pages"]==g["whole_body_pages"]-g["whole_body_fulltext_collation_pending"],"fulltext completed replay mismatch")
  require(ev["non_target_preliminary_pages"]==g["non_target_first_fascicle_preliminary_pages"],"preliminary non-body page replay mismatch")
  require(ev["nonbody_colophon_pages"]==g["f10_colophon_native_nonbody_pages"],"colophon non-body page replay mismatch")
  require(ev["any_page_target_absence_proven"]==r["any_page_target_absence_proven"]==False,"unproven page-level text absence")
  require(ev["all_body_passage_absence_proven"]==r["whole_old20_work_target_absence_proven"]==False,"unproven whole-work absence")
  require(ev["original_old20_target_folio_attested"]==r["any_original_old20_gaizao_louke_target_folio_positive_attestation"]==False,"unproven original target folio")
  require(ev["source_pdf_rehashed_in_this_batch"]==src["source"]["source_pdf_rehashed_this_batch"]==False,"false source PDF binary rehash")
  require(ev["copy_identity_unified_not_multiple_independent_physical_witnesses"]==True and ev["physical_holding"]==src["source"]["physical_holding"],"source copy multiplication")
  require(ev["distinct_1827_thematic_juan20_binding_proven"]==False and r["old20_juan_equivalent_to_1827_reorganized_thematic_juan"]==False,"false old/new juan equivalence")
  seam=Path(ev["direct_juan_seam_doc"])
  seam_bytes=(ROOT/seam).read_bytes()
  require(hashlib.sha1(b"blob "+str(len(seam_bytes)).encode("ascii")+b"\0"+seam_bytes).hexdigest()==ev["direct_juan_seam_blob_sha"],"chronological seam source drift")
  sm=json.loads(seam_bytes)
  require({(x["from_juan"],x["to_juan"],x["shared_pdf_page"]) for x in sm["seams"]}>={(18,19,81),(19,20,137)},"old20 mixed-leaf seam evidence missing")
  revisions=issue.get("source_page_coverage_revisions",[])
  require(isinstance(revisions,list),"source-page revisions must be a list")
  require(len({x.get("revision_id") for x in revisions})==len(revisions),"duplicate page-review revision id")
  for rev in revisions:
   require(rev.get("review_kind") in ("DIRECT_ORIGINAL_TARGET_FOLIO","FULL_SOURCE_HIGH_RES_LINEWISE_NEGATIVE"),"source-page revision kind unsupported")
   for key in ("revision_id","source_doc","source_blob_sha","physical_holding","original_folio_ref","original_image_sha256","reviewed_by","review_date","review_kind"):
    require(isinstance(rev.get(key),str) and bool(rev[key]),"source-page revision field missing: "+key)
   import re
   require(bool(re.fullmatch(r"[0-9a-f]{40}",rev["source_blob_sha"])),"revision Git blob SHA format")
   require(bool(re.fullmatch(r"[0-9a-f]{64}",rev["original_image_sha256"])),"revision image SHA256 format")
   new_path=Path(rev["source_doc"])
   require(new_path.parts[:2]==("docs","research") and ".." not in new_path.parts,"revision evidence doc path")
   newbytes=(ROOT/new_path).read_bytes()
   require(hashlib.sha1(b"blob "+str(len(newbytes)).encode("ascii")+b"\0"+newbytes).hexdigest()==rev["source_blob_sha"],"revision source blob integrity")
   doc=json.loads(newbytes)
   match=doc.get("source_page_review_revision",{})
   for key in ("revision_id","physical_holding","original_folio_ref","original_image_sha256","reviewed_by","review_date","review_kind"):
    require(match.get(key)==rev[key],"revision original page source binding mismatch: "+key)
   require(match.get("original_image_source_url") and match.get("human_direct_glyph_or_linewise_review") is True,"revision original image and human review required")
   if rev["review_kind"]=="FULL_SOURCE_HIGH_RES_LINEWISE_NEGATIVE":
    require(match.get("whole_body_pages_linewise_reviewed")==ev["body_source_pages"],"full manuscript negative lacks source-scoped complete linewise pages")
    require(match.get("complete_original_page_image_manifest_sha256") and not match.get("source_coverage_gaps"),"negative source completeness unproved")
   else:
    require(match.get("target_passage")=="改造漏刻" and match.get("target_passage_original_glyph_directly_visible") is True,"positive target original glyph not proven")
  if issue["status"]=="RESOLVED_WITH_EVIDENCE":
   require(bool(revisions),"old bounded page snapshot cannot by itself resolve target")
   require(bool(issue.get("resolution_evidence")),"resolution evidence must be explicit")


 for issue in data["issues"]:
  if "g893_six_control_snapshot" not in issue:
   continue
  ev=issue["g893_six_control_snapshot"]
  import hashlib
  p=Path(ev["source_doc"]);oldp=Path(ev["baseline_control_source_doc"])
  require(p.parts[:2]==("docs","research") and ".." not in p.parts and oldp.parts[:2]==("docs","research") and ".." not in oldp.parts,"G893 evidence paths escaped repository")
  raw=(ROOT/p).read_bytes();old_raw=(ROOT/oldp).read_bytes()
  h=lambda b:hashlib.sha1(b"blob "+str(len(b)).encode("ascii")+b"\0"+b).hexdigest()
  require(h(raw)==ev["source_doc_git_blob_sha"] and h(old_raw)==ev["baseline_control_source_git_blob_sha"],"G893 existing source blob drift")
  src=json.loads(raw);base=json.loads(old_raw)
  require(ev["catalog_source_id"]==src["source_identity"]["source_id"]==base["source_id"],"G893 source identifier diverged")
  require(ev["catalog_identifier"]==src["source_identity"]["identifier"],"G893 copied catalog identity changed")
  require(ev["provider_book_cd"]=="GK00893_00" and base["g893_object"]["book_cd"]==ev["provider_book_cd"],"G893 object code not source-bound")
  acq=src["acquisition"]
  require(acq["complete_sequence"] is True and ev["acquired_physical_pages"]==acq["physical_pages_acquired"]==acq["physical_pages_expected"]==ev["expected_physical_pages"]==204,"G893 whole source capture misrepresented")
  archive=ev["acquisition_archive"]
  require(archive["workflow_run_id"]==acq["workflow_run_id"] and archive["artifact_id"]==acq["artifact_id"] and archive["name"]==acq["artifact_name"],"G893 archived image artifact mismatch")
  require(src["adjudication"]["legacy_six_g893_controls"]=="NOT_ADJUDICATED_IN_THIS_BATCH" and base["target_status"]=="ALL_SIX_PENDING_DIRECT_TARGET_PAGE","G893 six controls mistakenly closed from other source")
  ids=base["target_controls"]
  controls=ev["six_original_target_controls"]
  require(len(controls)==len(ids)==6 and [c["id"] for c in controls]==ids,"G893 one of six control IDs was lost or reordered")
  require(all(c["status"]=="PENDING_DIRECT_TARGET_PAGE_COLLATION" and c["original_page_id"] is None and c["original_page_sha256"] is None and c["direct_glyph_and_numeric_replay"] is None for c in controls),"G893 six targets falsely adjudicated from 12CW")
  require(ev["independent_original_target_numeric_decisions"]==0 and ev["whole_book_capture_completed"] is True and ev["historical_source_snapshot_not_six_target_collation"] is True and ev["old_acquisition_blocker_resolved"] is True,"G893 whole book access vs six target separation lost")
  observed=src["direct_physical_collation"]
  anchors=ev["independently_reviewed_non_six_loci"]
  require(len(anchors)==2 and [(x["page_id"],x["original_jpeg_sha256"]) for x in anchors]==[("052a",observed["winter_opening_052a"]["sha256"]),("077a",observed["summer_transition_077a"]["sha256"])],"G893 non-six source page identities falsely transferred")
  require(ev["exact_impression_year"]=="UNRESOLVED" and ev["provider_year_scope"]==src["source_identity"]["provider_date_scope"],"G893 inferred exact printed year")
  require(issue["status"]!="BLOCKED_SOURCE_ACCESS","G893 complete source mistakenly access-blocked")
  require(issue["status"]!="RESOLVED_WITH_EVIDENCE","G893 6 original number controls still uncollated")
 for issue in data["issues"]:
  locators=issue.get("g893_target_page_locators",[])
  require(isinstance(locators,list),"G893 locators must be list")
  ids=[x["control_id"] for x in locators]
  require(len(ids)==len(set(ids)),"G893 locator control duplicated")
  if not locators:continue
  import hashlib,re
  known={c["id"] for c in issue["g893_six_control_snapshot"]["six_original_target_controls"]}
  require(set(ids).issubset(known),"G893 unknown target locator ID")
  for row in locators:
   p=Path(row["evidence_doc"])
   require(p.parts[:2]==("docs","research") and ".." not in p.parts,"G893 page evidence outside research")
   doc=json.loads((ROOT/p).read_text(encoding="utf-8"))
   target=doc["target"]
   require(target["control_id"]==row["control_id"] and target["verified_page_id"]==row["page_id"] and target["source_original_page_sha256"]==row["page_sha256"],"G893 locator target source mismatch")
   require(len([x for x in doc["source_original_direct_review"] if x["page_id"]==row["page_id"] and x["source_page_sha256"]==row["page_sha256"]])==1,"G893 original page provenance missing")
   require(bool(re.fullmatch(r"[0-9a-f]{64}",row["page_sha256"])),"G893 page SHA malformed")
   require(row["status"]=="LOCATED_NUMERIC_UNADJUDICATED" and row["numeric_value"] is None and target["original_difference_reading"] is None and target["numeric_collation_status"]=="PENDING_VALUE_AND_FIELD_SEMANTICS","G893 source page location laundered into numeric decision")
   require(doc["known_archive"]["reported_jpeg_digest_matches_from_independent_download"]==doc["known_archive"]["source_original_jpeg_count"]==204 and doc["known_archive"]["digest_mismatches"]==0,"G893 recovered original JPEG manifest validation status missing")
 for issue in data["issues"]:
  readings=issue.get("g893_direct_glyph_observations",[])
  require(isinstance(readings,list),"G893 glyph observations must be list")
  if not readings:continue
  locs={x["control_id"]:x for x in issue.get("g893_target_page_locators",[])}
  require(len({x["control_id"] for x in readings})==len(readings),"G893 glyph observation control duplicated")
  for o in readings:
   loc=locs.get(o["control_id"])
   require(loc is not None and o["page_id"]==loc["page_id"] and o["page_sha256"]==loc["page_sha256"],"G893 observed glyph source-page locator mismatch")
   p=Path(o["evidence_doc"])
   require(p.parts[:2]==("docs","research") and ".." not in p.parts,"G893 observed glyph evidence path")
   doc=json.loads((ROOT/p).read_text(encoding="utf-8"))
   match=[x for x in doc["observations"] if x["control_id"]==o["control_id"]]
   require(doc["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and doc["provider_book_cd"]=="GK00893_00" and len(match)==1,"G893 glyph evidence copy mismatch")
   s=match[0]
   require(s["page_id"]==o["page_id"] and s["source_original_page_sha256"]==o["page_sha256"] and s["surface"]==o["observed_surface"],"G893 direct glyph evidence mismatch")
   require(o["observed_surface"] and s["scope"]==o["scope"] and s["confidence"]==o["confidence"] and o["grade"]=="SOURCE_ORIGINAL_VISIBLE_GLYPH_SEGMENT_ONLY","G893 glyph observation authority inflation")
   require(s["human_visual_source_jpeg_review"] is True and s["ocr_used"] is False and s["source_issued_original_image_url"].startswith("https://kyudb.snu.ac.kr/ImageServlet.do?"),"G893 glyph image direct origin absent")
   require(o["normalized_numeric_value"] is None and o["numeric_decision_awarded"]==0 and s["normalized_numeric_value"] is None and s["new_independent_witness_votes"]==0,"G893 direct glyph promoted without semantics")
   require(s["numeric_adjudication_status"]=="FIELD_SEMANTICS_PRECISION_AND_CROSS_WITNESS_REPLAY_PENDING" and doc["guardrails"]["all_six_numeric_adjudications_awarded"]==0 and doc["guardrails"]["new_source_registry_records"]==0 and doc["guardrails"]["new_transmission_edges"]==0 and doc["guardrails"]["new_algorithm_reopens"]==0,"G893 glyph claim made numeric/lineage without basis")
 for issue in data["issues"]:
  field_rows=issue.get("g893_target_field_reviews",[])
  require(isinstance(field_rows,list),"G893 field reviews must be list")
  if not field_rows:continue
  locs={x["control_id"]:x for x in issue.get("g893_target_page_locators",[])}
  require(len({x["control_id"] for x in field_rows})==len(field_rows),"G893 full-field duplicate")
  for f in field_rows:
   loc=locs.get(f["control_id"])
   require(loc is not None and loc["page_id"]==f["page_id"] and loc["page_sha256"]==f["page_sha256"],"G893 full-field locator mismatch")
   p=Path(f["evidence_doc"])
   require(p.parts[:2]==("docs","research") and ".." not in p.parts,"G893 full-field evidence path")
   e=json.loads((ROOT/p).read_text(encoding="utf-8"))
   o=e["target"];h=e["structural_header"];im=e["source_page"]
   require(o["control_id"]==f["control_id"] and o["original_literal_full_field"]==f["original_literal_full_field"] and o["source_scoped_compact_reading"]==f["source_scoped_reading"],"G893 full-field original glyph mismatch")
   require(h["page_id"]==f["header_page_id"] and h["source_original_sha256"]==f["header_page_sha256"] and h["observed_column_label"]=={"VAR-NUM-LUNAR-L114-DAYRATE":"遲疾曆日率","VAR-NUM-LUNAR-L124-JI-XINGDU":"疾曆限行度"}.get(f["control_id"]) and h["independent_page_sha256_checked_against_report"] is True,"G893 original column header provenance mismatch")
   require(im["page_id"]==f["page_id"] and im["source_original_sha256"]==f["page_sha256"] and im["source_original_jpeg_reviewed"] is True,"G893 source original full-field image mismatch")
   require(f["stage"]=="SOURCE_ORIGINAL_FULL_LITERAL_FIELD_AND_HEADER_VERIFIED" and f["cross_witness_numeric_variant_final_decision"] is None and f["new_source_or_lineage_votes"]==0,"G893 source literal promoted to historical final decision")
   require(o["arithmetic_derivation_and_unit_standardization"]=="PENDING" and o["cross_witness_variant_cause"]=="PENDING" and e["safeguards"]["all_six_cross_edition_arithmetic_variant_decisions_completed"]==0,"G893 new field numerical adjudication premature")
   require(e["safeguards"]["new_source_registry_records"]==0 and e["safeguards"]["new_lineage_edges"]==0 and e["safeguards"]["algorithm_changes"]==0 and e["safeguards"]["historical_12xq_not_rewritten"] is True,"G893 full-field scope leakage")
   if f["control_id"]=="VAR-NUM-LUNAR-L124-JI-XINGDU":
    require(o["original_literal_full_field"]=="一度〇二八一" and o["normalized_numeric_value"] is None and e["physical_source"]["catalog_book_code"]=="GK00893_00" and e["guards"]["ocr_used"] is False,"G893 L124 original glyph source-grade mismatch")
    require(e["archived_original"]["archive_sha256"]=="ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107" and len(e["original_rgb_pixel_regions"]["regions"])==3,"G893 L124 source archive/ROI mismatch")
 for issue in data["issues"]:
  rows=issue.get("g893_field_identity_roi_reviews",[])
  require(isinstance(rows,list),"G893 ROI review list missing")
  if not rows:continue
  locs={x["control_id"]:x for x in issue.get("g893_target_page_locators",[])}
  require(len(rows)==len({x["control_id"] for x in rows}),"G893 ROI duplicate controls")
  for item in rows:
   old=locs.get(item["control_id"])
   require(old and old["page_id"]==item["page_id"] and old["page_sha256"]==item["page_sha256"],"G893 ROI source page binding mismatch")
   p=Path(item["evidence_doc"])
   require(p.parts[:2]==("docs","research") and ".." not in p.parts,"G893 ROI path invalid")
   ev=json.loads((ROOT/p).read_text(encoding="utf-8"))
   matches=[x for x in ev["reviews"] if x["control_id"]==item["control_id"]]
   require(len(matches)==1 and ev["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and ev["book_cd"]=="GK00893_00","G893 ROI physical source mismatch")
   x=matches[0]
   require(x["target_page_id"]==item["page_id"] and x["target_original_jpeg_sha256"]==item["page_sha256"] and x["header_page_id"]==item["header_page_id"] and x["header_original_jpeg_sha256"]==item["header_page_sha256"],"G893 ROI header/target original mismatch")
   require(item["header_page_id"]==("001a" if item["page_id"]=="002b" else "018b"),"G893 ROI wrong table family header")
   require(item["header_page_sha256"]==("8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5" if item["header_page_id"]=="001a" else "4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a"),"G893 ROI unbound header image")
   import re
   for key in ("day_heading_region","table_candidate_region","source_header_region"):
    v=item[key];box=v["rect_px"]
    require(isinstance(box,list) and len(box)==4 and all(type(a) is int for a in box) and 0<=box[0]<box[2]<=1150 and 0<=box[1]<box[3]<=2000,"G893 ROI invalid pixel coordinates")
    require(v==x[key] and re.fullmatch(r"[0-9a-f]{64}",v["rgb_pixel_sha256"]) is not None,"G893 ROI image region hash mismatch")
   require(item["status"]=="PIXEL_REGIONS_BOUND_FIELD_IDENTITY_UNRESOLVED" and item["field_literal"] is None and item["numeric_value"] is None and item["negative_proof"] is False,"G893 ROI falsely promotes numeric field or negative proof")
   require(x["field_identity_positive"] is False and x["field_literal"] is None and x["numeric_value"] is None and x["negative_absence_proven"] is False and x["cross_witness_comparability"]=="PENDING_SOURCE_COLUMN_MAPPING","G893 ROI scope reinterpreted as original glyph")
   require(ev["archive"]["source_jpg_digest_matches"]==ev["archive"]["source_original_jpgs_total"]==204 and ev["guards"]["cross_edition_complete_numeric_decisions_new"]==0 and ev["guards"]["new_external_source_records"]==0 and ev["guards"]["new_historical_physical_witnesses"]==0 and ev["guards"]["new_genealogy_edges"]==0 and ev["guards"]["algorithm_reopens"]==0,"G893 ROI proof source/witness overcount")
 for issue in data["issues"]:
  fields=issue.get("g893_loss_gain_complete_field_reviews",[])
  require(isinstance(fields,list),"G893 loss-gain literal reviews must be list")
  if not fields:continue
  known={x["control_id"]:x for x in issue.get("g893_target_page_locators",[])}
  require(len({x["control_id"] for x in fields})==len(fields),"G893 loss-gain duplicate original field")
  for row in fields:
   loc=known.get(row["control_id"])
   require(loc and row["page_id"]==loc["page_id"] and row["page_sha256"]==loc["page_sha256"],"G893 loss-gain original source-page mismatch")
   p=Path(row["evidence_doc"])
   require(p.parts[:2]==("docs","research") and ".." not in p.parts,"G893 loss-gain evidence path unsafe")
   doc=json.loads((ROOT/p).read_text(encoding="utf-8"))
   matched=[f for f in doc["original_fields"] if f["control_id"]==row["control_id"]]
   require(len(matched)==1 and doc["source_id"]=="EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893" and doc["catalog_book_code"]=="GK00893_00","G893 loss-gain physical copy identity mismatch")
   f=matched[0]
   require(f["page_id"]==row["page_id"] and f["source_jpeg_sha256"]==row["page_sha256"] and f["complete_original_literal"]==row["original_full_literal"] and f["field_identity"]==row["field_identity"],"G893 loss-gain glyph/source evidence mismatch")
   require(f["header_page_id"]==row["header_page_id"]=="018b" and f["header_page_jpeg_sha256"]==row["header_page_sha256"]=="4decd1801d832ba5b471b047dd84cca487245038622a589b48552a0fb43ab83a","G893 loss-gain original header mismatch")
   require(row["source_glyph_grade"]=="SOURCE_ORIGINAL_FULL_LITERAL_LOSS_GAIN_FIELD_ONLY" and row["normalized_numeric_value"] is None and row["cross_witness_final_decision"] is None and row["new_source_votes"]==0,"G893 loss-gain source literal falsely promoted to numerical conclusion")
   require(f["normalized_numeric_value"] is None and f["whole_numeric_variant_adjudication"]=="PENDING_UNIT_FIELD_AND_CROSS_WITNESS_MECHANICAL_REPLAY" and f["independent_physical_witness_votes_added"]==0 and f["no_ocr"] is True,"G893 loss-gain new variant authority claimed")
  symmetric=issue.get("g893_same_copy_symmetric_control_locators",[])
  require(len(symmetric)==2 and {x["limit"] for x in symmetric}=={35,159},"G893 same-copy symmetry page coverage missing")
  for entry in symmetric:
   matching=[x for x in doc["same_copy_symmetry_control_locator_only"] if x["limit"]==entry["limit"]]
   require(len(matching)==1 and matching[0]["page_id"]==entry["page_id"] and matching[0]["sha256"]==entry["page_sha256"] and entry["evidence_doc"]==str(p),"G893 same-copy symmetric page digest mismatch")
   require(entry["status"]=="DAY_HEADER_LOCATED_SYMMETRIC_FIELD_PENDING" and entry["original_target_value"] is None and matching[0]["target_field_original_literal"] is None and matching[0]["target_value_normalized"] is None,"G893 symmetric control falsely treated as collated field")
  require(doc["known_image_archive"]["jpgs_verified_against_original_acquisition_report"]==doc["known_image_archive"]["reported_total_jpgs"]==204 and doc["scope"]["full_numeric_mechanical_variant_decisions"]==0 and doc["scope"]["source_registry_delta"]==0 and doc["scope"]["lineage_edge_delta"]==0 and doc["scope"]["algorithm_reopens"]==0,"G893 loss-gain source or numeric scope inflated")
 require(data["definition"].startswith("NON_EXHAUSTIVE"),"not falsely exhaustive")
 require(len(data["explicit_limits"])>=3 and any("not be recovered" in x for x in data["explicit_limits"]),"unsaved research limitation")
 require(data["binding"]["reviewed_state_version"]==state["schema_version"],"state review missing")
 require(data["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"]),"research focus changed without ledger review")
 require(data["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ")[0],"latest research family review missing")
 require(data["binding"]["branch"]==state["development_branch"] and data["binding"]["repository"]==state["repository"],"repository scope")
 require(set(data["coverage_axes"])==REQUIRED_AXES and len(data["coverage_axes"])==len(REQUIRED_AXES),"coverage axes not exhaustive as method")
 require(data["resolution_policy"]["allowed_statuses"]==["OPEN","BLOCKED_SOURCE_ACCESS","RESOLVED_WITH_EVIDENCE"],"allowed statuses")
 ids=[x.get("id") for x in data["issues"]]
 require(len(ids)==len(set(ids)),"duplicate issue IDs")
 require(BASELINE_IDS.issubset(set(ids)),"baseline research issue silently removed")
 require(len(data["issues"])>=len(BASELINE_IDS),"missing baseline issues")
 matrix=read(MATRIX)
 matrix_ids={x["rule_id"] for x in matrix["rows"]}
 missing_ids={x["rule_id"] for x in matrix["rows"] if x["audit_status"]=="MISSING_FROM_PRODUCT"}
 tracked_ids={rid for x in data["issues"] for rid in x.get("matrix_rule_ids",[])}
 require(tracked_ids.issubset(matrix_ids),"unrecognized Matrix rule coverage reference")
 require(missing_ids.issubset(tracked_ids),"missing product candidate coverage: "+", ".join(sorted(missing_ids-tracked_ids)))
 for x in data["issues"]:
  for key in ("id","title","priority","scope","origin","source_refs","evidence_boundary","missing_evidence","next_action","closure_criteria","history","resolution_evidence"):
   require(x.get(key),"missing issue field: "+x["id"]+" "+key) if key not in ("resolution_evidence",) else require(isinstance(x.get(key),list),"resolution evidence list")
  require(x["status"] in ALLOWED,"issue status "+x["id"])
  require(x["priority"] in ("P0","P1","P2"),"priority "+x["id"])
  if "matrix_rule_ids" in x:
   require(isinstance(x["matrix_rule_ids"],list) and len(x["matrix_rule_ids"])==len(set(x["matrix_rule_ids"])),"duplicate matrix rule IDs "+x["id"])
  require(x["history"][0]["event"]=="REGISTERED_UNRESOLVED","registration lost")
  if x["status"]=="RESOLVED_WITH_EVIDENCE":
   require(x["resolution_evidence"],"closed issue without evidence "+x["id"])
   require(x["history"][-1]["event"]=="RESOLVED_WITH_EVIDENCE" and x["history"][-1].get("evidence_refs"),"resolution event missing "+x["id"])
  else:
   require(not x["resolution_evidence"],"open issue cannot have asserted resolution "+x["id"])
  for s in x["source_refs"]:
   require(isinstance(s,str) and s.startswith("docs/") and ".." not in Path(s).parts,"path escape/unstable evidence ref "+x["id"])
   if exists_fn is not None:
    require(exists_fn(s),"missing primary reference "+x["id"]+": "+s)
 checks=data["checkpoint_log"]
 require(len(checks)>0,"checkpoint log empty")
 require(checks[-1]["state_version"]==state["schema_version"],"checkpoint not latest state")
 require(set(checks[-1]["reviewed_issue_ids"])==set(ids),"unreviewed open items")
 require("Research omission and interruption recovery gate" in protocol and str(LEDGER) in protocol,"protocol missing recovery requirement")
 guard=state["historical_audit"]["research_omission_guard"]
 require(guard["ledger"]==str(LEDGER) and guard["verifier"]=="scripts/verify-research-omission-risk-ledger-r1.py","state guard paths")
 require(guard["version"]==data["version"] and guard["reviewed_state_version"]==state["schema_version"],"state guard synchronization")
 open_count=sum(x["status"]!="RESOLVED_WITH_EVIDENCE" for x in data["issues"])
 require(guard["open_issues"]==open_count and guard["coverage_status"]=="INCREMENTAL_NOT_EXHAUSTIVE","state open count cannot masquerade as exhaustiveness")
 h=state["historical_audit"];i=state["invariants"]
 require(h["row_count"]==h["audited_row_count"]==len(matrix["rows"]) and h["repaired_provenance_metadata_defect_count"]==matrix["audit_summary"]["repaired_provenance_metadata_defect_count"],"historical matrix snapshot")
 manifest=read(MANIFEST)
 require(h["external_source_registry_root_count"]==manifest["root_source_count"] and h["external_source_registry_extension_count"]==manifest["extension_source_count"] and h["external_source_registry_total_unique_count"]==manifest["combined_source_count"],"source registry snapshot")
 require(i["deterministic_fusion_chart_product_r1"]=="CLOSED" and i["algorithm_reopen_count"]==0,"product and algorithm freeze")
 return {"result":"PASS","tracked_issues":len(ids),"open_issues":open_count,"coverage":"NON_EXHAUSTIVE","state_version":state["schema_version"]}
def check_forward_only(old,new):
 before=record_statuses(old);after=record_statuses(new)
 require(set(before).issubset(set(after)),"old issue removed instead of retaining history")
 require(old["coverage_axes"]==new["coverage_axes"],"coverage axes changed without versioned protocol")
 require(new["checkpoint_log"][:len(old["checkpoint_log"])]==old["checkpoint_log"],"prior checkpoint overwritten")
 for k,x in before.items():
  y=after[k]
  for name in ("id","origin","scope"):
   require(x[name]==y[name],"immutable issue identity changed: "+k)
  require(y["history"][:len(x["history"])]==x["history"],"prior issue history overwritten: "+k)
  if x["title"]!=y["title"]:
   require(len(y["history"])>len(x["history"]),"issue title silently changed: "+k)
   last=y["history"][-1]
   require(last.get("event")=="TITLE_CORRECTION" and last.get("previous_title")==x["title"] and last.get("new_title")==y["title"] and "title" in last.get("changed_fields",[]) and last.get("reason") and last.get("evidence_refs"),"title correction lacks original/evidence record: "+k)
  require(set(x["source_refs"]).issubset(set(y["source_refs"])),"prior source reference removed: "+k)
  require(set(x.get("matrix_rule_ids",[])).issubset(set(y.get("matrix_rule_ids",[]))),"prior matrix coverage removed: "+k)
  if x.get("source_page_coverage"):
   require(y.get("source_page_coverage"),"prior source-page coverage missing: "+k)
   require(x["source_page_coverage"]==y["source_page_coverage"],"historical source-page snapshot rewritten: "+k)
  prior_revisions=x.get("source_page_coverage_revisions",[])
  later_revisions=y.get("source_page_coverage_revisions",[])
  require(isinstance(prior_revisions,list) and isinstance(later_revisions,list),"page revisions not append-only list: "+k)
  require(later_revisions[:len(prior_revisions)]==prior_revisions,"source-page revisions rewritten or removed: "+k)
  if len(later_revisions)>len(prior_revisions):
   require(len(y["history"])>len(x["history"]),"new source-page revision without history: "+k)
   last=y["history"][-1]
   require(last.get("event")=="SOURCE_PAGE_REVIEW_REVISION" and last.get("evidence_refs") and last.get("reason"),"new source-page revision needs evidence-scoped history: "+k)
  if x.get("source_page_coverage_interpretation"):
   require(y.get("source_page_coverage_interpretation")==x["source_page_coverage_interpretation"],"prior source-grade interpretation silently rewritten: "+k)
  if x.get("g893_six_control_snapshot"):
   require(y.get("g893_six_control_snapshot")==x["g893_six_control_snapshot"],"historical G893 six-control source snapshot overwritten: "+k)
  older=x.get("g893_target_page_locators",[])
  newer=y.get("g893_target_page_locators",[])
  require(isinstance(older,list) and isinstance(newer,list) and newer[:len(older)]==older,"historic G893 target locators removed/rewritten: "+k)
  if len(newer)>len(older):
   require(len(y["history"])>len(x["history"]) and y["history"][-1].get("event")=="G893_SOURCE_PAGE_TARGET_LOCATOR_APPEND" and y["history"][-1].get("evidence_refs"),"G893 new locator added without cited history: "+k)

  prev_g=x.get("g893_direct_glyph_observations",[])
  next_g=y.get("g893_direct_glyph_observations",[])
  require(isinstance(prev_g,list) and isinstance(next_g,list) and next_g[:len(prev_g)]==prev_g,"G893 observed glyph records removed/rewritten: "+k)
  if len(next_g)>len(prev_g):
   require(len(y["history"])>len(x["history"]) and y["history"][-1].get("event")=="G893_DIRECT_ORIGINAL_GLYPH_OBSERVATION_APPEND" and y["history"][-1].get("evidence_refs"),"G893 newly observed glyph lacks cited history: "+k)
  old_fields=x.get("g893_target_field_reviews",[])
  new_fields=y.get("g893_target_field_reviews",[])
  require(isinstance(old_fields,list) and isinstance(new_fields,list) and new_fields[:len(old_fields)]==old_fields,"G893 prior field review removed/rewritten: "+k)
  if len(new_fields)>len(old_fields):
   require(len(y["history"])>len(x["history"]) and y["history"][-1].get("event")=="G893_SOURCE_FULL_FIELD_COLLATION_APPEND" and y["history"][-1].get("evidence_refs"),"G893 full-field review lacking forward history: "+k)
  prior_roi=x.get("g893_field_identity_roi_reviews",[])
  added_roi=y.get("g893_field_identity_roi_reviews",[])
  require(isinstance(prior_roi,list) and isinstance(added_roi,list) and added_roi[:len(prior_roi)]==prior_roi,"G893 original ROI history lost/rewritten: "+k)
  if len(added_roi)>len(prior_roi):
   require(len(y["history"])>len(x["history"]) and y["history"][-1].get("event")=="G893_FIELD_IDENTITY_PIXEL_SCOPE_APPEND" and y["history"][-1].get("evidence_refs"),"G893 new ROI lacks forward evidence event: "+k)
  for name in ("g893_loss_gain_complete_field_reviews","g893_same_copy_symmetric_control_locators"):
   olditems=x.get(name,[]);newitems=y.get(name,[])
   require(isinstance(olditems,list) and isinstance(newitems,list) and newitems[:len(olditems)]==olditems,"G893 previous loss-gain/symmetry research overwritten: "+k+" "+name)
   if len(newitems)>len(olditems):
    require(len(y["history"])>len(x["history"]) and y["history"][-1].get("event")=="G893_LOSSGAIN_COMPLETE_FIELD_AND_SYMMETRY_LOCATOR_APPEND" and y["history"][-1].get("evidence_refs"),"G893 new original loss-gain field lacks witnessed append event: "+k)
  material=("priority","evidence_boundary","missing_evidence","next_action","closure_criteria")
  changed={name for name in material if x[name]!=y[name]}
  if changed:
   require(len(y["history"])>len(x["history"]),"scope silently changed: "+k)
   last=y["history"][-1]
   require(changed.issubset(set(last.get("changed_fields",[]))) and last.get("reason") and last.get("evidence_refs"),"scope revision missing explicit field/evidence audit: "+k)
  if y["status"]!=x["status"]:
   require(len(y["history"])>len(x["history"]),"status silently changed: "+k)
   last=y["history"][-1]
   require(last.get("from")==x["status"] and last.get("to")==y["status"],"status transition missing scope: "+k)
   require(last.get("evidence_refs") or last.get("reason"),"transition missing evidence: "+k)
   if y["status"]=="RESOLVED_WITH_EVIDENCE":
    require(last["event"]=="RESOLVED_WITH_EVIDENCE","closure without resolution event: "+k)
  if x["status"]=="RESOLVED_WITH_EVIDENCE":
   require(y["resolution_evidence"][:len(x["resolution_evidence"])]==x["resolution_evidence"],"historical resolution evidence removed: "+k)
 return {"status":"PASS","old_issues_preserved":len(before)}
def parent_revision():
 p=subprocess.run(["git","show",f"HEAD^:{LEDGER.as_posix()}"],cwd=ROOT,capture_output=True,text=True)
 if p.returncode:
  # Initial installation only: ensure it was actually added this commit.
  check=subprocess.run(["git","diff-tree","--no-commit-id","--name-status","-r","HEAD","--",LEDGER.as_posix()],cwd=ROOT,capture_output=True,text=True)
  require(check.returncode==0 and any(s.startswith("A") for s in check.stdout.splitlines()),"cannot compare parent ledger; fetch at least 2 commits")
  return None
 return json.loads(p.stdout)
def verify(check_parent=False):
 data=read(LEDGER)
 result=validate(data,read(STATE),(ROOT/PROTOCOL).read_text(encoding="utf-8"),lambda x:(ROOT/x).is_file())
 if check_parent:
  previous=parent_revision()
  result["parent_check"]=check_forward_only(previous,data) if previous is not None else {"status":"INITIAL_LEDGER_COMMIT"}
 return result
if __name__=="__main__":
 a=argparse.ArgumentParser()
 a.add_argument("--check-parent",action="store_true")
 args=a.parse_args()
 print(json.dumps(verify(args.check_parent),ensure_ascii=False))
