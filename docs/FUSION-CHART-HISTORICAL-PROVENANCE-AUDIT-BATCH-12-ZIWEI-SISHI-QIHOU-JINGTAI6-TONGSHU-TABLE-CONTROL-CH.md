# Fusion Chart Historical Provenance Audit R1 — Batch 12CH

## 1455《四時氣候集解》景泰六年刻本：早明「通書」57/43→59/41→60/40 表與 1578《三命通會》南京化表的分層控制

Status: **DIRECT 1455 PHYSICAL PRINT CONFIRMS A PRE-1578 TONGSHU-LABELLED COARSE DAY/NIGHT-KE FAMILY / LIXIA 57/43, XIAOMAN 59/41, XIAZHI 60/40 PHYSICALLY READ WITHOUT OCR / THIS EARLY-MING TONGSHU BRANCH DOES NOT MATCH SANMING'S XIAZHI 59/41 / 1447 NANJING 59-KE OFFICIAL STANDARD AND 1455 TONGSHU 60-KE SUMMER-SOLSTICE TABLE THEREFORE COEXISTED / COMPOSITE-TRANSMISSION MODEL STRENGTHENED, DIRECT GENEALOGY STILL UNPROVED / NCL-03164 OLD MANUSCRIPT DATE SCOPE CORRECTED / HPA-ZDATE-006 REMAINS MISSING_FROM_PRODUCT / NO HAI VOTE / NO RUNTIME WINNER / NO ALGORITHM REOPEN**

## 1. Why this follows Batch 12CG

Batch 12CG identified a 1380s Nanjing Datong daily sunrise/daylength substrate and showed that its continuous curve can generate the numerical range occupied by the 1578 `《三命通會》` stepped day/night-ke display. It deliberately left the exact pre-1578 change-day fingerprint and quantization rule open.

The next useful witness is not another isolated `59/41` citation. We need to know what a securely pre-1578 **printed seasonal/tongshu transmission** actually did with the same numbers.

`《四時氣候集解》` is especially valuable because the work was compiled by Li Tai in the early Ming and explicitly embeds `通書云` day/night-ke statements. The direct 1455 print now lets us separate:

```text
work composition date
!= edition/impression date
!= date of a later/undated manuscript copy
```

That distinction is essential both for historical adjudication and for the new transmission-genealogy layer.

## 2. Evidence-scope correction: NCL-03164 is not itself safely datable to 1425/1455

The preceding acquisition workflow rendered NCL-03164, a 68-page National Central Library object. Its public metadata identifies it as:

```text
TITLE=四時氣候集解
AUTHOR=李泰
EDITION=舊鈔本
INTERNAL_PREFACE_DATE=洪熙元年（1425）
INTERNAL_POSTFACE_DATE=景泰六年（1455）
```

Evidence object:

```text
RUN=34926580491
ARTIFACT=10380281774
ARTIFACT_DIGEST=sha256:9d09bcff59e25617a5ef1ad2477a3f8a63ef8f295adc526b9c02360617756576
SOURCE_PDF_SHA256=c9f037cab1815ac5ac5f630f9f13659bc8acdb25b05d501ff88b7ed62a8b2ae5
PDF_PAGES=68
```

The internal preface/postface dates date the textual paratext, not automatically the surviving physical manuscript. Therefore the earlier workflow manifest label `DIRECT_PRE1578_MING_PHYSICAL_COLLATION` is too broad if applied to NCL-03164 itself.

Correct scope:

```text
NCL03164_PHYSICAL_OBJECT=OLD_MANUSCRIPT_OF_UNRESOLVED_COPY_DATE
TEXT_CONTAINS_1425_PREFACE_AND_1455_POSTFACE=true
PHYSICAL_COPY_ITSELF_PRE1578_PROVED=false
```

This correction changes no prior algorithm conclusion; it prevents a provenance shortcut.

## 3. Secure pre-1578 physical object: CADAL02090387 / Shanghai Library Jingtai-6 print

Independent bibliographic transmission records bind `《四時氣候集解四卷》` to the Shanghai Library holding described as **明景泰六年胡廷璨刻本**. `《續修四庫全書》第885冊` explicitly identifies its reproduction as an image of that Shanghai Library copy.

The public CADAL/Wikimedia object `CADAL02090387 四時氣候集解.djvu` was therefore acquired and fully rendered without OCR for final glyph judgment:

```text
RUN=34929836894
ARTIFACT=10380982344
ARTIFACT_DIGEST=sha256:74c581c8ef56ea20ece601e9699264466a903279c7cd67064555ac011aa9529e
SOURCE_DJVU_SHA256=487180d204235660caf715b0b5a2a81dad366a68e2deecde6e44cefc5d7261fb
DERIVED_PDF_SHA256=85e21d61ff32c5d25ea5e9eba35809dd21f671db28724bce9e38c4016b552c60
RENDERED_PAGES=123
OCR_USED_FOR_FINAL_GLYPH_JUDGMENT=false
```

The final physical page also directly preserves the dated end matter:

```text
景泰六年龍集乙亥孟春吉日
```

followed by the `門人武略將軍鳳陽姚福世昌書` attribution. This direct dated paratext agrees with, but does not replace, the bibliographic edition binding to the 1455 Hu Tingcan print.

## 4. Direct physical table readings

Three physically reviewed pages establish the numerical family.

### 4.1 Lixia: 57 / 43

Rendered p41, SHA-256:

```text
d5cd7938a682dc643d72d1491e5a5f2c8f89977d13d53873bcd3744333e8f448
```

Secure core reading:

```text
通書云立夏……晝五十七刻，夜四十三刻
```

### 4.2 Xiaoman: 59 / 41

Rendered p47, SHA-256:

```text
89bfdacd0c9e0e5d4b506e380ba07a166724332a76852df9d05f67894dd1d126
```

Secure core reading:

```text
小滿節
……
通書云小滿……晝五十九刻，夜四十一刻
```

### 4.3 Xiazhi: 60 / 40

Rendered p57, SHA-256:

```text
9bc7fb4730a9d85cdfd219b8592baa23c283d933a2a5a14b00bada44007c32c5
```

Secure core reading:

```text
通書云夏至……晝六十刻，夜四十刻
```

The numerical sequence is therefore directly physical:

```text
立夏 57/43
小滿 59/41
夏至 60/40
```

It agrees with the coarse `40↔60` Tongshu family already independently observed in the Ming-print `《類編曆法通書大全》` under Batch 12CE.

## 5. The decisive result: 1455 Tongshu 60/40 is not 1578 Sanming 59/41

The 1578 `《三命通會》` target display places:

```text
夏至 = 59/41
```

The direct 1455 `《四時氣候集解》` print instead places:

```text
夏至 = 60/40
```

while already containing `59/41` at `小滿`.

Therefore:

```text
SAME_NUMERIC_PAIR != SAME_SOLAR_TERM_ANCHOR
TONGSHU_LABEL != UNIQUE_TABLE_IDENTITY
PRE1578_TONGSHU_TRANSMISSION != AUTOMATIC_SANMING_PARENT
```

This is a stronger control than merely finding the number `59/41` in another early book.

## 6. Coexistence with the 1447 Nanjing 59-ke standard

Batch 12CF directly established that the official 1447 `《明英宗實錄》` record already distinguished:

```text
Nanjing solstitial extreme = 59 ke
Beijing solstitial extreme = 62 ke
```

Yet only eight years later, the physically reviewed 1455 seasonal print still preserves a `通書` summer-solstice value of `60/40`.

This means early Ming technical transmission was already layered:

```text
1447 official Nanjing/locality standard: 59-ke extreme
1455 printed Tongshu seasonal branch:    Xiazhi 60/40
```

One did not simply erase the other.

This materially strengthens the composite-transmission model developed in Batches 12CD–12CG:

```text
older coarse 40↔60 seasonal / leak-clock table family
        +
Ming Nanjing locality/calendar numerical layer
        +
possible later selection / quantization / editorial recomposition
        ->
1578 Sanming displayed 59/41 summer-solstice cap
```

The arrow remains a historical model, **not a proved direct-copy genealogy**. The exact compositing source, change-day fingerprint and quantization convention remain unresolved.

## 7. Transmission-genealogy impact

This batch is the first research record to state its lineage effect explicitly.

### Nodes strengthened

- `TEXT-WORK-SISHI-QIHOU-JIJIE`: early-Ming work with 1425 preface tradition.
- `EDITION-SISHI-QIHOU-JINGTAI6-HUTINGCAN-1455`: securely pre-1578 printed witness.
- `TABLE-FAMILY-TONGSHU-COARSE-40-60`: pre-1578 physical transmission of the coarse seasonal day/night-ke family.
- `STANDARD-NANJING-59KE-1447`: independently attested official locality standard from Batch 12CF.
- `TABLE-SANMING-1578-DAYNIGHT-KE`: later mantic display with a different Xiazhi cap/anchor.

### Edges supported

```text
SISHI_QIHOU_1455 --ATTESTS--> TONGSHU_COARSE_40_60
TONGSHU_COARSE_40_60 --PARALLEL_COEXISTS_WITH--> NANJING_59KE_1447
TONGSHU_COARSE_40_60 --STRUCTURAL_ANCESTRY_CANDIDATE_FOR--> SANMING_1578
NANJING_59KE_1447 --LOCALITY_ADAPTATION_CANDIDATE_FOR--> SANMING_1578
```

### Edges explicitly NOT established

```text
SISHI_QIHOU_1455 --DIRECT_COPY_PARENT_OF--> SANMING_1578   [NOT PROVED]
NANJING_59KE_1447 --DIRECT_TEXT_PARENT_OF--> SANMING_1578 [NOT PROVED]
```

This distinction is exactly why transmission history must be graph-shaped rather than a single lineage tree.

## 8. Product adjudication

For `HPA-ZDATE-006`:

- secure pre-1578 coarse Tongshu seasonal table: **physically closed at 1455 edition level**;
- same-family early-Ming summer-solstice cap: **60/40, not Sanming 59/41**;
- coexistence of 1447 Nanjing 59-ke standard and 1455 Tongshu 60/40 branch: **closed**;
- exact Sanming change-day/quantization parent: **open**;
- Fullbook upper-five-ke → Hai mechanical vote: **0**;
- runtime candidate/winner/collapse: **none**;
- algorithm reopen: **no**;
- `HPA-ZDATE-006`: remains **MISSING_FROM_PRODUCT**.

Accounting remains:

```text
Matrix rows = 198
Audited rows = 166
Current MISSING_FROM_PRODUCT rows = 10
Cumulative identified missing candidate families = 14
Confirmed/repaired provenance metadata defects = 11/11
Confirmed chart algorithm defects = 0
Algorithm reopens = 0
Candidate collapses = 0
```

## 9. Next gate

The Sanming-specific genealogy is now narrower. Search for a securely pre-1578 witness that either:

1. prints the `夏至 59/41` cap together with Sanming-like intermediate anchors/change-days, or
2. explicitly states a rule for recalibrating an older Tongshu `40↔60` family to a Nanjing/Datong 59-ke cap, or
3. provides a quantization/change-day rule that deterministically reproduces Sanming's displayed ladder from the Nanjing daily Datong curve.

Independently continue the Fullbook `上五刻 -> 昨夜亥時` lineage. Nothing in this batch supplies a Hai-branch vote.

Research record: `docs/research/ZIWEI-SISHI-QIHOU-JINGTAI6-TONGSHU-TABLE-CONTROL-R1.json`.
