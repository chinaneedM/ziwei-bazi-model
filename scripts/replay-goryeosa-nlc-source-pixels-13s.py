#!/usr/bin/env python3
"""13S: native PDF raster SHA and reproducible RGB crop. No OCR or historical edition decisions."""
import argparse,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13S-NLC-GORYEOSA-V52-ORIGINAL-PIXEL-REPLAY-AND-BIBLIOGRAPHIC-QUARANTINE-R1.json"
def read(p=E):
    return json.loads((ROOT/p).read_text(encoding="utf-8"))
def h(x):return hashlib.sha256(x).hexdigest()
def static_check(e):
    assert e["schema"]=="TIANWEN-13S-NLC-GORYEOSA-V52-NATIVE-SOURCE-PIXEL-REPLAY-R1"
    assert e["issue_id"]=="TW-OPEN-0005"
    assert e["expected_pdf_bytes"]==19799436 and e["expected_pdf_pages"]==64
    assert e["expected_pdf_sha256"]=="2b9e51cc5f44a4d92d3cb4a63318605f78cc8ffb118853036655b65ed279a689"
    assert len(e["page_replay"])==3 and [r["pdf_page_1based"] for r in e["page_replay"]]==[2,16,17]
    assert [r["xref"] for r in e["page_replay"]]==[13,111,118]
    assert [r["rgb_crop_encoded_png_sha256"] for r in e["page_replay"]]==[
      "a765c220d7e14f61c19ac3c684eed64287fe23bc447cd9fbb6b7e9637000ea60",
      "f3d52e8790db60958fce54b2b7459bdf6cfe3046d448120bc228b5751fac6066",
      "640ce449af4967bacc2e684a44b9269208d3b3056cfcc9b5a2fa18e1cfccc5bd"]
    assert [r["rgb_pixels_sha256"] for r in e["page_replay"]]==[
      "4f8a28e94e1a1591949066e9e40486b5d4a70d5a367dd7e531e6555c94325082",
      "4d9cdaf5d680ebfb534b29cf4fd40bb77fa4d5562ab8b72439310bc714bb19b5",
      "de35ba44e09dd083fc1fcef17aa9e224503e8c3e7412e933e4e112c3239b528e"]
    assert e["serialization_contract"]["normalized_pixel_mode"]=="RGB"
    assert e["serialization_contract"]["reference_stack"]=="PyMuPDF 1.26.7 / Pillow 12.3.0"
    assert e["upload_bibliography_secondary"]["catalog_candidate_value"]=="13494"
    assert e["upload_bibliography_secondary"]["catalog_candidate_status"]=="UNVERIFIED_FIRST_PARTY_ITEM_BINDING"
    assert e["upload_bibliography_secondary"]["identical_to_cadal02050311"] is None
    assert all(e["adjudication"][k]==0 for k in ("new_original_glyphs_decided","new_physical_originals_established","independent_numeric_votes_added","external_source_registry_entries_added","transmission_edges_added","algorithm_reopens"))
    assert e["adjudication"]["open_research_issues"]==11 and e["adjudication"]["product_r1"]=="CLOSED"
    old=read(e["previous_evidence"])
    assert [p["embedded_raster_sha256"] for p in old["native_page_records"]]==[p["expected_encoded_png_sha256"] for p in e["page_replay"]]
    assert [p["source_crop_xyxy"] for p in old["native_page_records"]]==[p["crop_box_xyxy"] for p in e["page_replay"]]
    assert [p["source_crop_png_sha256"] for p in old["native_page_records"]]==[p["rgb_crop_encoded_png_sha256"] for p in e["page_replay"]]
    state=read("docs/PROJECT-CURRENT-STATE-R1.json")
    ledger=read("docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json")
    assert tuple(map(int,state["schema_version"].split(".")))>=(1,678,0)
    assert state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
    assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
    assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
    assert any(s.startswith("13S ") for s in state["historical_audit"]["current_focus"])
    issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
    assert issue["status"]=="OPEN" and E in issue["source_refs"] and E[:-5]+".md" in issue["source_refs"]
    assert len(ledger["issues"])==11 and ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"]
    assert {x["id"] for x in ledger["issues"]}==set(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])
    return True
def rgb_crop_bytes(original_png,box):
    from PIL import Image
    rgb=Image.open(io.BytesIO(original_png)).convert("RGB").crop(tuple(box))
    buff=io.BytesIO();rgb.save(buff,format="PNG")
    return rgb.tobytes(),buff.getvalue()
def verify_source(pdf,e):
    import fitz
    assert pdf.stat().st_size==e["expected_pdf_bytes"]
    assert h(pdf.read_bytes())==e["expected_pdf_sha256"]
    doc=fitz.open(str(pdf))
    try:
      assert doc.page_count==e["expected_pdf_pages"]
      observed=[]
      for rec in e["page_replay"]:
        n=rec["pdf_page_1based"];xref=rec["xref"]
        page=doc.load_page(n-1)
        assert any(x[0]==xref for x in page.get_images(full=True)),("xref missing",n,xref)
        img=doc.extract_image(xref)
        assert img["ext"]=="png" and h(img["image"])==rec["expected_encoded_png_sha256"]
        raw,encoded=rgb_crop_bytes(img["image"],rec["crop_box_xyxy"])
        assert h(raw)==rec["rgb_pixels_sha256"],("RGB pixel mismatch",n)
        assert h(encoded)==rec["rgb_crop_encoded_png_sha256"],("RGB PNG encoding differs from recorded Pillow reference",n)
        observed.append({"page":n,"source_png_sha256":h(img["image"]),"rgb_pixel_sha256":h(raw),"rgb_png_sha256":h(encoded)})
      return observed
    finally:doc.close()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-pdf",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    e=read();static_check(e)
    if a.source_pdf is None:
      print(json.dumps({"status":"PASS_STATIC","pages_expected":len(e["page_replay"])}))
    else:
      result={"status":"PASS_FULL_SOURCE_REPLAY","pages":verify_source(a.source_pdf,e),"independent_ancient_witness_votes":0}
      if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
      print(json.dumps({"status":result["status"],"replayed":len(result["pages"]),"independent_ancient_witness_votes":0}))
if __name__=="__main__":main()
