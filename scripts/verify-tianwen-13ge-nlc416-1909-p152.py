#!/usr/bin/env python3
"""13GE later 1909 original print p152 D29-31, preserved earlier NLC 03130 D30 null."""
import argparse,hashlib,io,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GE-NLC416-1909-P152-D29-D31-DIRECT-FOURFEN-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
FY=ROOT/"docs/research/TIANWEN-13FY-NLC-P76-D29-D31-FOURFEN-SOURCE-NATIVE-COLLATION-R1.json"
FX=ROOT/"docs/research/TIANWEN-13FX-GK3467-P17-THREE-DAY-FOURFEN-SOURCE-FIELD-ERRATUM-R1.json"
DD=ROOT/"docs/research/TIANWEN-13DD-NLC416-1909-SUMMER-D28-NATIVE-ORIGINAL-GLYPH-R1.json"
CROP=ROOT/"docs/research/images/TIANWEN-13GE-NLC416-1909-D30-FOURFEN-NATIVE.png"
EXPECTED=[{"day":29,"source_heading":"二十九日","source_field":"四分","digits":"九〇六〇","integer_grid":49060,"heading_roi_xyxy":[1218,1055,1277,1252],"heading_rgb_sha256":"5b24c469bd798a4e61b90eea46b76ec1468be73efcb5620b39b01783e521b350","heading_png_sha256":"83cab543090a34838e31a1c7222fb71f91b10ddd45e2d396cb25a751011e196a","roi_xyxy":[1225,1285,1268,1555],"roi_rgb_sha256":"44cc266083535ca928b5dc0e05725767c9d824cba7e3e5d5f08bbeb5332a4fe0","roi_png_sha256":"f676bb56c7ebefeba35b6c2244d6e8f46be86d9943d4fd18bf9bff0b2fd6555d"},{"day":30,"source_heading":"三十日","source_field":"四分","digits":"九二二二","integer_grid":49222,"heading_roi_xyxy":[1039,1055,1100,1252],"heading_rgb_sha256":"1aa48673c4efde4836621faec90826f8cfb03c1f29709b02cca4c1a1992559bd","heading_png_sha256":"4867e2f6709126b7b1b562a1e9783103f4e473f75a26f1d11f21d815fed0db8c","roi_xyxy":[1050,1285,1095,1555],"roi_rgb_sha256":"57113a72fabe56dfb26655162c1f4a6a659c996290ea06502c8794a8d45991b2","roi_png_sha256":"ed6a83ef65a8693f9b103ce8aeff03dd258f94b9739d447dfe81c5983ee6e173"},{"day":31,"source_heading":"三十一日","source_field":"四分","digits":"九三八四","integer_grid":49384,"heading_roi_xyxy":[863,1055,922,1252],"heading_rgb_sha256":"3bc3d4924ee937736f14b2e4eb046fa5d5255f447014cf9ab43f9d18c53a35b6","heading_png_sha256":"752d583236a2e0d54fce7e7cef5ecdb097fe21cc751a856b6b41d0be788feea5","roi_xyxy":[873,1285,919,1555],"roi_rgb_sha256":"6f527a13458ac90a059402b9abe94157572ee0cae280271ff5dc351be776983c","roi_png_sha256":"c842fe243eaa529bd5e4421ee91cba8db174fa40302fc24bd1672808cecab482"}]
CN={s:i for i,s in enumerate("〇一二三四五六七八九")}
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def check(e,s,l,fy,fx,dd,source_pdf=None):
 assert e["schema"]=="TIANWEN-13GE-NLC416-1909-P152-D29-D31-DIRECT-FOURFEN-R1" and e["issue_id"]=="TW-OPEN-0005"
 z=e["source"];assert z["pdf_page_one_based"]==152 and z["original_pdf_embedded_image_xref"]==760
 assert z["source_pdf_sha256"]==dd["acquisition"]["source_sha256"] and z["original_image_native_rgb_sha256"]==dd["page_binding"]["source_page_152_native_rgb_sha256"]
 assert z["original_image_native_wh"]==[1486,2162] and z["new_independent_early_ancient_witnesses"]==0 and z["firstparty_item_identity"] is None
 assert e["source_original_rows"]==EXPECTED
 vals=[]
 for row in EXPECTED:
  assert row["source_field"]=="四分" and row["integer_grid"]==40000+sum(CN[ch]*10**(3-i) for i,ch in enumerate(row["digits"]))
  vals.append(row["integer_grid"])
 assert vals==[49060,49222,49384]
 assert e["arithmetic"]["original_integer_grid"]==vals
 assert [b-a for a,b in zip(vals,vals[1:])]==e["arithmetic"]["integer_grid_steps"]==[162,162]
 assert e["arithmetic"]["unit_bridge_certified"] is False
 assert [row["digits"] for row in fx["original_fourfen_rows"]]==[row["digits"] for row in EXPECTED]
 assert [row["digits"] for row in fy["direct_original_fields"]]==[EXPECTED[0]["digits"],EXPECTED[2]["digits"]]
 assert fy["day30"]["original_complete_fourfen_digits"] is None and fy["day30"]["printed_fourfen_field_exact_roi"] is None
 c=e["source_scoped_comparison"]
 assert c["NLC_03130_original_day30"] is None and c["NLC_03130_original_day30_roi"] is None and c["copy_independence"] is None and c["source_unit_equivalence"] is None
 assert c["late_print_concordance_does_not_fill_NLC_original"] is True
 u=e["unresolved"]
 for k in ("NLC_03130_original_d9","NLC_03130_original_d14","NLC_03130_original_d30","source_winner","ancient_fourfen_chudu_unit_bridge"):assert u[k] is None
 assert u["G893_original_six_controls"]=="OPEN" and u["legacy_13EI"]=="RETRACTED"
 assert e["transmission_impact"]["edges_supported"]==[] and e["transmission_impact"]["nodes_added_or_strengthened"]==[]
 counts=e["counts"]
 assert [counts[k] for k in ("matrix_rows","matrix_audited","sources","graph_nodes","graph_edges","risk_issues_open_or_blocked")]==[222,222,761,252,238,11]
 assert counts["product"]=="CLOSED"
 for k in ("algorithm_reopens","candidate_collapses","new_source_registry_entries","new_ancient_physical_witnesses","new_genealogy_nodes","new_genealogy_edges"):assert counts[k]==0
 cp=e["binary_positive"];assert cp["path"]==str(CROP.relative_to(ROOT)) and cp["png_sha256"]==EXPECTED[1]["roi_png_sha256"]
 assert hashlib.sha256(CROP.read_bytes()).hexdigest()==cp["png_sha256"]
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(f.startswith("13GE ") for f in s["historical_audit"]["current_focus"])
 issue=next(x for x in l["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["next_action"].startswith(l["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 for p in (str(E.relative_to(ROOT)),str(E.relative_to(ROOT)).replace(".json",".md"),str(CROP.relative_to(ROOT))):assert p in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13GE-1909-P152-D29-D31-20261025" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13GE-1909-P152-D29-D31-20261025" for x in l["checkpoint_log"])
 if source_pdf:
  from PIL import Image
  import fitz
  pdf=Path(source_pdf).read_bytes();assert hashlib.sha256(pdf).hexdigest()==z["source_pdf_sha256"]
  doc=fitz.open(stream=pdf,filetype="pdf");assert len(doc)==z["pdf_total_pages"]
  images=doc[z["pdf_page_one_based"]-1].get_images(full=True)
  assert len(images)==1 and images[0][0]==z["original_pdf_embedded_image_xref"]
  obj=doc.extract_image(images[0][0]);im=Image.open(io.BytesIO(obj["image"])).convert("RGB")
  assert list(im.size)==z["original_image_native_wh"] and hashlib.sha256(im.tobytes()).hexdigest()==z["original_image_native_rgb_sha256"]
  for r in EXPECTED:
   for pr in ("heading_",""):
    crop=im.crop(tuple(r[pr+"roi_xyxy"]))
    assert hashlib.sha256(crop.tobytes()).hexdigest()==r[pr+"rgb_sha256"]
    buf=io.BytesIO();crop.save(buf,format="PNG")
    assert hashlib.sha256(buf.getvalue()).hexdigest()==r[pr+"png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-pdf");a=ap.parse_args()
 assert check(read(E),read(S),read(L),read(FY),read(FX),read(DD),a.source_pdf)
 print("13GE_PASS_NATIVE_1909_PRINT_D29_D30_D31_NLC_03130_D30_NULL")
