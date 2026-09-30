# Fusion Chart Historical Provenance Audit R1 — Batch 12JF

## 《文物参考资料》1951年第9期 `wwck195109.pdf` 商业 manifest source-emitted 路由边界

Status: **51GUSHU HTTP200 / EXACT FILENAME+9.73MB MANIFEST CLOSED / 2 TOTAL ANCHORS / ZERO PDF-DOWNLOAD-SAMPLE-ATTACHMENT LINKS / XY980 CONNECTION REFUSED UNRESOLVED / PDF BYTES NOT RECOVERED / DIRECT PP.221–233 NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. 目标

12IT 已经关闭当前 IA / Open Library / Wikimedia 的公开目录检索面，但 `wwck195109.pdf` 仍只停留在“文件名 + 9.73 MB”定位层。12JF 不重复开放仓储搜索，而是直接检查现有商业 manifest 页面是否**自己发出**可匿名、合法继续追踪的 PDF、下载、样张、附件或网盘对象。

目标仍为：

- 《文物参考资料》1951年第9期；
- `wwck195109.pdf`；
- 赵万里《永乐大典展览的意义——一九五一年八月北京图书馆举办》；
- pp.221–233。

### 2. 可复现探针

控制性探针：

- workflow: `.github/workflows/probe-batch-12jf-wenwu-manifest-source-emitted-routes.yml`
- exact head: `60c25fd12848eef3bd1757b1dbc2961e78a322a3`
- run: `36774331720`
- artifact: `11125625596`
- artifact digest: `sha256:2f2fcfb3976b2198ac36bf86cff46bd7c434e947191d4e6d5ac5b2409a405dd3`

早先 run `36774050887` 因 runner 未安装 `requests` 而失败；run `36774221096` 因探针脚本漏定义 `get()` 形成空探测。二者均明确排除，不进入历史证据链。控制性版本增加了“没有任何 HTTP 状态即失败”的断言，防止“CI 绿但证据空”的假阳性。

### 3. 51古书网 manifest

当前公开页 `https://www.51gushu.com/um006465s.html`：

- HTTP 200；
- response 48,390 bytes；
- SHA-256 `959db6931f9f51cce7f1349abd08829a4cfa261144d2076c4292f6ed5d9e82c0`；
- 可见文本直接包含 `wwck195109.pdf`；
- 同一 manifest 直接显示 `9.73 MB`；
- 整页总锚点仅 2；
- candidate source-emitted link = 0；
- direct PDF candidate = 0；
- 未发现下载、样张、附件、网盘等候选链接。

因此 12IK 的“文件名/体量 locator”得到机器级再确认，但**没有升级为公开数字对象**。

### 4. xy980 发现线索

公开搜索索引还给出 `https://xy980.com/e/action/ShowInfo.php?classid=1&id=157` 这一发现线索。控制性 GitHub runner 对该正常公开 URL 得到：

`URLError: <urlopen error [Errno 111] Connection refused>`

所以当前只能记作：

`UNRESOLVED_DISCOVERY_LEAD_ONLY`

不能说它已经直接复核了同一 manifest，更不能把它计为第二个独立数字对象 witness。Connection refused 也不是目标不存在的负证据。

### 5. 证据防火墙

本批次明确禁止以下跳跃：

- 文件名 + 体量相同 ≠ 已取得 PDF；
- 商业目录“原刊扫描”描述 ≠ 已验证扫描 provenance；
- 某一 manifest 不发下载链接 ≠ 全网不存在开放对象；
- 搜索索引摘要 ≠ 直接页面审读；
- 连接拒绝 ≠ 负证据；
- 1951 issue manifest ≠ 2011《赵万里文集》第1卷 p.197 直接页；
- 在取得 provenance-bound bytes 前，不生成 SHA-256、页数、原始扫描来源或正文结论。

### 6. 项目影响

不改排盘产品，不改 runtime rule，不重开算法，不合并候选，不改 transmission graph。

计数维持：

- Matrix 198；
- audited 166；
- MISSING_FROM_PRODUCT 10；
- provenance defects 17/17 repaired；
- chart algorithm defects 0；
- reopen 0；
- candidate collapse 0。

### 7. 下一门

最高优先级仍是**合法直接恢复 2011《赵万里文集》第1卷 p.197**。并行继续：

1. 找到 1951 第9期 pp.221–233 的机构开放对象或 provenance-bound 等价扫描；
2. 继续 1997《北京图书馆馆史资料汇编（二）》pp.446–449 直接页恢复；
3. 只有当 51古书网开始 source-emit 新对象/链接时才重查该页；
4. xy980 仅在正常公开路由恢复可达时再审，不从搜索索引推断独立对象。

Research record: `docs/research/ZIWEI-WENWU-1951-WWCK195109-COMMERCIAL-MANIFEST-SOURCE-EMITTED-ROUTE-BOUNDARY-R1.json`.
