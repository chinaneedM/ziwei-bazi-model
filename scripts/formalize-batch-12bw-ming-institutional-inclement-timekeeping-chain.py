from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-MING-INSTITUTIONAL-INCLEMENT-TIMEKEEPING-CHAIN-BW"
PREV_ID = "BATCH-12-ZIWEI-YONGLE-DADIAN-18764-DIRECT-GLYPH-COLLATION-BV"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MING-INSTITUTIONAL-INCLEMENT-TIMEKEEPING-CHAIN-BW.md"
RESEARCH_ARTIFACT = "docs/research/ZIWEI-MING-INSTITUTIONAL-INCLEMENT-TIMEKEEPING-CHAIN-R1.json"
SRC_ZHENGDE = "EXT-CTEXT-ZHENGDE-MING-HUIDIAN-V176-TIMEKEEPING"
SRC_WANLI = "EXT-CTEXT-WANLI-DAMING-HUIDIAN-V223-TIMEKEEPING"
SRC_XINFA = "EXT-SHIDIAN-XINFA-SUANSHU-V1-DINGSHI-LUOJING"
FULLBOOK_AJ = "docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json"

URL_ZHENGDE = "https://ctext.org/wiki.pl?chapter=934432&if=gb"
URL_WANLI = "https://ctext.org/wiki.pl?chapter=242488&if=gb"
URL_XINFA = "https://www.shidianguji.com/zh/book/SK1525/chapter/1lasu1xyun8dl"


def dump_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_continuity_verifier() -> None:
    path = Path("scripts/verify-project-continuity-state-r1.py")
    text = path.read_text(encoding="utf-8")
    if BATCH_ID not in text:
        needle = f'    "{PREV_ID}",\n]'
        replacement = f'    "{PREV_ID}",\n    "{BATCH_ID}",\n]'
        if needle not in text:
            raise SystemExit("cannot locate Batch 12BV tail in continuity verifier")
        text = text.replace(needle, replacement, 1)
    wanted = f'LATEST_BATCH_DOC = "{BATCH_DOC}"'
    if wanted not in text:
        text, n = re.subn(r'^LATEST_BATCH_DOC = ".*"$', wanted, text, count=1, flags=re.MULTILINE)
        if n != 1:
            raise SystemExit("cannot update latest batch doc")
    path.write_text(text, encoding="utf-8")


def write_batch_doc() -> None:
    Path(BATCH_DOC).write_text(dedent(f'''\
    # Fusion Chart Historical Provenance Audit R1 — Batch 12BW

    ## 明代陰雨時刻取得與報時制度鏈：漏刻、時牌、鼓更、鐘鼓，及《新法算書》「晨昏陰雨用行漏」

    Status: **MING INSTITUTIONAL CURRENT-TIME ACQUISITION / DISSEMINATION CHAIN CLOSED AT TECHNICAL-CONTEXT LEVEL / ZHENGDE AND WANLI HUIDIAN TRANSMISSIONS RECORD 定時刻有漏・換時有牌・報更有鼓・晨昏有鐘鼓 / QINTIANJIAN LEAK-CLOCK PERSONNEL 調壺換牌 AND 報時 / XINFA-SUANSHU EXPLICITLY ASSIGNS DAY TO SUN-DIAL, NIGHT TO STAR-DIAL, MERIDIAN TO CORRECTED COMPASS, AND DAWN-DUSK-CLOUD-RAIN TO CALIBRATED RUNNING CLEPSYDRA / ORDINARY COMPASS-ALONE CLOCK EQUIVALENCE REJECTED / FULLBOOK 羅經 WORDING REMAINS SOURCE-SCOPED AND OPERATIONALLY UNRESOLVED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

    ## 1. Scope

    Batch 12AJ established a semantic tension: two directly reviewed Fullbook physical routes agree on `如天氣陰雨之際必須羅經以定真確時候`, whereas contemporary Ming astronomical practice assigns the compass to meridian orientation and a running clepsydra to dawn/dusk/cloud/rain timekeeping. Batch 12BW asks a narrower historical-operations question: what did Ming state timekeeping actually use to maintain and publish current time when celestial observation was unavailable?

    The answer is now sufficiently explicit to close the **institutional technical-context layer**, while leaving the Fullbook author's source-scoped use of `羅經` unresolved.

    ## 2. Zhengde 《明會典》 institutional chain

    The Zhengde 《明會典》 tradition, 欽天監 section, records:

    ```text
    凡定時刻有漏
    換時有牌
    報更有鼓
    警晨昏有鐘鼓
    ...
    輪差漏刻博士提調陰陽人如法調壺換牌
    ```

    Electronic witness: `{URL_ZHENGDE}`.

    This is an operational chain rather than a loose instrument list: the leak establishes time, hour tablets are changed, night watches are announced by drum, dawn/dusk by bell/drum, and designated Qintianjian personnel maintain the water clock and tablets.

    ## 3. Wanli 《大明會典》 continuity

    The Wanli recompilation preserves the same institutional structure:

    ```text
    凡定時刻有漏、換時有牌、報更有鼓、警晨昏有鐘鼓
    ...
    輪差漏刻博士、提調陰陽人、如法調壺換牌
    ```

    It separately describes court ceremony with the `漏刻博士` responsible for timing and a `五官司晨` reporting the hour/holding the time tablet.

    Electronic witness: `{URL_WANLI}`.

    Zhengde and Wanli are treated as transmitted/recompiled institutional controls, not as two statistically independent votes for one physical manuscript.

    ## 4. Chongzhen technical specification closes the inclement-weather function

    Xu Guangqi and the calendar bureau's 《新法算書》 technical memorandum makes the functional division explicit:

    ```text
    日晷以定晝時
    星晷以定夜時
    正線羅經以定子午
    若晨昏陰雨，當造如式行漏 ... 以濟二晷所不及
    ```

    It further says the water clock must be calibrated against celestial time; a normal compass gives direction rather than time and exclusive reliance on a compass can introduce variable time error.

    Electronic witness: `{URL_XINFA}`.

    Therefore a historically attested Ming technical current-time chain is:

    ```text
    celestial calibration / true meridian
      -> sun dial by day
      -> star dial by night
      -> calibrated running clepsydra when dawn/dusk/cloud/rain blocks the two dials
      -> institutional time tablet / drum / bell dissemination
    ```

    ## 5. Firewall against rewriting the Fullbook sentence

    This batch does **not** emend `羅經` to `行漏`, `壺漏`, `鐘`, or any other word. Two Fullbook physical edition routes already agree on `羅經`; there is presently no source-close physical variant showing an alternative glyph.

    The admissible conclusion is instead:

    ```text
    MING_INSTITUTIONAL_INCLEMENT_CURRENT_TIME_MECHANISM = CLOSED
    FULLBOOK_SOURCE_SCOPED_LUOJING_OPERATIONAL_MECHANISM = UNRESOLVED
    LUOJING_AS_STANDALONE_CLOCK = NOT_SUPPORTED_BY_CONTEMPORANEOUS_TECHNICAL_CONTROL
    ```

    This distinction matters: technical context can constrain interpretation, but it cannot silently replace the wording of the Ziwei witness.

    ## 6. Relation to the newly collated Sizijing line

    Batch 12BV physically closed `天陰雨露時難定` in the Yongle-Dadian recension, while the 1597 Yimen witness physically reads `天陰雨落難定`. Both establish the historical problem of inclement-weather birth-time uncertainty. Their following `旦夕/月建~月運/長短` wording may encode a seasonal or calendrical heuristic, but its exact mechanics are not yet proved and Batch 12BW does not use it to substitute for an instrument-based clock.

    ## 7. Effect on HPA-ZDATE-006

    - `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
    - Ming institutional inclement-current-time acquisition mechanism closed at technical-context level: `true`;
    - Fullbook source-scoped `羅經` operational mechanism closed: `false`;
    - ordinary compass-alone clock equivalence: `rejected`;
    - local apparent solar time runtime winner: `false`;
    - Hai-branch mechanical vote increment: `0`;
    - candidate collapsed: `false`;
    - algorithm reopen authorized: `false`.

    Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; chart algorithm defect/reopen/collapse remain `0/0/0`.

    ## 8. Next gate

    1. Search Fullbook-adjacent Ming/Qing Ziwei, fate-calculation, compass and calendrical witnesses for a source-close explanation of why `羅經` is invoked in cloudy/rainy birth-time determination.
    2. Continue philological work on the `旦夕將月建長短` versus `旦夕時刻且將月運長短` recension difference; do not call it a day-length algorithm until an operational parallel is found.
    3. Preserve the institutional clock chain as context only until a documented bridge connects it to the Fullbook practice statement.

    Research record: `{RESEARCH_ARTIFACT}`.
    '''), encoding="utf-8")


def write_research_artifact() -> None:
    data = {
        "schema": "ZIWEI-MING-INSTITUTIONAL-INCLEMENT-TIMEKEEPING-CHAIN-R1",
        "batch_id": BATCH_ID,
        "prior_batch_id": PREV_ID,
        "prior_fullbook_semantics": FULLBOOK_AJ,
        "question": "What operational infrastructure did Ming institutions use to acquire and disseminate current time when direct celestial observation was unavailable, and does that close the Fullbook luojing wording?",
        "institutional_controls": [
            {
                "source_id": SRC_ZHENGDE,
                "title": "(正德)明會典 卷176 欽天監",
                "url": URL_ZHENGDE,
                "readings": ["定時刻有漏", "換時有牌", "報更有鼓", "警晨昏有鐘鼓", "漏刻博士", "如法調壺換牌"],
                "classification": "MING_INSTITUTIONAL_TIME_ACQUISITION_AND_PUBLIC_SIGNAL_CHAIN",
            },
            {
                "source_id": SRC_WANLI,
                "title": "(萬曆)大明會典 卷223 欽天監",
                "url": URL_WANLI,
                "readings": ["定時刻有漏", "換時有牌", "報更有鼓", "警晨昏有鐘鼓", "漏刻博士", "如法調壺換牌"],
                "classification": "MING_INSTITUTIONAL_CONTINUITY_CONTROL",
            },
        ],
        "technical_control": {
            "source_id": SRC_XINFA,
            "title": "徐光啟等《新法算書》卷一 定時器具奏疏",
            "url": URL_XINFA,
            "functional_partition": {
                "day": "日晷以定晝時",
                "night": "星晷以定夜時",
                "meridian": "正線羅經以定子午",
                "dawn_dusk_cloud_rain": "行漏以濟二晷所不及",
            },
            "calibration": "clepsydra is calibrated against celestial instruments/time; it is not an uncalibrated absolute clock",
            "ordinary_compass_alone_clock_equivalence": False,
        },
        "adjudication": {
            "ming_institutional_inclement_current_time_mechanism_closed": True,
            "mechanism": "CELESTIAL_CALIBRATION_PLUS_SUN_OR_STAR_DIAL_WITH_CALIBRATED_RUNNING_CLEPSYDRA_FALLBACK_AND_PUBLIC_TIME_SIGNALS",
            "fullbook_source_scoped_luojing_operational_mechanism_closed": False,
            "fullbook_luojing_emended_to_xinglou": False,
            "fullbook_luojing_emended_to_hulou": False,
            "direct_fullbook_variant_supporting_emendation_found": False,
            "technical_context_can_replace_fullbook_wording": False,
        },
        "effect": {
            "hpa_zdate_006_status": "MISSING_FROM_PRODUCT",
            "institutional_context_layer_closed": True,
            "runtime_time_standard_winner_selected": False,
            "hai_branch_mechanical_vote_increment": 0,
            "candidate_collapsed": False,
            "algorithm_reopen_authorized": False,
            "matrix_counts_changed": False,
        },
    }
    dump_json(Path(RESEARCH_ARTIFACT), data)


def update_registry() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    existing = {s.get("source_id") for s in data["sources"]}
    additions = [
        {
            "source_id": SRC_ZHENGDE,
            "title": "(正德)《明會典》卷176欽天監定時刻/漏刻制度",
            "historical_period": "MING_ZHENGDE_COMPILATION_TRADITION",
            "provider": "Chinese Text Project",
            "url": URL_ZHENGDE,
            "source_role": "MING_INSTITUTIONAL_TIMEKEEPING_OPERATION_CONTROL",
            "quality_notes": "Records 定時刻有漏 / 換時有牌 / 報更有鼓 / 警晨昏有鐘鼓 and Qintianjian leak-clock personnel. Electronic base is a later transmitted edition; use for institutional text/semantics, not Ming-print glyph authority.",
        },
        {
            "source_id": SRC_WANLI,
            "title": "(萬曆)《大明會典》卷223欽天監定時刻/漏刻制度",
            "historical_period": "MING_WANLI_RECOMPILATION_1587",
            "provider": "Chinese Text Project",
            "url": URL_WANLI,
            "source_role": "MING_INSTITUTIONAL_TIMEKEEPING_CONTINUITY_CONTROL",
            "quality_notes": "Preserves the same leak-clock/time-tablet/drum/bell operational structure and court reporting duties. Do not double-count Zhengde and Wanli transmissions as independent physical witnesses.",
        },
    ]
    for item in additions:
        if item["source_id"] not in existing:
            data["sources"].append(item)
    data["access_date"] = "2026-09-14"
    dump_json(path, data)


def update_matrix() -> None:
    path = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    row = next(r for r in data["rows"] if r.get("rule_id") == "HPA-ZDATE-006")
    row["batch_12bw_ming_institutional_inclement_timekeeping_chain"] = {
        "source_ids": [SRC_ZHENGDE, SRC_WANLI, SRC_XINFA],
        "institutional_chain": ["漏刻定時", "時牌換時", "鼓報更", "鐘鼓警晨昏"],
        "technical_partition": "日晷定晝 / 星晷定夜 / 正線羅經定子午 / 晨昏陰雨用校準行漏",
        "ming_institutional_inclement_current_time_mechanism_closed": True,
        "fullbook_source_scoped_luojing_mechanism_closed": False,
        "ordinary_compass_standalone_clock_equivalence": False,
        "runtime_winner_selected": False,
        "algorithm_reopen_authorized": False,
        "research_artifact": RESEARCH_ARTIFACT,
    }
    dump_json(path, data)

    mdp = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.md")
    md = mdp.read_text(encoding="utf-8")
    if "## Progress through Batch 12BW" not in md:
        md += dedent('''

        ## Progress through Batch 12BW

        - Ming institutional timekeeping is now closed at the technical-context layer: the Zhengde and Wanli Huidian traditions record leak-clock time determination, hour-tablet changes, drum watch reporting, and bell/drum dawn-dusk signaling, with Qintianjian leak-clock personnel maintaining the system.
        - Xu Guangqi's Chongzhen technical memorandum supplies the weather fallback explicitly: sun dial by day, star dial by night, corrected compass for meridian orientation, and calibrated running clepsydra for dawn/dusk/cloud/rain when the dials cannot operate.
        - This establishes a historically attested inclement-weather current-time mechanism in Ming technical practice, but does not rewrite the Fullbook physical reading `羅經` into `行漏` or prove what exact instrument composition Fullbook practitioners intended.
        - HPA-ZDATE-006 remains MISSING_FROM_PRODUCT; no runtime winner, Hai mechanical vote, candidate collapse or algorithm reopen follows from this contextual closure.
        ''')
    mdp.write_text(md, encoding="utf-8")


def update_state() -> None:
    path = Path("docs/PROJECT-CURRENT-STATE-R1.json")
    state = json.loads(path.read_text(encoding="utf-8"))
    state["schema_version"] = "1.82.0"
    audit = state["historical_audit"]
    if BATCH_ID not in audit["completed_batches"]:
        audit["completed_batches"].append(BATCH_ID)
    audit["latest_batch_doc"] = BATCH_DOC
    additions = [
        "Batch 12BW closes the Ming institutional inclement-current-time mechanism at technical-context level: Zhengde/Wanli Huidian transmit 漏刻定時→時牌換時→鼓報更→鐘鼓警晨昏, while Chongzhen Xinfa Suanshu explicitly assigns cloudy/rainy fallback to a calibrated running clepsydra after celestial calibration.",
        "This does not emend the directly stable Fullbook physical reading 羅經. Fullbook's source-scoped operational meaning remains unresolved; ordinary compass-alone clock equivalence is rejected by contemporary technical control.",
        "HPA-ZDATE-006 remains MISSING_FROM_PRODUCT and runtime/Hai-vote/collapse/reopen invariants remain unchanged. Next gate is a source-close Fullbook-adjacent bridge for 羅經 or a defensible philological closure of the 旦夕/月建~月運/長短 wording.",
    ]
    for item in additions:
        if item not in audit["current_focus"]:
            audit["current_focus"].append(item)
    state["updated_at"] = "2026-09-14"
    dump_json(path, state)


def main() -> None:
    update_continuity_verifier()
    write_batch_doc()
    write_research_artifact()
    update_registry()
    update_matrix()
    update_state()


if __name__ == "__main__":
    main()
