# Fusion Chart Historical Provenance Audit — Batch 12CL

## Scope

This batch follows Batch 12CK's regional-calibration control. It asks whether a near-contemporary official Ming record documents a policy transition between Beijing-adjusted day/night-ke values and the older Hongwu/Yongle standard, and whether that transition materially strengthens the pre-1578 ancestry case for the `59`-ke regional family later seen in `《三命通會》`.

This is historical provenance / philology / transmission-genealogy work only. It does **not** reopen deterministic charting.

## 1. Direct source and date firewall

GitHub Actions run `34943188353` fetched the NLC/Wikimedia surrogate `NLC892-CBM0103-366392` (`《明英宗睿皇帝實錄》`第18冊) and rendered all 120 PDF pages. Artifact `10386575936` has digest `sha256:d0955fd7d29c05a2b1c2abcede8cd31d26269897af7eccc3f91b5fa5a5388fad`; the source PDF SHA-256 is `ca44b5b876559842335f264950d36535cad3a95838e72c637fe8e27bda5459fd`. `NO_OCR_USED=true`.

The evidence is date-scoped:

- target event: `正統十四年十二月`, 1449;
- work compilation: Ming dynastic Shilu compilation after the event;
- surviving manuscript-copy date: unresolved from the current surrogate metadata;
- digital surrogate: modern NLC/Wikimedia digitization/mirror.

These dates are not collapsed.

## 2. Physical-page locator repair and direct collation

Direct visual review of the rendered pages gives:

```text
page 090 sha256 0e845f89966e8f2b594962ceabbb5e3535f1040f2961358bed78fd13fa357aa3
  right leaf: 錄卷之一百八十六

page 091 sha256 2a16c48279773be48e4c00fffb7d2a04794789988c9bfabf3862b48407f58942
  contains the target Datong-calendar passage
```

Key directly adjudicated phrases on page 091 are:

```text
詔更定大統曆晷刻
以北京較之南京北極出地上高三度，南極入地下低三度
冬至晝短三刻，夏至晝長三刻
今後造曆，宜悉照洪武、永樂間舊式
```

A modern transcription was used only to cross-check reading order and normalized wording after the page was physically localized. OCR output is not evidence.

A continuation-control workflow (run `35007522124`, artifact `10411764656`, digest `sha256:422cb871c13b2fe2ba4a2db6532accd39238c78a45ce54127e7e945adf4f23a0`) separately rendered NLC volume 19. It begins with the卷187 sequence, so the initial suspicion that the卷186 target might continue there is rejected. This is a research locator correction, not a historical negative result and not a product defect.

## 3. What the 1449 passage actually proves

The official record preserves a concrete policy dispute. The defence of the Beijing-adjusted rule states that, compared with Nanjing, Beijing's polar altitude differs by three degrees and its solstitial daylight differs by three ke: shorter at winter solstice and longer at summer solstice. The emperor rejects Beijing as the universal reference and orders future calendars to follow the Hongwu/Yongle old style.

Therefore the 1449 witness directly proves:

1. `region/locality` was operationally material to official Ming day/night-ke calibration;
2. a Beijing-adjusted regime existed and was defended as an approved Datong-calendar standard;
3. the court then issued an explicit restoration/rollback order to the Hongwu/Yongle old style.

It does **not** directly print `59/41` or `62/38`.

## 4. Composite reading with the already audited 1447 evidence

Batch 12CF already directly established the contemporary official distinction:

```text
Nanjing: 59 ke at the summer-solstice extreme
Beijing: 62 ke at the summer-solstice extreme
difference: 3 ke
```

Batch 12CL independently supplies the policy side of the same regional contrast: Beijing versus Nanjing differs by three ke at the solstitial extreme, and the Beijing-adjusted regime is subsequently rejected in favour of the Hongwu/Yongle old style.

The combined evidence is stronger than either item alone. It makes the Nanjing `59` branch a historically persistent regional/policy family candidate rather than an isolated 1447 numerical datum. However, the Shilu restoration order does not by itself establish exact row-for-row identity between every Hongwu/Yongle old-style daily table and the 1447 Nanjing table.

## 5. Consequence for the 1578 Sanming ancestry problem

The viable chain is now sharper:

```text
pre-1449 Hongwu/Yongle old-style regional family
  -> 1447 directly attested Nanjing 59-ke standard
  -> 1449 official restoration away from Beijing-adjusted regime
  ... missing daily-ladder / change-day / quantization bridge ...
  -> 1578 Sanming 59/41 display
```

This is a strengthened **regional/policy ancestry candidate**, not a direct-copy proof. The missing bridge still has to explain the Huqian-style one-ke intra-term ladder, Sanming's change-day fingerprint, and the coarse selection/rounding behavior identified in Batch 12CI.

## 6. Tianwen transmission impact

New nodes:

```text
DIGITAL-SURROGATE-YINGZONG-SHILU-NLC892-V18
PASSAGE-YINGZONG186-DATONG-OLD-STYLE-RESTORATION-1449
RULE-FAMILY-MING-HONGWU-YONGLE-OLD-STYLE-DATONG
```

New edges:

```text
NLC volume18 surrogate --ATTESTS--> 1449 restoration passage
1449 restoration passage --ATTESTS--> restored Hongwu/Yongle old-style policy
Hongwu/Yongle old-style family --REGIONAL_ADAPTATION_CANDIDATE_FOR--> Nanjing 59-ke 1447
restored policy family 1449 --SYNTHESIS_COMPONENT_CANDIDATE_FOR--> Sanming 1578 table
```

No direct 1449 -> Sanming table-parent edge is asserted.

## 7. Product adjudication

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
NEW_RUNTIME_CANDIDATE=false
RUNTIME_WINNER=false
CANDIDATE_COLLAPSE=false
CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
ALGORITHM_REOPEN_COUNT=0
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

## 8. Next gate

1. search 1449-1578 Nanjing/Jiangnan calendars, almanacs, or technical tables that combine the restored old-style `59`-ke cap with an explicit Huqian-like intra-term ladder or Sanming-like change-day fingerprint;
2. search for an explicit historical selection/rounding instruction capable of explaining the Batch 12CI `(78,81]/147` precision-to-coarse threshold;
3. continue the independent Fullbook upper-five-ke -> previous-night Hai lineage without conflating it with seasonal-table ancestry.

Research record: `docs/research/ZIWEI-YINGZONG-SHILU-1449-DATONG-OLD-STYLE-RESTORATION-R1.json`.
