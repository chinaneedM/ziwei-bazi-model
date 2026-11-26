# 15EC｜台湾、香港1970年代命理出版候选检查点（未准入）

2026-11-26。基准HEAD 9647db06b7e1e5d9ed24f2ec433f024a7326ee89；六个R2绑定吻合，精确HEAD连续性CI [45825318143](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45825318143) 成功。读取时280项Actions中174成功、15运行、91排队，未见失败；不得声称全绿。依据15EB和史纲，仅补查不同题名/版次及独立期刊，非重复登记既有1971竹林、1975南北山人、1979孔日昌、慧心齋主或张开卷书目。

## 候选（全部待完整查重）

| 对象 | 可复核来源与字段 | 证据边界 |
|---|---|---|
| 《飛星紫微斗數, 紫微斗數考證合集》 | [Google Books 1_1IAAAAMAAJ](https://books.google.com/books/about/%E9%A3%9B%E6%98%9F%E7%B4%AB%E5%BE%AE%E6%96%97%E6%95%B8_%E7%B4%AB%E5%BE%AE%E6%96%97%E6%95%B8%E8%80%83%E8%AD%89%E5%90%88.html?id=1_1IAAAAMAAJ)：1975，387页，Original from University of Michigan，2007-09-12数字化 | 目录元数据，未见原书版权页，页面没有作者及出版者字段；原藏机构不证出版地或版次，不由后出商品补齐。 |
| 《紫微斗數考証》 | [WorldCat 32761793](https://search.worldcat.org/title/zi-wei-dou-shu-kao-zheng/oclc/32761793?ht=edition&referer=di)：梁湘潤著，台北市臺灣文源書局有限公司，民国68(1979)，3版 | 联合书目，页面未列可定位馆藏；不据三版倒推前两版年月，不将1975合集与1979单题书目合并，也不以题名认定飞星技法同一。 |
| 《卜筮星相》第2、3期 | [新亞圖書中心2011拍卖目录785](https://sunahbooks.blogspot.com/2011/07/701800.html)：韋千里主编，香港韋氏命苑，1975，16开二册 | 商业后出著录，无原刊图及具体月日；不得作为实际刊期、发行量、四柱内容或师承证明。与15AF香港袁树生《星相》及台湾《中华星相》分离。 |
| 《人的運氣》 | [三民转载2019复刻简介](https://www.sanmin.com.tw/product/index/007126903)：汪季高撰，称1965香港五行出版社初版及1954起报刊专栏 | 后出复刻方叙述，不是1965原刊记，其他零售同文不算独立证人；内容是否子平须核原页。 |
| 《生れ日の人間学 : 淵海子平・流運看命》 | [NDL 000001244131](https://ndlsearch.ndl.go.jp/books/R100000002-I000001244131)：設楽幸聖，けいせい，1975，254页，HR511-56，pid/12282559；[系列检索](https://ndlsearch.ndl.go.jp/search?cs=bib&from=0&q-title=%22%E7%94%9F%E3%82%8C%E6%97%A5%E3%81%AE%E4%BA%BA%E9%96%93%E5%AD%A6+%3A+%E6%B7%B5%E6%B5%B7%E5%AD%90%E5%B9%B3%E3%83%BB%E6%B5%81%E9%81%8B%E7%9C%8B%E5%91%BD%22&size=20)另列1976–77日本正統運命学研究会 | 日本四柱出版比较候选，非港台/南洋来源；个人送信限日本国内本注册用户，本轮不走账号路径；不据题名推导技术谱。 |

[NDL台湾期刊检索指南](https://ndlsearch.ndl.go.jp/rnavi/asia/post_146)列台湾国家图书馆期刊索引1970年起，以及馆藏1951–1970纸本索引；只提供后续查询路径，不作为原刊证据。南洋同期原件本轮未获，不推断不存在。

## 门禁与下一步

当前未作全库查重结论。通过R2.1既有CI请求覆盖题名、繁简/异文、馆目识别号及作者/出版者；收取精确checkpoint成功日志，处理匹配路径和语义后才决定准入。查重未完成，不新增source、graph node/edge、Matrix或算法结论。TW-OPEN-0046保持OPEN；五项P0原状态不变。不得将后出书目当成原刊记；不购买、不登录、不要求用户操作。

## 15EC正式准入追加：精确全库查询及版次辨析（2026-11-26）

[run 45826158887](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45826158887)，job 139930716204，exact HEAD `961bc39ccdc5e5b3dd8fe4a94b125d922da9b902`，62项R1及7项R2测试通过。R2程序blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。以下是完整旧manifest查询输出；新增后不可作为新manifest扫描。

```json
{
  "query_id": "15EC-taiwan-hk-1970s-print",
  "checkpoint_id": "TW-CHECKPOINT-15EC-PROVISIONAL-20261126",
  "request_blob_sha": "8e5863ae1918c414ca74ae0aefaee3de2de31641",
  "registry_manifest_blob_sha": "5ed110ad352f0d6c6dd9baa0bad3938eb6060f51",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 247,
  "records": 1333,
  "matching_files": 9,
  "per_term_matching_files": {
    "12282559": 0,
    "32761793": 0,
    "1_1IAAAAMAAJ": 0,
    "飛星紫微斗數": 3,
    "飞星紫微斗数": 1,
    "紫微斗數考證": 0,
    "紫微斗數考証": 0,
    "紫微斗數考证": 0,
    "紫微斗数考证": 0,
    "梁湘潤": 3,
    "梁湘润": 3,
    "臺灣文源書局": 0,
    "台灣文源": 0,
    "卜筮星相": 1,
    "韋氏命苑": 1,
    "韦氏命苑": 0,
    "人的運氣": 0,
    "人的运气": 0,
    "汪季高": 0,
    "五行出版社": 0,
    "000001244131": 0,
    "生れ日の人間学": 0,
    "設楽幸聖": 0,
    "设乐幸圣": 0
  },
  "hits": [
    {
      "path": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json",
      "blob_sha": "ea2ab50479450c39ce3fc7a00ea91cd713bf4a60",
      "terms": [
        "飛星紫微斗數",
        "飞星紫微斗数",
        "梁湘潤",
        "韋氏命苑"
      ]
    },
    {
      "path": "docs/research/TIANWEN-14E-FEIXING-ZIWEI-SOURCE-SHARD-R1.json",
      "blob_sha": "d30d9b042e3f111ffad02deb76565c6fbb18ab3f",
      "terms": [
        "飛星紫微斗數"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15W-YUANSHUSHAN-1934-SAMPLE-1947-SSID-SOURCE-SHARD-R1.json",
      "blob_sha": "e76408ec2ac079d2b027a699eebd66317977a2e9",
      "terms": [
        "卜筮星相"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15AD-HK-ZIWEI-TAIWAN-ZIPING-MODERN-TEACHING-NETWORKS-SOURCE-SHARD-R1.json",
      "blob_sha": "b2440edf822163ffd57d584e6abcf59a216ba6d4",
      "terms": [
        "梁湘潤"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15AE-TAIWAN-CHINESE-STAR-ASSOCIATION-PERIODICAL-SOURCE-SHARD-R1.json",
      "blob_sha": "a4d5354483b1bc66c2402b2e7bba44f63b031ff0",
      "terms": [
        "梁湘润"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15AF-HK-TAIWAN-XINGXIANG-PERIODICAL-CROSSCHECK-SOURCE-SHARD-R1.json",
      "blob_sha": "159989a07ad5fa75811ea35a1e98c82071558dba",
      "terms": [
        "梁湘润"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15AG-TAIWAN-XINGXIANG-PERIODICAL-PHOTO-AND-BOOK-EDITION-SOURCE-SHARD-R1.json",
      "blob_sha": "56fa8fad00f852b6cd826d010d2b4f4d5615e952",
      "terms": [
        "梁湘潤"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15AH-TAIWAN-1979-1980-LECTURE-AND-ENCYCLOPEDIA-SOURCE-SHARD-R1.json",
      "blob_sha": "281261477cc00560d48adf482d658bfbe0ba9765",
      "terms": [
        "梁湘润"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15DG-REPUBLICAN-ZIWEI-PRACTICE-WHITE-MONK-SOURCE-SHARD-R1.json",
      "blob_sha": "93006a36da0efa1f4725ba2d13989f84d9c718b6",
      "terms": [
        "飛星紫微斗數"
      ]
    }
  ],
  "truncated": false
}
```

九份命中语义审查：root清代十八飞星、2010《前定數》、1934/1936韋氏讲义及1935《千里命稿》非本次对象；14E民国《飛星紫微斗數原旨》及1972.10文源書局編輯部第三版（CiNii BA73216864，214页/19cm，东京中央馆400005730）为前置比较；15W袁樹珊1934《述卜筮星相學》缩印样书非韋氏刊物；15AD/AE/AF/AG/AH为梁氏后出自序、课程、年表及星相期刊/百科书系，袁樹生1977–79香港《星相》非1975《卜筮星相》；15DG白鈍僧1999武陵《飛星紫微斗數》为另版。未见本次五条对应记录，不声称无语义近似遗漏。

补证：[星僑1988合集商品页](https://ncc.com.tw/books/goods.php?id=9828)列陳錦芳、文源、ISBN9570458321、173页，转录梁湘潤1975乙卯春署名序及《考證》前言；[星易同ISBN](https://www.xinyi.hk/goods-9288.html?from=rss)标题陳錦芳但作者字段梁湘潤，标1988初版，与1975/387页馆目不宜合并。三张100px预览缩图无法核清文字/刊记。[露天卖家](https://www.ruten.com.tw/item/22627040095939/)搜索标题称1975.9《考證》初版，直接打开超时；[2010个人书目](https://classic-blog.udn.com/DejaVu/3899301?f_UA=pc)称1975梁氏考證与另项合订。仅为版本边界比较，未另增来源计数；不得倒证1975书或飞星流派起源。署序年不等于出版年。1975合集与1979 WorldCat重开失败，仅索引及先前所录字段可用，保留原页及作者/版次未决。

[2011新亞拍卖785](https://sunahbooks.blogspot.com/2011/07/701800.html)全文索引明确韋千里主編、香港韋氏命苑1975、第2/3期及两册，无原刊页。[三民2019复刻](https://www.sanmin.com.tw/product/index/007126903)简介列双桐馆主、1954–60年代星島晚報/天下半月刊及英文四柱（所称pp27–28），为后出出版方陈述。[NDL 000001244131](https://ndlsearch.ndl.go.jp/books/R100000002-I000001244131)复核1975东京、254p、authority 00073228，另青森/大阪/高知馆藏，非三个版本。南洋同期原件仍缺。

准入五条有界来源，见[分片](./TIANWEN-15EC-TAIWAN-HK-1970S-PRINT-SOURCE-SHARD-R1.json)。新增三个出版组节点、零传承边。总1338=647+691／247片，图484/375，Matrix222/222；TW-OPEN-0046 OPEN、46风险含五P0，核心CLOSED。
