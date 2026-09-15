from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-CI"
PREV_ID = "BATCH-12-ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-CH"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-CI.md"
RESEARCH = "docs/research/SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-R1.json"
SOURCE_ID = "EXT-SONGSHI-HANXIANFU-CADAL06060929"
LEIBIAN_SOURCE_ID = "EXT-NLC-LEIBIAN-LIFA-TONGSHU-MING-VOL1"

SONG_RUN = 34932102620
SONG_JOB = 104262273291
SONG_ARTIFACT = 10382077226
SONG_ARTIFACT_DIGEST = "sha256:754a9132f6ec902fe6393a34ef0d9e1a254fc1f86104341af4ea26745a279e75"
SONG_DJVU_SHA256 = "de3e5f7311b4190d790df6ababde566a45a3c0e45c463d59b46b3a88671094a1"
SONG_PDF_SHA256 = "63866e4696bbd2f2950d983162d71e8587f04760ae0f06bc912ec4c98edb2976"
SONG_PAGE_SHA256 = {
    "117": "2df15d1d296e124908afbe9e8d5f7db66525e339e17126fedba98c6302a6c1fb",
    "118": "eb41cda0774bdfa2cad589e79b61271a0d753184479d8a09cede84b5882d91e5",
    "119": "e505200775e213f0b2dd5dbfede1d0c0fccb669095f82600132c7d40777228c0",
    "120": "e22d005a0d5853ff5321953ee1680c8835d616c75ff1922f7a4cb8a09a4a2cf0",
    "121": "ea0a68b636ca65a4e0504a980cd82a868f7e57065758c052928b3d0594a01ac9",
    "122": "9b6a7fd74f5cd560dcb9753d6d581fff80785af84561a4dae756567b7cda6d77",
    "123": "1ccbea3ed7c9d1ed10b62bdfd1082888d2e92c54b114ef87da5126e9d0338880",
}
LEIBIAN_PAGE_SHA256 = {
    "18": "396d2a123a3d65b8813bab8944c376f7905bffe803149cf030b44476c35a3849",
    "19": "1b1633d233b9249f416cd62352c812de822e315fb99b772fd26ca006f62bbca6",
    "20": "15325745229581c336e407d0eb405a8ef75c6d3bcf28117209f51f0484af7ce4",
    "21": "a348fb2e6c4b06323bcdbc6851aa7f09ca72a76e8ab2d9e08bd50eabf79c3bbe",
    "22": "7055c809e21271a081b3319649687424b14a11dfe4f8698284257a3e1a61cb96",
    "23": "6bd322324e839814144a566fa2caa97752f5073afe2ef3c81a1f656603824bd1",
    "24": "0e94adaf05c5082b680ab210d2bf7703a5c184fe1217aa35b0ee96606870329f",
}

# Direct physical Songshi day-ke readings. Residuals are written as integer
# remainders in the table; their denominator is inferred from conservation:
# day residual + night residual = 147 in every non-equinox row.
SONG_ROWS = [
    ("冬至", 40, 5), ("小寒", 40, 55), ("大寒", 41, 78),
    ("立春", 43, 34), ("雨水", 45, 30), ("驚蟄", 47, 66),
    ("春分", 50, 0), ("清明", 52, 81), ("穀雨", 54, 137),
    ("立夏", 57, 6), ("小滿", 58, 99), ("芒種", 59, 102),
    ("夏至", 59, 142), ("小暑", 59, 102), ("大暑", 58, 99),
    ("立秋", 57, 6), ("處暑", 54, 137), ("白露", 52, 81),
    ("秋分", 50, 0), ("寒露", 47, 66), ("霜降", 45, 30),
    ("立冬", 43, 34), ("小雪", 41, 78), ("大雪", 40, 55),
]
COARSE_ROWS = {
    "冬至": 40, "小寒": 40, "大寒": 41,
    "立春": 43, "雨水": 45, "驚蟄": 47,
    "春分": 50, "清明": 53, "穀雨": 55,
    "立夏": 57, "小滿": 59, "芒種": 60,
    "夏至": 60, "小暑": 60, "大暑": 59,
    "立秋": 57, "處暑": 55, "白露": 53,
    "秋分": 50, "寒露": 47, "霜降": 45,
    "立冬": 43, "小雪": 41, "大雪": 40,
}
LEIBIAN_PAGE_MAP = {
    "立春": 18, "雨水": 18,
    "驚蟄": 19, "春分": 19, "清明": 19, "穀雨": 19,
    "立夏": 20, "小滿": 20, "芒種": 20, "夏至": 20,
    "小暑": 21, "大暑": 21, "立秋": 21, "處暑": 21,
    "白露": 22, "秋分": 22, "寒露": 22, "霜降": 22,
    "立冬": 23, "小雪": 23, "大雪": 23, "冬至": 23,
    "小寒": 24, "大寒": 24,
}


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replay_rows() -> list[dict]:
    out = []
    for term, integer_ke, residual in SONG_ROWS:
        coarse = COARSE_ROWS[term]
        nearest = integer_ke + (1 if residual * 2 >= 147 else 0)
        threshold_replay = integer_ke + (1 if residual >= 81 else 0)
        out.append({
            "solar_term": term,
            "song_integer_ke": integer_ke,
            "song_residual": residual,
            "inferred_residual_denominator": 147,
            "song_day_ke_decimal_for_analysis_only": round(integer_ke + residual / 147, 9),
            "ming_coarse_day_ke": coarse,
            "ming_coarse_physical_page": LEIBIAN_PAGE_MAP[term],
            "modern_nearest_integer": nearest,
            "modern_nearest_integer_match": nearest == coarse,
            "historical_threshold_replay_ge_81": threshold_replay,
            "threshold_replay_match": threshold_replay == coarse,
        })
    return out


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CH tail in continuity verifier")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch doc")
    p.write_text(s, encoding="utf-8")


def registry() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    ids = {x.get("source_id") for x in d["sources"]}
    if SOURCE_ID not in ids:
        d["sources"].append({
            "source_id": SOURCE_ID,
            "title": "《宋史》卷七十《律曆志三》韓顯符《銅渾儀法要》二十四氣晝夜刻表 / CADAL06060929",
            "author_attribution": "《宋史》元代官修史書；target passage records 北宋春官正韓顯符",
            "historical_period": "RECORDED_TECHNICAL_EVENT_DATED_DAZHONG_XIANGFU_3_1010; SONGSHI_COMPILATION_LATER; CURRENT_DIGITAL_SURROGATE_MODERN",
            "provider": "Wikimedia Commons / CADAL / Zhejiang University",
            "url": "https://commons.wikimedia.org/wiki/File:CADAL06060929_%E5%AE%8B%E5%8F%B2%C2%B7%E5%8D%B7%E5%85%AD%E5%8D%81%E4%B9%9D~%E5%8D%B7%E4%B8%83%E5%8D%81.djvu",
            "source_role": "DIRECT_PHYSICAL_RECEIVED_SONGSHI_WITNESS_FOR_RECORDED_1010_PRECISION_DAY_NIGHT_KE_TABLE",
            "quality_notes": "Batch 12CI directly reviews the CADAL physical-page surrogate without OCR for glyph claims. PDF pp117-119 establish the leak-clock context and the recorded Dazhong Xiangfu 3 / 1010 Han Xianfu submission; pp120-123 preserve the 24-term table. The 1010 date belongs to the recorded technical event/work, not to the surviving scanned physical copy. Direct textual genealogy to Ming tables is not inferred from chronology or numerical compatibility alone."
        })
    d["access_date"] = "2026-09-15"
    dump(p, d)


def research() -> None:
    rows = replay_rows()
    nearest_misses = [r["solar_term"] for r in rows if not r["modern_nearest_integer_match"]]
    threshold_matches = sum(1 for r in rows if r["threshold_replay_match"])
    residuals_down = sorted({r["song_residual"] for r in rows if r["ming_coarse_day_ke"] == r["song_integer_ke"]})
    residuals_up = sorted({r["song_residual"] for r in rows if r["ming_coarse_day_ke"] == r["song_integer_ke"] + 1})
    dump(RESEARCH, {
        "schema": "SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does the received Songshi physical witness preserve a recorded 1010 Han Xianfu precision 24-term day/night-ke table, and can its precision values mechanically account for the complete Ming coarse 40<->60 table without asserting direct textual descent?",
        "date_scope_firewall": {
            "recorded_technical_event_date": "大中祥符三年 / 1010",
            "recorded_person_role": "春官正韓顯符",
            "recorded_work": "銅渾儀法要",
            "songshi_compilation_date_is_not_event_date": True,
            "surviving_scanned_physical_copy_date_is_not_1010": True,
            "digital_surrogate_date_is_modern": True,
            "direct_genealogy_from_1010_event_to_ming_table_proved": False
        },
        "physical_witness": {
            "source_id": SOURCE_ID,
            "digital_object": "CADAL06060929 宋史·卷六十九~卷七十",
            "workflow_run_id": SONG_RUN,
            "job_id": SONG_JOB,
            "artifact_id": SONG_ARTIFACT,
            "artifact_digest": SONG_ARTIFACT_DIGEST,
            "source_djvu_sha256": SONG_DJVU_SHA256,
            "derived_pdf_sha256": SONG_PDF_SHA256,
            "pdf_page_count": 152,
            "target_page_sha256": SONG_PAGE_SHA256,
            "ocr_used_for_glyph_claims": False,
            "direct_context": {
                "p117": "漏刻 section introduces the classical leak-clock office/context.",
                "p118": "Directly describes copper vessels, water balance, clepsydra arrow and related palace timekeeping apparatus.",
                "p119_to_p120": "Records 大中祥符三年春官正韓顯符上《銅渾儀法要》, containing a 24-qi day/night advance-retreat and sunrise/sunset ke-number established method; table follows.",
                "p120_to_p123": "Direct 24-term numerical table."
            }
        },
        "song_precision_table": {
            "residual_denominator_status": "INFERRED_BY_DAY_NIGHT_CONSERVATION_NOT_EXPLICITLY_NAMED_IN_REVIEWED_PASSAGE",
            "inferred_residual_denominator": 147,
            "inference": "For every non-equinox row, day integer + night integer = 99 and day residual + night residual = 147; therefore each residual unit is 1/147 ke if total day+night is 100 ke. Equinox is exactly 50/50.",
            "do_not_parse_as_modern_decimal": True,
            "examples": [
                "冬至: day 40 ke + 5/147; night 59 ke + 142/147",
                "大寒: day 41 ke + 78/147; night 58 ke + 69/147",
                "清明: day 52 ke + 81/147; night 47 ke + 66/147",
                "夏至: day 59 ke + 142/147; night 40 ke + 5/147"
            ],
            "rows": rows
        },
        "ming_coarse_table_control": {
            "source_id": LEIBIAN_SOURCE_ID,
            "batch": "BATCH-12-ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-CE",
            "direct_physical_pages": list(range(18, 25)),
            "page_sha256": LEIBIAN_PAGE_SHA256,
            "full_24_term_day_ke": COARSE_ROWS,
            "physical_scope": "Ming print object; exact impression year within Ming unresolved in Batch 12CE",
            "same_family_as_1455_sishi_qihou_representative_anchors": True
        },
        "quantization_replay": {
            "rows_compared": 24,
            "exact_matches_under_residual_ge_81_rule": threshold_matches,
            "modern_nearest_integer_matches": 24 - len(nearest_misses),
            "modern_nearest_integer_misses": nearest_misses,
            "largest_residual_kept_down": max(residuals_down),
            "smallest_residual_rounded_up": min(residuals_up),
            "admissible_threshold_interval_in_residual_units": "(78, 81] if rule is of form round-up when residual >= threshold",
            "admissible_threshold_interval_as_ke_fraction": "(78/147, 81/147] ~= (0.530612, 0.551020]",
            "exact_historical_rounding_instruction_found": False,
            "modern_half_threshold_rejected_for_this_coarse_table": True,
            "mechanical_result": "FULL_24_OF_24_QUANTIZATION_COMPATIBILITY_WITH_A_SINGLE_THRESHOLD_INTERVAL",
            "genealogical_result": "STRUCTURAL/MECHANICAL_ANCESTRY_CANDIDATE_STRENGTHENED; DIRECT_TEXTUAL_DESCENT_UNPROVED"
        },
        "sanming_1578_comparison": {
            "known_examples": ["小寒 42/58", "立春 45/55", "雨水 47/53 then 48/52", "夏至 59/41"],
            "equals_song_precision_term_start_table_after_same_coarse_quantization": False,
            "equals_ming_coarse_40_60_table": False,
            "interpretation": "The Song precision -> coarse 40/60 bridge explains an older coarse family, not Sanming's Nanjing-like 59-ke cap. Sanming still requires the separately evidenced Ming/Nanjing locality/daily-table adaptation layer."
        },
        "transmission_impact": {
            "new_node": "TABLE-HANXIANFU-1010-24QI-PRECISION",
            "edge_to_coarse_family": "STRUCTURAL_ANCESTRY_CANDIDATE_FOR",
            "edge_strength": "HIGH_FOR_24/24_MECHANICAL_COMPATIBILITY; UNRESOLVED_FOR_DIRECT_TEXTUAL_GENEALOGY",
            "direct_copy_edge_authorized": False,
            "model_after_batch": "recorded 1010 precision 24-qi leak-clock table -> mechanically compatible coarse integer 40/60 family (exact textual route unresolved); early-Ming Nanjing/Datong locality layer then remains separately necessary to explain Sanming 1578's 59/41 cap and intermediate display"
        },
        "adjudication": {
            "precision_song_table_physically_received_witness_closed": True,
            "residual_147_denominator_inferred_by_conservation": True,
            "full_24_row_quantization_compatibility_closed": True,
            "exact_historical_threshold_instruction_closed": False,
            "direct_textual_genealogy_closed": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "reason": "This closes a much earlier numerical/timekeeping ancestry layer but does not establish the Fullbook-specific upper-five-ke -> previous-night Hai branch transformation or runtime clock binding."
        },
        "accounting": {
            "matrix_rows": 198,
            "audited_rows": 166,
            "current_missing_from_product_rows": 10,
            "identified_missing_candidate_families": 14,
            "confirmed_provenance_metadata_defect_count": 11,
            "repaired_provenance_metadata_defect_count": 11,
            "confirmed_chart_algorithm_defect_count": 0,
            "algorithm_reopen_count": 0,
            "candidate_collapse_count": 0
        }
    })


def matrix_json() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    row["batch_12ci_songshi_hanxianfu_1010_daynight_ke"] = {
        "source_ids": [SOURCE_ID, LEIBIAN_SOURCE_ID],
        "recorded_technical_event_date": 1010,
        "songshi_cadal_physical_pages_directly_reviewed": True,
        "song_residual_denominator_147_inferred_by_conservation": True,
        "ming_coarse_full_24_rows_directly_reviewed": True,
        "full_24_row_single_threshold_quantization_match": True,
        "modern_nearest_integer_match_count": 22,
        "modern_nearest_integer_misses": ["大寒", "小雪"],
        "historical_threshold_instruction_found": False,
        "direct_textual_genealogy_closed": False,
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
    marker = "## Progress — Batch 12CI"
    if marker not in s:
        s = s.rstrip() + "\n\n" + dedent(f'''\
        {marker}

        - Direct no-OCR review of `CADAL06060929 宋史·卷六十九~卷七十` physically closes the received `《宋史》卷七十` witness recording that in `大中祥符三年` (1010) 春官正韓顯符 submitted `《銅渾儀法要》` with a 24-qi day/night advance-retreat and sunrise/sunset ke-number established method. The 1010 date is the recorded technical event, not the date of the surviving scanned copy.
        - The 24-term day/night rows conserve exactly 100 ke. In every non-equinox row the integer parts total 99 and the residuals total 147, so the residual denominator is mechanically inferable as 147 per ke. `59刻142` must therefore not be misread as modern decimal `59.142`.
        - Re-review of the Ming-print `《類編曆法通書》` coarse table on physical pp18–24 closes all 24 integer term anchors. The entire table is compatible with one quantization threshold on the Song residuals: residuals `<=78` remain at the lower integer and residuals `>=81` advance one ke. No 79/80 residual occurs, so the exact threshold is only bounded to `(78,81]/147`.
        - Modern nearest-integer rounding is explicitly rejected as the historical explanation: it matches 22/24 but fails at `大寒` and `小雪`, where `41 + 78/147 ~= 41.531` would round to 42 while the direct Ming coarse table prints 41.
        - This establishes a full 24/24 **mechanical quantization compatibility** between the recorded 1010 precision table and the later coarse `40<->60` family. It does not prove direct textual copying, a specific historical rounding instruction, or the exact stemma.
        - The result explains the older coarse table family, not the 1578 `《三命通會》` Nanjing-like display: Sanming still differs materially (`小寒 42/58`, `立春 45/55`, `夏至 59/41`) and continues to require the separately evidenced Ming/Nanjing locality/daily-table adaptation layer.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi->Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Counts remain 198/166/10/14 and provenance defects 11/11.

        Batch document: `{BATCH_DOC}`. Research record: `{RESEARCH}`.
        ''')
        p.write_text(s, encoding="utf-8")


def graph() -> None:
    p = Path("docs/TRANSMISSION-GENEALOGY-GRAPH-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    node_ids = {x.get("node_id") for x in d["nodes"]}
    if "TABLE-HANXIANFU-1010-24QI-PRECISION" not in node_ids:
        d["nodes"].append({
            "node_id": "TABLE-HANXIANFU-1010-24QI-PRECISION",
            "node_type": "MECHANICAL_RULE",
            "label": "《宋史》所錄1010韓顯符二十四氣精細晝夜刻表",
            "system_scope": "SONG_TECHNICAL_TIMEKEEPING",
            "recorded_event_date": "NORTHERN_SONG_DAZHONG_XIANGFU_3_1010",
            "source_compilation_layer": "LATER_SONGSHI_HISTORIOGRAPHICAL_WITNESS",
            "physical_copy_date": "UNRESOLVED_FOR_CURRENT_CADAL_SURROGATE",
            "digital_surrogate_date": "MODERN_CADAL_WIKIMEDIA_SURROGATE",
            "mechanical_identity": "24 solar-term day/night values totaling 100 ke, with residual denominator 147 inferred by conservation; summer solstice day = 59 + 142/147 ke.",
            "evidence": [RESEARCH],
            "first_explicit_graph_batch": BATCH_ID
        })
    edge_ids = {x.get("edge_id") for x in d["edges"]}
    if "TG-E0008" not in edge_ids:
        d["edges"].append({
            "edge_id": "TG-E0008",
            "from": "TABLE-HANXIANFU-1010-24QI-PRECISION",
            "relation": "STRUCTURAL_ANCESTRY_CANDIDATE_FOR",
            "to": "TABLE-FAMILY-TONGSHU-COARSE-40-60",
            "status": "PROBABLE",
            "confidence": "HIGH_FOR_MECHANICAL_COMPATIBILITY_MEDIUM_FOR_TRANSMISSION_ANCESTRY",
            "evidence_class": "DIRECT_PHYSICAL_RECEIVED_SONGSHI_TABLE_PLUS_DIRECT_MING_COARSE_TABLE_24_OF_24_THRESHOLD_REPLAY",
            "evidence": [
                RESEARCH,
                "docs/research/ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-R1.json"
            ],
            "scope_note": "All 24 Ming coarse anchors are reproducible from the Song precision rows with one threshold interval (78,81]/147, but no direct textual-copy edge or exact historical rounding instruction is proved.",
            "adjudication_batch": BATCH_ID
        })
    non_edges = d.setdefault("explicit_non_edges", [])
    if not any(x.get("from") == "TABLE-HANXIANFU-1010-24QI-PRECISION" and x.get("to") == "TABLE-FAMILY-TONGSHU-COARSE-40-60" for x in non_edges):
        non_edges.append({
            "from": "TABLE-HANXIANFU-1010-24QI-PRECISION",
            "relation": "DIRECT_TEXTUAL_PARENT_OF",
            "to": "TABLE-FAMILY-TONGSHU-COARSE-40-60",
            "status": "UNRESOLVED",
            "reason": "24/24 numerical quantization compatibility and chronology establish a strong structural ancestry candidate, not a stemmatically demonstrated copy chain.",
            "evidence": [RESEARCH]
        })
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def graph_verifier() -> None:
    p = Path("scripts/verify-tianwen-transmission-genealogy-r1.py")
    s = p.read_text(encoding="utf-8")
    if '"TABLE-HANXIANFU-1010-24QI-PRECISION",' not in s:
        needle = '        "TABLE-SANMING-1578-DAYNIGHT-KE",\n'
        if needle not in s:
            raise SystemExit("cannot extend required transmission nodes")
        s = s.replace(needle, needle + '        "TABLE-HANXIANFU-1010-24QI-PRECISION",\n', 1)
    if '1010/coarse 24-row structural edge regressed' not in s:
        needle = '    ncl = next(n for n in nodes if n.get("node_id") == "PHYSICAL-COPY-SISHI-QIHOU-NCL03164-OLD-MANUSCRIPT")\n'
        block = '''    e8 = next((e for e in edges if e.get("edge_id") == "TG-E0008"), None)\n    if not e8 or e8.get("relation") != "STRUCTURAL_ANCESTRY_CANDIDATE_FOR" or e8.get("status") != "PROBABLE":\n        fail("1010/coarse 24-row structural edge regressed")\n\n'''
        if needle not in s:
            raise SystemExit("cannot insert E0008 graph verifier")
        s = s.replace(needle, block + needle, 1)
    p.write_text(s, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    h = d["historical_audit"]
    if BATCH_ID not in h["completed_batches"]:
        h["completed_batches"].append(BATCH_ID)
    h["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12CI directly closes the received Songshi physical witness for the recorded 1010 Han Xianfu 24-qi precision day/night-ke table; the 1010 date is the recorded technical event, not the surviving scanned-copy date.",
        "Batch 12CI infers a 147-part per-ke residual denominator by exact day/night conservation and closes 24/24 mechanical quantization compatibility to the Ming coarse 40<->60 table. Modern nearest-integer rounding fails at Dahan/Xiaoxue; the historical threshold is only bounded to (78,81]/147, not textually named.",
        "Tianwen transmission graph now records the 1010 precision table as a high-strength structural ancestry candidate for the coarse Tongshu family while explicitly withholding direct textual genealogy. Sanming 1578 still requires a separate Ming/Nanjing adaptation layer; HPA-ZDATE-006 remains MISSING_FROM_PRODUCT and no algorithm invariant changes."
    ]
    for x in additions:
        if x not in h["current_focus"]:
            h["current_focus"].append(x)
    d["schema_version"] = "1.95.0"
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def write_doc() -> None:
    rows = replay_rows()
    row_lines = "\n".join(
        f"| {r['solar_term']} | {r['song_integer_ke']} + {r['song_residual']}/147 | {r['ming_coarse_day_ke']} | {r['modern_nearest_integer']} | {'YES' if r['threshold_replay_match'] else 'NO'} |"
        for r in rows
    )
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CI

    ## 1010 韓顯符精細二十四氣晝夜刻表 × 明代粗表 24/24 量化重放

    Status: **RECEIVED SONGSHI PHYSICAL WITNESS DIRECTLY COLLATED / RECORDED 1010 HAN XIANFU TECHNICAL EVENT DATE SEPARATED FROM SURVIVING COPY DATE / 147-UNIT RESIDUAL DENOMINATOR INFERRED BY 100-KE CONSERVATION / FULL 24-TERM MING COARSE TABLE DIRECTLY RECOLLATED / 24/24 SINGLE-THRESHOLD QUANTIZATION COMPATIBILITY CLOSED / MODERN 0.5 ROUNDING REJECTED BY DAHAN-XIAOXUE / EXACT HISTORICAL ROUNDING INSTRUCTION AND DIRECT TEXTUAL GENEALOGY STILL OPEN / SANMING STILL REQUIRES NANJING ADAPTATION / HPA-ZDATE-006 UNCHANGED / NO ALGORITHM REOPEN**

    ## 1. Direct source and date firewall

    `CADAL06060929《宋史·卷六十九~卷七十》` was downloaded from the Zhejiang University/CADAL object exposed through Wikimedia Commons and rendered page-by-page without OCR.

    ```text
    RUN={SONG_RUN}
    JOB={SONG_JOB}
    ARTIFACT={SONG_ARTIFACT}
    ARTIFACT_DIGEST={SONG_ARTIFACT_DIGEST}
    SOURCE_DJVU_SHA256={SONG_DJVU_SHA256}
    DERIVED_PDF_SHA256={SONG_PDF_SHA256}
    PAGES=152
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    Physical p119->p120 records `大中祥符三年春官正韓顯符上銅渾儀法要`, followed by the statement that the work contains a 24-qi day/night advance-retreat and sunrise/sunset ke-number established method, and then the table.

    The date firewall is mandatory:

    ```text
    1010 = recorded Northern-Song technical event/submission date
    1010 != date of the current surviving scanned physical copy
    later Songshi compilation != original Han Xianfu autograph
    modern CADAL surrogate != medieval physical object
    ```

    ## 2. The 147 residual denominator

    The physical table does **not** use modern decimal notation. Representative day/night rows are:

    ```text
    冬至  晝40刻5    夜59刻142
    大寒  晝41刻78   夜58刻69
    清明  晝52刻81   夜47刻66
    夏至  晝59刻142  夜40刻5
    ```

    In every non-equinox row:

    ```text
    integer(day) + integer(night) = 99
    residual(day) + residual(night) = 147
    total = 100 ke
    ```

    Therefore the mechanically implied residual denominator is `147` parts per ke. This is an inference from conservation, not an explicit unit-name sentence in the reviewed passage. `59刻142` must not be parsed as `59.142`.

    ## 3. Full physical comparison with the Ming coarse table

    Batch 12CE had already identified the Ming-print `《類編曆法通書》` coarse `40<->60` family. This batch re-reviews all physical pp18–24 so all 24 anchors, not only the earlier eight summer examples, participate in the replay.

    | 節氣 | 1010精細晝刻 | 明粗表晝刻 | 現代最近整數 | 閾值模型命中 |
    |---|---:|---:|---:|---:|
    {row_lines}

    Result:

    ```text
    SINGLE_THRESHOLD_24_OF_24_MATCH=true
    LARGEST_RESIDUAL_KEPT_DOWN=78
    SMALLEST_RESIDUAL_ADVANCED=81
    ADMISSIBLE_THRESHOLD=(78,81]/147
    MODERN_NEAREST_INTEGER_MATCH=22/24
    MODERN_NEAREST_INTEGER_MISSES=大寒,小雪
    ```

    At `大寒` and `小雪` the Song value is `41 + 78/147 ~= 41.530612`. Modern nearest-integer rounding would produce 42, while the direct Ming table prints 41. Therefore **modern 0.5 rounding is not the historical rule represented by this coarse table**.

    No row contains residual 79 or 80, so the physical data cannot distinguish an exact threshold of 79, 80 or 81 residual units. The correct conclusion is an interval, not an invented exact rounding command.

    ## 4. Transmission consequence

    The evidence now supports a materially stronger but still fail-closed model:

    ```text
    recorded 1010 precision 24-qi leak-clock table
        -> 24/24 mechanically compatible coarse integer 40<->60 family
           [exact textual route / rounding instruction unresolved]
        + early-Ming Nanjing/Datong locality layer
        -> later recomposed/adapted displays including 1578 Sanming
    ```

    This is not a direct-copy claim. It is a **structural ancestry candidate** with unusually strong numerical support.

    ## 5. Why this still does not generate the 1578 Sanming table

    The same coarse quantization gives values such as `小寒 40`, `立春 43`, `夏至 60`. The 1578 `《三命通會》` display instead includes `小寒 42/58`, `立春 45/55`, `雨水 47/53 then 48/52`, and `夏至 59/41`.

    Therefore Sanming is not simply the Song precision table rounded into integers. The already established Ming/Nanjing daily numerical and locality-standard layers remain necessary.

    ## 6. Product adjudication

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

    This batch changes historical transmission knowledge, not deterministic chart code.

    ## 7. Next gate

    1. locate an independent early physical witness for the same precision/coarse conversion or an explicit rounding/selection instruction that can resolve the `(78,81]/147` threshold;
    2. audit the near-contemporary `《虎鈐經》傳箭` integer 48-arrow system as a separate Song operational lineage, without assuming it copied Han Xianfu;
    3. continue the separate pre-1578 search for the exact Nanjing/Sanming `59/41` cap plus intermediate change-day fingerprint;
    4. keep Fullbook upper-five-ke -> Hai research independent from this seasonal-table ancestry work.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def main() -> None:
    continuity()
    registry()
    research()
    matrix_json()
    matrix_md()
    graph()
    graph_verifier()
    state()
    write_doc()


if __name__ == "__main__":
    main()
