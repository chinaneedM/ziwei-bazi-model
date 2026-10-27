# Fusion Chart Historical Provenance Audit R1 — Batch 12AM

## 徐善繼、徐善述《人子須知》：明代術數內部的臬測—磁針機械語義橋

Status: **EARLY-MING SHUSHU DIRECT FACSIMILE BOUND / 正針縫針 DIRECT NO-OCR COLLATION / 臬測以景 vs 針以氣 MECHANICAL SEPARATION CONFIRMED / LUOJING NOT A STANDALONE CLOCK / FULLBOOK CLOUDY-RAINY TIME-GENERATION CHAIN STILL UNRESOLVED / NO CANDIDATE SELECTION / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12AJ established that contemporaneous Ming astronomical controls distinguish sundial/star-dial/clepsydra functions from meridian-compass orientation. Batch 12AK then supplied a much later Jiaqing operational bridge showing how compass orientation, celestial time measurement and mechanical-clock fallback could coexist.

Batch 12AM asks a narrower question: is there a sufficiently early **術數-internal** witness explaining what the needle/羅經 does mechanically relative to an astronomical reference, without projecting the Qing clock system backward?

The answer is yes. This closes the semantic bridge, not the Fullbook cloudy/rainy time-generation procedure.

## 2. Bibliographic and facsimile identity

CiNii Books NCID `BB17866565` binds `重刋人子須知資孝地理心學統宗 8卷`, 徐善繼、徐善述, 梅墅石渠閣, `萬暦11 [1583] 序`, with a holding at 東京大学 東洋文化研究所 図書室. It is an edition-family bibliographic witness only; exact physical-copy identity to the scan below is not claimed.

Wikimedia Commons exposes a 510-page mechanical scan labelled `重刊人子須知資孝地理心學統宗 八卷 / 明 徐善繼、徐善述 / 隆慶三年刊 / 萬曆十一年梅墅石渠閣補刊本`, source `故宮珍本叢刊`.

```text
WORKFLOW_RUN=34332573715
PROBE_COMMIT=3882638a6de37a248134f5ae2185a91758dccf4a
ARTIFACT=10096390533
ARTIFACT_ZIP_SHA256=b79fb61aa46624a601c97fff386fb5090afeb4aaa8dd07f382e9c3f5cf6977b6
PDF_BYTES=263325842
PDF_SHA256=80de366d62066bf73046834771a43976fdf353de6ea1704d06c46dfa568a44ba
PDF_PAGES=510
```

The original-file URL came from the Commons API, not identifier guessing. The exact target leaves are not assigned individually to the 1569 original blocks versus the 1583 supplementary blocks; that printing-phase question remains open.

## 3. Direct no-OCR physical collation

The scan was first contact-sheeted for visual localization, then the relevant window was re-rendered at higher resolution. No OCR was generated or used for the decisive reading.

### PDF p414

Direct heading: `三昧論有引`.

Rendered JPEG SHA-256: `dd5a837256f30491cecdd783f63f980450764cfb0acf9ab268bf6a9215708405`.

### PDF p415

Direct heading: `正針縫針`.

The physical page directly frames the procedure through `地理之用莫切於羅經`, spring/autumn equinox gnomon-shadow measurement, `立內外二盤`, and distinguishes `正針` from `縫針` according to needle versus gnomon-measured direction.

Rendered JPEG SHA-256: `cfdeb2d59fe4be2dd75ea3c03bcb548be11688e80b128efb2a9fedc3c3080ee1`.

### PDF p416

The decisive physical wording is:

```text
臬測以景
針以氣
故不能符
```

and later:

```text
推七政之纏次
皆准於臬
以天而測天
至當不易之論也
```

Rendered JPEG SHA-256: `877d39d8d7cbe20adc50fe60a6aa84af1c1c5ba27d534037708dad07f267adab`.

## 4. Transcription control

CText chapter `551648` is retained only as navigation/semantic control. Machine hits include `地理之用莫切於羅經`, `立內外二盤`, `正針`, `縫針`, `臬測以景`, `針以氣`, `推七政之纏次`, `皆准於臬`. It receives zero independent physical-witness weight.

## 5. Philological and mechanical adjudication

The physical text explicitly distinguishes two reference mechanisms:

1. **臬 / shadow reference** — solar/astronomical observational geometry.
2. **針 / magnetic reading** — a qi-responsive needle orientation that can differ from the gnomon reference.
3. **正針 / 縫針 / inner-outer plates** — the text's technical response to that non-identity.
4. **七政 coordinates** — celestial-coordinate work is explicitly returned to the gnomon reference: `皆准於臬`.

Therefore Batch 12AM strengthens Batch 12AJ:

```text
羅經 != standalone clock
羅經 != true solar time
羅經 != local apparent solar runtime field
magnetic needle direction != gnomon/shadow astronomical reference
```

This is a same-period shushu semantic control, not Ziwei doctrinal authority.

## 6. Why the Fullbook problem remains open

The Fullbook says that under cloudy/rainy conditions one must use 羅經 to determine exact time. Batch 12AM does not supply the missing mechanical step:

```text
cloud/rain
-> no direct solar shadow
-> 羅經 orientation
-> ?? actual time-generation mechanism ??
-> birth-hour reading
```

Accordingly Batch 12AM does not prove Fullbook authorial inheritance, a standalone compass clock, true/apparent-solar runtime, backward projection of the Jiaqing clock stack, or an interpolation/error claim.

## 7. HPA-ZDATE-006 effect

```text
HPA-ZDATE-006=MISSING_FROM_PRODUCT
RUNTIME_TIME_STANDARD_BINDING=EARLY_MING_SHUSHU_GNOMON_NEEDLE_SEMANTIC_SEPARATION_CONFIRMED_FULLBOOK_INCLEMENT_TIME_REALIZATION_AND_RUNTIME_BINDING_STILL_OPEN
NEW_FULLBOOK_TEXTUAL_WITNESS=0
NEW_HAI_GLYPH_WITNESS=0
NEW_EARLY_MING_SHUSHU_SEMANTIC_CONTROL=1
CANDIDATE_SELECTION=NO
CANDIDATE_COLLAPSE=0
ALGORITHM_REOPEN=NO
```

Accounting remains 198 rows / 166 audited / 10 current MISSING_FROM_PRODUCT / 14 cumulative missing candidate families / provenance defects 10 confirmed and 10 repaired / algorithm defect-reopen-collapse all zero.

## 8. Next gate

Find a Fullbook-line or sufficiently early Ziwei witness that supplies its own complete cloudy/rainy operational chain from orientation/time reference to an actual birth-time reading. Do not infer that chain from 羅經 alone.

Machine evidence: `docs/research/ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-R1.json`.
