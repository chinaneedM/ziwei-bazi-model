# Fusion Chart Historical Provenance Audit R1 — Batch 12JV

## 国家图书馆 outRes《文汇报》资源题名匿名检索零结果边界

Status: **SOURCE-EMITTED PUBLIC GET USED / FOUR TITLE TERMS TESTED / ALL HTTP 200 / ALL pageTotal=0 / SEARCH TERM ECHO != HIT / OUTRES ZERO != OPAC NONHOLDING / NO PERSON OR DATE QUERY / DIRECT PAGE NOT REVIEWED / ZERO PRODUCT IMPACT**

### 1. 检索范围

严格复用 12JU 页面自身 `getOutResSearch()` 合同，仅查询四个资源题名：`文汇报60年报纸光盘`、`文汇报`、`文匯報`、`文汇报61年全文数据光盘`。

四个响应均 HTTP 200 且 `pageTotal=0`。HTML 中可见检索词是页面把 `searchName` 回显进脚本变量，并非资源命中；没有观察到对应结果 item/link。

### 2. 证据边界

该零结果只说明当前匿名 `read.nlc.cn/outRes` 外购资源索引没有返回上述四个题名。它不能证明 `opac.nlc.cn` 无馆藏、不能否定 2003 年受赠报道，也不能证明 1951-08-18 原报页不存在。

### 3. 控制记录

Run `36845037948` / job `110313030409` / artifact `11153465153` / digest `sha256:82a139a7312863b38bb7096d4bb87c94d0790d16155e3b9f0475b46af86d5f64`。未使用登录、读者账号、注册、验证码绕过或状态改变请求。

### 4. 下一门

停止重复 outRes 题名检索。下一步沿国图首页 source-emitted 的 `opac.nlc.cn/F/?func=file&file_name=login-session` 公开导航恢复 OPAC 搜索合同，再决定是否做 OPAC 题名查询。

Research record: `docs/research/ZIWEI-NLC-WENHUI-RESOURCE-TITLE-SEARCH-ZERO-RESULT-BOUNDARY-R1.json`.
