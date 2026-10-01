# Fusion Chart Historical Provenance Audit R1 — Batch 12JM

## 上海大学《文汇报》1951年5–8月合订本馆藏路线

Status: **SHU FIRST-PARTY HOLDING CLOSED / SHANGHAI WENHUI 1951(5-8) CLOSED / TARGET DATE INSIDE COVERAGE / SHANGHAI-HONG-KONG EDITIONS SEPARATED / SPECIFIC AUG-18 ISSUE NOT REVIEWED / NO ARTICLE TEXT / ZERO PRODUCT IMPACT**

### 1. 目标

12JJ 已有上海社科院 1951 整年《文汇报》馆藏路线，12JK 保留 1951-08-18 刊载说为二手未核原页线索。12JM 寻找一个独立机构、且时间范围更贴近目标日期的实体报纸路线。

### 2. 上海大学第一方馆藏页

第一方对象为 `https://lib.shu.edu.cn/gybengua/bggk/lhtsg/bz_hdb_gzml.htm`。控制探针取得 HTTP 200、164,150 bytes、SHA-256 `a3a9b77e4eb0ab5b53d0c35ea7c9fc0de9bd6401eabf585a13da52c0f8734198`。

### 3. 上海版目标行

第一方 HTML 表格直接给出：`7 | 文汇报 | 1951(5-8);... | 新校区 | 嘉定校区 | 6--10`。目标日 1951-08-18 落在该月份范围内，但月份覆盖不等于已经看到 8 月 18 日那一期或目标文章。

### 4. 香港版同页控制

同一页另列 `53 | 文汇报(香港版) | 1951(1-4,8-12);... | 嘉定校区 | 13--15`。因此第一方页面本身已经区分上海《文汇报》与《文汇报(香港版)》，禁止合并。

### 5. 控制性探针

- workflow: `.github/workflows/probe-batch-12jm-shu-wenhui-1951-bound-volume-holding.yml`
- exact head: `993fe194ae6f2da63b4fab9563a350a6ef52e318`
- run: `36831993406`
- job: `110270494878`
- artifact: `11148225440`
- digest: `sha256:b01fba8966e7163116586c44581b6b270b56da8f3085aa6563b59de4bc7e1e80`

### 6. 证据防火墙

`month range includes date != specific issue survives/reviewed`; `physical holding != direct page review`; `newspaper title != article title`; `Shanghai Wenhui != Hong Kong Wenhui`; `holding route != proof of secondary chronology claim`.

### 7. 当前裁决

- SHU first-party holding route = CLOSED
- Shanghai Wenhui 1951(5-8) = CLOSED_AT_PHYSICAL_HOLDING_LEVEL
- Shanghai/Hong-Kong disambiguation = CLOSED_ON_SAME_FIRST_PARTY_PAGE
- Specific 1951-08-18 issue/page = NOT_REVIEWED
- Target Zhao article = NOT_REVIEWED
- Direct Wenwu pp.221-233 = NOT_REVIEWED
- Direct 2011 Wenji p.197 = NOT_REVIEWED
- FIRST_PUBLICATION_STATUS = UNRESOLVED

### 8. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；chart algorithm defects 0；algorithm reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改；`TRANSMISSION_IMPACT=NONE`。

### 9. 下一门

上海大学路线作为独立实体定位点；继续优先寻找公开页级对象。若未来需要馆方复制/调阅，仍必须按明确授权边界处理。

Research record: `docs/research/ZIWEI-WENHUIBAO-1951-0818-SHU-BOUND-VOLUME-HOLDING-ROUTE-R1.json`.
