from __future__ import annotations

import json
import re
from pathlib import Path
from textwrap import dedent

BATCH_ID = "BATCH-12-ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-CH"
PREV_ID = "BATCH-12-ZIWEI-DATONG-RICHU-DAILY-TABLE-SANMING-MULTIPOINT-REPLAY-CG"
BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-CH.md"
RESEARCH = "docs/research/ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-R1.json"
PRINT_SRC = "EXT-SISHI-QIHOU-JINGTAI6-CADAL02090387"
NCL_SRC = "EXT-NCL-SISHI-QIHOU-NCL03164"

PRINT_URL = "https://commons.wikimedia.org/wiki/File:CADAL02090387_%E5%9B%9B%E6%99%82%E6%B0%A3%E5%80%99%E9%9B%86%E8%A7%A3.djvu"
NCL_URL = "https://commons.wikimedia.org/wiki/File:NCL-03164_%E5%9B%9B%E6%99%82%E6%B0%A3%E5%80%99%E9%9B%86%E8%A7%A3.pdf"
XUXIU_URL = "https://commons.wikimedia.org/wiki/File:%E7%BA%8C%E4%BF%AE%E5%9B%9B%E5%BA%AB%E5%85%A8%E6%9B%B8%E7%AC%AC0885%E5%86%8A.pdf"

RUN_ID = 34929836894
ARTIFACT_ID = 10380982344
ARTIFACT_DIGEST = "sha256:74c581c8ef56ea20ece601e9699264466a903279c7cd67064555ac011aa9529e"
SOURCE_DJVU_SHA256 = "487180d204235660caf715b0b5a2a81dad366a68e2deecde6e44cefc5d7261fb"
DERIVED_PDF_SHA256 = "85e21d61ff32c5d25ea5e9eba35809dd21f671db28724bce9e38c4016b552c60"


def dump(path: str | Path, obj: object) -> None:
    Path(path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_committed_artifacts() -> None:
    for path in (BATCH_DOC, RESEARCH):
        if not Path(path).exists():
            raise SystemExit(f"missing committed Batch 12CH artifact: {path}")
    research = json.loads(Path(RESEARCH).read_text(encoding="utf-8"))
    if research.get("batch_id") != BATCH_ID:
        raise SystemExit("Batch 12CH research batch_id mismatch")


def continuity() -> None:
    p = Path("scripts/verify-project-continuity-state-r1.py")
    s = p.read_text(encoding="utf-8")
    if BATCH_ID not in s:
        needle = f'    "{PREV_ID}",\n]'
        if needle not in s:
            raise SystemExit("cannot locate Batch 12CG tail in continuity verifier")
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
    if NCL_SRC not in ids:
        d["sources"].append({
            "source_id": NCL_SRC,
            "title": "《四時氣候集解》NCL-03164",
            "author": "李泰",
            "historical_period": "EARLY_MING_WORK_TRANSMISSION; SURVIVING NCL OBJECT COPY DATE UNRESOLVED",
            "edition": "國家圖書館公開標示舊鈔本",
            "provider": "National Central Library rare-book object via Wikimedia Commons",
            "url": NCL_URL,
            "source_role": "OLD_MANUSCRIPT_TRANSMISSION_CONTROL_NOT_A_SECURE_PRE1578_PHYSICAL_WITNESS",
            "quality_notes": "NCL metadata records a Hongxi-1/1425 preface and Jingtai-6/1455 postface, but those internal paratext dates do not date the surviving old manuscript itself. Batch 12CH corrects the earlier acquisition-manifest overbreadth: NCL-03164 may preserve early-Ming text, but it contributes no independent pre-1578 physical-object vote unless its copy date is separately established."
        })
    if PRINT_SRC not in ids:
        d["sources"].append({
            "source_id": PRINT_SRC,
            "title": "《四時氣候集解四卷》明景泰六年胡廷璨刻本",
            "author": "李泰",
            "historical_period": "MING_JINGTAI_6_1455",
            "edition": "上海圖書館藏明景泰六年胡廷璨刻本",
            "provider": "Shanghai Library physical-copy lineage as reproduced in 續修四庫全書 / public CADAL-Wikimedia scan",
            "url": PRINT_URL,
            "bibliographic_witness_url": XUXIU_URL,
            "source_role": "DIRECT_PRE1578_PHYSICAL_PRINT_FOR_TONGSHU_LABELLED_SEASONAL_DAY_NIGHT_KE_TABLE",
            "quality_notes": "Batch 12CH renders all 123 pages without OCR for final glyph judgment. Direct pp.41/47/57 read 立夏 57/43, 小滿 59/41, 夏至 60/40 under 通書云; p.123 directly preserves 景泰六年龍集乙亥孟春吉日 dated end matter. 續修四庫全書第885冊 independently identifies the reproduced Shanghai Library copy as the Jingtai-6 Hu Tingcan print. The witness proves a pre-1578 coarse Tongshu branch but does not match Sanming 1578's Xiazhi 59/41 anchor."
        })
    d["access_date"] = "2026-09-15"
    dump(p, d)


def matrix_json() -> None:
    p = Path("docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    row = next((x for x in d["rows"] if x.get("rule_id") == "HPA-ZDATE-006"), None)
    if row is None:
        raise SystemExit("HPA-ZDATE-006 missing")
    row["batch_12ch_sishi_qihou_jingtai6_tongshu_table_control"] = {
        "source_ids": [PRINT_SRC, NCL_SRC],
        "jingtai6_1455_print_physically_reviewed": True,
        "direct_anchors": {
            "立夏": "57/43",
            "小滿": "59/41",
            "夏至": "60/40"
        },
        "same_family_as_batch_12ce_coarse_tongshu_table": True,
        "sanming_1578_xiazhi": "59/41",
        "exact_table_identity_with_sanming": False,
        "nanjing_1447_59ke_and_1455_tongshu_xiazhi_60ke_coexistence_closed": True,
        "ncl03164_old_manuscript_copy_date_unresolved": True,
        "exact_sanming_change_day_parent_closed": False,
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
    marker = "## Progress — Batch 12CH"
    if marker not in s:
        s = s.rstrip() + "\n\n" + dedent(f'''\
        {marker}

        - Direct no-OCR review of `CADAL02090387 四時氣候集解` closes a securely pre-1578 printed Tongshu-labelled coarse day/night-ke branch. Bibliographic reproduction metadata binds the object to the Shanghai Library `明景泰六年胡廷璨刻本`; physical p123 independently preserves `景泰六年龍集乙亥孟春吉日` dated end matter.
        - Physical p41/p47/p57 read `立夏 57/43`, `小滿 59/41`, `夏至 60/40`. This is the same coarse `40↔60` family independently observed in Batch 12CE and is **not** the 1578 Sanming table at the summer-solstice anchor: Sanming prints `夏至 59/41`.
        - Batch 12CF already closed an official Nanjing solstitial `59` layer in 1447. Its coexistence with a 1455 printed Tongshu `夏至 60/40` branch proves that early-Ming technical transmission remained layered; one locality/calendar standard did not simply replace all older seasonal tables.
        - NCL-03164 is retained as an `舊鈔本` transmission control only. Its internal 1425 preface and 1455 postface do not by themselves date that surviving manuscript copy, so the earlier acquisition-manifest `DIRECT_PRE1578` label is explicitly narrowed rather than propagated.
        - The composite-transmission model is strengthened but direct genealogy remains open: coarse 40↔60 seasonal lineage + Nanjing/Datong 59-ke locality layer + unresolved selection/quantization/editorial recomposition may explain Sanming, but no direct-copy edge is asserted.
        - `HPA-ZDATE-006` remains `MISSING_FROM_PRODUCT`; upper-Zi→Hai vote +0; runtime winner/candidate collapse/algorithm reopen remain none/0. Matrix counts remain 198/166/10/14 and provenance defects remain 11/11.
        - Batch 12CH also records an explicit `transmission_impact` graph section in its research JSON so future lineage work can distinguish attestation, coexistence, candidate ancestry and unproved direct-copy edges.

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
        "Batch 12CH directly reviews the Shanghai-Library-lineage Jingtai-6/1455 Hu Tingcan print of 四時氣候集解 via CADAL02090387: p41/p47/p57 physically preserve the Tongshu-labelled coarse sequence 立夏57/43, 小滿59/41, 夏至60/40; p123 preserves 景泰六年乙亥孟春 dated end matter.",
        "Batch 12CH closes an important coexistence layer: the official 1447 Nanjing 59-ke solstitial standard and a 1455 printed Tongshu Xiazhi 60/40 branch coexisted. Therefore generic 通書 wording or the isolated pair 59/41 cannot establish direct Sanming ancestry; the composite-transmission model is strengthened while exact parent/quantization remains open.",
        "Batch 12CH corrects NCL-03164 scope: it is publicly cataloged 舊鈔本 with internal 1425 preface and 1455 postface, so the surviving physical manuscript itself is not counted as pre-1578 without an independent copy-date binding.",
        "Batch 12CH begins explicit per-batch transmission-genealogy recording through a transmission_impact graph section. Next Sanming gate is a securely pre-1578 source that combines Xiazhi59/41 with Sanming-like intermediate anchors or states the recalibration/quantization rule; Fullbook upper-five-ke -> Hai remains independently unresolved."
    ]
    focus = h["current_focus"]
    for item in additions:
        if item not in focus:
            focus.append(item)
    d["schema_version"] = "1.93.0"
    d["updated_at"] = "2026-09-15"
    dump(p, d)


def main() -> None:
    validate_committed_artifacts()
    continuity()
    registry()
    matrix_json()
    matrix_md()
    state()


if __name__ == "__main__":
    main()
