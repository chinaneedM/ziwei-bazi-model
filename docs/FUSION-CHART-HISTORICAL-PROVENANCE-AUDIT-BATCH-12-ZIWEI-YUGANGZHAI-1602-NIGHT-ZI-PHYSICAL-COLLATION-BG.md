# Fusion Chart Historical Provenance Audit R1 — Batch 12BG

## 《鬱岡齋筆麈》萬曆三十年「夜子時」原葉物理校讀

Status: **DIRECT PUBLIC-DOMAIN FACSIMILE COLLATION / MING WANLI-30 (1602) WANG KENTANG WITNESS / SCAN P87–88 DIRECTLY ATTESTS PRE-MIDNIGHT FOUR KE = TODAY = 夜子時 AND POST-MIDNIGHT FOUR KE = TOMORROW / AUTHOR WARNS UNIFORM NEXT-DAY TREATMENT CAN SHIFT TWO PILLARS / NO EXPLICIT 亥-BRANCH REASSIGNMENT / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AW established an early 1594 Zhang Guo Xingzong witness for two facts that must not be conflated: birth-time Zi/Hai confusion exists, and a night-Zi upper/lower-four-ke distinction exists. It still did **not** directly state the mechanical bridge `upper/night Zi -> Hai branch`.

Batch 12BG asks whether a separate Ming witness close in time can independently fix the temporal/date semantics of the night-Zi split, and whether that witness itself supplies the missing Hai-branch reassignment.

## 2. Source and physical scan

The source is 王肯堂《鬱岡齋筆麈》. Public bibliographic/facsimile metadata identifies the relevant edition tradition as the **明萬曆三十年（1602）王懋錕刻本**.

A public-domain Wikimedia Commons DJVU was acquired directly:

- file: `CADAL02038286 鬱岡齋筆麈（三）.djvu`
- SHA-256: `c4ffdcf04c4a49e6e7d3e4d7f93a25f6740096ac9f27f1db0ccc08cdb6a6de08`
- page count: `169`
- target scan pages: `87–88`

The final glyph judgment below was made by direct visual collation of the rendered facsimile pages, not OCR.

## 3. Direct physical collation

### Scan p.87

> 夜子時
>
> 曆家以子之前四刻屬今日爲夜子時而以子
>
> 之後四刻屬明日今人生子以夜半者皆作明

### Scan p.88

> 日推筭萬一以初爲正則四柱已差兩柱矣禍
>
> 福豈不舛乎要之如西域法分二十四時而後
>
> 無兩日共一時犬牙參錯之弊也

Normalized only for punctuation, not mechanics:

> 曆家以子之前四刻屬今日，爲夜子時；而以子之後四刻屬明日。今人生子以夜半者皆作明日推筭，萬一以初爲正，則四柱已差兩柱矣，禍福豈不舛乎？要之如西域法分二十四時，而後無兩日共一時犬牙參錯之弊也。

## 4. Philological/mechanical adjudication

The physical leaf securely establishes all of the following:

1. `子之前四刻` is assigned to **今日**.
2. The same pre-midnight four-ke segment is explicitly named **夜子時**.
3. `子之後四刻` is assigned to **明日**.
4. Wang Kentang considers indiscriminately treating midnight-Zi births as the next day capable of shifting **two pillars**.
5. He prefers a 24-hour division to avoid one traditional double-hour straddling two civil/calendar dates.

This is an important independent Ming witness for the **orientation and date attribution** of night Zi. It is also very close chronologically to the 1594 Zhang Guo Xingzong witness.

But it does **not** state that the pre-midnight/night-Zi segment is mechanically reclassified as the earthly branch `亥`.

Therefore:

```text
pre-midnight upper/night Zi -> current/today date     DIRECTLY ATTESTED
post-midnight lower Zi -> next/tomorrow date          DIRECTLY ATTESTED
upper/night Zi -> Hai branch                          NOT DIRECTLY ATTESTED
```

The date-semantic bridge is stronger; the branch-reassignment bridge remains missing.

## 5. Effect on HPA-ZDATE-006

No status change is authorized:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- new explicit `亥`-branch vote: `0`
- runtime winner selected: `false`
- candidate collapsed: `false`
- algorithm reopen: `false`

The current product still lacks a source-scoped runtime method for the Nanyangtang-style half-Zi-to-Hai natal-hour candidate, but this batch does not by itself prove that candidate's branch mapping.

## 6. Relationship to the 1594 Zhang Guo witness

The two independent Ming witnesses now converge on a narrower historical point:

- Zhang Guo Xingzong 1594: night Zi has an upper/lower-four-ke division; the surrounding birth-time discussion explicitly recognizes Zi/Hai confusion.
- Yugangzhai 1602: pre-midnight four ke are `今日` and called `夜子時`; post-midnight four ke are `明日`.

What still cannot be inferred without another direct text is that the first statement's upper four ke and the second statement's night-Zi/current-day segment **must therefore be labeled Hai branch**. That inference remains philologically plausible but mechanically unclosed.

## 7. Access/research controls

The research path used only:

1. Shidian public HTML already delivered without authentication, as a locator/transcription aid;
2. a Wikimedia Commons public-domain DJVU for physical-page collation;
3. direct visual reading of the target pages.

No CText restriction was bypassed, no login was used, no private API was guessed, and OCR was not used as final glyph authority.

## 8. Durable evidence

Machine-readable evidence is stored at:

`docs/research/ZIWEI-YUGANGZHAI-1602-NIGHT-ZI-PHYSICAL-COLLATION-R1.json`

Hosted research run:

- run `34756513240`
- job `103721687957`
- artifact `10316898759`
- artifact ZIP SHA-256 `f98d7602c73f3c44ac9f65d06da6efc3bcf9bd27d613418b91156270d3aee7a4`

## 9. Next gate

Continue prioritizing an independent early source whose physical target leaf says, in direct mechanical terms, that the upper/night-Zi segment is `亥` or otherwise unambiguously maps that segment to Hai branch. Catalog-only duplicates and date-semantics-only witnesses must not be counted as that missing bridge.
