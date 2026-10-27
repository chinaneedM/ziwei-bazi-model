# Fusion Chart Historical Provenance Audit R1 — Batch 12KW

## NCPSsd articleinfo.js：中文期刊详情数据合同

Status: **DETAIL-DATA CONTRACT RECOVERED / ENDPOINT NOT EXECUTED / ZERO PRODUCT IMPACT**

getjournalarticletable contract recovered; read/download remain login/signature gated。

核心裁决：

```text
batch_id = BATCH-12-ZIWEI-NCPSSD-ARTICLEINFO-SCRIPT-CONTRACT-KW
matrix = 198 / 166 / 10
provenance defects = 17 / 17 repaired
chart algorithm defects = 0
algorithm reopen = 0
candidate collapse = 0
```








The source-emitted `articleinfo.js` exposes `/articleinfoHandler/getjournalarticletable`. For Chinese journal articles its client code sends JSON `{lngid:id,type:typename,pageType:pageType}`; read/download routines require login/signature and remain outside the current anonymous research boundary.

控制证据：workflow `.github/workflows/probe-batch-12kw-ncpssd-articleinfo-script-contract.yml`; exact head `eaf47da8b7c5bf524b9647a3287d71aaff93c61f`; run/job/artifact `36865867041 / 110381080380 / 11164580641`; artifact digest `sha256:df67075add6d133c6b40cd9214a82b58521bc8d34d717a085885946b981ed0f4`。

下一门：Extract only the exact secure shell's server-emitted hidden values for ftl_urlId, ftl_urlType, ftl_urlTypename, ftl_urlPagetype and related controls. Apply only local Base64 decoding if the values satisfy the same client condition.

Transmission Graph 不变；确定性排盘核心继续 CLOSED。

Research record: `docs/research/ZIWEI-NCPSSD-ARTICLEINFO-SCRIPT-CONTRACT-R1.json`.
