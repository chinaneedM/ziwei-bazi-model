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
BATCH_12DP = ROOT / "docs/research/ZIWEI-DATONG-CIIN-49-58-CROSSING-AND-QICE-OFFSET-REPLAY-R1.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (CHARTER, PROTOCOL, GRAPH, STATE, BATCH_12CH, BATCH_12DP):
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
        "PHYSICAL-COPY-GEXIANG-NCL06265-ZHENGDE15-1520",
        "SOURCE-FAMILY-YUELING-CITED-TONGSHU-DAYNIGHT",
        "TABLE-LEIBIAN-FINE-SISHI-38-62",
        "PHYSICAL-COPY-LEIBIAN-NLC-MING-VOL1",
        "PHYSICAL-COPY-YINYANG-BAOJIAN-NLC-MINGCHU-V1-4",
        "PHYSICAL-COPY-LEIBIAN-NLC-JIAJING30-1551-VOL1",
        "PHYSICAL-COPY-HEBING-TONGSHU-LOC-JIAJING33-1554-JUAN17",
        "PHYSICAL-COPY-TONGSHU-LEIJU-NLC-JIAJING30-1551-V16-19",
        "TEXT-WORK-ZHUYI-JIANGXUQI-1616",
        "TEXT-WORK-LEIJING-TUYI-ZHANGJIEBIN-1624",
        "TABLE-FAMILY-POST1578-NANJING-59-41-STEPPED",
        "PHYSICAL-COPY-TAIYI-TONGZONG-XUXIU-MING-MANUSCRIPT",
        "PASSAGE-TAIYI-JUAN1-DAILY-SUNRISE-INTERPOLATION",
        "RULE-SHOUSHI-DATONG-QICE-15_2184375",
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
    e46 = next((e for e in edges if e.get("edge_id") == "TG-E0046"), None)
    if not e46 or e46.get("relation") != "ATTESTS" or e46.get("status") != "CONFIRMED":
        fail("Gexiang 1520 physical attestation edge regressed")
    gexiang1520 = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-GEXIANG-NCL06265-ZHENGDE15-1520")
    if gexiang1520.get("edition_impression_date") != "1520_ZHENGDE15":
        fail("Gexiang 1520 edition date regressed")
    e47 = next((e for e in edges if e.get("edge_id") == "TG-E0047"), None)
    if not e47 or e47.get("relation") != "EXPLICITLY_CITES" or e47.get("status") != "CONFIRMED":
        fail("Yueling generic Tongshu citation edge regressed")
    cited_tongshu = next(n for n in nodes if n.get("node_id") == "SOURCE-FAMILY-YUELING-CITED-TONGSHU-DAYNIGHT")
    if cited_tongshu.get("source_label") != "通書" or cited_tongshu.get("exact_bibliographic_identity") != "UNRESOLVED" or cited_tongshu.get("pre1578_status") != "UNRESOLVED":
        fail("Yueling cited Tongshu identity firewall regressed")
    e48 = next((e for e in edges if e.get("edge_id") == "TG-E0048"), None)
    if not e48 or e48.get("relation") != "ATTESTS" or e48.get("status") != "CONFIRMED":
        fail("Leibian fine-table physical attestation edge regressed")
    e49 = next((e for e in edges if e.get("edge_id") == "TG-E0049"), None)
    if not e49 or e49.get("relation") != "PARALLEL_COEXISTS_WITH" or e49.get("status") != "CONFIRMED":
        fail("Leibian fine/coarse coexistence edge regressed")
    e50 = next((e for e in edges if e.get("edge_id") == "TG-E0050"), None)
    if not e50 or e50.get("relation") != "ATTESTS" or e50.get("status") != "CONFIRMED":
        fail("1551 Leibian fine-table pre-1578 attestation edge regressed")
    if e50.get("from") != "PHYSICAL-COPY-LEIBIAN-NLC-JIAJING30-1551-VOL1" or e50.get("to") != "TABLE-LEIBIAN-FINE-SISHI-38-62":
        fail("1551 Leibian fine-table attestation endpoints regressed")
    e51 = next((e for e in edges if e.get("edge_id") == "TG-E0051"), None)
    if not e51 or e51.get("relation") != "ATTESTS" or e51.get("status") != "CONFIRMED":
        fail("1554 Hebing Tongshu coarse-table attestation edge regressed")
    if e51.get("from") != "PHYSICAL-COPY-HEBING-TONGSHU-LOC-JIAJING33-1554-JUAN17" or e51.get("to") != "TABLE-FAMILY-TONGSHU-COARSE-40-60":
        fail("1554 Hebing Tongshu attestation endpoints regressed")
    tongshu_leiju_1551 = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-TONGSHU-LEIJU-NLC-JIAJING30-1551-V16-19")
    if tongshu_leiju_1551.get("edition_impression_date") != "MING_JIAJING_30_1551_CENSUS_AND_SHANBEN_CATALOG_BOUND":
        fail("1551 Tongshu Leiju edition binding regressed")
    if tongshu_leiju_1551.get("identifier") != "NLC census 110000-0101-0013797 / call no. 14202 / OPAC doc 001790345 / internal id 411999023866 / Shanben catalog item 450":
        fail("1551 Tongshu Leiju identifier binding regressed")
    if tongshu_leiju_1551.get("public_digital_index_status") != "CLOSED_NO_TARGET_RECORD_OBSERVED_UNDER_EXACT_TITLE_OR_EXACT_SBNUMBER_14202":
        fail("1551 Tongshu Leiju public digital-index boundary regressed")
    opac1551 = tongshu_leiju_1551.get("opac_control", {})
    if opac1551.get("doc_number") != "001790345" or opac1551.get("internal_id") != "411999023866" or opac1551.get("holding") != "南区善本阅览室":
        fail("1551 Tongshu Leiju OPAC strengthening regressed")
    surrogate1551 = tongshu_leiju_1551.get("public_surrogate_discovery", {})
    if surrogate1551.get("olcc_b1micu") != "AUTHENTICATION_BLOCKED_TARGET_PRESENCE_UNRESOLVED":
        fail("1551 Tongshu Leiju microform access firewall regressed")
    if surrogate1551.get("union_bibliography") != "48_OF_48_PAGES_576_OF_576_RECORDS_NO_TARGET_OR_VARIANT_COPY":
        fail("1551 Tongshu Leiju union-bibliography closure regressed")
    if "Table family and Sanming/Yueling fingerprint remain unresolved." not in tongshu_leiju_1551.get("target_result", ""):
        fail("1551 Tongshu Leiju target-text unresolved firewall regressed")
    if not any(
        x.get("from") == "PHYSICAL-COPY-TONGSHU-LEIJU-NLC-JIAJING30-1551-V16-19"
        and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE"
        and x.get("relation") == "DIRECT_TARGET_FINGERPRINT_ATTESTATION"
        and x.get("status") == "UNRESOLVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("1551 Tongshu Leiju/Sanming target-fingerprint unresolved firewall missing")
    if not any(
        x.get("from") == "PHYSICAL-COPY-TONGSHU-LEIJU-NLC-JIAJING30-1551-V16-19"
        and x.get("to") == "TABLE-YUELING-1589-DAYNIGHT-FINGERPRINT"
        and x.get("relation") == "DIRECT_TARGET_FINGERPRINT_ATTESTATION"
        and x.get("status") == "UNRESOLVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("1551 Tongshu Leiju/Yueling target-fingerprint unresolved firewall missing")
    hyp12dk = next((h for h in graph.get("lineage_hypotheses", []) if h.get("hypothesis_id") == "TG-H0001"), None)
    if hyp12dk is None or not any(
        x.get("batch") == "BATCH-12-ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-OPAC-SURROGATE-AND-UNION-BIBLIOGRAPHY-CLOSURE-DK"
        and "zero textual/numeric vote" in x.get("update", "")
        for x in hyp12dk.get("evidence_updates", [])
    ):
        fail("Batch 12DK genealogy hypothesis access-only update missing")
    locator12dl = tongshu_leiju_1551.get("secondary_reproduction_locator_after_12dl", {})
    if locator12dl.get("status") != "SCHOLARLY_LOCATOR_ONLY_PENDING_DIRECT_PHYSICAL_PAGE":
        fail("Batch 12DL secondary locator status regressed")
    if locator12dl.get("juan16_end_colophon_locator") != "卷十六末" or locator12dl.get("direct_physical_colophon_page_observed") is not False:
        fail("Batch 12DL juan-16 physical-page firewall regressed")
    if locator12dl.get("same_printing_shop_proves_textual_or_table_lineage") is not False or locator12dl.get("numeric_ancestry_vote_increment") != 0:
        fail("Batch 12DL printing-shop lineage firewall regressed")
    if not any(
        x.get("batch") == "BATCH-12-ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-TITLE-COLOPHON-AND-REPRODUCTION-TARGETING-DL"
        and "zero textual/numeric vote" in x.get("update", "")
        and "downstream reuse" in x.get("update", "")
        for x in hyp12dk.get("evidence_updates", [])
    ):
        fail("Batch 12DL genealogy hypothesis locator/dedup update missing")
    route12dm = tongshu_leiju_1551.get("current_lawful_access_route_after_12dm", {})
    if route12dm.get("request_status") != "PRECISE_PAYLOAD_FROZEN_NOT_SUBMITTED":
        fail("Batch 12DM access-route request status regressed")
    if route12dm.get("target_call_number") != "14202" or route12dm.get("target_microfilm_presence") != "UNRESOLVED":
        fail("Batch 12DM target access identity/microfilm boundary regressed")
    if route12dm.get("direct_page_obtained") is not False or route12dm.get("provider_acceptance") is not False:
        fail("Batch 12DM provider/direct-page firewall regressed")
    if route12dm.get("textual_vote_increment") != 0 or route12dm.get("numeric_vote_increment") != 0:
        fail("Batch 12DM access-route genealogy vote firewall regressed")
    if not any(
        x.get("batch") == "BATCH-12-ZIWEI-TONGSHU-LEIJU-JIAJING30-1551-NLC-CURRENT-REPRODUCTION-SERVICE-ROUTE-DM"
        and "zero textual/numeric vote" in x.get("update", "")
        and "no request has been submitted" in x.get("update", "")
        for x in hyp12dk.get("evidence_updates", [])
    ):
        fail("Batch 12DM genealogy hypothesis access-route update missing")

    zhu12dn = next(n for n in nodes if n.get("node_id") == "TEXT-WORK-ZHUYI-JIANGXUQI-1616")
    leijing12dn = next(n for n in nodes if n.get("node_id") == "TEXT-WORK-LEIJING-TUYI-ZHANGJIEBIN-1624")
    family12dn = next(n for n in nodes if n.get("node_id") == "TABLE-FAMILY-POST1578-NANJING-59-41-STEPPED")
    if zhu12dn.get("pre1578_witness") is not False or "1616" not in zhu12dn.get("edition_impression_date", ""):
        fail("Batch 12DN Zhu Yi graph chronology regressed")
    if leijing12dn.get("pre1578_witness") is not False or "1624" not in leijing12dn.get("edition_impression_date", ""):
        fail("Batch 12DN Leijing graph chronology regressed")
    if family12dn.get("direct_pre1578_attestation") is not False or family12dn.get("exact_sanming_yueling_fingerprint_identity") is not False:
        fail("Batch 12DN post1578 table-family firewall regressed")
    e52 = next((e for e in edges if e.get("edge_id") == "TG-E0052"), None)
    e53 = next((e for e in edges if e.get("edge_id") == "TG-E0053"), None)
    e54 = next((e for e in edges if e.get("edge_id") == "TG-E0054"), None)
    if not e52 or e52.get("relation") != "ATTESTS" or e52.get("to") != "TABLE-FAMILY-POST1578-NANJING-59-41-STEPPED":
        fail("Batch 12DN Zhu Yi attestation edge regressed")
    if not e53 or e53.get("relation") != "ATTESTS" or e53.get("to") != "TABLE-FAMILY-POST1578-NANJING-59-41-STEPPED":
        fail("Batch 12DN Leijing attestation edge regressed")
    if not e54 or e54.get("relation") != "STRUCTURAL_MECHANISM_CANDIDATE_FOR" or e54.get("status") != "PROBABLE":
        fail("Batch 12DN C-II-N structural-mechanism edge regressed")
    for later_id in ("TEXT-WORK-ZHUYI-JIANGXUQI-1616", "TEXT-WORK-LEIJING-TUYI-ZHANGJIEBIN-1624"):
        if not any(x.get("from") == later_id and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("relation") == "DIRECT_ANCESTOR_OF" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
            fail(f"Batch 12DN chronology non-edge missing for {later_id}")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-DATONG-CIIN-INTEGER-CROSSING-AND-POST1578-59-41-LADDER-DN" and "zero pre-1578 parent vote" in x.get("update", "") and "day67=47.1074" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DN genealogy hypothesis correction/homology update missing")

    taiyi12do = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-TAIYI-TONGZONG-XUXIU-MING-MANUSCRIPT")
    passage12do = next(n for n in nodes if n.get("node_id") == "PASSAGE-TAIYI-JUAN1-DAILY-SUNRISE-INTERPOLATION")
    if taiyi12do.get("calendar_layer_pre1578_physically_proved") is not False or "1303" not in taiyi12do.get("work_composition_date", ""):
        fail("Batch 12DO Taiyi graph chronology firewall regressed")
    if passage12do.get("daily_interpolation_directly_observed") is not True or passage12do.get("direct_method_heading") != "求每日日出分術":
        fail("Batch 12DO Taiyi direct passage regressed")
    e55 = next((e for e in edges if e.get("edge_id") == "TG-E0055"), None)
    e56 = next((e for e in edges if e.get("edge_id") == "TG-E0056"), None)
    if not e55 or e55.get("relation") != "ATTESTS" or e55.get("status") != "CONFIRMED":
        fail("Batch 12DO Taiyi physical attestation edge regressed")
    if not e56 or e56.get("relation") != "STRUCTURAL_MECHANISM_CANDIDATE_FOR" or e56.get("status") != "POSSIBLE" or e56.get("to") != "TABLE-NANJING-DATONG-DAILY-CII-N-1380S":
        fail("Batch 12DO Taiyi mechanism-candidate edge regressed")
    if e54.get("confidence") != "HIGH_FOR_INTERIOR_42_58_THRESHOLD_AND_QICE_OFFSET_COMPATIBILITY" or not any("49-ke d81=48.9632/d82=49.0948" in str(x) and "58-ke d160=57.9862/d161=58.0424" in str(x) for x in e54.get("evidence", [])):
        fail("Batch 12DP TG-E0054 42-58/qice strengthening regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-DATONG-CIIN-42-48-CROSSING-AND-TAIYI-DAILY-INTERPOLATION-DO" and "seven consecutive 42-48" in x.get("update", "") and "summer endpoint" in x.get("update", "") and "zero exact pre-1578 Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DO genealogy hypothesis mechanism/firewall update missing")
    if not any(x.get("from") == "PHYSICAL-COPY-TAIYI-TONGZONG-XUXIU-MING-MANUSCRIPT" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("relation") == "DIRECT_ANCESTOR_OF" and x.get("status") == "UNRESOLVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12DO Taiyi/Sanming direct-ancestry firewall missing")

    qice12dp = next(n for n in nodes if n.get("node_id") == "RULE-SHOUSHI-DATONG-QICE-15_2184375")
    if qice12dp.get("qice_days") != 15.2184375 or qice12dp.get("direct_cii_n_parent") is not False or qice12dp.get("direct_sanming_parent") is not False:
        fail("Batch 12DP qi-ce graph node regressed")
    batch12dp = json.loads(BATCH_12DP.read_text(encoding="utf-8"))
    if batch12dp.get("leijing_1624_transition_replay", {}).get("historical_counting_convention_selected") is not False:
        fail("Batch 12DP counting-convention firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-DATONG-CIIN-49-58-CROSSING-AND-QICE-OFFSET-REPLAY-DP" and "seventeen consecutive 42-58" in x.get("update", "") and "0.5291" in x.get("update", "") and "zero exact pre-1578 Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DP genealogy hypothesis threshold/qice update missing")

    leibian_fine = next(n for n in nodes if n.get("node_id") == "TABLE-LEIBIAN-FINE-SISHI-38-62")
    if leibian_fine.get("exact_sanming_yueling_target_identity") is not False:
        fail("Leibian fine-table exact-target mismatch regressed")
    if leibian_fine.get("pre1578_physical_attestation_closed") is not True:
        fail("Leibian fine-table pre-1578 chronology closure regressed")
    if leibian_fine.get("chronology_after_12dh") != "DIRECT_PRE1578_ATTESTATION_BY_NLC_JIAJING30_1551_CATALOG_BOUND_COPY":
        fail("Leibian fine-table 1551 chronology binding regressed")
    leibian_1551 = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-LEIBIAN-NLC-JIAJING30-1551-VOL1")
    if leibian_1551.get("edition_impression_date") != "MING_JIAJING_30_1551_CATALOG_BOUND":
        fail("1551 Leibian physical-copy date binding regressed")
    hebing1554 = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-HEBING-TONGSHU-LOC-JIAJING33-1554-JUAN17")
    if hebing1554.get("edition_impression_date") != "MING_JIAJING_33_1554_CATALOG_AND_COLOPHON_NOTE_BOUND":
        fail("1554 Hebing Tongshu physical-copy date binding regressed")
    coarse_family = next(n for n in nodes if n.get("node_id") == "TABLE-FAMILY-TONGSHU-COARSE-40-60")
    if coarse_family.get("direct_1554_anchors") != {"大寒":"41/59","雨水":"45/55","夏至":"60/40"}:
        fail("1554 Hebing Tongshu coarse anchors regressed")
    if not any(
        x.get("from") == "PHYSICAL-COPY-HEBING-TONGSHU-LOC-JIAJING33-1554-JUAN17"
        and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE"
        and x.get("status") == "DISPROVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("1554 Hebing/Sanming unchanged-table non-edge missing")
    if not any(
        x.get("from") == "PHYSICAL-COPY-LEIBIAN-NLC-JIAJING30-1551-VOL1"
        and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE"
        and x.get("status") == "DISPROVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("1551 Leibian/Sanming unchanged-table non-edge missing")
    yinyang_baojian = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-YINYANG-BAOJIAN-NLC-MINGCHU-V1-4")
    if yinyang_baojian.get("surviving_scope") != "VOLUMES_1_TO_4_ONLY; VOLUME_5_MISSING_FROM_CURRENT_SCAN":
        fail("Yinyang Baojian surviving-scope firewall regressed")
    if yinyang_baojian.get("whole_work_negative") is not False:
        fail("Yinyang Baojian whole-work negative was overpromoted")
    if not any(
        x.get("from") == "PHYSICAL-COPY-YINYANG-BAOJIAN-NLC-MINGCHU-V1-4"
        and x.get("to") == "TABLE-YUELING-1589-DAYNIGHT-FINGERPRINT"
        and x.get("status") == "UNRESOLVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("Yinyang Baojian target-fingerprint scope control missing")
    if not any(
        x.get("from") == "TABLE-LEIBIAN-FINE-SISHI-38-62"
        and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE"
        and x.get("status") == "DISPROVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("Leibian fine/Sanming unchanged-parent non-edge missing")

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
