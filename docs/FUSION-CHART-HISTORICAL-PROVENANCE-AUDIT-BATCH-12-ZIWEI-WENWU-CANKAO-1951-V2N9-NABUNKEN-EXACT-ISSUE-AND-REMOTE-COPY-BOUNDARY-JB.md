# Fusion Chart Historical Provenance Audit R1 — Batch 12JB

## 奈良文化財研究所《文物参攷資料》1951 Vol.2 no.9：第一方精确单期 item 与远程复制制度边界

Status: **NABUNKEN FIRST-PARTY EXACT ISSUE ITEM CLOSED / VOL.2 NO.9 / LOCAL BIB SB00333452 / HOLD TS00027259 / DOCUMENT ID 10024273 / REQUEST 202.505||3||1951-9C / PUBLIC DIRECT PP.221–233 NOT RECOVERED / REMOTE COPY REQUIRES LIBRARY INTERMEDIARY FOR INDIVIDUALS / FEES APPLY / NO REQUEST SENT / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

### 1. Why this batch exists

Batch 12HH 已经把赵万里 1951 原刊定位到《文物参考资料》第9期 pp.221–233，并通过大阪公立大学第一方 OPAC 与若干 CiNii union-holding 范围闭合了实体馆藏路线。12IS 又闭合了 NDL 纸本 bundle 与当前数字提供者边界。

12JB 不重复“有馆藏”这一结论，而是继续沿 CiNii `NCID AA11467834` 当前页面自己发出的奈良文化財研究所 OPAC 路线，把目标推进到**馆方第一方的单期 item 身份**，并单独审计馆方当前远程复制制度。

### 2. Reproducible anonymous probe

Probe workflow:

`.github/workflows/probe-batch-12jb-nabunken-wenwu-1951-v2n9.yml`

Successful run:

- workflow run: `36752861983`
- exact probe head: `d6397eb2a68e0ca771fa8705d305fb2a5c63eb21`
- artifact: `11115411027`
- artifact name: `batch-12jb-nabunken-wenwu-1951-v2n9`
- artifact digest: `sha256:062324181d463477152c18c189152474d334ec842ac41ae09a0bf52304455884`

The runner follows the CiNii source-emitted Nabunken entry and closes all required exact-item markers with anonymous GET only.

### 3. Exact issue item

奈良文化財研究所第一方 OPAC 当前直接闭合：

- serial identity: `NCID AA11467834`
- local bibliography: `SB00333452`
- exact issue: `Vol.2, no.9`
- year: `1951`
- hold id: `TS00027259`
- Document ID: `10024273`
- request number: `202.505||3||1951-9C`

因此：

`NABUNKEN_ORIGINAL_1951_V2N9_EXACT_ISSUE_ITEM = CLOSED_FIRST_PARTY`

这比 union-catalog 的“馆藏范围包含第9期”更精确，但仍然只是实体 item / access routing 身份。

### 4. Direct-text boundary

当前公开 item 页面没有恢复赵万里 pp.221–233 的页图或正文数字对象。

```text
ORIGINAL_1951_PP221_233_DIRECTLY_REVIEWED=false
PUBLIC_PAGE_LEVEL_SURROGATE_RECOVERED=false
DIRECT_DING_SIX_WORDING_COLLATED=false
DIRECT_1951_VS_2011_TEXTUAL_IDENTITY=UNRESOLVED
```

精确单期 item 不等于文章正文；馆藏请求号也不等于收到复制件。

### 5. Current remote-copy policy

奈良文化財研究所图書資料室当前官方利用案内明确给出远程复制制度：

- 个人用户的复制咨询不直接受理；
- 个人须通过所属机构图书馆或就近公共图书馆联系；
- 机构可走馆际路径，页面同时标示 NACSIS-ILL；
- 白黑复制：每页 60 日元 + 邮费；
- 彩色复制：每页 200 日元 + 邮费。

这只闭合**当前制度与动作边界**，不等于复制申请已被接受，更不等于目标页必然可复制。

本批次没有：

- 登录；
- 提交复制申请；
- 提交 ILL；
- 传输用户身份/联系资料；
- 支付费用；
- 绕过验证码、TLS 或访问控制。

任何实际馆际/付费复制动作继续要求用户显式授权。

### 6. Relation to prior evidence

- Batch 12HH：原刊期号与多条实体持有路线继续有效；
- Batch 12IS：NDL 当前数字提供者边界继续有效；
- Batch 12IG：2026 浙江图书馆官方 PDF 的 `[2]197` 引文桥继续有效；
- Batch 12JA：2011《赵万里文集》第1卷 p.197 仍未直接取得。

12JB 的新增量严格限定为：

`FIRST_PARTY_EXACT_ISSUE_ITEM + CURRENT_MEDIATED_REMOTE_COPY_POLICY`

不把 1951 原刊与 2011 汇编文字默认视为逐字相同。

### 7. Project consequence

- Matrix: 198 rows / 166 audited
- MISSING_FROM_PRODUCT: 10
- provenance metadata defects: 17 / 17 repaired
- chart algorithm defects: 0
- algorithm reopen: 0
- candidate collapse: 0
- transmission graph change: none
- runtime/product change: none

### 8. Highest next gate

1. 最高优先级仍是新的、合法公开/机构页级表面，直接取得 2011《赵万里文集》第1卷 p.197。
2. 对 1951 原刊继续优先寻找**无需外部申请**的公开页级 surrogate，以直接审阅 pp.221–233。
3. 如果公开路线继续关闭，奈文研的馆际/付费复制路线与 NDL 付费复制一样，只有在用户显式授权后才可发起。
4. 1997《北京图书馆馆史资料汇编（二）》pp.446–449 继续作为并行直页门。

Research record: `docs/research/ZIWEI-WENWU-CANKAO-1951-V2N9-NABUNKEN-EXACT-ISSUE-AND-REMOTE-COPY-BOUNDARY-R1.json`.
