# Fusion Chart Historical Provenance Audit R1 — Batch 12KY

## NCPSsd 赵万里 1951 期刊详情对象：第一方书目元数据闭合

Status: **SOURCE-CLOSED DETAIL POST / HTTP200 JSON / 101-KEY DETAIL OBJECT / TITLE+AUTHOR+CARRIER+YEAR+ISSUE+PAGECOUNT+ISSN CLOSED / PDF URL METADATA NOT FOLLOWED / ZERO PRODUCT IMPACT**

12KX 已把详情数据请求严格闭合为：

```json
{"lngid":"1002462903","type":"中文期刊文章","pageType":1}
```

12KY 只执行这一个匿名只读 `POST /articleinfoHandler/getjournalarticletable`。返回 HTTP 200、`application/json`、2426 bytes，顶层 `code=200`、`result=true`，详情对象共有 101 个字段。

第一方详情对象直接给出：

```text
lngid      = 1002462903
titlec     = 永樂大典展覽的意義——一九五一年八月北京圖書舘舉辦
showwriter = 趙萬里
mediac     = 文物
mediae     = Cultural Relics
years      = 1951
num        = 9
pagecount  = 13
clazz      = K87
gch        = 97337X
issn       = 0511-4772
```

这比 12KT 的搜索结果更强：当前 NCPSsd 第一方详情对象确认该记录的题名、作者、载体、年份、期号、页数和 ISSN。这里的载体仍按来源原样记录为 `文物`，**不得静默改写成“文物参考资料”**；此前的 carrier-label tension 继续保留，除非后续出现明确 crosswalk。

详情对象还发出 `qkEncryptedUrl`，以及：

```text
pdfurl = http://www.nssd.org/articles/article_down.aspx?id=1002462903
pdfsize = 334977
```

12KY **没有跟随**这些值。脚本已证明阅读/下载存在登录/签名边界，因此“返回 pdfurl 元数据”不等于“匿名全文已经开放”。

KY 的字段选择曾按 `beginPage/endPage` 检索，而实际对象 key 为 lower-case `beginpage/endpage`；因此页码范围尚未在本批落盘。这是下一门 12KZ 的唯一必要补充之一。

控制证据：workflow `.github/workflows/probe-batch-12ky-ncpssd-zhao-journal-detail-data.yml`; exact head `baca4c413b44ad4dfda2041b3ea3a1847d7f5d8e`; run/job/artifact `36868341358 / 110389410761 / 11166270400`; artifact digest `sha256:3ce20951eee1ba6acec548fe854c0a2873d72fcfc76e66ab2005ff5e98bdbb67`。

下一门 12KZ：只重放同一个已经闭合的详情 POST，补取现有对象中的 `beginpage/endpage/pagenum/publishdate/source/remarkc/keywordc` 等字段；任何 URL 字段只作为字符串记录，不执行网络跟随。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 无新增边。

Research record: `docs/research/ZIWEI-NCPSSD-ZHAO-JOURNAL-DETAIL-DATA-R1.json`.
