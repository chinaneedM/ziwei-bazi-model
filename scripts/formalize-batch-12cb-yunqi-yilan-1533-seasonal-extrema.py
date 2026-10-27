from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-YUNQI-YILAN-1533-SEASONAL-EXTREMA-CB"
PREV_ID = "BATCH-12-ZIWEI-SANMING-SHOUSHI-LOCALITY-AND-TABLE-MISMATCH-CA"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-YUNQI-YILAN-1533-SEASONAL-EXTREMA-CB.md"
RESEARCH = "docs/research/ZIWEI-YUNQI-YILAN-1533-SEASONAL-EXTREMA-R1.json"
SRC = "EXT-XUXIU-SIKU-0983-YUNQI-YILAN-1533-CHENGQIAO"
URL = "https://commons.wikimedia.org/wiki/File:%E7%BA%8C%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%AC%AC0983%E5%86%8A.pdf"

WORKFLOW_RUN = 34859366584
ARTIFACT_ID = 10354496404
ARTIFACT_DIGEST = "sha256:65f611f28d8989ae4d2dc7d25e4ee2ed6e4075b065d8ee36db2bda090a2aff0a"
SOURCE_PDF_SHA256 = "a1b0bcba30eaccacd7860d6444e7e7811d98b3fc3649b5cfcd7657edb31e0b0c"
PAGE8_SHA256 = "fcb0597a86bfaeead333ce610ec20114e119680f2583dffa2259dca3e83dadc6"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12CA tail in continuity verifier")
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
    if SRC not in ids:
        d["sources"].append({
            "source_id": SRC,
            "title": "汪機《運氣易覽》三卷，明嘉靖十二年程鐈刻本影印",
            "author": "汪機",
            "historical_period": "MING_JIAJING_12_1533_PRINT",
            "edition": "明嘉靖十二年（1533）程鐈刻本；《續修四庫全書》第983冊影印中國科學院圖書館藏本",
            "provider": "《續修四庫全書》影印 / Wikimedia Commons delivery",
            "url": URL,
            "source_role": "DIRECT_PRE1578_PHYSICAL_MEDICAL_YUNQI_CONTROL_FOR_SEASONAL_DAY_NIGHT_KE_EXTREMA",
            "quality_notes": "Workflow run 34859366584 directly renders PDF p8 without OCR. The physical page headed 論四時氣候 reads 晝夜分五十刻亦陰陽之中分, 夏至日長不過六十刻, and 冬至日短不過四十刻. This is a pre-1578 conceptual/disciplinary parallel for the 50/50 and 60/40 seasonal family, not an exact witness for Sanming Tonghui's distinctive multi-point 42/58...59/41 table and not proof of direct genealogy."
        })
    d["access_date"] = "2026-09-14"
    dump(p, d)


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-YUNQI-YILAN-1533-SEASONAL-EXTREMA-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does the 1533 Chengqiao-print Yunqi Yilan preserve the exact pre-1578 numeric seasonal day/night-ke table used in Sanming Tonghui, or only the broader seasonal extrema tradition?",
        "physical_witness": {
            "source_id": SRC,
            "work": "運氣易覽",
            "author": "汪機",
            "edition": "明嘉靖十二年（1533）程鐈刻本",
            "facsimile_container": "續修四庫全書第0983冊",
            "workflow_run_id": WORKFLOW_RUN,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "source_pdf_sha256": SOURCE_PDF_SHA256,
            "pdf_page": 8,
            "page_render_sha256": PAGE8_SHA256,
            "ocr_used_for_glyph_claims": False
        },
        "direct_physical_collation": {
            "heading": "論四時氣候",
            "readings": [
                "晝夜分五十刻亦陰陽之中分",
                "夏至日長不過六十刻陽至此而極",
                "冬至日短不過四十刻陰至此而極"
            ],
            "semantic_scope": "Seasonal/equinox-solstice day-night ke extrema inside a medical yunqi exposition.",
            "independent_pre1578_conceptual_parallel": True
        },
        "sanming_comparison": {
            "sanming_reference_source_id": "EXT-SANMING-NCL-1578-MAIN",
            "sanming_distinctive_points": [
                "小寒 42/58",
                "立春 45/55",
                "雨水 47/53 then 48/52",
                "春秋分 near/equal 50/50",
                "夏至 59/41"
            ],
            "yunqi_yilan_exact_multipoint_table_witness": False,
            "exact_numeric_table_equivalence": False,
            "reason": "The reviewed edition-scoped 論四時氣候 locus gives equinoctial 50/50 and solstitial bounds 60/40, but does not itself print the Sanming multi-point seasonal table; Sanming's displayed summer-solstice value is 59/41 rather than an exact 60/40 row.",
            "direct_genealogy_to_sanming_proved": False,
            "candidate_parent_rejected_as_exact_numeric_table_equivalent": True,
            "broader_shared_tradition_remains_possible": True
        },
        "adjudication": {
            "pre1578_40_60_medical_yunqi_tradition_attested": True,
            "pre1578_50_50_equinox_language_attested": True,
            "exact_sanming_table_provenance_closed": False,
            "sanming_table_can_be_labeled_yunqi_yilan_table": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "most_conservative_reading": "The 1533 Yunqi Yilan physically proves an earlier medical-yunqi 50/50 and 60/40 seasonal-extrema tradition, but it does not supply the exact multi-point table printed by Sanming Tonghui. Exact table genealogy therefore remains open."
        },
        "received_text_cross_checks_not_glyph_authority": [
            "https://ctext.org/wiki.pl?chapter=4158339&if=gb",
            "https://jicheng.tw/tcm/book/%E9%81%8B%E6%B0%A3%E6%98%93%E8%A6%BD/index.html"
        ],
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "remaining_blockers": [
                "trace the exact pre-1578 source of the Sanming multi-point 42/58...59/41 seasonal table",
                "identify the locality/standard encoded by that exact table rather than the broader 40/60 extrema tradition",
                "independently close the Fullbook upper-five-ke -> previous-night Hai branch mechanism"
            ]
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


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CB

    ## 1533《運氣易覽》季节刻漏实体校勘：50/50、60/40 传统与《三命通會》精确表谱不等同

    Status: **1533 CHENGQIAO-PRINT YUNQI YILAN PHYSICALLY CONFIRMS PRE-1578 MEDICAL-YUNQI 50/50 EQUINOX AND 60/40 SOLSTICE EXTREMA / REVIEWED 論四時氣候 LOCUS IS NOT THE EXACT SANMING MULTI-POINT TABLE / DIRECT YUNQI-YILAN→SANMING GENEALOGY NOT PROVED / BROADER SHARED SEASONAL TIMEKEEPING TRADITION REMAINS POSSIBLE / EXACT SANMING TABLE PROVENANCE STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this batch follows 12CA

    Batch 12CA rejected the shortcut that Wan Minying's displayed table is simply the exact Yandu Shoushi 62/38 table. Its next gate was to trace the precise pre-1578 ancestry of the distinctive Sanming sequence rather than stop at generic 40/60 endpoints.

    A high-value pre-1578 candidate is Wang Ji's medical-yunqi work 《運氣易覽》, surviving here in a facsimile identified as the Ming Jiajing 12 (1533) Chengqiao print.

    ## 2. Physical witness and machine evidence

    The full source is 《續修四庫全書》第983冊, which reproduces the 1533 Chengqiao-print 《運氣易覽》. A dedicated no-OCR workflow rendered the relevant physical page.

    ```text
    WORKFLOW_RUN={WORKFLOW_RUN}
    ARTIFACT={ARTIFACT_ID}
    ARTIFACT_DIGEST={ARTIFACT_DIGEST}
    SOURCE_PDF_SHA256={SOURCE_PDF_SHA256}
    TARGET_PDF_PAGE=8
    TARGET_PAGE_SHA256={PAGE8_SHA256}
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    PDF p8 directly carries the heading `論四時氣候`.

    ## 3. Direct physical readings

    No OCR is used for the glyph claims below. The physical page directly reads:

    ```text
    晝夜分五十刻亦陰陽之中分
    夏至日長不過六十刻陽至此而極
    冬至日短不過四十刻陰至此而極
    ```

    Therefore a medical `運氣` source printed in 1533 unquestionably transmits the broad seasonal structure:

    ```text
    equinox -> day/night midpoint at 50/50
    summer-solstice day length -> not beyond 60 ke
    winter-solstice day length -> not beyond 40 ke
    ```

    This predates the 1578 Sanming physical witness and materially strengthens the pre-Sanming history of the 40/60 family.

    ## 4. It is not the exact Sanming numeric table

    The decisive distinction is **table identity**, not thematic similarity.

    The reviewed 《運氣易覽·論四時氣候》 locus gives extrema/bounds. It does not itself print the distinctive Sanming multi-point table such as:

    ```text
    小寒 42/58
    立春 45/55
    雨水 47/53 -> 48/52
    春秋分 near/equal 50/50
    夏至 59/41
    ```

    In particular, `夏至日長不過六十刻` is a bound/extreme statement; it is not the same numeric row as Sanming's displayed `59/41`.

    Hence the following inference is forbidden:

    ```text
    1533 Yunqi Yilan contains the exact Sanming table
      -> therefore Sanming copied this table from Yunqi Yilan
    ```

    The evidence supports a **broader shared seasonal-timekeeping tradition**, not direct textual genealogy or exact numeric-table equivalence.

    ## 5. Philological consequence

    This result is useful precisely because it separates three layers that would otherwise be conflated:

    1. general hundred-ke seasonal extrema (`40/60`, `50/50`);
    2. an interpolated or conventionally rounded multi-point seasonal table;
    3. a locality-specific official-calendar table such as Yandu Shoushi `38/62`.

    The 1533 medical witness closes layer 1 before Sanming. It does not identify layer 2's exact ancestor or location, and it does not convert layer 3 into Sanming's table.

    ## 6. Product adjudication

    For `HPA-ZDATE-006`:

    - pre-1578 medical-yunqi 50/50 and 60/40 tradition: **physically attested**;
    - exact Yunqi Yilan = Sanming multi-point table: **rejected**;
    - direct Yunqi Yilan -> Sanming genealogy: **not proved**;
    - exact Sanming table provenance/locality: **open**;
    - upper-Zi -> Hai mechanical vote: **0**;
    - new runtime candidate: **none**;
    - runtime winner: **none**;
    - algorithm reopen: **no**;
    - `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

    ## 7. Next gate

    Search the exact multi-point fingerprint, not merely the endpoints. Priority strings include combinations of `小寒 42/58`, `立春 45/55`, `雨水 47/53 -> 48/52`, and `夏至 59/41` in pre-1578 calendrical, leak-clock, almanac, medical-yunqi and mantic sources. Later exact matches may establish downstream transmission or a shared ancestor, but by chronology cannot be promoted into an ancestor of the 1578 witness.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12cb_yunqi_yilan_1533_seasonal_extrema"] = {
        "source_ids": [SRC, "EXT-SANMING-NCL-1578-MAIN"],
        "pre1578_medical_yunqi_50_50_60_40_physical_witness": True,
        "yunqi_yilan_exact_sanming_multipoint_table_equivalence": False,
        "direct_yunqi_yilan_to_sanming_genealogy_proved": False,
        "broader_shared_seasonal_timekeeping_tradition_possible": True,
        "exact_sanming_table_provenance_closed": False,
        "upper_zi_to_hai_mechanical_vote_increment": 0,
        "new_runtime_candidate_created": False,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH
    }
    dump(p, d)

    mdp = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = mdp.read_text(encoding="utf-8")
    if "## Progress through Batch 12CB" not in md:
        md += dedent('''

        ## Progress through Batch 12CB

        - A no-OCR physical review of the 1533 Chengqiao-print 《運氣易覽·論四時氣候》 directly confirms `晝夜分五十刻`, `夏至日長不過六十刻`, and `冬至日短不過四十刻` in a pre-1578 medical-yunqi witness.
        - This closes an earlier 50/50 + 60/40 conceptual/disciplinary parallel, but the reviewed locus does not print Sanming Tonghui's distinctive multi-point 42/58...59/41 table. Exact table identity and direct genealogy are therefore not established.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no Hai-branch vote, runtime candidate, winner, collapse or algorithm reopen is introduced.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.87.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12CB physically closes a pre-1578 medical-yunqi 50/50 and 60/40 seasonal-extrema witness in the 1533 Chengqiao-print Yunqi Yilan.",
        "The reviewed Yunqi Yilan locus is not the exact Sanming Tonghui 42/58...59/41 multi-point table; direct genealogy and the exact Sanming table locality remain unresolved.",
        "Next gate: trace the distinctive Sanming multi-point numeric fingerprint in pre-1578 calendrical, leak-clock, almanac, medical-yunqi and mantic sources rather than generic 40/60 endpoints."
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-14"
    dump(p, d)


def main() -> None:
    continuity()
    registry()
    write_research()
    write_doc()
    matrix()
    state()


if __name__ == "__main__":
    main()
