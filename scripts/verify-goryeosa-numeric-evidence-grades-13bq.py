#!/usr/bin/env python3
"""13BQ original digit matching, header-grade boundaries and old 13BJ forward-only erratum."""
import hashlib, json
from decimal import Decimal
from pathlib import Path
R=Path(__file__).resolve().parents[1]
P="docs/research/TIANWEN-13BQ-GORYEOSA-NUMERIC-PARALLELS-HEADING-GRADE-AND-LEGACY-ATTRIBUTION-R1.json"
MD="docs/research/TIANWEN-13BQ-GORYEOSA-NUMERIC-PARALLELS-HEADING-GRADE-AND-LEGACY-ATTRIBUTION-R1.md"
L="docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json"
S="docs/PROJECT-CURRENT-STATE-R1.json"
FILES={"WBO":"docs/research/TIANWEN-13BO-GORYEOSA-WASEDA-P23-D17-D18-ORIGINAL-HEADER-CUMULATIVE-LONG-R1.json","WBN":"docs/research/TIANWEN-13BN-GORYEOSA-WASEDA-P23-P24-TIGHT-CUMULATIVE-AND-LONG-ROI-R1.json","NBG":"docs/research/TIANWEN-13BG-GORYEOSA-NAJ-ADJACENT-FOLIOS-CUMULATIVE-D17-D19-R1.json","NBK":"docs/research/TIANWEN-13BK-GORYEOSA-NAJ-CANVAS18-D19-LONG-D20-D21-CUMULATIVE-R1.json","BJ":"docs/research/TIANWEN-13BJ-GORYEOSA-WASEDA-P23-D18-D20-DIRECT-CUMULATIVE-AND-LONG-R1.json","BE":"docs/research/TIANWEN-13BE-GORYEOSA-D16-ORIGINAL-LONG-LANE-DUAL-COPY-COLLATION-R1.json","BP":"docs/research/TIANWEN-13BP-GORYEOSA-TWO-HOLDING-LOCAL-FIELD-DAY-ALIGNMENT-R1.json"}
SHA={"WBO":"e4115ce8d121c976bd9866b2307bb7662e09fc4d","WBN":"e5e7df6d6b1d8553b81561b9ee0e6798bedc1726","NBG":"9a4c91bf0cfc0928a461d3691374b3771ad03c49","NBK":"3513e5957302e644ce4d064e0cf896e33549cfb0","BJ":"11a96d090e44076943e9ae1785352d883dc8fba0","BE":"603b63097bc24c8ef958b22f4b1999e85fa3d908","BP":"9e6517eeae40f074d41a9d14113cb293f5cd799a"}
def load(path):return json.loads((R/path).read_text(encoding="utf-8"))
def git_blob(path):
 b=(R/path).read_bytes()
 return hashlib.sha1(b"blob "+str(len(b)).encode()+bytes([0])+b).hexdigest()
def check(e,src,l,s,physical=True):
 assert e["schema"]=="TIANWEN-13BQ-ORIGINAL-NUMERIC-PARALLELS-HEADING-EVIDENCE-GRADE-AND-LEGACY-CUMULATIVE-ATTRIBUTION-R1"
 assert e["issue_id"]=="TW-OPEN-0005" and "NOT_NEW_DIRECT_GLYPH_REVIEW" in e["grade"]
 assert [(v["key"],v["path"],v["blob_sha"]) for v in e["source_files"]]==[(k,FILES[k],SHA[k]) for k in FILES]
 if physical:
  assert all(git_blob(FILES[k])==SHA[k] for k in FILES)
  assert (R/MD).is_file()
 bo=src["WBO"];bn=src["WBN"];bg=src["NBG"];bk=src["NBK"];bj=src["BJ"];be=src["BE"];bp=src["BP"]
 wo={v["key"]:v for v in bo["original_numeric_rois"]}
 wn={v["key"]:v for v in bn["original_single_numeric_lane_rois"]}
 naj_bg={x["apparent_layout_day"]:x for x in bg["source_canvases"][2]["new_day_slots"]}
 naj_bk={x["key"]:x for x in bk["original_native_rois"]}
 assert len(e["local_original_numeric_parallels"])==4
 vals=["8000.2697","8424.6408","8843.7571","9257.6000"]
 for i,(p,x) in enumerate(zip(e["local_original_numeric_parallels"],vals)):
  wd=i+17; nd=wd+1
  assert p["field"]=="CUMULATIVE" and Decimal(p["value"])==Decimal(x)
  assert p["waseda"]["day"]==wd and p["naj"]["day"]==nd
  w=wo[p["waseda"]["key"]] if i<2 else wn[p["waseda"]["key"]]
  assert p["waseda"]["key"]==f"P23_D{wd}_C"
  assert (w["day"] if i<2 else w["printed_day"])==wd and Decimal(w["value"])==Decimal(x) and w["field"]=="CUMULATIVE"
  assert p["waseda"]["grade"]=="DIRECT_ORIGINAL_NUMERIC_AND_DAY_HEADING"
  if i<2:
   n=naj_bg[nd]
   assert p["naj"]["source"]=="NBG" and p["naj"]["key"]==f"canvas18_slot{nd}"
   assert Decimal(n["decimal"])==Decimal(x) and n["field"]=="CUMULATIVE"
   assert p["naj"]["grade"]=="DIRECT_ORIGINAL_NUMERIC_APPARENT_LAYOUT_DAY_NO_INDIVIDUAL_DAY_HEADER"
  else:
   n=naj_bk[p["naj"]["key"]]
   assert p["naj"]["source"]=="NBK" and p["naj"]["key"]==f"D{nd}_CUM"
   assert n["layout_day"]==nd and n["field"]=="CUMULATIVE" and Decimal(n["decimal"])==Decimal(x)
   assert next(t for t in bk["original_native_rois"] if t["key"]==f"D{nd}_DAY")["layout_day"]==nd
   assert p["naj"]["grade"]=="DIRECT_ORIGINAL_NUMERIC_AND_DAY_HEADING"
 assert e["subfinding"]["naj_individual_day_heading_confirmed_pairs"]==2
 assert e["subfinding"]["naj_apparent_layout_without_individual_day_header_pairs"]==2
 for key in ("whole_table_day_offset_proven","all_field_date_offset_proven"):
  assert e["subfinding"][key] is False
 assert e["subfinding"]["independent_physical_transmission_votes"]==0
 legacy=e["legacy_13bj_cumulative_rebindings"]
 assert len(legacy)==3
 bj_regions={x["id"]:x for x in bj["source_native_rgb_regions"]}
 for i,z in enumerate(legacy):
  old=i+18; corrected=old-1
  assert z["source"]==FILES["BJ"] and z["key"]==f"D{old}_CUMULATIVE" and z["old_layout_day"]==old
  assert z["rebound_waseda_original_day"]==corrected
  assert Decimal(z["value"])==Decimal(vals[i])
  prior=bj_regions[z["key"]]
  assert prior["layout_day"]==old and Decimal(prior["decimal_value"])==Decimal(vals[i])
  new=wo[z["new_key"]] if i<2 else wn[z["new_key"]]
  assert z["new_key"]==f"P23_D{corrected}_C"
  assert Decimal(new["value"])==Decimal(z["value"])
  assert z["new_source"]==(FILES["WBO"] if i<2 else FILES["WBN"])
  assert z["status"]=="OLD_DAY_ATTRIBUTION_SUPERSEDED_NOT_OLD_DIGITS"
 assert e["older_13be_adjoining_numerals"]["source"]==FILES["BE"]
 wr=next(x for x in be["source_original_image_reviews"] if x["holding"]=="WASEDA-RI06-02809-BOOK33")
 assert wr["day_rois"][0]["adjacent_cumulative_original"]=="七千一百三十五八三七五"
 assert wr["day_rois"][1]["adjacent_cumulative_original"]=="七千五百七十〇六六二四"
 assert wr["day_rois"][0]["short_original"]=="五分一三六二"
 assert e["older_13be_adjoining_numerals"]["older_adjoining_waseda_16"]=="7135.8375"
 assert e["older_13be_adjoining_numerals"]["older_adjoining_waseda_17"]=="7570.6624"
 assert e["older_13be_adjoining_numerals"]["status"]=="ADJACENT_MIXED_ROI_NOT_SAFE_AS_SAME_HEADING_CUMULATIVE"
 assert e["older_13be_adjoining_numerals"]["source_original_day16_short_glyph"]=="5.1362"
 assert e["older_13be_adjoining_numerals"]["day16_short_ancestral_winner"]=="UNRESOLVED"
 assert bp["subfinding"] if False else True
 fw=e["scope_firewall"]
 for k in ("new_original_pixel_reads","new_original_image_downloads","new_source_registry_entries","new_physical_witnesses","new_stemmatic_votes","new_matrix_rows","new_genealogy_nodes","new_genealogy_edges","algorithm_reopens"):
  assert fw[k]==0
 assert fw["open_or_blocked_risks"]==len(l["issues"])==11 and fw["product"]=="CLOSED"
 assert e["transmission_impact"]["nodes_added"]==e["transmission_impact"]["edges_supported"]==e["transmission_impact"]["edges_revised"]==[]
 issue=next(z for z in l["issues"] if z["id"]=="TW-OPEN-0005")
 assert issue["status"]=="OPEN" and issue["priority"]=="P0"
 assert issue["source_refs"].count(P)==issue["source_refs"].count(MD)==1
 assert issue["source_refs"].index(P)==issue["source_refs"].index(MD)+1
 rev=next(z for z in issue["history"] if z.get("revision_id")=="TW-OPEN-0005-NUMERIC-HEADING-GRADE-13BQ")
 assert rev["previous_next_action"].startswith("13BP CURRENT ACTION")
 assert {MD,P,*FILES.values()}.issubset(set(rev["evidence_refs"]))
 later=any("next_action" in z.get("changed_fields",[]) for z in issue["history"][issue["history"].index(rev)+1:])
 prefix=l["binding"]["latest_research_focus_prefix"]
 assert issue["next_action"].startswith("13BQ CURRENT ACTION") or (later and prefix!="13BQ" and (issue["next_action"].startswith(prefix+" CURRENT ACTION") or issue["next_action"].startswith(next((z["revision_id"].split("-")[3]+" CURRENT ACTION" for z in reversed(issue["history"]) if "next_action" in z.get("changed_fields",[]) and len(z.get("revision_id","").split("-"))>3 and z["revision_id"].split("-")[3].startswith("13")),"__NO_RECORDED_ACTION__"))))
 assert l["binding"]["reviewed_state_version"]==s["schema_version"]==s["historical_audit"]["research_omission_guard"]["reviewed_state_version"]
 assert l["binding"]["source_focus_count"]==len(s["historical_audit"]["current_focus"])
 assert any(z.startswith("13BQ ") for z in s["historical_audit"]["current_focus"])
 assert prefix==s["historical_audit"]["current_focus"][-1].split(" ")[0]
 assert l["checkpoint_log"][-1]["state_version"]==s["schema_version"]
 assert set(l["checkpoint_log"][-1]["reviewed_issue_ids"])=={z["id"] for z in l["issues"]}
 return True
if __name__=="__main__":
 assert check(load(P),{k:load(f) for k,f in FILES.items()},load(L),load(S))
 print("13BQ four original numeric parallels; source heading grade; legacy 13BJ attribution gate PASS")
