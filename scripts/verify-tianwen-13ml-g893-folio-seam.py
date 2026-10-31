#!/usr/bin/env python3
"""13ML: source-original G893 seam topology and 1569 independent print scope (no OCR)."""
import argparse,hashlib,json
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/"docs/research/TIANWEN-13ML-G893-ORIGINAL-FOLIO-SEAM-D9-D19-HEADER-GEOMETRY-R1.json"
def file_sha(b):return hashlib.sha256(b).hexdigest()
def verify(e,s,l):
 assert e["schema"]=="TIANWEN-13ML-G893-ORIGINAL-FOLIO-SEAM-D9-D19-HEADER-GEOMETRY-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and e["source_acquisition"]["no_ocr"]
 assert e["source_acquisition"]["artifact_run"]==41144025711
 assert e["source_acquisition"]["zip_sha256"]=="1d8f10da7c27411bf38ad635494a1b9f4e700fb76cb37b2a7541c075a0ca9835"
 rows=e["g893_original_images"]
 assert [x["page"] for x in rows]==["001a","002a","002b"]
 assert [x["sha256"] for x in rows]==["8b07513ca8aad42ae167a93f22c39f14850c8cd1c345db9ce98c1e0e769226a5","31d0452e9350e32ff73549f49d894ab26f6e588654926d45b3a603ae4da9a914","f9812e8c6a357eb6cd1117bb2af58d816e01030d5b93f34e7094bddb766b2b55"]
 assert [x["roi_rgb_sha256"] for x in rows]==["04471ba8b25ca5b114e0fc4f3817c968a2426db1d5cecad1f25091c86ad5735c","7bb283826af72ba381c6abc9bb5555d698439597dc5eaf7f5a1e10d7a2b7439d","d7b5b7fd7199d23ecd8c38479c4ead362e18929de8a7fe4d56bb5fbebdcc83df"]
 assert [x["source_day_headings_left_to_right"] for x in rows[1:]]==[[13,12,11,10,9],[19,18,17,16,15,14]]
 assert e["day_sequence"]["contiguous_source_day_numbers"]==list(range(9,20))
 assert e["day_sequence"]["left_page_last_day_at_left_edge"]+1==e["day_sequence"]["next_page_first_day_at_right_edge"]
 assert set(rows[0]["observed_source_labels"])=={"積日","日差","盈縮加分","盈縮積度"}
 assert rows[0]["observed_source_small_glyph"]=="加一秒八十六少"
 p=e["independent_original_print"]
 assert p["source_pdf_sha256"]=="4c006b7ce131902fe33012d42f62cd2bbc2140affa3d5886e0da02966352cb7c"
 assert p["source_page15_rgb_sha256"]=="7b35af0e1e802c9346c927a02c67d1681e01b5120c3cf891160126f2018478d5"
 assert p["p15_roi_rgb_sha256"]=="72f4069db6044ce0b77f85259303c830b4f1cd14407469f73ac37e6d00632e41"
 vals=[Decimal(r["decimal"]) for r in p["direct_source_values"]]
 assert [r["day"] for r in p["direct_source_values"]]==[15,16,17]
 assert vals[1]-vals[0]==vals[2]-vals[1]==Decimal(p["local_decimal_increment"])==Decimal("0.0186")
 c=e["comparison_gate"]
 assert c["G893_vs_zhouxiang_same_column_and_unit"]=="UNPROVEN" and c["G893_D16_source_numeric_field_mapping"]=="UNRESOLVED"
 assert c["historical_G893_six_cross_original_winners"]==0 and c["algorithm_reopens"]==0 and c["product"]=="CLOSED"
 assert all(c[k]==0 for k in ("source_registry_delta","matrix_delta","genealogy_nodes_delta","genealogy_edges_delta","newly_proved_algorithms","candidate_collapse"))
 assert s["schema_version"]==l["binding"]["reviewed_state_version"]
 assert tuple(map(int,s["schema_version"].split(".")))>=(1,974,0)
 focus=s["historical_audit"]["current_focus"]
 assert any(x.startswith("13ML ") for x in focus)
 assert len(focus)==l["binding"]["source_focus_count"]
 assert l["binding"]["latest_research_focus_prefix"]==focus[-1].split(" ",1)[0]
 issue=next(i for i in l["issues"] if i["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["next_action"]  # archive survives later evidence-scoped issue revisions
 assert "docs/research/TIANWEN-13ML-G893-ORIGINAL-FOLIO-SEAM-D9-D19-HEADER-GEOMETRY-R1.json" in issue["source_refs"]
 assert any(x.get("revision_id")=="TW-OPEN-0005-13ML-FOLIO-SEAM-20261031" for x in issue["history"])
 assert any(x.get("state_version")=="1.974.0" and x.get("id")=="OMISSIONS-13ML-G893-ORIGINAL-D9-D19-FOLIO-SEAM-20261031" for x in l["checkpoint_log"])
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 return True
def replay_images(e,dirpath):
 from PIL import Image
 for row in e["g893_original_images"]:
  raw=(Path(dirpath)/row["jpg"]).read_bytes()
  assert file_sha(raw)==row["sha256"],row["page"]
  with Image.open(Path(dirpath)/row["jpg"]) as f:
   assert list(f.size)==row["native_size"] and f.format=="JPEG"
   rgb=f.convert("RGB")
  assert file_sha(rgb.tobytes())==row["rgb_sha256"]
  assert file_sha(rgb.crop(tuple(row["roi"])).tobytes())==row["roi_rgb_sha256"]
  if "second_roi" in row:
   assert file_sha(rgb.crop(tuple(row["second_roi"])).tobytes())==row["second_roi_rgb_sha256"]
 return True
def replay_print(e,source):
 from PIL import Image
 with Image.open(source) as f: rgb=f.convert("RGB")
 p=e["independent_original_print"]
 assert file_sha(rgb.tobytes())==p["source_page15_rgb_sha256"]
 assert file_sha(rgb.crop(tuple(p["p15_roi"])).tobytes())==p["p15_roi_rgb_sha256"]
 return True
if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("--g893-dir",help="Locally verified exact-original JPEG directory (optional)")
 ap.add_argument("--zhou-p15",help="Locally original-PDF 2.5x RGB p15 image (optional)")
 args=ap.parse_args()
 e=json.loads(E.read_text(encoding="utf8"))
 s=json.loads((ROOT/"docs/PROJECT-CURRENT-STATE-R1.json").read_text(encoding="utf8"))
 l=json.loads((ROOT/"docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json").read_text(encoding="utf8"))
 assert verify(e,s,l)
 if args.g893_dir: assert replay_images(e,args.g893_dir)
 if args.zhou_p15: assert replay_print(e,args.zhou_p15)
 print(json.dumps({"status":"PASS","native_pages":3,"consecutive_source_days":11,"G893_historical_winners":0,"source_original_replay":bool(args.g893_dir),"printed_original_replay":bool(args.zhou_p15)}))
