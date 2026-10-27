# Fusion Chart Historical Provenance & School Audit R1

## Batch 11O - Joseon Sillok Native Table Collation

Status: **COMPLETE FOR FIVE LUNAR CONTROLS; SOLAR D16 PENDING DIRECT CONTINUATION IMAGE**

Batch ID: `BATCH-11-BAZI-JOSEON-SILLOK-NATIVE-COLLATION-O`

Machine-readable evidence:

`docs/research/SILLOK-CHILJEONGSAN-NATIVE-DIRECT-COLLATION-R1.json`

This batch upgrades the Sejong Sillok route from article/table-family localization to
direct no-OCR reading of five lunar target cells on official Taebaeksan native images.
It does **not** substitute the Sillok for G894 or G893, and it does not infer the
still-unread solar D16 from a filename sequence.

## 1. Reproducible official-image chain

The article-level viewer binding had already directly exposed:

- solar article `wda_50016011` → `da/ide_d156006a00` at
  `60冊 156卷 6張 A面`;
- lunar article `wda_50016016` → a 35-token official `imgArr` beginning at
  `da/ide_d156013a00`.

Native-page workflow `34015344051` at
`9bf393f5af9d4238fe8ef2198f6487da6501d377` uploaded artifact
`9983778498` (digest
`sha256:2ced8f35b0b7eaca4f4388245b30768824ffb9cfa693570149e346b60492dc01`).
It contained 34 of the 35 lunar native JPEGs at 2560×3616; the sole unavailable
token in that run was `da/ide_d156016b00`, which is not one of the five controls
closed here.

Transport workflow `34015491636` independently observed valid official JPEG bytes
for the directly bound 6A and 13A tokens.

## 2. Five direct lunar readings

| Control | Official leaf/token | Direct surface | Normalized value | Immediate comparison |
| --- | --- | --- | --- | --- |
| L8 損益分 | 156卷14張A / `ide_d156014a00` | `益一十〇分五六〇一七七五` | 10.5601775 | aligns with Goryeosa received value, not Ming 1569 10.561775 |
| L101 遲疾度 | 156卷23張A-B / `ide_d156023a00` + `ide_d156023b00` | `五度二十〇四八一一二五` | 5.20481125 | same mechanical value as Goryeosa normalization, but explicit zero is visible |
| L114 日率 | 156卷24張B / `ide_d156024b00` | `九日三四八九` | 9日3489 | aligns with Ming 1569 and direct Goryeosa images; not KRDB-o 2489 transcription |
| L124 疾行度 | 156卷25張B / `ide_d156025b00` | `疾一度〇二八一` | 1.0281 | aligns with Ming 1569 and mechanically linked Ogawa evidence; differs from Goryeosa 1.0821 |
| L132 損益分 | 156卷26張B / `ide_d156026b00` | `損七分八八六〇七五` | 7.886075 | explicit zero contrasts with Goryeosa compact `七分八八六七五` |

All five are direct human visual readings of rendered official images; OCR was not used.

## 3. Transmission consequence: no source-bloc voting

The Sillok does not fall wholesale on one side of the Ming/Goryeosa differences.

- L8 follows the Goryeosa received branch.
- L124 follows Ming 1569 and the mechanically linked Ogawa evidence.
- L101 and L132 preserve explicit positional zero glyphs that are absent in the
  corresponding compact Goryeosa received surfaces.

Therefore:

```text
WHOLE_COPY_VARIANT_INHERITANCE=FORBIDDEN
SOURCE_COUNT_AS_VARIANT_ADJUDICATION=FORBIDDEN
CELL_LEVEL_TRANSMISSION_ANALYSIS=REQUIRED
```

This is exactly the kind of evidence for which the project philology rule
`surface wording != mechanical identity` is required.

## 4. Solar D16 remains fail-closed

The directly bound official 6A native image is real and reproducible, but visual
inspection shows that it does not itself contain the D16 target cell.

Two follow-up routes were tested:

1. physical-span workflow `34018914805` / artifact `9984847854` tried the
   unobserved interior filename candidates only as transport probes; all returned
   no valid image bytes. Because those filenames were never observed from the
   official viewer, the result has **zero page/glyph authority**;
2. official image-tree workflow `34019510671` / artifact `9985014616` followed
   the viewer JavaScript's own
   `/search/ajaxSelectImageInfo.do?imageId=ide_d156006a00` route, but the API
   timed out at the starting request (`START_API_UNAVAILABLE`).

Consequently:

```text
SILLOK_SOLAR_D16=PENDING_DIRECT_OFFICIAL_CONTINUATION_IMAGE
UNOBSERVED_FILENAME_SEQUENCE_AS_PAGE_BINDING=FORBIDDEN
NETWORK_TIMEOUT_AS_SOURCE_EVIDENCE=FORBIDDEN
```

No D16 value is entered.

## 5. G894 and G893 remain independent pending witnesses

Nothing in this batch transfers Sillok values into:

- Kyujanggak `七政算內篇 奎貴894-v.1-3`;
- Kyujanggak `授時曆立成 奎貴893`.

Their physical/object identities and transmission roles remain separate. No target
value is pre-populated into either witness.

## 6. Runtime consequence

None.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN_COUNT=0
CANDIDATE_COLLAPSE_COUNT=0
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

The historical-calendar adapter remains fail-closed.

## 7. Next work

1. retry the official Sillok image-tree next-node route when the provider transport
   is available and directly bind the continuation image containing D16;
2. bind G894 exact solar/lunar target folios and read all six controls independently;
3. continue searching for direct G893 target pages without using G894/Sillok as a
   substitute;
4. compare Ming, Sillok, G894, G893, Goryeosa and Ogawa only at independently
   read cells, with edition/object and mechanical-layer distinctions preserved.
