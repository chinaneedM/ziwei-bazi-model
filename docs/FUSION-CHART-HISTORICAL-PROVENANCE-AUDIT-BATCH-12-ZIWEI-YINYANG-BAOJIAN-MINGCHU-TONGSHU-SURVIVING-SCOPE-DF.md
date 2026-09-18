# Batch 12DF — 明初《新刊陰陽寶鑒克擇通書前集》现存卷1–4目标指纹范围关闭

## Status

```text
SOURCE=新刊陰陽寶鑒克擇通書前集
CATALOG_VERSION=刻本
CATALOG_DATE=明初(1368-1424)
CATALOG_VOLUME_COUNT=5
CURRENT_SCAN_SURVIVING_SCOPE=卷1-4
SCANNED_FASCICLES=2
SCANNED_PAGES=75
PRE1578_TONGSHU_PHYSICAL_WITNESS=YES_AT_CATALOG_SCOPE
DAYNIGHT_KE_TARGET_CANDIDATE_IN_SURVIVING_V1_4=NOT_OBSERVED
WHOLE_WORK_NEGATIVE=FORBIDDEN
MISSING_VOLUME_5=OPEN
EXACT_YUELING_CITED_TONGSHU_IDENTITY=UNPROVED
RUNTIME_CHANGE=NONE
ALGORITHM_REOPEN=NONE
```

## 1. Why this follows 12DE

12DD physically bound the exact 1589 `《月令通攷》` Dahan/Yushui fingerprint to a generic source label `通書`. 12DE then directly excluded the reviewed Ming `《類編曆法通書大全》` fine 38/62 branch as the unchanged target table.

The next rational search therefore moves to other securely pre-1578 Tongshu witnesses.

The first such candidate reviewed here is `《新刊陰陽寶鑒克擇通書前集》`.

## 2. Bibliographic control

The current Chinese rare-book union-catalog record identifies:

```text
TITLE=新刊陰陽寶鑒克擇通書前集
VERSION=刻本
VOLUMES=5
PUBLICATION_DATE=明初(1368-1424)
QUANTITY=2冊
HOLDER=中國國家圖書館
NOTE=18行28字，黑口，四周雙邊
RECORD=rarecatx0302496
```

The public scan description explicitly says:

```text
存4卷：1至4
```

Therefore this object is securely useful as a **pre-1578 Tongshu witness**, but it is not a complete five-volume witness.

## 3. Controlled digital objects

### Fascicle 1

```text
OBJECT=NLC892-411999004958-98769
PAGES=29
SHA256=fa9c6ff222ff76c532380ff24292b7bb41b08cd0b8d84728348408349428a0d9
SCOPE=surviving volumes 1-2
```

### Fascicle 2

```text
OBJECT=NLC892-411999004958-98801
PAGES=46
SHA256=aef1b5fed6e6f9f946fe9b4738b7fc44f0b770c2ebb48b100f56d5125d8763fd
SCOPE=surviving volumes 3-4
```

Probe chain:

```text
RUN=35351457657
ARTIFACT=10549749706
ARTIFACT_DIGEST=sha256:a333f829cb69957f6b62da7474bfa3fe150f4fbeb3e46ef28ac3c5ecda3ce67e
RENDERED_PAGES=75
RENDER_DPI=145
CONTACT_SHEETS=4
OCR_USED_FOR_FINAL_GLYPH_CLAIMS=false
```

## 4. Text layer: zero hits, but no negative authority

The extracted text layer reports zero occurrences in both fascicles for every probe term, including:

```text
晝夜 百刻 雨水 大寒
四十三刻 四十四刻 四十七刻 四十八刻
十三後 後四日 日出 日入 銅壺 通書
```

This **does not** prove absence. The text layer is retained only as a locator control and has no content-negative authority.

## 5. Complete surviving-scope structural locator

All 75 rendered pages are covered by complete visual contact review. The locator specifically looked for the structural signatures expected from the target family:

- solar-term rows paired with day/night ke;
- 100-ke day/night numerical ladders;
- Dahan/Yushui change-day ranges;
- table architecture comparable with the physically reviewed Sanming/Yueling/Leibian/Huqian witnesses.

Result:

```text
CANDIDATE_SOLAR_TERM_DAYNIGHT_TABLE_LEAF=NOT_OBSERVED
CANDIDATE_HUNDRED_KE_DAYNIGHT_TABLE_LEAF=NOT_OBSERVED
CANDIDATE_SANMING_YUELING_FINGERPRINT_LEAF=NOT_OBSERVED
HIGH_RES_TARGET_FOLLOWUP_PAGE=NONE_IDENTIFIED
```

The surviving material is visibly dominated by selection/mantic calendrical rules, ritual/directional/auspicious-day material and related diagrams rather than the target seasonal day/night-ke numerical-table architecture.

This is a **structural-locator negative**, not a fine-glyph sentence-by-sentence negative.

## 6. Scope firewall

The allowed conclusion is:

```text
THIS_PHYSICAL_WITNESS_SURVIVING_VOLUMES_1_TO_4
  -> no candidate target table leaf observed
```

The forbidden conclusion is:

```text
THE_WHOLE_WORK
  -> never contained the target material
```

because:

```text
CATALOG_VOLUME_COUNT=5
SURVIVING_SCAN=VOLUMES_1_TO_4
VOLUME_5=MISSING_FROM_THIS_DIGITAL_OBJECT
```

A complete copy, volume 5, or another recension remains a valid target.

## 7. Relation to the 1589 Yueling citation

A title containing `通書` does not establish identity with the generic `通書` source label physically observed in Yueling 1589.

Thus:

```text
YUELING_GENERIC_TONGSHU = THIS_TITLE    UNPROVED
THIS_SURVIVING_V1_4 = EXACT_FINGERPRINT_CARRIER    NOT_OBSERVED
MISSING_V5_OR_OTHER_RECENSION = OPEN
```

This is the same anti-collapse rule established by 12DD/12DE: `通書` is a source-family label, not one invariant numeric text.

## 8. Transmission consequence

12DF does not create a positive genealogy edge. It narrows the search:

1. this early-Ming physical witness is chronologically eligible;
2. its surviving volumes 1–4 do not expose a candidate target table at complete structural-locator resolution;
3. missing volume 5 and other copies/recensions remain open;
4. other pre-1578 Tongshu/almanac witnesses should now receive priority over repeatedly rescanning the same surviving four volumes.

## 9. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA_ZDATE_006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, winner, collapse, or algorithm reopen is authorized.

Research record: `docs/research/ZIWEI-YINYANG-BAOJIAN-MINGCHU-TONGSHU-SURVIVING-SCOPE-R1.json`.
