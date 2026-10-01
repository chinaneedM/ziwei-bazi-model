# Fusion Chart Historical Provenance Audit R1 — Batch 12KP

## NCPSsd articlelist 初始化合同：pageSize/order/search/searchname/ajaxKeys

Status: **INIT VALUES CLOSED / NO DYNAMIC API EXECUTION / ZERO PRODUCT IMPACT**

source-emitted articlelist.js closes runtime initialization before API execution。

核心裁决：

```text
batch_id = BATCH-12-ZIWEI-NCPSSD-ARTICLELIST-INIT-REQUEST-CONTRACT-KP
matrix = 198 / 166 / 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```

`articlelist.js` initializes `nums=10` and `order=synUpdateType|DESC,date|DESC,ik_subject|DESC,id|DESC`; `search/searchname` are URL-derived Base64 values and `ajaxKeys` is optional. No result endpoint is executed in this batch.








控制证据：workflow `.github/workflows/probe-batch-12kp-ncpssd-articlelist-init-request-contract.yml`; exact head `aeec65334fa635dc1e6cb9e898cd03edf2537c81`; run/job/artifact `36864017249 / 110374917367 / 11162003453`; artifact digest `sha256:219fa16aadebe60ae42a1f5a92004b7433377c848ec877b935fb492f2d0b5cb2`。

下一门：Prove getUrlParam behavior for an absent ajaxKeys on the exact positive-control URL. Do not execute /searchHandler/search in the same batch.

Transmission Graph 不变；确定性排盘核心继续 CLOSED。

Research record: `docs/research/ZIWEI-NCPSSD-ARTICLELIST-INIT-REQUEST-CONTRACT-R1.json`.
