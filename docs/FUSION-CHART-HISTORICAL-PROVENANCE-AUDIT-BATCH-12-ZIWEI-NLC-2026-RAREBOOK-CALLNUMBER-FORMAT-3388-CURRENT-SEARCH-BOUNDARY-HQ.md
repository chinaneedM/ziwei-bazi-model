# Fusion Chart Historical Provenance Audit R1 — Batch 12HQ

## 国图善本“索书号”前导零格式与 FID070 当前编号检索边界

Status: **CURRENT NLC 3388/03388 SEARCH RERUN = NO TARGET CROSSWALK / 2026 NLC RARE-BOOK PUBLICATION DIRECTLY USES 索书号 02461, 09373, 11261 / LEADING-ZERO FORMAT IS INSTITUTIONALLY REAL BUT TARGET 3388→03388 REMAINS UNPROVED / SEARCH-ONLY HYPOTHESIS AUTHORIZED, IDENTITY CLAIM FORBIDDEN / CURRENT SYS-UID-905S, 3368↔3388 SUCCESSION AND EXACT QU ACCESSION BATCH REMAIN UNRESOLVED / ZERO PRODUCT OR MATRIX CHANGE**

## 1. Why this batch exists

Batch 12HP closed the physical-object identity of FID `412004000070` and the Tieqin Tongjian Lou Yuan-impression ten-line witness at a high-confidence multilayer provenance/catalog/format level. It deliberately left three different identifier layers unresolved:

```text
1959 printed number 3368
1987 book number 3388
current NLC SYS / UID / 905s / shelfmark
```

The immediate question is whether current public NLC evidence permits either `3388 -> 03388` or a direct modern machine-identifier crosswalk. It does not.

## 2. Fresh current-catalog rerun

The already committed Batch 12HN probe was rerun against the live NLC metadata service on 2026-09-27.

```text
workflow run = 36308947738
rerun attempt = 2
job = 108608704600
artifact = 10930436779
artifact digest = sha256:398cc3cc2a45348aeb92b3f46e30af26a576c58f15e3c335f97ed948b264ddcd
```

Observed outcomes:

```text
3388           -> no matching result
03388          -> no matching result
SBYL:03388     -> no matching result
NLC:SBYL:03388 -> server error
题名 + 3388     -> unrelated 2010 knitting-book false positive
题名 + 03388    -> timeout
```

Therefore current SYS / UID / 905s / shelfmark all remain `UNRESOLVED`. A failed public lookup is not an absence proof.

The rerun reused the already committed HN workflow source revision `ef2fc91c...`; it is evidence about the external NLC responses at rerun time, not an exact-current-project-HEAD CI claim.

## 3. New institutional formatting control

A National Library of China / China Ancient Books Protection page dated 2026-04-09 presents the National Library Rare Books Department's newly published `《北京图书馆古籍善本书目》配补本图录` (国家图书馆古籍馆 编, 广西师范大学出版社, 2026年03月, ISBN 978-7-5598-9279-9).

The page explicitly states that the work is selected and ordered from the 1987 `《北京图书馆古籍善本书目》` (`《北图善目》`) and labels concrete rare-book locators as **索书号**:

```text
《资治通鉴》   索书号 02461
《外台秘要方》 索书号 09373
《藏说小萃》   索书号 11261
```

Source: https://www.nlc.cn/pcab/zx/xw/20260409_2652363.shtml

This establishes `LEADING_ZERO_FIVE_DIGIT_RAREBOOK_CALL_NUMBER_FORMAT = DIRECTLY_ATTESTED_ON_A_CURRENT_NLC_HOSTED_INSTITUTIONAL_SURFACE`.

## 4. What this does not prove

The 2026 page does not print the target title, `3388`, or `03388`. It also does not state whether its five-digit examples preserve the exact 1987 printed number including its original leading-zero semantics, or pass through a later/current call-number formatting layer.

Therefore the project must not infer `3388 = 03388` from formatting similarity alone.

Forward-only adjudication:

```text
AUTOMATIC_ZERO_PADDING_AS_ASSERTED_IDENTITY = FORBIDDEN
LITERAL_03388_AS_SEARCH_CANDIDATE = AUTHORIZED_AS_SEARCH_ONLY_HYPOTHESIS
```

This narrows the old firewall without rewriting HN or HP: `03388` is now a historically/institutionally plausible query form, but still not a proved identifier for FID070.

## 5. 3368 and 3388 remain separate historical layers

Nothing in this batch explains why the 1959 catalog prints `3368` while the 1987 catalog prints `3388` for the same high-confidence object identity chain.

```text
DIRECT_3368_TO_3388_SUCCESSION_RECORD = false
RENUMBERING_OR_CATALOG_SUCCESSION_MECHANISM = UNRESOLVED
```

No offset rule, insertion rule, zero-padding rule, or global catalog arithmetic may be invented from the difference.

## 6. Donation/accession chronology remains object-unresolved

Existing institutional evidence establishes that Qu/Tieqin books entered public custody through multiple donation and priced-transfer episodes. Batch 12HP establishes `瞿捐` on the exact 1959 target entry. This batch still does not recover an accession ledger or transfer list that assigns FID070 to one exact batch/date.

```text
FID070_EXACT_QU_DONATION_OR_ACCESSION_BATCH = UNRESOLVED
FID070_EXACT_QU_DONATION_OR_ACCESSION_DATE = UNRESOLVED
```

Aggregate family chronology is not object-level membership evidence.

## 7. Product and transmission firewall

This is an identifier/access-history boundary only. Matrix rows = 198; audited rows = 166; MISSING_FROM_PRODUCT = 10; confirmed chart algorithm defects = 0; algorithm reopen = 0; candidate collapse = 0; runtime rule change = false; transmission genealogy topology change = false. Batch 12HP's physical-object identity closure remains intact.

## 8. Next gate

Highest-value next work:

1. recover an object-specific current NLC SYS/UID/905s/shelfmark bridge for FID070;
2. recover direct catalog-preparation or succession evidence explaining 1959 `3368` versus 1987 `3388`;
3. recover the exact Qu donation/accession batch/date from accession/donation/transfer records;
4. continue Zhang Lijuan 2018 full-text retrieval for current-identifier/detail evidence.

Until then:

```text
03388 = SEARCH HYPOTHESIS ONLY
3388 = DIRECT 1987 BOOK NUMBER
3368 = DIRECT 1959 PRINTED NUMBER
FID 412004000070 = DIGITAL/OLD-CATALOG CONTROL LAYER
CURRENT NLC MACHINE IDENTIFIER = UNRESOLVED
```
