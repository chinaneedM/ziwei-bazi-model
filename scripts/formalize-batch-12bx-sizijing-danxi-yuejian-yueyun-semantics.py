from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-SIZIJING-DANXI-YUEJIAN-YUEYUN-SEMANTICS-BX"
PREV_ID = "BATCH-12-ZIWEI-MING-INSTITUTIONAL-INCLEMENT-TIMEKEEPING-CHAIN-BW"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SIZIJING-DANXI-YUEJIAN-YUEYUN-SEMANTICS-BX.md"
RESEARCH = "docs/research/ZIWEI-SIZIJING-DANXI-YUEJIAN-YUEYUN-SEMANTICS-R1.json"
SRC_YONGLE = "EXT-TIME-YONGLE-DADIAN-18764-QIANDINGSHU-SIZIJING"
SRC_YIMEN = "EXT-NLC-YIMEN-GUANGDU-1597-SIZIJING"
SRC_SUI = "EXT-WIKISOURCE-SUI-SHU-V19-LOUKE-SEASONAL-LENGTH"
SRC_QUNSHU = "EXT-WIKISOURCE-QUNSHU-KAOSUO-V56-YUEJIAN-LOUKE"
SRC_FANGYAN = "EXT-WIKISOURCE-FANGYAN-V12-YUEYUN-ASTRONOMICAL-SEMANTICS"
SRC_HAITAO = "EXT-WIKISOURCE-HAITAO-LUN-YUEYUN-SHUOWANG"

URL_SUI = "https://zh.wikisource.org/wiki/%E9%9A%8B%E6%9B%B8/%E5%8D%B719"
URL_QUNSHU = "https://zh.wikisource.org/wiki/%E7%BE%A3%E6%9B%B8%E8%80%83%E7%B4%A2_(%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E6%9C%AC)/%E5%8D%B756"
URL_FANGYAN = "https://zh.wikisource.org/wiki/%E6%96%B9%E8%A8%80/%E5%8D%B7%E5%8D%81%E4%BA%8C"
URL_HAITAO = "https://zh.wikisource.org/wiki/%E5%85%A8%E5%94%90%E6%96%87/%E5%8D%B70440"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate BW tail")
        s = s.replace(needle, f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]', 1)
    latest = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if latest not in s:
        s, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', latest, s, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update LATEST_BATCH_DOC")
    p.write_text(s, encoding="utf-8")


def batch_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12BX

    ## 《四字經》「旦夕—月建/月運—長短」訓詁：季節漏刻語義域閉合，具體取時算法仍開放

    Status: **YONGLE PHYSICAL READING 旦夕將月建長短而推言 / YIMEN-1597 PHYSICAL READING 旦夕時刻且將月運長短定推言之 / 月建~月運 IS A REAL RECENSION VARIANT NOT OCR NOISE / SUI-SONG TIMEKEEPING CONTROLS DIRECTLY LINK QI/DOUJIAN TO SEASONAL DAY-NIGHT AND LEAK-CLOCK LENGTH / CLASSICAL 月運 HAS AN ASTRONOMICAL MOTION SENSE AND MUST NOT BE NORMALIZED TO MODERN MONTHLY-FORTUNE CYCLE / SEASONAL TIMEKEEPING SEMANTIC FIELD STRONGLY SUPPORTED / EXACT NUMERIC BIRTH-TIME RECOVERY ALGORITHM NOT PROVED / NO STEMMATIC WINNER / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

    ## 1. Physical recension readings

    Batch 12BV directly collated the Yongle-Dadian page without OCR. The relevant ending reads:

    `...天陰雨露時難定便是神仙也有差。旦夕將月建長短而推言。萬無一失矣。`

    The 1597 Yimen-Guangdu physical page directly reads across columns:

    `...天陰雨落難定便是神仙也有差別旦 / 夕時刻且將月運長短定推言之萬無一失矣。`

    Thus `月建` versus `月運` is a genuine recension-level glyph/wording difference, not a CText OCR artifact. The two witnesses also differ syntactically (`旦夕將...` versus `旦夕時刻且將...定推言之`).

    ## 2. Why `長短` belongs to a historical timekeeping semantic field

    《隋書》卷19〈漏刻〉 directly states that the hundred刻 are divided between day and night, that winter/summer have different daytime/nighttime allocations, that `漏刻皆隨氣增損`, and that the winter-summer day/night difference totals twenty刻. Its arrows encode 朝/禺/中/晡/夕, night watches and 昏旦. Evidence: `{URL_SUI}`.

    Song Zhang Ruyu's 《羣書考索》卷56〈刻漏〉 makes the seasonal bridge more explicit: the leak-clock arrows have winter/summer `長短`; it explains `斗建寅` / `斗建午` with north/south seasonal movement, then says spring causes the arrow to lengthen and autumn causes it to shorten, and finally binds forty-eight arrows to the twenty-four qi. Evidence: `{URL_QUNSHU}`.

    These controls show that a phrase combining `旦夕`, calendrical/seasonal position, and `長短` can naturally inhabit the technical vocabulary of varying day/night and leak-clock allocation. Therefore the Yongle reading `旦夕將月建長短而推言` has a strong historically grounded **seasonal-timekeeping semantic fit**.

    ## 3. Why 1597 `月運` cannot be mechanically read as modern fortune-cycle jargon

    Western Han 《方言》卷12 glosses motion terminology with `日運為躔，月運為逡` — here `月運` is plainly the moon's movement. Evidence: `{URL_FANGYAN}`.

    Tang Dou Shumeng's 《海濤論》 likewise writes `天運晦明，日運寒暑，月運朔望`, again using `月運` in an astronomical/lunar-cycle sense. Evidence: `{URL_HAITAO}`.

    Consequently the Yimen physical wording `月運長短` cannot be normalized, without further evidence, to the modern Bazi/Ziwei sense of a monthly fortune period. The local syntax `旦夕時刻且將...長短定推言之`, immediately after a birth-hour uncertainty discussion, also keeps time/calendar semantics active.

    This does **not** prove that Yimen `月運` means exactly the same operation as Yongle `月建`. Classical `月運` can denote lunar motion, while `月建` is calendrical/seasonal. The recension may preserve synonymic compression, semantic drift, scribal substitution, or a genuinely different explanatory model. The current evidence does not choose among them.

    ## 4. Philological adjudication

    The strongest admissible conclusion is:

    ```text
    YONGLE 月建長短 = STRONG_SEASONAL_TIMEKEEPING_SEMANTIC_FIT
    YIMEN 月運長短 = CLASSICAL_ASTRONOMICAL_SEMANTICS_POSSIBLE; MODERN_MONTHLY_FORTUNE_NORMALIZATION_FORBIDDEN
    月建 ↔ 月運 = REAL_RECENSION_VARIANT
    EXACT_OPERATIONAL_EQUIVALENCE = UNPROVED
    EXACT_NUMERIC_BIRTH_TIME_RECOVERY_ALGORITHM = UNPROVED
    STEMMATIC_WINNER = NONE
    ```

    The premodern leak-clock parallels explain *why* seasonal `長短` can matter for `旦夕時刻`; they do not supply the missing source-specific table, birthplace coordinate, instrument procedure, or formula needed to implement a deterministic runtime resolver.

    ## 5. Effect on HPA-ZDATE-006

    - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
    - seasonal timekeeping semantic field for `旦夕/月建/長短`: `strongly supported`;
    - Yimen `月運` = modern monthly fortune: `not authorized`;
    - exact Yongle/Yimen operational equivalence: `false/unproved`;
    - exact numeric current-time recovery mechanism closed: `false`;
    - Hai-branch mechanical vote increment: `0`;
    - runtime winner selected: `false`;
    - candidate collapsed: `false`;
    - algorithm reopen authorized: `false`.

    Global matrix/accounting counts remain unchanged.

    ## 6. Next gate

    1. Search for an independent early 《四字經》 or close derivative that preserves the complete `旦夕/月建~月運/長短` clause, to determine whether either wording has wider recension support.
    2. Search pre-Ming/Song-Ming timekeeping or fate-calculation texts for an explicit operational formula that combines 月建/節氣, day-night length and recovery of an uncertain birth hour.
    3. Keep the Fullbook `陰雨必須羅經` line separate: Batch 12BX clarifies the Sizijing semantic field but does not prove that the Fullbook compass sentence uses the same mechanism.

    Research record: `{RESEARCH}`.
    '''), encoding="utf-8")


def research() -> None:
    dump(RESEARCH, {
        "schema": "ZIWEI-SIZIJING-DANXI-YUEJIAN-YUEYUN-SEMANTICS-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "physical_readings": {
            "yongle": {
                "source_id": SRC_YONGLE,
                "reading": "旦夕將月建長短而推言萬無一失矣",
                "glyph_authority": "DIRECT_NO_OCR_PHYSICAL_COLLATION_FROM_BATCH_12BV"
            },
            "yimen_1597": {
                "source_id": SRC_YIMEN,
                "reading": "旦夕時刻且將月運長短定推言之萬無一失矣",
                "glyph_authority": "DIRECT_NO_OCR_PHYSICAL_COLLATION",
            },
            "variant": "月建~月運 PLUS SYNTAX DIFFERENCE",
            "variant_is_ocr_noise": False,
        },
        "semantic_controls": [
            {
                "source_id": SRC_SUI,
                "url": URL_SUI,
                "core": ["漏刻皆隨氣增損", "冬夏二至之間晝夜長短凡差二十刻", "每差一刻為一箭", "晝有朝禺中晡夕", "昏旦有星中"],
                "role": "PREMING_TECHNICAL_CONTROL_FOR_SEASONALLY_VARIABLE_DAY_NIGHT_LEAK_CLOCK_LENGTH",
            },
            {
                "source_id": SRC_QUNSHU,
                "url": URL_QUNSHU,
                "core": ["漏之箭晝夜共百刻冬夏之間有長短焉", "斗建寅", "斗建午", "漸北則春分而箭加長", "漸南則秋分而箭加短", "四十八箭以候二十四氣"],
                "role": "SONG_TECHNICAL_BRIDGE_FROM_DOUJIAN_SEASONAL_POSITION_TO_LEAK_ARROW_LENGTH",
            },
            {
                "source_id": SRC_FANGYAN,
                "url": URL_FANGYAN,
                "core": "日運為躔月運為逡",
                "role": "CLASSICAL_LEXICAL_CONTROL_SHOWING_YUEYUN_CAN_MEAN_LUNAR_MOTION",
            },
            {
                "source_id": SRC_HAITAO,
                "url": URL_HAITAO,
                "core": "天運晦明日運寒暑月運朔望",
                "role": "TANG_USAGE_CONTROL_FOR_ASTRONOMICAL_YUEYUN",
            },
        ],
        "adjudication": {
            "yongle_yuejian_seasonal_timekeeping_semantic_fit": "STRONG",
            "yimen_yueyun_modern_monthly_fortune_normalization_authorized": False,
            "yimen_yueyun_classical_astronomical_semantics_possible": True,
            "yuejian_yueyun_exact_operational_equivalence_proved": False,
            "recension_variant_real": True,
            "stemmatic_winner_selected": False,
            "exact_numeric_birth_time_recovery_algorithm_proved": False,
            "source_specific_table_or_formula_located": False,
        },
        "effect": {
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "hai_branch_mechanical_vote_increment": 0,
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
    add = [
        {"source_id": SRC_SUI, "title": "《隋書》卷19〈漏刻〉季節晝夜/漏刻長短", "historical_period": "TANG_HISTORIOGRAPHIC_TRANSMISSION_OF_EARLIER_TIMEKEEPING", "provider": "Wikisource", "url": URL_SUI, "source_role": "PREMING_TECHNICAL_SEASONAL_LEAK_CLOCK_CONTROL", "quality_notes": "Explicitly states 漏刻皆隨氣增損 and winter/summer day-night length differences; used for semantic/technical control, not Ziwei doctrine."},
        {"source_id": SRC_QUNSHU, "title": "宋章如愚《羣書考索》卷56〈刻漏〉斗建/四十八箭", "historical_period": "SONG", "provider": "Wikisource / Siku transmission", "url": URL_QUNSHU, "source_role": "SONG_DOUJIAN_TO_SEASONAL_LEAK_ARROW_LENGTH_BRIDGE", "quality_notes": "Links 斗建寅/午 and seasonal north-south progression to arrow lengthening/shortening and 48 arrows for 24 qi; not a direct Sizijing witness."},
        {"source_id": SRC_FANGYAN, "title": "楊雄《方言》卷12 日運/月運詞義", "historical_period": "WESTERN_HAN_TEXT_TRADITION", "provider": "Wikisource", "url": URL_FANGYAN, "source_role": "CLASSICAL_LEXICAL_CONTROL_FOR_YUEYUN_ASTRONOMICAL_MOTION", "quality_notes": "Reads 日運為躔，月運為逡; prevents automatic normalization of 月運 to modern monthly-fortune jargon."},
        {"source_id": SRC_HAITAO, "title": "唐竇叔蒙《海濤論》月運朔望", "historical_period": "TANG", "provider": "Wikisource / Quan Tang Wen", "url": URL_HAITAO, "source_role": "TANG_USAGE_CONTROL_FOR_YUEYUN_ASTRONOMICAL_SEMANTICS", "quality_notes": "Uses 天運晦明、日運寒暑、月運朔望; corroborates a non-fortune astronomical use of 月運."},
    ]
    for x in add:
        if x["source_id"] not in ids:
            d["sources"].append(x)
    d["access_date"] = "2026-09-14"
    dump(p, d)


def matrix() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next(x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bx_sizijing_danxi_yuejian_yueyun_semantics"] = {
        "source_ids": [SRC_YONGLE, SRC_YIMEN, SRC_SUI, SRC_QUNSHU, SRC_FANGYAN, SRC_HAITAO],
        "physical_variant": "YONGLE=旦夕將月建長短而推言; YIMEN1597=旦夕時刻且將月運長短定推言之",
        "seasonal_timekeeping_semantic_field": "STRONGLY_SUPPORTED",
        "yueyun_modern_monthly_fortune_normalization_authorized": False,
        "exact_operational_equivalence_proved": False,
        "exact_numeric_recovery_algorithm_proved": False,
        "runtime_winner_selected": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH,
    }
    dump(p, d)
    mdp = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = mdp.read_text(encoding="utf-8")
    if "## Progress through Batch 12BX" not in md:
        md += dedent('''

        ## Progress through Batch 12BX

        - The end of the Sizijing inclement-time passage now has a two-recension physical reading: Yongle `旦夕將月建長短而推言` versus 1597 Yimen `旦夕時刻且將月運長短定推言之`; `月建/月運` is a genuine recension variant, not OCR noise.
        - Premodern technical controls place `旦夕/長短` in a real seasonal timekeeping domain: Sui Shu says leak-clock allocation changes with qi and winter/summer day-night length, while Song Qunshu Kaosuo explicitly links 斗建 and seasonal progression to leak-arrow length and 48 arrows keyed to 24 qi.
        - Classical `月運` also means lunar motion (`方言`: 日運為躔、月運為逡; Tang 海濤論: 月運朔望), so the Yimen reading cannot be silently converted into a modern monthly-fortune cycle.
        - Semantic domain is narrowed, but exact 月建↔月運 operational equivalence and a numeric birth-time recovery formula remain unproved. HPA-ZDATE-006 and runtime invariants do not change.
        ''')
    mdp.write_text(md, encoding="utf-8")


def state() -> None:
    p = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    d["schema_version"] = "1.83.0"
    a = d["historical_audit"]
    if BATCH_ID not in a["completed_batches"]:
        a["completed_batches"].append(BATCH_ID)
    a["latest_batch_doc"] = BATCH_DOC
    notes = [
        "Batch 12BX physically fixes the Sizijing post-inclement clause as Yongle 旦夕將月建長短而推言 versus 1597 Yimen 旦夕時刻且將月運長短定推言之; 月建/月運 is real recension variation, not OCR noise.",
        "Sui/Song technical controls strongly support a seasonal timekeeping semantic field: leak-clock day/night allocation varies with qi and length, and Song Qunshu Kaosuo explicitly connects 斗建 seasonal movement to arrow length and 48 arrows for 24 qi.",
        "Classical 月運 can mean lunar motion, so modern monthly-fortune normalization is forbidden. Exact 月建~月運 operational equivalence and numeric uncertain-birth-hour recovery remain open; HPA-ZDATE-006/runtime/reopen invariants remain unchanged.",
    ]
    for n in notes:
        if n not in a["current_focus"]:
            a["current_focus"].append(n)
    d["updated_at"] = "2026-09-14"
    dump(p, d)


def main() -> None:
    continuity(); batch_doc(); research(); registry(); matrix(); state()

if __name__ == "__main__":
    main()
