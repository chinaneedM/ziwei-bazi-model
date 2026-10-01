# Fusion Chart Historical Provenance Audit R1 — Batch 12LU

## 全国报刊索引：用户手册节点与文件候选闭合

Status: **USER-MANUAL NODE HTTP 200 / OLD+NEW MANUAL LABELS OBSERVED / FIVE HREF-SRC CANDIDATES / LABEL↔FILE BINDING NOT YET CLOSED / NO DOWNLOAD / NO QUERY / ZERO PRODUCT IMPACT**

控制 run `36892505113` / job `110471322678` / artifact `11176554703` 在 exact head `2ca2d750e47f99ad59812de19cff4c5b9009a056` 上，只使用 12LS 第一方帮助树已经给出的节点 `161 用户手册下载`，按活动 `zTreeOnClick` 契约执行 `POST /portal/footCategory/findNews` + form payload `id=161`。

响应 HTTP 200 `application/json;charset=UTF-8`，6491 bytes，SHA-256 `29d7bae0aacb4a06d9c8fcce5aefd2ada352469cb2e1d5a2469c130823a78815`。正文标题为“用户手册下载”；content 长 1546、SHA-256 `2906c292cb3b417cab8149aa0bc87ece4994adbb2ac745eb0df52866a4336408`；去 HTML 后正文 82 字符。

可见正文直接命名两份对象：`平台用户手册（老平台）.doc` 与 `平台用户手册（新平台）.docx`，并说明它们“详细介绍了《全国报刊索引》网站中不同数据库的检索方式”。但正文仍没有直接出现普通/高级/专业检索、题名/作者/刊名/分类号等具体字段语义。

当前抽取到 5 个 source-emitted href/src：四个 `uploadFile` 对象加一个 UEditor 文件类型图标。由于 12LU 有意只做扁平 href/src inventory，尚未证明哪一个 uploadFile 对应老平台 `.doc`、哪一个对应新平台 `.docx`；因此本门禁止下载、禁止按 URL 顺序猜文件身份。

下一门 12LV 只重取同一节点并静态解析 HTML：逐个记录 `<a>` 的锚文本、href、内部 `<img src>` 及 uploadFile 周边上下文，同时记录 JSON 顶层 `linkUrl/linkItemId`。不跟随任何链接。只有绑定闭合后才能进入具体手册对象。

控制证据：workflow `.github/workflows/probe-batch-12lu-cnbksy-user-manual-node-contract.yml`; run/job/artifact `36892505113 / 110471322678 / 11176554703`; artifact digest `sha256:a0f6fa95c777e2aa149a6971a7ae5f7b7f8322cdda6fb3476296b1ea331ab97c`。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-USER-MANUAL-NODE-CONTRACT-R1.json`.
