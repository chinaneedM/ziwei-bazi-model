# Fusion Chart Historical Provenance Audit R1 — Batch 12KQ

## NCPSsd 缺省 ajaxKeys 语义：getUrlParam 返回 null

Status: **ajaxKeys ABSENT -> null / NO POST / ZERO PRODUCT IMPACT**

exact hot-link URL omits ajaxKeys; first-party getUrlParam missing case is null。

核心裁决：

```text
batch_id = BATCH-12-ZIWEI-NCPSSD-GETURLPARAM-ABSENT-SEMANTICS-KQ
matrix = 198 / 166 / 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```


The exact source-emitted positive-control URL omits `ajaxKeys`; the first-party `getUrlParam` implementation returns `null` when a parameter is absent.







控制证据：workflow `.github/workflows/probe-batch-12kq-ncpssd-geturlparam-absent-semantics.yml`; exact head `3352579841e5d44776b51e1656c7562b00f097a7`; run/job/artifact `36864304640 / 110375880379 / 11162678885`; artifact digest `sha256:37b28911de18718e261aa6746f342f3f3da9c1c8f94e9a84607fe10cd3459a2a`。

下一门：Inspect the exact source-emitted jQuery version to determine how null object values are serialized into application/x-www-form-urlencoded data. Do not send the result request yet.

Transmission Graph 不变；确定性排盘核心继续 CLOSED。

Research record: `docs/research/ZIWEI-NCPSSD-GETURLPARAM-ABSENT-SEMANTICS-R1.json`.
