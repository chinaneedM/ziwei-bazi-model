# Fusion Chart Historical Provenance Audit R1 — Batch 12IQ

## 冀淑英 2009 日本馆藏公共内容增强边界：京都 openBD / BOOK数据ASP 与立命馆 BOOK数据均无可用目次

Status: **CINII EXACT OBJECT CLOSED / SOURCE-EMITTED JAPAN OPAC ROUTES TESTED / KYOTO OPENBD NO CONTENT / KYOTO BOOKDATA ASP NO CONTENT / RITSUMEIKAN BOOKDATA ASP NO CONTENT / OPENBD ISBN RETURNS NULL / CHAPTER 9 PAGINATION UNRESOLVED / NO PHYSICAL-TOC ABSENCE CLAIM / ZERO PRODUCT CHANGE**

### 1. 目标与方法

Batch 12IP 已关闭国家图书馆出版社 Product 4660 当前 Booktext 小载荷路线。本批次转向 CiNii Books 对同一 2009 版的日本馆藏链，目标不是扩充“有几家图书馆收藏”，而是验证各馆匿名 OPAC 是否公开了可用于第九讲分页的 **目次／内容增强数据**。

目标书目：

- 《冀淑英古籍善本十五讲》
- 冀淑英著、李文洁插图
- 国家图书馆出版社，2009.7
- ISBN 9787501340637
- CiNii NCID BB00252412
- 241p

仅使用 CiNii source-emitted OpenURL、页面自身 source-emitted 内容增强调用以及 openBD 官方公开 ISBN API。没有猜私有 API 参数。

### 2. 匿名 OPAC 正控

最终控制 probe：GitHub Actions run `36719801871`。

#### 京都大学 KULINE

CiNii OpenURL 匿名访问成功并解析到 exact item：

- HTTP 200
- local bibid `BB03342067`
- exact ISBN `9787501340637`
- exact NCID `BB00252412`

页面源码直接发出：

```text
view_openbd('/opac/opac_openbdinfo/','9787501340637','BB03342067',200)
view_bookplus('/opac/opac_bookplusinfo/','9787501340637','BB03342067',200,'0')
```

为避免从函数名猜参数，本批次让 headless Chrome 直接从稳定 OpenURL 起步，在同一浏览器会话中执行页面自己的 JavaScript。最终 DOM 明确显示：

- openBD：`目次・あらすじの電子情報はありません。`
- BOOKデータASP：`あらすじ・目次の情報はありません。`

因此不是静态抓取漏掉异步数据。

#### 立命馆大学 RUNNERS

匿名 exact item HTTP 200，local bibid `TT41845508`。页面 source-emits：

```text
view_bookplus('/opac/opac_bookplusinfo/','9787501340637','TT41845508',120,'0')
```

同一 Chrome 正常执行后，BOOKデータASP 明确显示：

```text
あらすじ・目次の情報はありません。
```

#### 天理大学 / 东京大学

- 天理 exact OPAC：HTTP 200，书名、ISBN、NCID 可核；当前页面没有观察到 BOOK数据/目次增强块。
- 东京大学 source-emitted OpenURL 当前返回 HTTP 202、空 body。该现象只记录为当前 transport boundary，不能作内容不存在的证据。

### 3. openBD 官方 ISBN 正控

京都页面同时明确调用 openBD。独立使用 openBD 官方公开 ISBN GET：

```text
https://api.openbd.jp/v1/get?isbn=9787501340637
```

返回：

- HTTP 200
- `application/json; charset=UTF-8`
- 6 bytes
- SHA-256 `1d8fc6ceb1f94c6326d6d5483d258fcb2e179e9869325b245d105c2219bf69fd`
- JSON：单一 null record

因此 openBD 当前没有该 ISBN 的可用公开书目/内容对象。这与京都渲染后的“无电子目次/あらすじ”一致，但仍只是 **当前 openBD 路线** 的结论。

### 4. 分页裁决

本批次没有获得新页码：

- Chapter 9 exact page range：`UNRESOLVED`
- Chapter 9 direct text：`NOT_REVIEWED`
- Chapter 10/11 exact pagination：`UNRESOLVED`
- 六点既有分页锚点继续禁止线性、比例或邻近插值

尤其禁止把以下命题偷换：

```text
京都/立命馆当前内容增强无数据
→ 物理书没有目录
```

前者成立，后者不成立。

### 5. 安全与证据防火墙

- 不登录
- 不使用 My Library
- 不发复制/参考咨询请求
- 不付费
- 不绕验证码、权限或 TLS
- 不猜私有 API 参数
- 页面 JavaScript 由公开浏览器会话正常执行
- 不保存完整 OPAC HTML 或渲染 DOM

日外 BOOK数据ASP 是 OPAC 内容增强服务；本批次只裁决当前两个馆的渲染结果，不外推为该商业数据库全局没有此书记录。

### 6. 项目影响

- Matrix：198 行
- audited：166 行
- MISSING_FROM_PRODUCT：10
- provenance metadata defects：17 / 17 repaired
- chart algorithm defects：0
- algorithm reopen：0
- candidate collapse：0
- transmission graph：`NONE`
- runtime / product change：无

### 7. 下一门

1. 不再重复京都/立命馆当前 BOOK数据ASP 与京都/openBD 路线，除非页面内容发生变化。
2. 继续寻找真正的带页码目录、第九讲直接页/正文，或第 10 / 11 讲精确分页。
3. 并行继续 2011《赵万里文集》第1卷 p.197。
4. 并行继续 `wwck195109.pdf` 的权威/开放对象恢复。
5. 若公共路线持续关闭，东京/NDL 的 reference/copy 请求仍需用户明确授权后才能执行。

Research record: `docs/research/ZIWEI-JI-SHUYING-2009-JAPAN-OPAC-OPENBD-BOOKDATA-PUBLIC-CONTENT-BOUNDARY-R1.json`.
