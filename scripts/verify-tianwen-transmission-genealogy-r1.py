#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHARTER = ROOT / "docs/TIANWEN-SYSTEM-CHARTER-R1.md"
PROTOCOL = ROOT / "docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md"
GRAPH = ROOT / "docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json"
STATE = ROOT / "docs/PROJECT-CURRENT-STATE-R1.json"
BATCH_12CH = ROOT / "docs/research/ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-R1.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (CHARTER, PROTOCOL, GRAPH, STATE, BATCH_12CH):
        if not path.is_file():
            fail(f"Tianwen transmission artifact missing: {path.relative_to(ROOT)}")

    charter = CHARTER.read_text(encoding="utf-8")
    for marker in (
        "SYSTEM_UMBRELLA_NAME_ZH=天问",
        "SYSTEM_UMBRELLA_NAME_EN=TIANWEN",
        "天以命运问人，人以命理问天。",
        "DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED",
        "TIANWEN_TRANSMISSION_GENEALOGY_R1=ACTIVE_INCREMENTAL",
        "PREDICTION_AI_INTERPRETATION=CURRENTLY_OUT_OF_SCOPE",
    ):
        if marker not in charter:
            fail(f"Tianwen charter marker missing: {marker}")

    protocol = PROTOCOL.read_text(encoding="utf-8")
    for marker in (
        "GENEALOGY_MODEL=EVIDENCE_SCOPED_GRAPH_NOT_SINGLE_TREE",
        "work_composition_date",
        "edition_impression_date",
        "physical_copy_date",
        "digital_surrogate_date",
        "相同数字 ≠ 同一数表",
        "FUTURE_BATCH_TRANSMISSION_IMPACT=REQUIRED_WHEN_MATERIAL",
    ):
        if marker not in protocol:
            fail(f"Transmission protocol marker missing: {marker}")

    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    if graph.get("schema") != "TIANWEN-TRANSMISSION-GENEALOGY-GRAPH-R1":
        fail("Transmission graph schema mismatch")
    if graph.get("status") != "ACTIVE_INCREMENTAL":
        fail("Transmission graph status regressed")
    inv = graph.get("invariants", {})
    required_true = (
        "single_tree_assumption_forbidden",
        "work_edition_physical_copy_digital_surrogate_dates_must_be_separated_when_material",
        "same_wording_does_not_prove_direct_copy",
        "same_numeric_pair_does_not_prove_same_table",
        "same_title_does_not_prove_same_edition_or_copy",
        "parallel_coexistence_does_not_prove_lineage",
        "genealogy_change_does_not_automatically_reopen_chart_algorithm",
        "prediction_ai_interpretation_scope_unchanged",
    )
    if any(inv.get(k) is not True for k in required_true):
        fail("Transmission graph invariant regressed")

    nodes = graph.get("nodes", [])
    node_ids = [n.get("node_id") for n in nodes]
    if len(node_ids) != len(set(node_ids)):
        fail("Duplicate transmission node_id")
    required_nodes = {
        "TEXT-WORK-SISHI-QIHOU-JIJIE",
        "EDITION-SISHI-QIHOU-JINGTAI6-HUTINGCAN-1455",
        "PHYSICAL-COPY-SISHI-QIHOU-NCL03164-OLD-MANUSCRIPT",
        "TABLE-FAMILY-TONGSHU-COARSE-40-60",
        "STANDARD-NANJING-59KE-1447",
        "TABLE-NANJING-DATONG-DAILY-CII-N-1380S",
        "TABLE-SANMING-1578-DAYNIGHT-KE",
        "TABLE-HANXIANFU-1010-24QI-PRECISION",
        "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",
        "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",
        "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",
        "PHYSICAL-COPY-CHILJEONGSAN-NAEPYEON-G894-1444",
        "PASSAGE-SEJONG158-HANYANG-LOCAL-CALIBRATION",
        "STANDARD-HANYANG-61KE-1444",
        "PERSON-ZHAO-YOUQIN-YUANDU",
        "PASSAGE-GEXIANG-HUNDRED-KE-HALF-ZI",
        "PHYSICAL-COPY-SHENDAO-HKU-B17672971-FASC4",
        "PASSAGE-SHENDAO-V11-ZHAOYUANDU-HUNDRED-KE-HALF-ZI",
        "PASSAGE-SHENDAO-V11-REGIONAL-DAYNIGHT-CALIBRATION",
        "PHYSICAL-COPY-SANMING-NCL06589-1578",
        "PASSAGE-SANMING-1578-HUNDRED-KE-HALF-ZI",
        "RULE-FAMILY-HUNDRED-KE-HALF-ZI-TEXTUAL-LINEAGE",
    }
    if not required_nodes.issubset(set(node_ids)):
        fail("Transmission graph seed nodes incomplete")

    edges = graph.get("edges", [])
    edge_ids = [e.get("edge_id") for e in edges]
    if len(edge_ids) != len(set(edge_ids)):
        fail("Duplicate transmission edge_id")
    node_set = set(node_ids)
    allowed_rel = set(graph.get("relation_types", []))
    allowed_status = set(graph.get("allowed_statuses", []))
    for edge in edges:
        if edge.get("from") not in node_set or edge.get("to") not in node_set:
            fail(f"Transmission edge has missing endpoint: {edge.get('edge_id')}")
        if edge.get("relation") not in allowed_rel:
            fail(f"Transmission edge relation not registered: {edge.get('edge_id')}")
        if edge.get("status") not in allowed_status:
            fail(f"Transmission edge status not registered: {edge.get('edge_id')}")
        if not edge.get("evidence_class"):
            fail(f"Transmission edge lacks evidence class: {edge.get('edge_id')}")
        if not edge.get("evidence"):
            fail(f"Transmission edge lacks evidence: {edge.get('edge_id')}")

    e3 = next((e for e in edges if e.get("edge_id") == "TG-E0003"), None)
    if not e3 or e3.get("relation") != "PARALLEL_COEXISTS_WITH" or e3.get("status") != "CONFIRMED":
        fail("1447/1455 coexistence edge regressed")
    e7 = next((e for e in edges if e.get("edge_id") == "TG-E0007"), None)
    if not e7 or e7.get("relation") != "DISPROVES_LINEAGE_SHORTCUT" or e7.get("status") != "CONFIRMED":
        fail("1455/Sanming lineage-shortcut firewall regressed")

    e8 = next((e for e in edges if e.get("edge_id") == "TG-E0008"), None)
    if not e8 or e8.get("relation") != "STRUCTURAL_ANCESTRY_CANDIDATE_FOR" or e8.get("status") != "PROBABLE":
        fail("1010/coarse 24-row structural edge regressed")

    e11 = next((e for e in edges if e.get("edge_id") == "TG-E0011"), None)
    if not e11 or e11.get("relation") != "STRUCTURAL_ANCESTRY_CANDIDATE_FOR" or e11.get("status") != "PROBABLE":
        fail("Huqianjing/Sanming structural ancestry edge regressed")
    e12 = next((e for e in edges if e.get("edge_id") == "TG-E0012"), None)
    if not e12 or e12.get("relation") != "SHARED_COMMON_ANCESTOR_CANDIDATE" or e12.get("status") != "HIGH_CONFIDENCE":
        fail("Huqianjing cross-recension common-ancestry edge regressed")

    e13 = next((e for e in edges if e.get("edge_id") == "TG-E0013"), None)
    if not e13 or e13.get("relation") != "ATTESTS" or e13.get("status") != "CONFIRMED":
        fail("G894 Hanyang standard attestation edge regressed")
    e14 = next((e for e in edges if e.get("edge_id") == "TG-E0014"), None)
    if not e14 or e14.get("relation") != "ATTESTS" or e14.get("status") != "CONFIRMED":
        fail("Sejong 158 Hanyang-locality attestation edge regressed")
    e15 = next((e for e in edges if e.get("edge_id") == "TG-E0015"), None)
    if not e15 or e15.get("relation") != "PARALLEL_COEXISTS_WITH" or e15.get("status") != "CONFIRMED":
        fail("Hanyang/Nanjing regional parallel edge regressed")

    e37 = next((e for e in edges if e.get("edge_id") == "TG-E0037"), None)
    if not e37 or e37.get("relation") != "ATTESTS" or e37.get("status") != "CONFIRMED":
        fail("Shendao physical/prose attestation edge regressed")
    e38 = next((e for e in edges if e.get("edge_id") == "TG-E0038"), None)
    if not e38 or e38.get("relation") != "EXPLICITLY_CITES" or e38.get("status") != "CONFIRMED":
        fail("Shendao Zhao-Yuandu attribution edge regressed")
    e43 = next((e for e in edges if e.get("edge_id") == "TG-E0043"), None)
    if not e43 or e43.get("relation") != "TEXTUAL_ANCESTRY_CANDIDATE_FOR" or e43.get("status") != "PROBABLE":
        fail("Gexiang/Shendao textual ancestry candidate edge regressed")
    e44 = next((e for e in edges if e.get("edge_id") == "TG-E0044"), None)
    if not e44 or e44.get("relation") != "TEXTUAL_ANCESTRY_CANDIDATE_FOR" or e44.get("status") != "PROBABLE":
        fail("Gexiang/Sanming textual ancestry candidate edge regressed")

    shendao = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-SHENDAO-HKU-B17672971-FASC4")
    if "UNRESOLVED_WITHIN_RANGE" not in shendao.get("physical_copy_date", ""):
        fail("Shendao manuscript was falsely narrowed to a pre-1578 physical-copy date")

    ncl = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-SISHI-QIHOU-NCL03164-OLD-MANUSCRIPT")
    if ncl.get("physical_copy_date") != "UNRESOLVED":
        fail("NCL-03164 physical-copy date was falsely closed")

    non_edges = graph.get("explicit_non_edges", [])
    if not any(
        x.get("from") == "EDITION-SISHI-QIHOU-JINGTAI6-HUTINGCAN-1455"
        and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE"
        and x.get("status") == "UNRESOLVED"
        for x in non_edges
    ):
        fail("Direct-copy non-edge firewall missing")

    batch = json.loads(BATCH_12CH.read_text(encoding="utf-8"))
    impact = batch.get("transmission_impact", {})
    if not impact or not impact.get("nodes_strengthened") or not impact.get("edges_supported"):
        fail("Batch 12CH transmission_impact missing")
    if batch.get("adjudication", {}).get("algorithm_reopen_authorized") is not False:
        fail("Transmission seed unexpectedly reopened algorithm")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    identity = state.get("tianwen_identity", {})
    if identity.get("umbrella_name_zh") != "天问" or identity.get("umbrella_name_en") != "TIANWEN":
        fail("Current-state Tianwen identity missing")
    if identity.get("transmission_genealogy_status") != "ACTIVE_INCREMENTAL":
        fail("Current-state transmission status missing")
    if state.get("invariants", {}).get("deterministic_fusion_chart_product_r1") != "CLOSED":
        fail("Tianwen formalization changed deterministic product invariant")
    if state.get("invariants", {}).get("prediction_ai_interpretation_scope") != "OUT_OF_SCOPE_FOR_CURRENT_STAGE":
        fail("Tianwen formalization changed prediction scope invariant")

    bootstrap = state.get("new_chat_bootstrap_order", [])
    for path in (
        "read docs/TIANWEN-SYSTEM-CHARTER-R1.md",
        "read docs/TRANSMISSION-GENEALOGY-PROTOCOL-R1.md",
        "read docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json",
    ):
        if path not in bootstrap:
            fail(f"Tianwen startup dependency missing: {path}")

    print("TIANWEN_TRANSMISSION_GENEALOGY_R1=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
