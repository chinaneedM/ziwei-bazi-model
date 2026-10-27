# Fusion Chart Historical Provenance Audit R1 — Batch 12IS

## NDL《文物参考资料》1951 后半年：纸本合订对象已闭合，当前 NDL Digital provider 路线为零

Status: **12HI PHYSICAL IDENTITY CARRIED FORWARD / NDL OPENSEARCH DIGITAL PROVIDER POSITIVE-CONTROLLED / TARGET SERIAL NDL-DL=0 / TARGET SERIAL NDL-DL-OPEN=0 / TARGET ARTICLE NDL-DL=0 / EXACT PAPER BOUND VOLUME 2(7)-2(12) 1951 / CALL Z8-AC150 / NO DL.NDL.GO.JP OR PID LINK / ISSUE 9 SCAN NOT RECOVERED / PP.221-233 NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. 本批次只升级数字访问边界，不重复计算纸本馆藏

Batch 12HI 已经闭合 NDL 的纸本合订对象《文物参考资料 2(7)-2(12) 1951》，并确认目标第9期包含于该范围。本批次不把同一对象重复计作新馆藏。

12IS 的问题只有一个：当前 NDL Search / NDL Digital provider 是否已经把该刊、该文章或该合订对象公开绑定到 NDL Digital 页面对象。

### 2. NDL Digital provider 正控

NDL OpenSearch 的 `dpid=ndl-dl` 先用《吾輩は猫である》做正控：

- HTTP 200
- `totalResults = 165`
- 首批结果直接出现 `https://dl.ndl.go.jp/pid/...`

因此 `dpid=ndl-dl` 过滤器在本次探测时是正常工作的，目标零结果不能归因于“接口整体失效”。

### 3. 目标刊与目标文章的 provider 结果

在同一接口与同一访问条件下：

- 《文物参考資料》+ 1951 + `dpid=ndl-dl`：0
- 《文物参考资料》+ 1951 + `dpid=ndl-dl`：0
- 《文物参考資料》+ 1951 + `dpid=ndl-dl-open`：0
- 《永樂大典展覽的意義》+ `dpid=ndl-dl`：0
- 《永乐大典展览的意义》+ `dpid=ndl-dl`：0

取消 provider 限制后，目标刊 1951 查询返回 8 条，并重新出现 NDL 的后半年纸本 item：

`R100000002-Ia0000051292-i25241426`

这证明“全 provider 有目标纸本对象”和“当前 NDL Digital provider 没有对应结果”是可区分的两个状态。

### 4. 精确 item 元数据

NDL OpenSearch / OAI / item 页面共同闭合：

- 标题：《文物参考资料》
- 卷号：`2(7)-2(12) 1951`
- 出版者：文物出版社
- 出版年：1951
- 资料种别：杂志
- 资料形态：纸
- NDL call number：`Z8-AC150`
- NDL bibliographic ID：`a0000051292`
- item：`R100000002-Ia0000051292-i25241426`

官方刊行序列同时给出 1951 年为 2卷1期至2卷12期，因此第9期明确位于 `2(7)-2(12)` 合订范围内。这个包含关系不是页码插值，也不等于第9期拥有独立数字 object ID。

### 5. 数字对象裁决

精确 item 页当前：

- 没有 `dl.ndl.go.jp` 链接
- 没有 PID 链接
- NDL Digital provider 查询为零
- NDL Digital open provider 查询为零

所以当前只允许：

> NDL 官方纸本合订对象已闭合；当前测试的 NDL Digital provider 路线没有暴露目标数字对象。

不允许扩大为：

> 世界范围内没有数字化；NDL 永远没有数字化；第三方扫描不存在；`wwck195109.pdf` 不真实。

### 6. 仍未取得的高价值对象

以下状态全部保持：

- `wwck195109.pdf`：未取得字节
- 第9期独立扫描对象：未闭合
- 赵万里 1951 pp.221–233：`NOT_REVIEWED`
- 2011《赵万里文集》第1卷 p.197：`NOT_REVIEWED`

1951 引文中的宋刻《春秋左传注疏》继续禁止与 FID070 折叠；FID070 物理裁决仍为元刻元印十行本。

### 7. 项目影响

- Matrix：198
- audited：166
- MISSING_FROM_PRODUCT：10
- provenance metadata defects：17 / 17 repaired
- chart algorithm defects：0
- algorithm reopen：0
- candidate collapse：0
- transmission graph：`NONE`
- runtime / product change：无

### 8. 下一门

1. 不再重复当前 NDL `ndl-dl` / `ndl-dl-open` 同类查询，除非 NDL provider 状态变化或源码直接发出新 PID。
2. 把 `wwck195109.pdf` 的权威/开放对象发现移出已闭合的当前 NDL Digital 路线；一旦合法取得字节，先哈希、验刊期和分页。
3. 继续 2011《赵万里文集》第1卷 p.197 的合法公开直页/预览。
4. 继续冀淑英第九讲或第10/11讲新的直接页码证据。

Research record: `docs/research/ZIWEI-NDL-WENWU-CANKAO-1951-H2-DIGITAL-PROVIDER-BOUNDARY-R1.json`.
