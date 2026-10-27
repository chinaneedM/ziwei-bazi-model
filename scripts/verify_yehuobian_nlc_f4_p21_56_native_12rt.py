#!/usr/bin/env python3
"""12RT original F4 p21-56 hash pinned visual scope and overlapping old-review gate."""
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RT-NLC411999003250-F4-P21-56-NATIVE-DEDUP-R1.json"
RS=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RS-NLC411999003250-F4-P1-20-NATIVE-IMAGE-SCREEN-R1.json"
QM=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12QM-NLC411999003250-FASC4-5-SCOPED-MANUAL-IMAGE-TRIAGE-R1.json"
PINS=["4ff5735ca091a36b46999a474250597f602cc9f9b1ec2c7334e823a300fc771f","f33b6934db79b5c01c24ef5b7582f45078d8ce145194eb6fe37904f12dc0c9dd","5e795b0ff7be0da22202a68b76c4c5d0d5b247ee06a51117096edc0ce1e836de","0e046f3911e1e2df35e72a8dc408b8df6dc128bee348782b4929f1818958cf53","8313c588cc24c7d123aa3919e827c1ea3f744c2138a853ab95cc74cf0b7ebca8","89fc00d03a92611a4d9ac9109b1531f927239b644c0bccf555beae5866156f22","42db470a16529b0cc7845fa6a5add7582a1aaed2cf219f7284718fce39169216","8e674a47b1bbd051e5c4e65e5c4959a4235bb16272d6a54a40d8e4f8a27a4440","e5f7304bd9e814137ab936e528fa353f610f02bf3a4c437ea0acf510a93d33f0","2fff5cd750b8b10a1f4a2c9a184a1aa4cd17615a68af0dfe37ca229d21a6d079","040912c0bab191bf698b5683645986ca66e258781bfc594da6c4588943ebf6dc","b66ee30ef41b0845b4083f97295979e1a3aec94befd0455d65ba92a768f9d02e","f74a977ebf0b866cf190ab697ef072bed0ccb9fc9ff3be34cae73a6594eb2416","26acf4bd04a122da8fc2bd0f5e17ad37bca8250170f5e0847846f1f52510a7d2","320a25d6902b0e5e0a4e9931eda67b2882195f6f96abdfb862c4b1ef0afa8e76","1f8d225bb49b7924b76d5a31d43fb86d2fa38e1bae5ff92cbf9918ea52c98e7c","495d94a94bb2a32f817f303e4cc70e2e8a8f15ba4e674f929bcbe5f862e5be00","685a9dd89172234fa8c47c51e7547c091e3de652ddf439862b88dbadcba7225a","bcc7e336e5a8b0a5dd799b61dac3eeb968cf38db2c679f976f09439efd2a5aa1","4df5cb7e109f22429d67a65279517a5ba99c5d3fdc426e26c9729cb9aa1d132a","2636275778f50549ee17985d1a6d54eb4424bad0d7392b4b62e5029ec0e2d35b","95cb3606205807bbd6739721fb60b277a396e25564c529f47cc7c5fb9fcc0e84","ee6a9a210f84730dffdf4b9900ef33634acbc6269c0b559b39238b4904bcbbda","3aacf311bea31f93c39f5ff8805651919301ca4c4976292eb8aa2cdebec634ba","7df40fe0ed6cb3c2fb986cd85259f2466c1d578d3f6ce7f1b7c670e1f40f512b","8bda0aba09bfd74fd3f46cd24425fa1308bc188459a6d9e6fc78a3cdb214c8ff","1ad4962b3a3bd2ad82666492ddc6d711993f6e533b4937e8119d0ddaeb956159","b1bb1225bac491cc33adac9af2816b9cbc090fa987309b1b365d64a5e0d30abd","8ff0e194b365bbb807b3c60b71125a8ee25adf134626f99424202110acef7bf5","2ed808c199b58ec0e7342516c77be181bd22a93cfc707e7d7fccbb9b142b07a1","5390b96ae6cc93fa19ea23978a142fb5ef3ad54bff0e4b25965a931d2d065033","63f85bd60c84487e3d0f5347eda447f4a798590fdeabb736fc4090aa53b615b3","319ce1a6efb676c2b8b42739927fa645b255bf147a534f15e8f7a26d07635323","0eb58be8e5f5f600f4a9917bde908db8f9aeb188de378b3b2887e0781d593c4f","656adab5ab430f181f8b846d32502a7a806e86b5d013bd2388e0b604f25778df","c0500d19b5b3033fb89f5a0b68cbbb3117f4a75cfb9814ea3ecfd28c7fe3ebad"]
FIRST20="8a443e749f36b5f5f187ec2ad027df4fd9ccc3e3649b0390f02e10e99e83e2a9"
CHAIN36="3b078a3c35a75817ce7e26b2aeb4c9d9a50a7436774f2a5133fae66eb0dad119"
CHAIN56="b1866e1fe3cf4c3b73f87d88699d1dae31e6e1ea65aa7c545072d15c0006c8e1"

def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def chain(v): return hashlib.sha256("".join(v).encode("ascii")).hexdigest()
def verify(record_path=RECORD,rs_path=RS,qm_path=QM):
 d,rs,qm=(read(p) for p in (record_path,rs_path,qm_path))
 s,v,u,q=d["source"],d["review"],d["identity_dedup"],d["queue"]
 p=rs["source"]; old=rs["review"]; qm4=next(x for x in qm["checked_artifacts"] if x["digital_fascicle"]==4)
 if not(d["batch"]=="12RT" and d["parent_open_batch"]=="12QE" and d["stage"]=="12QE_OPEN"
   and d["status"]=="F4_56_56_SOURCE_BOUNDED_VISUAL_REVIEW_DEDUP_ONLY_NOT_FULLTEXT"
   and s["holding"]==p["physical_holding"]=="NLC411999003250_ONE_HOLDING"
   and s["fascicle"]==p["fascicle"]==4 and s["commons_id"]==p["commons_file_id"]
   and s["source_pdf_pages"]==p["source_pdf_pages"]==56
   and s["pdf_sha256_inherited_from_12ql"]==p["source_pdf_sha256_from_12ql"]
   and s["pdf_binary_rehashed_this_batch"] is False
   and s["artifact_id"]==p["archive_artifact_id"]==11674246374
   and s["archive_zip_sha256"]==p["archive_zip_sha256"]
   and s["manifest_sha256"]==p["archive_status_json_sha256"]
   and s["jpeg_sources_rechecked"]==56 and s["jpeg_sha_or_size_drift"]==0
   and s["full56_chain"]==p["whole_56_source_jpeg_sha256_concatenation_chain"]==CHAIN56):raise ValueError("12RT_SOURCE_IDENTITY_DRIFT")
 first=old["source_jpeg_sha256_in_pdf_order"];last=v["source_jpeg_shas"]
 if not(v["mode"]=="ORIGINAL_PIXELS_PAGES_DISPLAYED_IN_NINE_2X2_MONTAGES_PAGE_BOUNDED_REVIEW_NO_LINE_BY_LINE_TRANSCRIPTION"
   and (v["first_page"],v["last_page"])==(21,56)
   and v["source_pages_sha_and_size_verified"]==36 and v["images_displayed_for_visual_review"]==36
   and last==PINS and len(first)==20 and len(last)==36
   and chain(last)==v["window_chain"]==CHAIN36
   and chain(first)==v["first20_chain"]==FIRST20
   and chain(first+last)==v["combined56_chain"]==CHAIN56
   and [x["pages"] for x in v["observations"]]==[[21,24],[25,28],[29,36],[37,44],[45,52],[53,56]]):
  raise ValueError("12RT_WINDOW_HASH_OR_VISUAL_BOUNDARY_DRIFT")
 blocked=("new_old_juan9_title_direct_attestation","old20_gaizao_louke_original_target_glyph_found","fulltext_collated",
 "ocr_performed","page_target_absence_proven","whole_fascicle_absence_proven",
 "whole_old20_work_target_absence_proven","original_juan_equivalence_to_1827_proven")
 if any(v.get(x) is not False for x in blocked):raise ValueError("12RT_FALSE_GLYPH_OR_ABSENCE_PROOF")
 source_map={i+1:sha for i,sha in enumerate(first+last)}
 qm_source={x["page"]:x["jpeg_sha256"] for x in qm4["original_pages_opened"]}
 if not(u["key"]=="NLC411999003250/fascicle4/pdf-page/source-JPEG-SHA256"
   and u["review12rs_pages"]==[1,20] and u["review12rt_pages"]==[21,56]
   and u["previous12qm_source_pages"]==sorted(qm_source)==[1,19,27,56]
   and u["current_window_previous12qm_overlap"]==[27,56]
   and u["old_12ql_heading_page"]==1
   and all(source_map[i]==sha for i,sha in qm_source.items())
   and len(source_map)==len(set(source_map))==u["f4_distinct_source_pdf_pages_reviewed"]==56
   and u["source_p1_to_p56_bounded_visual_coverage"] is True
   and u["full_holding_1030_page_source_union_completed"] is False
   and u["global_source_visual_totals_recounted"] is False):raise ValueError("12RT_DOUBLE_COUNT_OR_SOURCE_REBINDING_DRIFT")
 if not(q=={"previous_batch":"12RS","f4_pages_total":56,"f4_remaining_visual_pages":0,
  "prior_global_native_count":339,"prior_global_preview_count":689,
  "new_global_native_count":None,"new_global_preview_count":None,
  "full_text_body_pages_pending":1027,"next":"F5_P1_63_AND_LOCATE_OLD20_GAIZAO_LOUKE_DIRECT_FOLIO"}
  and d["transmission_impact"]["edges_supported"]==[]
  and d["invariants"]=={"matrix":"222/222","metadata_repairs":"45/45","source_registry":"647+7=654",
   "product":"CLOSED","md_g03":"OPEN","hpa_dayun_cal_002":"MISSING_FROM_PRODUCT","algorithm_reopens":0}):
  raise ValueError("12RT_SCOPE_OR_INVARIANT_DRIFT")
 return {"batch":"12RT","f4_native_firstpass":"56/56","newly_reviewed_window":36,
  "prior_overlap":[1,19,27,56],"full_body_text_pages_pending":1027,
  "global_count_deferred":True,"old20_target_presence_or_absence_proven":False}
if __name__=="__main__":print(json.dumps(verify(),ensure_ascii=False,indent=2))
