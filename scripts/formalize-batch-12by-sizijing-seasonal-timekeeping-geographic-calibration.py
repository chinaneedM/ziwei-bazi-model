from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-SIZIJING-SEASONAL-TIMEKEEPING-GEOGRAPHIC-CALIBRATION-BY"
PREV_ID = "BATCH-12-ZIWEI-SIZIJING-DANXI-YUEJIAN-YUEYUN-SEMANTICS-BX"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SIZIJING-SEASONAL-TIMEKEEPING-GEOGRAPHIC-CALIBRATION-BY.md"
RESEARCH = "docs/research/ZIWEI-SIZIJING-SEASONAL-TIMEKEEPING-GEOGRAPHIC-CALIBRATION-R1.json"
SRC_YUHAI = "EXT-WIKISOURCE-YUHAI-V11-WANGPU-GUANLI-KELOU-GEOGRAPHIC-CALIBRATION"
SRC_SIKU = "EXT-WIKISOURCE-SIKU-ZONGMU-V107-GUANLI-KELOU-GEOGRAPHIC-CALIBRATION"
SRC_SONGSHI48 = "EXT-WIKISOURCE-SONGSHI-V48-YUETAI-LINAN-GNOMON-GEOGRAPHY"
SRC_SONGSHI75 = "EXT-WIKISOURCE-SONGSHI-V75-DAILY-SUNRISE-LEAK-FORMULAE"
SRC_YONGLE = "EXT-TIME-YONGLE-DADIAN-18764-QIANDINGSHU-SIZIJING"

URL_YUHAI = "https://zh.wikisource.org/wiki/%E7%8E%89%E6%B5%B7_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B7011"
URL_SIKU = "https://zh.wikisource.org/wiki/%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%B8%BD%E7%9B%AE%E6%8F%90%E8%A6%81/%E5%8D%B7107"
URL_SONG48 = "https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B7048"
URL_SONG75 = "https://zh.wikisource.org/wiki/%E5%AE%8B%E5%8F%B2_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%85%A8%E8%A6%BD3"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate BX tail")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch")
    p.write_text(s, encoding="utf-8")


def write_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12BY

    ## 《四字經》季节取时语义的地域校准约束：王普《官历刻漏图》、岳台与临安

    Status: **SONG OFFICIAL TIMEKEEPING SOURCES CONFIRM SEASONAL DAY-NIGHT / LEAK-CLOCK LENGTH IS GEOGRAPHICALLY CALIBRATED / WANG PU GUANLI KELOU TU SELF-PREFACE SAYS YUETAI IS THE STANDARD BUT NINE-REGION SOLSTICE DAY-NIGHT KE DIFFER AND 24-QI ARROW-CHANGE DATES SHIFT / SONGSHI SAYS LINAN GNOMON PARAMETERS DIFFER FROM YUETAI / DAILY SUNRISE-SUNSET-LEAK FORMULAE EXIST FOR A SPECIFIC STANDARD LOCATION / UNIVERSAL MONTH-ONLY TABLE REJECTED AS HISTORICAL TECHNICAL MODEL / NO DIRECT PROOF SIZIJING USED WANG-PU TABLE / NO SOURCE-SPECIFIC BIRTH-TIME FORMULA RECOVERED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Why this batch follows 12BX

    Batch 12BX established that Yongle `旦夕將月建長短而推言` sits naturally in a premodern seasonal-timekeeping semantic field, but did not recover an operational formula. The next question is whether such `長短` could historically be treated as a universal monthly schedule.

    Song official timekeeping evidence answers no: the seasonal schedule itself was geographically calibrated.

    ## 2. Wang Pu's 《官曆刻漏圖》

    Wang Yinglin's 《玉海》 records the bibliography and substance of Northern/Southern Song official leak-clock work. For early Shaoxing it states that 太常博士王普 wrote 《官曆刻漏圖》 and that its preface said:

    ```text
    百刻分十二辰，晝夜長短以岳臺為定。
    九服之地，冬夏至晝夜刻數或與岳臺不同，
    則二十四氣前後易箭之日亦皆少差。
    ```

    Evidence: `{URL_YUHAI}`.

    The Siku catalogue independently describes the same work as an `永樂大典本`, attributes it to Song Wang Pu, and preserves the same geographical-calibration statement. Evidence: `{URL_SIKU}`.

    The critical point is operational: even when one starts from the same 24-qi seasonal framework, different regions do not necessarily use the same solstitial day/night ke counts or the same dates for changing seasonal leak-clock arrows.

    ## 3. Songshi control: Yue-tai versus Lin'an

    《宋史》卷48's gnomon discussion explicitly says `地里遠近古今亦不同` and records criticism that Lin'an's gnomon shadow should not simply reuse Yue-tai's parameters. It gives a distinct Lin'an winter-solstice initial-limit proposal rather than the Yue-tai value. Evidence: `{URL_SONG48}`.

    《宋史》 calendrical material also preserves full daily calculation procedures for Yue-tai, including daily gnomon shadow, dawn/dusk, sunrise/sunset and `每日夜半定漏`. Evidence: `{URL_SONG75}`.

    This proves that a real technical implementation of seasonal `旦夕/長短` was not merely `month -> fixed clock value`; it depended on a defined observing/calibration location and calendrical parameters.

    ## 4. Constraint on interpreting the Sizijing clause

    If Yongle `旦夕將月建長短而推言` reflects this broad technical tradition, then the minimum historically defensible model would require:

    ```text
    calendrical seasonal position / qi
    + geographical observing location or calibrated regional table
    + day/night or dawn/dusk length model
    + a rule for mapping the uncertain event to that model
    ```

    Only the first and general `長短` idea are textually visible in the Sizijing clause. No Sizijing witness currently supplies the location standard, table, formula, or mapping rule.

    Therefore it is forbidden to manufacture a universal `month -> birth-hour correction` table from the one sentence, and equally forbidden to import Yue-tai's Song official formula as though it were the Sizijing author's own procedure.

    ## 5. Product effect

    This batch adds a **future implementation constraint**, not a runtime candidate:

    - any future candidate claiming to operationalize the seasonal-timekeeping reading must declare its geographical calibration basis;
    - a location-free universal monthly correction is historically under-specified;
    - current shared time credentials already make geographic/time-coordinate provenance representable, but that engineering capacity is not evidence for the missing historical rule;
    - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT` remains unchanged;
    - no Hai-branch mechanical vote, runtime winner, candidate collapse or algorithm reopen.

    ## 6. Next gate

    1. Locate a pre-Ming/Song-Ming fate-calculation source that explicitly applies seasonal day/night or sunrise/sunset tables to recover an uncertain **birth hour**, not merely civil timekeeping.
    2. Search surviving/quoted material from 《官曆刻漏圖》 and related `日出入氣刻立成` works for a formula that could explain the Sizijing's compressed wording, while preserving the no-import firewall unless a textual bridge is found.
    3. Search additional early Sizijing recensions for the `月建/月運` locus to establish whether the geographical-timekeeping-compatible `月建` reading has broader textual support.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def write_research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-SIZIJING-SEASONAL-TIMEKEEPING-GEOGRAPHIC-CALIBRATION-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "question": "If Sizijing yuejian/long-short belongs to seasonal timekeeping, was that technical system historically location-independent?",
        "song_controls": [
            {
                "source_id": SRC_YUHAI,
                "title": "王應麟《玉海》卷11所錄王普《官曆刻漏圖》",
                "url": URL_YUHAI,
                "core": "百刻分十二辰; 晝夜長短以岳臺為定; 九服之地冬夏至晝夜刻數或與岳臺不同; 二十四氣前後易箭之日亦皆少差",
                "role": "SONG_BIBLIOGRAPHIC_AND_TECHNICAL_GEOGRAPHIC_CALIBRATION_CONTROL",
            },
            {
                "source_id": SRC_SIKU,
                "title": "《四庫全書總目》卷107《官曆刻漏圖》提要",
                "url": URL_SIKU,
                "core": "宋王普撰; 永樂大典本; 官曆漏刻以岳臺為定; 九服之地差異導致二十四氣易箭日差",
                "role": "INDEPENDENT_CATALOG_TRANSMISSION_CONTROL_FOR_WANGPU_PREFACE",
            },
            {
                "source_id": SRC_SONGSHI48,
                "title": "《宋史》卷48 天文志土圭",
                "url": URL_SONG48,
                "core": "冬至晷景長短實與歲差相應而地里遠近古今亦不同; 臨安之晷景當與岳臺異",
                "role": "OFFICIAL_HISTORIOGRAPHIC_GEOGRAPHIC_GNOMON_CALIBRATION_CONTROL",
            },
            {
                "source_id": SRC_SONGSHI75,
                "title": "《宋史》律曆志步晷漏術",
                "url": URL_SONG75,
                "core": ["求岳臺晷景", "求每日晨昏分及日出入分", "求每日夜半定漏"],
                "role": "LOCATION_SCOPED_OPERATIONAL_DAILY_TIMEKEEPING_FORMULA_CONTROL",
            },
        ],
        "adjudication": {
            "seasonal_day_night_length_historically_geographically_calibrated": True,
            "universal_month_only_table_historically_sufficient": False,
            "direct_bridge_sizijing_to_wangpu_formula_found": False,
            "sizijing_location_standard_found": False,
            "sizijing_numeric_table_found": False,
            "sizijing_birth_hour_mapping_formula_found": False,
            "song_yuetai_formula_import_into_sizijing_authorized": False,
            "minimum_future_candidate_requirements": ["seasonal_or_qi_position", "geographic_calibration_basis", "day_night_or_dawn_dusk_model", "event_to_time_mapping_rule"],
        },
        "effect": {
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "future_candidate_location_provenance_required": True,
            "new_runtime_candidate_created": False,
            "runtime_winner_selected": False,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "matrix_counts_changed": False,
        },
    })


def registry() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    ids = {x.get("source_id") for x in d["sources"]}
    items = [
        {"source_id": SRC_YUHAI, "title": "《玉海》卷11：王普《官曆刻漏圖》地域校準記載", "historical_period": "SOUTHERN_SONG_WANG_YINGLIN_TRANSMISSION_OF_SHAOXING_OFFICIAL_WORK", "provider": "Wikisource / Siku transmission", "url": URL_YUHAI, "source_role": "SONG_GEOGRAPHICALLY_CALIBRATED_SEASONAL_TIMEKEEPING_CONTROL", "quality_notes": "Records Wang Pu preface: Yue-tai standard, regional solstitial day/night differences, and shifted 24-qi arrow-change dates. Not a Sizijing witness."},
        {"source_id": SRC_SIKU, "title": "《四庫全書總目》卷107《官曆刻漏圖》", "historical_period": "QING_CATALOG_OF_YONGLE-DADIAN_RECOVERED_SONG_WORK", "provider": "Wikisource", "url": URL_SIKU, "source_role": "WANGPU_GUANLI_KELOU_TRANSMISSION_CONTROL", "quality_notes": "Independently preserves author/title and geographic calibration statement; later catalog transmission, not Song physical glyph authority."},
        {"source_id": SRC_SONGSHI48, "title": "《宋史》卷48：岳臺/臨安土圭地理差異", "historical_period": "YUAN_HISTORIOGRAPHY_OF_SONG_ASTRONOMICAL_PRACTICE", "provider": "Wikisource / Siku transmission", "url": URL_SONG48, "source_role": "OFFICIAL_HISTORIOGRAPHIC_GEOGRAPHIC_CALIBRATION_CONTROL", "quality_notes": "Explicitly states gnomon results vary with geography and records proposed Lin'an parameters differing from Yue-tai."},
        {"source_id": SRC_SONGSHI75, "title": "《宋史》律曆志：步晷漏術每日晨昏/日出入/夜半定漏", "historical_period": "YUAN_HISTORIOGRAPHY_PRESERVING_SONG_CALENDAR_FORMULAE", "provider": "Wikisource / Siku transmission", "url": URL_SONG75, "source_role": "LOCATION_SCOPED_OPERATIONAL_TIMEKEEPING_FORMULA_CONTROL", "quality_notes": "Preserves Yue-tai daily gnomon, dawn/dusk, sunrise/sunset and midnight leak computations; not authorized for direct import into Sizijing without a bridge."},
    ]
    for x in items:
        if x["source_id"] not in ids:
            d["sources"].append(x)
    d["access_date"] = "2026-09-14"
    dump(p, d)


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12by_sizijing_seasonal_timekeeping_geographic_calibration"] = {
        "source_ids": [SRC_YONGLE, SRC_YUHAI, SRC_SIKU, SRC_SONGSHI48, SRC_SONGSHI75],
        "geographic_calibration_required_by_historical_technical_context": True,
        "universal_month_only_table_supported": False,
        "direct_sizijing_to_wangpu_formula_bridge": False,
        "new_runtime_candidate_created": False,
        "runtime_winner_selected": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH,
    }
    dump(p, d)
    mdp = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = mdp.read_text(encoding="utf-8")
    if "## Progress through Batch 12BY" not in md:
        md += dedent('''

        ## Progress through Batch 12BY

        - Song official timekeeping evidence makes the seasonal-timekeeping interpretation more constrained: Wang Pu's Guanli Kelou Tu preface says Yue-tai is the standard, but regional solstitial day/night ke and even 24-qi arrow-change dates can differ across the realm.
        - Songshi likewise states geographic distance affects gnomon results and records Lin'an parameters differing from Yue-tai; separate calendar procedures compute daily dawn/dusk, sunrise/sunset and midnight leak for the standard location.
        - Therefore any future attempt to operationalize Sizijing `旦夕/月建/長短` must identify a geographic calibration basis. A universal month-only correction table is historically under-specified.
        - No direct bridge authorizes importing Song Yue-tai formulae into Sizijing, so no new runtime candidate, winner, Hai vote or algorithm reopen is created.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.84.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12BY establishes a geographic-calibration constraint on the seasonal-timekeeping reading: Wang Pu Guanli Kelou Tu says Yue-tai is the standard but regional solstitial day/night ke and 24-qi arrow-change dates differ; Songshi separately records Lin'an/Yue-tai parameter differences.",
        "A future operational Sizijing candidate therefore cannot be a location-free universal month table. It would need seasonal/qi position, geographic calibration, a day-night/dawn-dusk model and an explicit mapping from uncertain birth event to time.",
        "No textual bridge currently authorizes importing Song official Yue-tai formulae into Sizijing. HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; no runtime candidate/winner/collapse/reopen changes.",
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-14"
    dump(p, d)


def main() -> None:
    continuity(); write_doc(); write_research(); registry(); matrix(); state()

if __name__ == "__main__":
    main()
