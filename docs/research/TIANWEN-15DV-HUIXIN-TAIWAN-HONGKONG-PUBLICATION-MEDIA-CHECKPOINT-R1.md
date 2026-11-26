# 15DV｜慧心齋主早期出版及港台報刊傳播（臨時檢查點）

2026-11-26。恢复 HEAD `780c95c804d093d8428ea5d2a75f7fdb4c2a9040`，tree `d722b61c027a356f5e5aa11fbd80e9283e509927`。[15DU精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45808145920)通过；本轮复查最后一页Actions无异常，前次全量285项中284成功、一项运行。R2恢复沿用已核不可变blob。五P0不变。

## 排除重复
[1972 NDL Search](https://ndlsearch.ndl.go.jp/books/R100000001-I13111400033517) L9–23、48–58、120–147，张开卷《紫微斗數命理研究》，香港崑崙出版公司1972.1，12+140页，東京都立中央図書館4000057314，索书号1488-5004-72；NDL为聚合，非其自身藏本。[心一堂](https://publish.sunyata.hk/product/974.html?variant=zh-hant) L93–108称1949初版与1972底本。两者均已见现存紫微历史纲要，不重复登记；三种题名与物理版本关系未核原书，未证明师承。上轮将该馆目作为待新查候选的做法产生重复检索，本次纠正。

## 待查重来源（不计入来源统计）
- [Google Books DBAtPAAACAAJ](https://books.google.com/books?id=DBAtPAAACAAJ)：1982《紫微斗數看婚姻》，时報文化出版事業有限公司，211页，Edition 4为书目字段，未核实版权页，不等于确定1982首版。
- [Google Books gG25tgAACAAJ](https://books.google.com/books?id=gG25tgAACAAJ)：1985《如何推算命運：紫微斗數與四化星》，时報文化出版事業有限公司，258页。
- [Google Books cqxdAAAACAAJ](https://books.google.com/books?id=cqxdAAAACAAJ)：1992《紫微斗數入門》，博益出版集團有限公司，314页，ISBN 9621710367/9789621710369；出版地待版权页，不因出版社名称即证台湾流派传入香港。
- [Google Books nSMaAAAACAAJ](https://books.google.com/books?id=nSMaAAAACAAJ)：1994《紫微斗數導讀》，时報文化，199页，系列《紫微斗數全集》第1册。
- [Google Books xCzfAQAACAAJ](https://books.google.com/books?id=xCzfAQAACAAJ)：1994《紫微斗數看命宮》，时報文化出版企業有限公司，227页，同系列第2册。五项均只见书目元数据，无原页与馆藏实物绑定。
- [2021增订版零售试读](https://ftp.xinyi.hk/goods-8733.html) L433、437：受传第一人称文字称1980年在《台湾日报》以馥廬为笔名撰写紫微斗数，并称获12680服务标章。不能据转录认定字形、注册事实或同期报刊，原序与原报待核；以馥廬/馥庐作为搜索词，不建立姓名同一或师承边。
- [2021 Google Books S9oWEAAAQBAJ](https://books.google.com/books?id=S9oWEAAAQBAJ) 418页，2021.2.1，大塊文化；后出出版简介称1981出版、香港《东方日报》曾有长期专栏。[新北市立图书馆udn电子书简介](https://reading.udn.com/udnlib/tpc/B/178313) 及[大块文化新书资料](https://www.locuspublishing.com/book/detail/10748) 搜索摘要称1979《联合报》万象版首个专栏及跨区报刊传播；类似文案可能依赖共同出版社履历，不各算独立证词。另一出版社页10749打开超时，仅搜索摘要不作正文目验。1981零售所报ISBN9571301213及日期仍需书端核对，不当作原版事实。
- 未见民国独立同期实务新原件，不以检索未命中证明无载。

## NEXT
绑定查询覆盖当前根+240片全部1310来源，检索书目ID、题名、异体笔名与媒体定位；精确字面检索后仍作语义裁决。TW-OPEN-0020原有媒体传播缺口追加笔名与早期出版核查，不关闭任何事项。原书、原刊与标章只循合法免费免账号公开路线。无新史料登记、无图谱或规则变更。Matrix222/222、图474/375、39开放风险含五P0、核心CLOSED。


## 15DV 准入裁决（2026-11-26，追加）

精确HEAD `ad12eaf72254f6f7c4d4e2fc645471f7dadbc126`、[连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45810066300) job `139875281027` 成功；62项遗漏风险测试、7项R2测试通过。验证程序blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`，请求及manifest绑定如下。原始检索输出（字面非语义查重）：

```json
{
  "query_id": "15DV-huixin-publication-media-dedup-r2-20261126",
  "checkpoint_id": "TW-CHECKPOINT-15DV-PROVISIONAL-20261126",
  "request_blob_sha": "8ca5eae3a33154d2fe09ca945f42fab64997616d",
  "registry_manifest_blob_sha": "20644d274b35fa4afbf11ba72a2372b419b25322",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 241,
  "records": 1310,
  "matching_files": 1,
  "per_term_matching_files": {
    "12680": 0,
    "178313": 0,
    "慧心齋主": 1,
    "慧心斋主": 0,
    "馥廬": 0,
    "馥庐": 0,
    "DBAtPAAACAAJ": 0,
    "gG25tgAACAAJ": 0,
    "cqxdAAAACAAJ": 0,
    "nSMaAAAACAAJ": 0,
    "xCzfAQAACAAJ": 0,
    "S9oWEAAAQBAJ": 0,
    "9789621710369": 0,
    "9571301213": 0,
    "紫微斗數看婚姻": 0,
    "如何推算命運": 0,
    "紫微斗數導讀": 0,
    "紫微斗數看命宮": 0,
    "goods-8733.html": 0,
    "book/detail/10748": 0
  },
  "hits": [
    {
      "path": "docs/research/TIANWEN-15DS-TAIWAN-ZIWEI-PERIODICAL-INDEX-SOURCE-SHARD-R1.json",
      "blob_sha": "91140cc427e0c8fb789fc4b771467f8cb85847ea",
      "terms": [
        "慧心齋主"
      ]
    }
  ],
  "truncated": false
}
```

唯一命中15DS，1989《拾穗》黄露惠访谈式题名（A07050233），不是本批书籍或自序。额外复核15DR既有金庸文库目录中1986《紫微斗數看錢財》《紫微斗數趨吉避凶法》，也为不同文献对象；两部1986书籍不再次登记。五项Google Books书目按检索索引重新核对题名、作者、出版年及页数，其中三个简短ID链接当前直接打开失败，但以题名检索均返回准确对应的书目ID及字段。1982/1985/1992/1994各书版权页、印次、实体本与完整正文未核，1994《紫微斗數看命宮》副题据书目补为《現象說與溯因說》。1985记录另见零售所列1986/1995日期，仅保留印次待核，不作新源。两本1994书目零售分别报199/227页，作为辅助定位。参考：[1994导读](https://www.sanmin.com.tw/product/index/000088759)、[1994看命宫](https://www.sanmin.com.tw/product/index/001551076)、[1986零售日期](https://www.taaze.tw/products/11100210973.html)、[1995零售日期](https://www.eslite.com/product/1001110931408376)。

2021零售页L196–207、235–274、394–437复核到受传自序及出版简介，前者含笔名和标章自述，后者含1979/1981及香港专栏、后期改写的叙述。新北市立图书馆udn电子书页L25–37与后者高度同文，故不作为独立传播证词。大块10748当前打开跳首页，仅其搜索摘要定位，不能提升验证等级。2021 Google Books 418页与零售414页/附册字段有差异；无书端，不另作版次结论或重复计数。零售所载辛酉序、自序和2021营销文案必须分别辨析形成时间，不能把2021页面日期当作序文撰写日期，也不能把修订本内容倒推1980年代。两术分立及图谱无变更。

正式准入五条书目和一条受传自序/简介，共六个有限来源对象，见[分片](TIANWEN-15DV-HUIXIN-PUBLICATION-MEDIA-SOURCE-SHARD-R1.json)。不证1979/1980同期原刊、12680正式标章、跨地区确切专栏序列或独立师承。不宣称原书原报不存在。TW-OPEN-0020/0035/0037/0039保持OPEN。来源1316=647+669／241片，图474/375，Matrix222/222，39开放风险含五P0，核心CLOSED。NEXT：继续民国同期独立紫微实务与港台原始出版及报刊传播。
