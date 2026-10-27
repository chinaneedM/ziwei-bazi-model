# Fusion Chart Historical Provenance Audit R1 — Batch 12JR

## 上海图书馆 / 全国报刊索引 2020–2026 开放数据清单范围与 API 文档谱系

Status: **ANNUAL FIRST-PARTY LISTING CHRONOLOGY CLOSED / MODERN NEWSPAPER DB LISTED 2020–2022 / NOT LISTED 2023–CURRENT / OMISSION != NONEXISTENCE / 2024–2026 API PDF BYTE-IDENTICAL / CURRENT 1951 API SCOPE UNRESOLVED / NO KEY / NO TARGET QUERY / ZERO PRODUCT IMPACT**

### 1. 目标

12JP 闭合当前 APIKey 鉴权；12JQ 闭合 2020 第一方公开说明书+样例 ZIP。12JR 进一步分开“年度开放数据列项”与“API 文档继续存在”两个不同事实，检查当前 competitionSearch 是否可被推定为仍覆盖 1951 报纸。

### 2. 年度第一方清单

修正字符集后的 controlling probe 直接抓取 2020–2025 年页面与当前 2026 页面。中国近代报纸数字文献全库在 2020、2021、2022 明确列出；在 2023、2024、2025 和当前 2026 页面不再列出。

该 omission 只描述年度开放数据页面的列项变化；不得扩写为数据库已经不存在、馆内不可访问或历史内容已经删除。

### 3. API 文档对象谱系

2024 API PDF、2025 页面 source-emitted 的 API PDF 与当前 2026 API PDF 均为 332,913 bytes，SHA-256 均为 7fc1d1d42bf30b639a03fee1a999d201d5c42f0a5272d8130fc03ea1b1877648；其中 2025 页面发出的 URL 路径仍包含 /2024/。

因此 API_DOCUMENT_PERSISTENCE != DATASET_SCOPE_CONTINUITY，YEAR_OR_PATH_LABEL != PROOF_OF_DOCUMENT_REVISION。

### 4. 探针质量控制

第一次 run 36840111958 虽为 workflow success，但 requests.text 的字符集回退导致中文页面被误解码。该 run 明确 SUPERSEDED，不计研究证据。

修正后的 controlling probe：exact head 90ee45f228681412ecb7d7827209b90c79f2a4e1；run 36840258132；job 110297437835；artifact 11150672206；artifact digest sha256:f37730cb3c19bc1ca8e692a3b988ae585b03c13cf13985aacc65d916970936ea。

### 5. 裁决

年度清单谱系在已审 2020–2026 页面范围内 CLOSED。现代报纸库不再连续列入当前开放数据清单，但 post-2022 database nonexistence = NOT_PROVED；current competitionSearch 1951 newspaper scope = UNRESOLVED；12JP 的 APIKey requirement 继续控制；本批未提交目标查询，未审读 1951 原页。

### 6. 项目影响

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0。无 runtime、产品或 transmission graph 修改。

### 7. 下一门

不再根据 API 文档长期复用来猜当前数据范围。合法 APIKey 仍是任何目标查询的必要条件，但未来即使获授权查询，也应先把结果解释为 API 当前收录/检索范围证据，再与直接原报页证据分层。

最高直接文本门保持：上海《文汇报》1951-08-18；《文物参考资料》1951年第9期 pp.221–233；2011《赵万里文集》第1卷 p.197。

Research record: docs/research/ZIWEI-CNBKSY-2020-2026-OPEN-DATA-LISTING-SCOPE-CHRONOLOGY-R1.json.
