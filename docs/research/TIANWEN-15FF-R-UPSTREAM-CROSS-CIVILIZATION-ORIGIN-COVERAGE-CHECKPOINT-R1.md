# 天问15FF-R｜第一阶段验收前的上游跨文明源流覆盖复核（2026-11-27，未结项）

## 1. 恢复及边界

精确基线 HEAD c23b7ababd3b81eeb05a0e140d47f9462db813da，tree 5a8d17547ebe0792ca823220f6d0f81120d33c3d。20项已触发 Actions 均 success，未见 verify-research-omission-continuity，不能使用 R2 快路径；逐一解析六个权威 Git blob（树中合计8,925,344字节），绑定6/6，复核五P0及58未决，Matrix222/222，647+841=1488来源/276分片，图819/581。R2视图紧凑JSON 3567字符；不是平台上下文余量测量。执行瑕疵：R1/R2正文、issue history一度未经足够字段限制输出并遭截断；后续仅投影必要字段，不把截断作原文已读。没有新的来源登记或历史结论。

用户确认初衷为追溯核心技术的源头，不是以某祖师/书名/国境为终点；宽度优先与独立双系统不变。上轮[15FF-Q](TIANWEN-15FF-Q-CORE-RULE-PASSAGE-CROSSWALK-CHECKPOINT-R1.md)为非终验的第三/第四门槛复评，已有11 SOURCE_INSUFFICIENT缺口索引仍有效。本轮新增一个独立P1而非覆盖其他未决事项。

## 2. 既有证据与结构性盲区

复读双史纲和图册：紫微史纲前史已有杜牧、《百中经》、P.4071和1430/1441题名、1581《捷览》；四柱史纲已有隋《五行大义》、唐吕才/李虚中、宋命书和四柱实例。13ZW的P.4071馆目列f.2r五星行度宫宿、f.2v十一曜见生及《聿廝經》《五星經》征引；14S直接影像定位 f.1r出生字段、f.1v–2v 星曜/宫宿、f.8r开宝题记。不能把十一曜黄道宫同十四主星斗数、三组干支加时支同完整子平时柱混同。既有赵江红2023星平合参摘要及15T机械证据表是候选路径而非祖源裁决。现代南亚传播单元15FD/15FE与古代输入方向不同。图谱全体819节点中以有限字面词检索发现P.4071及日本宿曜等导航；不据关键词结果断言全库没有其他古代文献。根源库单独搜索不代表全库，待R2.1真实全量查重。

| 上游轴 | 紫微待证 | 子平待证 | 入手顺序 |
|---|---|---|---|
| 中国本土历法、星官、干支五行、禄命 | 北斗/南斗、五行局、月时安命、四化形成 | 年本/纳音至日主/月令、十神及起运 | 复用既有隋唐宋明原证，逐机制而非术名 |
| 南亚、印度及南印度 | Jyotiṣa十二宫、宫义/宫序、强弱、运期、方盘图式；南印度特异性须独立证明 | 仅在有日期及技术输入链时记录可能借用，不能将出生时间共用当四柱同源 | 梵文/地域版本、年代、图形与算法；Yavanajātaka、Bṛhajjātaka为待核线索 |
| 希腊化星学 | 宫位、星体状态、角宫与三角结构是否经其他文明进入中国 | 只追有具体机制的跨术关系 | 原文及版本、区别共同祖源与直接借用 |
| 伊朗、中亚及佛教译经网络 | 十二宫、十一曜、术语翻译及实际命例 | 星命与禄命并用及影响边界 | 先追P.4071所引《聿廝經》及候选《宿曜經》《七曜攘災訣》，比较载体、语种与传播方向 |
| 唐宋至明的中国中介 | 宿曜、七政四余、十八飞星、星平合参、明刊十四主星之间的关系 | 宋元子平与相邻星命实践分立 | 区别原页、后出传文、现代解释，逐项找同机制及反例 |

以上候选仅为检索/覆盖框架，未直接取得或校核新的梵文、希腊文、波斯文古籍，不声称其确定年代、作者或传承。比较须区别宫位数/宫义排列/宫位输入、真实天体位置/符号安星、行星周期/十年大限、三角几何/实际推算法、方形绘图/布局历史；这些相似不得单独建强边。南印度来源需要排除广泛印度传统、希腊化共同来源、伊朗中介及独立发展等替代解释。若证据指向更早地区/体系再拓展，不预设传播链。

## 3. 后续与上下文验证

新增 TW-OPEN-0059 OPEN P1；保持原58事项及全部五P0不变。当前 checkpoint TW-CHECKPOINT-15FF-R-UPSTREAM-ORIGIN-20261127，同提交设置R2.1查询；查重仅字面匹配，需读取成功日志并核对请求、manifest、范围、逐词计数和truncated，语义去重另行判断。若无成功日志不得视为零命中。未完成广度第一阶段验收；下一步先完成上游证据导航与已有Q缺口风险交叉复核，再决定四门槛是否满足。独立双纲、CLOSED确定性排盘、零算法重开/候选坍缩/AI预测不变。无新增来源/节点/边，transmission_impact=NONE。新HEAD CI待验证。


## 4. 15FF-R2｜上游原文定位及真实查询验收（2026-11-27，候选未准入）

恢复基线 47b36fbbbe7dd218744f94968bb66d95061e1bdd；tree 0a093a9362b174f440525305fb139069effc1b35；R2六绑定吻合，4943字节，五P0均保留。精确HEAD连续性检查 [45998779815](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45998779815)，job140504808241成功；59风险及前一58项历史保留、62遗漏测试与7上下文测试成功。全库查询实际结果见下（日志留存期不作唯一交接）。Actions动态分页初次总数282、返回283，期间仍有运行中和排队项，不能据此宣称全检查通过。协议未变化，当前操作复用本对话已读约束；大状态与ledger仅在原子更新时读取。未测实际对话token余量。

验证程序 blob 3387254ce53ec0a1f1a3b779291e0c40997bf190；query结果（原始JSON字段保留）：

```json
{
  "query_id": "15FF-R-upstream-origin-coverage",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R-UPSTREAM-ORIGIN-20261127",
  "request_blob_sha": "eb6e9c50b413fbd064793c5fccd069f351077c68",
  "registry_manifest_blob_sha": "d5081119bedd4afa0324a7eec36bc5b1ce4372c3",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 277,
  "records": 1488,
  "matching_files": 3,
  "per_term_matching_files": {
    "宿曜": 1,
    "聿廝": 0,
    "聿斯": 1,
    "都利": 0,
    "七曜攘災": 0,
    "七曜攘灾": 0,
    "Yavanajataka": 0,
    "Yavanajātaka": 0,
    "Bṛhajjātaka": 0,
    "Brihat Jataka": 0,
    "Jyotiṣa": 0,
    "Jyotisha": 0,
    "Kotyk": 1,
    "Hellenistic": 0,
    "Indo-Iranian": 0,
    "印度占星": 0,
    "波斯占星": 0,
    "南印度": 0,
    "Mak 2014": 1,
    "星平合参": 1
  },
  "hits": [
    {
      "path": "docs/research/TIANWEN-13ZW-TANG-SONG-NATAL-SOURCE-SHARD-R1.json",
      "blob_sha": "35ba14024d22fd90c948bb5daf37c4dbc2710773",
      "terms": [
        "聿斯",
        "Mak 2014"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15I-SONG-BREADTH-SECONDARY-SCHOLARSHIP-SOURCE-SHARD-R1.json",
      "blob_sha": "eb40a0d6fc9608b0e0bdd896d18d2f4170e67247",
      "terms": [
        "星平合参"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CW-JAPAN-SUKUYO-SOURCE-SHARD-R1.json",
      "blob_sha": "0053175920498a025e5cfa90856bd061151620f3",
      "terms": [
        "宿曜",
        "Kotyk"
      ]
    }
  ],
  "truncated": false
}
```

三命中分片均实际读取：13ZW复用 Mak 2014《聿斯经》及P.4071馆目/研究；15I复用赵江红2023星平合参摘要；15CW复用 Kotyk 2018 **日本佛教宿曜研究**，并非另文2018 Sino-Platonic Papers 282。宿曜等并不意味着已经登记全部T1299/T1308；最初检索对书名末字「訣／決」、经号、刊名和异体仍需补充，不能以零命中准入。

### 唐代传本文献与后世斗数十二宫比较

SAT电子大藏经 T21n1308 p0427c08–p0428a15（[正文](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&s=&useid=1308_%2C01)）实际可见《七曜攘災決》七曜旁通表。按传文表的相对顺序提取标签（词义概括，不复制判断正文）：命、财、兄弟、田宅、男女、僮仆、妻妾、疾病、迁移、官位、福相、困穷；下段妻妾→夫妻、疾病→病厄、困穷→祸害，须保留同文语词差别。此为大正藏电子传文C，非唐原叶；不得直接断定所有段落同一年代。CBETA T1308_002直开未见检索所示本命宫句（动态加载），不作重复独立见证。T1299 SAT检索能定位黄道十二宫的说法，直开未复得目标句，保留候选。

| 比较维度 | T1308七曜表 | 通行紫微斗数（现有史纲/产品导航，非所有古本） |
|---|---|---|
| 起始与顺序 | 1命、2财、3兄弟、4田宅、5男女 | 1命、2兄弟、3夫妻、4子女、5财帛 |
| 疾病、迁移、官位 | 8、9、10 | 6、7、9 |
| 福相与末位 | 11福相、12困穷/祸害 | 11福德、12父母 |
| 星曜输入 | 日月五星、九执/七曜临宫表 | 十四主星及辅曜依出生历法字段安置 |

宫义部分重合而排列与输入机制不同；不能由相似语词断定抄传。亦不能把黄道十二星座、相对命宫十二人生领域和中国十二地支直接等同。

Kotyk 2018《The Sinicization of Indo-Iranian Astrology in Medieval China》（[原刊PDF](https://sino-platonic.org/complete/spp282_Indo-Iranian_Astrology_China.pdf)）文字检索与印页26–28截图实核：图3把宿、黄道与节气对照；图4为作者依据T1308重绘的圆盘，图内列星座、宫义、七曜和地支；印页28论中国星命以太阳与时辰排定宫位，与依纬度/升度计算的古典上升点区别。作者印页25将T1308编纂置806–865，另述都利聿斯经译785–805及不同伊朗路线；均是现代学术论证C，不能当作唐代实物年或紫微祖源裁决。图4是现代重绘、非唐原图。由此可设可检验中间机制，而非假定南印度直传。Mak 2015印度佛教星学传播论文与2013 Yavanajātaka年代修订论文暂仅机构书目/摘要线索，DOAJ直开403、期刊robots阻挡；不固定该梵文作品首作年代。新增候选均待精确二轮全库查重及语义核对，未注册新来源，未建边。

后续优先对T1308卷下 p0452b、T1299 p0387a26–b02原页/版本及既有Mak 2014全文页核；并补梵文及南印度特异图式，比较宫序与安命输入而非外形。四柱仅记录同场禄命/星命的知识环境，不因宫位证据更改四柱源流。TW-OPEN-0059 OPEN，五P0不变；保持第一阶段未验收、Matrix222/222、1488来源/276片、819/581图谱、59未决、核心CLOSED。transmission_impact=NONE。


## 5. 15FF-R3｜全库别名查询回收、传文年代分层及梵文宫序对读（2026-11-27，未结项）

本轮重新恢复 HEAD `a6348ba4ab4c48f50ff2504cb9323e8b52d3e652`、tree `649f68713198673afe5c23d0e31334befcd8a88d`，R2六绑定一致；精确HEAD连续性CI [45999562246](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45999562246) job 140507425917 success，62遗漏测试与7 R2测试通过。完整分页观察285个不同run，275 success、10 in_progress、无已知失败；非全绿。R2恢复文件4594字节（tree报告），全部五P0复阅，未改语义权威文件。启动阶段输出曾过量展开R1/R2正文及首100条Actions，属可避免的上下文开销，后续应仅输出白名单、分页聚合；不据此推断实际token窗口。

### 已回收的精确第二轮查询（取自上述job日志）

验证程序 blob 3387254ce53ec0a1f1a3b779291e0c40997bf190；查询请求、manifest、checkpoint均核对；如下为完整结果，不把字面未命中当作语义缺席。

```json
{
  "query_id": "15FF-R2-ancient-astrology-exact-aliases",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R-SINO-IRANIAN-HOUSES-20261127",
  "request_blob_sha": "15f76a4c2578f9e0ba7b0a5f5452fc85f2e7dc14",
  "registry_manifest_blob_sha": "d5081119bedd4afa0324a7eec36bc5b1ce4372c3",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 277,
  "records": 1488,
  "matching_files": 3,
  "per_term_matching_files": {
    "T1308": 0,
    "T21n1308": 0,
    "七曜攘災決": 0,
    "七曜攘灾决": 0,
    "七曜攘災訣": 0,
    "七曜攘灾诀": 0,
    "T1299": 0,
    "宿曜經": 0,
    "宿曜经": 0,
    "spp282": 0,
    "Sinicization of Indo-Iranian Astrology": 0,
    "Kotyk": 1,
    "Transmission of Buddhist Astral Science": 0,
    "Yavanajātaka": 0,
    "Yavanajataka": 0,
    "金俱吒": 0,
    "Dorotheus": 0,
    "都利聿斯": 0,
    "都利聿廝": 0,
    "P.4071": 2
  },
  "hits": [
    {
      "path": "docs/research/TIANWEN-13ZW-TANG-SONG-NATAL-SOURCE-SHARD-R1.json",
      "blob_sha": "35ba14024d22fd90c948bb5daf37c4dbc2710773",
      "terms": [
        "P.4071"
      ]
    },
    {
      "path": "docs/research/TIANWEN-14S-NCL-08346-TINGSHI-SOURCE-SHARD-R1.json",
      "blob_sha": "7ab6201cc48ea8a78bca04f62e593c08d85a8c5d",
      "terms": [
        "P.4071"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CW-JAPAN-SUKUYO-SOURCE-SHARD-R1.json",
      "blob_sha": "0053175920498a025e5cfa90856bd061151620f3",
      "terms": [
        "Kotyk"
      ]
    }
  ],
  "truncated": false
}
```

三命中分片已读取：13ZW的P.4071、Mak 2014已有登记；14S仅《桯史》对象及对照引用，不能重复登记P.4071；15CW的Kotyk为2018日本宿曜道论文，与SPP282作品题名/刊物不同。T1308/T1299和SPP282字面查重已完成，准入仍须核对同物异名与具体来源级别；不得把两处电子转录视为两个古代实物。

### 三组传文的技术区别与年代警戒

1. **T1308**：[SAT传文](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&s=&useid=1308_%2C01) p0452b03–09 实读（不是原叶）：图包括十二宫及二十八宿分度，白羊为初；以出生时所在宫移充卯时上宫，建立本命宫，其余十一位随人变化；句读与具体运算仍待版本/注疏核定。关键：p0452a29明载日本「長保元年三月五日」（999年为该年号首年，不换算具体日），b10–21另有日本校勘跋语与不同卷题。**不可把卷末这段直接标为806–865年唐代原文**，应先划分正文、附记、校勘及传抄层。p0452a25–26紧邻另一项重要中介证据：破军/午/日、武曲/未巳/土、廉贞/申辰/金、文曲/酉卯/木、禄存/戌寅/水、巨门/丑亥/火、贪狼/子/月；[CBETA同传文](https://cbetaonline.dila.edu.tw/zh/T21n1308_002) 可检索相同位置，非独立古本。七星与七曜和地支配对，既非斗数十四主星安星公式，亦不能径称纯印度原制。日期相邻不等于前段表也可精确定年为999。T1311 p0462a12、26附近北斗本命生年支配对为新增候选对照（[SAT入口](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?key=%E6%9C%AC%E5%91%BD%E6%98%9F&mode=detail&useid=1311_%2C21%2C0462)），暂只定位，不登记原页或强边；并入既有TW-OPEN-0059上游机制查核。
2. **T1299《宿曜经》**：SAT搜索定位p0387a26–b02，但精确页直开失败；[识典K1367卷上](https://www.shidianguji.com/zh/book/K1367/chapter/1kkt2w6oj73fo) 实读电子传文：十二宫为七曜运行分区，十二宫名从狮子开始，分别分配星宿九足，日/月各统六宫，宫与星曜有所属。这里的宫位是黄道星座分区，不能和T1308以本命宫为起点的十二人生领域合并。暂不升级为独立版本物证。
3. **Varāhamihira《Bṛhajjātaka》**：[哥廷根GRETIL梵文电子语料](https://gretil.sub.uni-goettingen.de/gretil/corpustei/transformations/html/sa_varAhamihira-bRhajjAtaka.htm) BJ_01.15–19 实读，2020-07-31 TEI转换，不是古抄本影像。1.15十二领域依次概括身体、家财/家族、兄弟、亲属/居处、子、敌、妻、死、善业/福、地位/职业、所得、损失（译义暂定，需核古注）。1.16明确以lagna为参照，1.17–18区分角宫等位置；与T1308上卷十二领域在相对顺序上大体接近，而通行斗数第2兄弟、第3夫妻、第4子女、第5财帛及父母/福德结构显著不同。宫序的相似支持跨文化比较价值，不证明直接借用或独有南印度起源。现有南北印度图式现代说明只能作为候选导航，未取得可定年南印度早期方盘原件；不据现代排版倒推祖源。

**本次研究裁决（暂定）**：将候选证据明确分为黄道分区、从命宫起的十二领域、七曜与北斗本命的配对、出生时移宫算法、十四主星排布五种独立机制。最值得继续的是T1308卷末层次及T1311/道教北斗文献、P.4071与《聿斯经》对照的具体机制；梵文文献与区域方盘须独立取证。下一步：在既有开放检查点内核对新增候选别名（Bṛhajjātaka/Brihat Jataka/GRETIL/Varāhamihira/T1311/北斗七星等），完成版本身份与来源准入，随后按同一提交更新登记、风险/纲要/图谱与R2视图。上一节待领取查询事项已完成，此节为追加证据 checkpoint，不宣告语义批次结项；当前状态文件原焦点的准入工作仍未完成。TW-OPEN-0059 OPEN，全部五P0保留，1488来源/276片、222/222 Matrix、819/581图谱、59未决、确定性核心CLOSED；transmission_impact=NONE（无新边）。第一阶段不终验，不变更排盘。新HEAD CI尚待核查。
