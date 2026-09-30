# Fusion Chart Historical Provenance Audit R1 — Batch 12IU

## 《赵万里文集》第1卷日本 OPAC 公共内容边界：馆藏身份可绑定，p.197 与目标正文仍未公开取得

Status: **KANSAI / KYOTO / NIJL EXACT VOLUME-1 BIBLIOGRAPHIC BINDING / KYOTO OPENBD + BOOKDATA REPORT NO CONTENTS-SUMMARY DATA / SAITAMA + TOHOKU CURRENT ACCESS BOUNDARY / DIRECT 2011 P.197 NOT REVIEWED / ZERO PRODUCT CHANGE**

### 1. 目标

Batch 12IR 已把《赵万里文集·第一卷》绑定到国家图书馆出版社 Product 5325 与 ISBN `9787501346653`，但 direct p.197 仍未取得。12IU 沿 CiNii Books 的 NCID `BB08679512` 所发出的日本机构 OPAC 路线继续查找公开目录、摘要、页码或正文入口。

目标仍是：

- 2011《赵万里文集》第1卷；
- printed p.197；
- 与瞿氏捐赠 / 《永乐大典》展览相关的目标引文链；
- 仅使用匿名公开馆藏/内容面，不发起 ILL、复印、账户或付费动作。

### 2. 控制探针

Probe commit: `6bf22b4a54ca2f828071ed461194ab1a3d02a1b7`

Workflow run: `36730261776`

Artifacts:

- static: `11105575170`, digest `sha256:ddcdf6d11bef808de2f228a6950865890df511e2ba296c9388efbdef86e29d13`
- rendered: `11105525251`, digest `sha256:87c0c39a7ec0630b0f07667169bbf9bc99b86ed5aefd9c5f16d5acd145b0fa95`

### 3. 三条可直接绑定的机构 OPAC

关西大学、京都大学 KULINE、国文学研究资料馆三条公开路线均在当前探针中直接返回：

- 目标书名《趙萬里文集》；
- NCID `BB08679512`；
- 第1卷卷次；
- ISBN `9787501346653`。

因此，这三条路线可以作为**机构馆藏/书目身份与卷次绑定**，但不能提升为 p.197 正文见证。

### 4. 公开内容面裁决

静态页面与 headless-rendered 页面均未出现：

- 独立的 `197` 页码文本；
- 丁惠康；
- 《東家雜記》/《东家杂记》；
- 《太平樂府》/《太平乐府》；
- 《永樂大典》/《永乐大典》；
- 六十二 / 六種 / 六种等目标词组。

关西大学渲染面明确显示“Contents and Summary”无电子信息。京都大学 KULINE 的 openBD 与 BOOKデータASP 内容块分别返回：

- `目次・あらすじの電子情報はありません。`
- `あらすじ・目次の情報はありません。`

这些都是**当前公开增强内容面为空**的直接证据，不是实体书中没有目录、没有 p.197 或没有目标文字的证明。

### 5. 两条访问边界

埼玉大学与东北大学静态请求当前返回 HTTP 403；headless 页面也未形成可用目标书目内容。故这两条仅记为当前 runner / anonymous-route access boundary，不赋予任何负面文本权重。

### 6. 项目裁决

Direct 2011 p.197 仍为 `NOT_REVIEWED`。本批次：

- 不新增规则候选；
- 不修改 Matrix 行数或 audited 数；
- 不新增 provenance defect；
- 不重开 deterministic chart algorithm；
- 不改变 transmission genealogy。

Matrix 仍为 198 / audited 166 / MISSING_FROM_PRODUCT 10 / provenance defects 17/17 repaired / chart algorithm defects 0 / reopen 0 / candidate collapse 0。

### 7. 下一门

停止重复当前已关闭的关西/京都/国文研“公开目录/摘要”内容面，除非页面状态或内容服务发生变化。继续寻找新的、合法的机构数字对象/页级预览/引用页来直接取得 2011 p.197；并继续 authoritative/open `wwck195109.pdf` 路线与冀淑英第九讲/第10–11讲直接页码证据。

Research record: `docs/research/ZIWEI-ZHAO-WANLI-WENJI-V1-JAPAN-OPAC-PUBLIC-CONTENT-BOUNDARY-R1.json`.
