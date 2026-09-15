from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-CJ"
PREV_ID = "BATCH-12-ZIWEI-SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-CI"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-CJ.md"
RESEARCH = "docs/research/ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-R1.json"
CADAL_SOURCE_ID = "EXT-CADAL-HUQIANJING-SIKU-CHUANJIAN"
TIANYIGE_SOURCE_ID = "EXT-TIANYIGE-HUQIANJING-MING-CHUANJIAN"

CADAL_RUN = 34933201296
CADAL_JOB = 104265544592
CADAL_ARTIFACT = 10382093979
CADAL_ARTIFACT_DIGEST = "sha256:7e5eeffd870581275a9e4968bb5061ae864142ad1e3dcdaac80068702c611eac"
CADAL_DJVU_SHA256 = "287547b1867829d35a6c788f20e73714b1fbce80e4c81717b0fb2eaa6a3e2707"
CADAL_PDF_SHA256 = "e6e191136e71a4bb2d2e6f1fc220830a5863c8c89c12ddf09b4aa6d8ffcb381d"
CADAL_PAGE_SHA256 = {
    "14": "02708ac131649012a2c592eb2cc4fc36b00a3d5f841753eee9a76b0cbf942107",
    "15": "b6381ac14f6479163b2c2a10ac59b2c6f773aac44c613818eab950ff50402883",
    "16": "e1fcd26c6d2749c0d627204c00fda4a3cdcb90525095b6cb380bb6642d61b0ef",
    "17": "92a8c982afded23778dea7f8ea32f801825bd783514208dfc11d94a1ef4ff6f5",
    "18": "b28425179b226185a86c24ce1ae12bdf2794c7b1315390ced165242b2b675182",
    "19": "bdabbc178705bd7ae4e456ec7a61a09085ffe10baa516f00f1d66c5747d30b6a",
    "20": "88eaa969c8508a00e71f0ce83d253475b4f3e5f42fd98ee450d825440ef5a96f",
    "21": "18f24f70e5f625be7436e52935ffd2acbc2e3868ff61fc27339fa77d85bf3df6",
    "22": "e95bef773ac636d7cbd9ffeff31029705c393412780beb1b470f6a412da7d1a3",
    "23": "e68a844791550da54f8af6ad7ed65d4d4fecbd4f98ef88f87bc9dd4749b61029",
}
TIANYIGE_RUN = 34832306143
TIANYIGE_ARTIFACT = 10342711240
TIANYIGE_ARTIFACT_DIGEST = "sha256:87bd11223e5fdbfe1ec79b2bc4e2a7577fbe459559e0386287c96f3074f2f27d"
TIANYIGE_PAGE_SHA256 = {
    "74": "a86cade9b99ed1b5cc943370e4b66e914d7968bc08943225bb99530fb15721ab",
    "75": "cc7546f4d93b85fb0327e30cead9c994ae017d81dc2f1dd1b86e994babb3cf83",
    "76": "2136201c372c0f8ea51dce46c1babcfc135758a98c775afa52c09c39fc8d5534",
    "77": "802b1bf753163ffe99daafb357201d89d1211463c5a2407031aa3f035f65cd6e",
    "78": "6660683f3a6b3dde0423bdacf7689fd62cd51c53e5bcd77c8f237fa152530cd6",
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CI tail in continuity verifier")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch doc")
    p.write_text(s, encoding="utf-8")


def correct_prior_research_text() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-CI.md")
    s = p.read_text(encoding="utf-8")
    old = "audit the near-contemporary `《虎鈐經》傳箭` integer 48-arrow system as a separate Song operational lineage"
    new = "audit the near-contemporary `《虎鈐經》傳箭` 20-number arrow cycle, reused across opposite half-year directions, as a separate Song operational lineage"
    if old in s:
        s = s.replace(old, new, 1)
    if "48-arrow system" in s:
        raise SystemExit("unrepaired 48-arrow shorthand remains in Batch 12CI")
    p.write_text(s, encoding="utf-8")


def registry() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    ids = {x.get("source_id") for x in d["sources"]}
    if CADAL_SOURCE_ID not in ids:
        d["sources"].append({
            "source_id": CADAL_SOURCE_ID,
            "title": "《欽定四庫全書》系《虎鈐經》卷七~卷十一 / CADAL06049792；卷七《傳箭》第七十六",
            "author_attribution": "《虎鈐經》傳統題宋許洞撰；作品年代不得直接等同於現存掃描實物年代",
            "historical_period": "SONG_WORK_RECEIVED_THROUGH_LATER_SIKU_RECENSION; EXACT_SURVIVING_PHYSICAL_COPY_DATE_UNRESOLVED_IN_THIS_BATCH",
            "provider": "Wikimedia Commons / CADAL / Zhejiang University",
            "url": "https://commons.wikimedia.org/wiki/File:CADAL06049792_%E8%99%8E%E9%88%90%E7%B6%93%C2%B7%E5%8D%B7%E4%B8%83~%E5%8D%B7%E5%8D%81%E4%B8%80.djvu",
            "source_role": "DIRECT_PHYSICAL_RECEIVED_SIKU_RECENSION_WITNESS_FOR_HUQIANJING_CHUANJIAN",
            "quality_notes": "Batch 12CJ directly reviews rendered physical-page images without OCR for glyph claims. The reviewed locus preserves 傳箭第七十六, 每時有八刻二十分, 一刻六十分, 一日十二時合一百刻, the 40/60->60/40 one-ke ladder, arrow numbers 第一箭 through 第二十箭, and the summer-solstice reset to 第一箭. Song authorship/composition context does not date this surviving scanned physical copy."
        })
    d["access_date"] = "2026-09-15"
    dump(p, d)


def research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-HUQIANJING-TIANYIGE-SIKU-CROSS-RECENSION-COLLATION-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Do an independent Tianyige Ming-print witness and a CADAL/Siku-recension witness preserve the same core Huqianjing Chuanjian operational mechanics, and what transmission claims are justified without inventing direct-copy direction?",
        "research_text_correction": {
            "prior_batch": PREV_ID,
            "rejected_shorthand": "48-arrow system",
            "corrected_mechanical_description": "20 numbered arrows (第一箭 through 第二十箭), with numbering reused after the solstitial reset for the opposite half-year direction",
            "correction_class": "RESEARCH_TEXT_CORRECTION_NOT_CHART_ALGORITHM_DEFECT",
            "provenance_defect_counter_increment": 0
        },
        "cadal_siku_received_witness": {
            "source_id": CADAL_SOURCE_ID,
            "workflow_run_id": CADAL_RUN,
            "job_id": CADAL_JOB,
            "artifact_id": CADAL_ARTIFACT,
            "artifact_digest": CADAL_ARTIFACT_DIGEST,
            "source_djvu_sha256": CADAL_DJVU_SHA256,
            "derived_pdf_sha256": CADAL_PDF_SHA256,
            "pdf_page_count": 152,
            "target_pages": list(range(14, 24)),
            "target_page_sha256": CADAL_PAGE_SHA256,
            "ocr_used_for_glyph_claims": False,
            "date_firewall": "The work is traditionally Song/early-11th-century; this does not date the surviving Siku-recension physical copy or modern CADAL surrogate.",
            "direct_readings": [
                "p14 heading: 傳箭第七十六",
                "p14: 每時有八刻二十分",
                "p14: 一刻六十分",
                "p14: 一日十二時合一百刻",
                "p14: 冬至前三日改第一箭 with day/night 40/60",
                "p14: 小寒初日改第三箭 with day/night 42/58",
                "p16: 雨水初日改第八箭 with day/night 47/53",
                "p18-p19: pre-summer 第二十箭 reaches 59/41",
                "p19: 夏至前三日改第一箭 with day/night 60/40",
                "p19-p23: post-summer sequence decreases daylight one ke at a time while arrow numbering again advances from 第一箭",
                "p23: late-year 第二十箭 is around 41/59 before winter reset"
            ]
        },
        "tianyige_ming_print_witness": {
            "source_id": TIANYIGE_SOURCE_ID,
            "workflow_run_id": TIANYIGE_RUN,
            "artifact_id": TIANYIGE_ARTIFACT,
            "artifact_digest": TIANYIGE_ARTIFACT_DIGEST,
            "target_page_sha256": TIANYIGE_PAGE_SHA256,
            "ocr_used_for_glyph_claims": False,
            "direct_control": [
                "p74 preserves the same opening hundred-ke / 60-fen-per-ke mechanics and winter 第一箭 40/60",
                "p74-p76 preserves the ascending one-ke seasonal ladder and numbered-arrow sequence",
                "p76 preserves 夏至前三日改第一箭 with 60/40",
                "p77-p78 preserves the descending return sequence toward winter"
            ]
        },
        "cross_recension_mechanical_adjudication": {
            "core_operational_sequence_stable_across_two_physical_witnesses": True,
            "arrow_number_domain": "1..20",
            "summer_solstice_resets_to_first_arrow": True,
            "annual_model": "TWO_OPPOSITE_HALF_YEAR_SEQUENCES_REUSING_ARROW_NUMBERS_1_TO_20",
            "day_total_ke": 100,
            "fen_per_ke": 60,
            "winter_extreme": "40/60",
            "summer_extreme": "60/40",
            "one_ke_step_ladder": True,
            "full_character_for_character_identity_all_loci_claimed": False,
            "direct_tianyige_to_siku_copy_direction_proved": False,
            "direct_siku_to_tianyige_copy_direction_proved": False,
            "direct_han_xianfu_to_huqian_copying_proved": False,
            "shared_work_or_common_recensional_ancestry_supported": True
        },
        "relationship_to_songshi_hanxianfu": {
            "near_contemporary_technical_context": True,
            "han_xianfu_recorded_event_date": 1010,
            "huqianjing_traditional_early_song_context": True,
            "shared_100_ke_day_context": True,
            "shared_40_60_seasonal_extrema_family": True,
            "mechanical_forms_differ": "Han Xianfu = precision 24-qi table with residuals; Huqianjing = operational integer arrow-change ladder with intra-term change dates.",
            "direct_textual_parent_child_relation": "UNRESOLVED"
        },
        "relationship_to_sanming_1578": {
            "shared_stepwise_pairs": ["42/58", "45/55", "47/53", "48/52", "49/51", "51/49", "53/47", "55/45", "56/44", "58/42", "59/41"],
            "same_mechanical_family": True,
            "exact_table_identity": False,
            "decisive_difference": "Huqianjing resets to 60/40 at summer solstice; Sanming displays 59/41 at 夏至 and has different date/term anchoring.",
            "structural_ancestry_candidate_strengthened": True,
            "direct_copying_proved": False
        },
        "transmission_impact": {
            "nodes_added_or_strengthened": [
                "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",
                "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",
                "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60"
            ],
            "edges_supported": ["TG-E0009", "TG-E0010", "TG-E0011", "TG-E0012"],
            "edges_revised": [],
            "edges_rejected_or_unproved": [
                "Tianyige Ming print -> Siku received copy direct-copy direction NOT PROVED",
                "Han Xianfu precision table -> Huqianjing direct textual parent NOT PROVED"
            ],
            "unresolved_lineage_questions": [
                "What intermediary source or rule connects the Huqian-style intra-term arrow-change ladder to the Ming Nanjing 59-ke cap?",
                "Is there an explicit historical conversion/selection rule connecting the 1010 precision table to coarse integer tables?",
                "Which pre-1578 witness combines a 59/41 solstitial cap with Sanming-like intermediate change dates?"
            ]
        },
        "adjudication": {
            "huqianjing_core_operational_sequence_cross_recension_stable": True,
            "forty_eight_arrow_shorthand_rejected": True,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "confirmed_chart_algorithm_defect_count": 0,
            "algorithm_reopen_authorized": False,
            "deterministic_fusion_chart_product_r1": "CLOSED"
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "reason": "This closes a cross-recension seasonal leak-arrow transmission layer but does not establish the Fullbook-specific upper-five-ke -> previous-night Hai branch transformation or a runtime clock binding."
        }
    })


def graph() -> None:
    p = Path("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    node_ids = {x.get("node_id") for x in d["nodes"]}
    new_nodes = [
        {
            "node_id": "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",
            "node_type": "PHYSICAL_COPY",
            "label": "天一閣藏明刻本《虎鈐經》卷七《傳箭》第七十六",
            "system_scope": "SONG_TECHNICAL_TIMEKEEPING_RECEIVED_IN_MING_PRINT",
            "work_composition_date": "TRADITIONAL_NORTHERN_SONG_EARLY_11TH_CENTURY_CONTEXT",
            "edition_impression_date": "MING_PRINT_EXACT_IMPRESSION_DATE_UNRESOLVED_IN_THIS_GRAPH_NODE",
            "physical_copy_date": "MING_PRINT",
            "digital_surrogate_date": "MODERN_TIANYIGE_WIKIMEDIA_SURROGATE",
            "evidence": ["docs/research/ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-R1.json", RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",
            "node_type": "PHYSICAL_COPY",
            "label": "CADAL06049792《欽定四庫全書》系《虎鈐經》卷七~卷十一",
            "system_scope": "SONG_TECHNICAL_TIMEKEEPING_RECEIVED_IN_SIKU_RECENSION",
            "work_composition_date": "TRADITIONAL_NORTHERN_SONG_EARLY_11TH_CENTURY_CONTEXT",
            "edition_impression_date": "SIKU_RECENSION; EXACT_CURRENT_COPY_DATE_UNRESOLVED",
            "physical_copy_date": "UNRESOLVED_WITHIN_LATER_SIKU_RECENSION",
            "digital_surrogate_date": "MODERN_CADAL_WIKIMEDIA_SURROGATE",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        },
        {
            "node_id": "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",
            "node_type": "RULE_FAMILY",
            "label": "《虎鈐經·傳箭》二十號箭循環40↔60季節漏刻家族",
            "system_scope": "SONG_OPERATIONAL_TIMEKEEPING",
            "mechanical_identity": "100-ke day; 60 fen per ke; arrows numbered 1..20; winter half-year ascends daylight 40->60 by one-ke steps, summer solstice resets numbering to 第一箭 and the opposite half-year descends 60->40.",
            "evidence": [RESEARCH, "docs/research/ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-R1.json"],
            "first_explicit_graph_batch": BATCH_ID
        }
    ]
    for node in new_nodes:
        if node["node_id"] not in node_ids:
            d["nodes"].append(node)
            node_ids.add(node["node_id"])

    edge_ids = {x.get("edge_id") for x in d["edges"]}
    new_edges = [
        {
            "edge_id": "TG-E0009",
            "from": "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",
            "relation": "ATTESTS",
            "to": "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_PHYSICAL_MING_PRINT_TEXT",
            "evidence": [RESEARCH, "docs/research/ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-R1.json"],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0010",
            "from": "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",
            "relation": "ATTESTS",
            "to": "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",
            "status": "CONFIRMED",
            "confidence": "HIGH",
            "evidence_class": "DIRECT_PHYSICAL_SIKU_RECENSION_TEXT",
            "evidence": [RESEARCH],
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0011",
            "from": "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",
            "relation": "STRUCTURAL_ANCESTRY_CANDIDATE_FOR",
            "to": "TABLE-SANMING-1578-DAYNIGHT-KE",
            "status": "PROBABLE",
            "confidence": "MEDIUM_HIGH",
            "evidence_class": "CROSS_RECENSION_PHYSICAL_STABILITY_PLUS_SHARED_ONE_KE_LADDER",
            "evidence": [RESEARCH, "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-CD.md"],
            "scope_note": "Shared stepwise pairs and stable operational ladder strengthen structural ancestry; differing change dates and Huqian 60/40 versus Sanming 59/41 prohibit exact-table or direct-copy claims.",
            "adjudication_batch": BATCH_ID
        },
        {
            "edge_id": "TG-E0012",
            "from": "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",
            "relation": "SHARED_COMMON_ANCESTOR_CANDIDATE",
            "to": "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",
            "status": "HIGH_CONFIDENCE",
            "confidence": "HIGH",
            "evidence_class": "INDEPENDENT_PHYSICAL_RECENSIONS_WITH_STABLE_SECTION_AND_CORE_MECHANICS",
            "evidence": [RESEARCH],
            "scope_note": "The two witnesses preserve the same work/section and core mechanics. Direct copy direction between the physical witnesses is not inferred.",
            "adjudication_batch": BATCH_ID
        }
    ]
    for edge in new_edges:
        if edge["edge_id"] not in edge_ids:
            d["edges"].append(edge)
            edge_ids.add(edge["edge_id"])

    non_edges = d.setdefault("explicit_non_edges", [])
    if not any(x.get("from") == "TABLE-HANXIANFU-1010-24QI-PRECISION" and x.get("to") == "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60" for x in non_edges):
        non_edges.append({
            "from": "TABLE-HANXIANFU-1010-24QI-PRECISION",
            "relation": "DIRECT_TEXTUAL_PARENT_OF",
            "to": "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",
            "status": "UNRESOLVED",
            "reason": "Near-contemporary chronology and shared seasonal 100-ke context do not prove direct textual transmission; the mechanical forms are different.",
            "evidence": [RESEARCH]
        })
    if not any(x.get("from") == "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING" and x.get("to") == "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU" and x.get("relation") == "DIRECT_COPY_PARENT_OF" for x in non_edges):
        non_edges.append({
            "from": "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",
            "relation": "DIRECT_COPY_PARENT_OF",
            "to": "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",
            "status": "UNRESOLVED",
            "reason": "Cross-recension mechanical stability supports common textual ancestry, not direct physical-copy direction.",
            "evidence": [RESEARCH]
        })
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def graph_verifier() -> None:
    p = Path("scripts/verify-tianwen-transmission-genealogy-r1.py")
    s = p.read_text(encoding="utf-8")
    if '"PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",' not in s:
        needle = '        "TABLE-HANXIANFU-1010-24QI-PRECISION",\n'
        block = (
            '        "PHYSICAL-COPY-HUQIANJING-TIANYIGE-MING",\n'
            '        "PHYSICAL-COPY-HUQIANJING-CADAL06049792-SIKU",\n'
            '        "RULE-FAMILY-HUQIANJING-CHUANJIAN-20ARROW-40-60",\n'
        )
        if needle not in s:
            raise SystemExit("cannot extend Tianwen required nodes")
        s = s.replace(needle, needle + block, 1)
    if 'e11 = next((e for e in edges if e.get("edge_id") == "TG-E0011"), None)' not in s:
        needle = '    ncl = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-SISHI-QIHOU-NCL03164-OLD-MANUSCRIPT")\n'
        block = dedent('''
            e11 = next((e for e in edges if e.get("edge_id") == "TG-E0011"), None)
            if not e11 or e11.get("relation") != "STRUCTURAL_ANCESTRY_CANDIDATE_FOR" or e11.get("status") != "PROBABLE":
                fail("Huqianjing/Sanming structural ancestry edge regressed")
            e12 = next((e for e in edges if e.get("edge_id") == "TG-E0012"), None)
            if not e12 or e12.get("relation") != "SHARED_COMMON_ANCESTOR_CANDIDATE" or e12.get("status") != "HIGH_CONFIDENCE":
                fail("Huqianjing cross-recension common-ancestry edge regressed")

        ''')
        if needle not in s:
            raise SystemExit("cannot insert Huqian graph checks")
        s = s.replace(needle, block + needle, 1)
    p.write_text(s, encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    rp = row.setdefault("research_progress", {})
    rp["batch_12cj_huqianjing_tianyige_siku_cross_recension"] = {
        "source_ids": [TIANYIGE_SOURCE_ID, CADAL_SOURCE_ID],
        "independent_physical_witnesses": 2,
        "core_operational_sequence_cross_recension_stable": True,
        "arrow_number_domain": "1..20",
        "summer_solstice_resets_to_first_arrow": True,
        "forty_eight_arrow_shorthand_rejected": True,
        "direct_copy_direction_proved": False,
        "direct_han_xianfu_parent_proved": False,
        "upper_zi_to_hai_vote_increment": 0,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen_authorized": False,
        "transmission_impact_recorded": True,
        "research_artifact": RESEARCH
    }
    dump(p, d)


def matrix_md() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    s = p.read_text(encoding="utf-8")
    if "## Progress — Batch 12CJ" not in s:
        s += dedent(f'''

        ## Progress — Batch 12CJ

        - A new no-OCR physical review of `CADAL06049792《虎鈐經·卷七~卷十一》` provides an independent Siku-recension control for `卷七《傳箭》第七十六`. It preserves the same core mechanics already observed in the Tianyige Ming-print witness: `每時有八刻二十分`, `一刻六十分`, `一日十二時合一百刻`, winter `40/60`, summer `60/40`, and the one-ke seasonal ladder.
        - Direct physical collation corrects the prior Batch 12CI shorthand `48-arrow system`. The section numbers arrows only `第一箭` through `第二十箭`; at summer solstice it resets to `第一箭` and reuses the numbering for the opposite half-year direction. This is a research-text correction, not a chart algorithm defect and not a provenance-defect counter increment.
        - The two physical witnesses materially strengthen the stability of the Huqianjing operational rule family across recensions, but no direct-copy direction between Tianyige and the Siku witness is asserted, and no direct Han-Xianfu -> Huqian textual edge is asserted.
        - For 1578 Sanming, the Huqian lineage remains a strong structural component candidate because it preserves the same one-ke stepwise numeric family, while its `夏至 60/40` reset and change-day schedule remain non-identical to Sanming's `夏至 59/41` display.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts and deterministic product invariants are unchanged.

        Batch document: `{BATCH_DOC}`. Research record: `{RESEARCH}`.
        ''')
    p.write_text(s, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d["historical_audit"]
    if BATCH_ID not in h["completed_batches"]:
        h["completed_batches"].append(BATCH_ID)
    h["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12CJ independently cross-collates the Tianyige Ming-print and CADAL/Siku-recension Huqianjing Chuanjian witnesses. The core 100-ke / 60-fen-per-ke / 40<->60 one-ke ladder is stable across both physical witnesses.",
        "Batch 12CJ corrects the Batch 12CI research shorthand '48-arrow system': direct physical evidence numbers arrows 第一箭 through 第二十箭, then resets to 第一箭 at summer solstice for the opposite half-year sequence. This correction does not increment provenance-defect or algorithm-defect counters.",
        "Tianwen transmission graph now records the Huqianjing 20-number-arrow operational family as cross-recension stable and as a strengthened structural ancestry candidate for Sanming, while withholding direct Tianyige->Siku, Han-Xianfu->Huqian, or Huqian->Sanming copy claims."
    ]
    for x in additions:
        if x not in h["current_focus"]:
            h["current_focus"].append(x)
    d["schema_version"] = "1.96.0"
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def write_doc() -> None:
    p = Path(BATCH_DOC)
    p.write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CJ

    ## 《虎鈐經·傳箭》天一閣明刻本 × 四庫系受傳本跨版本機械校勘

    Status: **TWO INDEPENDENT PHYSICAL WITNESSES DIRECTLY COLLATED / CORE CHUANJIAN OPERATIONAL SEQUENCE CROSS-RECENSION STABLE / ARROWS NUMBERED 1 THROUGH 20 AND REUSED AFTER SOLSTITIAL RESET / PRIOR 48-ARROW SHORTHAND REJECTED / 40↔60 ONE-KE LADDER STRENGTHENED AS A STABLE TRANSMISSION LAYER / DIRECT COPY DIRECTION AND HAN-XIANFU PARENTAGE NOT PROVED / SANMING STRUCTURAL ANCESTRY CANDIDATE STRENGTHENED BUT EXACT TABLE IDENTITY REJECTED / HPA-ZDATE-006 UNCHANGED / NO ALGORITHM REOPEN**

    ## 1. Why this batch follows 12CI

    Batch 12CI closed a recorded 1010 Han Xianfu precision 24-qi table and a 24/24 mechanical bridge to the later coarse integer family. Its next gate called for an independent audit of the near-contemporary `《虎鈐經·傳箭》` operational lineage. During that follow-up the earlier shorthand `48-arrow system` proved inaccurate and therefore requires an explicit forward-only research correction.

    ## 2. New independent physical witness

    `CADAL06049792《虎鈐經·卷七~卷十一》` was rendered page-by-page without OCR.

    ```text
    RUN={CADAL_RUN}
    JOB={CADAL_JOB}
    ARTIFACT={CADAL_ARTIFACT}
    ARTIFACT_DIGEST={CADAL_ARTIFACT_DIGEST}
    SOURCE_DJVU_SHA256={CADAL_DJVU_SHA256}
    DERIVED_PDF_SHA256={CADAL_PDF_SHA256}
    PAGES=152
    TARGET=P14-P23 / 卷七 傳箭第七十六
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    Date firewall:

    ```text
    《虎鈐經》宋代作品脈絡 != 當前四庫系物理副本年代
    四庫系受傳本 != 宋代原本
    CADAL modern surrogate != historical physical copy date
    ```

    ## 3. Direct mechanical readings

    The CADAL/Siku-recension witness directly preserves:

    ```text
    傳箭第七十六
    每時有八刻二十分
    一刻六十分
    一日十二時合一百刻
    冬至前三日改第一箭 ... 晝四十刻 / 夜六十刻
    ...
    小寒初日改第三箭 ... 42/58
    ...
    雨水初日改第八箭 ... 47/53
    ...
    第二十箭 ... 59/41
    夏至前三日改第一箭 ... 60/40
    ```

    After the summer-solstice reset, the text again advances from `第一箭` while daylight decreases one ke at a time toward winter.

    Therefore the mechanically safe description is:

    ```text
    ARROW_NUMBER_DOMAIN=1..20
    SOLSTITIAL_RESET=summer solstice -> 第一箭
    ANNUAL_MODEL=two opposite half-year sequences reusing arrow numbers 1..20
    ```

    It is **not** a 48-arrow numbering system.

    ## 4. Cross-recension control with the Tianyige Ming print

    Batch 12CD had already physically reviewed the Tianyige Ming-print witness. Re-collation against pp74–78 confirms the same core operational architecture:

    - the same hundred-ke day and sixty-fen-per-ke framework;
    - winter first arrow `40/60`;
    - one-ke stepwise seasonal changes;
    - numbered-arrow progression;
    - `夏至前三日改第一箭` at `60/40`;
    - the descending return sequence after summer.

    This closes **core mechanical stability across two distinct received physical witnesses**. It does not authorize a character-for-character identity claim for every locus, and it does not identify one surviving physical copy as the direct parent of the other.

    ## 5. Research-text correction

    Batch 12CI used the shorthand:

    ```text
    integer 48-arrow system
    ```

    Direct cross-recension physical evidence rejects that wording. The corrected description is:

    ```text
    20-number arrow cycle, reused across opposite half-year directions
    ```

    Classification:

    ```text
    RESEARCH_TEXT_CORRECTION=true
    PROVENANCE_METADATA_DEFECT_INCREMENT=0
    CHART_ALGORITHM_DEFECT_INCREMENT=0
    ```

    ## 6. Relationship to Han Xianfu and Sanming

    The evidence now separates three mechanical forms more cleanly:

    ```text
    1010 Han Xianfu precision 24-qi table
        = fine values with residuals

    Huqianjing Chuanjian operational ladder
        = intra-term arrow changes + integer one-ke steps + 40/60 <-> 60/40

    1578 Sanming display
        = shares many one-ke pairs but has different anchoring and Xiazhi 59/41
    ```

    Near chronology and shared technical vocabulary are insufficient to prove `Han Xianfu -> Huqianjing` copying. Likewise the stable Huqian ladder is a materially strengthened **structural ancestry candidate** for Sanming, not an exact table parent: Huqian reaches `夏至 60/40`; Sanming prints `夏至 59/41`.

    ## 7. Tianwen transmission impact

    The graph now adds/strengthens:

    ```text
    Tianyige Ming physical witness ─┐
                                   ├─ ATTESTS -> Huqianjing 20-number-arrow 40↔60 rule family
    CADAL/Siku physical witness ───┘

    Huqianjing rule family
        -> STRUCTURAL_ANCESTRY_CANDIDATE_FOR -> Sanming 1578
    ```

    The two surviving witnesses receive only a `SHARED_COMMON_ANCESTOR_CANDIDATE` relation; direct-copy direction remains unresolved.

    ## 8. Product adjudication

    ```text
    HPA-ZDATE-006=MISSING_FROM_PRODUCT
    UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
    NEW_RUNTIME_CANDIDATE=false
    RUNTIME_WINNER=false
    CANDIDATE_COLLAPSE=false
    CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
    ALGORITHM_REOPEN_COUNT=0
    DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
    ```

    ## 9. Next gate

    1. search specifically for a pre-1578 intermediary that combines a Huqian-style intra-term step ladder with the Nanjing/Datong `59`-ke cap or Sanming-like change-day fingerprint;
    2. search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI `(78,81]/147` precision-to-coarse threshold;
    3. continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def main() -> int:
    continuity()
    correct_prior_research_text()
    registry()
    research()
    graph()
    graph_verifier()
    matrix()
    matrix_md()
    state()
    write_doc()
    print("BATCH_12CJ_FORMALIZATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
