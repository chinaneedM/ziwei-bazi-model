#!/usr/bin/env python3
"""13CZ: source-image evidence and forward-only handoff; optional full PDF pixel replay."""
import argparse
import hashlib
import io
import json
from decimal import Decimal
from pathlib import Path

R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13CZ-NLC416-1909-GORYEOSA-V52-NATIVE-D15-D17-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"

def load(p):
    return json.loads((R/p).read_text(encoding="utf-8"))

def check(e,s,l):
    assert e["schema"]=="TIANWEN-13CZ-NLC416-1909-GORYEOSA-V52-NATIVE-D15-D17-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    p=e["provenance"]
    assert (p["workflow_run"],p["artifact_id"],p["bytes"],p["pages"])==(39795608954,12433047576,38410680,755)
    assert p["sha256"]=="b4bd5c557c7ba44bac1fc881e6c2e8784c9d56a8d2629f17b5255a1ec6bd9e97"
    assert p["ocr_used"] is False and p["firstparty_nlc_item_binding"]=="UNBOUND"
    t=e["page_binding"]
    assert (t["volume_start_pdf"],t["section_pdf"],t["numeric_pdf"])==(134,142,143)
    assert t["volume_literal"]=="志卷第六 / 高麗史五十二"
    assert (t["section"],t["field"],t["numeric_printed_page"])==("授時曆立成","日差加一秒八十六少","百三十六")
    assert t["image_dimensions"]==[1486,2162]
    assert t["p142_rgb_sha256"]=="08825e0c24812cd6c378a0176419987a76e0f9195e7d1b78b2ecdd944346fc06"
    assert t["p143_rgb_sha256"]=="30fd1c9c1601d871d1739a8691e90183960ca19ce3e2f225fd1573ddb8e110b4"
    target=[
        (15,"五分二一七六","5.2176",[570,1090,755,1680],"577416d8461852fe589bec4f1360560e2401685673531515ea8b872efc924dfc"),
        (16,"五分一三六二","5.1362",[388,1090,572,1680],"2c8c72e3a269daa2cb0db28318ca2c11ad3c54fb2577f124bc9cb1f2672fbe32"),
        (17,"五分二五四八","5.2548",[205,1090,388,1680],"18c86303431e46a98cd44125869c92beab6b8fef7186c83fdcf1da5b8d6c469e"),
    ]
    got=[(a["day"],a["literal"],a["value"],a["bbox"],a["rgb_sha256"]) for a in e["native_original_rois"]]
    assert got==target
    for x in e["native_original_rois"]:
        a,b,c,d=x["bbox"]
        assert 0<=a<c<=1486 and 0<=b<d<=2162
    v=[Decimal(x["value"]) for x in e["native_original_rois"]]
    n=e["numerical_scope"]
    assert v[1]-v[0]==Decimal(n["d15_to_d16"])
    assert v[2]-v[1]==Decimal(n["d16_to_d17"])
    assert (v[0]+v[2])/2==Decimal(n["derived_d16_conjecture"])
    assert (v[0]+v[2])/2-v[1]==Decimal(n["difference"])==Decimal("0.1000")
    assert n["observed_d16"]=="5.1362" and n["emend_original_text"] is False
    h=e["lineage"]
    assert h["later_print_direct_text_witness"] is True
    assert h["independent_early_physical_witnesses_added"]==h["graph_nodes_added"]==h["graph_edges_added"]==0
    assert h["algorithm_reopen_authorized"] is False
    assert not e["transmission_impact"]["edges_supported"]
    assert not e["transmission_impact"]["nodes_added_or_strengthened"]
    z=e["snapshot"]
    assert (z["matrix_rows"],z["audited_rows"],z["registered_sources"],z["graph_nodes"],z["graph_edges"],z["unresolved_risks"],z["deterministic_chart"],z["algorithm_reopens"])==(222,222,754,252,238,11,"CLOSED",0)
    assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
    assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(x.startswith("13CZ ") for x in s["historical_audit"]["current_focus"])
    i=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
    assert i["status"]=="OPEN" and E in i["source_refs"]
    assert any(x.get("revision_id")=="TW-OPEN-0005-13CZ-NLC416-D15-D17-NATIVE" for x in i["history"])
    assert any(x.get("id")=="OMISSIONS-13CZ-NLC416-D15-D17-20261022" for x in l["checkpoint_log"])
    assert sum(x["status"] in ("OPEN","BLOCKED_SOURCE_ACCESS") for x in l["issues"])==11
    assert s["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED"
    return True

def replay_pdf(e,p):
    import fitz
    from PIL import Image
    raw=Path(p).read_bytes()
    assert len(raw)==e["provenance"]["bytes"]
    assert hashlib.sha256(raw).hexdigest()==e["provenance"]["sha256"]
    d=fitz.open(stream=raw,filetype="pdf")
    assert len(d)==755
    images={}
    for n in (142,143):
        x=d[n-1].get_images(full=True)
        assert len(x)==1
        rawim=d.extract_image(x[0][0])["image"]
        im=Image.open(io.BytesIO(rawim)).convert("RGB")
        assert im.size==(1486,2162)
        assert hashlib.sha256(im.tobytes()).hexdigest()==e["page_binding"][f"p{n}_rgb_sha256"]
        images[n]=im
    for item in e["native_original_rois"]:
        crop=images[143].crop(tuple(item["bbox"]))
        assert hashlib.sha256(crop.tobytes()).hexdigest()==item["rgb_sha256"]
    return True

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--original-pdf")
    args=parser.parse_args()
    e,s,l=load(E),load(S),load(L)
    check(e,s,l)
    if args.original_pdf:replay_pdf(e,args.original_pdf)
    print("TIANWEN_13CZ_NLC416_ORIGINAL_D15_D17=PASS")
