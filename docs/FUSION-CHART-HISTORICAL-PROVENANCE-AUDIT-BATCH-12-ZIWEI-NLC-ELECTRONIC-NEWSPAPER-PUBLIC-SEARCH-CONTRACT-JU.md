# Fusion Chart Historical Provenance Audit R1 — Batch 12JU

## 国家图书馆电子资源页公开检索合同

Status: **FIRST-PARTY CLIENT-SIDE SEARCH CONTRACT CLOSED / ourReswords -> searchName / GET /outRes/outResList / FIXED type=全部 / NO QUERY SUBMITTED / OPAC SEPARATE / ZERO PRODUCT IMPACT**

### 1. 直接合同

控制探针只读取国图 `read.nlc.cn` 当前页面及页面自己引用的脚本。搜索按钮 `onclick=getOutResSearch()`；页面内联函数直接读取 `#ourReswords`，把它映射为 `searchName`，固定 `typeName="全部"`，随后用 GET 导航到 `/outRes/outResList?type=全部&searchName=<ourReswords>`。

分页函数则在同一路径使用 `type / searchName / pageNo / urlType`。这是页面自身发出的合同，不是猜测接口。

### 2. 边界

本批未提交任何搜索词、未登录、未调用读者账号、未 POST 表单。该合同属于 outRes 外购/电子资源列表，不等于 OPAC 馆藏目录合同。

### 3. 控制记录

Run `36844745344` / job `110312077411` / artifact `11152144796` / digest `sha256:1fca09b8ec9b3db9a877c3d053601f9b9b8936bb65aeeb55d2b50b1beba0275f`。页面对象 404,829 bytes / SHA-256 `b8991f6d96bb95e8fba6dff11866ece8b146ee097fa902d9afb25b0c7d7856cf`。

### 4. 项目影响

198 / 166 / 10；provenance defects 17/17；algorithm defects 0；reopen 0；candidate collapse 0；无 runtime/product/genealogy 变化。

Research record: `docs/research/ZIWEI-NLC-ELECTRONIC-NEWSPAPER-PUBLIC-SEARCH-CONTRACT-R1.json`.
