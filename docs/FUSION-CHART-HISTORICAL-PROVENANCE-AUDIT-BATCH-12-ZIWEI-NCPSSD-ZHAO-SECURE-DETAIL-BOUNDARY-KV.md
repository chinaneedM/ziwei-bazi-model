# Fusion Chart Historical Provenance Audit R1 — Batch 12KV

## NCPSsd 赵万里 secure detail 匿名边界

Status: **DETAIL HTTP200 SHELL / LOGIN BOUNDARY / NO READ-DOWNLOAD / ZERO PRODUCT IMPACT**

HTTP200 generic shell / target tokens absent / login markers present / articleinfo.js emitted。

核心裁决：

```text
batch_id = BATCH-12-ZIWEI-NCPSSD-ZHAO-SECURE-DETAIL-BOUNDARY-KV
matrix = 198 / 166 / 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```







The exact source-derived secure-detail GET returns HTTP 200 / 149,306 bytes but no Zhao/title/1951/文物 tokens. Login markers are present and the shell directly emits `/js/web/Literature/articleinfo.js`. No read/download action occurs.


控制证据：workflow `.github/workflows/probe-batch-12kv-ncpssd-zhao-secure-detail-boundary.yml`; exact head `ed1d8e675fbe9a90d6190bf9c9b4c0c7bc059695`; run/job/artifact `36865703472 / 110380530783 / 11164055802`; artifact digest `sha256:8571770c43485d1aeda155922a69dfa3dcd3d1928dc079ac5356c93ee13b895f`。

下一门：Retrieve only the source-emitted /js/web/Literature/articleinfo.js and recover its detail-data contract. Do not execute discovered detail-data, read, download, collect or user endpoints in the same batch.

Transmission Graph 不变；确定性排盘核心继续 CLOSED。

Research record: `docs/research/ZIWEI-NCPSSD-ZHAO-SECURE-DETAIL-BOUNDARY-R1.json`.
