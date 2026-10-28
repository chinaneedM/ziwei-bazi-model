#!/usr/bin/env python3
"""Diagnostic: find historical source counts accidentally compared to live counts.

This is a non-destructive, non-authoritative triage report. A literal 761 in a
frozen source evidence assertion is legitimate; only current state/manifest
comparisons deserve modernization, with source-specific review.
"""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
LIVES=("external_source_registry_total_unique_count","combined_source_count","extension_source_count")
def scan(root):
 out=[]
 for f in sorted((root/"scripts").glob("*.py")):
  for n,s in enumerate(f.read_text(encoding="utf-8",errors="replace").splitlines(),1):
   if "assert " not in s or "==761" not in s.replace(" ","") and "==114" not in s.replace(" ",""):continue
   if not any(k in s for k in LIVES):continue
   out.append({"path":f.relative_to(root).as_posix(),"line":n,"source":s.strip()[:420],
               "historic_snapshot_may_be_legitimate":True})
 return out
def main():
 result={"schema":"TIANWEN_STALE_LIVE_SOURCE_COUNT_GUARD_DIAGNOSTIC_R1","possible_live_count_overconstraints":scan(R),
         "automatic_fix_authorized":False,"historical_snapshot_rewrite_authorized":False}
 print(json.dumps(result,ensure_ascii=False))
if __name__=="__main__":main()
