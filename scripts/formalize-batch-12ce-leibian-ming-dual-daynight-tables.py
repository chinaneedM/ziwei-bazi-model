from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-CE"
PREV_ID = "BATCH-12-ZIWEI-GEXIANG-HUQIAN-COMPOSITE-TIMEKEEPING-ANCESTRY-CD"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-CE.md"
RESEARCH = "docs/research/ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-R1.json"
CADAL_SRC = "EXT-ZIWEI-LEIBIAN-LIFA-TONGSHU-CADAL02094403"
NLC_SRC = "EXT-NLC-LEIBIAN-LIFA-TONGSHU-MING-VOL1"
XING_SRC = "EXT-XINGYUNLU-GUJIN-LVLIKAO-V47-NANJING-59-41"
SANMING_SRC = "EXT-SANMING-NCL-1578-MAIN"

NLC_URL = "https://commons.wikimedia.org/wiki/File:NLC892-411999018604-67969_%E9%A1%9E%E7%B7%A8%E6%9B%86%E6%B3%95%E9%80%9A%E6%9B%B8%E5%A4%A7%E5%85%A8_%E7%AC%AC1%E5%86%8A.pdf"
XING_URL = "https://ctext.org/wiki.pl?chapter=539078&if=gb"
NLC_RUN = 34866426888
NLC_JOB = 104051295890
NLC_ARTIFACT = 10357132602
NLC_DIGEST = "sha256:8dcf2e8e7ffeb987c3c2016545b3d252ed2d0e7ab118bcd240c0b28bafcdc098"
NLC_SOURCE_SHA256 = "50a308f8adbfd7010b398cc68bc64dc66f7c1dbdcfe6470029e04aacd22e6419"
NLC_TRIGGER_COMMIT = "2c854752663dcdd446ca3888145d4b28d3361830"
NLC_CI_RUN = 34866426723
NLC_PAGE_SHA256 = {
    "20": "15325745229581c336e407d0eb405a8ef75c6d3bcf28117209f51f0484af7ce4",
    "21": "a348fb2e6c4b06323bcdbc6851aa7f09ca72a76e8ab2d9e08bd50eabf79c3bbe",
    "24": "0e94adaf05c5082b680ab210d2bf7703a5c184fe1217aa35b0ee96606870329f",
    "25": "f4305f0f8b7e766dd0f31cb4d78ecb15154e6db1820975335bd53ddda109130f",
}
FAILED_PACKAGING_RUN = 34866248129


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12CD tail in continuity verifier")
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

    cadal = next((x for x in d["sources"] if x.get("source_id") == CADAL_SRC), None)
    if cadal is not None:
        cadal["batch_12ce_dual_daynight_table_review"] = {
            "physical_scope": "CADAL02094403 volume 1 received facsimile, pp66-80 reviewed directly without OCR",
            "coarse_copper_pot_family": "24-qi day/night table with 40/60 solstitial family; includes 小滿 59/41, 芒種/夏至/小暑 60/40, 大暑 59/41",
            "fine_four_seasons_family": "四時加減晝夜節氣 one-ke ladder with 38/62 to 62/38 extrema",
            "same_received_title_preserves_both": True,
            "exact_scan_impression_date_still_unresolved": True
        }

    if NLC_SRC not in ids:
        d["sources"].append({
            "source_id": NLC_SRC,
            "title": "《類編曆法通書大全》第1冊，國家圖書館系明刻本影像",
            "author_attribution": "〔元〕宋魯珍通書（Wikimedia/NLC metadata）；received title also belongs to later layered 通書 compilation tradition",
            "historical_period": "MING_PRINT_EXACT_YEAR_UNRESOLVED_1368_1644",
            "edition": "刻本；公開書目標示明[1368-1644]；95頁；存卷一至卷四",
            "provider": "National Library of China digitization via Wikimedia Commons",
            "url": NLC_URL,
            "source_role": "DIRECT_MING_PRINT_PHYSICAL_WITNESS_FOR_COEXISTING_40_60_AND_38_62_DAY_NIGHT_TABLE_FAMILIES",
            "quality_notes": "Batch 12CE no-OCR physical review. PDF pp20-21 directly preserve the coarse copper-pot/24-qi family including 小滿59/41, 芒種60/40, 夏至60/40, 小暑60/40, 大暑59/41. PDF pp24-25 directly preserve 四時加減晝夜節氣 with a fine one-ke ladder from winter 38/62 toward summer 62/38. Exact Ming impression year is unresolved, so this object proves coexistence in Ming-print transmission but is not automatically a pre-1578 ancestor of Sanming Tonghui."
        })
    if XING_SRC not in ids:
        d["sources"].append({
            "source_id": XING_SRC,
            "title": "邢雲路《古今律曆考》卷四十七《刻漏》",
            "author": "邢雲路",
            "historical_period": "MING_WANLI_LATE_EXPLANATORY_CONTROL",
            "edition": "received text; NCL separately catalogs a 1600 Wanli-28 print of the work",
            "provider": "Chinese Text Project / later Ming textual witness",
            "url": XING_URL,
            "source_role": "LATER_MING_EXPLANATORY_CONTROL_FOR_NANJING_DATONG_59_41_VS_YANDU_SHOUSHI_62_38",
            "quality_notes": "卷47 explicitly says early-Ming Datong day/night change was recalibrated to Nanjing clepsydra: summer-solstice day and winter-solstice night 59 ke, reverse 41; Yandu Shoushi is 62/38. The 1600 work is later than the 1578 Sanming witness and therefore cannot be promoted into its ancestor; it is explanatory control only."
        })
    d["access_date"] = "2026-09-14"
    dump(p, d)


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-LEIBIAN-MING-DUAL-DAYNIGHT-TABLES-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does a directly dated-to-Ming-print witness of Leibian Lifa Tongshu preserve multiple day/night-ke table families in the same physical volume, and what does that imply for Sanming Tonghui's 'Shoushi calendar' language and 59/41 display?",
        "nlc_ming_print_witness": {
            "source_id": NLC_SRC,
            "bibliographic_scope": "Wikimedia/NLC metadata: 刻本, 明[1368-1644], 95 pages, author field 〔元〕宋魯珍通書; exact impression year unresolved",
            "workflow_run_id": NLC_RUN,
            "job_id": NLC_JOB,
            "artifact_id": NLC_ARTIFACT,
            "artifact_digest": NLC_DIGEST,
            "source_pdf_sha256": NLC_SOURCE_SHA256,
            "page_count": 95,
            "page_sha256": NLC_PAGE_SHA256,
            "render_trigger_commit": NLC_TRIGGER_COMMIT,
            "exact_head_ci_run": NLC_CI_RUN,
            "ocr_used_for_glyph_claims": False,
            "failed_prior_packaging_run": {
                "run_id": FAILED_PACKAGING_RUN,
                "source_download_succeeded": True,
                "all_95_pages_rendered": True,
                "failure_scope": "contact-sheet filename padding bug only",
                "content_negative_authority": False
            }
        },
        "coarse_copper_pot_24qi_table": {
            "physical_pages": [20, 21],
            "observed_rows": [
                "立夏 57/43",
                "小滿 59/41",
                "芒種 60/40",
                "夏至 60/40",
                "小暑 60/40",
                "大暑 59/41",
                "立秋 57/43",
                "處暑 55/45"
            ],
            "broader_received_sequence_extrema": "winter-solstice family 40/60, summer-solstice family 60/40",
            "sanming_exact_table_equivalence": False,
            "decisive_difference": "This coarse table has 夏至 60/40; the 1578 Sanming display has 夏至 59/41."
        },
        "fine_four_seasons_daynight_table": {
            "physical_pages": [24, 25],
            "heading": "四時加減晝夜節氣",
            "observed_structure": "one-ke ladder from winter 38/62 upward through 39/61, 40/60, 41/59, 42/58 ... and reaches summer 62/38",
            "yandu_shoushi_like_extrema": "38/62 <-> 62/38",
            "sanming_exact_table_equivalence": False,
            "decisive_difference": "The fine table reaches 62/38, not Sanming's summer-solstice 59/41."
        },
        "dual_table_coexistence": {
            "same_physical_ming_print_volume": True,
            "families": ["coarse 24-qi copper-pot 40/60 family", "fine 四時加減 38/62 family"],
            "historical_consequence": "A Ming calendrical/almanac transmission can preserve multiple day/night-ke conventions side-by-side. Therefore a generic reference to 授時/曆分 cannot safely be collapsed to one literal Yandu 62/38 table without edition- and locus-specific evidence.",
            "exact_sanming_parent_proved": False,
            "pre1578_ancestry_proved_by_this_copy": False,
            "reason_pre1578_not_proved": "The physical object is bibliographically Ming but its exact impression year within 1368-1644 is unresolved."
        },
        "xingyunlu_later_explanatory_control": {
            "source_id": XING_SRC,
            "work_print_control": "NCL catalogs a Wanli-28 / 1600 print of 古今律曆考",
            "received_v47_reading": "Early-Ming Datong recalibrated day/night change to Nanjing clepsydra: 夏至晝/冬至夜 59 ke, 冬至晝/夏至夜 41 ke; Yandu Shoushi 62/38.",
            "explains_nanjing_59_41_layer": True,
            "can_be_ancestor_of_1578_sanming": False,
            "use": "later explanatory control only"
        },
        "sanming_comparison": {
            "source_id": SANMING_SRC,
            "displayed_examples": ["小寒 42/58", "立春 45/55", "雨水 47/53 then 48/52", "夏至 59/41"],
            "equals_coarse_leibian_table": False,
            "equals_fine_leibian_table": False,
            "nanjing_59_41_hypothesis_materially_strengthened": True,
            "exact_pre1578_table_parent_closed": False,
            "best_current_model": "older one-ke leak-arrow ladder + coexistence of multiple calendrical table families + Ming locality adaptation, with Nanjing 59/41 strongly explained by later Ming technical testimony"
        },
        "adjudication": {
            "ming_print_dual_table_coexistence_physically_attested": True,
            "one_literal_shoushi_table_assumption_rejected": True,
            "sanming_table_exactly_equals_either_leibian_table": False,
            "nanjing_59_41_explanatory_layer_supported": True,
            "exact_pre1578_sanming_table_genealogy_closed": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "reason": "The batch materially narrows the historical table ecology but does not establish the Fullbook-specific upper-five-ke -> previous-night Hai branch rule.",
            "remaining_blockers": [
                "find a securely pre-1578 direct Ming/Nanjing witness that actually prints or generates the 59/41 summer-solstice layer with Sanming-like term anchors",
                "close the precise stemmatic/generative bridge from that table to the 1578 Sanming display",
                "independently close the Fullbook upper-five-ke -> previous-night Hai branch mechanism"
            ]
        }
    })


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CE

    ## 明刻《類編曆法通書大全》同卷雙表：40/60 銅壺二十四氣表與 38/62《四時加減晝夜節氣》並存

    Status: **INDEPENDENT MING-PRINT PHYSICAL COPY DIRECTLY CONFIRMS TWO DIFFERENT DAY/NIGHT-KE TABLE FAMILIES IN THE SAME VOLUME / COARSE 24-QI COPPER-POT FAMILY REACHES 60/40 AND CONTAINS 59/41 ADJACENT ROWS / FINE FOUR-SEASONS TABLE REACHES 62/38 / SANMING 59/41 AT SUMMER SOLSTICE EQUALS NEITHER TABLE EXACTLY / LATER 1600 XING-YUNLU CONTROL EXPLICITLY EXPLAINS NANJING DATONG 59/41 VS YANDU SHOUSHI 62/38 / EXACT PRE-1578 SANMING TABLE PARENT STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this follows 12CD

    Batch 12CD separated the older hundred-ke prose lineage from the older 40↔60 stepwise leak-arrow numeric lineage. The unresolved layer was Ming adaptation: how can a mantic text say `授時曆分之` yet display a table that is not the literal Yandu Shoushi 62/38 table?

    The decisive new evidence is that a single Ming-print calendrical/almanac volume physically preserves **more than one day/night-ke convention**.

    ## 2. Independent Ming-print physical witness

    Controlling public object:

    ```text
    TITLE=類編曆法通書大全 第1冊
    METADATA_AUTHOR=〔元〕宋魯珍通書
    EDITION=刻本
    PUBLICATION=明[1368-1644]
    PAGE_COUNT=95
    EXACT_IMPRESSION_YEAR=UNRESOLVED
    ```

    Evidence chain:

    ```text
    RUN={NLC_RUN}
    JOB={NLC_JOB}
    ARTIFACT={NLC_ARTIFACT}
    ARTIFACT_DIGEST={NLC_DIGEST}
    SOURCE_PDF_SHA256={NLC_SOURCE_SHA256}
    P20_SHA256={NLC_PAGE_SHA256['20']}
    P21_SHA256={NLC_PAGE_SHA256['21']}
    P24_SHA256={NLC_PAGE_SHA256['24']}
    P25_SHA256={NLC_PAGE_SHA256['25']}
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    The earlier run `{FAILED_PACKAGING_RUN}` successfully downloaded the same source and rendered all 95 pages, but its contact-sheet step failed because of a page-filename padding bug. It has **no content-negative authority**. The corrected workflow run above succeeded and produced the durable artifact.

    ## 3. First physical table: coarse 24-qi copper-pot family

    PDF pp20-21 directly show the seasonal rows. Secure examples include:

    ```text
    立夏 57/43
    小滿 59/41
    芒種 60/40
    夏至 60/40
    小暑 60/40
    大暑 59/41
    立秋 57/43
    處暑 55/45
    ```

    The full received family is the older 40/60-style copper-pot table. Crucially, it contains `59/41`, but **not at the same solar-term anchor as Sanming**: this physical table prints `夏至 60/40`, whereas the 1578 Sanming display prints `夏至 59/41`.

    Therefore:

    ```text
    shared number 59/41 != exact table identity
    ```

    ## 4. Second physical table: fine 38/62 ladder

    On PDF p24 the left leaf directly opens:

    ```text
    四時加減晝夜節氣
    ```

    and begins the winter ladder at `38/62`, then `39/61`, `40/60`, `41/59`, `42/58` and onward. PDF p25 continues the one-ke progression and reaches the summer range culminating at `62/38`.

    This is structurally Yandu/Shoushi-like, but it is likewise **not** Sanming's displayed summer-solstice `59/41` table.

    ## 5. The key historical result is coexistence, not one winning table

    The same Ming-print physical volume therefore preserves at least:

    ```text
    A. coarse 24-qi copper-pot 40/60 family
    B. fine 四時加減 38/62 family
    ```

    That directly falsifies an overly simple historical normalization:

    ```text
    'mentions Shoushi/calendar division' -> must mean one unique literal 62/38 table everywhere
    ```

    Premodern calendrical/almanac transmission could carry multiple day/night-ke schemes side by side. A mantic author could inherit prose, numerical ladders, locality conventions and term anchors from different layers.

    ## 6. Later Ming explanatory control: Nanjing 59/41

    邢雲路《古今律曆考》卷47 explicitly contrasts two geographic standards:

    ```text
    Yandu / Shoushi:  夏至晝 62 / 夜 38
    early-Ming Nanjing Datong: 夏至晝 59 / 夜 41
    ```

    The work is securely represented by a Wanli-28 (1600) print, so it is **later than the 1578 Sanming witness**. It cannot be used as Sanming's ancestor. Its value is explanatory: it proves that the Ming technical tradition itself understood `59/41` as a Nanjing-calibrated Datong layer distinct from Yandu `62/38`.

    This materially strengthens—but does not close—the hypothesis that Sanming's `59/41` belongs to a Ming locality-adaptation layer rather than the literal Yandu Shoushi table.

    ## 7. Chronology firewall

    The NLC Leibian object is catalogued only as Ming `[1368-1644]`. Therefore this batch may say:

    ```text
    Ming-print transmission physically preserves both table families.
    ```

    It may **not** say:

    ```text
    this exact physical impression definitely predates 1578;
    therefore Sanming copied this exact book.
    ```

    That ancestor claim remains open until an edition securely dated before 1578, or another direct pre-1578 Ming/Nanjing table, is locked.

    ## 8. Product adjudication

    For `HPA-ZDATE-006`:

    - Ming-print dual-table coexistence: **physically attested**;
    - one-literal-Shoushi-table assumption: **rejected**;
    - Sanming = coarse Leibian table: **no**;
    - Sanming = fine 38/62 table: **no**;
    - Nanjing 59/41 explanatory layer: **strongly supported by later Ming technical testimony**;
    - exact pre-1578 table parent: **open**;
    - upper-Zi -> Hai vote: **0**;
    - runtime candidate/winner/collapse: **none**;
    - algorithm reopen: **no**;
    - `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

    ## 9. Next gate

    Search specifically for a **securely pre-1578 Ming/Nanjing physical or edition-scoped witness** that prints or generates `夏至 59/41` and ideally carries Sanming-like intermediate solar-term anchors. Priority: early Datong almanacs, Nanjing official clepsydra/day-night tables, pre-1578 tongshu recensions, and calendrical appendices. Only then can the adaptation layer move from explanatory model to chronological genealogy.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12ce_leibian_ming_dual_daynight_tables"] = {
        "source_ids": [CADAL_SRC, NLC_SRC, XING_SRC, SANMING_SRC],
        "ming_print_dual_table_coexistence_physically_attested": True,
        "coarse_40_60_family_and_fine_38_62_family_same_volume": True,
        "sanming_exactly_equals_coarse_table": False,
        "sanming_exactly_equals_fine_table": False,
        "later_ming_nanjing_59_41_explanatory_control": True,
        "exact_pre1578_sanming_table_parent_closed": False,
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
    if "## Progress through Batch 12CE" not in md:
        md += dedent('''

        ## Progress through Batch 12CE

        - An independent NLC-derived Ming-print physical copy of 《類編曆法通書大全》第1冊 directly confirms two day/night-ke systems in the same volume: a coarse 24-qi copper-pot 40/60 family and a fine `四時加減晝夜節氣` 38/62 one-ke ladder.
        - The coarse table physically includes `小滿 59/41`, `夏至 60/40`, `大暑 59/41`; the fine table reaches `62/38`. Therefore Sanming's `夏至 59/41` equals neither table exactly, while dual-table coexistence materially strengthens a mixed/adapted lineage model.
        - A later Ming control, Xing Yunlu's 《古今律曆考》卷47, explicitly distinguishes Nanjing Datong `59/41` from Yandu Shoushi `62/38`. Because the work is later than the 1578 Sanming witness, this is explanatory control, not ancestor proof.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; no Hai vote, runtime winner, candidate collapse or algorithm reopen is introduced.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.90.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12CE physically confirms that a Ming-print Leibian Lifa Tongshu volume preserves both a coarse 40/60 copper-pot day/night table and a fine 38/62 four-seasons table; historical transmission is therefore not reducible to one literal Shoushi table.",
        "Sanming's 夏至59/41 equals neither physically reviewed Leibian table exactly; later 1600 Xing Yunlu testimony strongly explains a Nanjing Datong 59/41 layer distinct from Yandu Shoushi 62/38 but cannot be backdated as Sanming ancestry.",
        "Next gate: securely pre-1578 Ming/Nanjing physical or edition-scoped witness for 夏至59/41 plus Sanming-like intermediate anchors; Fullbook upper-five-ke -> Hai remains independently unresolved."
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
