from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-CG"
PREV_ID = "BATCH-12-ZIWEI-YINGZONG-SHILU-1447-NANJING-59-41-PHYSICAL-COLLATION-CF"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-CG.md"
RESEARCH = "docs/research/ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-R1.json"
NCL_SRC = "EXT-NCL-DATONG-RICHU-NCL06267"
LI_SRC = "EXT-LI-LIANG-SUNRISE-TABLES-2022"
JINGFU_SRC = "EXT-CBETA-X21N0376-JINGFUDIAN-CHENLOU"
SANMING_SRC = "EXT-SANMING-NCL-1578-MAIN"

NCL_URL = "https://commons.wikimedia.org/wiki/File:NCL-06267_%E5%A4%A7%E7%B5%B1%E6%97%A5%E5%87%BA%E5%88%86.pdf"
CBETA_URL = "https://tripitaka.cbeta.org/zh-cn/X21n0376_001"
LI_URL = "https://publikationen.badw.de/de/048385459/048385459%5BCC%20BY-NC-ND%5D.pdf"
RUN_ID = 34869676923
ARTIFACT_ID = 10358685142
ARTIFACT_DIGEST = "sha256:fdb1fd4b9e0fc785d9fb467e00daa71544c412482e2093d31cf553152bd518fe"
SOURCE_SHA256 = "0d3ed2b54f92b5eb2f11e5d06babebcc177e04ec5b8c7168b56f1fb25f94797d"
PAGE_SHA256 = {
    "02": "010e5bb728738126426bd784da05f53fe83a14ff540cdf0f46e627c4799a9d11",
    "03": "3611a747aee0d01b57c87be4c32fbe66d1b7a6b7e5bb15f209a45d513fac528b",
    "04": "44ee08862757b4b1581ba1386b0e0ceaebd73f8af5f21bd99796bccd03b953a4",
    "05": "0ffa5e0c5f86a1ae1a1ebd63816475be26443f798bc4cbd4fdd2816a76d4eff4",
    "06": "8424b8c33cdf04f8eabb52cacf55548096a27801fb49a1276812619cdd41157d",
    "07": "39913feab54f7ae77bd129efa54610f903f0e3c2a799a1cc762343ef0c100ef8",
}

REPLAY_POINTS = [
    {"day_after_winter_solstice": 21, "half_day_fen": 2101.63, "daylight_ke": 42.0326, "nearest_integer_ke": 42, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 34, "half_day_fen": 2154.21, "daylight_ke": 43.0842, "nearest_integer_ke": 43, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 43, "half_day_fen": 2208.19, "daylight_ke": 44.1638, "nearest_integer_ke": 44, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 52, "half_day_fen": 2257.14, "daylight_ke": 45.1428, "nearest_integer_ke": 45, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 59, "half_day_fen": 2302.41, "daylight_ke": 46.0482, "nearest_integer_ke": 46, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 67, "half_day_fen": 2348.62, "daylight_ke": 46.9724, "nearest_integer_ke": 47, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 74, "half_day_fen": 2401.90, "daylight_ke": 48.0380, "nearest_integer_ke": 48, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 89, "half_day_fen": 2494.04, "daylight_ke": 49.8808, "nearest_integer_ke": 50, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 98, "half_day_fen": 2559.25, "daylight_ke": 51.1850, "nearest_integer_ke": 51, "reading_scope": "DIRECT_VISUAL_APPROX"},
    {"day_after_winter_solstice": 178, "half_day_fen": 2930.34, "daylight_ke": 58.6068, "nearest_integer_ke": 59, "reading_scope": "LI_LIANG_TABLE5_EXACT_TRANSCRIPTION"},
    {"day_after_winter_solstice": 181, "half_day_fen": 2931.51, "daylight_ke": 58.6302, "nearest_integer_ke": 59, "reading_scope": "LI_LIANG_TABLE5_EXACT_TRANSCRIPTION"},
]


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate 12CF tail in continuity verifier")
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
    if LI_SRC not in ids:
        raise SystemExit(f"expected existing scholarly source missing: {LI_SRC}")
    if NCL_SRC not in ids:
        d["sources"].append({
            "source_id": NCL_SRC,
            "title": "《大統日出分》NCL-06267",
            "historical_period": "MING_DATONG_TABLE_TRADITION; TABLE_FAMILY_DATED_TO_1380S_BY_MODERN_SCHOLARSHIP; SURVIVING_NCL_COPY_EXACT_IMPRESSION_DATE_NOT_RE-ADJUDICATED_HERE",
            "provider": "National Central Library rare-book microfilm route via Wikimedia Commons",
            "url": NCL_URL,
            "source_role": "DIRECT_PHYSICAL_DAILY_NANJING_DATONG_SUNRISE_SUNSET_TABLE_FOR_MULTIPOINT_REPLAY",
            "quality_notes": "Batch 12CG directly reviews the 21-page physical table without OCR. The exact artifact is bound by run/artifact/source SHA-256. Li Liang 2022 independently classifies 大統日出入分 as Type C-II-N, dates the table to the 1380s, identifies N as Nanjing, and prints an excerpt whose opening/end numerical values agree with this NCL object. This source is used as a physical numerical substrate, not as proof that Wan Minying copied this exact surviving copy."
        })
    if JINGFU_SRC not in ids:
        d["sources"].append({
            "source_id": JINGFU_SRC,
            "title": "《盂蘭盆經疏鈔餘義》卷一〈節氣加減刻漏規式〉",
            "author_attribution": "宋·日新隨聽次錄",
            "historical_period": "WORK_PREFACE_DATES_LECTURE_AND_REPUBLICATION_TO_XINING_1_1068; CURRENT_CBETA_IS_A_LATER_RECEIVED_DIGITAL_TEXT_NOT_A_1068_PHYSICAL_OBJECT",
            "provider": "CBETA / 卍續藏 received-text edition",
            "url": CBETA_URL,
            "source_role": "PRE1578_RECEIVED_TEXT_MECHANICAL_CONTROL_FOR_INTRA_SOLAR_TERM_INTEGER_DAY_NIGHT_KE_BINS",
            "quality_notes": "The work's own preface dates the lecture to 熙寧元年(1068). The target section says 今依本朝定景福殿秤漏 and explicitly assigns integer day/night pairs from 40/60 through 60/40 to date ranges inside solar terms. This closes the existence of the algorithmic form well before Sanming, but not Sanming's exact table genealogy or identical change-days."
        })
    d["access_date"] = "2026-09-15"
    dump(p, d)


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-R1",
        "schema_version": "1.0.0",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "Can the gap between the pre-1578 Nanjing 59-ke endpoint and the 1578 Sanming multipoint 42..59 ladder be narrowed by a directly bound Ming Nanjing daily sunrise/daylength table plus an independently earlier integer-bin timekeeping algorithm family?",
        "physical_source": {
            "source_id": NCL_SRC,
            "title": "大統日出分 / NCL-06267",
            "workflow_run_id": RUN_ID,
            "artifact_id": ARTIFACT_ID,
            "artifact_digest": ARTIFACT_DIGEST,
            "source_pdf_sha256": SOURCE_SHA256,
            "page_count": 21,
            "page_sha256": PAGE_SHA256,
            "ocr_used_for_glyph_claims": False,
            "direct_structure": [
                "daily argument sequence after winter solstice and after summer solstice",
                "columns 晨分 / 日出分 / 半晝分 / 日入分 / 昏分",
                "physical numerical progression is daily rather than only 24 fixed solar-term rows"
            ]
        },
        "independent_scholarly_binding": {
            "source_id": LI_SRC,
            "url": LI_URL,
            "work": "Li Liang, Tables of Sunrise and Sunset in Yuan and Ming China (1271–1644) and their Adoption in Korea",
            "table_identity": "大統日出入分 = Type C-II-N",
            "dating": "1380s",
            "site_code": "N = Nanjing",
            "type_ii_argument": "days 0..182 after a solstice",
            "type_ii_columns": ["accumulated day", "dawn", "sunrise", "half daytime", "sunset", "dusk"],
            "published_cii_n_excerpt": {
                "day0_half_day_fen": 2068.30,
                "day10_half_day_fen": 2075.89,
                "day178_half_day_fen": 2930.34,
                "day179_half_day_fen": 2930.86,
                "day180_half_day_fen": 2931.25,
                "day181_half_day_fen": 2931.51,
                "day182_half_day_fen": 2931.66
            },
            "physical_object_numeric_identity": "OPENING_AND_ENDPOINT_FINGERPRINTS_AGREE_WITH_NCL06267",
            "direct_copy_genealogy_to_sanming_proved": False
        },
        "conversion_and_replay": {
            "conversion": "full_daylight_ke = 2 * half_day_fen / 100, under the hundred-ke day and 10,000-fen day units used by the table tradition",
            "replay_points": REPLAY_POINTS,
            "coverage_review_days": [21, 34, 43, 52, 59, 67, 74, 82, 89, 98, 106, 114, 122, 129, 137, 140, 148, 162, 178, 181],
            "integer_ladder_result": "THE_DAILY_NANJING_CURVE_CONTINUOUSLY_SPANS_THE_SANMING_INTEGER_DAYLIGHT_LADDER_FROM_LOW_40S_TO_59; SELECTED_DIRECT_POINTS_REPLAY_MULTIPLE_DISTINCT_ANCHORS",
            "exact_sanming_change_day_thresholds_recovered": False,
            "nearest_integer_rounding_as_historical_sanming_rule_proved": False,
            "reason_for_firewall": "A numerical replay can demonstrate a generative substrate without proving which historical quantization/rounding convention or source copy Wan Minying actually used."
        },
        "pre1578_integer_bin_mechanical_control": {
            "source_id": JINGFU_SRC,
            "work_preface_date": "熙寧元年 / 1068",
            "surviving_evidence_class": "LATER_RECEIVED_TEXT_PRESERVING_A_SELF_DATED_SONG_WORK; NOT_A_1068_PHYSICAL_SCAN",
            "target_heading": "節氣加減刻漏規式",
            "institutional_phrase": "今依本朝定景福殿秤漏，春秋二分各五十刻",
            "mechanical_form": "integer day/night ke pairs are assigned to explicit day ranges within solar terms",
            "range": "40/60 through 60/40",
            "exact_sanming_change_days_identical": False,
            "genealogy_to_sanming_proved": False,
            "value": "This independently closes that intra-term integer-bin day/night tables are a much older operational form; it prevents treating Sanming's stepped format as a uniquely late invention."
        },
        "historical_synthesis": {
            "pre1578_nanjing_daily_numeric_substrate": "CLOSED_AT_TABLE_FAMILY_LEVEL",
            "pre1578_integer_bin_algorithm_family": "CLOSED_AT_RECEIVED_TEXT_LEVEL",
            "sanming_1578_multipoint_table_mechanically_explainable_from_these_families": True,
            "exact_textual_parent_or_borrowing_direction": "UNRESOLVED",
            "exact_quantization_change_days": "UNRESOLVED",
            "safe_model": "older integer-bin leak-clock tradition + Ming/Nanjing daily Datong numerical substrate -> a historically plausible generative bridge for the Sanming displayed ladder; exact compositing event/source remains open"
        },
        "adjudication": {
            "mechanical_bridge_closed_one_layer": True,
            "exact_pre1578_sanming_table_parent_closed": False,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "upper_zi_to_hai_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False
        },
        "impact_on_hpa_zdate_006": {
            "status_before": "MISSING_FROM_PRODUCT",
            "status_after": "MISSING_FROM_PRODUCT",
            "reason": "The new evidence strengthens the historical day/night-ke numerical substrate around natal time adjudication but does not establish the Fullbook-specific upper-five-ke -> previous-night Hai branch transformation or a source-closed runtime clock binding.",
            "next_gate": [
                "find a securely pre-1578 source that prints the Sanming change-day fingerprint itself or gives its exact quantization rule",
                "continue the independent Fullbook upper-five-ke -> Hai lineage and time-coordinate search"
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


def matrix_json() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    row["batch_12cg_datong_richu_daily_table_sanming_replay"] = {
        "source_ids": [NCL_SRC, LI_SRC, JINGFU_SRC, SANMING_SRC],
        "ncl_datong_daily_table_physically_reviewed": True,
        "li_liang_classifies_table_as_1380s_c_ii_n_nanjing": True,
        "daily_halfday_curve_replays_multiple_sanming_integer_anchors": True,
        "pre1578_intra_term_integer_bin_algorithm_family_attested": True,
        "exact_sanming_change_day_fingerprint_parent_closed": False,
        "exact_historical_rounding_rule_closed": False,
        "upper_zi_to_hai_vote_increment": 0,
        "runtime_winner_selected": False,
        "candidate_collapsed": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH
    }
    dump(p, d)


def matrix_md() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    s = p.read_text(encoding="utf-8")
    marker = "## Progress — Batch 12CG"
    if marker not in s:
        s = s.rstrip() + "\n\n" + dedent(f'''\
        {marker}

        - Direct no-OCR review of NCL-06267 `《大統日出分》` closes a physical daily Nanjing Datong numerical substrate. Li Liang's independent table study classifies `大統日出入分` as 1380s Type `C-II-N` (Nanjing) and its published C-II-N opening/end fingerprints agree with the NCL object.
        - Converting `半晝分` to full daylight ke replays multiple distinct integer anchors across the 42→59 ladder seen in the 1578 `《三命通會》` seasonal table. This is a generative/numerical bridge, not proof that Wan Minying copied this exact surviving object or used modern nearest-integer rounding.
        - Song 日新 `《盂蘭盆經疏鈔餘義》` self-dates its lecture/republication to 熙寧元年 (1068); its received `〈節氣加減刻漏規式〉` says `今依本朝定景福殿秤漏` and assigns integer 40/60→60/40 day/night pairs to explicit intra-solar-term day ranges. It independently proves the stepped integer-bin algorithmic form long predates Sanming, while its exact change-days are not equated to Sanming.
        - Therefore the pre-1578 mechanical bridge is materially closed one layer: older integer-bin leak-clock practice + a Ming/Nanjing daily Datong numerical table can explain the form and value range of the Sanming ladder. Exact textual parent, compositing event and quantization thresholds remain unresolved.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts remain 198/166/10/14 and provenance defects remain 11/11.

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
    focus = h["current_focus"]
    additions = [
        "Batch 12CG directly reviews NCL-06267 大統日出分 as a daily physical numerical table and binds it to Li Liang's independent 1380s C-II-N/Nanjing classification; published opening/end fingerprints agree with the NCL object.",
        "Batch 12CG replays multiple Sanming integer daylight anchors from the Nanjing daily half-day curve and separately binds Song 日新's self-dated 1068 received 景福殿秤漏 section as a pre-1578 intra-solar-term integer-bin algorithm family. This closes one mechanical bridge layer but not the exact Sanming table parent or rounding/change-day rule.",
        "Next gate: find a securely pre-1578 witness that prints the Sanming change-day fingerprint or its exact quantization rule; independently continue Fullbook upper-five-ke -> Hai. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT and all algorithm invariants remain unchanged."
    ]
    for item in additions:
        if item not in focus:
            focus.append(item)
    d["schema_version"] = "1.92.0"
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12CG

    ## NCL《大統日出分》逐日南京數表 × 1578《三命通會》多點刻數重放

    Status: **1380s NANJING DATONG DAILY SUNRISE/DAYLENGTH TABLE FAMILY INDEPENDENTLY IDENTIFIED AND PHYSICALLY REVIEWED / MULTIPLE 42→59 SANMING INTEGER ANCHORS NUMERICALLY REPLAYED FROM THE DAILY HALF-DAY CURVE / SONG 1068 SELF-DATED RECEIVED TEXT INDEPENDENTLY ATTESTS INTRA-SOLAR-TERM INTEGER DAY/NIGHT-KE BINS / MECHANICAL BRIDGE CLOSED ONE LAYER / EXACT SANMING CHANGE-DAY PARENT AND QUANTIZATION RULE STILL OPEN / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this follows Batch 12CF

    Batch 12CF physically closed the pre-1578 Nanjing solstitial `59` layer with the 1447 `《明英宗實錄》`, but deliberately left the intermediate `42/58`, `45/55`, `47/53`, `48/52`-style ladder open.

    This batch asks whether an earlier Ming/Nanjing *daily numerical substrate* and an independently older *integer-bin timekeeping form* can explain those intermediate anchors without inventing a genealogy.

    ## 2. Direct NCL physical object

    ```text
    SOURCE=NCL-06267 大統日出分
    RUN={RUN_ID}
    ARTIFACT={ARTIFACT_ID}
    ARTIFACT_DIGEST={ARTIFACT_DIGEST}
    SOURCE_SHA256={SOURCE_SHA256}
    PDF_PAGES=21
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    Direct review shows a daily table rather than a 24-row solar-term summary. It contains daily arguments after the solstices and columns `晨分 / 日出分 / 半晝分 / 日入分 / 昏分`. Representative rendered page hashes are machine-bound in the research record.

    ## 3. Independent identification: 1380s Type C-II-N = Nanjing

    Li Liang's study *Tables of Sunrise and Sunset in Yuan and Ming China (1271–1644) and their Adoption in Korea* independently classifies:

    ```text
    大統日出入分 = 1380s = C-II-N
    C = Chinese source
    II = daily pick-up table type
    N = Nanjing
    ```

    The published Type C-II-N excerpt prints days `0..10` and `178..182`. Its `半晝分` values begin at `2068.30` and end at `2931.66`; those opening/end fingerprints agree with the physical NCL object. The source also explains Type II as a daily table and identifies the relevant columns.

    This supplies a secure external identity bridge. It does **not** make the modern article a historical authority, and it does not prove Wan Minying handled this exact surviving copy.

    ## 4. Numerical replay against the Sanming integer ladder

    Under the hundred-ke day / 10,000-fen day framework, the table's `半晝分` converts to full daylight ke by:

    ```text
    daylight_ke = 2 * half_day_fen / 100
    ```

    Selected direct no-OCR points across the NCL curve replay distinct integer anchors:

    ```text
    day 21   half-day ≈2101.63 -> daylight ≈42.0326 -> 42
    day 34   half-day ≈2154.21 -> daylight ≈43.0842 -> 43
    day 43   half-day ≈2208.19 -> daylight ≈44.1638 -> 44
    day 52   half-day ≈2257.14 -> daylight ≈45.1428 -> 45
    day 59   half-day ≈2302.41 -> daylight ≈46.0482 -> 46
    day 67   half-day ≈2348.62 -> daylight ≈46.9724 -> 47
    day 74   half-day ≈2401.90 -> daylight ≈48.0380 -> 48
    day 89   half-day ≈2494.04 -> daylight ≈49.8808 -> 50
    day 98   half-day ≈2559.25 -> daylight ≈51.1850 -> 51
    day 178  half-day 2930.34  -> daylight 58.6068  -> 59
    day 181  half-day 2931.51  -> daylight 58.6302  -> 59
    ```

    The daily curve therefore supplies the entire continuous numerical range in which the Sanming 42→59 integer ladder sits. The important result is **generative compatibility at daily resolution**, not a claim that `round()` was Wan Minying's textual rule.

    Firewall:

    ```text
    EXACT_SANMING_CHANGE_DAY_THRESHOLDS_RECOVERED=false
    NEAREST_INTEGER_ROUNDING_PROVED_AS_HISTORICAL_RULE=false
    DIRECT_COPY_FROM_NCL06267_TO_SANMING=false
    ```

    ## 5. Much earlier integer-bin form: Song received 景福殿秤漏 passage

    The received `《盂蘭盆經疏鈔餘義》` identifies 日新 as recorder, and its own preface dates the lecture/republication to `熙寧元年` (1068). The current CBETA object is a later received digital text, **not a 1068 physical scan**.

    Its `〈節氣加減刻漏規式〉` states:

    ```text
    今依本朝定景福殿秤漏，春秋二分各五十刻
    ```

    and then assigns every integer day/night pair from `40/60` through `60/40` to explicit ranges *inside* solar terms, e.g. rows such as `42/58`, `43/57`, `44/56` and onward.

    This is decisive for algorithmic form: long before 1578, a received Song text already preserves a scheme in which seasonal timekeeping is discretized into integer ke bins whose change-points occur inside solar terms.

    It is **not** the exact Sanming table: its day ranges differ, and no direct genealogy is asserted.

    ## 6. Historical synthesis

    The safe reconstruction is now narrower:

    ```text
    older intra-term integer-bin leak-clock tradition
      +
    Ming/Nanjing daily Datong sunrise/daylength numerical substrate
      ->
    historically plausible generative bridge for Sanming's stepped multipoint display
    ```

    This closes one mechanical layer that Batch 12CF had left open. It still does not identify the exact pre-1578 parent text, the compositing event, or the exact quantization/change-day convention used by Wan Minying.

    ## 7. Product adjudication

    For `HPA-ZDATE-006`:

    - pre-1578 Nanjing daily numerical substrate: **closed at table-family level**;
    - pre-1578 intra-term integer-bin algorithm family: **closed at received-text level**;
    - exact Sanming multipoint parent/change-day fingerprint: **open**;
    - upper-Zi → Hai mechanical vote: **0**;
    - runtime candidate/winner/collapse: **none**;
    - algorithm reopen: **no**;
    - status: **MISSING_FROM_PRODUCT**.

    Counts remain `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11 confirmed / 11 repaired`; chart algorithm defect/reopen/collapse remain `0/0/0`.

    ## 8. Next gate

    Search for a securely pre-1578 calendrical, mantic, tongshu or institutional source that either:

    1. prints the **same Sanming intra-term change-day fingerprint**, or
    2. states an exact quantization rule that deterministically reproduces those change-days from a Nanjing/Datong daily table.

    Continue the Fullbook `上五刻 -> 昨夜亥時` line independently; none of the evidence in this batch supplies a Hai-branch vote.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def main() -> None:
    continuity()
    registry()
    write_research()
    matrix_json()
    matrix_md()
    state()
    write_doc()


if __name__ == "__main__":
    main()
