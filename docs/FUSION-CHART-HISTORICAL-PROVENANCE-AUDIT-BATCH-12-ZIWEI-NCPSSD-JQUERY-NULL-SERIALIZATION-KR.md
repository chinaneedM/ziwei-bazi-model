# Fusion Chart Historical Provenance Audit R1 — Batch 12KR

## NCPSsd jQuery null 序列化：null → 空字符串

Status: **jQuery null -> empty string / NO NETWORK SEARCH / ZERO PRODUCT IMPACT**

source-emitted jQuery 1.11.1 $.param serializes null scalar as empty string。

核心裁决：

```text
batch_id = BATCH-12-ZIWEI-NCPSSD-JQUERY-NULL-SERIALIZATION-KR
matrix = 198 / 166 / 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```



The exact source-emitted jQuery 1.11.1 normalizer contains `null==b?"":b`, so the runtime `ajaxKeys=null` becomes the form field `ajaxKeys=`.






控制证据：workflow `.github/workflows/probe-batch-12kr-ncpssd-jquery-null-serialization.yml`; exact head `c1db8875c9ef8674a916d16522faf23ca3584e49`; run/job/artifact `36864657833 / 110377053487 / 11161979359`; artifact digest `sha256:cbef1cd07b28b11c16c24132f6822435e14fb35e045d2374c999385ed3c1e8c8`。

下一门：Execute only /searchHandler/search for the already source-emitted 红楼梦 positive control using the closed field order and serialization. Do not call log, facet, detail, read or download endpoints.

Transmission Graph 不变；确定性排盘核心继续 CLOSED。

Research record: `docs/research/ZIWEI-NCPSSD-JQUERY-NULL-SERIALIZATION-R1.json`.
