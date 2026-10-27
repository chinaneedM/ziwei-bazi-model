# Fusion Chart Historical Provenance Audit R1 — Batch 12IN

## CNKI `WENW195109` 旧静态索引公开传输边界：正控失败，目标零命中不得作阴性证据

Status: **LEGACY-ID PATTERN DISCOVERY LEAD ONLY / KNOWN-POSITIVE CONTROL FAILED ON ALL TESTED SAFE PUBLIC ROUTES / NO TLS BYPASS / TARGET IDS UNRESOLVED / NO TARGET ENUMERATION AFTER CALIBRATION / ZERO NEGATIVE AUTHORITY / ZERO DIRECT TEXT / ZERO PRODUCT CHANGE**

### 1. Discovery control

维基文库讨论页为另一篇 1951《文物参考资料》文章记录 `CNKI WENW195106001`。这只证明旧编号格式是一个可追踪的二手 discovery lead，不证明第9期或赵万里目标文章的具体 CNKI 编号。

### 2. Probe 1

在 `ff48283f...` / run `36707671218` 中尝试 `WENW195109001–040` 的 `https://www.cnki.com.cn/Article/CJFDTotal-*.htm` 假设路线。40 次请求全部在读取内容之前因 TLS 证书主机名不匹配失败。`POSITIVES=[]` 因此没有阴性证据价值。

### 3. Calibrated probe 2

在 `8bc1aeb0...` / run `36707936856` 中先用已知 discovery control `WENW195106001` 校准四个不绕过 TLS 的公开变体：

- `https://www.cnki.com.cn/...` → curl 60 / HTTP 000 / certificate hostname mismatch；
- `https://cnki.com.cn/...` → curl 28 / 443 timeout；
- `http://www.cnki.com.cn/...` → HTTP 418 / empty body；
- `http://cnki.com.cn/...` → curl 28 / port 80 timeout。

没有一个变体通过正控，因此本轮按设计不枚举任何第9期目标候选。没有使用 `-k`、未禁用证书校验、未登录、未绕验证码、未访问付费/下载接口。

### 4. Adjudication

`WENW195109xxx` 目前只能视为从旧编号格式外推的假设候选族，不是 CNKI source-emitted 的目标标识。当前公开面只能关闭为 transport/access boundary：不能证明赵万里文章不存在于 CNKI，也不能证明某个候选编号为空。

1951 原刊 pp.221–233、2011 p.197、冀淑英第九讲仍均为 `NOT_REVIEWED`。FID070/宋刻对象身份防火墙、瞿氏确切批次/日期与 `3368→3288` 未决状态全部保持。

### 5. Highest next gate

停止重复当前失效的 CNKI 旧静态路线，除非出现新的 source-emitted 工作主机/URL 或可通过的正控。优先继续 `wwck195109.pdf` 的权威/开放对象恢复、2011 p.197 公开直接页，以及冀淑英第9讲/第10-11讲精确页码。

Research record: `docs/research/ZIWEI-CNKI-WENW195109-LEGACY-INDEX-TRANSPORT-BOUNDARY-R1.json`.
