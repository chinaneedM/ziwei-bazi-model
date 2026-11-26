# 15DS｜台湾紫微期刊传播书目与民国报刊假阳性（临时检查点）

2026-11-26。启动HEAD `99649534b5c512bd1735154634be5b68182feea0`、tree `7e222cd993ca62ca7ac1116ca593c22b3e8682b5`；[精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45796768963)通过，分页复核285/285 Actions成功，六绑定吻合，五P0保留。

## 民国证据筛查与误命中排除

- [国图联合目录 rarecatx0428879](https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=1&item=1b36e75d6cb348bcafa51089508d41ccfDI3ODUxNA2.T5_fvtPg0BL_gp0oecUpf3kBMYmGj_Zu9aAWwhejGlk_&page=3538&sourceWhereString=&whereString=IChOVUxMSUYoQ3JlYXRlcl9OYW1lLCAnICcpIGlzIE5VTEwgYW5kIE5VTExJRihEb2N1bWVudF9Xcml0ZXIsICcgJykgaXMgTlVMTCBhbmQgTlVMTElGKEpvdXJuYWxfV3JpdGVyLCAnICcpIGlzIE5VTEwgKSA1.cHNKVlDaZLqmac_B_QboEZhR4vv4gJ8MEx7vCx6fK8U_) L34–48：1923–1926上海影印《紫微斗数》三卷，册1114，中国国家图书馆藏，丛书字段《正统道藏》。既有13ZI及紫微历史纲要已经明确记录，非新增来源，也不是民国职业实务。
- [《文化新聞》1940年第105期数字PDF](https://upload.wikimedia.org/wikipedia/commons/0/01/NLC404-00J010053-103975_%E6%96%87%E5%8C%96%E6%96%B0%E8%81%9E_1940%E5%B9%B4%E7%AC%AC%E4%B8%80%E7%99%BE%E9%9B%B6%E4%BA%94%E6%9C%9F.pdf) NLC404-00J010053-103975：搜索提取文本L120、125称“子平推命法”“紫微活盤的圖說”。直接目验零基PDF p2，1040px宽渲染；实际右侧段标题为“（二）幾個活報劇的圖…”及“（三）書店，出版社及其…”，中间大标题不是“子平推命法”。明确否定这两个提取命中为目标术数文章标题；未逐字遍历全期，不推论该期绝无术数内容。不登记为术数正证，无原始字节哈希。
- [民国文献大全](https://cadal.hytung.com.cn/)服务页明确仅CADAL成员馆开放，报纸及部分期刊需机构购买；不使用该付费/机构限制渠道，不作馆藏内容否定。

## 三条独立定年台湾期刊目录候选

数字典藏联合目录所列来源均为国家图书馆台湾期刊论文索引系统。以下直接读取L27、39–54，标题、作者、期刊、卷期、页次、日期均可定位；三条原始资料链接均返回403，未获取原刊正文或图页。

| 目录标识 | 作者、文章题名 | 刊期及页次 |
|---|---|---|
| [A07050233](https://catalog.digitalarchives.tw/item/00/51/f0/d6.html) | 黃露惠〈慧心齋主談紫微斗數真義〉 | 《拾穗》2=464，民78.12（1989-12），76–77页 |
| [A06044192](https://catalog.digitalarchives.tw/item/00/4c/9a/07.html) | 幻業居士〈從紫微斗數看一位紅顏的遭遇〉 | 《力與美》3，民79.07（1990-07），104–109页 |
| [A05045529](https://catalog.digitalarchives.tw/item/00/4b/88/38.html) | 王文靜〈龍游淺水，虎落平陽：青創楷模林正倫的紫微斗數傳奇〉 | 《商業周刊》384，1995-04-03至04-09，26–27页 |

原始索引地址均为 https://tpl.ncl.edu.tw/NclService/JournalContentDetail?SysId= 加各自标识。联合目录为索引衍生记录，不是期刊原页；标题显示公众访谈、个案叙述、商业媒体人物报道三个传播主题，但不据标题推定内容、从业身份、预测应验或规则、师承。与15DR慧心齋主1986书籍目录为不同题名/载体；既有13ZI不重复。根及五个相关分片的8词局部查重无命中，不是全库结论。

## 下一步

TW-OPEN-0037 P1 OPEN：领取绑定236分片manifest的全库字面查询结果，结合文章标题/索引号/载体/日期作语义裁决；若准入仅限期刊索引著录，不重复登记同原始索引与聚合目录；原刊仅合法免费免账号路线。TW-OPEN-0035仍OPEN，无同期民国紫微独立职业实务新证据。当前1296来源/236片、图474/375、Matrix222/222、37开放风险含五P0、确定性核心CLOSED。

## 15DS 正式有界裁决（2026-11-26，追加）

精确旧HEAD `b0fa28700c6c8942a1c50c8cf0205e8af707b237`，[连续性CI 45801532773](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45801532773)，job `139845704330`，62项遗漏测试与7项R2测试通过。验证程序blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。查询结果以下为实际日志JSON，作为保留期限之外的可复核记录：

```json
{
  "query_id": "15DS-taiwan-ziwei-periodical-index-dedup-r2-20261126",
  "checkpoint_id": "TW-CHECKPOINT-15DS-PROVISIONAL-20261126",
  "request_blob_sha": "7f6a79e685162acf1618bf7571db6776d193589b",
  "registry_manifest_blob_sha": "07fd93e42570681f89e68703a5a54a9c69312594",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 237,
  "records": 1296,
  "matching_files": 0,
  "per_term_matching_files": {
    "4950072": 0,
    "5020167": 0,
    "5370070": 0,
    "A07050233": 0,
    "A06044192": 0,
    "A05045529": 0,
    "慧心齋主談紫微斗數真義": 0,
    "慧心斋主谈紫微斗数真义": 0,
    "從紫微斗數看一位紅顏的遭遇": 0,
    "从紫微斗数看一位红颜的遭遇": 0,
    "青創楷模林正倫": 0,
    "青创楷模林正伦": 0,
    "00/51/f0/d6.html": 0,
    "00/4c/9a/07.html": 0,
    "00/4b/88/38.html": 0,
    "NLC404-00J010053-103975": 0,
    "rarecatx0428879": 0,
    "幻業居士": 0,
    "幻业居士": 0
  },
  "hits": [],
  "truncated": false
}
```

目录三页本轮再次核阅题名/作者/刊期/页码。全库字面零命中不等于语义无重复；既有13ZI的1923–26《道藏》影印锚点即使编号零命中仍不新增。15DR的1986慧心齋主两种图书与1989访谈式期刊题名为不同载体和书目对象。三条索引ID、作者、刊物、日期、页码互异；聚合目录与其NCL原始索引同源，不双重计数。另两个1980–90年代期刊题名不证所叙事实或任何直接传承。没有原刊，不确定正文、术式、师承、职业身份、传播规模或实际读者。

准入3条 `BIBLIOGRAPHIC_METADATA_ONLY` 来源，[新分片](./TIANWEN-15DS-TAIWAN-ZIWEI-PERIODICAL-INDEX-SOURCE-SHARD-R1.json)；不增图节点/边，不把1940假阳性入库。TW-OPEN-0037保留OPEN并追加证据范围修订，TW-OPEN-0035仍OPEN。来源1299=647+652／237片、图474/375、Matrix222/222、37开放风险含五P0，核心CLOSED。下一步继续独立可定年民国紫微实务、港台地域传播及合法免费原刊，非重复查询已登记索引。
