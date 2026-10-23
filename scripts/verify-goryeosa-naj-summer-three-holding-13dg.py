#!/usr/bin/env python3
"""13DG: NAJ original summer 3-row value with bounded triple-holding consistency and no fake stemmatic vote."""
import argparse,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
E="docs/research/TIANWEN-13DG-NAJ-ORIGINAL-SUMMER-XINGDU-THREE-HOLDING-R1.json"
W="docs/research/TIANWEN-13DE-WASEDA-SUMMER-XINGDU-D28-D30-THREE-ROW-ORIGINAL-R1.json"
P="docs/research/TIANWEN-13DD-NLC416-1909-SUMMER-D28-NATIVE-ORIGINAL-GLYPH-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def check(e,w,p,s,l):
 assert e["schema"]=="TIANWEN-13DG-NAJ-SUMMER-ORIGINAL-CROSSHOLDING-DAY-OFFSET-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["preceding_waseda"]==W and e["preceding_1909"]==P
 h=e["naj_physical_witness"]
 assert (h["archived_prior_action"],h["archived_prior_artifact"],h["photo_ordinal"],h["source_jpeg_size"])==(39410644745,12258588506,27,1021783)
 assert h["manifest_sha256"]=="3f38f52860bd06ca7f4b89cec65a32b8529fcb547ac098548120e8071fe370a1"
 assert h["source_jpeg_sha256"]=="3a1cdf95c11d29e06041de00b8cc56e158775cdfc058ecce46fe5f796a5e606b"
 assert h["source_rgb_sha256"]=="333a05cd333353607b8ed082bc4c70b0ea07dcd2d5e83ad63ba9e0d4641a8d62"
 assert h["dimensions"]==[3000,2215] and h["is_new_independent_stemmatic_vote"] is False
 assert h["archived_zip_sha256"]=="320b0e09c00c7e1005b33756b05cf78f381b77c7ec0ef2fb76821c60e4bad8b6"
 x=h["current_live_reacquisition"]
 assert (x["run_id"],x["http_status"],x["ordinal_attempted"])==(39876177996,403,19)
 assert x["recovered_via_existing_hash_bound_13ba_artifact"] and x["not_an_original_glyph_negative"]
 expected=[
 (28,"二十八日",[1930,520,2020,745],"c826680e59984f4fb8e68bf59cf5639ea3b7308aab636706a304145cf5426d8d","初度九十六四〇六二","0.964062",[2011,951,2054,1720],"835e6809bfd884683a4d6ff4a78cbab441c01d3e71052caea044b37cd9e9a3c5"),
 (29,"二十九日",[1755,520,1850,745],"71603661cb3077be2afbd245ec6c930953676bbd0d018b5685ede37b0c5bff72","初度九十九四五四九","0.994549",[1839,951,1881,1720],"dcec0e200dcbbf64bee3e6c531343b7290fe4ae411a3cdad57266c45b81bd6be"),
 (30,"三十日",[1580,520,1675,745],"228cf760abf29df29104b10ccdcac3971da0cc4af4bc91e62aad4a6d901edee7","初度九十六五〇三八","0.965038",[1691,951,1733,1720],"eeda3d2141a842541473dda4bc4245d84d9be36651e104de47a24fdc68400aa4")]
 got=[(q["printed_day"],q["heading"],q["heading_bbox"],q["heading_rgb_sha256"],q["glyph"],q["value"],q["bbox"],q["roi_sha256"]) for q in e["naj_direct_rows"]]
 assert got==expected
 for q in e["naj_direct_rows"]:
  for k in ("heading_bbox","bbox"):
   a,b,c,d=q[k];assert 0<=a<c<=3000 and 0<=b<d<=2215
 comp=e["three_holding_comparison"]
 assert comp["registered_distinct_holdings"]==3 and comp["established_stemmatically_independent_votes_added"]==0
 assert comp["same_three_values"]==["0.964062","0.994549","0.965038"]
 assert comp["waseda_source_printed_days"]==comp["naj_source_printed_days"]==[28,29,30]
 assert comp["later_1909_source_printed_days"]==[27,28,29]
 assert [z["xingdu_value"] for z in w["source_native_loci"]]==[z["value"] for z in e["naj_direct_rows"]]
 assert comp["same_glyph_across_all_three_loci"]==w["source_native_loci"][1]["xingdu_literal"]==p["adjudication"]["original_1909_XINGDU_D28"]=="初度九十九四五四九"
 assert comp["matched_glyph_day_NAJ"]==comp["matched_glyph_day_WASEDA"]==29 and comp["matched_glyph_day_1909"]==28
 assert comp["candidate_0_964549_attested_as_original_in_any_of_these_loci"] is False
 assert comp["direct_early_archetype_emendation"]=="NOT_AUTHORIZED"
 imp=e["impact"]
 assert (imp["matrix_rows"],imp["matrix_audited"],imp["registry_sources"],imp["genealogy_nodes"],imp["genealogy_edges"],imp["open_or_blocked_issues"])==(222,222,754,252,238,11)
 assert all(imp[x]==0 for x in ("new_registry_sources","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"))
 assert imp["deterministic_product"]=="CLOSED"
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert l["binding"]["latest_research_focus_prefix"]==s["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(z.startswith("13DG ") for z in s["historical_audit"]["current_focus"])
 i=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert i["status"]=="OPEN" and E in i["source_refs"]
 assert any(z.get("revision_id")=="TW-OPEN-0005-13DG-NAJ-THREE-HOLDING" for z in i["history"])
 assert any(z.get("id")=="OMISSIONS-13DG-NAJ-THREE-HOLDING-20261023" for z in l["checkpoint_log"])
 return True
def replay(e,p):
 from PIL import Image
 raw=Path(p).read_bytes()
 assert len(raw)==e["naj_physical_witness"]["source_jpeg_size"]
 assert hashlib.sha256(raw).hexdigest()==e["naj_physical_witness"]["source_jpeg_sha256"]
 im=Image.open(p).convert("RGB")
 assert list(im.size)==[3000,2215]
 assert hashlib.sha256(im.tobytes()).hexdigest()==e["naj_physical_witness"]["source_rgb_sha256"]
 for z in e["naj_direct_rows"]:
  for bb,digest in (("heading_bbox","heading_rgb_sha256"),("bbox","roi_sha256")):
   assert hashlib.sha256(im.crop(z[bb]).tobytes()).hexdigest()==z[digest]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--naj-photo27");opts=ap.parse_args()
 e=load(E);assert check(e,load(W),load(P),load(S),load(L))
 if opts.naj_photo27:assert replay(e,opts.naj_photo27)
 print("TIANWEN_13DG_NAJ_THREE_HOLDING_ORIGINAL_GLYPH=PASS")
