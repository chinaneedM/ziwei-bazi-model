#!/usr/bin/env python3
"""Prepare the fixed, already-reviewed R8 admission transaction without remote writes.

Inputs are pinned to the existing pending checkpoint. Output is a set of complete
replacement files, not a second state database. A local checkout is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = "docs/research/TIANWEN-15FF-R-UPSTREAM-CROSS-CIVILIZATION-ORIGIN-COVERAGE-CHECKPOINT-R1.md"
SHARD = "docs/research/TIANWEN-15FF-R8-REGIONAL-AND-CROSS-CIVILIZATION-SOURCE-SHARD-R1.json"
OUTLINE = "docs/TIANWEN-ZIWEI-HISTORICAL-OUTLINE-R1.md"
ATLAS = "docs/TIANWEN-DUAL-HISTORY-COVERAGE-ATLAS-R1.md"
QUERY = "docs/PROJECT-REGISTRY-QUERY-R2.json"
VIEW = "docs/PROJECT-RECOVERY-VIEW-R2.json"
PINS = {
    "docs/PROJECT-CURRENT-STATE-R1.json": "702e82b65ecf87c01b2d52363272ca64802c0783",
    "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json": "5453fef89e6e3173337043381b9d5e35010fc1c1",
    "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json": "46a75cadb4940cf265fb302f0e911fa646d50253",
    "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json": "ea2ab50479450c39ce3fc7a00ea91cd713bf4a60",
    "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json": "5919e1b6bbc3c4b150507c41a13ccc9e13d20f17",
    "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json": "5ef9ca3e5507df6ea4250453cf7f663b3d2137cc",
    SHARD: "9c11f0d0b4229ca899526b9e8b9dd9b21e6a5e9d",
    # The new literal query keeps the same pre-admission checkpoint and manifest.
    # Its evidence is not used to broaden the six-source R8 transaction.
    QUERY: "6191233a1e58797456e5266f34528f5232bd0ac6",
}
VERSION = "1.1588.0"
CP = "TW-CHECKPOINT-15FF-R8-REGIONAL-CROSS-CIVILIZATION-ADMISSION-20261127"
FOCUS = ("13ZZ CURRENT ACTION 15FF-R8: exact rounds6–8 each 280 files/1499 records, zero literal hits, all archived. "
         "Six bounded catalog/secondary sources admitted: Wellcome Iyer 1885, BL EAP1294/2/33, Thomann 2008 bibliography, "
         "Greenbaum/Jones 2017, Jones 2026, Mak HSSA 2013. Current frame B photo (four frames same papyrus) and Jones pp35–36 "
         "screenshots rechecked; Mak screenshot blocked, text only. No ancient glyph/lineage verdict. 1505 sources/280 shards, "
         "graph819/581, Matrix222/222, 59 OPEN five P0, core CLOSED. NEXT retrieve dated South Indian original chart and "
         "Iranian/Central Asian specific technical witnesses, then admit remaining qualified candidates; Tenri/Jingu juan4 "
         "and 1959 base still open. No final breadth acceptance.")
NEXT = ("15FF-R8续：优先南印度实际方盘图页（Iyer印页6、EAP1294/2/33；新增目录线索EAP1294/2/44待查重），"
        "希腊抄本与敦煌原页、伊朗/中亚技术中介；Mak SCIAMVS及未准入候选继续身份复核；"
        "天理/神宫卷四古叶与1959底本仍待证。59未决五P0及Q不足项保留，不终验。")
BOUNDARY = (" R8: rounds 6–8 full 280-file/1499-record literal queries passed; six scoped bibliographic/secondary "
            "sources admitted. P.Berl.9825 frame B photograph recovered (four frames one artifact), Jones pp35–36 "
            "rechecked, Mak HSSA received text only. No ancient square chart, original Sanskrit glyph or direct "
            "lineage adjudication.")
NAV = ("\n\n### 15FF-R8｜跨文明上游候选的有限准入（2026-11-27）\n\n"
       "[检查点§11](research/TIANWEN-15FF-R-UPSTREAM-CROSS-CIVILIZATION-ORIGIN-COVERAGE-CHECKPOINT-R1.md)及"
       "[六来源分片](research/TIANWEN-15FF-R8-REGIONAL-AND-CROSS-CIVILIZATION-SOURCE-SHARD-R1.json)："
       "Iyer1885与EAP1294/2/33仅馆目；Thomann2008仅书目及反向假说归属；"
       "Greenbaum/Jones2017、Jones2026、Mak2013为现代研究。四装框同一纸草，非四独立物证；"
       "497图式年代及印度星占定年仍有争议。1505来源/280分片；无直传边，紫微/子平独立，59未决五P0、核心CLOSED，不终验。\n")

def need(ok, message):
    if not ok:
        raise ValueError(message)

def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()

def encode(value, compact=False):
    if compact:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def prepare(root: Path):
    originals = {p: (root / p).read_bytes() for p in PINS}
    for p, sha in PINS.items():
        need(blob_sha(originals[p]) == sha, "stale pinned input: " + p)
    ctx = runpy.run_path(str(root / "scripts/project-context-r2.py"))
    paths = ctx["PATHS"]
    data = {k: json.loads(originals[p]) for k, p in paths.items()}
    s, l, m = (data[k] for k in ("state", "ledger", "manifest"))
    shard = json.loads(originals[SHARD])
    need(s["schema_version"] == "1.1587.0" and l["binding"]["source_focus_count"] == 3283,
         "wrong baseline")
    need(len(l["issues"]) == 59 and len(l["checkpoint_log"]) == 1018, "ledger count")
    need(m["combined_source_count"] == 1499 and len(m["shards"]) == 279 and len(shard["sources"]) == 6,
         "source baseline")
    need(not any(x["path"] == SHARD for x in m["shards"]), "already admitted")
    need(all(x["physical_glyph_authority"] is False for x in shard["sources"]), "unexpected authority upgrade")
    need("PENDING_ATOMIC_PUBLICATION" in (root / BATCH).read_text(encoding="utf-8"),
         "missing pending checkpoint")
    m["schema_version"] = "1.260.0"
    m["date"] = "2026-11-27"
    m["shards"].append({"path": SHARD, "schema": shard["schema"], "blob_sha": PINS[SHARD], "source_count": 6})
    m["extension_source_count"] += 6
    m["combined_source_count"] += 6
    m["additional_research_evidence_15ff_r8"] = ("Six scoped records after exact R7 query rounds 6–8 and identity/grade review: "
        "two first-party catalogs, Thomann bibliography, Greenbaum/Jones 2017 paper and Jones 2026 critical edition, "
        "Mak 2013 HSSA. Same papyrus four frames; no direct lineage or glyph authority. " + BATCH)
    s["schema_version"] = VERSION
    s["updated_at"] = "2026-11-27"
    ha = s["historical_audit"]
    ha["external_source_registry_extension_count"] = m["extension_source_count"]
    ha["external_source_registry_total_unique_count"] = m["combined_source_count"]
    ha["current_focus"].append(FOCUS)
    ha["research_omission_guard"]["reviewed_state_version"] = VERSION
    rs = s["research_execution_strategy"]
    rs["next_deliverable"] = NEXT
    rs["breadth_first_progress"] += "\n" + FOCUS
    l["updated_at"] = "2026-11-27"
    l["binding"].update(reviewed_state_version=VERSION, source_focus_count=len(ha["current_focus"]),
                        latest_research_focus_prefix="13ZZ")
    issue = next(x for x in l["issues"] if x["id"] == "TW-OPEN-0059")
    previous = {k: issue[k] for k in ("evidence_boundary", "next_action")}
    issue["evidence_boundary"] += BOUNDARY
    issue["next_action"] = NEXT
    need(SHARD not in issue["source_refs"], "source already attached")
    issue["source_refs"].append(SHARD)
    issue["history"].append({
        "event": "EVIDENCE_SCOPE_REVISION", "date": "2026-11-27",
        "changed_fields": ["evidence_boundary", "next_action"], "previous_fields": previous,
        "reason": "Complete exact-HEAD registry rounds and bounded evidence admission, not historical closure.",
        "evidence_refs": [BATCH, SHARD],
    })
    l["checkpoint_log"].append({
        **l["checkpoint_log"][-1], "id": CP, "date": "2026-11-27", "state_version": VERSION,
        "result": FOCUS, "evidence_refs": [BATCH, OUTLINE, ATLAS, SHARD, QUERY],
        "unresolved_breadth_leads": [{"scope": "TW-OPEN-0059", "status": "OPEN", "next_evidence": NEXT}],
    })
    replacement = {paths[k]: encode(data[k], compact=(k == "ledger"))
                   for k in ("state", "ledger", "manifest")}
    bindings = {p: blob_sha(replacement.get(p, originals[p])) for p in paths.values()}
    replacement[VIEW] = ctx["encode"](ctx["project"](data, bindings))
    # This sentence appears only in prepared replacement files, never the live
    # checkpoint until the complete transaction is actually published.
    replacement[BATCH] = (root / BATCH).read_bytes() + (
        "\n\n### 11c. R8正式准入事务（以此整套权威文件提交为生效边界）\n\n"
        "六项限定来源准入，1505总来源/280分片、state 1.1588.0。"
        "此前PENDING及传输失败记录全部保留。旧query跨checkpoint，不能作为新manifest查询结果。"
        "Matrix222/222、图819/581、59未决五P0、CLOSED不变；transmission_impact=NONE，不终验。\n"
    ).encode("utf-8")
    for p in (OUTLINE, ATLAS):
        replacement[p] = (root / p).read_bytes() + NAV.encode("utf-8")
    # Compare the full reconstructed in-memory objects with the unchanged
    # prior ledger using the existing forward-only verifier.
    verifier = runpy.run_path(str(root / "scripts/verify-research-omission-risk-ledger-r1.py"))
    verifier["check_forward_only"](json.loads(originals[paths["ledger"]]), l)
    return replacement

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="new, separate directory for replacement files; never writes the checkout")
    args = parser.parse_args()
    out = args.output_dir.resolve()
    need(not out.exists(), "output directory must not exist")
    need(not out.is_relative_to(ROOT), "output must be outside the checkout")
    files = prepare(ROOT)
    for p, raw in files.items():
        target = out / p
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    print(json.dumps({"status": "PREPARED_NOT_PUBLISHED", "files": {p: {"bytes": len(raw), "blob_sha": blob_sha(raw)}
                         for p, raw in files.items()}}, ensure_ascii=False))

if __name__ == "__main__":
    main()
