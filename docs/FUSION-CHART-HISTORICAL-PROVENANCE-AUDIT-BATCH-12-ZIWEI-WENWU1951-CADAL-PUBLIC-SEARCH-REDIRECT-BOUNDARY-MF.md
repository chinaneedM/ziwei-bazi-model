# Fusion Chart Historical Provenance Audit R1 — Batch 12MF

## 1951《文物参考资料》：CADAL 公开检索重定向边界

Status: **PUBLIC FORM SOURCE-CLOSED / SAME-SESSION REDIRECT RECONFIRMED / NO TARGET OBJECT / NO DIRECT ORIGINAL PAGE / NO ABSENCE CLAIM / ZERO PRODUCT IMPACT**

本批闭环远端已经完成的三次 CADAL 探测。目标仍是赵万里《永乐大典展览的意义——一九五一年八月北京图书馆举办》，1951 年《文物参考资料》vol.2 no.9 pp.221–233；不是把现代引用升级成原刊核读。

| 探测 | Run / job / artifact | 结果 |
| --- | --- | --- |
| 公开首页合同 | 37175585343 / 111357402786 / 11292709922 | 首页 HTTP 200，322,516 bytes，公开表单 POST `/cadalinfo/search` |
| 首次目标查询 | 37175671876 / 111357662181 / 11293356523 | 三个查询均 HTTP 302 → `/index/home`，空响应体 |
| 同会话校准 | 37175777604 / 111357960349 / 11293252198 | 首页和表单重新确认后，在同一匿名 session 中三个查询仍全部 302 → `/index/home` |

公开表单字段为 `searchContent=<query>`、`searchType=sw`、`oneOrSecond=first`。三个查询分别是“文物参考资料”“永樂大典展覽的意義”“永乐大典展览的意义”。首次 POST 未先访问首页，故不足以排除初始化影响；第三次校准补上首页 GET 和同会话 cookie 接续，结果仍相同。只记录 cookie 名称，不保存或展示 cookie 值。

控制性同会话 artifact ZIP 的 SHA-256 为 `b67ff21326676916eac800607163a4bf80be1dd809693ff5c9cc3bd0c0ba725a`，已下载独立校验；成员 JSON SHA-256 为 `a7f6c8e018996b8d90c90ba723a696df52b0152407646ef7916d2930884fa8c6`，且与 job 日志中的输出对象一致。三次 exact HEAD/tree 和 artifact digest 均绑定在研究 JSON。

### 裁决

该结果是当前 runner 下的公开检索重定向边界。没有检索结果页、目标馆藏对象、阅读器或原刊页面，因此不能解释为“检索为零”，不能证明目标不存在，也不能仅凭重定向断言需要账号或机构 IP。重定向原因保持未决。

CADAL 当前 POST 分支停止，等待实质性的新第一方访问机制，不再重复同一请求或更换关键词。没有登录、认证绕过、私有接口猜测、读页请求或付费动作。

`DIRECT_1951_ORIGINAL_PAGES=NOT_REVIEWED`；2011《赵万里文集》第一卷 p.197 与上海《文汇报》1951-08-18 也仍未核读。`EVIDENCE_VOTE_INCREMENT=0`，`TRANSMISSION_IMPACT=NONE_ACCESS_BOUNDARY_ONLY`。

下一门 12MG：寻找实质性的新第一方期刊对象/可工作的公开数字目录路线，先与既有 12IT、12IN 记录去重。HathiTrust 仍是访问未决，只有恢复正常公开入口或得到新 source-emitted 对象标识才继续。复制申请、付费或认证服务动作仍遵守已有明确授权门槛。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0；确定性排盘保持 CLOSED。

Research record: `docs/research/ZIWEI-WENWU1951-CADAL-PUBLIC-SEARCH-REDIRECT-BOUNDARY-R1.json`.
