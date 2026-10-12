#!/usr/bin/env python3
"""Kyoto Letters source-bound original-leaf inquiry; an unsent draft is not permission."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD="docs/research/MING-DATONG-YEHUOBIAN-12UV-KYOTO-LETTER-LIBRARY-SPECIFIC-INQUIRY-R1.json"
PACKET="docs/research/MING-DATONG-YEHUOBIAN-12UU-ORIGINAL-JUAN20-ACQUISITION-PACKET-R1.json"
UM="docs/research/MING-DATONG-YEHUOBIAN-12UM-KYOTO-DUAL-ITEM-ACQUISITION-GATE-R1.json"
EXPECTED={
 ("BB05477307","BVIb||Y||2 200023037620","JUAN20_ORIGINAL_LEAF"),
 ("BB18578034","B||VIb||9-1 188987L","JUAN20_ORIGINAL_LEAF"),
 ("BB18578034","B||VIb||9-1 188987","FRONTMATTER_DATE_ONLY")
}
TRUE_GUARDS=(
"main_central_library_policy_does_not_apply_automatically",
"rare_book_form_only_if_item_specific_classification_requires",
"generic_wakan_copy_warning_not_item_specific_denial",
"older_external_guidance_currentness_unconfirmed",
"no_physical_original_juan20_image_obtained",
"digital_archive_general_iiif_support_not_item_manifest",
"preface_dated_1827_not_print_impression_proof",
"frontmatter_not_juan20_glyph_witness",
"same_edition_not_proof_of_shared_plates",
"no_individualized_copy_permission","no_remote_submission","no_library_contact_sent","no_fees_paid",
"no_historical_glyph_votes","no_algorithm_reopen"
)
def validate(record,packet,um):
 if record.get("schema")!="TIANWEN-12UV-KYOTO-LETTERS-EXACT-ITEM-INQUIRY-GATE-R1":
  raise ValueError("schema")
 if record.get("status")!="DRAFT_NOT_SENT" or record.get("collection_scope")!="KYOTO_UNIVERSITY_GRADUATE_SCHOOL_OF_LETTERS_LIBRARY_NOT_CENTRAL_LIBRARY":
  raise ValueError("institution or preflight status")
 src=record.get("authority_sources",[])
 if not any(x.get("url")=="https://www.kulib.kyoto-u.ac.jp/newdb/12109" for x in src):
  raise ValueError("missing first-party Letters service policy")
 items=record.get("items",[])
 if len(items)!=3 or {(x.get("ncid"),x.get("call_number"),x.get("role")) for x in items}!=EXPECTED:
  raise ValueError("three distinct item/role bindings")
 prior={x["source_issued_item_identifier"] for x in packet["original_copy_candidates"] if x["institution_group"]=="KYOTO"}
 if prior!={"BVIb||Y||2 200023037620","B||VIb||9-1 188987L"}:
  raise ValueError("original source-item candidate queue changed")
 um_items={x["source_issued_call_number"]:x["role"] for x in um["distinct_request_items"]}
 if um_items.get("B||VIb||9-1 188987")!="PREFACE_FRONTMATTER" or um_items.get("B||VIb||9-1 188987L")!="JUAN20_TARGET":
  raise ValueError("frontmatter role conflated with target")
 for x in items:
  if x.get("catalog_url")!="https://ci.nii.ac.jp/ncid/"+x["ncid"] or x.get("original_image_url") is not None or x.get("original_folio") is not None or x.get("print_state")!="UNVERIFIED":
   raise ValueError("catalogue identity or original evidence prematurely asserted")
 if len(record.get("source_dependent_inquiry_goals",[]))!=5:
  raise ValueError("inquiry prerequisites")
 if any(record.get("policy_boundaries",{}).get(k) is not True for k in TRUE_GUARDS):
  raise ValueError("historical/permission boundary promoted")
 acq=record.get("acquisition",{})
 if any(acq.get(k) is not False for k in ("sent","payment","item_specific_permission")):
  raise ValueError("external action not authorized by draft")
 if any(acq.get(k)!=0 for k in ("exact_images","original_glyph_votes","new_external_source_count")):
  raise ValueError("unearned new ancient source")
 a=record.get("accounting",{})
 if (a.get("sources"),a.get("matrix_rows"),a.get("audited"),a.get("repairs"),a.get("graph_nodes"),a.get("graph_edges"),a.get("formal_batches"),a.get("product"),a.get("algorithm_reopens"))!=(687,222,222,45,250,237,487,"CLOSED",0):
  raise ValueError("project accounting changed")
 return {"status":"PASS","original_juan20_items":2,"paratext_only_items":1,"inquiries_sent":0,"ancient_glyph_votes":0}
def verify(root=ROOT):
 def load(p):return json.loads((root/p).read_text(encoding="utf-8"))
 return validate(load(RECORD),load(PACKET),load(UM))
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,sort_keys=True))
