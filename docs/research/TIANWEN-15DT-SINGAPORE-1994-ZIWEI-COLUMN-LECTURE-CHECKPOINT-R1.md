# 15DT｜新加坡1994紫微报刊连载与讲座记述（临时检查点）

2026-11-26。恢复HEAD `75a210d078a3618273ee6cb0e835fbf6f7e22864`、tree `33d119a84896349b376cf937edb50e6ebf98e4e0`。六项恢复绑定全部吻合；[精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45802526833)通过。末次分页复核285项中231成功、16运行、38排队、零已见失败；综合门禁220步成功，Full unittest运行，未称全验收。维持五项P0及核心CLOSED。

## 独立同期报刊候选：从招课公告扩展到专题出版和讲座接受

均为新加坡国家图书馆 NewspaperSG 第一方期次页面可见文章标题、栏目、署名及有限OCR片段。本轮未取得原报像素、完整文章或SHA-256，不能用OCR异文裁决原字。书目候选不等于已经入库。

| 期次及链接 | 页／定位 | 有界证据 |
|---|---|---|
| [1994-06-15《联合早报》](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhzb19940615-1) | 第43页，L2684、2727–2735 | 刘含芝〈过尽千驹战胜自己〉；OCR提及听李佛紫微斗数演讲。不同报纸/作者的同期接受线索，地点、实际讲座日期、主题及听众尚未核。 |
| [1994-07-14《联合晚报》](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhwb19940714-1) | 第15页，L1037、1080–1087 | 李佛《海阔天空谈紫微》栏目〈太阳星正直有为（下）〉；题名提示上下篇，但未查全上篇。 |
| [1994-10-21《联合晚报》](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhwb19941021-1) | L1816–1824，页位原图未核 | 同栏目〈动态与静态的人生〉；有限OCR提到甲、乙级星及六十四颗星曜。仅作候选术语坐标，不立固定星数、安星表或派别同一。 |
| [1994-11-03《联合晚报》](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhwb19941103-1) | 第19页，L1234、1277–1285 | 同栏目〈紫微破军谋定后动〉；OCR涉及双星合宫、杀破狼及机月同梁分类；不是全段判法或算法定论。 |

三则同作者不同期次构成至少三个相隔日期的同名专栏定位；不推定每日连续、起止年月、完整篇数，也不是三个独立师承证人。另一份报纸的讲座接受记述并不证明课程举办全貌或讲座发生于新加坡；待全文核实。不得从六十四星等表面术语推出与王裁珊规则直接同源。

## 既有来源与重复筛查

15BE已有1990-07-01、1996-10-17、2000-10-02、2007-10-29四期招生公告，已复核双史纲与15BE文档；不新增。2000期次现有网页目录附近显示第15页相关广告，与15BE所记第14页存在潜在页位解释差异；未见原页，不作静默更改，不影响公告主题定位。

此前15DS台湾三条期刊索引与此组日期、刊名、文章身份不同。民国紫微职业实务仍未获新的同期可定年正证；1923–26道藏影印、1935《斗数宣微》后出重刊宣传等已有线索不重复登记，未访问付费机构报纸库。

## NEXT

提交与现有237分片manifest绑定的R2.1全库字面检索请求，含期次号、栏目繁简体、题名、作者与异体组合；待精确HEAD日志和语义裁决后才决定新增条目。TW-OPEN-0038 P1 OPEN：全库查重、原报图/正文、专栏起止及讲座具体上下文。TW-OPEN-0035、0037保持OPEN；民国独立实践和港台地域传播仍为后续主线，补东南亚同期证据是广度覆盖而非改换项目方向。

目前1299=647+652／237片、图474/375、Matrix222/222、38开放风险含五P0；无新增来源、图节点或边，无算法修改。

## 15DT 有界准入及补充定位（2026-11-26，追加）

[旧精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45803273075)，HEAD `cd28fe0793644a3a0d8a185e1b92d72b08e923d2`，job `139851750380`，62项遗漏门禁测试与7项R2测试通过。查询脚本blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。实际查询日志保全：

```json
{
  "query_id": "15DT-singapore-1994-ziwei-column-lecture-dedup-r2-20261126",
  "checkpoint_id": "TW-CHECKPOINT-15DT-PROVISIONAL-20261126",
  "request_blob_sha": "ad43a450fe2c0cb631729a38b2e95895d1807814",
  "registry_manifest_blob_sha": "05518b6c83b38885c7c287d809cfe37936c4c5dd",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 238,
  "records": 1299,
  "matching_files": 1,
  "per_term_matching_files": {
    "lhzb19940615-1": 0,
    "lhwb19940714-1": 0,
    "lhwb19941021-1": 0,
    "lhwb19941103-1": 0,
    "海阔天空谈紫微": 0,
    "海闊天空談紫微": 0,
    "太阳星正直有为": 0,
    "太陽星正直有為": 0,
    "动态与静态的人生": 0,
    "動態與靜態的人生": 0,
    "紫微破军谋定后动": 0,
    "紫微破軍謀定後動": 0,
    "过尽千驹战胜自己": 0,
    "過盡千駒戰勝自己": 0,
    "刘含芝": 0,
    "劉含芝": 0,
    "李佛": 0,
    "Li Fo": 0,
    "lhwb19900701-1": 1,
    "lhwb20001002-2": 1
  },
  "hits": [
    {
      "path": "docs/research/TIANWEN-15BE-SINGAPORE-1990-2007-COURSE-ANNOUNCEMENTS-SOURCE-SHARD-R1.json",
      "blob_sha": "1fc5e294b8dd8d072b4c08f35a1fbe4388a67afa",
      "terms": [
        "lhwb19900701-1",
        "lhwb20001002-2"
      ]
    }
  ],
  "truncated": false
}
```

唯一命中分片为15BE既有课程公告，复核blob `1fc5e294b8dd8d072b4c08f35a1fbe4388a67afa` 与四个期次URL，与本批四期不同，不重复登记。字面零命中不是语义无重复；四个原候选重新复核机构页题名、日期、作者、栏目和有限OCR，按 `RECEIVED_TEXT_VERIFIED`（仅可见索引/片段范围）准入，[分片](./TIANWEN-15DT-SINGAPORE-1994-ZIWEI-COLUMN-LECTURE-SOURCE-SHARD-R1.json)。六月讲座记述作者不同于专栏作者，但不证明讲座内容或师承，不将同作者三期视为独立传承证词。

### 三个新增同栏期次（待独立查重，不计入来源）

| 日期及期次 | 栏目题名与定位 |
|---|---|
| [1994-10-24 联合晚报](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhwb19941024-1) | 第19页，L1413–1421，李佛〈‘机、月、同、梁’型的人生〉；有限OCR提示主星分类 |
| [1994-11-10 联合晚报](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhwb19941110-1) | L1417–1425，李佛〈武曲天相进入各宫〉；可见题名和有限双星说明 |
| [1994-11-27 联合晚报](https://eresources.nlb.gov.sg/newspapers/digitised/issue/lhwb19941127-1) | 第15页，L1082、1098–1105，李佛〈太阳太阴明暗生辉〉；OCR严重乱码，不据其裁决义理 |

已定位专栏观察区间7月14日至11月27日，至少六期候选，三期已登记，不证明连续日刊或完整篇目。[NLB OneSearch FAQ](https://search.nlb.gov.sg/onesearch/FAQs) 说明完整报纸记录可到馆访问；[Newslink FAQ](https://eresources.nlb.gov.sg/main/Open/FAQ/10) 的账户/馆内限制不作为自主免费免账号获取路径。不要求用户到馆，不宣称原图已获。

TW-OPEN-0038 保留，补充查询绑定新manifest；TW-OPEN-0035、0037仍OPEN。来源1303=647+656／238片，图474/375、Matrix222/222、38风险含五P0，核心CLOSED。

## 15DT 补充三期准入（2026-11-26，追加）

精确HEAD `294ff2f8661a420560ba11c9311f7d2b807baf2e`，[连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45804545566)，job `139856198424`，62项遗漏测试、7项R2测试通过。验证程序blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。保全实际全库查询日志：

```json
{
  "query_id": "15DT-singapore-1994-supplement-column-dedup-r2-20261126",
  "checkpoint_id": "TW-CHECKPOINT-15DT-SUPPLEMENT-20261126",
  "request_blob_sha": "3a44aa551b3b17b73745ce462bc6db3756fa2a7f",
  "registry_manifest_blob_sha": "1b2670caea03928e4b1b29c9a9c3366f56d22df3",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 239,
  "records": 1303,
  "matching_files": 1,
  "per_term_matching_files": {
    "lhwb19941024-1": 0,
    "lhwb19941110-1": 0,
    "lhwb19941127-1": 0,
    "机、月、同、梁": 0,
    "機、月、同、梁": 0,
    "机月同梁型的人生": 0,
    "機月同梁型的人生": 0,
    "武曲天相进入各宫": 0,
    "武曲天相進入各宮": 0,
    "太阳太阴明暗生辉": 0,
    "太陽太陰明暗生輝": 0,
    "海阔天空谈紫微": 1,
    "海闊天空談紫微": 0,
    "李佛": 1,
    "Li Fo": 0
  },
  "hits": [
    {
      "path": "docs/research/TIANWEN-15DT-SINGAPORE-1994-ZIWEI-COLUMN-LECTURE-SOURCE-SHARD-R1.json",
      "blob_sha": "2547a8a81993bd8579262e3b0a1ab279bdebeb66",
      "terms": [
        "海阔天空谈紫微",
        "李佛"
      ]
    }
  ],
  "truncated": false
}
```

唯一命中为本批原四期分片（blob `2547a8a81993bd8579262e3b0a1ab279bdebeb66`）；原记录日期为6月15日、7月14日、10月21日、11月3日，与新增10月24日、11月10日、11月27日期次不同。同一栏目、同一作者不等于相同文章对象；未取得完整正文，不能排除内容重复或改写。复查机构期次网页：10月24日第19页L1413–1421，11月10日**第21页**L1384及1417–1425，11月27日第15页L1082及1098–1105；前两条可见有界主题片段，后者OCR严重乱码，仅采用题名、作者、栏目、日期。三条均按 RECEIVED_TEXT_VERIFIED 限定公开索引/片段准入，非原报字形或完整术理证明。[新增分片](./TIANWEN-15DT-SINGAPORE-1994-ZIWEI-COLUMN-SUPPLEMENT-SOURCE-SHARD-R1.json)。

至此1994年7月14日至11月27日至少六个已登记的同栏发表期次，另有6月15日不同作者的讲座接受记述；不宣称完整连载、师承、实际授课细节或最早传播日期。TW-OPEN-0038、0035、0037均保留。1306=647+659／239片，图474/375，Matrix222/222，38风险含五P0，核心CLOSED。下一单元回到独立可定年民国紫微实务及港台出版/实践传播。
