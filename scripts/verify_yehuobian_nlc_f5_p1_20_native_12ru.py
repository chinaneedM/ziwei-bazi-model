#!/usr/bin/env python3
"""12RU F5 p1-20 source archive hashes and visual evidence firewall."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RU-NLC411999003250-F5-P1-20-NATIVE-REVIEW-R1.json"
QL=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json"
QM=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QM-NLC411999003250-FASC4-5-SCOPED-MANUAL-IMAGE-TRIAGE-R1.json"
PINS=["7b6499149c1a0f21c7dc2e03018af90eafc390001115c9969a64a7b88c0f37e7","b8a0b07385b9512a46b4ab2ddb97d6621d03829b16c8cfbb9a79cf810b63713f","ffceaa880828fdc6a36e56fe495d2c437cc44b127f5cc82f7687c3e53a98c479","f45643381b396e3b7f6f426ac017a896b4bc4c7a4f15cfa7c21f69bfd0332075","f7eb7c4acd0b9187e194591551be68ff2d04f469277e3a474759f425b4406331","614bbada9156067701db683ed14ef054d1da0ffb465246c0fca0c72ee7ea3ecf","909391bdfd7307b12b5a14d974ad1af1902d78695e207ecc28491ba6c0d6255e","ee7afd45b5a08132f38b05a8803daf02419a944698deb81f630a0aef16459b6e","8c24e39229ed6334e41b7ab8ca0d9cc65be949b9caacfdea74617ae2deeefe08","3a752d0939deaa27f3b1e0c9b81dcf436dbab7a6713d4e2db3aa6003cf1aaf89","47bb60e5cd1c1a0399f0daec70433352c8aaa56873e131fb9e5bd3ad53b0fd51","4050541744c0ba1cb994351584857038931e33dc75274aa9625a5ecbcc109344","981f9f4e985b1d95084d4cb2db9a45a5409182679a255ccaf9d16f635f944334","1a8455a050faf0480969396d7df5f5297b50c8a6bb17defffafb5f8b156db6ac","4f63deeaec17b7765bce84adcd610cfb56f0149be9a3724fed90033fa503ce02","58a1db3e3ec7ec6d2cbd9a0c7b503ec27f4abf732faf3649483cc1286862330b","cadf3f9f75ecbd14b88df2cd415dd7b31ceec2b4e8b71558b7dc2990f86ec72d","96b567d89c5219c442dae367d4e59f5cb9b2cabc5ab7d91fdadd9407bcf4983c","12ac64bdcd62fa3db2d103b83d891987234667b2869838be0650ab85700b239f","63a7652b3ec7acfa70a513c557506c58d5c2c3cbdfd8ee7c53231af87e603c06"]
CHAIN20="a6d58dbc294970c879225acadca29c101a66dc6acf3e16afd2b4781b8b6cf48e"
CHAIN63="d66546a59822762c76936edd93d5fd11db907ffdf9dd247b69be50066592c950"
def read(p):return json.loads(Path(p).read_text(encoding="utf-8"))
def chain(a):return hashlib.sha256("".join(a).encode("ascii")).hexdigest()
def verify(record_path=RECORD,ql_path=QL,qm_path=QM):
 d,ql,qm=(read(p) for p in (record_path,ql_path,qm_path))
 s,v,q=d["source"],d["review"],d["queue"]
 ql5=next(x for x in ql["sources"] if x["fascicle"]==5)
 qm5=next(x for x in qm["checked_artifacts"] if x["digital_fascicle"]==5)
 if not(d["batch"]=="12RU" and d["stage"]=="12QE_OPEN" and d["parent_open_batch"]=="12QE"
  and d["status"]=="F5_P1_20_ORIGINAL_JPEG_BOUNDED_VISUAL_SCREEN_NOT_FULLTEXT"
  and s["holding"]=="NLC411999003250_ONE_HOLDING"
  and s["fascicle"]==ql5["fascicle"]==5 and s["commons"]=="NLC892-411999003250-383066"
  and s["catalogue_original_juan"]==ql5["volume_labels"]==[10]
  and s["source_pdf_pages"]==ql5["source_pdf_pages"]==63
  and s["artifact_id"]==ql5["artifact_id"]==11674555957
  and s["pdf_sha256_inherited"]==ql5["source_pdf_sha256"] and s["pdf_binary_rehashed"] is False
  and s["zip_sha256"]=="89d314baafc615809a2ba906bb308bedbe130bd7f100571724cdba8a27978c36"
  and s["status_sha256"]=="73a464cf649f92226d6f016ad50acb71d2f1f00a32ba8bf9c7c43eb3828d77a7"
  and s["original_jpeg_hash_size_checked"]==63 and s["original_jpeg_mismatch"]==0
  and s["full63_ordered_jpeg_sha256_chain"]==CHAIN63):raise ValueError("12RU_SOURCE_ARCHIVE_DRIFT")
 h=v["image_pins"]
 p1=next(x for x in qm5["original_pages_opened"] if x["page"]==1)["jpeg_sha256"]
 heading=next(x["exact_opening"] for x in ql["direct_new_manual_volume_headings"] if x["fascicle"]==5)
 if not(v["mode"]=="NATIVE_SOURCE_JPEG_FIVE_2X2_PAGE_MONTAGE_BOUNDED_HEADING_TOPIC_REVIEW_NOT_LINEWISE"
  and (v["pdf_first"],v["pdf_last"],v["images_page_by_page_visited"])==(1,20,20)
  and h==PINS and chain(h)==v["first20_chain"]==CHAIN20 and h[0]==p1
  and v["first_page_juan_heading"]==heading=="萬曆三十五年丁未卷十"
  and v["previous_heading_source"]=="12QL"
  and [x["pages"] for x in v["topics"]]==[[1,4],[5,8],[9,12],[13,16],[17,20]]):raise ValueError("12RU_HEADING_OR_PAGE_HASH_DRIFT")
 false_fields=("original_old20_gaizao_louke_glyph_attested","ocr_performed","fulltext_linewise_collated",
              "page_target_absence_proven","whole_fascicle_target_absence_proven","whole_work_target_absence_proven")
 if any(v.get(x) is not False for x in false_fields) or v["physical_copy_increment"]!=0:
  raise ValueError("12RU_FALSE_GLYPH_ABSENCE_OR_INDEPENDENT_WITNESS")
 if not(q=={"previous":"12RT","f5_source_pages":63,"f5_current_screened":[1,20],
  "f5_remaining":[21,63],"remaining_firstpass_pages":43,
  "global_native_accounting_not_recomputed":True,"old_global_native_count":339,
  "old_global_preview_count":689,"whole_body_fulltext_pages_remaining":1027}
  and d["transmission_impact"]["edges_supported"]==[]
  and d["invariants"]=={"matrix":"222/222","repaired_metadata":"45/45",
   "source_registry":"647+7=654","product_r1":"CLOSED","algorithm_reopens":0,
   "md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT"}):
  raise ValueError("12RU_QUEUE_OR_INVARIANTS_DRIFT")
 return {"batch":"12RU","f5_native_bounded":"20/63","f5_remaining":43,
     "fullbody_text_collation_pending":1027,"original_target_presence_or_absence_proven":False}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
