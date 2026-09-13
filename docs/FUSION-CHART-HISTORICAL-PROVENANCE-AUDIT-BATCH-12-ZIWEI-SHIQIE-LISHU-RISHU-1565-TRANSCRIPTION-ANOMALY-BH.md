# Fusion Chart Historical Provenance Audit R1 — Batch 12BH

## 《筮篋理數日抄》嘉靖四十四年本「上四亥」转录异常审判

Status: **PUBLIC TRANSCRIPTION LOCATOR / JIAJING-44 (1565) EDITION METADATA / TARGET PAGE+PARAGRAPH IDS BOUND / `上四亥` QUARANTINED PENDING PHYSICAL LEAF / SAME PASSAGE REPEATEDLY SAYS `上四刻` AND `下四刻` / INDEPENDENT TONGSHU TRANSCRIPTION ALSO SAYS `係上四刻` / NO PHYSICAL TARGET GLYPH / NO HAI-BRANCH MECHANICAL VOTE / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BG strengthened the historical date orientation of night Zi but still did not supply the missing mechanical bridge `upper/night Zi -> Hai branch`.

A new public transcription of 《筮篋理數日抄》 appears at first glance to contain the unusually attractive token `上四亥`. Because that token would materially affect HPA-ZDATE-006, this batch treats it adversarially: it must survive internal philology, independent textual control, and physical-leaf verification before it can count as a Hai-branch witness.

## 2. Source identity and access surface

Public metadata delivered by the Shidian page identifies:

- title: 《筮篋理數日抄》
- author metadata: 一壺天俱道人
- edition metadata: **嘉靖44年刊本** (1565)
- image-source metadata: **日本内阁文库**
- book ID: `NA06425`
- chapter ID: `1m44zy4jwa4ab`
- total-page metadata: `2148`

This is a **public digital transcription/locator surface**. The target physical leaf itself has not yet been directly read in this project.

## 3. Target transcription

The delivered transcription reads:

> 初初刻、初一刻、初二刻、初三刻、初四刻，巳上是上四亥。
>
> 正初刻、正一刻、正二刻、正三刻、正四刻，巳上是下四刻。
>
> 論子時隔界，凡半夜子時隔界之類，一時有八刻二十分。上四刻屬本日管，下四刻屬第二日管。
>
> ……四月二十六日甲子夜子時初二刻，小滿，是上四刻作二十六日管，故有夜字。

The target is bound on the public payload to page ID `7640563520069697576`; target paragraph ID `7649191097545588762` contains `巳上是上四亥。`.

## 4. Philological/mechanical adjudication

`上四亥` is **not** accepted as a branch-reassignment statement.

The reasons are cumulative:

1. It occurs in a counting-label slot after a five-entry list of `初...刻` values.
2. The exactly parallel lower list ends `巳上是下四刻`.
3. The immediately following explanatory prose explicitly says `上四刻屬本日管，下四刻屬第二日管`.
4. The example sentence again says `是上四刻作二十六日管`.
5. An independent received transcription of 熊宗立《類編曆法通書大全》 preserves the same mechanism as `係上四刻，屬本日管` / `係下四刻，屬第二日管`.

Accordingly, the strongest defensible judgment is:

```text
Shiqie public transcription contains literal token 上四亥     OBSERVED
physical target leaf glyph = 亥                            NOT OBSERVED
上四亥 means upper Zi is reassigned to Hai branch          NOT ESTABLISHED
upper four ke = current/base day                            TRANSCRIPTION-LEVEL SUPPORT
lower four ke = second/next day                            TRANSCRIPTION-LEVEL SUPPORT
```

Even if a future physical collation were to confirm that the printed glyph really is `亥`, the sentence would still require contextual proof that it denotes an Earthly-Branch reassignment rather than a typographical/lexical anomaly. Mechanical identity cannot be inferred from a single glyph alone.

## 5. Access-boundary findings

The research path stayed fail-closed:

- Shidian public HTML returned the edition metadata, target transcription, page IDs and paragraph IDs.
- The reviewed public SSR payload did **not** emit a literal target-page image URL for the bound target page IDs.
- The National Archives of Japan public root returned HTTP 403 to the hosted runner; no hidden search endpoint or object ID was guessed.
- A public Cabinet Library catalog mirror listed the title but emitted no literal National Archives href around the entries.

Therefore no physical target leaf was obtained and no access restriction was bypassed.

## 6. Effect on HPA-ZDATE-006

No product or historical-winner state changes:

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- new explicit Hai-branch mechanical vote: `0`
- physical Hai-glyph witness increment: `0`
- runtime winner selected: `false`
- candidate collapsed: `false`
- algorithm reopen: `false`

This batch is valuable precisely because it prevents an attractive transcription token from being overcounted.

## 7. Durable evidence

Machine-readable evidence:

`docs/research/ZIWEI-SHIQIE-LISHU-RISHU-1565-TRANSCRIPTION-ANOMALY-R1.json`

Hosted research runs are recorded there with run/job/artifact IDs and artifact ZIP SHA-256 values.

## 8. Next gate

Acquire either:

1. the physical target leaf of the Jiajing-44 《筮篋理數日抄》 copy and read the disputed glyph directly; or
2. another independent early physical leaf that states in unambiguous mechanical terms that upper/night Zi is assigned to the Earthly Branch Hai.

Date-semantics-only witnesses and catalog duplicates must continue to receive zero Hai-branch mechanical votes.
