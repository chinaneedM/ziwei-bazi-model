#!/usr/bin/env python3
"""12YT Mei native original printed numeral reproducibility and source boundary."""
from pathlib import Path
from decimal import Decimal
import json
ROOT=Path(__file__).resolve().parents[1]
DOC="docs/research/TIANWEN-12YT-MEI-CADAL06054965-ORIGINAL-NUMERIC-THREE-LOCI-R1.json"
def load():
 return tuple(json.loads((ROOT/p).read_text(encoding="utf-8")) for p in (DOC,"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json","docs/PROJECT-CURRENT-STATE-R1.json"))
def check(p,msg):
 if not p:raise ValueError(msg)
def verify(doc,ledger,state):
 s=doc["source"];a,b,c=doc["verified_original"];scope=doc["boundary"]
 check(doc["schema"]=="TIANWEN-12YT-DIRECT-MEI-CADAL06054965-THREE-ORIGINAL-LOCI-R1","scope")
 check(s["bytes"]==4259929 and s["pages"]==126 and s["sha256"]=="195c3ff35ae297b43fad6bb597d46dd046b109bee4c8eae8732fba336adab800" and s["sha1"]=="7cf69e5d86e6adc061c778c22ea7451d164f264a","actual DjVu source")
 check(s["source_impression_year"]=="UNVERIFIED" and s["IA_link_same_bytes"]=="UNPROVEN" and s["CText_251951_same_physical_copy"]=="UNPROVEN" and s["no_ocr"] is True,"false print year or copy")
 check((a["page"],b["page"],c["page"])==(26,26,76) and (a["printed"],b["printed"],c["printed"])==("一秒八十六微","四分九十三秒八十六微","○一八六"),"source-printed glyph")
 check((a["field"],b["field"],c["field"])==("加分立差","平立合差","每日之差"),"column role")
 check(a["original_png_sha"]==b["original_png_sha"]=="8cc3c7c89acff565f540fbb8171fa9c64e3f96468a3d1cf92ffbca41f27185d0" and c["original_png_sha"]=="1f64352a84b5ac9a5db7c883f025835192c71fdee7ef323f9c3e42d2c2280ef6","native source pixel scope")
 check((a["bounds"],b["bounds"],c["bounds"])==([790,250,1340,2860],[280,850,1360,2900],[285,290,905,2850]),"original text ROI")
 check((a["crop_rgb_sha"],b["crop_rgb_sha"],c["crop_rgb_sha"])==("d38e3ea7a6116efeb5c889af1c7407b4e543bea7518d402fccde087f52a1ae8a","9b56c3c49839f9f4d0030299b5dcbd3edc898b454dd10168378861e306e72d1d","b576341a0e57f4842c88190aaf01f968a2c3d392f72711ee583cc7072d0bc740"),"crop source-pixel hash")
 check((a["crop_png_sha"],b["crop_png_sha"],c["crop_png_sha"])==("f105a762ef69b42e00b1a1262381b5870545183c44508c667359a31b29e049be","44a46519f5e05a614a0104036b6522e734408241afa10b3505a29d7181a70436","be5a84e789b9ca3a436561371a5f5b2c8faade3d1b09be27b659be373c09d1e7"),"lossless crop hashes")
 check(Decimal("0.0031")*6==Decimal(a["number"]) and 2*Decimal("2.4600")+Decimal(a["number"])==Decimal(b["number"]) and (Decimal("6.5568")-Decimal(b["number"]))/87==Decimal(c["number"]),"historical digit arithmetic")
 check(scope["digitized_items"]==1 and scope["direct_print_glyph_positions"]==3 and scope["distinct_ancient_physical_witnesses_proven"]==0 and scope["common_ancestry_proven"] is False,"source count / genealogy")
 check(scope["original_edition_date_proven"] is False and scope["same_original_page_ROI_overlaps_intentional"] is True and scope["prior_12YS_IA_404_not_retracted"] is True,"antiquarian edition and 404 safeguards")
 check(scope["source_registry_new_entries"]==scope["graph_new_nodes"]==scope["graph_new_edges"]==scope["chart_algorithm_reopens"]==0 and scope["G893_original_principal"]=="5/6" and scope["G893_cross_witness_final"]=="0/6" and scope["research_open_count"]==11 and scope["product"]=="CLOSED","unsupported product/source upgrade")
 issues=ledger["issues"];i=next(x for x in issues if x["id"]=="TW-OPEN-0005")
 check(i["status"]=="OPEN" and DOC in i["source_refs"] and DOC.replace(".json",".md") in i["source_refs"] and i["mei_12yt_verified_cadal06054965_original"][0]["original_printed_glyphs"]==3,"omission ledger original evidence")
 check(state["schema_version"]==ledger["binding"]["reviewed_state_version"]==state["historical_audit"]["research_omission_guard"]["reviewed_state_version"] and tuple(map(int,state["schema_version"].split(".")))>=(1,632,0),"state synchronization")
 check(ledger["checkpoint_log"][-1]["state_version"]==state["schema_version"] and len(ledger["checkpoint_log"][-1]["reviewed_issue_ids"])==len(issues) and any(x.startswith("12YT ") for x in state["historical_audit"]["current_focus"]),"historic context persistence")
 check(state["invariants"]["deterministic_fusion_chart_product_r1"]=="CLOSED" and state["invariants"]["algorithm_reopen_count"]==0,"chart closed")
 return {"status":"PASS","source_scanned_pages":126,"direct_original_Mei_glyphs":3,"original_print_item":1,"G893_final":"0/6","open_issues":len(issues)}
if __name__=="__main__":print(json.dumps(verify(*load()),ensure_ascii=False))
