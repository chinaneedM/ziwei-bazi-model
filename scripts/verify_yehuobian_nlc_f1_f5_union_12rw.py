#!/usr/bin/env python3
"""12RW: replay bounded source-image page identity for NLC old20 F1–F5 only."""
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/"docs/research/MING-DATONG-YEHUOBIAN-12RW-NLC411999003250-F1-F5-NATIVE-PAGE-UNION-R1.json"
LAYOUT=[["12QZ",1,3,22],["12RA",1,23,42],["12RB",1,43,62],["12RC",1,63,88],["12RD",1,89,119],["12RF",2,1,20],["12RH",2,21,40],["12RI",2,41,60],["12RJ",2,61,72],["12RK",3,1,20],["12RL",3,21,40],["12RM",3,41,60],["12RO",3,61,80],["12RN",3,81,84],["12RP",3,85,104],["12RQ",3,105,121],["12RS",4,1,20],["12RT",4,21,56],["12RU",5,1,20],["12RV",5,21,63]]
FULL={"2":"522bbc07c36b5f95f1d8fd427368d233cb3b336a278ad85a418021e0fce38890","3":"9e15a3a0707adda7cd5b319b21d24f7e1df38b64dc35c48034cb92800e1eb769","4":"b1866e1fe3cf4c3b73f87d88699d1dae31e6e1ea65aa7c545072d15c0006c8e1","5":"d66546a59822762c76936edd93d5fd11db907ffdf9dd247b69be50066592c950"}
PAGES=[119,72,121,56,63]
def read(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def chain(hashes): return hashlib.sha256("".join(hashes).encode("ascii")).hexdigest()
def fail(name): raise ValueError("12RW_"+name)
def verify(record_path=RECORD,replacement_sources=None,ql_path=None):
    d=read(record_path)
    if (d.get("batch"),d.get("parent_open_batch"),d.get("stage"))!=("12RW","12QE","12QE_OPEN") or d.get("status")!="F1_F5_REPLAYED_SOURCE_PAGE_IDENTITY_UNION_BOUNDED_NATIVE_FIRSTPASS_NOT_FULLTEXT": fail("SCOPE")
    if d["source"]["holding"]!="NLC411999003250_ONE_HOLDING" or d["source"]["reference_capture"]!="docs/research/MING-DATONG-YEHUOBIAN-12QL-NLC411999003250-TEN-FASCICLE-BINARY-CAPTURE-RECONCILIATION-R1.json": fail("HOLDING")
    ql=read(ql_path or ROOT/d["source"]["reference_capture"])
    if len(d["source"]["fascicles"])!=5: fail("FASCICLE_COUNT")
    for n,(s,total) in enumerate(zip(d["source"]["fascicles"],PAGES),1):
        old=next((x for x in ql["sources"] if x["fascicle"]==n),None)
        if not old or (s["fascicle"],s["source_pages"],s["first_reviewed_page"],s["native_bounded_review_pages"])!=(n,total,3 if n==1 else 1,total-(2 if n==1 else 0)): fail("SOURCE_PAGE_SCOPE")
        if s["source_pdf_sha256"]!=old["source_pdf_sha256"] or s["artifact_id"]!=old["artifact_id"] or old["source_pdf_pages"]!=total or old["source_page_images"]!=total or s["source_image_chain"]!=FULL.get(str(n)): fail("SOURCE_CAPTURE_IDENTITY")
    if len(d["windows"])!=len(LAYOUT): fail("WINDOW_COUNT")
    seen={}; by_fascicle={}; replacements=replacement_sources or {}
    for w,expected in zip(d["windows"],LAYOUT):
        if [w[k] for k in ("batch","fascicle","first","last")]!=expected: fail("WINDOW_LAYOUT")
        batch,n,a,b=expected
        if (not w["path"].startswith("docs/research/MING-DATONG-YEHUOBIAN-"+batch+"-NLC411999003250-") or not w["path"].endswith("-R1.json") or ".." in w["path"]): fail("WINDOW_PATH")
        old=read(replacements.get(batch,ROOT/w["path"]))
        if old.get("batch")!=batch or old.get("stage")!="12QE_OPEN": fail("UPSTREAM_STAGE")
        v=old["review"]; hashes=v[w["hash_field"]]
        if len(hashes)!=b-a+1 or any(not isinstance(h,str) or not re.fullmatch("[0-9a-f]{64}",h) for h in hashes): fail("PAGE_HASHES")
        if chain(hashes)!=w["chain"] or chain(hashes)!=v[w["chain_field"]]: fail("HASH_CHAIN")
        st=next((v[k] for k in ("pdf_page_first","first_pdf_page","window_pdf_page_first","first_page","pdf_first") if k in v),None)
        en=next((v[k] for k in ("pdf_page_last","last_pdf_page","window_pdf_page_last","last_page","pdf_last") if k in v),None)
        if (st,en)!=(a,b): fail("ORIGINAL_PAGE_RANGE")
        for page,h in enumerate(hashes,a):
            key=(n,page)
            if key in seen: fail("DUPLICATE_PAGE")
            seen[key]=h
        by_fascicle.setdefault(n,[]).extend(hashes)
    for n,total in enumerate(PAGES,1):
        if [p for f,p in sorted(seen) if f==n]!=list(range(3 if n==1 else 1,total+1)): fail("CONTIGUITY")
        if str(n) in FULL and chain(by_fascicle[n])!=FULL[str(n)]: fail("FULL_FASCICLE_HASH")
    if d["accounting"]!={"first_five_source_images":431,"first_five_unique_native_body_pages":429,"f1_preliminary_source_pages_not_native_target_reviewed":2,"source_images_f6_f10_outside_this_union":599,"whole_source_images":1030,"whole_body_pages":1027,"fulltext_body_pages_still_pending":1027,"global_1030_native_source_union_computed":False,"prior_339_native_689_preview_global_totals_not_replaced":True}: fail("COUNT_FIREWALL")
    if d["scope_guards"]!={"one_holding":True,"review_not_fulltext":True,"no_target_absence_proof":True,"no_new_target_glyph":True,"no_independent_witness":True,"no_algorithm_reopen":True}: fail("EVIDENCE_FIREWALL")
    if d["transmission_impact"]["edges_supported"] or d["transmission_impact"]["edges_revised"] or d["invariants"]!={"matrix_rows":222,"matrix_audited":222,"repairs":45,"sources":"647+7=654","md_g03":"OPEN","missing_candidate":"HPA-DAYUN-CAL-002","product":"CLOSED","algorithm_reopens":0}: fail("PRODUCT_OR_LINEAGE")
    return {"batch":"12RW","native_source_identity_pages_f1_f5":len(seen),"source_pages_f1_f5":431,"outside_f1_f5":599,"fulltext_body_pending":1027,"whole_1030_page_union_claimed":False}
if __name__=="__main__": print(json.dumps(verify(),ensure_ascii=False,indent=2))
