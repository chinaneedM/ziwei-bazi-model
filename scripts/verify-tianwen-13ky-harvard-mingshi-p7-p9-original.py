#!/usr/bin/env python3
"""13KY source-native Harvard Ming Shi v11 PDF P7/P9 direct original glyphs; optional pixel replay."""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13KY-HARVARD-MINGSHI-V11-P7-P9-DIRECT-ORIGINAL-DUAL-GLYPHS-R1.json"
P="docs/research/TIANWEN-13KT-HARVARD-MINGSHI-V11-J35-DIRECT-ORIGINAL-THREE-CONSTANTS-R1.json"
R="docs/research/TIANWEN-13KV-MINGSHI-V35-THIRTEEN-SYNODIC-REM-RUBRIC-RECEIVED-VARIANTS-R1.json"
Q="docs/research/TIANWEN-13KW-MINGSHI-V35-13KU-SOURCE-ATTRIBUTION-FORWARD-ERRATUM-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def ensure(v,s):
 if not v:raise ValueError(s)
def read():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (E,P,R,Q,S,L))
def sha(data):return hashlib.sha256(data).hexdigest()
def verify(e,old,variants,erratum,state,ledger,pdf=None):
 ensure(e["schema"]=="TIANWEN-13KY-HARVARD-MINGSHI-V11-P7-P9-DIRECT-ORIGINAL-DUAL-GLYPHS-R1" and e["issue_id"]=="TW-OPEN-0005","identity")
 src=e["source"];pages=e["source_native_page_collations"];comp=e["comparison"];ar=e["fractional_replay"]
 ensure(src["original_file_sha256"]==old["provenance"]["source_sha256"]=="36a2a99461d9d16a71e203d95ffa6cac189f1bbab94295de51ed6d3b60bd649b","original bytes digest")
 ensure(src["original_file_bytes"]==old["provenance"]["source_bytes"]==70809419 and src["pdf_page_count"]==74,"source file length")
 ensure(src["source_existing_13kt_receipt"]==P and src["recovered_existing_artifact_run_id"]==40891158390 and src["recovered_existing_artifact_id"]==12904614601,"recovered artifact identity")
 ensure(src["distinct_original_physical_impressions_new"]==src["source_registry_new_entries"]==0 and src["actual_1739_edition_impression_authenticated"] is False and src["s_other_original_copy_or_recension_authenticated"] is False,"no counterfeit physical copy")
 ensure(len(pages)==2 and [x["pdf_page_1_based"] for x in pages]==[7,9] and [x["pdf_zero_index"] for x in pages]==[6,8],"page order")
 known=[
 ([1800,1549],"b1e6e6065b9816ee8abbfb31ca36304a8af01c730a79275237116af0d9511e1f",[1035,220,1230,1210],"fff1575bcf1e94a81c285a5d804a890e529456ba832d501962abc17ea0c32961","有閏加二十三萬八九七七○九"),
 ([1800,1551],"9078906ef067886b1bd2fc98c069fd90861cad795d50204c31c930f0b8605fef",[920,210,1370,1220],"13fbbdcc23e7554690d37c50ad71e0e3d957678004d4e7c53a3f0a4adca37146","推遲疾限各置遲疾歷以日轉限乘之即得限數")]
 for item,expected in zip(pages,known):
  size,page_sha,box,roi_sha,glyph=expected
  ensure(item["rgb_image_size"]==size and item["full_page_rgb_sha256"]==page_sha and item["roi_xyxy"]==box and item["roi_rgb_sha256"]==roi_sha,"original pixel hash")
  ensure(item["positive_glyph"]==glyph and item["pixmap_render"]=="PyMuPDF RGB 1.0x alpha=False no OCR","original glyph and method")
 ensure(comp["ordinary_received_quote_number"]==variants["sources"]["common_received"]["phrase_month_13"].replace("有閏，加","有閏加"),"ordinary transcript numeric")
 ensure(comp["ordinary_received_quote_subject"]=="各置遲次歷" and comp["siku_labeled_received_subject"]=="各置遲疾歴","cross scope")
 ensure(comp["siku_labeled_received_number"]==variants["sources"]["siku_received"]["phrase_month_13"],"Siku received number")
 ensure(comp["original_harvard_subject"]=="遲疾歷" and comp["original_harvard_number_replays"]=="238977.09","cross-scope originals")
 ensure(comp["crosswise_evidence_must_be_scoped_per_phrase"] is True and comp["one_printed_volume_is_one_physical_citation_family"] is True,"source scope")
 for k in ("original_siku_288977_original_image_confirmed","common_wikisource_chici_is_a_false_reading_proven","handwritten_or_printed_recension_genealogy_proven","thirteen_month_formula_index_rounding_calendar_date_proven"):
  ensure(comp[k] is False,"unearned source promotion "+k)
 ensure(erratum["transition"]=="FORWARD_ONLY_SOURCE_ATTRIBUTION_ERRATUM_NO_PREVIOUS_EVIDENCE_REWRITE","preserve original erratum")
 period=F(ar["period_basic_units"]);mod=F(ar["modulus_basic_units"]);q=(ar["months"]*period)//mod
 rem=ar["months"]*period-q*mod
 ensure(period==F("295305.93") and mod==600000 and ar["months"]==13 and q==ar["quotient"]==6 and rem==F("238977.09") and F(ar["remainder_basic_units"])==rem,"original 13-month arithmetic")
 ensure(ar["matched_prior_13kv_harvard_original_13month_candidate"] is True and ar["does_not_match_siku_received_variant"] is True and F(ar["numerical_difference_from_siku_received_basic_units"])==50000,"source-scoped comparison")
 a=e["adjudication"]
 for k in ("upgraded_from_received_only_in_13kv_for_harvard_specific_p7_numeric_glyph","upgraded_from_received_only_in_13ku_for_harvard_specific_p9_operator_glyph","old_13ku_received_quote_source_attribution_erratum_13kw_still_valid"):ensure(a[k] is True,"positive new source and erratum")
 for k in ("historical_83_84_limit_index_selected","historical_167_168_mechanism_equivalent_proven","physical_copy_edition_impression_year_proven"):ensure(a[k] is False,"not a historic selection")
 for k in ("original_g893_six_historical_numeric_winners","new_independent_historical_source_vote","new_transmission_nodes","new_transmission_edges","chart_algorithm_reopens"):ensure(a[k]==0,"unearned historical vote")
 ensure(a["product"]=="CLOSED" and a["research_risks_open"]==11 and e["counts"]==dict(registered_sources=765,matrix_rows=222,graph_nodes=252,graph_edges=238,risks_open=11),"counts and scope")
 ensure(not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"],"no lineage")
 h=state["historical_audit"];binding=ledger["binding"];i=state["invariants"]
 ensure(state["schema_version"]==h["research_omission_guard"]["reviewed_state_version"]==binding["reviewed_state_version"],"state review sync")
 ensure(h["current_focus"][-1].startswith("13KY ") and binding["latest_research_focus_prefix"]=="13KY" and binding["source_focus_count"]==len(h["current_focus"]),"current research")
 ensure(i["deterministic_fusion_chart_product_r1"]=="CLOSED" and i["algorithm_reopen_count"]==0 and h["external_source_registry_total_unique_count"]==765 and h["row_count"]==h["audited_row_count"]==222,"chart invariant")
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 ensure(issue["status"]=="OPEN" and issue["priority"]=="P0" and issue["next_action"].startswith("13KY CURRENT ACTION:"),"unresolved issue next")
 ensure(E in issue["source_refs"] and E.replace(".json",".md") in issue["source_refs"] and any(z.get("revision_id")=="TW-OPEN-0005-13KY-HARVARD-P7-P9-ORIGINAL-20261030" and E in z.get("evidence_refs",[]) for z in issue["history"]),"forward event")
 ensure(len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"],"ledger review")
 if pdf is not None:
  import fitz
  from PIL import Image
  pdf=Path(pdf);raw=pdf.read_bytes()
  ensure(sha(raw)==src["original_file_sha256"] and len(raw)==src["original_file_bytes"],"raw source PDF bytes")
  doc=fitz.open(stream=raw,filetype="pdf");ensure(len(doc)==74,"PDF pages")
  for p in pages:
   pix=doc[p["pdf_zero_index"]].get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
   im=Image.frombytes("RGB",(pix.width,pix.height),pix.samples)
   ensure(list(im.size)==p["rgb_image_size"] and sha(im.tobytes())==p["full_page_rgb_sha256"],"native page RGB")
   ensure(sha(im.crop(p["roi_xyxy"]).tobytes())==p["roi_rgb_sha256"],"native source ROI")
  doc.close()
 return dict(status="PASS",native_original_pages=[7,9],replayed_pdf_pixels=pdf is not None,harvard_printed_remainder=str(rem),harvard_original_object=comp["original_harvard_subject"],historical_winners=0,algorithm_reopens=0)
if __name__=="__main__":
 parser=argparse.ArgumentParser();parser.add_argument("--pdf",type=Path);args=parser.parse_args()
 print(json.dumps(verify(*read(),pdf=args.pdf),ensure_ascii=False))
