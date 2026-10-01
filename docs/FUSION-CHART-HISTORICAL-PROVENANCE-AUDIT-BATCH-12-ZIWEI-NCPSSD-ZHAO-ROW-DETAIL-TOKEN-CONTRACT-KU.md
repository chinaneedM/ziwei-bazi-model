# Fusion Chart Historical Provenance Audit R1 — Batch 12KU

## NCPSsd 赵万里结果行 detail token 合同

Status: **encryptedUrl OBSERVED / DETAIL NOT EXECUTED / ZERO PRODUCT IMPACT**

encryptedUrl and source-emitted secure detail builder recovered; detail not followed。

核心裁决：

```text
batch_id = BATCH-12-ZIWEI-NCPSSD-ZHAO-ROW-DETAIL-TOKEN-CONTRACT-KU
matrix = 198 / 166 / 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```






The exact Zhao row contains a non-empty `encryptedUrl`; first-party `hrefinfo()` uses it to build `/Literature/secure/articleinfo?params=<encryptedUrl>&pageUrl=<encoded current URL>`. KU does not follow that detail route.



控制证据：workflow `.github/workflows/probe-batch-12ku-ncpssd-zhao-row-detail-token-contract.yml`; exact head `9a033ab8d87e15770f05101ec15db3e056a96560`; run/job/artifact `36865479469 / 110379805467 / 11163685518`; artifact digest `sha256:57c02c8a9af29115dd63cd51674ef85f91bcce91513512904450c0bb11c1ea79`。

下一门：Follow exactly the source-derived secure detail GET once, without automatic redirects. Inventory only returned HTML identity, target tokens and source-emitted scripts; no read/download action.

Transmission Graph 不变；确定性排盘核心继续 CLOSED。

Research record: `docs/research/ZIWEI-NCPSSD-ZHAO-ROW-DETAIL-TOKEN-CONTRACT-R1.json`.
