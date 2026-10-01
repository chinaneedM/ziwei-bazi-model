# Fusion Chart Historical Provenance Audit R1 — Batch 12JN

## 上海大学 2025.10《文汇报》现行定位修订与数字倍增平台访问边界

Status: **CURRENT SHU LOCATOR A7-1 CLOSED / LEGACY 6--10 PRESERVED / COVERAGE UNCHANGED 1951(5-8) / DIGITAL PLATFORM MEDIATED ON-SITE / TARGET OBJECT NOT BOUND / NO REMOTE PAGE / ZERO PRODUCT IMPACT**

### 1. 目标

12JM 已关闭上海大学的独立实体馆藏路线，但使用的是旧目录中的 `6--10` 定位。12JN 前向核对 2025.10 现行目录，并检查同馆数字倍增平台是否公开绑定目标对象。

### 2. 现行目录

2025.10 更新版页面直接给出 `7 文汇报 A7-1 1951(5-8)... B L`，同时表头包含架号、收藏情况、装订馆、收藏馆。页面说明 B=新校区期刊室、W=延长校区期刊室、L=嘉定校区期刊室。

因此：现行架号 `A7-1`；覆盖仍为 `1951(5-8)`；旧 12JM 的 `6--10` 保留为 prior-directory locator，不静默覆盖历史记录。

### 3. 数字倍增平台

第一方平台页说明约有 30 万册数字资源，但使用流程为邮件预约、等待工作人员答复、再到校本部图书馆五楼电子阅览室指定位置使用。页面未出现目标《文汇报》1951 的对象标识，也没有公开远程页级查看契约。

### 4. 控制性探针

- workflow: `.github/workflows/probe-batch-12jn-shu-current-wenhui-locator-digital-access.yml`
- exact head: `ff349b405d07454bba82377df5d274a40f325ff7`
- run: `36833087275`
- job: `110273972471`
- artifact: `11147354008`
- digest: `sha256:56e180e465a397afe542a728e036480dfe023e07cfc6315f5ad31fd1f465f95d`

### 5. 证据防火墙

`current locator update != rewrite prior capture`; `physical locator != page review`; `generic digital platform != target object`; `mediated on-site access != public remote view`; `no public target binding != target absent from platform`; `no email/appointment action without explicit authorization`.

### 6. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0；`TRANSMISSION_IMPACT=NONE`。

### 7. 下一门

继续公开直接页级恢复；如确需邮件预约或到馆调阅，必须另行获得明确授权。

Research record: `docs/research/ZIWEI-WENHUIBAO-SHU-2025-CURRENT-LOCATOR-AND-DIGITAL-ACCESS-BOUNDARY-R1.json`.
