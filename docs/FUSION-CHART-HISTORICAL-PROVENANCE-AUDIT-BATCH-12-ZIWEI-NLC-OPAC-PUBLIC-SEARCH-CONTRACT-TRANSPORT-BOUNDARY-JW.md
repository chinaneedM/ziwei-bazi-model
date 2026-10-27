# Fusion Chart Historical Provenance Audit R1 — Batch 12JW

## 国家图书馆 OPAC 公开搜索合同传输边界

Status: **SOURCE-EMITTED OPAC ROOT REACHED / ROOT HTTP 200 + 318 BYTES / SOURCE-EMITTED LOGIN-SESSION TIMEOUT / PUBLIC SEARCH CONTRACT NOT OBSERVED / NO FIND-PARAMETER GUESS / NO TARGET QUERY / OPAC NONHOLDING NOT PROVED / ZERO PRODUCT IMPACT**

### 1. 目标

12JV 已经证明当前 `read.nlc.cn/outRes` 外购资源索引对四个《文汇报》资源题名返回零结果，但该索引不是 OPAC。12JW 因此只沿国家图书馆首页自己发出的 OPAC 路由恢复公开目录检索合同，不自行构造 Aleph 查询参数。

### 2. 路由结果

控制探针直接检查两个 source-emitted 路由：

- `http://opac.nlc.cn/` → HTTP 200，318 bytes，SHA-256 `999e28e32e671494ad7a97c0a46446f192c8767264adca9d068ef0c3f4fe2a68`；
- `http://opac.nlc.cn/F/?func=file&file_name=login-session` → `ConnectTimeout`，35 秒内未取得页面。

OPAC 根页响应没有可用 form/input/link；login-session 又未取得，因此本批没有直接观察到公开 OPAC 搜索 action。

### 3. 防火墙

```text
ROOT_REACHED = true
LOGIN_SESSION_REACHED = false
PUBLIC_SEARCH_CONTRACT = NOT_OBSERVED
GUESSED_ALEPH_FIND_PARAMETERS = false
TARGET_QUERY_SUBMITTED = false
NLC_OPAC_NONHOLDING = NOT_PROVED
DIRECT_1951_PAGE = NOT_REVIEWED
```

传输超时不能改写成目录不可用，更不能改写成无馆藏。12JV 的 outRes 零结果继续与 OPAC 馆藏严格分层。

### 4. 控制证据

- run: `36845686120`
- job: `110315142748`
- artifact: `11153541592`
- artifact digest: `sha256:2933160c6211d76c6ea25264241975fffed1f75f719b81acd509144ea770d039`

未登录、未用读者账号、未注册、未提交表单、未猜私有端点、未提交题名/人物/日期查询。

### 5. 项目影响与下一门

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0。

下一步不重复失效的 login-session 请求，也不猜 `func=find-*`。优先复用已经由国家图书馆第一方页面或既有审计证明的公开目录替代入口（例如文津搜索），尝试闭合《文汇报60年报纸光盘》的 item-level 身份。直接《文汇报》1951-08-18、《文物参考资料》pp.221–233 与 2011《赵万里文集》第1卷 p.197 仍未直接审读。

Research record: `docs/research/ZIWEI-NLC-OPAC-PUBLIC-SEARCH-CONTRACT-TRANSPORT-BOUNDARY-R1.json`.
