# Fusion Chart Historical Provenance Audit R1 — Batch 12JO

## 文汇报官方电子报公开日期契约访问边界

Status: **OFFICIAL EPAPER HOST KNOWN / CONTROLLING RUNNER TIMEOUT / DATE CONTRACT UNCALIBRATED / TARGET DATE NOT SUBMITTED / ZERO PRODUCT IMPACT**

### 1. 目标

12JN 后继续寻找上海《文汇报》1951-08-18 直接页。文汇报当前官方电子报使用 `dzb.whb.cn`，现代公开页面按日期组织；12JO 的目的不是根据现代 URL 模式猜 1951 路径，而是先确认站点是否自己发出合法的日期选择契约。

### 2. 控制探针

- workflow: `.github/workflows/probe-batch-12jo-whb-epaper-public-date-contract.yml`
- exact head: `d4bb22afafade69cf6e5f21ca9db11448798d568`
- run: `36834874380`
- job: `110279768574`
- artifact: `11148592500`
- digest: `sha256:fdf0f44210a45e233995e7142734ac9e7d94c124d05c30dad1fdc83bd72b3783`

GitHub runner 对官方根入口和一个已知现代日期页均 ConnectTimeout，因此没有取得脚本、表单或 source-emitted 日期契约。

### 3. 裁决

```text
CONTROLLING_RUNNER_EPAPER_SURFACE = UNREACHED_TIMEOUT
SOURCE_EMITTED_DATE_CONTRACT = NOT_CALIBRATED
TARGET_1951_08_18_SUBMITTED = false
DIRECT_1951_08_18_PAGE = NOT_REVIEWED
```

公开搜索引擎能索引现代日期页，不等于控制 runner 已校准日期选择契约；现代路径模式也不授权直接拼接 1951 URL。

### 4. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0；`TRANSMISSION_IMPACT=NONE`。

### 5. 下一门

继续新的公开页级路线；只有当官方页面或 source-emitted 脚本直接给出日期契约时，才重新考虑电子报目标日期请求。

Research record: `docs/research/ZIWEI-WENHUI-OFFICIAL-EPAPER-PUBLIC-DATE-CONTRACT-BOUNDARY-R1.json`.
