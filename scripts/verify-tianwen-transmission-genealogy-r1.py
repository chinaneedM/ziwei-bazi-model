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
BATCH_12DQ = ROOT / "docs/research/ZIWEI-DATONG-NANJING59-ENDPOINT-RECOMPOSITION-R1.json"
BATCH_12DR = ROOT / "docs/research/ZIWEI-NLC-TAIYIN-TONGGUI-CHENGHUA-PHYSICAL-CII-N-CLOSURE-R1.json"
BATCH_12DS = ROOT / "docs/research/ZIWEI-NLC-TAIYIN-TONGGUI-CONTINUOUS-FEN-CONSUMER-INTERFACE-R1.json"
BATCH_12DT = ROOT / "docs/research/ZIWEI-KYUDB-DATONG-LIFA-TONGGUI-COMPONENT-SET-CROSSWALK-R1.json"
BATCH_12DU = ROOT / "docs/research/ZIWEI-NLC-DATONG-LIFA-TONGGUI-XUXIU1031-PHYSICAL-SCOPE-R1.json"
BATCH_12DV = ROOT / "docs/research/ZIWEI-XUXIU1031-ZHUNZHAI-CLEPSYDRA-JIEHOU-ARROW-SELECTION-R1.json"
BATCH_12DW = ROOT / "docs/research/ZIWEI-YONEZAWA-SHILIN1492-LIKOU-48ARROW-24QI-PHYSICAL-CLOSURE-R1.json"
BATCH_12DX = ROOT / "docs/research/ZIWEI-NAJDA-SUISHU-YUAN-LOUKE-48ARROW-HUANGJI5986-PHYSICAL-CLOSURE-R1.json"
BATCH_12DY = ROOT / "docs/research/ZIWEI-WUZONG-SHILU-1518-MULTISOURCE-LOCAL-CALIBRATION-PROPOSAL-R1.json"
BATCH_12DZ = ROOT / "docs/research/ZIWEI-LANPEN-KYOTO-40-60-PHYSICAL-HUQIAN-COPY-CONTROL-R1.json"
BATCH_12EA = ROOT / "docs/research/ZIWEI-JIUTANGSHU-JIAJING17-GUILOU-HALFUP-ROUNDING-R1.json"
BATCH_12EB = ROOT / "docs/research/ZIWEI-XINGYUNLU-DATONG-ENDPOINT-BINDING-R1.json"
BATCH_12EC = ROOT / "docs/research/ZIWEI-NCL06627-DATONGLIZHU-THRESHOLD-FINGERPRINT-R1.json"
BATCH_12ED = ROOT / "docs/research/ZIWEI-KYUDB-DATONGLIZHU-GK02426-PARTIAL-FINGERPRINT-R1.json"
BATCH_12EE = ROOT / "docs/research/ZIWEI-KYUDB-DATONGLIZHU-GK02538-1434-TYPE-POSTFACE-AND-FINGERPRINT-R1.json"
BATCH_12EI = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-INRYEOKJA-BODY-SCALE-COMPATIBILITY-AND-CASTING-FIREWALL-R1.json"
BATCH_12EJ = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-DAETONGLYOKJA-NAME-SCOPE-AND-SEJONG-LIST-FIREWALL-R1.json"
BATCH_12EK = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-SOURCE-BOUND-SHARED-GLYPH-CROPS-R1.json"
BATCH_12EL = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-MEDIUM-SIZECLASS-BINDING-R1.json"
BATCH_12EM = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-NOMINAL-PHYSICAL-SCALE-THREE-GLYPH-COMPARISON-R1.json"
BATCH_12EN = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-DATED-INRYEOKJA-THREE-WAY-FORM-VARIATION-FIREWALL-R1.json"
BATCH_12EO = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-OBJECT-SPECIFIC-FOUR-SIZE-CALIBRATION-R1.json"
BATCH_12EP = ROOT / "docs/research/ZIWEI-KYUDB-GK02538-IMJIN-TYPE-LOSS-RECOVERY-CONTINUITY-FIREWALL-R1.json"
BATCH_12EQ = ROOT / "docs/research/ZIWEI-WENYUANGE1441-ZHUNZHAI-TITLE-EXISTENCE-CHRONOLOGY-FIREWALL-R1.json"
BATCH_12ER = ROOT / "docs/research/ZIWEI-ZHUNZHAI-YUAN-SHOUSHI-COMPOSITION-ATTRIBUTION-FIREWALL-R1.json"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (CHARTER, PROTOCOL, GRAPH, STATE, BATCH_12CH, BATCH_12DP, BATCH_12DQ, BATCH_12DR, BATCH_12DS, BATCH_12DT, BATCH_12DU, BATCH_12DV, BATCH_12DW, BATCH_12DX, BATCH_12DY, BATCH_12DZ, BATCH_12EA, BATCH_12EB, BATCH_12EC, BATCH_12ED, BATCH_12EE, BATCH_12EI, BATCH_12EJ, BATCH_12EK, BATCH_12EL, BATCH_12EM, BATCH_12EN, BATCH_12EO, BATCH_12EP, BATCH_12EQ, BATCH_12ER):
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
        "TEXT-WORK-YUANTONG-DATONG-LIFA-TONGGUI-HONGWU17",
        "EDITION-NLC-DATONG-LIFA-TONGGUI-RESIDUAL-MING-MS-RECENSION",
        "PHYSICAL-COPY-NLC-DATONG-LIFA-TONGGUI-RESIDUAL-MING-MS",
        "DIGITAL-SURROGATE-XUXIU1031-NLC-DATONG-TONGGUI-RESIDUAL",
        "EDITION-KYUDB-DATONG-LIFA-TONGGUI-GK12434-12439-GABINJA",
        "PHYSICAL-COPY-KYUDB-SIYU-GK12434-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-TAIYANG-GK12435-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-JIAOSHI-GK12438-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-WUXING-GK12439-15C-GABINJA",
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
        "RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR",
        "PHYSICAL-COPY-NLC-TAIYIN-TONGGUI-CHENGHUA-411999012050",
        "PASSAGE-NLC-TAIYIN-TONGGUI-CHENHUN-LICHENG",
        "PHYSICAL-COPY-NLC-ZHUNZHAI-JILOU-DAOGUANG3-HUANG-SHILIJU-MS",
        "RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62",
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

    composite12dq = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR")
    if composite12dq.get("single_global_constant_fractional_threshold_disproved") is not True or composite12dq.get("exact_pre1578_combined_rule_text") != "UNRESOLVED":
        fail("Batch 12DQ composite-rule node firewall regressed")
    if composite12dq.get("clean_42_59_value_architecture_mechanically_covered") is not True or composite12dq.get("direct_sanming_parent") is not False:
        fail("Batch 12DQ composite value-architecture/direct-parent firewall regressed")
    e57 = next((e for e in edges if e.get("edge_id") == "TG-E0057"), None)
    e58 = next((e for e in edges if e.get("edge_id") == "TG-E0058"), None)
    e59 = next((e for e in edges if e.get("edge_id") == "TG-E0059"), None)
    if not e57 or e57.get("from") != "TABLE-NANJING-DATONG-DAILY-CII-N-1380S" or e57.get("to") != "RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR" or e57.get("relation") != "SYNTHESIS_COMPONENT_CANDIDATE_FOR" or e57.get("status") != "PROBABLE":
        fail("Batch 12DQ C-II-N composite-component edge regressed")
    if not e58 or e58.get("from") != "STANDARD-NANJING-59KE-1447" or e58.get("to") != "RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR" or e58.get("relation") != "SYNTHESIS_COMPONENT_CANDIDATE_FOR" or e58.get("status") != "PROBABLE":
        fail("Batch 12DQ Nanjing59 endpoint-component edge regressed")
    if not e59 or e59.get("from") != "RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR" or e59.get("to") != "TABLE-FAMILY-POST1578-NANJING-59-41-STEPPED" or e59.get("relation") != "STRUCTURAL_MECHANISM_CANDIDATE_FOR" or e59.get("status") != "PROBABLE":
        fail("Batch 12DQ composite clean-family edge regressed")
    batch12dq = json.loads(BATCH_12DQ.read_text(encoding="utf-8"))
    threshold12dq = batch12dq.get("constant_fractional_threshold_test", {})
    if threshold12dq.get("threshold_lower_bound") != 0.9862 or threshold12dq.get("threshold_upper_bound") != 0.6332 or threshold12dq.get("constant_threshold_intersection_empty") is not True:
        fail("Batch 12DQ constant-threshold contradiction regressed")
    if not any(
        x.get("from") == "RULE-FAMILY-NANJING-CII-INTEGER-THRESHOLD-PLUS-59-ENDPOINT-ANCHOR"
        and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE"
        and x.get("relation") == "DIRECT_ANCESTOR_OF"
        and x.get("status") == "UNRESOLVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("Batch 12DQ composite/Sanming direct-ancestry firewall missing")
    if not any(
        x.get("batch") == "BATCH-12-ZIWEI-DATONG-NANJING59-ENDPOINT-RECOMPOSITION-DQ"
        and "empty intersection" in x.get("update", "")
        and "zero exact-parent vote" in x.get("update", "")
        for x in hyp12dk.get("evidence_updates", [])
    ):
        fail("Batch 12DQ genealogy hypothesis endpoint-recomposition update missing")

    nlc12dr = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-NLC-TAIYIN-TONGGUI-CHENGHUA-411999012050")
    passage12dr = next(n for n in nodes if n.get("node_id") == "PASSAGE-NLC-TAIYIN-TONGGUI-CHENHUN-LICHENG")
    cii12dr = next(n for n in nodes if n.get("node_id") == "TABLE-NANJING-DATONG-DAILY-CII-N-1380S")
    if nlc12dr.get("identifier") != "411999012050 / NLC892-411999012050-103144 / NLC892-411999012050-103188":
        fail("Batch 12DR NLC physical-copy node identity regressed")
    if passage12dr.get("direct_heading") != "冬夏二至日出晨昏分立成鈐" or passage12dr.get("ocr_used_for_final_glyph_or_numeric_claims") is not False:
        fail("Batch 12DR passage heading/no-OCR control regressed")
    if passage12dr.get("direct_numeric_fingerprints", {}).get("day0", {}).get("morning_fen") != 2681.7 or passage12dr.get("direct_numeric_fingerprints", {}).get("day178", {}).get("morning_fen") != 1819.66:
        fail("Batch 12DR passage numeric fingerprints regressed")
    if cii12dr.get("direct_chinese_pre1578_physical_carrier_closed") is not True or cii12dr.get("direct_chinese_pre1578_physical_carrier") != "PHYSICAL-COPY-NLC-TAIYIN-TONGGUI-CHENGHUA-411999012050":
        fail("Batch 12DR C-II-N Chinese carrier closure regressed")
    e60 = next((e for e in edges if e.get("edge_id") == "TG-E0060"), None)
    e61 = next((e for e in edges if e.get("edge_id") == "TG-E0061"), None)
    if not e60 or e60.get("relation") != "ATTESTS" or e60.get("status") != "CONFIRMED" or e60.get("to") != "PASSAGE-NLC-TAIYIN-TONGGUI-CHENHUN-LICHENG":
        fail("Batch 12DR physical-copy attestation edge regressed")
    if not e61 or e61.get("relation") != "TRANSMITS_RULE" or e61.get("status") != "HIGH_CONFIDENCE" or e61.get("to") != "TABLE-NANJING-DATONG-DAILY-CII-N-1380S":
        fail("Batch 12DR C-II-N transmission edge regressed")
    if not any(
        x.get("from") == "PHYSICAL-COPY-NLC-TAIYIN-TONGGUI-CHENGHUA-411999012050"
        and x.get("to") == "PHYSICAL-COPY-KYUDB-TAIYIN-GK12436-15C-GABINJA"
        and x.get("relation") == "DIRECT_ANCESTOR_OF"
        and x.get("status") == "DISPROVED"
        for x in graph.get("explicit_non_edges", [])
    ):
        fail("Batch 12DR Chenghua/Sejong surviving-copy chronology non-edge missing")
    batch12dr = json.loads(BATCH_12DR.read_text(encoding="utf-8"))
    if batch12dr.get("adjudication", {}).get("chinese_pre1578_physical_carrier_for_cii_n") != "CLOSED":
        fail("Batch 12DR Chinese carrier adjudication regressed")
    if batch12dr.get("adjudication", {}).get("exact_pre1578_whole_ke_reduction_selection_rule_found") is not False or batch12dr.get("adjudication", {}).get("direct_parent_of_sanming_1578") is not False:
        fail("Batch 12DR quantization/Sanming-parent firewall regressed")
    if not any(
        x.get("batch") == "BATCH-12-ZIWEI-NLC-TAIYIN-TONGGUI-CHENGHUA-PHYSICAL-CII-N-CLOSURE-DR"
        and "Chinese pre-1578 physical carrier" in x.get("update", "")
        and "zero exact Sanming-parent vote" in x.get("update", "")
        for x in hyp12dk.get("evidence_updates", [])
    ):
        fail("Batch 12DR genealogy hypothesis Chinese-carrier update missing")

    local12ds = cii12dr.get("local_consumer_interface_after_12ds", {})
    if local12ds.get("full_morning_fraction_directly_copied_and_consumed") is not True or local12ds.get("full_evening_fraction_directly_copied_and_consumed") is not True:
        fail("Batch 12DS C-II-N full-fraction consumer-interface node regressed")
    if local12ds.get("whole_ke_reduction_attested_in_reviewed_interface") is not False or local12ds.get("nanjing_59_endpoint_binding_attested_in_reviewed_interface") is not False:
        fail("Batch 12DS C-II-N local whole-ke/endpoint firewall regressed")
    if local12ds.get("scope_limit") != "LOCAL_INTERFACE_ONLY_NOT_WHOLE_WORK_NEGATIVE":
        fail("Batch 12DS C-II-N scope firewall regressed")
    batch12ds = json.loads(BATCH_12DS.read_text(encoding="utf-8"))
    if batch12ds.get("adjudication", {}).get("local_taiyin_interface_preserves_full_fractional_fen") != "CLOSED":
        fail("Batch 12DS local fractional-consumer adjudication regressed")
    if batch12ds.get("adjudication", {}).get("exact_pre1578_whole_ke_reduction_selection_rule_found") is not False:
        fail("Batch 12DS missing whole-ke-rule firewall regressed")
    if not any(
        x.get("batch") == "BATCH-12-ZIWEI-NLC-TAIYIN-TONGGUI-CONTINUOUS-FEN-CONSUMER-INTERFACE-DS"
        and "local consumer interface" in x.get("update", "")
        and "zero exact Sanming-parent or quantization-rule vote" in x.get("update", "")
        for x in hyp12dk.get("evidence_updates", [])
    ):
        fail("Batch 12DS genealogy hypothesis interface-narrowing update missing")

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

    batch12dt = json.loads(BATCH_12DT.read_text(encoding="utf-8"))
    if batch12dt.get("adjudication", {}).get("kyudb_component_set_crosswalk") != "CLOSED":
        fail("Batch 12DT component-set adjudication regressed")
    if batch12dt.get("adjudication", {}).get("exact_1444_impression_date_for_every_surviving_component") != "UNRESOLVED":
        fail("Batch 12DT exact-date adjudication firewall regressed")
    edition12dt = next(n for n in nodes if n.get("node_id") == "EDITION-KYUDB-DATONG-LIFA-TONGGUI-GK12434-12439-GABINJA")
    if edition12dt.get("exact_set_level_impression_year_proved") is not False or len(edition12dt.get("component_identifiers", [])) != 6:
        fail("Batch 12DT aggregate edition date firewall regressed")
    e62 = next((e for e in edges if e.get("edge_id") == "TG-E0062"), None)
    if not e62 or e62.get("from") != "EDITION-KYUDB-DATONG-LIFA-TONGGUI-GK12434-12439-GABINJA" or e62.get("relation") != "EDITION_OF" or e62.get("to") != "TEXT-WORK-YUANTONG-DATONG-LIFA-TONGGUI-HONGWU17":
        fail("Batch 12DT aggregate edition/work edge regressed")
    component_nodes12dt = [
        "PHYSICAL-COPY-KYUDB-SIYU-GK12434-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-TAIYANG-GK12435-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-TAIYIN-GK12436-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-RITONGGUI-GK12437-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-JIAOSHI-GK12438-15C-GABINJA",
        "PHYSICAL-COPY-KYUDB-WUXING-GK12439-15C-GABINJA",
    ]
    for node_id in component_nodes12dt:
        if not any(e.get("from") == node_id and e.get("relation") == "PHYSICAL_COPY_OF_EDITION" and e.get("to") == "EDITION-KYUDB-DATONG-LIFA-TONGGUI-GK12434-12439-GABINJA" and e.get("status") == "HIGH_CONFIDENCE" for e in edges):
            fail(f"Batch 12DT component-set edge missing: {node_id}")
    if batch12dt.get("content_scope_firewall", {}).get("gk12436_cii_n_table_may_be_imputed_to_other_components") is not False:
        fail("Batch 12DT sibling-content imputation firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-DATONG-LIFA-TONGGUI-COMPONENT-SET-CROSSWALK-DT" and "zero whole-ke" in x.get("update", "") and "Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DT genealogy hypothesis zero-vote update missing")

    batch12du = json.loads(BATCH_12DU.read_text(encoding="utf-8"))
    if batch12du.get("adjudication", {}).get("nlc_ming_manuscript_public_reproduction_scope") != "CLOSED":
        fail("Batch 12DU physical-scope adjudication regressed")
    if batch12du.get("adjudication", {}).get("exact_pre1578_physical_copy_status") != "NOT_PROVED":
        fail("Batch 12DU Ming-date firewall regressed")
    nlc_edition12du = next(n for n in nodes if n.get("node_id") == "EDITION-NLC-DATONG-LIFA-TONGGUI-RESIDUAL-MING-MS-RECENSION")
    nlc_copy12du = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-NLC-DATONG-LIFA-TONGGUI-RESIDUAL-MING-MS")
    nlc_surrogate12du = next(n for n in nodes if n.get("node_id") == "DIGITAL-SURROGATE-XUXIU1031-NLC-DATONG-TONGGUI-RESIDUAL")
    if "三卷" not in nlc_edition12du.get("juan_count_note", ""):
        fail("Batch 12DU juan-count tension note missing")
    if nlc_copy12du.get("exact_pre1578_physical_copy_status") != "NOT_PROVED" or "p578-p622" not in nlc_copy12du.get("reproduced_scope", ""):
        fail("Batch 12DU NLC physical-scope graph boundary regressed")
    if "07348e40ec26ca38efe9c9736a69c403c61f9b07a2c89a847fc68d00ce6d8c25" not in nlc_surrogate12du.get("identifier", ""):
        fail("Batch 12DU surrogate source hash missing")
    for edge_id, rel in (("TG-E0069", "EDITION_OF"), ("TG-E0070", "PHYSICAL_COPY_OF_EDITION"), ("TG-E0071", "DIGITAL_SURROGATE_OF")):
        e = next((x for x in edges if x.get("edge_id") == edge_id), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12DU transmission edge regressed: {edge_id}")
    if batch12du.get("bibliographic_tension", {}).get("normalization_forbidden") is not True:
        fail("Batch 12DU catalog normalization firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-NLC-DATONG-LIFA-TONGGUI-XUXIU1031-PHYSICAL-SCOPE-DU" and "zero whole-ke" in x.get("update", "") and "Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DU genealogy hypothesis zero-vote update missing")

    batch12dv = json.loads(BATCH_12DV.read_text(encoding="utf-8"))
    if batch12dv.get("adjudication", {}).get("received_calendar_term_to_discrete_arrow_selection_mechanism") != "CLOSED":
        fail("Batch 12DV selection-mechanism adjudication regressed")
    if batch12dv.get("adjudication", {}).get("exact_pre1578_physical_copy_status") != "NOT_PROVED":
        fail("Batch 12DV chronology firewall regressed")
    copy12dv = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-NLC-ZHUNZHAI-JILOU-DAOGUANG3-HUANG-SHILIJU-MS")
    rule12dv = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62")
    if copy12dv.get("physical_copy_date") != "QING_DAOGUANG_3_1823" or copy12dv.get("exact_pre1578_physical_copy_status") != "NOT_PROVED":
        fail("Batch 12DV physical-copy date firewall regressed")
    if rule12dv.get("direct_arrow_count") != 25 or rule12dv.get("direct_extrema") != {"first_arrow": "38/62", "twenty_fifth_arrow": "62/38"}:
        fail("Batch 12DV rule-family mechanics regressed")
    e72 = next((e for e in edges if e.get("edge_id") == "TG-E0072"), None)
    e73 = next((e for e in edges if e.get("edge_id") == "TG-E0073"), None)
    if not e72 or e72.get("relation") != "ATTESTS" or e72.get("from") != "PHYSICAL-COPY-NLC-ZHUNZHAI-JILOU-DAOGUANG3-HUANG-SHILIJU-MS" or e72.get("to") != "RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62":
        fail("Batch 12DV ATTESTS edge regressed")
    if not e73 or e73.get("relation") != "STRUCTURAL_MECHANISM_CANDIDATE_FOR" or e73.get("status") != "POSSIBLE" or e73.get("to") != "TABLE-SANMING-1578-DAYNIGHT-KE":
        fail("Batch 12DV structural-mechanism edge regressed")
    if not any(x.get("from") == "RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12DV unchanged-table non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-XUXIU1031-ZHUNZHAI-CLEPSYDRA-JIEHOU-ARROW-SELECTION-DV" and "zero exact Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DV genealogy hypothesis zero-vote update missing")

    batch12dw = json.loads(BATCH_12DW.read_text(encoding="utf-8"))
    if batch12dw.get("adjudication", {}).get("secure_pre1578_arrow_qi_physical_witness") != "CLOSED":
        fail("Batch 12DW secure pre-1578 arrow/qi adjudication regressed")
    copy12dw = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-YONEZAWA-SHILIN-AA060-HONGZHI5-1492")
    rule12dw = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-SHILIN-48ARROW-24QI-40-60")
    if copy12dw.get("physical_copy_date") != "MING_HONGZHI_5_1492_PRINT_AS_CATALOGUED" or copy12dw.get("secure_pre1578_physical_witness") is not True:
        fail("Batch 12DW physical-copy chronology regressed")
    if rule12dw.get("direct_arrow_count") != 48 or rule12dw.get("direct_qi_count") != 24 or rule12dw.get("direct_arrows_per_qi") != 2:
        fail("Batch 12DW 48-arrow/24-qi mechanics regressed")
    if rule12dw.get("direct_extrema") != {"winter_solstice": "40/60", "summer_solstice": "60/40", "equinox": "50/50"}:
        fail("Batch 12DW 40/60 extrema control regressed")
    e74 = next((e for e in edges if e.get("edge_id") == "TG-E0074"), None)
    e75 = next((e for e in edges if e.get("edge_id") == "TG-E0075"), None)
    if not e74 or e74.get("relation") != "ATTESTS" or e74.get("from") != "PHYSICAL-COPY-YONEZAWA-SHILIN-AA060-HONGZHI5-1492" or e74.get("to") != "RULE-FAMILY-SHILIN-48ARROW-24QI-40-60":
        fail("Batch 12DW ATTESTS edge regressed")
    if not e75 or e75.get("relation") != "STRUCTURAL_MECHANISM_CANDIDATE_FOR" or e75.get("status") != "POSSIBLE" or e75.get("to") != "TABLE-SANMING-1578-DAYNIGHT-KE":
        fail("Batch 12DW structural-mechanism edge regressed")
    if not any(x.get("from") == "RULE-FAMILY-SHILIN-48ARROW-24QI-40-60" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12DW unchanged-table non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-YONEZAWA-SHILIN1492-LIKOU-48ARROW-24QI-PHYSICAL-CLOSURE-DW" and "zero exact Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DW genealogy hypothesis zero-vote update missing")

    batch12dx = json.loads(BATCH_12DX.read_text(encoding="utf-8"))
    if batch12dx.get("adjudication", {}).get("secure_pre1578_physical_louke_witness") != "CLOSED":
        fail("Batch 12DX secure pre-1578 Sui Shu witness regressed")
    copy12dx = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-NAJDA-SUISHU-280-0071-YUAN")
    huo12dx = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-SUISHU-HUORONG-48ARROW-2DU4FEN")
    yuan12dx = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-SUISHU-YUANCHONG-19DAY-CHANGE-ARROW-40-60")
    liu12dx = next(n for n in nodes if n.get("node_id") == "TABLE-SUISHU-LIUZHUO-HUANGJI-24QI-59_86-40_14")
    if copy12dx.get("secure_pre1578_physical_witness") is not True or "YUAN_DYNASTY" not in copy12dx.get("physical_copy_date", ""):
        fail("Batch 12DX physical-copy chronology regressed")
    if huo12dx.get("direct_arrow_count") != 48 or huo12dx.get("direct_change_threshold") != "2 du 4 fen -> 1 ke":
        fail("Batch 12DX Huo Rong graph mechanics regressed")
    if yuan12dx.get("direct_summer_endpoint") != "60/40" or yuan12dx.get("direct_reviewed_change_interval_days") != 19:
        fail("Batch 12DX Yuan Chong graph mechanics regressed")
    if liu12dx.get("direct_qi_count") != 24 or liu12dx.get("direct_solstitial_values") != {"long_side": "59.86", "short_side": "40.14"} or liu12dx.get("actual_clepsydra_use") is not False:
        fail("Batch 12DX Liu Zhuo graph mechanics/non-use regressed")
    for eid, rel in (("TG-E0076","ATTESTS"),("TG-E0077","ATTESTS"),("TG-E0078","ATTESTS"),("TG-E0079","STRUCTURAL_MECHANISM_CANDIDATE_FOR"),("TG-E0080","SYNTHESIS_COMPONENT_CANDIDATE_FOR")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12DX transmission edge regressed: {eid}")
    if not any(x.get("from") == "TABLE-SUISHU-LIUZHUO-HUANGJI-24QI-59_86-40_14" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12DX unchanged-table non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-NAJDA-SUISHU-YUAN-LOUKE-48ARROW-HUANGJI5986-PHYSICAL-CLOSURE-DX" and "zero exact Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DX genealogy hypothesis zero-vote update missing")

    batch12dy = json.loads(BATCH_12DY.read_text(encoding="utf-8"))
    if batch12dy.get("adjudication", {}).get("pre1578_multisource_local_calibration_proposal") != "CLOSED":
        fail("Batch 12DY proposal closure regressed")
    passage12dy = next(n for n in nodes if n.get("node_id") == "PASSAGE-WUZONG169-ZHUYU-CALIBRATION-PROPOSAL-1518")
    rule12dy = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-MING-QINTIANJIAN-MULTISOURCE-LOCAL-CALIBRATION-PROPOSAL-1518")
    if passage12dy.get("proposal_status") != "SUBMITTED_AND_REVIEWED_NOT_PROVED_ADOPTED_OR_EXECUTED":
        fail("Batch 12DY passage proposal-status firewall regressed")
    if rule12dy.get("adopted_or_executed") is not False or rule12dy.get("direct_59_numeral") is not False or rule12dy.get("direct_whole_ke_reduction_rule") is not False:
        fail("Batch 12DY rule-family adoption/numeric firewall regressed")
    for eid, rel in (("TG-E0081","ATTESTS"),("TG-E0082","ATTESTS"),("TG-E0083","PARALLEL_COEXISTS_WITH")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12DY transmission edge regressed: {eid}")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-WUZONG-SHILU-1518-MULTISOURCE-LOCAL-CALIBRATION-PROPOSAL-DY" and "zero exact Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DY genealogy hypothesis zero-vote update missing")

    batch12dz = json.loads(BATCH_12DZ.read_text(encoding="utf-8"))
    if batch12dz.get("adjudication", {}).get("kyoto_received_whole_ke_table_physical_attestation") != "CLOSED":
        fail("Batch 12DZ Kyoto physical table closure regressed")
    copy12dz = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-LANPEN-KYOTO-RB00017646")
    table12dz = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-LANPEN-JINGFUDIAN-WHOLEKE-40-60")
    col12dz = next(n for n in nodes if n.get("node_id") == "PASSAGE-LANPEN-KYOTO-1716-SONG-PRINT-COLLATION-COLOPHON")
    if copy12dz.get("physical_copy_date") != "UNRESOLVED_MANUSCRIPT":
        fail("Batch 12DZ Kyoto physical-copy chronology firewall regressed")
    if table12dz.get("direct_yushui_bucket") != "46/54 @ 雨水後四日至後九日" or table12dz.get("terminal_summer_cap") != "60/40" or table12dz.get("contains_59_41") is not True:
        fail("Batch 12DZ Kyoto whole-ke table mechanics regressed")
    if "宋刻古本" not in "".join(col12dz.get("direct_text", ())):
        fail("Batch 12DZ Song-print collation passage regressed")
    for eid, rel in (("TG-E0084","ATTESTS"),("TG-E0085","ATTESTS"),("TG-E0086","STRUCTURAL_ANCESTRY_CANDIDATE_FOR")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12DZ transmission edge regressed: {eid}")
    if not any(x.get("from") == "RULE-FAMILY-LANPEN-JINGFUDIAN-WHOLEKE-40-60" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12DZ Sanming unchanged-table non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-LANPEN-KYOTO-40-60-PHYSICAL-AND-HUQIAN-COPY-CONTROL-DZ" and "Zero exact Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12DZ genealogy hypothesis zero-vote update missing")


    batch12ea = json.loads(BATCH_12EA.read_text(encoding="utf-8"))
    if batch12ea.get("adjudication", {}).get("pre1578_physical_base100_halfup_rule") != "CLOSED":
        fail("Batch 12EA pre-1578 half-up rule closure regressed")
    copy12ea = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-JIUTANGSHU-NCL01535-JIAJING17-1538")
    rule12ea = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-JIUTANGSHU-GUILOU-BASE100-HALFUP")
    if copy12ea.get("secure_pre1578_physical_witness") is not True or copy12ea.get("physical_copy_date") != "MING_JIAJING_17_1538_PRINT_AS_CATALOGUED":
        fail("Batch 12EA physical chronology control regressed")
    if rule12ea.get("direct_base_denominator") != 100 or rule12ea.get("direct_guilou_extension") is not True or rule12ea.get("global_cii_n_interior_mapping") is not False:
        fail("Batch 12EA rule-family mechanical firewall regressed")
    for eid, rel in (("TG-E0087","ATTESTS"),("TG-E0088","SYNTHESIS_COMPONENT_CANDIDATE_FOR")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12EA transmission edge regressed: {eid}")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-JIUTANGSHU-JIAJING17-GUILOU-HALFUP-ROUNDING-EA" and "Zero exact Sanming-parent vote" in x.get("update", "") for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EA genealogy hypothesis zero-vote update missing")

    batch12eb = json.loads(BATCH_12EB.read_text(encoding="utf-8"))
    if batch12eb.get("adjudication", {}).get("direct_physical_datong_endpoint_binding") != "CLOSED_FOR_REVIEWED_MING_NLC_OBJECT":
        fail("Batch 12EB endpoint-binding closure regressed")
    copy12eb = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-XINGYUNLU-NLC371920-MING-WANLI")
    rule12eb = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-XINGYUNLU-DATONG-ENDPOINT-FEN-TO-59_41")
    if copy12eb.get("secure_pre1578_physical_witness") is not False or copy12eb.get("physical_copy_date") != "UNRESOLVED_WITHIN_MING_WANLI_RANGE":
        fail("Batch 12EB chronology firewall regressed")
    if rule12eb.get("direct_summer_sunrise_fen") != "2068.30" or rule12eb.get("direct_winter_sunrise_fen") != "2931.70" or rule12eb.get("direct_summer_day_night") != "59/41":
        fail("Batch 12EB endpoint mechanics regressed")
    for eid, rel in (("TG-E0089","ATTESTS"),("TG-E0090","STRUCTURAL_MECHANISM_CANDIDATE_FOR")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12EB transmission edge regressed: {eid}")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-XINGYUNLU-DATONG-ENDPOINT-BINDING-EB" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EB genealogy hypothesis zero-vote update missing")

    batch12ec = json.loads(BATCH_12EC.read_text(encoding="utf-8"))
    ad12ec = batch12ec.get("adjudication", {})
    if ad12ec.get("direct_physical_term_threshold_and_wholeke_coexistence") != "CLOSED_FOR_REVIEWED_NCL06627_TEXT_STATE":
        fail("Batch 12EC compound architecture regressed")
    if ad12ec.get("sanming_exact_change_day_fingerprint_match") is not False or ad12ec.get("secure_pre1578_binding_witness") is not False:
        fail("Batch 12EC fingerprint/chronology firewall regressed")
    copy12ec = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-DATONGLIZHU-NCL06627-MING-MANUSCRIPT")
    rule12ec = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE")
    if copy12ec.get("secure_pre1578_physical_witness") is not False or copy12ec.get("physical_copy_date") != "MING_MANUSCRIPT_EXACT_DATE_UNRESOLVED":
        fail("Batch 12EC physical chronology control regressed")
    if rule12ec.get("direct_summer_day_night") != "59/41" or rule12ec.get("threshold_proved_as_wholeke_operator") is not False or rule12ec.get("exact_sanming_yueling_fingerprint") is not False:
        fail("Batch 12EC rule-family firewall regressed")
    for eid, rel in (("TG-E0091","ATTESTS"),("TG-E0092","STRUCTURAL_MECHANISM_CANDIDATE_FOR")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12EC transmission edge regressed: {eid}")
    if not any(x.get("from") == "RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12EC unchanged-table non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-NCL06627-DATONGLIZHU-THRESHOLD-FINGERPRINT-EC" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EC genealogy hypothesis zero-vote update missing")

    batch12ed = json.loads(BATCH_12ED.read_text(encoding="utf-8"))
    ad12ed = batch12ed.get("adjudication", {})
    if ad12ed.get("shared_datonglizhu_threshold_architecture") != "CLOSED_FOR_REVIEWED_KYUDB_OBJECT":
        fail("Batch 12ED Kyudb threshold architecture regressed")
    if ad12ed.get("dahan_day13_to_44_56_convergence") is not True or ad12ed.get("rainwater_exact_sanming_fingerprint_match") is not False:
        fail("Batch 12ED partial-convergence firewall regressed")
    if ad12ed.get("secure_pre1578_binding_witness") is not False or ad12ed.get("direct_sanming_parent_vote_increment") != 0:
        fail("Batch 12ED chronology firewall regressed")
    copy12ed = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02426-GWANSANGGAM-WOODTYPE")
    rule12ed = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE")
    if copy12ed.get("secure_pre1578_physical_witness") is not False or copy12ed.get("physical_copy_date") != "UNRESOLVED_KYUDB_CATALOG_KANEN_MISHO":
        fail("Batch 12ED physical chronology control regressed")
    if rule12ed.get("direct_rainwater_47_53_timing") != "後六日" or rule12ed.get("direct_dahan_44_56_timing") != "後十三日" or rule12ed.get("exact_sanming_yueling_fingerprint") is not False:
        fail("Batch 12ED rule-family fingerprint control regressed")
    for eid, rel in (("TG-E0093","ATTESTS"),("TG-E0094","SHARED_COMMON_ANCESTOR_CANDIDATE")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12ED transmission edge regressed: {eid}")
    if not any(x.get("from") == "RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12ED Sanming unchanged-table non-edge missing")
    if not any(x.get("from") == "RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "RULE-FAMILY-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12ED NCL-recension unchanged-identity non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-DATONGLIZHU-GK02426-PARTIAL-FINGERPRINT-ED" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12ED genealogy hypothesis zero-vote update missing")

    batch12ee = json.loads(BATCH_12EE.read_text(encoding="utf-8"))
    ad12ee = batch12ee.get("adjudication", {})
    if ad12ee.get("direct_1434_type_event_statement") != "CLOSED_FOR_ATTACHED_POSTFACE_TEXT":
        fail("Batch 12EE direct postface closure regressed")
    if ad12ee.get("rainwater_exact_sanming_fingerprint_match") is not False or ad12ee.get("dahan_exact_sanming_fingerprint_match") is not False:
        fail("Batch 12EE exact-fingerprint firewall regressed")
    if ad12ee.get("secure_pre1578_binding_witness") is not False or ad12ee.get("direct_sanming_parent_vote_increment") != 0:
        fail("Batch 12EE chronology/lineage firewall regressed")
    copy12ee = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02538-GWANSANGGAM-MOVABLETYPE")
    rule12ee = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-KYUDB-DATONGLIZHU-GK02538-TERM-THRESHOLD-WHOLEKE-SCHEDULE")
    if copy12ee.get("physical_copy_date") != "UNRESOLVED_KYUDB_CATALOG_KANEN_MISHO" or copy12ee.get("secure_pre1578_physical_witness") is not False or copy12ee.get("direct_1434_type_event_postface") is not True:
        fail("Batch 12EE physical chronology control regressed")
    if rule12ee.get("direct_rainwater_47_53_timing") != "後五六日" or rule12ee.get("direct_rainwater_48_52_timing") != "後十三四日" or rule12ee.get("direct_dahan_44_56_timing") != "後十三四日" or rule12ee.get("exact_sanming_yueling_fingerprint") is not False:
        fail("Batch 12EE rule-family fingerprint control regressed")
    for eid, rel in (("TG-E0095","ATTESTS"),("TG-E0096","SHARED_COMMON_ANCESTOR_CANDIDATE")):
        e = next((x for x in edges if x.get("edge_id") == eid), None)
        if not e or e.get("relation") != rel:
            fail(f"Batch 12EE transmission edge regressed: {eid}")
    if not any(x.get("from") == "RULE-FAMILY-KYUDB-DATONGLIZHU-GK02538-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "TABLE-SANMING-1578-DAYNIGHT-KE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12EE Sanming unchanged-table non-edge missing")
    if not any(x.get("from") == "RULE-FAMILY-KYUDB-DATONGLIZHU-GK02538-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("relation") == "DIRECT_UNCHANGED_TABLE_IDENTITY_WITH" and x.get("to") == "RULE-FAMILY-KYUDB-DATONGLIZHU-TERM-THRESHOLD-WHOLEKE-SCHEDULE" and x.get("status") == "DISPROVED" for x in graph.get("explicit_non_edges", [])):
        fail("Batch 12EE GK02426 unchanged-identity non-edge missing")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-DATONGLIZHU-GK02538-1434-TYPE-POSTFACE-AND-FINGERPRINT-EE" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EE genealogy hypothesis zero-vote update missing")


    if copy12ee.get("terminal_internal_date_line") != "正統七年十二月日" or copy12ee.get("terminal_internal_date_gregorian_year") != 1442:
        fail("Batch 12EF GK02538 terminal chronology node regressed")
    if copy12ee.get("terminal_textual_layer_terminus_post_quem_year") != 1442 or copy12ee.get("explicit_yinchū_marker_adjacent_to_terminal_date") is not False:
        fail("Batch 12EF textual-terminus / 印出 firewall regressed")
    if copy12ee.get("exact_impression_year_adjudicated") is not False or copy12ee.get("physical_copy_date") != "UNRESOLVED_KYUDB_CATALOG_KANEN_MISHO":
        fail("Batch 12EF exact-impression firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-DATONGLIZHU-GK02538-1442-TERMINAL-DATE-IMPRESSION-FIREWALL-EF" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EF genealogy hypothesis zero-vote update missing")


    if copy12ee.get("gwansanggam_type_category_unique_1434_event") is not False:
        fail("Batch 12EG Gwansanggam type-category node firewall regressed")
    if copy12ee.get("inherited_original_imprint_can_survive_later_reprint") is not True or copy12ee.get("internal_date_or_imprint_alone_dates_current_copy") is not False:
        fail("Batch 12EG inherited-colophon node firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-DATONGLIZHU-GK02538-GWANSANGGAM-TYPE-CATEGORY-AND-INHERITED-COLOPHON-CONTROL-EG" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EG genealogy hypothesis zero-vote update missing")


    if copy12ee.get("dated_inryeokja_physical_comparators_acquired") is not True:
        fail("Batch 12EH dated-comparator node control regressed")
    if copy12ee.get("annual_calendar_layout_is_copy_dating_operator") is not False or copy12ee.get("gwansanggam_specific_subtype") != "UNRESOLVED" or copy12ee.get("casting_generation") != "UNRESOLVED":
        fail("Batch 12EH type-subtype/copy-dating node firewall regressed")
    if copy12ee.get("shared_glyph_identity_control_status") != "NOT_YET_CLOSED":
        fail("Batch 12EH shared-glyph gate regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-DATED-INRYEOKJA-PHYSICAL-COMPARATOR-AND-SUBTYPE-FIREWALL-EH" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EH genealogy hypothesis zero-vote update missing")


    if abs(copy12ee.get("gk02538_nominal_vertical_slot_pitch_cm", 0) - 1.204761905) > 1e-8:
        fail("Batch 12EI GK02538 nominal type-slot scale regressed")
    if copy12ee.get("type_body_scale_compatibility_status") != "SUPPORTED_NOMINAL_VERTICAL_SCALE_ONLY":
        fail("Batch 12EI type-body scale compatibility node missing")
    if copy12ee.get("direct_glyph_body_measurement_performed") is not False or copy12ee.get("scale_compatibility_proves_same_casting_generation") is not False:
        fail("Batch 12EI scale-to-casting firewall regressed")
    if copy12ee.get("gwansanggam_specific_subtype") != "UNRESOLVED" or copy12ee.get("casting_generation") != "UNRESOLVED" or copy12ee.get("shared_glyph_identity_control_status") != "NOT_YET_CLOSED":
        fail("Batch 12EI unresolved subtype/shared-glyph gate regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-INRYEOKJA-BODY-SCALE-COMPATIBILITY-AND-CASTING-FIREWALL-EI" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EI genealogy hypothesis zero-vote update missing")
    batch12ei = json.loads(BATCH_12EI.read_text(encoding="utf-8"))
    impact12ei = batch12ei.get("transmission_impact", {})
    if "PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02538-GWANSANGGAM-MOVABLETYPE" not in impact12ei.get("nodes_strengthened", []):
        fail("Batch 12EI transmission impact node strengthening missing")
    if impact12ei.get("edges_supported") != []:
        fail("Batch 12EI unexpectedly closed a transmission edge")


    if copy12ee.get("title_string_implies_daetongryokja_subtype") is not False:
        fail("Batch 12EJ title-to-Daetongryokja node firewall regressed")
    if copy12ee.get("kasi_1997_bibliographic_label") != "大統曆註（觀象監活字）" or copy12ee.get("kasi_1997_table_membership_proves_sejong_impression") is not False:
        fail("Batch 12EJ KASI bibliography node control regressed")
    if copy12ee.get("daetongryokja_name_is_title_identity_rule") is not False:
        fail("Batch 12EJ type-name identity firewall regressed")
    if copy12ee.get("gwansanggam_specific_subtype") != "UNRESOLVED" or copy12ee.get("casting_generation") != "UNRESOLVED":
        fail("Batch 12EJ unresolved subtype/casting gate regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-DAETONGLYOKJA-NAME-SCOPE-AND-SEJONG-LIST-FIREWALL-EJ" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EJ genealogy hypothesis zero-vote update missing")
    batch12ej = json.loads(BATCH_12EJ.read_text(encoding="utf-8"))
    impact12ej = batch12ej.get("transmission_impact", {})
    if "PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02538-GWANSANGGAM-MOVABLETYPE" not in impact12ej.get("nodes_strengthened", []):
        fail("Batch 12EJ transmission impact node strengthening missing")
    if impact12ej.get("edges_supported") != []:
        fail("Batch 12EJ unexpectedly closed a positive transmission edge")


    if copy12ee.get("shared_glyph_crop_control_status") != "CLOSED_SOURCE_BOUND_FIXED_PIXEL_CROPS":
        fail("Batch 12EK shared-glyph crop node status regressed")
    if copy12ee.get("shared_glyph_manual_set") != ["正", "月"]:
        fail("Batch 12EK shared-glyph manual set regressed")
    if copy12ee.get("shared_glyph_probe_artifact_id") != 10671595229 or copy12ee.get("gyeongjin1580_shared_glyph_size_class_binding") != "UNRESOLVED":
        fail("Batch 12EK artifact/size-class node firewall regressed")
    if copy12ee.get("shared_glyph_visual_resemblance_or_difference_proves_casting_generation") is not False or copy12ee.get("shared_glyph_identity_control_status") != "NOT_YET_CLOSED":
        fail("Batch 12EK visual-form/casting firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-GYEONGJIN1580-SOURCE-BOUND-SHARED-GLYPH-CROPS-EK" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EK genealogy hypothesis zero-vote update missing")
    batch12ek = json.loads(BATCH_12EK.read_text(encoding="utf-8"))
    impact12ek = batch12ek.get("transmission_impact", {})
    if impact12ek.get("edges_supported") != []:
        fail("Batch 12EK unexpectedly closed a transmission edge")

    if copy12ee.get("gyeongjin1580_12el_original_size_class_binding") != "MEDIUM_INRYEOKJA_CLASS_SUPPORTED_AT_OBJECT_LAYOUT_LEVEL":
        fail("Batch 12EL original Gyeongjin medium-class inference was not preserved")
    if copy12ee.get("gyeongjin1580_shared_glyph_size_class_binding") != "OBJECT_SPECIFIC_MONTH_NAME_HEADING_正/月_APPROX_1.4W_X_1.2H_CM; 大_SAME_VISIBLE_HEADING_CLASS_ONLY":
        fail("Batch 12EO object-specific Gyeongjin target binding regressed")
    if copy12ee.get("same_size_class_shared_glyph_control_status") != "CLOSED_NOMINAL_VERTICAL_1.2CM_LEVEL_ONLY":
        fail("Batch 12EO vertical-only shared-glyph gate refinement regressed")
    if copy12ee.get("physical_scale_normalized_shared_glyph_form_comparison_status") != "NOT_YET_CLOSED":
        fail("Batch 12EL physical-scale normalization firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-GYEONGJIN1580-MEDIUM-SIZECLASS-BINDING-EL" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EL genealogy hypothesis zero-vote update missing")
    batch12el = json.loads(BATCH_12EL.read_text(encoding="utf-8"))
    impact12el = batch12el.get("transmission_impact", {})
    if impact12el.get("edges_supported") != []:
        fail("Batch 12EL unexpectedly closed a transmission edge")

    if copy12ee.get("medium_normalized_shared_glyph_manual_set") != ["正","月","大"]:
        fail("Batch 12EM graph manual glyph set regressed")
    if copy12ee.get("medium_normalized_probe_artifact_id") != 10671577720 or copy12ee.get("nominal_vertical_pitch_normalized_three_glyph_corpus_status") != "CLOSED_SOURCE_HASH_BOUND":
        fail("Batch 12EM graph artifact/corpus status regressed")
    if copy12ee.get("normalized_three_glyph_form_divergence_observed") is not True or copy12ee.get("normalized_form_divergence_proves_different_casting_generation") is not False:
        fail("Batch 12EM graph form-divergence firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-GYEONGJIN1580-NOMINAL-PHYSICAL-SCALE-THREE-GLYPH-COMPARISON-EM" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EM genealogy hypothesis zero-vote update missing")
    batch12em = json.loads(BATCH_12EM.read_text(encoding="utf-8"))
    impact12em = batch12em.get("transmission_impact", {})
    if impact12em.get("edges_supported") != []:
        fail("Batch 12EM unexpectedly closed a transmission edge")

    if copy12ee.get("dated_inryeokja_three_way_manual_set") != ["正","月","大"]:
        fail("Batch 12EN graph manual glyph set regressed")
    if copy12ee.get("dated_inryeokja_three_way_probe_artifact_id") != 10672460495 or copy12ee.get("dated_inryeokja_three_way_corpus_status") != "CLOSED_SOURCE_HASH_BOUND":
        fail("Batch 12EN graph artifact/corpus status regressed")
    if "NOT_INDEPENDENTLY_CLOSED" not in copy12ee.get("ryu1604_shared_glyph_size_class_binding", ""):
        fail("Batch 12EN graph 1604 size-class firewall regressed")
    if copy12ee.get("dated_inryeokja_category_level_form_variation_observed") is not True:
        fail("Batch 12EN graph dated-control variation status regressed")
    if copy12ee.get("dated_inryeokja_visual_nearest_neighbor_proves_casting_generation") is not False or copy12ee.get("dated_inryeokja_visual_nearest_neighbor_proves_impression_date") is not False:
        fail("Batch 12EN graph visual nearest-neighbor firewall regressed")
    if copy12ee.get("shared_glyph_identity_control_status") != "NOT_YET_CLOSED" or copy12ee.get("physical_scale_normalized_shared_glyph_form_comparison_status") != "NOT_YET_CLOSED":
        fail("Batch 12EN unresolved identity/physical-scale firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-DATED-INRYEOKJA-THREE-WAY-FORM-VARIATION-FIREWALL-EN" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EN genealogy hypothesis zero-vote update missing")
    batch12en = json.loads(BATCH_12EN.read_text(encoding="utf-8"))
    impact12en = batch12en.get("transmission_impact", {})
    if impact12en.get("edges_supported") != []:
        fail("Batch 12EN unexpectedly closed a transmission edge")

    if copy12ee.get("gyeongjin1580_object_specific_month_name_heading_size_cm_width_height") != [1.4,1.2]:
        fail("Batch 12EO graph month-heading measurement regressed")
    if copy12ee.get("gyeongjin1580_four_size_scheme_cm_width_height") != [[1.4,1.2],[1.0,0.9],[0.7,0.6],[0.3,0.3]]:
        fail("Batch 12EO graph four-size scheme regressed")
    if copy12ee.get("gyeongjin1580_target_medium_size_class_supported") is not False or copy12ee.get("gk02538_to_gyeongjin1580_width_equivalence_proven") is not False:
        fail("Batch 12EO graph generic-medium/width firewall regressed")
    if copy12ee.get("gk02538_to_gyeongjin1580_month_heading_vertical_delta_pct") != 0.396825:
        fail("Batch 12EO graph vertical delta regressed")
    if copy12ee.get("physical_scale_normalized_shared_glyph_form_comparison_status") != "NOT_YET_CLOSED" or copy12ee.get("shared_glyph_identity_control_status") != "NOT_YET_CLOSED":
        fail("Batch 12EO graph unresolved full-scale/identity firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-GYEONGJIN1580-OBJECT-SPECIFIC-FOUR-SIZE-CALIBRATION-EO" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EO genealogy hypothesis zero-vote update missing")
    batch12eo = json.loads(BATCH_12EO.read_text(encoding="utf-8"))
    impact12eo = batch12eo.get("transmission_impact", {})
    if impact12eo.get("edges_supported") != []:
        fail("Batch 12EO unexpectedly closed a transmission edge")

    if copy12ee.get("imjin_calendar_apparatus_loss_or_dispersal_attested") is not True or copy12ee.get("imjin_calendar_cast_type_recovery_attested") is not True:
        fail("Batch 12EP graph wartime loss/recovery controls regressed")
    if copy12ee.get("prewar_postwar_physical_sort_stock_status") != "UNRESOLVED_PARTIAL_RECOVERY_ATTESTED":
        fail("Batch 12EP graph continuity status regressed")
    if copy12ee.get("prewar_postwar_complete_sort_continuity_proven") is not False or copy12ee.get("prewar_postwar_complete_sort_discontinuity_proven") is not False:
        fail("Batch 12EP graph two-sided continuity firewall regressed")
    if copy12ee.get("ryu_series_1594_woodblock_control") is not True or copy12ee.get("ryu_series_1596_1597_1604_1606_metal_inryeokja_control") is not True:
        fail("Batch 12EP graph Ryu media controls regressed")
    if copy12ee.get("ryu1604_same_casting_generation_as_gyeongjin1580_proven") is not False or copy12ee.get("visual_nearest_neighbor_across_imjin_boundary_is_dating_operator") is not False:
        fail("Batch 12EP graph casting/dating firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-KYUDB-GK02538-IMJIN-TYPE-LOSS-RECOVERY-CONTINUITY-FIREWALL-EP" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EP genealogy hypothesis zero-vote update missing")
    batch12ep = json.loads(BATCH_12EP.read_text(encoding="utf-8"))
    impact12ep = batch12ep.get("transmission_impact", {})
    if impact12ep.get("edges_supported") != []:
        fail("Batch 12EP unexpectedly closed a transmission edge")

    zhun_phys12eq = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-NLC-ZHUNZHAI-JILOU-DAOGUANG3-HUANG-SHILIJU-MS")
    zhun_rule12eq = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62")
    if zhun_phys12eq.get("pre1578_title_family_catalog_attestation_status") != "CLOSED_AT_1441_CATALOG_TEXT_LAYER":
        fail("Batch 12EQ graph title-family chronology regressed")
    if zhun_phys12eq.get("pre1578_exact_25arrow_rule_text_status") != "NOT_CLOSED" or zhun_phys12eq.get("exact_pre1578_physical_copy_status") != "NOT_PROVED":
        fail("Batch 12EQ graph physical/rule-text firewall regressed")
    if zhun_rule12eq.get("pre1578_title_family_catalog_year") != 1441 or zhun_rule12eq.get("pre1578_catalog_title") != "準齋九漏新式":
        fail("Batch 12EQ graph catalog title control regressed")
    if zhun_rule12eq.get("catalog_title_variant_exact_identity_proven") is not False or zhun_rule12eq.get("pre1578_exact_25arrow_rule_text_status") != "NOT_CLOSED":
        fail("Batch 12EQ graph title-identity/rule-text firewall regressed")
    if zhun_rule12eq.get("secure_pre1578_physical_witness") is not False or zhun_rule12eq.get("pre1578_catalog_attestation_proves_rule_parameters") is not False:
        fail("Batch 12EQ graph pre1578 physical/parameter firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-WENYUANGE1441-ZHUNZHAI-TITLE-EXISTENCE-CHRONOLOGY-FIREWALL-EQ" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12EQ genealogy hypothesis zero-vote update missing")
    batch12eq = json.loads(BATCH_12EQ.read_text(encoding="utf-8"))
    impact12eq = batch12eq.get("transmission_impact", {})
    if impact12eq.get("edges_supported") != []:
        fail("Batch 12EQ unexpectedly closed a transmission edge")

    zhun_phys12er = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-NLC-ZHUNZHAI-JILOU-DAOGUANG3-HUANG-SHILIJU-MS")
    zhun_rule12er = next(n for n in nodes if n.get("node_id") == "RULE-FAMILY-ZHUNZHAI-25ARROW-JIEHOU-SELECTION-38-62")
    if zhun_phys12er.get("yuan_composition_hypothesis_status") != "STRONGLY_CORROBORATED_NOT_PRIMARY_COLOPHON_CLOSED":
        fail("Batch 12ER graph Yuan composition hypothesis regressed")
    if zhun_phys12er.get("yanling_sun_fengji_1281_identity_with_zhunzhai_author") != "POSSIBLE_NOT_PROVED":
        fail("Batch 12ER graph author-identity firewall regressed")
    match12er = zhun_rule12er.get("first_arrow_cross_witness_match", {})
    if match12er.get("exact_range_and_value_match") is not True:
        fail("Batch 12ER graph first-arrow cross-witness match regressed")
    if zhun_rule12er.get("received_song_attribution_controls_composition_date") is not False or zhun_rule12er.get("pre1578_exact_25arrow_rule_text_status") != "NOT_CLOSED":
        fail("Batch 12ER graph attribution/rule-text firewall regressed")
    if not any(x.get("batch") == "BATCH-12-ZIWEI-ZHUNZHAI-YUAN-SHOUSHI-COMPOSITION-ATTRIBUTION-FIREWALL-ER" and "zero exact sanming-parent vote" in x.get("update", "").lower() for x in hyp12dk.get("evidence_updates", [])):
        fail("Batch 12ER genealogy hypothesis zero-vote update missing")
    batch12er = json.loads(BATCH_12ER.read_text(encoding="utf-8"))
    impact12er = batch12er.get("transmission_impact", {})
    if impact12er.get("edges_supported") != []:
        fail("Batch 12ER unexpectedly closed a transmission edge")

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
