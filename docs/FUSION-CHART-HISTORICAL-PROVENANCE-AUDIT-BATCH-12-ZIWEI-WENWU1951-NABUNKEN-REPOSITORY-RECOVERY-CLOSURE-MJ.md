# Fusion Chart Historical Provenance Audit R1 — Batch 12MJ

## 奈文研公开仓储核查与当前匿名原刊恢复分支收束

Status: **PUBLIC REPOSITORY POSITIVE-CONTROLLED / FIVE MODERN ITEMS EXCLUDED / ORIGINAL PAGES NOT RECOVERED / RECOVERY BRANCH PAUSED_ACCESS_UNRESOLVED**

本批按 12MI 下一门执行，先去重 12HH/HI/IS/IT/JB 已闭合的日本原刊馆藏、影印本、数字提供者和复制制度。奈文研 `SB00333452 / TS00027259 / Document10024273` 已是精确单期实体 item，本批未再次查询 OPAC，也不把馆藏身份重复计票。

### 新公开路线及结果

第一方仓储 `https://repository.nabunken.go.jp/dspace/` 返回 HTTP 200，公开表单直接发出 GET `/dspace/simple-search`，参数 `query`、`submit`。其帮助页支持大写 OR；索引可覆盖元数据，全文则取决于是否启用。仓储与实体馆藏不是同一集合。

| 检索 | 实际结果 | 审读范围 |
| --- | --- | --- |
| 奈良文化財研究所年報，正控制 | 1183 条，首屏 10 条 | 证明公开表单可正常返回检索结果 |
| 文物参攷資料 / 文物参考資料 / 文物参考资料，OR | 5 条，全部逐项查看公开元数据 | 2004、2005、2011、2006、2020 年现代研究材料；无目标原刊对象 |
| 简繁文章题名，OR | 页面明确无对应记录 | 仅此索引与查询面的零命中 |

五个 source-emitted handle 是 `11177/1863`、`11177/731`、`11177/7539`、`11177/7719`、`11177/7827`。分别为参考文献、十二支像、唐代腰带、铜镜、朝阳北塔材料。各自页面虽发出 PDF 链接，均属于现代材料；只记录链接，没有下载或假称核读全文。不能把刊名关键词命中当成 1951 期刊扫描。

第一方图书资料室利用页另行成功读取。馆际/付费复制制度维持 12JB 边界；没有提交预约、联系、ILL 或复制请求。尤其公共图书馆等非费用相抵参加馆的路线有“日本国内仅该所持有时受理”的条件，不能据此保证现有多馆持有的目标可受理。

### 收束裁决

没有恢复《文物参考资料》1951 vol.2 no.9 pp.221–233。当前匿名原刊恢复分支记为 `PAUSED_ACCESS_UNRESOLVED_PENDING_MATERIALLY_NEW_ROUTE`，不再重复既有目录、挑战或配额表面。此状态只描述当前已查路径，不宣称全世界不存在扫描或原文。

重新开启条件：新的第一方精确期号/页对象、实质不同的公开访问机制，或另行获授权的机构恢复。直接 1951 pp.221–233、2011《赵万里文集》第一卷 p.197、上海《文汇报》1951-08-18 继续 `NOT_REVIEWED`；丁惠康六种中余下四题、原刊/汇编逐字关系和目标 acquisition edge 继续未决。

`EVIDENCE_VOTE_INCREMENT=0`；`TRANSMISSION_IMPACT=NONE`；排盘保持 CLOSED。计数维持 198 / 166 / 10、来源缺陷 17/17 已修复、算法缺陷/重开/候选折叠 0。

### 下一项实质审计

12MK 回到尚未完成的 `HPA-ZIWEI-013`：核查身宫干支展示是否严格为已发布 `body_address` 与 `address_attributes.stem` 的身份联接，分别追溯已审计 `HPA-ZIWEI-002`、`HPA-ZIWEI-004`，运行现有回归并审查缺失/非唯一身份的回退。不能把展示字段再包装成一种独立古法。

研究记录：`docs/research/ZIWEI-WENWU1951-NABUNKEN-REPOSITORY-RECOVERY-CLOSURE-R1.json`；原始公开 HTML、采集时间、请求 URL、字节摘要及结果清单：`docs/research/evidence/batch-12mj/`。此次是本地 WORK 网络采集，不是 GitHub runner 网络探测。
