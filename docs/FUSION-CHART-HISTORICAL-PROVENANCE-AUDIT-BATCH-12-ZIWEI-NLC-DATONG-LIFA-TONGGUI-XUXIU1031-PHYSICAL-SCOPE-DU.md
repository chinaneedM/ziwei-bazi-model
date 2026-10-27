# Fusion Chart Historical Provenance Audit R1 — Batch 12DU

## 國圖《大統曆法通軌》殘存明抄本公開實物範圍：續修四庫1031五題名序列與「三卷」口徑防火牆

Status: **XUXIU1031 PUBLIC PHYSICAL REPRODUCTION SCOPE CLOSED / NLC MING-MANUSCRIPT BLOCK DIRECTLY LOCATED AT PDF P578–P622 / 交食→日食→月食→四餘→五星 TITLE SEQUENCES DIRECTLY REVIEWED / 月食通軌終 AND 四餘纏度通軌終 DIRECTLY VISIBLE / P623 SEPARATOR / P624 NEXT WORK / 2019 THREE-JUAN VS XUXIU FIVE-NAMED-ONE-JUAN METADATA NOT NORMALIZED / CURRENT NLC CALL NUMBER UNRESOLVED / ZERO WHOLE-KE OR SANMING-PARENT VOTE / NO RUNTIME CHANGE / NO ALGORITHM REOPEN**

## 1. Why this batch

12DT closed the Kyujanggak component-set catalog model and left the separately reported National Library of China manuscript `《大統曆法通軌》三卷` as an active source gate.

The repaired National Ancient Books Census probe now parses live HTML correctly, but target-title/call-number requests still time out. That remains an access boundary, not negative evidence.

A stronger route exists at physical-reproduction level: `《續修四庫全書》第1031冊` describes and reproduces an NLC-held Ming manuscript containing the residual Tonggui title set. 12DU directly reviews that reproduction without OCR.

## 2. Source control

```text
續修四庫全書第1031冊
public PDF pages = 740
source sha256 = 07348e40ec26ca38efe9c9736a69c403c61f9b07a2c89a847fc68d00ce6d8c25
underlying copy label = 影印國家圖書館藏明抄本
exact Ming copying date = UNRESOLVED
current NLC call number = UNRESOLVED
```

Workflow: run `35436035101`, job `105878719081`, artifact `10581254254`, digest `sha256:e62c5978e36296d68321e2ba0345964947fe3214cd06952702fbcbc073e37145`.

Final title/boundary claims are direct rendered-page judgments; OCR was not used.

## 3. Direct physical sequence

- **p578** directly shows `交食通軌`; upper leaf begins `大交食通軌 / 用數日錄`. SHA256 `3a52d069759700decacd80c3ba70c9a2da7ccde25b1b6d4853105e7c72833fdb`.
- **p579–p584** is the `日食通軌` sequence. p579 lower leaf reads `日食通軌 / 欽天監正一元統 / 按經編輯`; p584 lower reproduction area is marked `原缺`, so no missing text is reconstructed.
- **p585–p591** is the `月食通軌` sequence. p591 directly reads `月食通軌終`. SHA256 `e64f4081c5bd0e510b21fd35711f4dcbb57b28abf72ee4b2b0f98897d978ca19`.
- **p591/p592–p598** is the fourth-residual sequence. p592 shows `四餘通軌`; p598 directly reads `四餘纏度通軌終`. SHA256 `f805d133f19b196bd9cf67126495326af87624ef3c60b8e34b040622b9f40bde`.
- **p599–p622** is the `五星通軌` sequence. p599 directly opens `五星通軌 / 用數日錄`; p622 remains within that title.
- **p623** is a separator; **p624** begins the next work `三垣列舍入宿去極集`.

Therefore the reproduced NLC target block is physically bounded at `p578–p622`.

## 4. “三卷” versus five named one-juan units

The registered 2019 scholarly locator reports NLC manuscript `《大統曆法通軌》三卷`.

Xuxiu1031 metadata instead describes the reproduced NLC Ming manuscript as:

```text
交食通軌一卷
日食通軌一卷
月食通軌一卷
四餘通軌一卷
五星通軌一卷
```

The direct images confirm all five named sequences. Tianwen retains both descriptions and leaves the exact codicological reason unresolved. A fascicle-vs-textual-juan or catalog-granularity explanation is possible but unproved; normalization is forbidden.

## 5. First-party NLC access boundary

Repaired census run `35435565217` / artifact `10582640319` now correctly parses `span[data-field]` markup. Network results were:

```text
20 total queries
19 target/title/call-number requests -> curl rc 28 / zero body
1 broad 元統 request -> success / 24 server hits
target identity among those broad hits -> NONE
```

So the current NLC call number/item id remains unresolved. The timeouts do not authorize a no-holding inference.

## 6. Mechanism consequence

The physically scoped title units are eclipse / residual-motion / planetary. No `太陰通軌`, `大統曆日通軌`, or `太陽通軌` title unit is observed within this p578–p622 reproduced block.

This is title-scope control only, not a whole-text negative for every calculation inside those pages.

```text
whole-ke reduction rule vote      = 0
59-ke endpoint-binding vote       = 0
exact 大寒十三後/雨水後四日 vote = 0
direct Sanming-parent vote        = 0
```

## 7. Product adjudication

```text
MATRIX_ROWS=198
AUDITED_ROWS=166
CURRENT_MISSING_FROM_PRODUCT=10
HPA-ZDATE-006=MISSING_FROM_PRODUCT
CONFIRMED_PROVENANCE_METADATA_DEFECT_COUNT=12
REPAIRED_PROVENANCE_METADATA_DEFECT_COUNT=12
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

No runtime candidate, no winner and no algorithm reopen.

## 8. Next gate

The main search returns to sources that can actually bridge continuous C-II-N fen into whole-ke display: pre-1578 Tongshu/almanac reduction or table-selection instructions, clepsydra/`改箭` institutional rules, another Datong/Tonggui mechanism section, and the exact `大寒十三後 / 雨水後四日` fingerprint.

The NLC call-number and “三卷 vs five named one-juan units” issue remains open as a catalog/codicology question.

Research record: `docs/research/ZIWEI-NLC-DATONG-LIFA-TONGGUI-XUXIU1031-PHYSICAL-SCOPE-R1.json`.
