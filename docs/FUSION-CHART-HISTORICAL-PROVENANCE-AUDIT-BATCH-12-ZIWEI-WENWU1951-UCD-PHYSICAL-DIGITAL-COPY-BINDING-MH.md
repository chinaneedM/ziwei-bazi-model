# Fusion Chart Historical Provenance Audit R1 — Batch 12MH

## 《文物参考资料》UC Davis 实物与数字副本身份

Status: **ANONYMOUS CATALOGUE WORKING / 12 PHYSICAL ITEMS BOUND TO 12 HATHITRUST HTIDS / AGGREGATE YEAR UNRESOLVED / ZERO ORIGINAL-TEXT VOTES**

12MG 暴露的 MARC 035 `sdr-ucd.990022440100403126` 本批已接回 UC Davis 第一方目录。先读取官方 UC Library Search 使用说明及 Ex Libris Primo VE 公开接口说明，再使用文档支持的 PNX 标识查询。UC Davis 说明无需登录即可检索目录；这不等于无需授权即可阅读所有电子正文。

### 记录与检索合同

目标 PNX、后继《文物 (1959)》正控制、原始 MARC 均返回 HTTP 200。目标为 `alma990022440100403126`、OCLC `18030125`、题名“文物参考資料”。联合目录 MARC 001 为 `9912383409706531`，996 保留 UCD 本地控制号，两层标识不得混用。

网页 GET 仅返回动态客户端壳。公开 source-emitted 客户端 bundle 进一步给出 `getPhysicalService`、`titleServices` 与 `holdings` 的真实路径和参数构造。后两者路径名称含 `/priv/`，但本次无登录、无 Authorization header、无 guest JWT 的匿名读取成功；并非猜测私有 Alma API。

初始 titleServices 响应 `items=[] / no-items=0`，同时给出号段过滤器。这是尚未展开明细，不能作为馆藏缺失。按客户端 `calculateRequestParams / getLocationsItems` 合同作一次只读 holdings POST 后，返回 12 个实体项目，`partial=false / current-start-pos=13`。该 POST 是馆藏查询，不是借阅、预约、复制或联系馆员的提交。

### 副本身份已闭合

Shields Library / General Collection / `DS715 .W44`，holding `22237179290003126`，总馆藏声明 `no.1-27,33-35,37-39,41-100(1950-1958)`。12 个实际 itembarcode 全部等于 12 个 HathiTrust UCD htid 的 `uc1.` 后缀，且 itemdescription 与 MARC 974 号段全部精确一致。

| 合订号段 | UCD item ID | 实物条码 | HathiTrust htid |
| --- | --- | --- | --- |
| no.13–18 | 23237179140003126 | 31175002281353 | uc1.31175002281353 |
| no.19–24 | 23237179130003126 | 31175002281361 | uc1.31175002281361 |

完整 12 项对应保存在研究 JSON。这加强的是原始馆藏与数字副本的可复核对应，不是新增 12 个独立原文见证，也不重复给同一副本计票。

### 年代与读页仍未决

实际响应年份过滤器仅 `Other..`，实体明细只有号段，没有逐册出版年。期刊总跨度 1950–1958、MARC 974 的 y=1958、条码对应、Loanable / Item in place 均不能替代“1951 卷二第九期”的直接编号桥接，也不能授权全文阅读。未取得任何原刊图像。

展开响应 serviceinfo 只有 Report a Problem，未提交该表单；这仅是该响应范围，不证明全局没有其他阅读或复制服务。未重试 HathiTrust 403 阅读器，未登录、借阅、预约或发出复制请求。

原始联合目录 MARC 776 另给 Online version OCLC `647437409`。这是下一步可用的数字副本标识线索，当前不宣称已经取得可读正文。

### 裁决与下一门

12MH 闭合 UCD 实物/数字副本身份；合订号段逐年对应和目标 1951 vol.2 no.9 pp.221–233 仍未决。2011《赵万里文集》p.197、上海《文汇报》1951-08-18 也仍未核读。历史文本谱系不变，`EVIDENCE_VOTE_INCREMENT=0`。

12MI 优先寻找直接的机构或物理编号/年代桥接，并以新验证的 MARC 776 OCLC `647437409` 探索文档支持的数字记录路线。不重复无年份的 12 册清单，不用算术消除未决状态。

矩阵 198 / 166 / 10、来源缺陷 17/17 已修复、算法缺陷/重开/候选折叠均为 0，排盘保持 CLOSED。

原始响应与只读请求保存于 `docs/research/evidence/batch-12mh/`，按 URL、方法、字节数及 SHA-256 绑定。客户端完整 bundle 和说明页不复制入仓库，只保存检索摘要、摘要值、真实路径和函数定位指纹。

Research record: `docs/research/ZIWEI-WENWU1951-UCD-PHYSICAL-DIGITAL-COPY-BINDING-R1.json`.
