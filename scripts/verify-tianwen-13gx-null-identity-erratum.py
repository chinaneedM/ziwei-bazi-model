#!/usr/bin/env python3
"""13GX: old false gate != proof of mechanical non-equivalence; forward-only null overlay."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GX-FOURFEN-CHUDU-UNKNOWN-IDENTITY-ERRATUM-R1.json"
def blob(data):return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def check(x):
 assert x["schema"]=="TIANWEN-13GX-FOURFEN-CHUDU-UNKNOWN-IDENTITY-ERRATUM-R1" and x["issue_id"]=="TW-OPEN-0005"
 assert x["kind"]=="FORWARD_ONLY_EPISTEMIC_SEMANTIC_CORRECTION"
 s=x["source_snapshot"];p=ROOT/s["file"];raw=p.read_bytes();assert blob(raw)==s["git_blob_sha"]
 old=json.loads(raw);q=old["inference_firewall"]; assert q["fourfen_chudu_are_mechanical_identical"] is False and q["fourfen_chudu_relation_adjudicated"] is False
 assert q["source_specific_day14_fourfen_field_bound"] is None and q["original_ancient_unit"] is None
 assert old["source"]["source_image_rgb_sha256"]==s["source_original_rgb_sha256"]
 assert s["prior_flag_value"] is False and s["prior_relation_adjudicated"] is False and s["preserved_immutable"] is True
 c=x["correction"]
 for key in ("effective_fourfen_chudu_mechanical_identity","effective_fourfen_chudu_ancient_unit_identity","original_complete_D14_numeric","original_D14_terminal","old_D9_numeric","old_D30_numeric","independent_physical_copy"):assert c[key] is None,key
 assert c["effective_relationship_status"]=="UNADJUDICATED"
 assert c["effective_column_heading_readings"]==["四分","初度"]
 assert c["heading_scope"]=="SOURCE_SURROGATE_VISUAL_PROVISIONAL_ONLY"
 assert c["previous_false_interpretation"]=="NEGATIVE_GUARD_AGAINST_POSITIVE_MERGER_NOT_PROVEN_NON_EQUIVALENCE"
 for k in ("direct_original_disproof_of_equivalence","direct_original_proof_of_equivalence","proven_non_edge","new_source_observation"):assert c[k] is False,k
 assert x["guards"]=={"chart":"CLOSED","algorithm_reopens":0,"candidate_collapses":0,"matrix":[222,222],"registry":761,"genealogy":[252,238],"issues_open":11,"g893_six":"OPEN","old_d5":"〇/五_UNRESOLVED","old_13EI":"RETRACTED","new_physical_witnesses":0,"non_edges_added":0}
 t=x["transmission_impact"]
 assert all(t[k]==[] for k in ("edges_supported","edges_revised","edges_rejected","non_edges_added"))
 return True
if __name__=="__main__":
 print("13GX_PASS_FORWARD_NULL_OVERLAY_PRESERVES_OLD_SOURCE" if check(json.loads(E.read_text(encoding="utf8"))) else "FAIL")
