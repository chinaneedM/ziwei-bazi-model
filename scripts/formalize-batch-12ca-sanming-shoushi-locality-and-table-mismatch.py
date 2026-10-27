from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-SANMING-SHOUSHI-LOCALITY-AND-TABLE-MISMATCH-CA"
PREV_ID = "BATCH-12-ZIWEI-SANMING-SHOUSHI-BIRTH-TIME-BRIDGE-BZ"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANMING-SHOUSHI-LOCALITY-AND-TABLE-MISMATCH-CA.md"
RESEARCH = "docs/research/ZIWEI-SANMING-SHOUSHI-LOCALITY-AND-TABLE-MISMATCH-R1.json"
AT_RESEARCH = "docs/research/ZIWEI-SANMING-TONGHUI-1578-TIMEKEEPING-PHYSICAL-COLLATION-R1.json"

SRC_YUAN = "EXT-YUANSHI-V55-SHOUSHI-JIUFU-LOCALITY"
SRC_BAIBIAN = "EXT-BAIBIAN-V54-DIZHONG-YANDU-DAYNIGHT"
SRC_HUQIAN = "EXT-TIANYIGE-HUQIANJING-MING-CHUANJIAN"
SRC_HUQIAN_TEXT = "EXT-WIKISOURCE-HUQIANJING-V7-CHUANJIAN"

URL_YUAN = "https://ctext.org/wiki.pl?chapter=985472&if=gb"
URL_BAIBIAN = "https://zh.wikisource.org/wiki/%E7%A8%97%E7%B7%A8_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B7054"
URL_HUQIAN = "https://commons.wikimedia.org/wiki/File:Tianyige-330000-1705-0004205_%E8%99%8E%E9%88%90%E7%B6%93%E4%BA%8C%E5%8D%81%E5%8D%B7_%E5%AE%8B%E8%A8%B1%E6%B4%9E%E6%92%B0_%E6%98%8E%E5%88%BB%E6%9C%AC.pdf"
URL_HUQIAN_TEXT = "https://zh.wikisource.org/zh-hans/%E8%99%8E%E9%88%90%E7%B6%93_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B707"

HUQIAN_RUN = 34832306143
HUQIAN_ARTIFACT = 10342711240
HUQIAN_DIGEST = "sha256:87bd11223e5fdbfe1ec79b2bc4e2a7577fbe459559e0386287c96f3074f2f27d"
HUQIAN_PDF_SHA256 = "52ea8f81c8cd6ccc1000db4bb15a07b18b5e2196966a3ebdcf740bc423686dfc"
HUQIAN_P74_SHA256 = "a86cade9b99ed1b5cc943370e4b66e914d7968bc08943225bb99530fb15721ab"
HUQIAN_P75_SHA256 = "cc7546f4d93b85fb0327e30cead9c994ae017d81dc2f1dd1b86e994babb3cf83"
HUQIAN_P76_SHA256 = "2136201c372c0f8ea51dce46c1babcfc135758a98c775afa52c09c39fc8d5534"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12BZ tail in continuity verifier")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch doc")
    p.write_text(s, encoding="utf-8")


def registry() -> str:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    sanming_id = None
    for src in d["sources"]:
        if src.get("research_artifact") == AT_RESEARCH:
            sanming_id = src["source_id"]
            break
    if not sanming_id:
        raise SystemExit("cannot locate 1578 Sanming source")
    ids = {x.get("source_id") for x in d["sources"]}
    items = [
        {
            "source_id": SRC_YUAN,
            "title": "《元史》卷55《授時曆經下》九服晝夜刻與漏刻地方校準術",
            "historical_period": "YUAN_CALENDAR_METHOD_PRESERVED_IN_MING_YUANSHI",
            "provider": "Chinese Text Project / Wikisource received text",
            "url": URL_YUAN,
            "source_role": "PRIMARY_OR_NEAR_PRIMARY_CONTROL_FOR_SHOUSHI_REGIONAL_LOCALITY_CAPABILITY",
            "quality_notes": "Explicitly says nine-region day/night ke and central-star rates are computed by local pole altitude; local leak-clock values may be established by instrument observation or water clock. This proves system-level locality capability, not Wan Minying birthplace localization."
        },
        {
            "source_id": SRC_BAIBIAN,
            "title": "唐順之《稗編》卷54所錄馬端臨《晝夜刻數》",
            "historical_period": "MING_COMPILATION_TRANSMITTING_EARLIER_TECHNICAL_DISCUSSION",
            "provider": "Wikisource / Siku transmission",
            "url": URL_BAIBIAN,
            "source_role": "HISTORICAL_COMPARATIVE_CONTROL_FOR_DIZHONG_40_60_VS_YANDU_SHOUSHI_62_38",
            "quality_notes": "Distinguishes Cai's 地中 60/40 extremes from Shoushi-calendar Yandu 62/38 extremes and attributes the difference to geography. Useful comparative control, not direct proof of Sanming table genealogy."
        },
        {
            "source_id": SRC_HUQIAN,
            "title": "天一閣藏明刻本《虎鈐經》卷七《傳箭》第七十六",
            "author": "許洞",
            "historical_period": "SONG_WORK_SURVIVING_IN_MING_PRINT",
            "provider": "Tianyige Museum scan via Wikimedia Commons",
            "url": URL_HUQIAN,
            "source_role": "DIRECT_PHYSICAL_CROSS_DISCIPLINARY_CONTROL_FOR_40_60_SEASONAL_LEAK_ARROW_TABLE_TRADITION",
            "quality_notes": "No-OCR direct review. PDF p74 begins 傳箭第七十六 and physically prints one-day hundred-ke framework plus winter-solstice 40/60; p76 physically reaches summer-solstice 60/40. This is not a genealogy vote for Sanming Tonghui."
        },
        {
            "source_id": SRC_HUQIAN_TEXT,
            "title": "《虎鈐經》卷七《傳箭》第七十六 received transcription",
            "historical_period": "SONG_WORK_RECEIVED_TRANSMISSION",
            "provider": "Wikisource / Siku transmission",
            "url": URL_HUQIAN_TEXT,
            "source_role": "TRANSCRIPTION_CONTROL_FOR_FULL_40_60_ARROW_SEQUENCE",
            "quality_notes": "Used with the Tianyige physical witness to inspect the full seasonal sequence. Exact glyph-critical claims remain anchored to the physical scan."
        }
    ]
    for x in items:
        if x["source_id"] not in ids:
            d["sources"].append(x)
    d["access_date"] = "2026-09-14"
    dump(p, d)
    return sanming_id


def write_research(sanming_id: str) -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-SANMING-SHOUSHI-LOCALITY-AND-TABLE-MISMATCH-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Does the Shoushi-calendar bridge in Sanming Tonghui authorize a specific locality standard such as Dadu/Yandu, and is Wan Minying's displayed seasonal table the Shoushi Yandu table?",
        "shoushi_locality_control": {
            "source_id": SRC_YUAN,
            "direct_received_text": [
                "其九服所在晝夜刻分及中星諸率並準隨處北極出地度數推之",
                "求九服所在漏刻各於所在以儀測驗或下水漏以定其處冬至或夏至夜刻"
            ],
            "adjudication": "SHOUSHI_SYSTEM_REGIONAL_LOCALITY_CAPABILITY_SOURCE_CLOSED",
            "mechanical_scope": "Local day/night ke and related rates are explicitly location-dependent and may be calibrated by local latitude/instrument/water-clock observation.",
            "wan_minying_birthplace_localization_proved": False
        },
        "historical_standard_comparison": {
            "source_id": SRC_BAIBIAN,
            "reported_dizhong_extremes": {"summer_day": 60, "summer_night": 40, "winter_day": 40, "winter_night": 60},
            "reported_yandu_shoushi_extremes": {"summer_day": 62, "summer_night": 38, "winter_day": 38, "winter_night": 62},
            "semantic_value": "Historical technical tradition explicitly recognized that 40/60 and 62/38 can represent different geographic standards rather than mere scribal disagreement.",
            "authority_boundary": "Ming compilation transmitting earlier discussion; comparative control only."
        },
        "sanming_actual_table": {
            "source_id": sanming_id,
            "physical_and_received_controls": [
                "Ming physical juan-2 witnesses reviewed in Batches 12AT/12BZ",
                "received/Siku text lists 小寒 42/58, 立春 45/55, 雨水 47/53 then 48/52, 春秋分 near/equal 50/50, 夏至 59/41"
            ],
            "exact_yandu_62_38_equivalence": False,
            "reason": "The displayed mantic table does not use the Yandu Shoushi 62/38 solstitial extreme; the summer-solstice line is 59/41 and the winter sequence belongs to a different rounded/simplified table structure.",
            "beijing_dadu_runtime_binding_authorized": False
        },
        "huqianjing_cross_disciplinary_physical_control": {
            "source_ids": [SRC_HUQIAN, SRC_HUQIAN_TEXT],
            "workflow_run_id": HUQIAN_RUN,
            "artifact_id": HUQIAN_ARTIFACT,
            "artifact_digest": HUQIAN_DIGEST,
            "pdf_sha256": HUQIAN_PDF_SHA256,
            "target_page_hashes": {"74": HUQIAN_P74_SHA256, "75": HUQIAN_P75_SHA256, "76": HUQIAN_P76_SHA256},
            "direct_no_ocr_findings": [
                "PDF p74: 傳箭第七十六; 一日十二時合一百刻; 冬至第一箭晝四十刻夜六十刻",
                "PDF p76: summer transition reaches 夏至 first arrow with 晝六十刻夜四十刻"
            ],
            "full_received_sequence_role": "Shows the 40/60 seasonal arrow-table family is a wider premodern timekeeping tradition and is not unique to later mantic texts.",
            "direct_genealogy_to_sanming": False,
            "independent_mantic_vote_increment": 0,
            "ocr_used_for_glyph_claims": False
        },
        "adjudication": {
            "shoushi_regional_locality_algorithm_attested": True,
            "wan_minying_birthplace_localization_proved": False,
            "sanming_table_exact_dadu_shoushi_equivalence": False,
            "dadu_beijing_runtime_binding_authorized": False,
            "sanming_invokes_shoushi_framework_but_uses_exact_yandu_table": False,
            "most_conservative_reading": "Wan Minying invokes Shoushi calendrical/time-division authority while presenting a table that is not the exact Yandu 62/38 Shoushi standard; its precise table genealogy/locality remains unresolved.",
            "huqianjing_direct_genealogy_to_sanming": False,
            "forty_sixty_family_is_broader_historical_control": True,
            "exact_sanming_table_provenance_closed": False
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "runtime_time_standard_binding": "SHOUSHI_LOCALITY_CAPABILITY_CLOSED_BUT_SANMING_SELECTED_LOCALITY_TABLE_UNRESOLVED",
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "remaining_blockers": [
                "trace the exact pre-1578 provenance of the Sanming seasonal sunrise/sunset/day-night table rather than assuming Yandu Shoushi",
                "identify whether Wan's operational practice selected a normative standard location, practitioner location, or merely a conventional rounded table",
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


def write_doc(sanming_id: str) -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CA

    ## 《三命通會》“授時曆分之”的地域边界与表谱错配：九服地方算法、地中 40/60、燕都 62/38

    Status: **YUANSHI SHOUSHI METHOD DIRECTLY SUPPORTS REGIONAL LOCALITY CALIBRATION / NINE-REGION DAY-NIGHT KE DEPEND ON LOCAL POLE ALTITUDE AND MAY BE CALIBRATED BY INSTRUMENT OR WATER CLOCK / MING TECHNICAL TRANSMISSION EXPLICITLY DISTINGUISHES DIZHONG 40/60 FROM YANDU SHOUSHI 62/38 / SANMING TONGHUI DISPLAYED MANTIC TABLE IS NOT THE EXACT YANDU 62/38 TABLE / TIANYIGE MING-PRINT HUQIANJING PHYSICALLY CONFIRMS A BROADER 40/60 SEASONAL LEAK-ARROW TRADITION / NO DIRECT HUQIANJING→SANMING GENEALOGY CLAIM / SANMING SELECTED LOCALITY OR TABLE GENEALOGY STILL UNRESOLVED / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this batch follows 12BZ

    Batch 12BZ closed a primary Ming mantic bridge from difficult natal birth-time adjudication to `授時曆分之`. The remaining question is whether that phrase licenses a unique modern time coordinate or a specific Dadu/Beijing standard.

    The answer is no: the Shoushi method itself is explicitly regional, while Wan Minying's displayed table is not the exact Yandu Shoushi table.

    ## 2. 《元史·授時曆經》: locality is native to the system

    《元史》卷55 directly states that the `九服` day/night ke and central-star rates are to be computed according to the local pole altitude. It then gives `求九服所在漏刻`: each place may use instrument observation or a water clock to establish its own solstitial night-ke value, from which the daily values are derived.

    Therefore:

    - Shoushi is not intrinsically a single location-free table;
    - nor is it intrinsically only a Dadu table at the method level;
    - regional realization is explicitly part of the received computational framework.

    This closes **calendar-system locality capability**, but does not prove Wan Minying recalculated a natal chart for the birthplace.

    ## 3. Historical distinction: 地中 40/60 versus 燕都 62/38

    唐順之《稗編》卷54, transmitting a discussion attributed to 馬端臨, explicitly contrasts:

    ```text
    蔡氏據地中而言：長極六十，短止四十。
    授時曆據今燕都而言：長極六十二，短極三十八。
    ```

    This is decisive as a comparative control: differing solstitial ke values can encode differing geographic standards rather than a mere textual error.

    It does not by itself establish which table Wan Minying used.

    ## 4. The Sanming table is not exact Yandu Shoushi

    The Ming physical/received 《三命通會》 `論時刻` table includes values such as 小寒 42/58, 立春 45/55, 雨水 47/53 and 48/52, and 夏至 59/41. Its displayed structure therefore does not equal the historical Yandu Shoushi 62/38 extreme table.

    Consequently, the phrase `余姑就授時曆分之` must not be normalized into:

    ```text
    use the exact Dadu/Beijing Shoushi day-night table
    ```

    and it certainly does not authorize a modern Beijing longitude/latitude runtime default.

    ## 5. Tianyige Ming physical 《虎鈐經》 control

    To test whether 40/60-style seasonal tables belong to a wider historical timekeeping tradition, a Tianyige Ming-print physical copy of the Song work 《虎鈐經》 was rendered and reviewed without OCR.

    - workflow run `{HUQIAN_RUN}`
    - artifact `{HUQIAN_ARTIFACT}`
    - artifact digest `{HUQIAN_DIGEST}`
    - source PDF SHA-256 `{HUQIAN_PDF_SHA256}`
    - PDF p74 render SHA-256 `{HUQIAN_P74_SHA256}`
    - PDF p76 render SHA-256 `{HUQIAN_P76_SHA256}`

    PDF p74 directly reads `傳箭第七十六`, the hundred-ke day, and winter-solstice first-arrow `晝四十刻 / 夜六十刻`. PDF p76 reaches the summer-solstice reversal `晝六十刻 / 夜四十刻`.

    This physically establishes a broader premodern 40/60 seasonal leak-arrow family. It does **not** prove that 《三命通會》 copied 《虎鈐經》, and no genealogy vote is added.

    ## 6. Product adjudication

    For `HPA-ZDATE-006`:

    - `授時曆` regional/locality capability: **closed**;
    - Wan Minying actual birthplace localization: **not proved**;
    - Sanming table = exact Yandu Shoushi table: **rejected**;
    - Dadu/Beijing runtime binding: **not authorized**;
    - exact Sanming seasonal-table genealogy: **open**;
    - upper-Zi → Hai mechanical vote: **0**;
    - runtime candidate: **none**;
    - `HPA-ZDATE-006`: remains `MISSING_FROM_PRODUCT`.

    ## 7. Next gate

    Trace the **exact pre-1578 provenance** of the Sanming seasonal table using distinctive multi-point strings rather than the generic 40/60 endpoints. Priority targets are pre-1578 medical `運氣`, almanac/tongshu and calendrical manuals. A later matching table can be used as transmission evidence, never as an ancestor merely because it matches.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def matrix(sanming_id: str) -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12ca_sanming_shoushi_locality_and_table_mismatch"] = {
        "source_ids": [sanming_id, SRC_YUAN, SRC_BAIBIAN, SRC_HUQIAN, SRC_HUQIAN_TEXT],
        "shoushi_regional_locality_algorithm_attested": True,
        "wan_minying_birthplace_localization_proved": False,
        "sanming_table_exact_dadu_shoushi_equivalence": False,
        "dadu_beijing_runtime_binding_authorized": False,
        "huqianjing_40_60_physical_parallel_confirmed": True,
        "huqianjing_direct_genealogy_to_sanming": False,
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
    if "## Progress through Batch 12CA" not in md:
        md += dedent('''

        ## Progress through Batch 12CA

        - Yuan Shoushi-calendar methods explicitly support regional realization: nine-region day/night ke depend on local pole altitude, and local solstitial leak values can be fixed by instruments or water clocks.
        - A Ming technical transmission explicitly distinguishes a 地中 40/60 standard from the Yandu Shoushi 62/38 standard. Sanming Tonghui's displayed mantic table is therefore not automatically the exact Yandu table; its summer-solstice line is 59/41.
        - Tianyige's Ming-print Huqianjing physically confirms that 40/60-style seasonal leak-arrow tables belong to a wider historical timekeeping tradition, but no direct genealogy from Huqianjing to Sanming is claimed.
        - Locality capability is closed at the calendar-system level; Wan Minying's selected locality/table genealogy and any modern-instant binding remain unresolved. HPA-ZDATE-006 stays MISSING_FROM_PRODUCT with no new candidate, winner, Hai vote, collapse or reopen.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.86.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12CA closes Shoushi system-level locality capability: Yuan received methods compute nine-region day/night ke from local pole altitude and permit local instrument/water-clock calibration.",
        "Sanming Tonghui's displayed mantic seasonal table is not the exact Yandu Shoushi 62/38 table, so no Dadu/Beijing runtime binding is authorized by the phrase 授時曆分之.",
        "A Tianyige Ming-print Huqianjing physical witness confirms the wider 40/60 seasonal leak-arrow tradition, without proving direct genealogy to Sanming. Exact Sanming table provenance remains the next gate."
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-14"
    dump(p, d)


def main() -> None:
    continuity()
    sanming_id = registry()
    write_research(sanming_id)
    write_doc(sanming_id)
    matrix(sanming_id)
    state()


if __name__ == "__main__":
    main()
