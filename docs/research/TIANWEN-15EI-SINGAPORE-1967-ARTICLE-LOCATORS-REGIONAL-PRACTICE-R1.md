# 15EI｜1967新加坡一鼎金专栏独立文章定位及15EJ区域实践候选

2026-11-26，承接15EH。精确HEAD `fc7920f42280fb8e06a80856e7cf6fce3dac7742`，连续性 [run 45839758264](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45839758264)，job 139978004284，62+7测试通过。查询程序 blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。六权威绑定与完整远端树一致，五P0全部保留。全库字面查询结果原样保全：

```json
{
  "query_id": "15EI-yidingjin-1967",
  "checkpoint_id": "TW-CHECKPOINT-15EH-ADMITTED-15EI-PROVISIONAL-20261126",
  "request_blob_sha": "7e38b1c80aa8ff7d52d2937601dd0d45b43b9df8",
  "registry_manifest_blob_sha": "6a23458ad44c54de0edc2e4f010f91155bf22b16",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 253,
  "records": 1360,
  "matching_files": 1,
  "per_term_matching_files": {
    "shinmin19671106-1": 0,
    "shinmin19671218-1": 0,
    "一鼎金": 1,
    "一鼎金居士": 0,
    "命理趣味問題解答": 0,
    "命理趣味问题解答": 0,
    "1967-11-06": 0,
    "1967-12-18": 0
  },
  "hits": [
    {
      "path": "docs/research/TIANWEN-15EH-SINGAPORE-BAZI-PAN-ZIWEI-SOURCE-SHARD-R1.json",
      "blob_sha": "5a4db16e28ff4b4cd75d05efaa71ec0eae7c9600",
      "terms": [
        "一鼎金"
      ]
    }
  ],
  "truncated": false
}
```

仅命中15EH同名栏目，既有1968–69五期均非1967两期，非独立师承见证。分别打开馆方期号、定位题名及其直接链接：

| 期号 | 版页及文章编号 | OCR范围 |
|---|---|---|
| [1967-11-06](https://eresources.nlb.gov.sg/newspapers/digitised/issue/shinmin19671106-1) | 第8页社会服务栏，[shinmin19671106-1.2.43.4](https://eresources.nlb.gov.sg/newspapers/digitised/article/shinmin19671106-1.2.43.4) | 520词索引，五行和柱字候选，多讹 |
| [1967-12-18](https://eresources.nlb.gov.sg/newspapers/digitised/issue/shinmin19671218-1) | 第2页，[shinmin19671218-1.2.16.3](https://eresources.nlb.gov.sg/newspapers/digitised/article/shinmin19671218-1.2.16.3) | 646词索引，辛丑、辛金、印、生身等技术词候选 |

两个直接文章地址实际均返回 Terms and Conditions of Use 页；未点击 I Agree，未绕过权限。原图、署名全称、完整命例、1969分苑实际活动和作者身份均未证。不能据OCR建立十神/格局规则或断言1967为首传；15ED 1950–51 Elliott田野与2014职业回顾仍为不同层次旧证据，不重计。两条有界来源准入，见[分片](TIANWEN-15EI-SINGAPORE-1967-ARTICLE-SOURCE-SHARD-R1.json)，图谱零新增节点/边。TW-OPEN-0051 OPEN。

## 15EJ｜新候选：一般算命职业与八字公共讨论分层

- [新加坡政府开放数据，NLB Straits Echo 1910–1914](https://data.gov.sg/datasets/d_8ff0050ff9ab94b500b278cf97acd2f5/view)：数据预览1910-01-03、第9页、文章编号 straitsecho19100103-1.2.8，题名 Chinese Fortune Teller，首50词OCR为算命者涉及法院上诉的报道。未读原报或完整报道；题名及案件不足以判定发生地点或术法，尤其不证四柱、紫微、合法教学或传承。政府数据字段明确为文章首50词，不是全文。
- [星洲日报1981-01-22](https://eresources.nlb.gov.sg/newspapers/digitised/issue/scjp19810122-1)：第28页索引《四千人与你同“八字”》，701词索引，开头涉及婚配及算命者使用八字。属于同期社会话语候选，未见独立文章ID、原图、全文或实际咨询个案，不判定文中四千人算法是否成立。
- [NUS历史报刊馆藏](https://www.nus.edu.sg/nuslibraries/collections/special-collections/historical-newspapers-collection)与[2020年馆方数字化说明](https://nus.edu.sg/nuslibraries/whats-on-listing/news/2020/09/02/chinese-newspapers-in-southeast-asia)为早期新马报刊检索路线，不计命理证据；后者报告当时已数字化27种新马报纸共90360期。仍须落实可免费公开访问的具体目标文章，不以馆藏覆盖代替目标文本。

15EJ两候选未准入，先执行完整登记库查重，归入现有TW-OPEN-0047范围。继续寻找马来西亚独立同期紫微与四柱证据；既有51未决和5P0不变。Matrix222/222，来源1362=647+715／253片，图495/375，排盘核心CLOSED。


## 15EJ｜全库查询领取及地域/证据分层复核（未完成正式准入）

2026-11-26，精确HEAD `a245dcb00b1318e6e2e260c43cfe95caaffb62da`，[连续性 run 45840927551](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45840927551)，job 139982042149，62+7测试通过；六个R2绑定与真实树一致。查询程序 blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`（沿用前一批；本次另需核对程序blob）。以下是实际日志原样解析结果：

```json
{
  "query_id": "15EJ-1910-1981-regional-practice",
  "checkpoint_id": "TW-CHECKPOINT-15EI-ADMITTED-15EJ-PROVISIONAL-20261126",
  "request_blob_sha": "2e2ba5a080e613292bf350dff0890cce6486c748",
  "registry_manifest_blob_sha": "d41f189215e59518d587d6d8d97ce3644aebcb11",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 254,
  "records": 1362,
  "matching_files": 0,
  "per_term_matching_files": {
    "straitsecho19100103-1": 0,
    "Chinese Fortune Teller": 0,
    "d_8ff0050ff9ab94b500b278cf97acd2f5": 0,
    "scjp19810122-1": 0,
    "四千人与你同": 0,
    "四千人與你同": 0,
    "1981-01-22": 0,
    "1910-01-03": 0
  },
  "hits": [],
  "truncated": false
}
```

### 独立复核

- [NLB官方开放数据](https://data.gov.sg/datasets/d_8ff0050ff9ab94b500b278cf97acd2f5/view)确认 1910-01-03，第9页，page ID straitsecho19100103-1.1.3，article ID straitsecho19100103-1.2.8；前50词OCR指向法院上诉报道。直接[期号](https://eresources.nlb.gov.sg/newspapers/digitised/issue/straitsecho19100103-1)及[文章](https://eresources.nlb.gov.sg/newspapers/digitised/article/straitsecho19100103-1.2.8)本次浏览均不可取，不推定具体访问限制。 [1905-08-10同报报头索引](https://eresources.nlb.gov.sg/newspapers/digitised/issue/straitsecho19050810-1)显示 Penang 电报地址及1903年创刊信息；这是报纸地域背景，不是1910案件发生地证据。不得将OCR误字的人名扩写为确定身份，亦不得由算命职业报道推出四柱/紫微实践。候选等级：同期一般社会/司法话语的文章定位及有限OCR。
- [1981-01-22星洲日报第28页](https://eresources.nlb.gov.sg/newspapers/digitised/issue/scjp19810122-1)复核题名《四千人与你同“八字”》位于星云版，701词为馆方索引标注，实际可见仅开头短段，涉及婚配及命理咨询。该条在可见页面未给出独立article链接。 [新加坡华族文化百科报业史](https://culturepaedia.singaporeccc.org.sg/zh/popular-culture/nanyang-siang-pau-and-sin-chew-jit-poh-the-history-of-chinese-newspapers-in-singapore/)明确1975年新加坡星洲日报公司及1982年合并背景；[NLB报业史](https://biblioasia.nlb.gov.sg/all-sections/vol-15-issue-4-jan-mar-2020-from-lat-pau-zaobao/)亦可交叉核验。该条作为新加坡报刊公共八字话语候选，不直接归入马来西亚实践史，不把文章标题数字当作命理算法、实际统计或独立个案。
- 全库八词零字面命中；不等于语义去重完全结束。上述两候选分别拟作一般职业/社会话语与四柱公共传播的有界记录，非技术规则、师承或原页证据。报头及报业史为背景，暂不独立计数。

本次为R2.1查询结果保全及研究检查点追加，未修改六权威输入、未准入来源、未关闭TW-OPEN-0047/0051或任一P0。下一步复用该查询结果（核对实际request/manifest/脚本blob），核定候选语义身份并按正式原子批次准入；继续独立搜寻马来西亚同期明确紫微/四柱证据。不重复查询旧词或宣告15EJ完成。
