#!/usr/bin/env python3
"""13GC same-original NLC p75 day17–20 bounded literal collation; preserve D30 NULL."""
import argparse, hashlib, io, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13GC-NLC-P75-D17-D20-ORIGINAL-FEN-LANES-R1.json"
FU=ROOT/"docs/research/TIANWEN-13FU-NLC-D16-DIRECT-FOURFEN-ORIGINAL-GLYPHS-R1.json"
GB=ROOT/"docs/research/TIANWEN-13GB-NLC-P75-D21-D25-CROSSPAGE-ORIGINAL-FEN-LANES-R1.json"
L=ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S=ROOT/"docs/PROJECT-CURRENT-STATE-R1.json"
EXPECTED=json.loads("[{\"day\":17,\"source_heading\":\"十七日\",\"prefix\":\"四\",\"remainder\":\"七一一六\",\"integer_grid\":47116,\"heading_roi_xyxy\":[730,160,797,302],\"heading_rgb_sha256\":\"35ad44d865f78e5dcf55de12452893fba0b964565897182a4ccda97ebd0879af\",\"heading_png_sha256\":\"fdcb3c5e64a7980ce93b16d0734edc003db182b9c0cd3ae22806a8c262d0cd50\",\"roi_xyxy\":[748,419,771,611],\"roi_rgb_sha256\":\"2cce73011235bdbc45f6352cf9372ac8de53af8fb80a91abdc152c68fdea9051\",\"roi_png_sha256\":\"bb12905ddea4590c92b6fec40f0db69604a8f7a54b4afe0c64721f4192c25b40\"},{\"day\":18,\"source_heading\":\"十八日\",\"prefix\":\"四\",\"remainder\":\"七二七八\",\"integer_grid\":47278,\"heading_roi_xyxy\":[641,160,713,302],\"heading_rgb_sha256\":\"77f8d4ca5a799f08fae9fcad0917cd67f85d4af5eaab12262150bb45a9add786\",\"heading_png_sha256\":\"69cf1179305424a2aab4d6f50e8cf91eee51fbafd0609ae81e9e714bd68a9926\",\"roi_xyxy\":[660,419,684,611],\"roi_rgb_sha256\":\"496207ee9e097a435bd2fa5bed9f9bc7139eb0441b7491ca4ec2f2beb3dee3cc\",\"roi_png_sha256\":\"3c0e77f1ffb7546dbd007589792c671afc29445d43b810833bc9798b01bff65f\"},{\"day\":19,\"source_heading\":\"十九日\",\"prefix\":\"四\",\"remainder\":\"七四四〇\",\"integer_grid\":47440,\"heading_roi_xyxy\":[552,160,624,302],\"heading_rgb_sha256\":\"7a03dd97964894ec498c9b97cd0be1b84bf5707566c2acfca64ad3aa391e6778\",\"heading_png_sha256\":\"7a4485be307be2f39ddb9d1b5841bb7dfdfe8ada4f94a00a001eda6c937157f0\",\"roi_xyxy\":[581,419,603,611],\"roi_rgb_sha256\":\"1a35a091701314636d170f923d359d788730781217850e3cfdcaab57ae6f237f\",\"roi_png_sha256\":\"ec193adf9e2a43627dab06352aa06ab5cd44f40a20044ec9830cd4256acfd257\"},{\"day\":20,\"source_heading\":\"二十日\",\"prefix\":\"四\",\"remainder\":\"七六〇二\",\"integer_grid\":47602,\"heading_roi_xyxy\":[475,160,545,302],\"heading_rgb_sha256\":\"09360a1843157957e03811f23c0bd7b609e6397157fb3656e3dba6b8d333dbb2\",\"heading_png_sha256\":\"d8c3ad3a41ce71b8c9d8a854e2972bb63bdc28714fae302617a3ae6fd7b2acbc\",\"roi_xyxy\":[514,419,537,611],\"roi_rgb_sha256\":\"38d14ec1e497c91a4c69c266aacd8f39cff1b428115d83f13f2c6755940db74b\",\"roi_png_sha256\":\"de8f2dc425d1ad705ef71a0a5d19bdc5a30684cadd815cb0d346b2476e0f3429\"}]")
DIGITS={c:i for i,c in enumerate("〇一二三四五六七八九")}
def read(p):return json.loads(p.read_text(encoding="utf-8"))
def check(e,fu,gb,ledger,state,source_image=None):
 assert e["schema"]=="TIANWEN-13GC-NLC-P75-D17-D20-ORIGINAL-FEN-LANES-R1" and e["issue_id"]=="TW-OPEN-0005"
 src=e["source"]
 assert src["png_sha256"]==fu["source"]["original_image_sha256"]==gb["source"]["png_sha256"]
 assert src["rgb_sha256"]==fu["source"]["native_rgb_sha256"]==gb["source"]["rgb_sha256"]
 assert src["native_wh"]==[1305,878] and src["artifact_id"]==12494518841 and src["pdf_page_one_based"]==75
 assert src["physical_copy_identity"] is None and src["impression_date"] is None and src["no_new_physical_witnesses"] is True
 assert e["direct_original_rows"]==EXPECTED
 vals=[]
 for row in EXPECTED:
  assert row["integer_grid"]==40000+sum(DIGITS[c]*10**(3-i) for i,c in enumerate(row["remainder"]))
  vals.append(row["integer_grid"])
 assert fu["original_field"]["complete_field_original_literal"]=="四分六九五四"
 assert gb["direct_original_rows"][0]["day"]==21 and gb["direct_original_rows"][0]["integer_grid"]==47764
 c=e["continuity"]
 assert c["day16_source"]==str(FU.relative_to(ROOT)) and c["day21_source"]==str(GB.relative_to(ROOT))
 assert c["observed_days"]==list(range(16,22))
 assert c["integer_grid"]==[46954]+vals+[47764]
 assert c["original_literal"]==["四分六九五四"]+["四分"+r["remainder"] for r in EXPECTED]+["四分七七六四"]
 assert [b-a for a,b in zip(c["integer_grid"],c["integer_grid"][1:])]==c["neighbor_differences"]==[162]*5
 assert c["same_digital_surrogate_only"] and not c["historic_unit_or_same_print_state_proven"] and c["not_extrapolatable_to_day30"]
 u=e["unresolved"]
 assert u["NLC_day30_exact_original"] is None and u["NLC_day30_original_field_roi"] is None
 assert u["NLC_day9_fourfen"] is None and u["G893_six_direct_original_controls"]=="OPEN" and u["historic_unit_equivalence"] is None
 assert u["copy_edition_independence"] is None and u["source_historical_winner"] is None and u["legacy_13EI"]=="RETRACTED"
 assert e["counts"]["matrix_rows"]==222 and e["counts"]["matrix_audited"]==222 and e["counts"]["sources"]==761
 assert e["counts"]["graph_nodes"]==252 and e["counts"]["graph_edges"]==238 and e["counts"]["risk_issues_open_or_blocked"]==11 and e["counts"]["product"]=="CLOSED"
 for key in ("algorithm_reopens","candidate_collapses","new_source_registry_entries","new_ancient_physical_witnesses","new_genealogy_nodes","new_genealogy_edges"):assert e["counts"][key]==0
 assert not e["transmission_impact"]["edges_supported"] and not e["transmission_impact"]["edges_revised"]
 assert ledger["binding"]["reviewed_state_version"]==state["schema_version"]
 assert ledger["binding"]["source_focus_count"]==len(state["historical_audit"]["current_focus"])
 assert ledger["binding"]["latest_research_focus_prefix"]==state["historical_audit"]["current_focus"][-1].split(" ",1)[0]
 assert any(x.startswith("13GC ") for x in state["historical_audit"]["current_focus"])
 issue=next(x for x in ledger["issues"] if x["id"]=="TW-OPEN-0005")
 assert issue["priority"]=="P0" and issue["status"]=="OPEN"
 assert issue["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")
 assert str(E.relative_to(ROOT)) in issue["source_refs"] and str(E.relative_to(ROOT)).replace(".json",".md") in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13GC-P75-D17-D20-20261025" for x in issue["history"])
 assert any(x.get("id")=="OMISSIONS-13GC-P75-D17-D20-20261025" for x in ledger["checkpoint_log"])
 if source_image:
  from PIL import Image
  data=Path(source_image).read_bytes()
  assert hashlib.sha256(data).hexdigest()==src["png_sha256"]
  im=Image.open(io.BytesIO(data)).convert("RGB")
  assert list(im.size)==src["native_wh"] and hashlib.sha256(im.tobytes()).hexdigest()==src["rgb_sha256"]
  for row in EXPECTED:
   for prefix in ("heading_",""):
    part=im.crop(tuple(row[prefix+"roi_xyxy"]))
    assert hashlib.sha256(part.tobytes()).hexdigest()==row[prefix+"roi_rgb_sha256"]
    buf=io.BytesIO();part.save(buf,format="PNG")
    assert hashlib.sha256(buf.getvalue()).hexdigest()==row[prefix+"roi_png_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--source-image");args=ap.parse_args()
 assert check(read(E),read(FU),read(GB),read(L),read(S),args.source_image)
 print("13GC_PASS_NLC_P75_D17_D20_DIRECT_ORIGINAL_D30_NULL")
