# Fusion Chart Historical Provenance Audit R1 — Batch 12MG

## 《文物参考资料》HathiTrust OCLC 数字卷册清单

Status: **DOCUMENTED IDENTIFIER API WORKING / DIGITAL SERIAL RECORD AND 39 ITEMS BOUND / EXACT 1951 NO.9 UNRESOLVED / READER HTTP 403 / ZERO ORIGINAL-TEXT VOTES**

12IT 测试过的目录导出 HTTP 403 保留为历史访问记录。本批寻找并使用不同的第一方机制：HathiTrust 当前官方 Bibliographic API 文档公开支持 OCLC 标识的 brief/full 查询。该接口是标识查询，不是关键词搜索。公开示例 OCLC 424023 返回正常 JSON，目标 OCLC 18030125 也返回 HTTP 200；网络执行发生于本地 WORK 环境，不宣称是 GitHub runner 探测。

### 已闭合的对象身份

目标返回 record `007245565`，OCLC `18030125`。完整 MARC 的 880 题名为“文物参考資料”，362 起讫为 1950 年第 1 期至 1958 年总 100 号。brief/full 的卷册数组完全一致，共 39 个不同 htid，均有来源机构和阅读器 URI。MARC 035 同时暴露 UCD、UCSD、UCLA 的原始记录控制号；本批不是给已知纸本馆藏重复计票。

| 卷册标记 | htid | 能支持的范围 |
| --- | --- | --- |
| yr.1951 no.1–2 | uc1.l0084846252 | 明确为 1951 第 1–2 期 |
| yr.1951 no.3–4 | uc1.l0084846211 | 明确为 1951 第 3–4 期 |
| no.13–18 | uc1.31175002281353 | 合订号段已绑定，年份和目标期对应未决 |
| no.19–24 | uc1.31175002281361 | 合订号段已绑定，年份和目标期对应未决 |

`no.19–24` 的 MARC 974 原样为机构 `UCD`、来源 `google`、号段 `no.19-24`、`y=1958`、rights `und`、basis `bib`、说明 `non-US bib date2 >= 1931`。不得把该年份字段直接当作单期出版年，也不得未经编号桥接就把号段映射成 1951 第 9 期。实际图像尚未取得，不能以算术推算替代期号核读。

### 阅读范围

API 的 39 项均有 `usRightsString=Limited (search-only)`，其中 rightsCode `ic` 26 项、`und` 13 项。该字符串是官方文档定义的美国用户描述，不等于全世界统一的权限裁决；`und` 也不等于可以任意下载。实际只访问一个 source-emitted 合订卷阅读器 URI，当前环境返回 HTTP 403，未获取正文或原刊影像，未登录或绕过权限。

Georgian National Science Library 的 MARC 前身项提供初始 OCLC 线索；该网页由检索工具读取，本地两次 GET 均 502，未保存其正文摘要。其主记录为后继《文物》，不能认定该馆有 1951 原刊。目标身份由 HathiTrust 实际响应的 OCLC、MARC 880 和出版跨度独立交叉确认。

### 裁决和下一门

本批确实恢复了一个以前未取得的数字期刊记录和 39 个数字对象标识，但尚未绑定目标 1951 vol.2 no.9 pp.221–233。明确 1951 卷册列表没有第 9 期，仅限这次单记录响应的枚举范围；不证明 HathiTrust 或其他平台全局缺失。

下一门 12MH 使用新暴露的 `sdr-ucd.990022440100403126` 原始记录控制号寻找 UC Davis 第一方目录/合订号段年代桥接及公开合法读页路线。先读取公开目录合同，不猜测私有 Alma API，不重复 403 阅读器，不用期刊总跨度冒充单期年代。

原刊页、2011《赵万里文集》p.197 和上海《文汇报》1951-08-18 仍未核读。`EVIDENCE_VOTE_INCREMENT=0`，历史文本传承边不变。矩阵 198 / 166 / 10、来源缺陷 17/17 已修复、算法缺陷/重开/候选折叠均为 0，排盘保持 CLOSED。

三个原始 API 元数据响应按原字节保存于 `docs/research/evidence/batch-12mg/`，研究 JSON 绑定各文件的 URL、HTTP status、字节数及 SHA-256，并记录官方说明/目录页面的响应摘要；后续无需重复网络查询即可复核核心元数据。

Research record: `docs/research/ZIWEI-WENWU1951-HATHITRUST-OCLC-DIGITAL-INVENTORY-R1.json`.
