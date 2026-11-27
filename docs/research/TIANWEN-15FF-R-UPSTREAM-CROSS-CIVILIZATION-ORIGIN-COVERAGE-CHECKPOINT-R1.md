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


## 6. 15FF-R4｜隋代七星本命对应与晚唐外来星学的分轴（2026-11-27，未结项）

恢复基线 `b7d6dcf198918c8bfd2ac93f47dc4fa73962702a`、tree `2bee170e60961d03f314222b1f5d01588c24ddc9`；20个Actions中19 success、1 in_progress，无已知失败；本HEAD无连续性专项验证，按R2回退R1。六权威blob实际取回并JSON解析，绑定6/6；五P0复阅。R3第二轮查询已保存，不重复领取。本轮将待办写回语义状态及台账，纠正旧指针仍显示待领取的情况。大型台账上传因将原有紧凑JSON误展开为4,247,414字符，两次连接中断；分支未移动，恢复原有紧凑编码后成功建立blob，未删历史。该为上下文/传输开销缺陷，非平台token容量测量。

### A. 本土七星本命机制

京都大学人文科学研究所[《五行大義》卷四电子正文](https://www.zinbun.kyoto-u.ac.jp/~takeda/kyoudou/gogyou/gogyoutaigi/gogyo_gogyo_04_g.html)北斗七政段引《黃帝斗圖》，实读七星与生年地支；[识典AMNL0019卷四](https://www.shidianguji.com/zh/book/AMNL0019/chapter/1m9z0i479abzn)同样见此对应。两个电子正文不能自动视为两个古代物理见证。作品传统归隋萧吉，所引书名不证明黄帝时代成书。与[CBETA T1308卷二](https://cbetaonline.dila.edu.tw/zh/T21n1308_002) p0452a25–26、[SAT T1308](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&s=&useid=1308_%2C01)对读：

| 星名 | 五行大义生年支 | T1308地支/七曜 |
|---|---|---|
| 贪狼 | 子 | 子/月 |
| 巨门 | 丑亥 | 丑亥/火 |
| 禄存 | 寅戌 | 寅戌/水 |
| 文曲 | 卯酉 | 卯酉/木 |
| 廉贞 | 辰申 | 辰申/金 |
| 武曲 | 巳未 | 巳未/土 |
| 破军 | 午 | 午/日 |

7/7对应一致。五行大义后文以天地经、斗魁刚及建指解释子午独属、其余两支共属，并记六十甲子配法与斗领二十八宿；紧接遁甲经的五行分配不能误作T1308七曜表。T1308卷末含长保纪年及后世跋语，不把相邻七星表定年999或806–865。此证本土星名/支属同构与七曜组合，不证直接抄传或斗数安星法同一。斗数七同名星中贪狼、巨门、廉贞、武曲、破军属十四主星，禄存、文曲另属其他星曜。下一步查[CiNii BA71079398](https://ge.nii.ac.jp/ncid/BA71079398)高野山三寶院钞本影印、[NDL古写本影印解题馆目](https://ndlsearch.ndl.go.jp/books/R100000136-I1971149384758468106)，当前未取得原叶。[T1311 梵天火羅九曜](https://cbetaonline.dila.edu.tw/zh-tw/T1311) p0462a祭本命星及图形定位，以及[太上玄靈北斗本命延生經](https://www.shidianguji.com/zh/book/NGJ892411999011335136272/chapter/1lo6unspuqi37)生年支，均为候选导航，非完整原本核校。

### B. 外来星学的具体机制

Kotyk 2017, “Iranian Elements in Late-Tang Buddhist Astrology,” Asia Major 30(1),25–58，[中研院原刊PDF](https://www11.ihp.sinica.edu.tw/storage/w2_file/2754DfNUyFU.pdf)、[NTU书目](https://dlbs.liberal.ntu.edu.tw/DLMBS/en/search/search_detail.jsp?seq=673625)。不同于SPP282与15CW日本宿曜论文。印页37–39提取文本：据罗睺历表806与宗叡865请来目录论证T1308编纂范围，认为金俱吒署名可疑，并述中国北斗延命信仰与外来星学共存。印页40(PDF index15)截图实核：论《宿曜经》与T1308身体/星宿图、朔望宿配及印度历法转换；区分大正藏28宿与日本所传27宿版本。印页37–38截图超时，限文字证据。[CBC T1308](https://cbc.dila.edu.tw/cbc/text/1045/)为现代归属数据库，不是独立古本。印页41提取文本区分中国365.25度与印度/希腊化360度，仍须原文核校。上述支持分机制研究本土、印度及伊朗成分，不证明紫微直接来自南印度。

### C. 语义状态与下一步

R3第二轮完整查询已回收；根647记录单独查询五行大义相关词命中EXT-WIKISOURCE-WUXING-DAYI-GANHE（卷二干合），不是卷四证据，但作品已登记；manifest路径未命中不作全库无重复。第三轮R2.1请求覆盖24个书名/编号/异名（北斗、五行大义、T1311、Kotyk 2017、梵文、版本馆目）；待全库277文件验证后语义去重，按作品/版次/物件/数字替身分级。未准入新来源，未建图谱边，TW-OPEN-0059仍OPEN，保留全部59事项/五P0、15FF-Q缺口；Matrix222/222，1488来源/276片，819/581图谱，CLOSED排盘核心与紫微/子平独立。transmission_impact=NONE。语义状态1.1584.0，下一步按新查询与原页边界开展来源准入并更新双史纲，第一阶段不终验。新HEAD CI待验。


## 7. 15FF-R5｜卷四图像验证与五项传文准入（2026-11-27，未结项）

恢复 HEAD cc775dfbe4a4667b324679c351b8a8184b4e3fea，tree 6f4abc9778284bdb0ed0ee965cc1bf2fafaa8b84；R2六绑定一致。精确连续性CI [46001197225](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46001197225) job140512969216 success，62遗漏与7R2测试成功；285 Actions 284 success、1 in_progress。五P0复阅。第三轮查询实际记录（验证程序blob 3387254ce53ec0a1f1a3b779291e0c40997bf190）：

```json
{
  "query_id": "15FF-R4-dipper-and-astral-transmission",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R4-DIPPER-NATAL-20261127",
  "request_blob_sha": "cdfd380083c31c9c3fe6b6acfba4006090c46159",
  "registry_manifest_blob_sha": "d5081119bedd4afa0324a7eec36bc5b1ce4372c3",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 277,
  "records": 1488,
  "matching_files": 4,
  "per_term_matching_files": {
    "26571274": 0,
    "五行大義": 3,
    "五行大义": 0,
    "Wuxing dayi": 0,
    "gogyou": 1,
    "黃帝斗圖": 0,
    "黄帝斗图": 0,
    "北斗七星": 0,
    "本命星": 0,
    "T1311": 0,
    "梵天火羅九曜": 0,
    "梵天火罗九曜": 0,
    "北斗本命延生": 0,
    "T1307": 0,
    "延命經": 0,
    "Iranian Elements in Late-Tang Buddhist Astrology": 0,
    "Kotyk": 1,
    "Zokushōsai": 0,
    "Bṛhajjātaka": 0,
    "Brihat Jataka": 0,
    "Varāhamihira": 0,
    "GRETIL": 0,
    "BA71079398": 1,
    "紙背穂久邇": 0
  },
  "hits": [
    {
      "path": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json",
      "blob_sha": "ea2ab50479450c39ce3fc7a00ea91cd713bf4a60",
      "terms": [
        "五行大義"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CU-WUXING-DAYI-YOUNIAN-SOURCE-SHARD-R1.json",
      "blob_sha": "06ad0517fc9be40c786cd36ace7d4c14e1add404",
      "terms": [
        "五行大義",
        "gogyou"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CV-JAPAN-WUXING-DAYI-SOURCE-SHARD-R1.json",
      "blob_sha": "b3b3caae930255fc63d814b1469a41a1198f8a89",
      "terms": [
        "五行大義",
        "BA71079398"
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

四命中文件：根卷二干合此前已核；15CU卷五京都传文、1989影印馆目及刊本导航；15CV三宝院卷五、1932影印；15CW Kotyk日本宿曜论文。三分片实际逐条读取。作品相同不重复建作品，卷四独立段落与已登卷二/卷五证据不同。R2第二轮全库别名查询及R4均完整，SPP282与日本宿曜论文不是同篇。依据本轮直接复核及前轮留证，新增五项有限来源，见[分片](TIANWEN-15FF-R-UPSTREAM-ASTRAL-SOURCE-SHARD-R1.json)：京都卷四、SAT T1308、识典K1367宿曜经、GRETIL梵文、Kotyk SPP282。前四为传文、末项现代研究，均不授古物字形权威、不新增传承边。GRETIL表头明确2020-07-31转换及1979第二版，BJ_01.15–16实际复得，印度地域特异性未证。SAT p0427c08及p0452a25–b21实际复得，后者明列长保纪年与享和、文政跋；K1367序分定宿直品实际复得27宿、12黄道分区及每宫九足；SPP282印页28（PDF index29）重新截图，明确作者所述以太阳时辰定升宫与经典升度运算不同；这是现代学说，不是古图。

### 版本范围纠偏与近代印本图像

复用[15CV](TIANWEN-15CV-JAPAN-757-YINYANG-CURRICULUM-1248-WUXING-DAYI-MANUSCRIPT-R1.md)：757日本阴阳生书目、约891书目、三宝院1248校点为已有证据，不能倒推具体段落。和歌山县[正式物件目录](https://wakayama-bunkazai.jp/bunkazai/bunkazai-spot-1201/)重新打开，确认三宝院仅卷五、一帖64丁，早镰仓写本的估计及1248校点；**卷五不能证明卷四北斗段落**。1932影印同为卷五，不是全五卷。日本文化厅[201/8362 指定01763](https://kunishitei.bunka.go.jp/heritage/detail/201/8362)另列五帖、镰仓、元弘三年闰二月智圆相传奥书、1956指定、音羽产业所有；与三宝院一帖不同物。与穂久邇文库1989–90影印的同物关系须查解题及历史所有者，不从相似奥书自动合并。新物件先查重。

[公开扫描 NLC511-023031404016947-25263 第二册](https://upload.wikimedia.org/wikipedia/commons/9/9a/NLC511-023031404016947-25263_%E4%BA%94%E8%A1%8C%E5%A4%A7%E7%BE%A9_%E4%BA%8C.pdf) 实际截图：PDF零基index2版权页，1939年12月初版、1959年10月补印、商务印书馆；index12印页74卷四，第十六论七政，人工辨读从右数第四至第六栏黃帝斗圖引文及相邻文字，贪狼子、巨门丑亥、禄存寅戌、文曲卯酉、廉贞辰申、武曲巳未、破军午可辨，均与京都受读相合。网页提取误把生读作牛、亥作女、辰申间夹巳等，不采用；以所见印页为该近代印本读字证据，不是隋代或镰仓原件；底本、馆藏实物精确绑定和图像字节SHA尚未取得，不准入物理字形权威。index14、15印页76–77为邻段控制。本轮两项目标页截图成功，未保存原PDF或SHA，NLC及五帖目录等待第四轮精确物件查询，不另计来源。CiNii BA71079398直开超时；不将超时记为无书。

已更新紫微史纲/双史图册及语义状态，当前1.1585.0；647+846=1493来源、277分片，819/581图谱、222/222 Matrix、59未决含五P0，核心CLOSED。保留Q不足项与TW-OPEN-0059 OPEN。下一步第四轮物件查询覆盖新manifest；不得以广义1959/出版社命中多寡当语义裁决。未获南印度可定年早期方盘或直传证据，T1311/Kotyk 2017仍候选。第一阶段不终验，transmission_impact=NONE。

## 8. 15FF-R5续｜第四轮全库查重回收、元弘相传本与九曜传文候选复核（2026-11-27，未结项）

基线 HEAD `416ae62354b5a083f24a7dbf48020e19d05ffcba`，tree `aeb7aae09370792670bf44ecb907ac6992cec73f`。R2派生视图六项绑定一致，但初始 exact-HEAD continuity queued，故实际读取、解析六权威blob回退R1，核对222/222、647+846/277、819/581、59未决五P0，均一致；随后[本HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46002841826) job140518585502 success，62遗漏与7 R2测试通过。首次全页Actions复核285个（231 success、37 queued、17 in_progress，无已知失败），不称全绿。R1大state普通读取为空，精确blob恢复成功。此次仍有全库命中语义核对和候选资料获取任务，未将运行状态误认成验收。

第四轮查询结果，验证程序blob 3387254ce53ec0a1f1a3b779291e0c40997bf190：

```json
{
  "query_id": "15FF-R5-wuxing-edition-and-object",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R5-PASSAGE-ADMISSION-20261127",
  "request_blob_sha": "ed4e3188c46e49d6582cfc03a623dce042707a48",
  "registry_manifest_blob_sha": "318b3f3beb9da3590d9656cd17929e303857a551",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 278,
  "records": 1493,
  "matching_files": 13,
  "per_term_matching_files": {
    "1959": 7,
    "NLC511-023031404016947-25263": 0,
    "023031404016947": 0,
    "叢書集成初編": 2,
    "丛书集成初编": 0,
    "商務印書館": 6,
    "201/8362": 0,
    "01763": 0,
    "元弘三年": 0,
    "元弘相伝": 0,
    "穂久邇": 1,
    "穗久邇": 0,
    "音羽産業": 0,
    "BN04262897": 1,
    "000002057459": 0,
    "T1311": 0,
    "梵天火羅九曜": 0,
    "Iranian Elements in Late-Tang Buddhist Astrology": 0
  },
  "hits": [
    {
      "path": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json",
      "blob_sha": "ea2ab50479450c39ce3fc7a00ea91cd713bf4a60",
      "terms": [
        "商務印書館",
        "1959"
      ]
    },
    {
      "path": "docs/research/MING-DATONG-YEHUOBIAN-12QE-EXTERNAL-SOURCE-REGISTRY-DELTA-R1.json",
      "blob_sha": "498ec4b80bfd7eca14b98b5642d8547ca32038d6",
      "terms": [
        "1959"
      ]
    },
    {
      "path": "docs/research/MING-DATONG-YEHUOBIAN-12TN-MODERN-1959-2012-SOURCE-SHARD-R1.json",
      "blob_sha": "98e868d66dc054f17eb7ac62ee353073fb33a5c7",
      "terms": [
        "1959"
      ]
    },
    {
      "path": "docs/research/MING-DATONG-YEHUOBIAN-12TP-JOURNAL-NDL-SOURCE-SHARD-R1.json",
      "blob_sha": "deca7555ebe14c27c202f26dff45fc33be4f5f70",
      "terms": [
        "1959"
      ]
    },
    {
      "path": "docs/research/MING-DATONG-YEHUOBIAN-12VA-PANG1959-SCHOLARLY-SOURCE-SHARD-R1.json",
      "blob_sha": "1933aedc64503732750d18a64c424d07d65fdd07",
      "terms": [
        "1959"
      ]
    },
    {
      "path": "docs/research/MING-DATONG-YEHUOBIAN-12VQ-MODERN-EDITION-DESCRIPTOR-FIREWALL-SOURCE-SHARD-R1.json",
      "blob_sha": "48d80ebc1f12d5dd3e78e05bd4a07b7c97368291",
      "terms": [
        "1959"
      ]
    },
    {
      "path": "docs/research/TIANWEN-13YZ-NLC511-1936-XING-J45-SOURCE-SHARD-R1.json",
      "blob_sha": "ab2841b5c92634e21a7adbd6bc4b1390c953bd7d",
      "terms": [
        "商務印書館"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15K-WENYUANGE-CATALOG-1935-1937-SOURCE-SHARD-R1.json",
      "blob_sha": "d54229af6ebcf3d2db12f322aae35f917f6a084f",
      "terms": [
        "叢書集成初編",
        "商務印書館"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CC-MINGSHI-YIWENZHI-NLC-SCAN-SOURCE-SHARD-R1.json",
      "blob_sha": "187ac72d8392323dad26ba7ea04fafe7d2bfd5fe",
      "terms": [
        "叢書集成初編",
        "商務印書館"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CH-XINGMING-ZONGKUO-PALACE-DEGREE-AND-ATTRIBUTION-SOURCE-SHARD-R1.json",
      "blob_sha": "a14ec0c934d29c0edd8b2993feb24ea870ce14da",
      "terms": [
        "商務印書館"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CN-SONG-DONG-ZIPING-TAIYIN-SANMING-SOURCE-SHARD-R1.json",
      "blob_sha": "b300d94c60032cfba9b9b9fdd6fce1e16d8c9e1d",
      "terms": [
        "商務印書館"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CU-WUXING-DAYI-YOUNIAN-SOURCE-SHARD-R1.json",
      "blob_sha": "06ad0517fc9be40c786cd36ace7d4c14e1add404",
      "terms": [
        "穂久邇",
        "BN04262897"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15DJ-TAIWAN-JAPAN-NISHIKAWA-SOURCE-SHARD-R1.json",
      "blob_sha": "d9b1a34c5da42e2888b24bca46781bb190c8e381",
      "terms": [
        "1959"
      ]
    }
  ],
  "truncated": false
}
```

实际读取并解析全部13命中文件（根647条及12个分片）。唯一相关的既有版本馆目为15CU的 EXT-TIANWEN-15CU-NDL-CINII-BN04262897-1989，复用而不重复登记；广义1959、出版社、丛书名命中不指向新增NLC卷四物件，根内卷二亦非卷四。字面查询结果不等于语义全库穷尽，新增异名、馆藏变迁仍需核实。

- [日本国会图书馆联合目录 BN04262897](https://ndlsearch.ndl.go.jp/books/R100000136-I1971149384758468106)实读：1989.12–1990.7汲古书院两册，第一册正文、第二册纸背，穂久邇文库所藏古写本影印；已登记15CU，复用。[NDL本馆第2册](https://ndlsearch.ndl.go.jp/books/R100000002-I000002057459)实读：1990.7、HR511-E143、pid13275615，馆内限定公开，不获得原页、不提出付费或登录申请。书店[ISBN 4762910929](https://www.toho-shoten.co.jp/toho-web/search/detail?bookType=jp&id=4762910929)记穂久邇文库五帖、元弘三年知円相传奥书，与[文化厅01763](https://kunishitei.bunka.go.jp/heritage/detail/201/8362)五帖、镰仓、元弘三年闰二月智円相传奥书、音羽产业所有描述高度相合；书店标第2册1989.12，与NDL 1990.7有差异，日期以对应馆目分层保留。现有证据加强同物候选，仍缺直接所有权/实物连续证据及卷四目标叶，不能合并为已确认同一物；亦不将1333奥书直接当正文抄写年代。1959近代印本与该古写本的底本关系仍未证。
- [SAT T1311 梵天火羅九曜](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&nonum=1&useid=1311_,00,0462)实读首段：一行修述署名与咸通十五年甲午（874）历年记载并存，不能把现存传文整体直接定年一行生前。又见罗睺年龄序列1、10、19等九年间隔，土星2、11、20等，属于另一类岁数九曜分配和攘灾机制，不能混作北斗七星地支本命或斗数十四主星安星。CBETA/SAT为传文校验，不计为两古本；段落年代与原刊图形待核。
- Kotyk 2017 [Asia Major 原刊](https://www11.ihp.sinica.edu.tw/storage/w2_file/2754DfNUyFU.pdf)实际截图index0/14（印页25/39）：作者明确将T1308视为多源合编，并以罗睺历表806起点及宗叡865请来目录作编纂区间的论证；书在中国实际运用范围不明，日本宿曜道使用的证据不能倒推紫微直接传承。这是现代研究论证，不是古物证据；T1308与T1311的署名及内在年代各自审查。

本节仅在已登记TW-OPEN-0059下追加实读候选与可复验查询结果，尚未准入新source、未新增图节点/边、未作语义状态结项；旧state/ledger当前检查点仍指本文件，前节“第四轮待领取”由本节成功查询回收事实补正。保留全部59未决/五P0、Q不足项及紫微/子平独立、CLOSED产品。下一步从本节直接进行已有候选的准入裁决（T1311、Kotyk 2017、NLC1959印本证据、文化厅物件和NDL特定影印册），核南北印度方盘历史见证与希腊化/伊朗中介具体机制；若有新词/编号，按现有R2.1查询规则执行，不重复领取已保全查询。原页身份未绑定及第一阶段不终验均不变。transmission_impact=NONE。

## 9. 15FF-R6｜九曜行年與北斗本命分離、版本系統新線索（2026-11-27）

基線 HEAD `e76078458de6142f7dec51727b1b36625fb95e55`、tree `9859a5650c38fe354a713257910126d0e32bf42a`。20 Actions（19 success、1 in_progress）；本HEAD無 continuity workflow，按R2回退R1，六原始JSON解析、6/6绑定，五P0及59未决核对。R5 exact 416ae62 continuity成功及第四轮全库278文件/1493来源/13命中已在§8保存；重用不重新查询。新增四来源见[分片](TIANWEN-15FF-R6-UPSTREAM-VERSION-AND-NAVAGRAHA-SOURCE-SHARD-R1.json)，非四件古物。

**T1311机制对读。** [SAT T1311](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&nonum=1&useid=1311_,00,0462) 本轮实际重读首段、行年段、葛仙公礼北斗段及跋：罗睺1/10/19、土2/11/20等九年间隔；另有贪狼子、巨门亥丑、禄存寅戌、文曲卯酉、廉贞辰申、武曲巳未、破军午，七组与《五行大义》卷四及T1308生年支表7/7相合。两套机制在现存传文中共存，却分别按岁数循环和出生年支归属。T1311另引《聿斯经》论罗睺计都及葛仙公礼北斗法；同书共存不证明同一技术、直接抄录、或同一时代。首段874纪年和一行署名并存，末有文治五年（1189）及后世书写校记；不得把整体、个别表、印本年代混同。未核原图与早期独立物证，不引入斗数运行时。

**外来传播研究复核。** [中研院原刊目录](https://www1.ihp.sinica.edu.tw/Publications/AsiaMajor/1047) 的全文链接实际可达 [原刊PDF](https://www1.ihp.sinica.edu.tw/storage/w2_file/2754DfNUyFU.pdf)，截图index0、14（pp25、39）本轮成功。Kotyk 2017 主张T1308多源编纂约806–865，依据罗睺历表起点与宗叡请来目录（注68 T2174A），中国实际使用范围尚不清楚。属现代研究而非独立原件，后续需核目录正文与伊朗术语/天文机制，不推导斗数直传。

**《五行大义》两条版本线。** 新发现中村璋八《日本の仏典に引用された五行大義に就いて》，《密教文化》1960 48–50，[J-STAGE原刊PDF](https://www.jstage.jst.go.jp/article/jeb1947/1960/48-50/1960_48-50_31/_pdf/-char/en)，实际截图index0/1（印页31/32）。p32作者论1699元禄刊本、1799《佚存丛书》、1804许宗彦校刊、1813知不足斋、1897盛氏、1939丛书集成的关系；又区分穂久邇文库元弘五帖、神宫文库模写本，与高野山卷五、天理图书馆1540–41天文钞本、阳明文库转写本的另一候选系谱。此为现代版本学判断；p32原刊图像可见卷五46处异同的作者统计，不是本项目独立重算。1959补印所据1939本与上述刊本链有明确研究入口，但未核实具体近代底本或卷四古写本异文。1958《日本中国学会报》第十集[PDF](https://spc.jst.go.jp/cad/literatures/download/1730) 可检索到同主题正文和奥书图版定位，尚未定位截图页、未准入、不将转写当古本；与1960文的同源关系需核。二文及其他版本名进入第五轮精确查重。日本文化厅01763与NDL本馆第二册馆目本轮再次实读，分别为物件和近代影印册书目证据；既有BN04262897复用。历史所藏与当前所有者连续性仍未证，原页仍未取得。

结论：新增4有限来源，1497总来源/278分片；图819/581，Matrix222/222；59未决含五P0。保留TW-OPEN-0059及15FF-Q缺口；本轮无新图谱边（transmission_impact=NONE），无历史直接祖源裁决，无排盘算法重开。下一步核第五轮查询、中村版本研究及天理/神宫卷四原页，继而南北印度地域证据和伊朗中亚具体中介。不作第一阶段终验。

## 10. 15FF-R7｜版本学复核与南印度方盘的可定年证据入口（2026-11-27）

基线 HEAD `f24c01c50fb88585e74a8fc4e21e81c66d8d379d`、tree `8178f78f15ccffe36730fb74640dd706cf20df69`。R2恢复视图六绑定与真实树一致；精确HEAD[连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46004260627) job140523331888 success，62风险测试、7 R2测试通过；首轮分页查询285 Actions中未见已完成失败，但有未完成项，不作全绿宣告。五P0保留。第五轮实际查询（验证程序blob 3387254ce53ec0a1f1a3b779291e0c40997bf190）：

```json
{
  "query_id": "15FF-R6-nakamura-manuscript-lanes",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R6-NAVAGRAHA-AND-EDITION-LANES-20261127",
  "request_blob_sha": "dec398cec5394a85b89b2049ab55e14747219687",
  "registry_manifest_blob_sha": "aa62b2c746e4a6e34a13e4deeb9782f06a305b96",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 279,
  "records": 1497,
  "matching_files": 2,
  "per_term_matching_files": {
    "1699": 2,
    "1799": 1,
    "1960_48-50_31": 0,
    "日本の仏典に引用された": 0,
    "日本の佛典に引用された": 0,
    "中村璋八": 0,
    "Nakamura Shohachi": 0,
    "spc.jst.go.jp/cad/literatures/download/1730": 0,
    "天文鈔本": 0,
    "天文写本": 0,
    "天理図書館": 0,
    "天理圖書館": 0,
    "卜部兼右": 0,
    "神宮文庫": 0,
    "陽明文庫": 0,
    "元弘相傳本": 0,
    "元弘相伝本": 0,
    "佚存叢書": 1
  },
  "hits": [
    {
      "path": "docs/FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json",
      "blob_sha": "ea2ab50479450c39ce3fc7a00ea91cd713bf4a60",
      "terms": [
        "1699",
        "1799"
      ]
    },
    {
      "path": "docs/research/TIANWEN-15CU-WUXING-DAYI-YOUNIAN-SOURCE-SHARD-R1.json",
      "blob_sha": "06ad0517fc9be40c786cd36ace7d4c14e1add404",
      "terms": [
        "1699",
        "佚存叢書"
      ]
    }
  ],
  "truncated": false
}
```

全部两命中文件实读并语义核查：根647条中命中为Fozhu编号或《文渊阁书目》1799见证，与《五行大义》版本学论文无关；15CU七项中复用1699元禄馆目及盛氏重雕馆目。新增两篇现代研究，不计为独立古物、亦不将同一作者的两篇文章计为两个独立校勘证据。见[来源分片](TIANWEN-15FF-R7-NAKAMURA-EDITION-STUDIES-SOURCE-SHARD-R1.json)。

**A. 1958版本研究与1960引文研究。** [JST正式论文目录](https://spc.jst.go.jp/cad/literatures/1730)确定中村璋八1958年《五行大義鈔本・版本の傳流とその資料的價値》；[全文PDF](https://spc.jst.go.jp/cad/literatures/download/1730)14页，本轮截图index0–4、12–13（印77–81、89–90）成功，index11超时，文字提取大量乱码，采用人工图像核读。p80作者比较1699元禄校刊本与元弘相传本，区分1799佚存丛书本，论后者较接近元禄刊本而非直接钞古本；p81区分清代许宗彦改订、知不足斋、常州先哲遗书等再刊与1939丛书集成初编，不能当作彼此独立的古代文本投票。pp89–90提到钞本批校、异本夹注以及从日本其他引文判别其可能归属，作者对材料不足的推断明确保留。该版本学分析比简单二分支更复杂，尤其不能把共享异文等同直接父子本。[1960密教文化原刊](https://www.jstage.jst.go.jp/article/jeb1947/1960/48-50/1960_48-50_31/_pdf/-char/ja)截图index0、1（31、32）本轮重新成功：p31记757阴阳生书目及日本历代引用，p32记版本回传、卷五异文46处及1540–41天文钞本。46为作者统计，尚非本项目复算，卷五不能替代卷四目标叶。未获取天理、神宫文库古叶，不将现代文献中的书目转述升级成原件核读。

**B. 南印度方盘分离“图式”“历法输入”“安星”。** [1885 Iyer英译本 Wellcome 馆藏扫描替身](https://upload.wikimedia.org/wikipedia/commons/a/a9/The_Brihat_jataka_of_Varaha_Mihira_%28IA_b2488442x%29.pdf)网页提取题名页为Madras Foster Press 1885、N. Chidambaram Iyer，印页6章一第6颂后的译者注说明南印度使用归于Jaimini的Rasi Chakra，并列十二固定黄道格：顶行双鱼、白羊、金牛、双子；右侧巨蟹、狮子；底行从右往左处女、天秤、天蝎、射手；左侧从下往上摩羯、水瓶。此为译者时代的地域见证候选，不是六世纪梵文原作所画图，也不能因归于Jaimini就认定古代年代。另一[Google扫描替身](https://www.wilbourhall.org/pdfs/the_brihat_jataka_of_varaha_mihira.pdf)同段可提取但顶行首格OCR错写Mesha，提示不能依网页文本定稿；Wellcome PDF截图请求因16MB大小限制失败，另一PDF截图超时。本轮**未实见图像**、未核馆藏号，不准入原页证据。其格固定黄道星座及行星守护，与紫微地支固定宫格的表现相似不等于相同坐标、命宫算法或星曜排布。下一步取得可复核页面及更早地域物证。

**C. 南印度地方文献检索。** [英国图书馆临时目录](https://searcharchives.bl.uk/?f%5Blevel_ssi%5D%5B%5D=%5B40%5D+File&f%5Bmaterial_type_ssi%5D%5B%5D=Archives+and+Manuscripts&f%5Bproject_collections_ssim%5D%5B%5D=Private+Collections+of+Palm-Leaf+Manuscripts+from+the+Tamil+Country&f%5Brelated_places_ssim%5D%5B%5D=India%2C+Asia&f%5Brelated_subjects_ssim%5D%5B%5D=Astrology&per_page=100)实际目录EAP1294/2/33 Stotrapāṭhaṃ，梵文及泰米尔文，1750–1900，27叶、33 TIFF，目录仅称可能包含命盘；EAP1294/2/55 Deśaporuttaṃ 同期、19叶加封叶、23 TIFF，婚配术候选。未见原叶或年代自证，不登记为实见方盘。已开第六轮精确查重，前两项目录、1885英译及中村1976专著等仅候选。继续查实际图像及较早文献，不从晚近形制倒推传入中国时间。

1499总来源/279分片；图819/581、Matrix222/222、59未决五P0。未新增传承边（transmission_impact=NONE），未裁决南印度独有祖源，不重开核心，不终验。保留Q不足项、TW-OPEN-0059及版本未绑定。新HEAD CI待复核。


### 10a. 15FF-R7 延续检查点｜方盘传播方向的反向假说与实物定位（2026-11-27）

基线 HEAD `cf579d12def723403ee9c5639d1b10258308a2af`、tree `f3b6674062df267366bc65f04c0529dc80b8dc9e`。六个权威blob绑定逐项吻合；exact-HEAD continuity run 46005276026 尚 queued，故没有启用R2派生快路径，直接解析六原始JSON，核59 OPEN、五P0、Matrix222/222、根647/扩展852/279分片及图819/581。第六轮全库查询尚未领取，不作未命中断言、不准入来源。本节为既有TW-OPEN-0059的研究候选保全，非新语义状态或结项。

- **Iyer版次物件绑定增强（馆目，不是目标原页）**：[Wellcome第一方目录](https://works.www.wellcomecollection.org/works/afmgm695) 实读 Madras: Foster Press, 1885、N. Chidambaram Iyer、236 pages, x、21 cm、Aryan miscellany、馆内位置 Closed stores AJA.23、Public Domain Mark。可读数字入口存在但工具未返回图像；IA b2488442x 的印页6目标仍未实见，馆目不能替代方盘原图，也不证明与其他扫描为同一实物。EAP1294/2/33 仍目录候选。
- **反向传播候选**：Johannes Thomann 2008, “Square Horoscope Diagrams in Middle Eastern Astrology and Chinese Cosmological Diagrams: Were These Designs Transmitted through the Silk Road?”, pp97–118, [Smithsonian书目](https://www.si.edu/object/siris_sil_922621)，[作者章节网页文本替身](https://www.academia.edu/24379875/The_Journey_of_Maps_and_Images_on_the_Silk_Road)。研究提出西亚方盘可能源于东亚其他占卜图式，并以敦煌Pelliot 2964r十二神运转图、西亚/希腊方盘作比较；目前为网页文本/书目核读，非全部原件复核。BnF[官方专题入口](https://heritage.bnf.fr/france-chine/manuscrits-dunhuang-relatifs-aux-mathematiques-et-lastronomie)列Pelliot chinois 2964，候选[数字对象](https://gallica.bnf.fr/ark:/12148/btv1b8302295m/f3.image.r=pelliot%20chinois%202964)仍待实际原图定位，不能据此判定其就是紫微命盘或定向传播。
- **2026现代论文实际图页核读**：Alexander Jones, “The Horoscope of AD 497 Attributed to Eutocius: Text, Translation, and Commentary”, Occasional Notes on the Ancient Astral Sciences 1, DOI 10.5281/zenodo.18852314，[NYU公开PDF](https://archive.nyu.edu/bitstream/2451/75616/2/Jones%202026%20Horoscope%20of%20AD%20497%20Attributed%20to%20Eutocius.pdf)，实际截图 index0,18,34,35（印pp1,19,35,36）。p1区分497命盘所指日期与传世11世纪 Laur. Plut.28.34 ff141v–143v、14世纪 Par.gr.2425 ff216v–219v；p19为现代英文重绘而非古叶照片；p35十二开放区域以地平/子午圈为参照，升点与中天等四角分出的不等黄道弧再三等分成宫界，不是固定星座格或地支格；p36讨论Thomann的东亚起源假说，认为即便该假说未证，此图仍可能后加。故不能把497事件日期作方图现存物证年代，也不能将图式共性升格为中国/印度/西亚直接传承。p36另提同抄本后文历表例为855而非796，这是作者判断，未重算。
- **希腊实物定位**：[佛罗伦萨Laurenziana第一方数字馆](https://tecabml.contentdm.oclc.org/digital/collection/plutei/id/567885)列 IT:FI0100_Plutei_28.34，1001–1100、羊皮纸、170 cc.、图像目录369项及目标143v；提供 [IIIF manifest](https://tecabml.contentdm.oclc.org/iiif/info/plutei/567885/manifest.json)。本轮未实见143v，不能把现代图19当古叶；原图、巴黎对本及二者具体版式异同待核。

机械比较独立四层：图框/分格几何、宫位坐标与命宫输入、天体或符号赋值、运限机制；每层均需独立年代与传播证据。反向传播、平行发展、多源汇流均为待检假说。下一步先保全原R7第六轮查询日志并核验所有命中，继而同一次全库查询加 Thomann、Eutocius、Jones、18852314、Plut.28.34、Par.gr.2425、Pelliot chinois 2964、btv1b8302295m、afmgm695、AJA.23 等明确异文与馆号，按实际字面命中及语义去重裁决；再取Iyer印页6、Laur.143v、P.2964及Tamil原叶。没有完成这些门禁之前，不新增登记或传承边，不做终验。transmission_impact=NONE；核心CLOSED及59 OPEN/五P0不变。


### 10b. 15FF-R7 延续｜第六轮全库查询保全与古代纸草对照（2026-11-27）

基线 HEAD `870d4653cd9d650506f3323032f6e61aed0abcf0`、tree `0f1d4249a6019450c188d0dcfcf8d1ff1689835f`。六权威输入blob与同对话上次已完整解析者完全一致；无需重复展开。精确HEAD Actions 20项（19 success、1 clean-training-system in_progress），无 continuity workflow，未冒用前一HEAD验收当前HEAD。相关PR #364 base为工作分支、head为12nk政策独立性分支，本次不合并或改动；另两PR base main。第六轮全库请求绑定未变，原请求提交 `cf579d12def723403ee9c5639d1b10258308a2af` 的 [continuity run 46005276026](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46005276026) job 140526757928 success，实取日志，62遗漏风险测试及7 R2测试通过；验证脚本blob 3387254ce53ec0a1f1a3b779291e0c40997bf190。以下为日志实际JSON字段保全：

```json
{
  "query_id": "15FF-R7-regional-chart-witnesses",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R7-NAKAMURA-REGIONAL-CHARTS-20261127",
  "request_blob_sha": "a9ade5d54a8db04d9692d9cba735342079574825",
  "registry_manifest_blob_sha": "46a75cadb4940cf265fb302f0e911fa646d50253",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 280,
  "records": 1499,
  "matching_files": 0,
  "per_term_matching_files": {
    "Chidambaram Iyer": 0,
    "Chidambaram Aiyar": 0,
    "b2488442x": 0,
    "22501499401": 0,
    "brihatjatakavar00iyergoog": 0,
    "Tiruvadi": 0,
    "Rasi Chakra": 0,
    "Rāśi Cakra": 0,
    "EAP1294/2/33": 0,
    "EAP1294/2/55": 0,
    "EAP1294": 0,
    "Stotrapāṭhaṃ": 0,
    "Stotrapatham": 0,
    "Deśaporuttaṃ": 0,
    "Tamil Country": 0,
    "Jaimini": 0,
    "南印度": 0,
    "五行大義の基礎的研究": 0,
    "000001242501": 0,
    "000007719927": 0
  },
  "hits": [],
  "truncated": false
}
```

无命中仅指原请求20个字面词，非语义无重复结论；旧请求结果已保全，可更新同检查点的查询合同。

**古代实物对照 P.Berl.9825。** Dorian Greenbaum & Alexander Jones, 2017, ISAW Papers 12, PDF印题页所示持久链接 http://doi.org/2333.1/brv15m2（规范引用以 [NYU原刊目录](https://dlib.nyu.edu/awdl/isaw/isaw-papers/) 的[文章](https://dlib.nyu.edu/awdl/isaw/isaw-papers/12/) 与[存档记录](https://archive.nyu.edu/jspui/handle/2451/49543)为准，原刊xhtml在本工具中不支持）。[作者存档PDF](https://archive.nyu.edu/jspui/bitstream/2451/49543/4/Greenbaum%20and%20Jones%202017%20PBerl%209825%20ISAW%20Papers.pdf)实见截图index0,4,6,7,28（页1/5/7/8/29），index5超时。图2、4、5为柏林埃及博物馆纸草馆Sandra Steiß摄影的同一纸草不同装框，实见残损希腊文字及分栏网格，不是三件独立文物；限发表照片的布局级核阅，未获馆方原始高分辨率对象图像，未逐字校勘。p8正文称现存四段分表，以红线框分；字迹符合由内容推算的四世纪年代，出生地纬度近Syene而出土地/编制地点不明；开端残缺，319是作者根据天文资料复算的事件日期，不是保存完整的抄写纪年。p29表7把此纸草与四种详细希腊命盘比较，包括黄道位置、宫主/界主、擢升、月交点、分点及命主等；仅用作独立技术比较。保留文物残损及未见装框B限制，不能由三幅照片断言原文完整地绝无其他图形。论文现代重绘图不等于古代纸草原图。此证据有助区分早期星占表格和后代方形十二宫，不能证明后代方盘已于319出现，更不证明紫微直接源于希腊。

**版本独立性与反证。** 2026 Jones论文另实读pp2–3（截图index1–2）：Vind. phil. gr. 179 ff80v–83r为节本，图式另见ff38v–39（作者叙述，未核原叶）；作者认为P与V经失传中介有共同祖本、L与该祖本又上溯非作者原稿的祖型。L删去历表引介、P保存相关文字及后章；图和正文传承可能不同步。原页待核，不能把三抄本视作三独立源头或把497事件日期作图式年代。 [Pinakes目录16215](https://pinakes.irht.cnrs.fr/notices/cote/16215/) 对Plut.28.34馆藏及11世纪后半作另一目录定位；其中Eutocius条目140v–142*，与论文141v–143v范围不完全同，仍以具体原叶验证。此处需更正10a中对该佛罗伦萨抄本11世纪的宽定年不能变成精确叶面日期。

**获取障碍及冲突。** Wellcome单页viewer入口出现JS反机器人检查，Florence IIIF manifest工具无法获取；[巴黎对本Gallica](https://gallica.bnf.fr/ark:/12148/btv1b107240960)返回403；BL EAP1294/2/33目录继续仅可能包含出生盘，未核图。Deborah Houlding的[现代图式讨论](https://www.skyscript.co.uk/greek_horoscope.html)指向1959 Neugebauer/Van Hoesen摄影翻印，主张497图可能保有早期内容，且将Laurentianus描述为10世纪；与第一方11世纪目录及Jones后加可能性形成待核对意见，不能据该网站裁决年代或独立见证。保留两种解释，不重复把现代转绘当原叶。

**下一步**：同一既有检查点发布第七轮全库字面请求，检索上述反向传播研究、古代纸草、抄本编号及Wellcome对象，待CI实际成功并核读命中后准入。Iyer、EAP的第六轮查询有效，仍待图页/语义消歧。保持TW-OPEN-0059、59 OPEN/五P0、Q不足项、Matrix222/222、来源1499/279、图819/581、双体系独立、核心CLOSED；本轮不改变语义状态、不新增source/edge、transmission_impact=NONE，不终验。


### 10c. 15FF-R7 延续｜梵文星占文本的年代校勘与传播机制（2026-11-27）

基线 HEAD `30ff4181102fd64f1ef59446c5efd41f1fc6a20a`、tree `6ce77ced38c1d79b5cf808b06a15120824e0934f`。六权威输入哈希仍与真实树一致。精确HEAD Actions 21项：20 success、clean-training-system in_progress；[continuity run 46006580879](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46006580879) job 140531138166 实际成功，62+7测试。第七轮查询日志按实际JSON保全（验证程序blob 3387254ce53ec0a1f1a3b779291e0c40997bf190）：

```json
{
  "query_id": "15FF-R7-counterdirection-and-papyrus-witnesses",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R7-NAKAMURA-REGIONAL-CHARTS-20261127",
  "request_blob_sha": "5f80dd4260d4be7dacb41019818c1aae17221da3",
  "registry_manifest_blob_sha": "46a75cadb4940cf265fb302f0e911fa646d50253",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 280,
  "records": 1499,
  "matching_files": 0,
  "per_term_matching_files": {
    "18852314": 0,
    "Thomann": 0,
    "Eutocius": 0,
    "Jones": 0,
    "Plut.28.34": 0,
    "Plut. 28.34": 0,
    "Par. gr. 2425": 0,
    "Vind. phil. gr. 179": 0,
    "Pelliot chinois 2964": 0,
    "Pelliot 2964": 0,
    "btv1b8302295m": 0,
    "afmgm695": 0,
    "AJA.23": 0,
    "P.Berl. 9825": 0,
    "P.Berol. inv. 9825": 0,
    "P.Berl.9825": 0,
    "brv15m2": 0,
    "Greenbaum": 0,
    "btv1b107240960": 0,
    "Houlding": 0
  },
  "hits": [],
  "truncated": false
}
```

零字面命中不是语义无重复。上一轮候选仍需入库裁决，尤其原件/现代论文/目录身份各自独立，禁止直接祖源边。不要因本节继续另一条研究支线而遗忘已完成的两轮查重和待准入来源。

**希腊—印度：Yavanajātaka 断代不是定论。** 本轮实读 Bill M. Mak, “The Date and Nature of Sphujidhvaja’s Yavanajātaka Reconsidered in the Light of Some Newly Discovered Materials”, HSSA 1 (2013), 1–20, [DOI](https://doi.org/10.18732/H2RP4T)，[大学期刊原刊PDF](https://journals.library.ualberta.ca/hssa/index.php/hssa/article/download/7/7/13)，[Érudit替身](https://www.erudit.org/en/journals/hssa/2013-v1-hssa09872/1116424ar.pdf)，印pp2–4、10–16、18的提取文本。截图尝试被反机器人或限制阻断，不能宣称实际核读其梵文原叶图1、2。另读同作者 [SCIAMVS 14 (2013) 59–148原刊](https://www.sciamvs.org/files/SCIAMVS_14_059-148_Mak.pdf) pp59、63–64、83校勘本提取文本；截图因13.8MB尺寸受阻。两篇不同论文、同一研究者和重叠手稿材料，不作独立古证投票。

- Pingree 1978的149/150及269/270 CE两日期是对末章第60–62颂的数字词（bhūtasaṃkhyā）及文字复原所得，不是明确抄本纪年。Mak HSSA pp13–14依据新抄本Q90v与N103r的异文，反对将相应词组解成71、191；p16指出希腊技术借词与印度本地材料并存，反对把现传本简化为希腊原典翻译。这里只记录作者的校勘论证与反驳，尚无独立梵文逐字重校，不能将新作者定为绝对权威。p10第14颂56/66及Śaka历元前后之争，亦说明追算历元不等于作品年代。Mak指出22 CE至多为相关章的年代下限候选，不能直接作为抄本或全书成书年。
- 抄本N：NGMPP A31/16，SCIAMVS列NAK 1/1180，HSSA缩写表另作NAK 1180/vi.jyaut.45，约12世纪为字形推定而非自署纪年。1954 Tucci摄影、1970缩微和2011彩色数字照片是N不同替身，不是独立古本。Q：NGMPP A1122/3 = NAK 6/2397，约18世纪纸本，新尼瓦尔文字，目录曾误题Bṛhadyavanajātaka；Q的独特异文可帮助弥补N损坏，并非较晚即无价值。HSSA p4称现有78页、编号至90；SCIAMVS p63则列81 folios (8–87,90)，数字与计量对象需原目录/实物核对，保留差异而不强行统一。Q把Pingree章77–79合为一章，报告104颂、N为101颂；另有章题和总颂数之争。
- 技术层：Mak p16列horā（希腊语对应）、drekkāṇa（三分/旬区）、liptā（角分）等借词与业力、阿育吠陀、印度诸神及165年yuga并存；这些是可分解的比较目标，不是对紫微星曜或安星算法的直接见证。p18指出与Sārāvalī、Mīnarāja的Vṛddhayavanajātaka共享段落的方向需要重新审查，不能把有共同文字预设为后书抄前书。
- 与天问相关的研究方法：先给跨文明文献的具体见证建立年代区间、原词与运算语义，再与中国本命北斗、十二宫/星宫、日月行星历表和后世斗数安星逐条比对。希腊—印度技术接触不等于印度—中国全部传承，更不能直接推出南印度—紫微单向复制。前两节的方盘图式反向传播候选独立保留。
- 未获取N、Q馆方完整原图，未确认现代论文中所用替身与馆藏在线物件的一一绑定。本轮第八轮查询加入梵文题名异体、作者、稿本号、两篇论文的稳定标识和相关反证著作。上轮第七轮查重与第六轮查重均已经保全；在新增登记使manifest变更之前，复用其现有结果，先完成前批候选语义消歧及准入，不无限延长查询循环。当前研究是既有TW-OPEN-0059支线，未新增风险类别、未改状态版本；59 OPEN五P0、1499来源/279分片、Matrix222/222、图819/581不变，transmission_impact=NONE，核心CLOSED，不终验。


## 11. 15FF-R8｜六来源裁决完成，原子发布待恢复（2026-11-27）

**状态：PENDING_ATOMIC_PUBLICATION，非正式准入。** 基线 HEAD `8ac248dcf70649cff9a732832bb49546b46ec5a8`、tree `dcbc81f60c96990d30e69c12774ba6b820a20cbd`。该HEAD [continuity run 46007149769](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46007149769) job140533070997 success，62+7 tests；21 Actions中20 success、1 clean-training-system in_progress。第八轮实际日志如下，验证脚本blob 3387254ce53ec0a1f1a3b779291e0c40997bf190：

```json
{
  "query_id": "15FF-R7-yavanajataka-dating-and-textual-witnesses",
  "checkpoint_id": "TW-CHECKPOINT-15FF-R7-NAKAMURA-REGIONAL-CHARTS-20261127",
  "request_blob_sha": "e26b9fc5901b4e44f64ace37fe4d1ab2bc2c802f",
  "registry_manifest_blob_sha": "46a75cadb4940cf265fb302f0e911fa646d50253",
  "status": "PASS",
  "scope": "ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY",
  "files": 280,
  "records": 1499,
  "matching_files": 0,
  "per_term_matching_files": {
    "Yavanajātaka": 0,
    "Yavanajataka": 0,
    "Yavanajātaka": 0,
    "Sphujidhvaja": 0,
    "Yavaneśvara": 0,
    "Bill M. Mak": 0,
    "Bill Mak": 0,
    "H2RP4T": 0,
    "h2rp4t": 0,
    "1116424ar": 0,
    "SCIAMVS_14_059-148_Mak": 0,
    "A31/16": 0,
    "A1122/3": 0,
    "NAK 6/2397": 0,
    "NAK 1/1180": 0,
    "vi.jyaut.45": 0,
    "Bṛhadyavanajātaka": 0,
    "Vṛddhayavanajātaka": 0,
    "Mīnarāja": 0,
    "Sārāvalī": 0
  },
  "hits": [],
  "truncated": false
}
```

第六、七轮结果见§10b/c。三轮均280文件/1499来源/20词零字面命中；仅对具体候选身份及字面检索范围作判断，不作普遍语义无重复断言。本轮六项有限准入裁决已完成，具体条目见[待登记分片](TIANWEN-15FF-R8-REGIONAL-AND-CROSS-CIVILIZATION-SOURCE-SHARD-R1.json)。该文件暂不在manifest中，不能计入正式来源总数，不能据其增加图谱节点/边。

Wellcome 1885 Iyer、BL EAP1294/2/33仅馆目；Thomann 2008限书目及反向假说归属；Greenbaum/Jones 2017为现代研究及同一P.Berl.9825四装框发表照片（本轮补读Fig3 frame B cols v–vii，版式级核阅）；Jones 2026 pp35–36复核为现代批判校勘及图式年代讨论；Mak HSSA 2013 pp13–18提取文本，截图受阻，非独立梵文原字裁决。EAP1294/2/44另有个人命盘的目录线索尚未查重、未取得原图。以上为上一工作单元的研究记录；本恢复轮不声称新增原图实读。保留Iyer印页6、Florence/BnF原叶、Mak SCIAMVS、天理/神宫卷四、1959底本、伊朗中亚中介等未决。不增加物理字形权威。

### 11a. 发布阻塞的精确复现与恢复合同

- 远端正式 state=1.1587.0，1499来源/279分片、Matrix222/222、图819/581、59 OPEN含五P0；core CLOSED。不得提前宣告1.1588.0或1505来源。
- 拟提交分片 Git blob `9c11f0d0b4229ca899526b9e8b9dd9b21e6a5e9d` 已生成并回读六条完整记录，本次仅将其作为未登记候选附在既有研究检查点。
- 拟提交manifest blob `a3931ce82103490efb1ef6f6cda740cc5f839be1` 已回读，六条新增、总1505/280分片。拟提交state blob `c4e1d8f81d75f764c10ddb335f27c851cacd6e1c` 已回读，schema1.1588.0、focus3284。二者仍未挂接权威路径，不是live state；若对象未来不可读则从当前权威文件和候选分片重建，不依赖孤立对象长期存续。
- 原台账blob `5453fef89e6e3173337043381b9d5e35010fc1c1`，实际紧凑UTF-8 4,070,463字节、3,737,867字符、1018 checkpoints，JSON parse及重序列化字节数一致。按原规则追加后的紧凑内容3,743,131字符。多次 create_blob（含紧凑编码）及 create_tree inline content 均失败，报 h2 protocol error: error reading a body from connection。不能确认具体服务端限额；不是可通过去掉缩进解决的问题。容器 curl/git ls-remote 无法解析github.com，无本地checkout发布路线。**未削弱校验、未删除任何历史数据、未修改工作流权限。**

恢复时先重新发现HEAD并验证canonical bindings/最新检查点/最新CI；若仍为1.1587.0及相同三权威blob，六条候选查重仍可复用。用具备真实checkout与Git写权限的执行路径（或后续可承载大blob的正常连接）完成：
1. 在同一工作树中保留候选分片，按已回读拟manifest/state的具体差异更新，核旧分片及来源计数完整、状态版本1.1588.0。
2. 读取原ledger全量JSON；保留旧对象、旧历史与1018个checkpoint原值。更新binding.reviewed_state_version=1.1588.0、source_focus_count=3284、latest_research_focus_prefix=13ZZ。对TW-OPEN-0059追加下述evidence_boundary（保留原文），next_action用拟state.research_execution_strategy.next_deliverable；source_refs只增不删，增加本分片路径；append EVIDENCE_SCOPE_REVISION，changed_fields=[evidence_boundary,next_action]、previous_fields为旧字段原值、reason为“Complete exact-HEAD registry rounds and bounded evidence admission, not historical closure.”、evidence_refs为本检查点及分片路径。追加checkpoint（复制上一个checkpoint中全部reviewed_issue_ids与discovery_mode，覆盖id为TW-CHECKPOINT-15FF-R8-REGIONAL-CROSS-CIVILIZATION-ADMISSION-20261127、date=2026-11-27、state_version=1.1588.0、result为拟state最后focus；evidence_refs为本检查点、双历史覆盖atlas、紫微outline、分片及现有query合同；unresolved_breadth_leads保留TW-OPEN-0059 OPEN，next_evidence为next_action）。evidence_boundary追加：
```text
 R8: rounds 6–8 full 280-file/1499-record literal queries passed; six scoped bibliographic/secondary sources admitted. P.Berl.9825 frame B photograph recovered (four frames one artifact), Jones pp35–36 rechecked, Mak HSSA received text only. No ancient square chart, original Sanskrit glyph or direct lineage adjudication.
```
3. 更新紫微历史纲及双史atlas的有限准入导航；将本节追加完成状态（不得重写本失败记录），运行 scripts/project-context-r2.py build/verify，现有来源和遗漏/forward-only gates；旧query checkpoint变更后应为STALE_CHECKPOINT，不是新manifest零命中。所有权威变更及派生view同一原子提交，非破坏性lease，回读远端及精确HEAD CI。新HEAD若已经推进则重新语义合并，不盲用拟blob。
4. 如果当前执行通道仍无法写入4MB台账，不得反复提交同一失败尝试。保留本checkpoint，转向不改变权威状态且可合规完成的原始资料调查；长期可评估保留全部历史、兼容全部调用者及CI门禁的台账分片方案，但未经过完整依赖审计和验证不实施迁移。

transmission_impact=NONE；本次仅保全未完成研究工作及恢复合同，不更改正式语义状态、计数或历史裁决。当前研究保持广度优先、不终验。


### 11b. 大台账存储治理：实际分布与依赖审计（2026-11-27）

基线 HEAD `22955d20275975654eac5cf0be7324ed59ea79f8`、tree `b83665851b199814f89a63f81d9492bbb486e652`。6个canonical binding核对一致；20 Actions中19成功、clean-training-system未完成；未把无触发的continuity当作当前成功。实际本地 git ls-remote 再试，github.com DNS不可解析。保留§11的六条候选和正式1499来源；不重试已证实失败的大blob写入。

原ledger完整解析（实际UTF-8 4,070,463字节），issues数组2,456,296字节、checkpoint_log数组1,612,785字节。TW-OPEN-0005一条2,198,111字节，其中history 741条、2,020,129字节，source_refs 1089条/91,331字节；TW-OPEN-0058 63,218字节。检查点按既有顺序每100条的大小分别为69,500/72,203/70,731/80,958/82,887/97,538/97,813/133,679/196,816/568,735字节，末18条141,935。单按issue分片仍会保留一个2.2MB的大热点；单按条数分组亦不能约束UTF-8字节。优先评估基于真实字节上限的不可变历史块+小型活动头/清单，不删除或重写任何既有语义记录，不把衍生视图改为权威。

已实际读取主要代码：scripts/verify-research-omission-risk-ledger-r1.py 的 read(LEDGER)与parent_revision直接从HEAD^同路径json反序列化，check_forward_only比较完整history/checkpoint前缀；scripts/project-context-r2.py 的make_view和SHA绑定直接使用六权威原始文件；tests/test_research_omission_risk_ledger_r1.py使用verifier.read(m.LEDGER)，tests/test_project_context_r2.py还直接从PATHS读取原始ledger并构造投影。现有workflow的路径过滤与父提交fetch-depth=2也需兼容。已检查verify-project-continuity-state-r1.py及两图谱脚本，没有发现该路径直接引用；不是全库无其它依赖的证明。

**本提交仅在现有R2测试文件追加只读静态依赖清点，不增加workflow、不改权限、不改变任何原有断言。** CI在实际checkout对全部Git tracked text执行git grep，输出HEAD及三类精确字面命中（ledger路径/Schema、字段、verifier入口），docs中的JSON/MD/TXT仅计数，其他文件路径完整输出。需要领取精确HEAD成功日志中 TIANWEN_LEDGER_DEPENDENCY_INVENTORY，逐一检查实际调用语义，尤其历史工作流的直接读取、父版本对比、测试fixtures及脚本动态路径。静态字面清单不是动态调用图；迁移必须额外复核间接导入及路径拼装。不得把无匹配或未领取CI结果称作完成审计。

候选迁移验收原则：①使用唯一权威manifest绑定各原始块，复原完整旧JSON并逐对象与基线完全相等（含所有历史、顺序、未知字段）；②所有活跃读取者和Git父版本对比同时支持旧格式与分片格式，历史workflow按实际兼容需要处理，不降级已有校验；③R2绑定必须覆盖全部权威块，不能只哈希未绑定的索引；④按UTF-8上限分块，旧块不可改写，任何新增变更经过原有validate及check_forward_only；⑤现有测试全通过并增加缺块/篡改/重复/顺序/错误parent/状态失配的负向测试；⑥迁移与六条史料正式准入可独立验证，不把迁移成功等同历史裁决。无完整依赖审计及兼容验证前不实施迁移。当前任务仍为TW-OPEN-0059，59未决五P0、核心CLOSED、不终验。


### 11d. 全库依赖实测后的低风险发布路线（2026-11-27）

基线 HEAD `9ff598487b5f32ae539d3cdb5996dffae314d490`、tree `95740bebf533d618e2987dc4e53bf82c0ebaf43f`。六绑定一致；21 Actions中20 success、clean-training-system in_progress；[continuity run 46008937761](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46008937761) job140539151184实际62+8 tests成功。日志 TIANWEN_LEDGER_DEPENDENCY_INVENTORY 是精确HEAD全Git tracked text字面扫描；path/schema 428命中（93 workflow、296 scripts、30 tests、9 docs数据），field 441（295 scripts、139 tests、7 docs），verifier入口78（66 workflow、1 script、3 tests、8 docs）。三组相互重叠，不得相加为独立调用者。全清单仍在该job日志，未逐一动态审计。实读13MX脚本等直接JSON读取、12XW读取台账并检查历史事件和版本，主CI及历史workflows大量调用。另有旧sync-project-state-batch-12cp workflow具contents:write但写入过时1.102.0状态，不得触发、改用或绕过权限。当前真实容器git ls-remote测试DNS失败。

**取舍：现阶段优先保持所有旧格式直接读取者兼容，验证小型确定性增量程序在具备checkout的执行通道重建完整文件；不是立即切换分片格式。** 新增固定范围 scripts/prepare-tianwen-r8-admission.py，8个已核blob pins、限定R8六来源、原check_forward_only；输出仅到checkout外新目录，无远端写、无权限改变。测试在临时本地硬链接镜像中先unlink再写替换文件，核原始台账字节未变，运行既有state/来源/遗漏/forward-only/R2 view及query门禁，核1018个旧checkpoint完整保留和1019新计数。该测试复用现有R2 CI，未改既有workflow和权威文件。需要领取 TIANWEN_R8_PREPARED_REPLAY 精确HEAD实际成功日志；若失败先检查原验证错误、资源或兼容问题。即便PASS也仅是预发布重放，不是远端正式准入或对传承争议裁决；不得提前更新语义计数。现有1.1587.0、1499/279、59 OPEN五P0及CLOSED保留。正常具备Git checkout和写权限的发布路线仍是独立依赖；未授权或不可用时不声称完成，不改变工作流权限。避免因为一个大文件就未经审计地改动数百历史校验器。


### 11e. R8增量重放首次CI的接口纠正（2026-11-27）

基线HEAD `1e35cf3094072a5b7a6ba96dbbae1e7e9be799b6`、tree `acfd18e90b72c1df9317bfe27e00722c27990f0d`。六权威绑定一致；21 Actions中19 success、1 in_progress、1 failure。精确HEAD [continuity run 46009495893](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46009495893) job140541075419实读日志：62原遗漏风险测试通过，当前权威视图与全库查询PASS；9项R2测试中8项成功、新增R8重放测试在line162因KeyError 'status'失败。该测试依次执行候选state、来源登记、遗漏风险等旧门禁，已到达遗漏风险输出解析；原verifier实际返回 {"result":"PASS",...} 而非 {"status":"PASS",...}，其进程退出码已通过检查。不能将此前失败记作完整候选验收，后续R2及全历史前缀断言未走完。本提交仅在新测试按特定verifier原合同读取result字段，并增加明确错误诊断；其余门禁、权威文件、prepare程序与权限不变。新HEAD须领取精确CI TIANWEN_R8_PREPARED_REPLAY成功结果，不以旧失败推断成功。当前仍1499/279、1.1587.0、59 OPEN五P0、CLOSED；正式发布路径仍未解决。


### 11f. 增量重放通过，待独立发布（2026-11-27）

精确HEAD `77e9c3823448362ad43eed20982c9fecf74ddcd3`、tree `46bab244503a13a45be0153006f37a0c1728d899`，六绑定一致。21 Actions中20 success、1 clean-training-system in_progress。[continuity run 46009705352](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/46009705352) job140541786156成功，62+9 tests，实取候选重放日志如下：

```json
{
  "status": "PASS_PREPARED_NOT_PUBLISHED",
  "gates": {
    "scripts/verify-project-continuity-state-r1.py ": "PASS",
    "scripts/verify-historical-source-registry-extensions-r1.py ": "PASS",
    "scripts/verify-research-omission-risk-ledger-r1.py ": "PASS",
    "scripts/project-context-r2.py verify": "PASS",
    "scripts/project-context-r2.py request": "STALE_CHECKPOINT"
  },
  "replacement_bytes": {
    "docs/PROJECT-CURRENT-STATE-R1.json": 1804737,
    "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json": 4076303,
    "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json": 183859,
    "docs/PROJECT-RECOVERY-VIEW-R2.json": 4907,
    "docs/research/TIANWEN-15FF-R-UPSTREAM-CROSS-CIVILIZATION-ORIGIN-COVERAGE-CHECKPOINT-R1.md": 75267,
    "docs/TIANWEN-ZIWEI-HISTORICAL-OUTLINE-R1.md": 152535,
    "docs/TIANWEN-DUAL-HISTORY-COVERAGE-ATLAS-R1.md": 238794
  },
  "candidate_blob_sha": {
    "docs/PROJECT-CURRENT-STATE-R1.json": "c4e1d8f81d75f764c10ddb335f27c851cacd6e1c",
    "docs/RESEARCH-OMISSION-RISK-LEDGER-R1.json": "7f9799d56bfe3e3f5265ae55fc7488b0c4b622bb",
    "docs/FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json": "a3931ce82103490efb1ef6f6cda740cc5f839be1",
    "docs/PROJECT-RECOVERY-VIEW-R2.json": "33a4235957bc1edc6a255c2c691e78bfa3b7f4d1",
    "docs/research/TIANWEN-15FF-R-UPSTREAM-CROSS-CIVILIZATION-ORIGIN-COVERAGE-CHECKPOINT-R1.md": "8b59b012ae6968cef72c9c6887dd5c4746831b0e",
    "docs/TIANWEN-ZIWEI-HISTORICAL-OUTLINE-R1.md": "322e63f69d51e04f868b826ddcb9829cf9519091",
    "docs/TIANWEN-DUAL-HISTORY-COVERAGE-ATLAS-R1.md": "488aced24cc74b37651bd0ea7377b6a3e6fc1846"
  }
}
```

实际隔离重建、既有状态/来源/遗漏/前向历史/R2验证均成功，1018旧checkpoint完整保留，候选1019；旧query正确返回STALE_CHECKPOINT。原始台账未改。候选台账4,076,303字节；远端fetch_blob对候选ledger及view均404，故本地重放成功不等于Git远端对象已写入。后续doc追加会改变候选BATCH摘要，prepare需对当前checkout重新生成；不要把上述整套候选hash当作永久固定包。保持无远端写权限的测试通道，既有发布阻塞未解除；无需重复同一4MB上传失败，也不改旧工作流权限。当前1499正式来源、六候选、1.1587.0、59 OPEN五P0不变。

## 12. 15FF-R9候选｜伊朗与中亚技术中介的独立证据路线（2026-11-27）

本节不是新准入；无重复全库查询结果、无古代字形裁决。避免工程发布阻塞全部源流研究。继续保留南印度实际方盘、Iyer印页6、希腊及敦煌原叶、Mak SCIAMVS和五P0。与前面R8准入程序的QUERY pin保持一致，本轮不改现行query合同；待发布或重新设计兼容的查重路线后统一检索以下候选。

**伊朗技术层。** 实读 David Pingree, [HOROSCOPE, Encyclopaedia Iranica XII/5, 477–478](https://www.iranicaonline.org/articles/horoscope/)（2004-12-15，2015-07-15更新）网页。作者把281-10-20与381-02-26两个星占事件定位在Dorotheus希腊作品的巴列维语翻译插入层，主要经约800年Umar ibn al-Farrukhan al-Tabari阿拉伯译文保存；书中事件日期不等同现存抄本纪年，未直接读取原译文或图。星占十二宫第一宫以出生时东方地平交黄道定升点（tale），宫界按不同数学分宫法；黄道等分星座不是同一坐标。技术比较候选：四角宫、三分/九分/十二分细分、月球两交点与七行星组成九曜。作者将九曜的额外两点归于印度实践，仍需原文本和中国中间载体核证；与紫微生年支、月时、十四主星排布没有直接同源证明。不得以四元素三合组类比中国五行三合即认定规则传承。

**中亚实物与佛经翻译。** Pingree 1963 [Isis 54:229–246](https://www.journals.uchicago.edu/doi/10.1086/349703)（DOI 10.1086/349703），[公开文本转录](https://penelope.uchicago.edu/Thayer/E/Journals/ISIS/54/2/Astronomy_and_Astrology_in_India_and_Iran%2A.html) pp240–243提出经佛教传播的nakshatra宿占路线及萨珊/阿拉伯技术汇合。与2004条目同研究者，不作两份独立古证。较有价值的版本学核验入口为创价大学国际佛教学高等研究所2015 [Buddhist Manuscripts from Central Asia: The St. Petersburg Sanskrit Fragments I](https://iriab.soka.ac.jp/content/pdf/stpsf/StPSF%20I%202015%28final%29.pdf)，实际读提取文本前言viii–ix及正文pp1–5（截图index10超时，未核图）。Miyazaki/Nagashima/Tamai/Zhou Liqun, “The Śārdūlakarṇāvadāna from Central Asia”：

- SI 1942圣彼得堡馆藏纸本：作者以字形定为约4世纪，22叶、18cm，前后部分笔迹不同；正文抄录由folio16起，残损及缺字明确标识。Bodleian MS. Sansk.e.23(P), part one 1091(1-8) 的Weber藏片folio7–15来自新疆南缘Kugiār（柯克亚附近），作者依据尺寸、连续叶码和前代校勘提出同一抄本的分藏关系；不是两独立古本投票。BL Or.15010/6,20为另一已刊残片线索，未核实物。抄本时代估计与1963 Pingree所述约500年需并列核验，不武断统一。
- SI 1942 folio16r转录l1–8含二十八宿分类、月与宿相对运行及其他天文词，现仅现代编辑转录；叶36v题记的编辑读法指月与行星占验。此为宿占/历法前史，不能等同后世十二宫命盘或斗数。编辑对梵、藏、汉文本逐行对照，指出部分读法接近竺法护《舍頭諫太子二十八宿經》(T1301)，另列《摩登伽經》(T1300)、T551、T552；需区分短本、天文增广本和后世尼泊尔历法增补。已明确作者及馆号，后续应实查T1300/T1301具体28宿顺序、分类与时间机制，不能用共同故事推断全部术数译传。
- 周利群2013北大博士论文《〈虎耳譬喻经〉与早期来华的印度星占术——基于中亚梵文残本与其他梵藏汉文本的对勘研究》是直接相关研究入口，本轮仅书目线索，未获全文。不得算独立于同作者2015导言的投票。

**11世纪伊朗星学著作与15世纪实物分层。** [Iranica KETĀB AL-TAFHIM](https://www.iranicaonline.org/articles/ketab-al-tafhim/) 已读网页：比鲁尼问答体兼算学、几何、天文学及占星，阿拉伯与波斯文版本具有内容差异，不用任一后世译本代替全体。第一方QDL/BL [Or 8349 馆目PDF](https://www.qdl.qa/download/pdf/81055_vdc_100022596633.0x000001_en.pdf) 提取文本：ff.i+159+ii，最早藏家题记Rajab 839/1436年1–2月，馆方推定抄写不迟于该时间附近；不是作者1029年亲笔本。馆目网页403，94,996,480字节PDF截图index0超限，未实际核阅图像。优先取单叶和具体分宫/星曜段。1920s以前版本及现代译本仍待核。

候选后续查重词（尚未发送）：Pingree、349703、Dorotheus、al-Farrukhan、Thabari/Tabari、al-Biruni/Bīrūnī、Ketab al-tafhim、Or 8349、SI 1942、Sansk.e.23、Or.15010、Śārdūlakarṇāvadāna/Sardulakarnavadana、虎耳譬喻经、摩登伽經、舍頭諫太子二十八宿經、周利群、StPSF。若后续查重命中旧T1300/T1301等记录，复用而非重建，仍需逐条核读。保留TW-OPEN-0059，transmission_impact=NONE，历史广度不终验。


### 12a. 汉译宿占的机制与版本分层：T1300/T1301、初雕高丽藏（2026-11-27）

恢复基线 HEAD `43ca27227951e4983287fd1622d4e62249f46342`、tree `aa1f13801000883392b5b0f0134f47d851533d5a`。六个权威blob均与R2绑定一致；exact-HEAD 20 Actions中19 success、clean-training-system in_progress（首次检查），未触发连续性CI，故依R2回退：实际fetch_blob完整解析六权威JSON，59 OPEN及五P0逐项复核，state 1.1587.0、1499/279、Matrix222、graph819/581，core CLOSED。上一轮R8六候选仍待正式发布。本次未重试已知4MB写入失败，不变动权威数据、query或门禁。完整查询尚未完成；仅根647条及图谱对 T1300/T1301/摩登伽/舍頭諫/舍头谏/虎耳經/K0764/E0069776/1121115280000 作字面检查未命中，分片未查，不得宣告全库去重或新准入。

**文本机制（传世电子转录，不是古叶字形）：** CBETA直连本次仅返回加载界面；实际核阅[《摩登伽經》卷1第五品](https://tripitaka.zensoul.org/T/T1300/1)（CBETA转录，网页75行）、[卷2](https://tripitaka.zensoul.org/T/T1300/2)（37行）与[《舍頭諫經》乾隆藏电子文本](https://www.shidianguji.com/zh/book/QLZ0642/chapter/1k5bafeh6a4nd)（网页82–89、167行，版叶未核）。将月站序位作为暂时对齐工具，并非每一译名/机械值已经确证同一。T1300用中国宿名、以昴为首；另一译本使用名稱、長育、鹿首等译名，同样以28为总数。两文都保留四方各七宿的组织。示例：首宿均记六星，次宿均五星，但第三宿虽同为三星，祭品、主神有差异；第5宿（井/增財）星数2/3；第7宿（柳/不覲）1/5。第20宿牛/無容在各自叙述中为短时月行条目，T1300分条一时、总结半日，T1301六须臾；不能把这些数据先统一再论同源。T1300六宿总结为二日一夜，部分分条只记一日半，存在内部不一致；T1301北德分条35须臾而总结45，悦可在总目但本段未独立描述；须核原叶、校记及梵藏对应，不补写缺文。T1300卷上九曜组合为七曜加罗睺与彗星，绝不直接归并为现代印度罗睺/计都两交点；卷下另有19年7闰、昼夜30分、十二寸表影与月会诸宿，以及七曜运行周期。T1301后段将宿与古国、行业、灾祥相联。两者都可作为宿占及历法知识译传的证据候选，不足以证明以出生时刻安置紫微命宫、十四主星、四化或四柱十神的直接来源；也不因前文使用“六亲”即认定术数六亲。

**译者与实物年代：** [法鼓经录CA0002930](https://authority.dila.edu.tw/catalog/search.php?code=CA0002930) 明列T1301竺法护；大正/CBETA年代范围266–313，高丽目录307–313，原底丽本、宋元明校本，高丽再雕目录板刻1243（思函284），不得混同翻译年代与现存物件。T1300传统题吴竺律炎、支谦；[Kotyk, Astrological Determinism in Indian Buddhism](https://www.academia.edu/38875166/Astrological_Determinism_in_Indian_Buddhism) 检索摘要提出后鸠摩罗什译风及《大唐内典录》求那跋陀罗另一归属，传统230与刘宋候选应并存，本文尚未完整核阅，待核原经录条及论文。不能将T1300传统题署用作230年的技术时间下限。

**东亚版本实物新线索：** 韩国学中央研究院[初雕本舍頭諫晉日太子二十八宿經 E0069776](https://encykorea.aks.ac.kr/Article/E0069776)，金成洙2011撰、2026-03-27更新，明确延世大学中央图书馆藏一轴38张，11世纪初雕版板刻、首张22行其余23行、每行14字，卷首长题及思函、2007-10-24指定宝物；板刻时代不是已独立确认的印刷时间。[韩国国家遗产门户 1121115280000](https://www.heritage.go.kr/heri/cul/culSelectDetail.do?ccbaCpno=1121115280000) 初开返回馆目，复查403，未获原图；[东国大学K0764](https://kabc.dongguk.edu/content/view?dataId=ABC_IT_K0764_T_001&rt=T) 搜索摘要见经号及译者，实开502。初雕/再雕与后世大正转录分别建候选身份，不把馆目、电子经文、同本数字图当成三票。**下一证据**：先追延世初雕卷的公开全幅或再雕对应宿占叶；并行敦煌P.334（馆号待核正，暂仅搜索摘要线索，不作实物认定）、T2149译者目录、T1301梵藏对勘。R9统一查重词增：虎耳經/虎耳经/捨頭諫經/舍頭諫晉日太子二十八宿經/CA0002930/K0764/E0069776/1121115280000/求那跋陀羅/Guṇabhadra/羅睺彗星/摩登伽經說星圖品。继续保留南印度实际方盘、古代十二宫图与技术中介缺环。

本段为受既有发布障碍约束的证据候选保全；无独立古叶实读、未完成全库查重、无新增正式来源或谱系边、无历史裁决。transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12b. 译者归属反证：T2149目录条目边界与梵汉词义对勘（2026-11-27）

基线 HEAD `c48aaad8648d7aa444659a2e1f27404df6ad150c`、tree `771a89e91f4a56db9efebc7f35f8fa2804e1cd85`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity触发。此为同一大对话内“继续”：六权威blob及R1/R2协议SHA均未改变，复用上轮实际完整解析与五P0核阅，不重复注入不可变正文；新HEAD树六绑定一致、最新12a检查点已核。1499/279、1.1587.0、222/222、819/581、59 OPEN五P0、core CLOSED。R8重放已通过但4MB台账发布未解，不再重试；本轮仅候选保全。

**前向修正12a的译者线索，不能以现代论文互引替代经录条目。** 实核 Jeffrey Kotyk, “Iranian Elements in Late-Tang Buddhist Astrology,” Asia Major 30.1 (2017), [中研院史语所PDF](https://www11.ihp.sinica.edu.tw/storage/w2_file/2754DfNUyFU.pdf) 印页27–28（PDF index2–3截图成功）。p28 n17将传统230年归至T2154.55.487c20–24；n18引林屋友次郎1945 p541的译风论；n19引T2149.55.298a18–20为刘宋求那跋陀罗归属。该作者另一篇 [Astrological Determinism in Indian Buddhism](https://www.academia.edu/38875166/Astrological_Determinism_in_Indian_Buddhism) pp152–153提取文本（非原刊页图）再陈述此归属，不能算独立古证。并列林屋“后5世纪末”与求那394–468的实际生年卒年存在时间张力，两者不能互证一个精确译年。

本轮直接核阅[《大唐内典录》卷七乾隆藏K1057电子转录](https://www.shidianguji.com/zh/book/K1057/chapter/1kkt1amtamhir)网页255–267行，以及[台湾大学佛学数位图书馆T2149重排PDF](https://dlbs.liberal.ntu.edu.tw/FULLTEXT/sutra/T/T55n2149.pdf)印页166（PDF index166实际截图，非大正藏原印刷页/古刻），两者都显示条目顺序：舍頭諫經—西晉永嘉竺法護譯；摩登伽經（上二經同本別出）；過去現在因果經—宋時求那跋陀羅於楊都譯。随后太子本起瑞應經另列支謙。此结构下求那归属首先指紧邻《过去现在因果经》，并非明显指《摩登伽经》；现代文献n19存在误读相邻条目的**实质反证**。本轮未取得大正55.298a原版栏图（SAT直链不可访问），尚不得把误引确认为跨版本终审；将求那候选保留为“现代解释受条目反证挑战”，不是古录明确见证。T2149两经同本别出与竺法护永嘉著录仍成立，不受此疑问否定。后续核T2149各版本原图、其它卷独立译者条以及林屋原书、原语词统计。 传统归属亦实查[《开元释教录》卷二QLZ1538转录](https://www.shidianguji.com/zh/book/QLZ1538/chapter/1k5fiypfmv8rp)第14行，记录黄龙二年庚戌及竺律炎四部；同段承认译者名异文。作品原始编成、译本形成、经录编纂、实物版刻与数字转录分别记载。另有T2034/安世高名下同名经候选，当前只见DDB摘要，未核目录原段，不能用作二世纪技术见证。

**可重放的三语义项对照：** 2025 [Translating Medicine Across Cultures: The Divergent Strategies of An Shigao and Dharmarakṣa in Introducing Indian Medical Concepts to China](https://www.mdpi.com/2077-1444/16/7/844)，DOI 10.3390/rel16070844，HTML表6、7及注（实际读取865–881行），以Mukhopadhyaya 1954校本和CBETA T21 1301 p415c26–27 / 1300 p405a20–22比对 pūrvabhādrapadā：梵校本记二星足迹形、30 muhūrta、肉血、Ahirbudhnya神、Jātūkarṇya姓；T1301前賢迹宿记二星相对、30須臾、餅肉、天、生耳；T1300室宿记二星步形、一日一夜、血肉、富單那神、闍罽那。仅就该段，T1300保留步形/血肉，T1301保留30单位且用意译姓氏；在该文所用30 muhūrta=一日的单位合同下，时间值可能等价。不可先把“須臾”视为中国各朝固定48分钟，不可把富單那与Ahirbudhnya自动归同一神，不可因两译本一处更贴近校本就选定整部最古。需要实际梵本/藏译、汉译原叶及译本全篇独立对勘。这提供比“都讲28宿”更严格的同机制、异译与本土化的比较法。该2025论文称T1300匿名并援林屋；与其1945依据不算独立定年。原梵文校本非本轮独立实读。

**下一证据路线：** 扩展R9待查重词至Kotyk/林屋友次郎/異譯經類の研究/善波/摩登伽經の天文暦數について/T2149/大唐內典錄/T2154/開元釋教錄/10.3390/rel16070844/前賢迹宿/闍罽那/Jātūkarṇya。优先核林屋1945 p541、善波1952 pp171–214、T2149大正298a原栏、初雕高丽卷实物；并沿Kotyk p29及后段的T397/T848/T1796/T1299查早期不等宿向等分27宿及12宫并用的实际规则（需与现有已登记材料查重，不能先设传播链）。T1300传统230仍为争议题署，不能作九曜/七曜周制已在230入华的时间下限。保留两体系独立，未获紫微直接来源证明。全库分片查重与正式准入均未完成；transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12c. 唐代宿曜的28/27宿双轨、十二宫分足与日本古写本候选（2026-11-27）

基线HEAD `b6283700b6107a24a7c507a7276d17514d432274`、tree `074170c360cacf9acbd25fcb0af87a378f80fc39`，20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity。六canonical绑定与两协议blob均未改变，同一大对话复用此前完整权威解析及五P0核阅；1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。根647条本次对T1299/宿曜經/宿曜经/宿曜経/Sukuyō/Xiuyao/9789004527256_032/300139069/MD00000266/1881703/IB00060059字面检索零命中，279分片仍待查，不称全库去重。4MB台账发布阻塞依11f保留，六条R8候选已重放未正式准入。

**双轨规则的实际反例（传世CBETA电子转录，非原版栏图）。** [T1299卷上](https://tripitaka.zensoul.org/T/T1299/1) l25–27、39–74、78–141、144–157与[卷下](https://tripitaka.zensoul.org/T/T1299/2) l75–95：卷上序署759史瑶初编、764扬景风修注。上卷宫宿划分用每宿四足，每宫九足，列狮子至蟹十二宫，日月分掌两组六宫，水金火木土依次对称配宫。狮子=星4+张4+翼1，女=翼3+轸4+角2；弓=尾4+箕4+斗1、磨竭=斗3+女4+虚2，牛宿不入这套分足。逐项12宫均9足，合计108=27×4，保留同名“牛宫”与被省略的“牛宿”的不同概念，绝不混为一项。按现代等分几何解释，一足为360/108度=3°20′，一宫30°，但转录原文未在该段写角度值；又明确实际宿有宽狭及前合/并合/随合三种月宿关系，不能把理论分配等同每一实际天区或观测算法。

同一卷上“大唐月建图”月日表却有牛宿，正月初一虚、二十七牛、二十八女、二十九又虚，呈28日周期；二月十五对应翼、十七对应角。卷下明确唐28、西国除牛为27；二月望宿角，十六亢、十七氐；其本命宿简算法对十七日加13=30，27取余3，自角含首顺数第三为氐，且与同卷逐日法一致。**同为二月十七，卷上表角，卷下本命宿氐；** 此为当前电子传本的可复算差异，不等于已证明二者原本均作为同类本命规则，也不直接归责杨景风本人；需核两卷日本/中国实体、表头和用途，保留候选。卷上同样声明天竺二月角月、望宿命名，正月翼月；表内二月十五为翼的冲突需独立检查，不擅改表格或把它套入现代宿曜产品。卷上昴宿正文六星、注中国七星，毕正文五与注八，说明有意保留外来星数与中国星官区别。与紫微的十二地支宫/命身宫及四柱十神不同，不能凭12宫、出生日期或宫主共同结构直接建立传承边。

**版本传承研究的两条互补路线（现代学术，不计原件票）。** Bill M. Mak 2023 [Two 8th-Century CE Recensions of Amoghavajra's Buddhist Astral Compendium](https://brill.com/display/book/9789004527256/BP000031.pdf), DOI 10.1163/9789004527256_032，pp363–368提取正文（PDF index1–3截图403）。作者区分史初稿/杨修订与日本/中国传本的2×2层次；后世合为下/上卷。日本觉胜本序明载两本并存，并用甲辰；大正传本相应段落缺该说明且作玄枵；版本范围限该校勘，未核古叶。作者指出下卷七曜有粟特、中古波斯及梵语音译，上卷修订简化，日月五星可能丢失星期次序；日本本又保有引用718《九执历》的星期计算段落，唐官方历算至佛教术数的具体传递候选。未直接核该公式、唐原本或外语音译原叶。无已知梵文整部底本，不能预设纯印度单源翻译。矢野道雄2016 [《宿曜経》的大蔵経本与和本比较（改正版）](https://icabs.repo.nii.ac.jp/records/367)，刊1:1–11，提取文本pp7–10（截图index8–9报429）：日本写本保存天竺十二宫图/新修十二宫图/二十七宿十二宫图的不同组合，部分图天地朝向相反；现有OCR抽取年代与次序明显不稳定，暂不用作抄本断代或图形实读。两作者引用关系及共同写本须消重；既有现代图像描述不等同古代方盘证据。

**可定位实物候选。** [NDL协作馆目 R000000025-I074640005344994](https://ndlsearch.ndl.go.jp/books/R000000025-I074640005344994) 明载同志社大学藏性然1322年（元亨2）抄《宿曜经》上下两册、23.9×15.5cm、7行17字、朱墨校记和虫损修补；1121宽理训点与1386道快校合识语是不同历史层，不称1121现存抄本。国书DB作品4370388搜索摘要对应DIG-DSSH-50141/BID300139069（正文JS未展开）；[同志社馆方数字入口 MD00000266](https://dgcl.doshisha.ac.jp/digital/collections/MD00000266)实开403，未获图或目标页。与矢野论文抽取文本的1333存在日期冲突，先采用明确馆目1322作为馆目级断代，待核原识语及原刊图，不默改旧论文。[名古屋大学觉胜本 n004-20230901-00308](https://da.adm.thers.ac.jp/item/n004-20230901-00308)馆目摘要含1736年序、无量寿院旧抄本及空海传写推测；不可把1736刊本与传称旧写本视同物件。林屋1945 [NDL pid1881703](https://ndlsearch.ndl.go.jp/books/R100000039-I1881703)核到1945.3、东洋文库论丛30、578页正文；馆方明确注册登录及境外限制，未得p541，不重复账户路线。[INBUDS IB00060059A](https://asvin.dhii.jp/INBUDS/search.php?a=&ekey1=schall&m=sch&uekey=%E6%91%A9%E7%99%BB%E4%BC%BD%E7%B5%8C)核善波周1952-02-01、171–214，仅书目，另有其1956《佛典の天文暦法について》DOI线索待查。

NEXT：优先公开获取同志社1322本卷上月日表及上下卷图、觉胜刊本及七寺/无量寿院原图；核各版本望宿与28/27算法差异、七曜原语/《九执历》实际算例、十二宫图形与功能。R9统一查重增加T1299/宿曜經/宿曜经/宿曜経/Sukuyō/Xiuyao/史瑤/揚景風/楊景風/矢野道雄/9789004527256_032/300139069/MD00000266/DIG-DSSH-50141/1881703/IB00060059/覺勝/九執曆/天竺十二宮圖/新修十二宮圖。图谱及Matrix不改，不声称全文查重、原图实读、完整历史源流或直接紫微传承。transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12d. 九执历的积日算法、算曜直章及日本配本身份纠偏（2026-11-27）

基线HEAD `3f506f03c111eb36eef577e559f03a335f110a47`、tree `939f06efa8d67022d0026119f4e7373f294f273b`。20 Actions中19 success、clean-training-system in_progress，未触发exact-HEAD continuity。六权威blob及两连续性协议未变，同一大对话复用此前完整权威解析及五P0审核；正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。R8六条仍待发布，4MB台账阻塞未解除。本次无全库查重及新准入，不再重复无效上传。

**具体技术传递候选。** 实读[四库本《唐开元占经》卷104电子转录 SK1586](https://www.shidianguji.com/zh/book/SK1586/chapter/1kg3naij1gylk) l13–23，与[另一馆藏转录 NGJ892411999012282111706](https://www.shidianguji.com/zh/book/NGJ892411999012282111706/chapter/1lo8sk7hwibsj) l44–101、205–209。以明庆二年丁巳（657）二月朔为历首，积日及小余算法由年、月、闰月、小月等组成；六十取余从庚申命干支，七取余从荧惑命曜。其后另有中日、中月、高月、定日定月、昼夜刻及宿刻等不同层。两转录可核共同的228、703及60、7除数、每相30度、12相一周及60分一度、十进位空位用点；不是两已核物理原叶。第二转录有“开元二十年甲寅”与甲寅/57年不合，第一转录作开元二年甲寅（714），657至714相差57年；另两转录均将429与169并列而未清楚标出校注层，积日/积月字样也混乱。不擅定完整历算重放，以原叶核对历元、常数、注文字段及从首命数的余0约定为下一步。数学上若沿同一绝对积日、同一起算边界连续推进，两个余数联合重复周期为lcm(60,7)=420日，这是推导，不是该古籍明载七元或证明其他术数同源。紫微出生历日、四柱干支的历史规则仍独立。

矢野道雄2016改正版[原刊PDF](https://icabs.repo.nii.ac.jp/record/367/files/%E7%9F%A2%E9%87%8E%E9%81%93%E9%9B%84%28%E8%A8%82%E6%AD%A3%E7%89%88%29.pdf) l109–119，明确认为杨景风附《算曜直章》大量引自《九执历》，和本保留、传世大陆本早期删去，并提出逆推历元精度可能为删章理由。PDF index4/5截图均429，现为正文提取而非纸页图。删章理由为作者推测，不作确定历史因果。806空海传入说亦需核其请来目录。立命馆ARC [arcBK01-0086 转录](https://www.dh-jac.net/db1/books/alltext.php?enter=berkeley&f1=arcBK01-0086&lang=en) l12–35的目录确有算曜直章条目及附录性质说明，但转录讹字甚多，未定位目标算式原叶。[ARC书志](https://www.dh-jac.net/db1/books/results-detail.php?enter=berkeley&f1=arcBK01-0086&lang=en)明确1736觉胜序、无量寿院藏版，现持有/图像提供字段为立命馆ARC；虽属Berkeley项目界面，不能仅据界面推定原件必在UC Berkeley。未实读原图，不建立直接引用的已验证谱系边。

**12c版本身份纠偏。** [名古屋大学j92完整馆目](https://da.adm.thers.ac.jp/item/n004-20230901-00308) l69–86、96–114、131–160，WB03054425/BB04263873、资料ID10050941/10050942、BID100436698，明确是上下卷不同版的配本：上为享保21年（1736）觉胜序、无量寿院藏版，10行；下为清顺治18年（1661）刊本系统之延宝9年（1681）和刻，8行、有朱笔校勘。馆目出版年统一列1681不能覆盖上卷，1736序不能覆盖下卷，也不能把两册共同视作1736单版见证。原刻及后印具体年代待核，公开manifest为 https://kokusho.nijl.ac.jp/biblio/100436698/manifest 。

[东北大学狩野文库10010000006572](https://touda.tohoku.ac.jp/collection/en/database/library/10010000006572) 为2/3846/2、TT21246837、78幅2021年黑白数字图、注延宝9年；另一馆目[10010000025726](https://touda.tohoku.ac.jp/collection/en/database/library/10010000025726) 同藏号同部门ID，标安政3（1856）无图。两条很可能同物不同记录，须先核刊记，不能作为两件独立见证；1681可为底版而1856为后印候选，不提前定论。[林文库10020000010521](https://touda.tohoku.ac.jp/collection/en/database/library/10020000010521) 林文/659、TT22199835，1681、78幅、地点著录江户（与其他京都记录有别）；[平山文库10020000000226](https://touda.tohoku.ac.jp/collection/en/database/library/10020000000226) MA/162、TT21625577、62幅，未核刊年。均有第一方IIIF入口，狩野manifest打开返回JSON类型但工具未展开canvas，未获图。另[东京大学T30107](https://da.dl.itc.u-tokyo.ac.jp/portal/assets/1cf6a35f-73cd-8598-57ce-f0706cd68972) 四写本合册，首件为宿曜算曜直章相关再计算，另有文化13年（1816）历草稿；后者年代不可直接用于首件写本或唐译断代。公开manifest入口供下一轮核算式，未读原图。

下一步优先目标是100436698配本上卷的算曜直章原叶、林文/659及狩野同号本的原刊记，继而T30107再计算具体算例、九执历原叶常数层。善波周1968《宿曜経の研究》NDL书目I938176、INBUDS IB00016703及网络OCR线索；非此前1952另一篇，暂未完整核读。R9统一查重追加：九執曆/九執歷/九执历/算曜直章/瞿曇悉達/NGJ892411999012282111706/SK1586/100436698/WB03054425/BB04263873/arcBK01-0086/10010000006572/10010000025726/TT21246837/10020000010521/TT22199835/10020000000226/T30107/IB00016703/I938176；全库279分片仍未扫描，不能断言新来源。保留跨文明中介及南印度方盘未决，transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12e. 敦煌P.4071命宫日/身宫机制及《大集经》宿直候选：复用已登记来源（2026-11-27）

基线HEAD `f4d49373187d92f1db07e3f2e03d0e89208d272e`、tree `1b565c3c118f2e83ae0cef191d482d720eb721bc`；20 Actions中19 success、clean-training-system in_progress，未触发exact-HEAD continuity。六权威blob及R1/R2未变，同一大对话复用此前完整解析及五P0核阅。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。R8六候选已通过重放但4MB台账发布仍未解决。T30107馆目[东京大学](https://da.dl.itc.u-tokyo.ac.jp/portal/assets/1cf6a35f-73cd-8598-57ce-f0706cd68972)本轮复核，IIIF返回JSON但未展开canvas；未得算曜直章目标叶，转向高收益且已有实物证据的中间机制，不重复无效获取。

**先纠偏重复登记风险。** 实读既有13ZW研究报告、来源分片（blob 35ba14024d22fd90c948bb5daf37c4dbc2710773）及14S报告/原叶证据JSON（blob 774a44f20abcaa611f6f21fd1401208983d13073）。P.4071并非新发现，原有来源 EXT-TIANWEN-13ZW-BNF-P4071-CATALOG、-GAL-P4071-SUBSTITUTE、-ISAHAYA-LIN-2017、-MAK-2014、-P4071-2025-ABSTRACT 共五条已经登记。14S有四幅替代件图像SHA-256及已核文字。此次根647条对P4071词零命中与分片真实命中并存，明确说明root-only查询不能判新。无新增独立写卷，不重新计数、未升级正式source_page_coverage。

**增加可定位的影印核读。** Mak 2014 [SCIAMVS 15, pp156–163](https://www.sciamvs.org/files/SCIAMVS_15_105-169_Mak.pdf)，实际截图 index51/53/58（印页156/158/163）。p156篇题误作Pelliot 4701，但影印顶部标4071及图注P4071r1，纠正为同一P.4071而非新馆藏。r1见三组出生干支及申时、房日兔、三方主金火月、昼夜48/52刻及月宿行度条目。r3左幅可见“命宫日”小题，紧接氐房宿与天蝎宫的关联；右幅见命宫、天秤宫及十一曜见生图题、覆墨与图/圈疑字。r8左幅题记与馆目所列开宝七年十二月十一日相符。BnF目录经[Biblissima](https://iiif.biblissima.fr/collections/manifest/9517a9fc7bade82688ecdb4a2546a4c287933a88)复核为十世纪14叶，星占f1r–8r，始端残，馆目题记换算975-01-25。Gallica直接入口403，使用已有论文印刷影像作局部复核，不声称取得原件native-resolution、全叶逐字校勘或新数字图SHA；保留14S疑字。

**两项现代研究的机制重构（不是原写卷自带完整算法）。** Isahaya & Lin 2017 [Historia Scientiarum 26(3),153–170](https://www.jstage.jst.go.jp/article/historiascientiarum/26/3/26_153/_pdf/-char/en)，实截图pp157–158,168–169（index4,5,15,16）。作者p168表2按既有Kalinowski研究列28日宿/曜/禽循环，第22项为房日兔；联合60干支日重复周期420日（lcm(28,60)=420）。与12d独立数学推导lcm(7,60)=420数值恰同，但7曜与28宿组合、历元、锚点不完全等同，不能用同周期直接建立算法同一。pp168–169援孔庆典的西夏1047历书和1094积日材料推及符天历660历元，仍为二手研究而非本轮原历书核读。p169根据命宫日段及日值推定天蝎，而按作者软件回算的传统地平升点在双鱼；这是特定历史算例的现代对照，不是我方独立天文重算。论文另区分《聿斯经》的升点义与写卷的命宫日，保留二者不同。

葛业静2025《敦煌遗书开宝七年星命书(P.4071)新探》[作者上传文本](https://www.academia.edu/145350781/)，DOI 10.13584/j.cnki.issn1000-4106.2025.05.006，实际取得HTML正文pp101–102段，不再只是旧摘要；原刊版面尚未取得。作者以房宿直日落天蝎为命宫，对宫金牛为身宫，区别于逢卯安命及太阳宫定命。把卷内数种月位置区分为宿直/天文行度/经文查表候选，指出积日22073和实泛日15873差6200，并以近点月常数解释其可能的运算尝试；原字及单位未完成独立数值复算，不能确认此解释。作者提出翼宿行度可能取自《大集经》、不同年龄运年属于同一盘主及曹延恭身份等，均为论证假说，不作事实升级。其采用的宿—宫边界与《七曜攘灾决》图不同，所举斗宿/井宿映射不宜视为普遍对应。2017与2025重构有相容之处，但依同一写卷及部分前人研究，非两个独立古证。

**实际回查经文的边界。** [CBETA T0397卷42转录](https://deerpark.app/cbeta/T0397/42)与[乾隆藏K0056卷42转录](https://www.shidianguji.com/zh/book/K0056/chapter/1kksgbomhn4lm)检索结果均见九月黑月第九日与翼宿对应；[别行《大乘大方等日藏经》卷8](https://www.shidianguji.com/zh/book/QLZ0058/chapter/1k57oq60x3okl)同段可供比较。只是电子转录同文线索；中国农历九月初九与经文黑月九日的历法转换必须另证，不能仅数字相同即认定康遵直接抄经。另有P.4058v（2025论文引陈于柱）、ИHB.No.5722《谨算》、ИHB.No.8085历书及日本《宿曜御运勘录》对照候选，待核原馆目、具体叶位与作品身份；不把2025复原十一曜图当作写卷保存的原图。

NEXT：优先检查七曜攘灾决各写本宿宫表和聿斯经命宫机制，追查P.4058v、黑水城历书及《宿曜御运勘录》具体原叶；核宿直/实际月位/升点/日月安命/紫微月时安命、身宫对宫/独立安置的区别。R9待查重补T0397/大方等大集經/大乘大方等日藏經/K0056/QLZ0058/日藏分/葛业静/葛業靜/10.13584/j.cnki.issn1000-4106.2025.05.006/P.4058/P4058/ИHB.No.5722/ИHB.No.8085/宿曜御運勘録/符天曆/七元法。既有P4071五条复用，其他词尚未全库核查。本轮仅证据候选追加，不变更源登记/图谱/矩阵，不以现代重构证明紫微或子平祖源，不声称命理预测有效。transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12f. 七曜攘灾决的本命宿双算法、北斗星名映射与宫序差异（2026-11-27）

基线HEAD `74a55aa2ab1415b29a2d626116994e16cb9054a0`、tree `000df9c5f882eda6823625633bed1c922d3a7a7a`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity触发。六权威blob及R1/R2未变，复用同一对话先前完整权威解析及五P0审核；正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。R8六候选重放成功但4MB台账发布受阻。实读13ZW、15CW报告/分片及15FF-R第一分片（blob 83308161f783b939d5d7e1192f9b98fd69bde1ad），复用已登记 EXT-TIANWEN-15FF-R-SAT-T1308、-K1367-XIUYAO、EXT-TIANWEN-13ZW-MAK-2014、EXT-TIANWEN-15CW-KOTYK-2018-JJRS-45-1 等，不把T1308/T1299或日本旧命例重登记；279分片全量查询未完成。

**本命宿的两个传文算法及可执行歧义。** [T1308卷上大正藏p428b电子转录](https://hermit.place/zh-TW/canon/t/t21n1308/juan-01/) l322–330，和[CBETA](https://cbetaonline.dila.edu.tw/T1308)：举十一月二十八日，倍月加日法（已过十月×2+28=48，从室数至心），另一法（13+28=41，从十一月望宿鬼数至斗）；作者自身对两法有保留。实际用标准角至轸宿序（27宿候选排牛）、含首/不含首四组合重算：
```json
[{"n":28,"inclusive":true,"methodA":"房","methodB":"箕"},{"n":28,"inclusive":false,"methodA":"心","methodB":"斗"},{"n":27,"inclusive":true,"methodA":"心","methodB":"斗"},{"n":27,"inclusive":false,"methodA":"尾","methodB":"女"}]
```
两个不同计数合同均能同时重现原例：28宿不含首，或27宿含首。此结果只说明该例不足以判别周长和计数起点；不能用一个示例拟合成唯一古法，不默选现代通行规则。另需闰月处理、其他月份起点、第二例、实际宿名顺序及原叶校记。两法本命宿为心/斗，不是命宫。与12c的T1299上下卷二月十七例互补，证明应保留源文本内多算法，不以宿曜之一式覆盖斗数或子平。

**命宫、十二位和北斗七星的输入与传本层次。** [T1308卷中传世大正转录](https://suttaworld.com/Collection_of_Buddhist/Taisho_Tripitaka/kgin/kgin21/1308-2.htm) l411–438，T21 p452b：先见破军—午日天、武曲—未巳土、廉贞—申辰金、文曲—酉卯木、禄存—戌寅水、巨门—丑亥火、贪狼—子月天；此是十二地支与七曜/北斗星名的对应记载，不是紫微十四主星安星公式。其后另记长保元年三月五日（999）、春分奎三度及重作十二宫图，又述卯时上宫为本命宫的方式。末附1802快道校刊说明、1803慈顺校笔、1820龙肝校写题记，并明言诸本讹误且对考仁和寺本。必须分开唐代作品题署、日本增补/校注、后世版本；相邻长保题记不直接给七星表或安命段定年。该转录两处同名并不证明该技术在865传日时即如此，亦未获仁和寺古本原叶。

卷上l227–271的十二位依序为命、财、兄弟、田宅、男女、僮仆、夫妻、病厄、迁移、官位、福相、祸害；和15CW所核日本天永例十二位主题顺序大体一致（部分名异）。与紫微常见逆布十二宫命、兄弟、夫妻、子女、财帛、疾厄、迁移、交友、官禄、田宅、福德、父母相比，宫名主题多有交集，但宫序、对宫及第十二主题均不同；反向环读仍不相同。不可因“命/夫妻/福德”等名称相似自动建立相同宫位机制。暂不据此改变产品宫序。

**《聿斯经》具体对读。** 实际核 Mak 2014 [SCIAMVS 15 p140](https://www.sciamvs.org/files/SCIAMVS_15_105-169_Mak.pdf) screenshot index35。万民英《星学大成》所收《西天聿斯经》首段以生时太阳所在黄道宫及出生时辰向东方回推命宫；同书《三辰论十二位高下歌》有相近文字；论文另列Dorotheus I.5平行及《明译天文书》1.21直接以东方出地平为命宫。现见为现代校勘与明代传文，不能回填为已获唐译全文，亦不把后出《星学大成》篇章当成独立唐代古证。文中以卯为第一位并逆布地支的解释不同于紫微以生月/时支安命。此为可检验机制比较，不能仅依译名把所有宫/位/黄道星座/地支方位强行同义。

**日本既有见证的复用。** 15CW（blob 826848e042b09b835b5c227411d452996eb33bbf）早已核宫内厅453・2/东大卷908第51号模写本00002468–00002471/00002481–82；出生1113、约1152作勘的命例记廉贞为本命星（生年壬辰），与T1308辰/申对应廉贞的局部映射吻合。1268生约1312作勘者实际题名为《宿曜御運録》，与前检查点推测《宿曜御運勘録》有异，先按既有机构著录题名，后者保留异称候选不另计。实读 Kotyk 2018 [JJRS45/1 pp62–65](https://nirc.nanzan-u.ac.jp/journal/6/article/1472/pdf/download) l811–917，PDF index26/27截图因51.75MB超限；只使用提取文本及15CW已有原页记录，不声称本轮重新获取原页。作者指出天永例取升点为本命宫，文永例取月所在宫；两例使用的命宫定义不同。天永例积日165428、文永例222245均被研究者联系至660符天历历元，和12e敦煌个案形成比较候选；并非单凭相同历元证明直接师承。15CW已核九曜行年规则，不重复登记。

NEXT：追早期T1308写本卷末层次（仁和寺本、宗叡请来目录及早期写本），寻找北斗七星命名与生年支/七曜映射之更早原文、紫微十四星首次明确安法之间的中间证据；比较《宿曜御運録》实际原图与《聿斯经》所载宫位/运限。待查重词追加七曜攘災決/七曜攘災訣/七曜攘灾决/七曜攘灾诀/T1308/宗叡/快道/慈順/龍肝/長保元年/仁和寺/倍月加日/三辰論十二位高下歌/明譯天文書/宿曜運命勘録/宿曜御運録/453・2。已有来源复用，不增加史料计数；新证据未全量查重、原写本未核；transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12g. 北斗七名的隋代地支映射与紫微命主输入转换：12/12精确结构对照（2026-11-27）

基线HEAD `be2f4878f583a23d34c293b835a40a26e187e266`、tree `a92b79236315877c0cf6f2ef259494f85eab5e95`。20 Actions中19成功、clean-training-system in_progress，未触发exact-HEAD continuity。六权威blob和R1/R2未变，复用同一对话先前完整权威解析及五P0核阅。正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。R8预发布通过但4MB ledger发布仍受阻。复用已登记 EXT-TIANWEN-15FF-R-KYOTO-WUXING-DAYI-V4（15FF-R首分片blob 83308161f783b939d5d7e1192f9b98fd69bde1ad）、15CV 757书目及1248卷五馆藏研究、15CW日本命例、15AM/14I/15AT明代安星规则。无全库查重、无新增登记。

**隋代受读层**：实际核[京都大学人文科学研究所《五行大義》卷四](https://www.zinbun.kyoto-u.ac.jp/~takeda/kyoudou/gogyou/gogyoutaigi/gogyo_gogyo_04_g.html) l64，另核[识典对应段](https://www.shidianguji.com/zh/mid-page/7557107645703454758) l8–12。第十六论七政并引四组名称：《合诚图》星官名、《黄帝斗图》七星名及生年属星、《孔子元辰经》阳明等名、《遁甲经》星名；同一北斗星体可以有多组名号，七政也有日月五星、北斗、四方七宿三义。黄帝斗图映射：子贪狼、丑亥巨门、寅戌禄存、卯酉文曲、辰申廉贞、巳未武曲、午破军。作品编成时代、被引佚书时代及现存传本时代分开。15CV古抄本是卷五而非此卷目标段，1248校点题记不可充作卷四原字证明；此次未验卷四古叶。京都转录同段《遁甲经》列水/水土/木土/金木/金土/火土/火，邻接引用层次和复合五行不能直接化约成现代七曜五行。

**精确而不同输入的传承候选**：核[《紫微斗數全書》现代受读全览](https://zh.wikisource.org/zh-hant/紫微斗數全書/全覽) l1251–1259 的安命主/安身主、l1082–1135安身命及南北斗诸星/昌曲/禄存。将廉真规范为廉贞仅用于比对，不抹去原文异写。安命主使用命宫地支，七组顺序及12地支逐一与黄帝斗图完全吻合（12/12）；前者输出命主星名，后者输出生年属星名，不能视为同一输入函数。最小反例：辰年生且命宫子，古生年属星为廉贞、斗数命主为贪狼；若辰年且命宫辰才两者同名。用12×12的纯组合输入遍历，命名匹配数=2×1²+5×2²=22/144（非统计出生分布、非历史概率）。现代十四主星中仅有贪狼、巨门、廉贞、武曲、破军五项；禄存按年干、文曲按时支独立安置。十四主星家族的其他九主星、左辅右弼须另追。不要把命主选择与该星在盘内的落宫混为一谈；以安命主段的午宫例和子宫例核实其需另查该星落宫。明确此为较强结构连续性候选，尚无跨代引用或改造过程证据，不宣告直传。15AM/14I/15AT已证明1581捷览家族现代受读五局生日安紫微与1607续道藏年支安紫微不同；本轮不重复发现、不将受读全览的安命主段提前认定为1581实物文字，需核具体明版目标叶。

**宗教语境的并行见证**：[SAT T1307 425c6–426a14、426b15–16](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&s=&useid=1307_,01) 与[CBETA转录](https://deerpark.app/cbeta/T1307) 见相同生年分组、七星按序对应七佛，另有星符和禄食；是宗教本命星体系，不是十四主星盘。[法鼓经录CA0000283](https://authority.dila.edu.tw/catalog/search.php?code=CA0000283) 明列底本长谷寺本享和二年刊（1802）；目录907时代标记与传本题“唐朝受持”不能合成精确唐代首证，卷末快道序与慈顺校笔须另分层。[《雲笈七籤》卷二十五受读](https://www.shidianguji.com/zh/book/HY1734/chapter/1mbco01ze21wp) l114–134见七名及辅弼、对应阳明至天关的宗教名号，反映另一用途，未核早刻原页。[邱博舜2006《貪狼諸詞來歷初探》](https://libap.nhu.edu.tw/citesys/jnPaperDetail.aspx?pID=5965)仅实读机构摘要，作者提出词语早见而七星组在汉后隋前形成、后应用于风水等；不能把作者推断当已独立证明的首次年代。

**新的跨地域调查入口**：Chenxue Liang 2025, Religions 16(12):1555, DOI 10.3390/rel16121555，[机构保存原刊PDF](https://lib.shnu.edu.cn/_upload/article/files/eb/14/617c576647a4a9887b83540f0970/f5e09516-303a-43a0-9407-1450f4b7d606.pdf)，实际截图index0和10（印页1、11），提取pp15–16。作者将日本属星祭的年支映射与隋代引文联系，分层考察P.2675V（861）/P.2675bis（924）食物礼俗、S.2404与S.612、T1311《梵天火羅九曜》之葛仙公礼北斗法、九至十世纪日本本命祭。T1311传统一行题署被学者质疑，文中转述Kotyk九世纪中叶候选，非本轮独立定年。pp15–16记村上天皇本命供论议：阴阳道按生年干支丙戌、宿曜道按生日干支丁亥，另有947年仪文保存在T2473与T2409，既取属星也取本命宿。均为现代学术导航，未取上述敦煌实物/仪文原页。后续应检查仪文日期、两种本命日算法和具体北斗星名是否确证；不要把祭祀信仰当预测效力证据。15CW已有1113出生例壬辰属廉贞，同本命年支映射可对读但不是新原图核读。

NEXT：优先取得早期明刻命主段原页及更早的可断代中介文本，分开七星宗教名号、七曜映射、命主及盘内主星/辅星安置，再沿十四主星其他九项追查紫微/天府等来源；R9查重补黃帝斗圖/黄帝斗图/孔子元辰經/五行大義/貪狼諸詞來歷初探/邱博舜/T1307/CA0000283/雲笈七籤/10.3390/rel16121555/Chenxue Liang/属星祭/屬星祭/P.2675V/P.2675bis/S.2404/S.612/T1311/梵天火羅九曜/T2473/T2409。既有相关来源应复用，全库279分片查重仍待完成；不增正式计数，不建立确证谱系边、不变Matrix及排盘。transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12h. 南斗星官、六司神名与十四主星分组：五名重合及断代反证（2026-11-27）

基线HEAD `86930c23638fab799948031c9bf16e3e620a726d`、tree `b69786fda9d6913352a6dc5eb53bb7bc6bf171d0`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity。六权威blob及R1/R2不变，同一对话复用此前完整解析及五P0复核。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。R8六候选已预发布重放，4MB台账远端写入受阻。实读15AM、14I、15AT、15CV及15FF-R首分片，复用已有斗数原页证据及五行大义材料，不重复登记。根647条针对南斗六司/南斗經/南斗经/施秦生/DAO14_05/中書000059/1kg3n86pw58v6/五斗經的字面命中数 0；命中ID []；279分片未全查，不能断言新来源。

**天文名称层。** [《晋书斠注》卷11](https://zh.wikisource.org/wiki/晉書斠注/卷011)及[CTEXT对应段](https://ctext.org/wiki.pl?chapter=861218&if=gb)传文：南斗六星按南二/中二/北二分三组，分别天梁/天相/天府庭；南斗又称天机，注引《太平御览》有天厨庭异读。实际核[四库本《开元占经》卷61](https://www.shidianguji.com/zh/book/SK1586/chapter/1kg3n86pw58v6) l14，引《北官候》以天府、天关、天机、天同为南斗相关别名，并将二星组称天府廷、相、天梁；又引多家军国占、爵禄、寿命、分野义。北二为庭/廷、相/天相等异文、别名与组名均分别保留。古代作者引书或唐修晋史的时间不能直接下推至晋代或更早特定星名原页；未取目标原刊。天文中的二星组、整个星官的别称与命盘独立星位不是同一对象。

**南斗六司层与可定位实物。** [道教文化中心书目](https://zh.daoinfo.org/index.php?title=太上說南斗六司延壽度人妙經)注明正统道藏洞神部本文类伤字号、涵芬楼341、提要618；[台北故宫实物目录1578](https://digitalarchive.npm.gov.tw/Collection/Detail/1578?dep=P) l15–51，物号中書000059N000000000、王道化康熙52年1713楷书册、十六开三十幅，官方释文明确六司顺序：天府/天相/天梁/天同/天枢/天机；相应主司为司命、司录、延寿、益算、度厄、上生。馆方提供CC0低阶图、CC BY4.0中阶图与IIIF入口，本轮只实读馆目及释文，未核特定图页。天枢尊号含文昌，不能径作斗数文昌安星规则。南斗六司名单与斗数常见南斗六星集合（天府、天机、天同、天相、天梁、七杀）交集五项；六司无七杀，斗数南斗六星集合不含天枢。五名共同不足以说明天枢被七杀直接取代。北斗七名与此六司也不是十四主星的两个布列序列。

**断代反证**：施秦生2022《五斗經》成書年代及作者新考，[香港中文大学期刊PDF](https://dao.crs.cuhk.edu.hk/Main/wp-content/uploads/2022/09/DAO14_05_%E6%96%BD%E7%A7%A6%E7%94%9F.pdf)，实读印页181及183截图（index36、38）并读正文末段。作者指出南宋吕元素《道门定制》卷三的六司位号紧接小字说明出于南斗经、其余依旧例；据其校订体例提出这些神名是吕氏补入王钦若大中祥符年间《罗天醮仪》旧材料的解释。故不可直接以旧仪年代定六司经文年代。论文也辨析《皇宋通鉴长编纪事本末》南斗经与《宋史》星经异文，认为不足支持太宗朝已有此南斗经。其整组五斗经形成假说为1015–1074，或进一步限1067–1074，成都玉局观李垂英等道士候选；属现代研究判断，不是已核宋原本或独立确定首证。需核《道门定制》31册680中、653下及赵抃《成都古今集记》、贾善翔《猶龍傳》对应原页。1713册不是宋初原物。

**十四主星的实际机械分组。** 实读[《紫微斗數全書》现代受读卷二](https://zh.wikisource.org/zh-hant/紫微斗數全書/全覽) l1082–1134、1251–1259。按地支顺行为正方向，紫微系偏移[0,-1,-3,-4,-5,-8]对应紫微/天机/太阳/武曲/天同/廉贞；天府系偏移[0,1,2,3,4,5,6,10]对应天府/太阴/贪狼/巨门/天相/天梁/七杀/破军。该受读文本呈6+8计算结构，不可把宗教的北斗七、南斗六或天文实际星体视作排盘直接分组。依既有15AM金四局初三例紫微丑、天府卯，重放：紫微丑/天机子/太阳戌/武曲酉/天同申/廉贞巳；天府卯/太阴辰/贪狼巳/巨门午/天相未/天梁申/七杀酉/破军丑。按古诀组合推得，不代表新核1581古叶或全盘。补身主原文：子午火铃星（保留传文疑异，不能直接纠成现代火星或铃星）、丑未天相、寅申天梁、卯酉天同、辰戌文昌、巳亥天机，输入生年支，与命主命宫支及南斗六司排序不同。此为下轮核原刻异文的独立任务，不改现有确定性实现。

紫微名称层以[《史记·天官书》传文](https://ja.wikisource.org/wiki/史記/卷027)中宫天极及紫宫作更早背景候选，不将紫宫整体等同斗数紫微单星；太阳/太阴为日月名称背景，具体斗数定位从星系偏移、非实测黄经，仍需追形成中介。七杀名称未在本轮南斗古文中获得独立前史证据，八字偏官七杀/其他神煞同名也不可自动并入。余九星目前五项南斗名号比较、三项紫微/日月背景及一项七杀待查，不等于九星来源已定。

NEXT：核早期《道门定制》《南斗经》及故宫1713册目标图页，追天枢/七杀差别和北斗、南斗、十四主星分组中介；紫微垣与帝星、日月虚拟落位、七杀在早期星命/禄命中的不同义项；早期明刻〈安南北斗诸星〉及〈安身主〉原页。R9待查重追加南斗六司/南斗經/南斗经/道門定制/羅天醮儀/施秦生/DAO14_05/五斗經/中書000059/中书000059/1kg3n86pw58v6/天府庭/天府廷/天廚庭/李垂英/成都古今集記/猶龍傳/玉局觀/天樞度厄/安身主。全库查重未完、无新正式登记、无确证直传边、无Matrix或产品改变。transmission_impact=NONE，TW-OPEN-0059保持OPEN，不终验。


### 12i. 七杀同名异义、日月虚拟布位及三命/五星并存的中间证据（2026-11-27）

基线HEAD `ec34490fcef41723b7677312a8f9ba531b72d3d7`、tree `76c6e9f5739bf02090b7da1e2d91588e9ed6e4bb`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity触发。六权威blob及R1/R2未变，同一对话复用此前完整权威解析及五P0核阅。正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。R8六候选已重放而4MB台账发布仍受阻。本轮根647条对濟度金書/济度金书/DZ0466/S.3326/S3326/Bonnet-Bidaud/洞微大限/bcb3335f94e0a0edc5f492f08e2c4a83字面检索命中 0 条（[]）；279分片未全查，不宣告无重复。复用15AM/14I/15AT、15FF-R及13ZW/14S已登记受读、原页及P4071证据。

**七杀三义，不擅定祖源。** [《紫微斗數全書》卷一受读](https://zh.wikisource.org/zh-hant/紫微斗數全書/卷一)及[识典《新鋟希夷陳先生紫微斗數全書》对应段7356346219947458598](https://www.shidianguji.com/zh/mid-page/7356346219947458598) l9，七杀为南斗第六、火金、斗中上将；后者为另一电子转录，未见影像及书志，不能独立确定明版刊年或最早出现。对照[《三命通會》四库本卷5](https://zh.wikisource.org/zh-hant/三命通會_(四庫全書本)/卷05) l177，七煞/偏官以甲庚、乙辛的隔七相克及制伏区别为义；与斗数天府系固定偏移的计算类型不同。[《靈寶領教濟度金書》卷320](https://www.shidianguji.com/zh/book/DZ0466/chapter/1lp2905ukcu80) l51另列七杀于安宅凶方神杀名目，与岁破、劫杀等并列，本段没有七杀单项定位公式，不从名目推断具体规则。三种语境分别登记候选；12h的南斗六司名单无七杀，当前搜索尚无足以确认更早南斗第六星名为七杀的独立证据。不是证明早期不存在，也不以共同武职、权威语义证明命理借用。四柱七杀不改动，紫微七杀亦不重开。

**三命与五星同卷并存的具体技术桥（受读层，非宋元原叶）。** 上述DZ0466卷320 l51将三命和五星分别列操作程序，又要求法师二者兼备。三命：阳男阴女至未来节、阴男阳女至过去节；三日一岁、三时一月，原例七日三时折二岁五月（7×4+1=29月），生月甲戌顺行乙亥→丙子→丁丑、逆行癸酉→壬申→辛未，分别二岁五月、十二岁五月、二十二岁五月。小运男一岁丙寅顺、女一岁壬申逆。此为传统三命规则可复算例，时为传统时辰，非现代小时；七日令三时等转录异字待核，不以该例决定所有分秒边界。五星：官历查出生太阳宿度/宫，自此宫按生时顺数至卯安命，官历查出生太阴宿度/宫安身；十二黄道宫按日月五星配属，洞微大限与小限/飞限、竹罗限等九种限法并列。其中洞微大限以命宫起，16、26、37、52、60、67、78为文中不同过宫年龄节点；不能与斗数每宫十年的大限等同。五星安身以太阴宫定位，与12e敦煌对宫说、12f日本命宫定义及15AT斗数月时安身均须分开。此为同卷两技术并用的直接受读证据，而非紫微由三命/五星混成的定论。[道教文化中心书目](https://zh.daoinfo.org/index.php?title=靈寶領教濟度金書&variant=zh-hant)明确南宋甯全真授、宋末元初林灵真编，原书据考仅12卷、正统道藏扩至320卷及目录，含元明增修；故卷320术文不能不经版本分层就标为南宋或林氏原作。下一步定位涵芬楼第263册及正统道藏邇字号目标叶、早期十二卷本与周思得后编对应段。

**紫微、日月的天文层反证。** [《晋书斠注》卷11](https://zh.wikisource.org/zh-hant/晉書斠注/卷011)传文区分紫宫垣十五星（又称紫微，帝座/宫垣意象）、北极五星、钩陈与天皇大帝；不是紫微单一恒星的坐标。实查英国图书馆[IDP S.3326馆目](https://idp.bl.uk/collection/7861395E5F814419BA05483EAB254832/) l27–67，日期字段649–684、说明文字又称可能8世纪初，保留其内在断代张力。Bonnet-Bidaud等2009[原刊PDF](https://www.epfl.ch/labs/lastro/wp-content/uploads/2018/07/Annexe-05-Bonnet-Bidaud_et_al_2009_DunhuangStarAtlas.pdf) 实截图index6/7/9（印页45、46、48），p46 Fig4为同一敦煌星图第13幅北极投影的论文印刷图，图中实际星点、线及星官题字可见，p48 Table3为现代拟合，非原图数字替身。p50–51正文作者以避讳字、书写与天文等证据提出649–684，未做碳14测年，星图天象时代与月令文本时代分离；未获取native图或逐字核校，不把论文印刷图当新物理见证。实际星图的极区坐标和星群结构不等于斗数十二地支环。古代紫微垣、北极星、帝星及现代极星不能互换。

**机械检验：固定安日月不等同天文黄经。** 实读[《捷覽》现代受读](https://shixingji.club/public/ziweidoushujielan) l279–311，复用15AM已登记金四局初三/初八及紫府斜对例、12h布星序列。取子=0至亥=11，紫微宫z，天府f=(4-z) mod12，太阳s=(z-3) mod12，太阴m=(f+1) mod12，则(m-s) mod12=(8-2z) mod12。实际枚举12个z仅得六种偶数宫差0/2/4/6/8/10（每种2次），而不是天文黄经连续变化；这里的宫差不是角度观测，不能将0当真实朔、6当真实望。初三金四局紫微丑、天府卯、太阳戌、太阴辰；初八同局紫微卯、天府丑、太阳子、太阴寅。两例机械差由6变2，非真实日月相位复算。对应原文按局生日安紫微及固定相对位置，不输入官历日月宿度；对照DZ0466五星术以官历定太阳太阴，存在实质计算差异。此为当前传文函数的可证数学性质，不是断定何时发生历史改造；1581《捷览》原刻目标图尚未获取，不以现代点校确定首证。

补充候选：2019《中国科技史杂志》40(2):146–160 [《传世著作〈星命溯源〉与五代至明中国星命术的发展》摘要](https://zgks.cbpt.cnki.net/portal/journal/portal/client/paper/bcb3335f94e0a0edc5f492f08e2c4a83)，作者区分托名张果五卷的多时期编者，研究十二宫、二十八宿五行化及神煞交融，只有公开摘要，待查既有登记及公开原刊；不由张果题署断唐代。NEXT：核DZ0466卷320旧本、洞微限具体历代文本、子平大运原例及五星命身宫中介；沿七杀早期同名义项与十四主星明刻原图继续，补星曜从天文坐标到固定布位的实际历史缺环。待查重追加濟度金書/济度金书/DZ0466/甯全真/林靈真/洞微大限/竹羅限/七煞/七殺南斗第六/7356346219947458598/S.3326/Or.8210/S.3326/Bonnet-Bidaud/Praderie/Whitfield/星命溯源/bcb3335f94e0a0edc5f492f08e2c4a83。全库查重和新证据正式准入仍待完成，transmission_impact=NONE，TW-OPEN-0059保持OPEN，不改正式来源/Matrix/graph/排盘，不终验。


### 12j. 星命溯源的编纂层与洞微百六限的实数重放（2026-11-27）

基线HEAD `a27b4e84d6995283960c827b5b92320d409e7525`、tree `1547c8a7a98c17a282f56ccc25033d559d6b6ffc`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity。六权威blob及R1/R2未变，同一大对话复用此前完整解析及五P0核阅；1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。R8预发布重放成功但4MB台账发布受阻；本轮未找到已经验证、合规且不改变工作流权限的新发布通道，不重复上传或宣称完成。根647条对星命溯源/宋神秘/洞微百六/645726/BA54006682/1206554/bcb3335f94e0a0edc5f492f08e2c4a83字面检索命中 0（[]），279分片未完成全量查询；不据根检索认定新增。

**编纂史分层。** 实读[《星命溯源》四库提要](https://zh.wikisource.org/zh-hant/星命溯源_(四庫全書本)) l110–123，提要署乾隆46年十二月（1781纪年）。卷1《通元遗书》杂录托名张果，卷2《果憕问答》称明李憕嘉靖2年九月遇张果，卷3《元妙经解》题张果撰、郑希诚注，卷4《观星要诀》及卷5《观星心传口诀补遗》不明作者；提要自身推断郑氏编卷4、后人增卷5。不能把卷2神异叙事作唐代成书证据，也不能把提要编者对李虚中不取时的理解当作已终裁的八字史实。宋神秘2019《中国科技史杂志》40(2):146–160，[期刊摘要](https://zgks.cbpt.cnki.net/portal/journal/portal/client/paper/bcb3335f94e0a0edc5f492f08e2c4a83)及[转载引言](https://m.fx361.com/news/2019/1111/15517744.html) l14–24：作者提出五代至宋术士、元末明初郑希诚及明李澄等多层编纂，宫宿五行化及三阶段/流派、神煞与八字交融。摘要作李澄、提要传文作李憕，需核原卷自署及现代作者的具体辨证；不预先等同或拆为两人。转载全文需登录APP，未取得原刊全篇，不能以摘要复述为三个阶段的具体技术史结论。新增可定位[台北国图联合馆目](https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=1&item=baf8bbe2f2144cd582796ceccfd8d8d3fDE0MDAxOA2.6xAL1H0xrIma1pYP47x8vmVpgmAWbp9ZE5r39F8H6bs_)、[数字典藏联合目录1206554](https://catalog.digitalarchives.tw/item/00/12/69/1a.html)同指故宫藏乾隆间写文渊阁本候选；非两件独立物。CiNii BA54006682为1930年代商务《四库全书珍本》另载体，CTEXT library res6840为影印入口；仅检索馆目/入口，未核影印原叶身份。已有13ZW提要引用应先复用。

**洞微大限：起年年龄节点与时长分开。** 实读[《星學大成》四库本卷7](https://zh.wikisource.org/wiki/星學大成_(四庫全書本)/卷07) l111–163，题明万民英撰，〈洞微百六限起例〉总100年6月。按命15、相貌10、福德11、官禄15、迁移8、疾厄7、妻妾11、奴仆/田宅/男女各4.5、财帛/兄弟各5相加=100.5年。前七宫若以一岁为起点、半开边界，实际重放：
```json
[{"n":"命","d":15,"start":1,"next":16},{"n":"相貌","d":10,"start":16,"next":26},{"n":"福德","d":11,"start":26,"next":37},{"n":"官禄","d":15,"start":37,"next":52},{"n":"迁移","d":8,"start":52,"next":60},{"n":"疾厄","d":7,"start":60,"next":67},{"n":"妻妾","d":11,"start":67,"next":78}]
```
与[《灵宝领教济度金书》卷320](https://www.shidianguji.com/zh/book/DZ0466/chapter/1lp2905ukcu80) l51所列16、26、37、52、60、67、78节点完全一致。这里16等为进入下一宫年龄标签，非前宫年数；星学大成的逐宫正文还明确官禄37入51出、迁移52入59出、疾厄60入66出。尚未核清奴仆、田宅、男女、兄弟、财帛的精确布宫顺序、半岁单位和真实生日/虚岁换界，不以总数吻合补全未知。两书受读规则的前七宫数值匹配是具体结构关联候选；不自动认定直接抄袭、同一版本或历史最早年代。五代至明作者归属与卷320后增风险继续保留。CTEXT卷7 chapter645726检索片段相符但直接打开403，不能算独立原本。

**独立运限算法的比较。** 洞微小限按一岁命宫逆行一年一宫；洞微飞限进入大限宫后前两年本宫、第三四年对宫、再按阴阳宫取三合等（原文后段与例需另重放）；洞微大限不是均匀十年。四柱大运由生月干支、节距及顺逆控制，紫微十四主星家族大限由命宫/局数/方向控制、每宫十年，均不同于此。比较范围只限规则输入、宫序及年龄边界，不主张预测有效。12i中同卷三命五星并用支持技术共存但不能单凭十年、神煞或术语证明同源。下一步追万民英〈星家源流〉、〈洞微百六限〉及《果老星宗》相应原刻，继续考证宫宿五行化和命身宫变化，并核独立运限体系的边界。R9待查重补宋神秘/星命溯源/果憕問答/李憕/李澄/通元遺書/元妙經解/鄭希誠/觀星要訣/BA54006682/1206554/res=6840/645726/洞微百六限/星學大成/星学大成/百六限/相貌宮。未取得原刊/古叶、未完成全库查重与正式准入；transmission_impact=NONE，TW-OPEN-0059保持OPEN，正式统计、Matrix、图谱与产品不变，不终验。


### 12k. 晚明星平汇编的数字载体定位、宫度双主及十干官星映射（2026-11-27）

基线HEAD `836c2f0305c81c9ebec6c05cbb0bf49262dbc132`、tree `977475a24c62973aeb42630812eb0f040fc52b94`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity。六权威blob及两协议不变，同一大对话复用此前完整解析及五P0核阅；正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。R8六候选已重放而4MB台账发布受阻，未找到经验证的替代发布路径。实读14R/15I/15BZ/15CH旧报告及14R来源分片，复用 EXT-TIANWEN-14R-NCL-HARVARD-XINGPING-ZONGHUI-1611 等既有来源。不将原已登记馆目、宫度分判、十干变曜作为新发现或重计。

**1611本数字载体已定位，不等于已读目标叶。** [台湾国图联合馆目](https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=1&item=ec7c6e87db3e450682730b956929836cfDkzNzYy0.iNUyTPtdmCRvYQ3Zuup7vvP8dhcjbhMJtIukIkRL8uc_)与[Commons六册入口](https://commons.wikimedia.org/wiki/Category:新刻星平總會命海全編)、[首册元数据](https://commons.wikimedia.org/wiki/File:Harvard_drs_53263996_新刻星平總會命海全編_v.1序、卷之首.pdf)相互定位：十卷首一卷，明万历辛亥1611积善堂陈奇泉刊，薛承爱遗稿、夏从仁编汇。数字对象DRS53263996、Alma990077551100203941；六册PDF共80+61+60+68+54+114=437个数字页（非437古叶），首册92,160,969字节，Commons公布SHA-1 c82b096e658b031b3a0e195cf3875cd25dc116e5（非本轮自行计算）。元数据记15行31字、白口单鱼尾、四周单边、框高21.8×12.4cm、2000年35mm缩微胶片，故数字图可能源于胶片而非直接彩色拍摄。Harvard [manifest](https://iiif.lib.harvard.edu/manifests/view/drs:53263996)及[Alma馆目](https://id.lib.harvard.edu/alma/990077551100203941/catalog)直开403；本轮未得目标原叶，不授原字权威。六册是同一馆藏书的数字分件，非六件独立古证。14R区分1877《增补星平会海》与1611《星平总会》，继续保持。

**编汇的明确自述与实际技术混合。** [识典HY1442卷首转录](https://www.shidianguji.com/zh/book/HY1442/chapter/1koboy2q7bbws) l6–7署万历辛亥冬、武夷夏青山、积善堂陈奇泉，序列三辰通载、五星子平、琴堂、果老、灵台等多家，并列子平、景纯、鬼谷等，说明删繁订讹及重增秘旨。可确认受读文本的编汇意图，不能从书目串自动划分每个标题、师承或实际引用祖本。l24–28同一卷首中，星命术既有宫主科甲星，也以生年十干配科名星（甲乙木、丙丁火、戊己土、庚辛金、壬癸水）；人马宫之对宫取水曜为科甲星，说明科名与科甲两个不同输入，勿与斗数化科等同。官星段解释甲干取辛为官，再从辛所属禄曜取紫炁；结合15BZ十干变曜表（甲火乙孛丙木丁金戊土己月庚水辛炁壬计癸罗）可作明确的复合映射候选：甲→辛→炁、乙→庚→水、丙→癸→罗、丁→壬→计。与卷首歌诀前四项一致；其余六项及原版讹字未校，暂不补成全表。此处借用干克/阴阳的官关系再投射到星曜，是术语与操作并用的证据，不等于子平十神直接来源或两术成为同一计算函数。星命星曜须另有位置输入，紫微四化使用另一组星曜与分类，复用15BZ反证。

**宫度双主的不同优先级，及四时五行。** [《古今图书集成》艺术典574卷](https://zh.wikisource.org/zh/欽定古今圖書集成/博物彙編/藝術典/第574卷) l155–215《张果星宗八》〈观星要诀〉以宫主、度主、身主为三主，并以春木、夏火、秋金、冬水、四季月土及节气分时；另分昼夜及五星迟留伏逆。 [576卷《张果星宗十》](https://zh.wikisource.org/zh-hans/欽定古今图书集成/博物汇编/艺术典/第576卷) l146–183具体例子宫虚日度：土为宫主、日为度主，三主优先序为身/度/宫，昼生重命度主、夜生重身度主；生我为恩、克我为难，仍须看季节与其他曜的制约。与15CH旧登记丑宫牛度、寅宫尾度双主相反作用对读，新增的是另一文本的优先序候选和季节输入，不假定跨著作统一优先级。四库总目卷111 [《吕氏摘金歌》《五曜源流》《五星考》《星平会海》相邻条目](https://zh.wikisource.org/zh-hant/四庫全書總目提要/卷111) l532–553则称立命宫所躔度最重、命主次、度主再次、身主又次；与张果星宗明确不一致，须保留批评者与原作者语境，不合成新诀。《五曜源流》虽以五曜命名却专论子平，以日干为主；《五星考》则为宫度及星曜神煞，另有单宿内分段五行异例；清提要认为星平会海取多家且有不合。此为后世目录评价，不作为预测有效性统计或早期作者定论。

NLC892-411999021002-92857《古今图书集成》第3153册[PDF](https://upload.wikimedia.org/wikipedia/commons/e/e8/NLC892-411999021002-92857_%E6%AC%BD%E5%AE%9A%E5%8F%A4%E4%BB%8A%E5%9C%96%E6%9B%B8%E9%9B%86%E6%88%90_%E7%AC%AC3153%E5%86%8A.pdf)提取文本632–650含目标段，截图index10因20737671字节超限失败；OCR作月日行十二度等与维基十三度异，不能视为原页校勘，不更正或选定。优先取得单页高清图，核三主次序及月行数值。此后出汇编并非张果亲著唐本或原始果老星宗独立原刊。

NEXT：哈佛DRS53263996首册序及官星、科名、科甲目标叶；卷六/七子平段与五星段的具体对照；《五曜源流》《五星考》独立书目与目标原页；十干映射的剩余六干及紫微化科语义对照。R9查重补DRS53263996/990077551100203941/新刻星平總會命海全編/HY1442/積善堂/陳奇泉/夏青山/薛承愛/五曜源流/五星考/呂氏摘金歌/宮度主論/觀星要訣/科甲星/科名星/藝術典574/藝術典576/411999021002-92857；既有14R馆目等继续复用，未全库查重、未正式准入，不增计数。transmission_impact=NONE，TW-OPEN-0059保持OPEN，正式Matrix/graph/产品不变，不终验。


### 12l. 星平官星十干全映射重放与集成单页影像复核（2026-11-27）

新大对话独立恢复HEAD `e53bb7eb8df8c5b687124c2582589396e8863bb3`、tree `9f4789d9f2f075e74ea8d4a180e37787f0e6c983`。20 Actions中19 success、clean-training-system in_progress、无exact-HEAD continuity；R2六绑定吻合但未启用快路径，直接读取并解析六权威blob（普通state读取为空），复核五P0及TW-OPEN-0059，state 1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。279分片manifest与tree blob逐项比对零不符、source_count合计852，根647条相关词命中4条（含既有EXT-WIKISOURCE-XINGXUE-DACHENG-TIANCHU）；未遍历所有分片正文，不作无重复声明。实读15BZ及14R来源分片、12QD最新Matrix报告，复用已登记卷568/卷一和1611馆目，不增计数。R8台账发布阻塞未解除，本段仅追加现有研究检查点，不改权威JSON。

**十干正官到星曜的复合规则。** 实读[《星學大成》四库本卷一〈論官星〉](https://zh.wikisource.org/zh-hant/星學大成_(四庫全書本)/卷01)及[《古今圖書集成》艺术典568卷数字页31](https://zh.wikisource.org/wiki/Page:Gujin_Tushu_Jicheng,_Volume_468_(1700-1725).djvu/31) l179–183，均以甲之官辛、辛之禄炁解释对禄。以15BZ十干天元禄序为映射L、阴阳相异的克我干为G，官星F=L(G)，工具层实际枚举十项：
```json
[["甲","辛","炁"],["乙","庚","水"],["丙","癸","羅"],["丁","壬","計"],["戊","乙","孛"],["己","甲","火"],["庚","丁","金"],["辛","丙","木"],["壬","己","月"],["癸","戊","土"]]
```
与星学大成受读官星歌十项10/10一致，集成受读以月代阴，属语境可解释的名称差异。识典[HY1442卷首](https://www.shidianguji.com/zh/book/HY1442/chapter/1koboy2q7bbws) l25–26戊项作攙倉且壬癸末句缺失、注文炁转录为无，不能据其他版本补写成1611原刻已证；本表验证的是明确受读规则，不是该原叶的十项字形。全表完成为12k四项机械重放的扩展。官星、催官、科名、科甲与十变曜天元禄为不同函数；例如甲的官星炁、催官金、科名木、天元禄火，科甲另需命宫对宫。不能合称紫微化科或子平正官星。

**已有扫描索引的正面影像复核。** 实开[卷568数字页31的单页图](https://thumb.wikimedia.org/wikipedia/commons/thumb/9/97/Gujin_Tushu_Jicheng%2C_Volume_468_%281700-1725%29.djvu/page31-1920px-Gujin_Tushu_Jicheng%2C_Volume_468_%281700-1725%29.djvu.jpg)，返回可见三栏版面及中栏左侧官星段，能辨官星标题、首对甲炁乙水、末部壬月癸土及甲辛取炁的注文结构。限显示分辨率的目标段目视，未做native逐字校勘或图像哈希；不强判戊句末字及全部小字。[Commons数字文件元数据](https://commons.wikimedia.org/wiki/File:Gujin_Tushu_Jicheng,_Volume_468_(1700-1725).djvu)注明123页、18.21MB、2016-10-17上传、来源为百度网盘而非明确馆藏原件。作品1700–1725编纂日期不能视为该扫描物理印本年代。15BZ已登记这一数字载体及卷次对应，故此为原有候选入口的目标段视觉复核，不是新增独立古本。清代汇编所收文本关系仍待明本校勘。

**同书两种参照系。** [HY1442卷七子平取格段（网页题卷八）](https://www.shidianguji.com/zh/book/HY1442/chapter/1kobozbi23jms) l5–9以日干、月令、财官印伤食煞取格，甲日酉月取官格，乙日申月取官格；卷首官星则以生年干经G及L选曜，再结合星曜宫度与运行状态。甲日酉月和甲年炁为不同条件/输出，不能互换。网页标题与正文卷次分歧保留，不改成已核原版。此为具体的星平技术并存及复合关系证据，而非紫微斗数直接来源、两术预测效度或子平正官首证。

NEXT：继续1611 DRS53263996卷首目标原叶，核戊句、壬癸缺句和《星學大成》明刻原表；沿《琴堂》对禄追更早有日期的操作实例，区分天元禄/官星/禄神/科名/科甲、星曜位置与紫微四化。保持南印度方盘、古籍卷四等原有上游未决路线。R9查重补Volume 468/卷568/官星/對祿/对禄/琴堂/1kobozbi23jms/論官星/十干官星之祿星；既有15BZ两来源复用，未完成全库查询，不正式登记新来源。transmission_impact=NONE，TW-OPEN-0059继续OPEN，正式统计不变，不终验。


### 12m. 琴堂妙曦的1282人物见证、1379序文层次与明刻《新刻琴堂五星》定位（2026-11-27）

同一大对话基线HEAD `c02e32931a243d38efaf95ad14918096dced6624`、tree `29a8e084a460460de7452d97940773111e33c311`。20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity；六权威blob逐项核对不变，复用上一轮已完整解析及五P0核阅，正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。根647条对琴堂/妙曦/季董宗舒/黃秋山/黄秋山/17008/411999028759/文山集/宋明时期黄道十二宫/ee3455be9d91293f66d896f31145a013/從域外秘辛/从域外秘辛/韋兵/韦兵命中0；实读15BB、15BC及15BB分片，证明根无命中不等于全库无相关文山集条目（已有卷13/四部丛刊卷9而非本轮卷21）。279分片正文尚未全查，不正式准入，既有R8大台账写入阻塞仍在。

**人物与术法年代分开。** [《文山集》四库本卷21〈纪年录〉](https://zh.wikisource.org/zh-hant/文山集_(四庫全書本)/卷21) l195–197，壬午（至元十九年1282）下的鄧傳雲段确见“初閩僧妙曦號琴堂以談星見”，并叙其进言土星犯帝座。这是后传纪年录的明确人物/活动纪年线索，并非琴堂出生日期、文天祥亲笔证言、对禄术法或预测验证。卷首l115说明正文和注释来源不同，注杂取鄧光薦丞相传等； l198–200并及1323、1341后事，不能把整卷定为文天祥生前原作。CTEXT chapter142364 行82检索返回同段，但直接打开403；不算另一个独立物理见证。韦兵《从域外秘辛到本土知识：《星学大成》所见10～13世纪的星命术及其中国化》（《唐宋历史评论》第十一辑，当前[转载](https://www.astro-read.com/arcview/252) l22及[书目](https://www.sanmin.com.tw/product/index/012069537) 可定位，未核原刊页码）将辛未授业纪年解为1271，并推测妙曦即琴堂文本作者、吕逸斋为师；六十年循环纪年及注释脱字须另核，不能据1282人物活动单独确定1271授业或全部琴堂篇作者。

**1379自署序与多层编纂。** [《星學大成》四库本卷8](https://zh.wikisource.org/zh-hans/星學大成_(四庫全書本)/卷08) l115–123：卷首先为易水育吾子的编者序，称虚实五星结合四柱与星曜、搜集并改编六十四条，认为可与子平互参；后接虚实五星源流序，明注经编者笔削润色，洪武十二年正月十九日署括苍龙泉季董宗舒，追述1373受蒲庵来复授书及灵椿、普澄、慧月等传递，又叙1378后与叶季原、杨文叔校订。保留“季董宗舒”自署与其他篇题“季宗舒”的异称，待人名消歧。黄秋山前言自称学琴堂二十余年，并称吕逸斋玉板歌经过琴堂摘编。三层署名、序文纪年和先前传说不能合并为一条已证唐一行至元明师承；原刻目标页未核。 [卷24识典受读](https://www.shidianguji.com/book/SK1609/chapter/1m1elftaz71uj)与[CTEXT索引](https://ctext.org/wiki.pl?chapter=604962&if=gb) l106,109将琴堂与耶律、子平等取用分开，并述年/月/日/时及胎元的虚实处理。传文“傳授呂逸齋”存在方向歧义，现代韦兵补“於”为解释候选，不静默修字。原先对禄的十干完整公式仍只核到明清受读，不能直接移到1271或1282。

**具体复合规则，而非纯粹名词相似。** 卷8 l123的坐实例以命宫子取土为命主，火/罗为生我曜；再检用曜所居地支是否见于出生四柱的四个支。抽象为两个独立条件：生我关系 E 与地支集合成员关系 S；用例四支卯戌午未，若用曜在午则S=true、在申则S=false。此为受读文字明确的可重放成员判定，不将其推广为完整琴堂断法、真实预测或紫微地支宫规则。与十二宫主、实际星曜位置及四柱共同使用，构成比同名官禄更具体的本土化机制。卷24年/月/日/时虚实与年龄区段（25/26–50/50至末等边界）须继续原页核对，暂不补足不明确的50岁交界。

**独立明刻定位。** Commons所载中国国家图书馆《格致丛书》善本号17008、胡文焕编、文会堂明刻、郑振铎跋，[第9册141225](https://commons.wikimedia.org/wiki/File:NLC892-411999028759-141225_格致叢書_第9冊.pdf) 48个数字页，收《新刻琴堂五星》卷一二；[第10册141226](https://commons.wikimedia.org/wiki/File:NLC892-411999028759-141226_格致叢書_第10冊.pdf) 41个数字页，收卷三四、附录及总断法例，另列《传授源流》一卷，是否同书组成部分待核实际叶。元数据指明同一馆藏套书，不算两件独立明本。第10册原PDF因10,756,359字节超过网页工具限额无法打开；第9册单页1封面影像可见，2–4页960px直接取图失败，未核目标正文或明确刊年，不授原字权限。明代胡氏活动年段不能充作本物件的精确刊年。此载体比清代集成汇录提供独立早期刻本追索入口，尚未确认目标对禄段。

**现代研究的具体下一步。** 宋神秘《宋明时期黄道十二宫与二十八宿的竞争》，《中国科技史杂志》2025,46(4):614–627，[期刊摘要及注3](https://zgks.cbpt.cnki.net/portal/journal/portal/client/paper/ee3455be9d91293f66d896f31145a013) 明列宫度主三种优先候选，且指琴堂卷4/8/24/25与集成卷589/590可比；仅公开摘要、注释，不冒充已核全文。中研院网站[《中国星命学中案例的运用》](https://www.ihp.sinica.edu.tw/~medicine/active/years/astro.PDF) 提取文字l426–445区分琴堂格局示例与个案；截图index13/14中文字渲染为空，故保留为提取文字候选，不能称原刊视觉核读。卷589/590对禄字面检索未命中，有限检索不是全书不存在的证据。

NEXT：优先找17008卷一至四的可用目标页和季董宗舒、蒲庵来复、吕逸斋、黄秋山的独立记载，核辛未及对禄原句；再循韦兵指出的《秤星灵台秘要经》洞微大数/限歌与《星學大成》卷7、通志梁嗣真书目做独立年代和算法对照，继续南印度方盘和希腊化、伊朗中亚等上游路线。R9查重追加妙曦/琴堂和尚/呂逸齋/吕逸斋/季董宗舒/季宗舒/蒲庵/來復/灵椿/靈椿/普澄/慧月/黃秋山/黄秋山/指金虛實五星/17008/411999028759/141225/141226/文山集卷21/142364/韋兵/韦兵/從域外秘辛/从域外秘辛/ee3455be9d91293f66d896f31145a013/astro.PDF/秤星靈台秘要經/梁嗣真。全库查重和R8正式准入未完；transmission_impact=NONE，TW-OPEN-0059保持OPEN，不改变正式来源、Matrix、图谱、算法或终验状态。


### 12n. 秤星经书目分层、洞微大数十二宫全量重放及年龄异文（2026-11-27）

同一大对话基线HEAD `5856254437e959e3252cf7d3c2065e4634100187`、tree `903ac05d64766b4892b0895dd441059acd7bd11b`。20 Actions中19 success、clean-training-system in_progress、无exact-HEAD continuity；六权威绑定不变，复用本大对话完整权威解析及五P0核阅，正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。根647条针对秤星/洞微/梁嗣真/郡齋讀書志/郡斋读书志/靈臺經/灵台经/DZ0289/DZ0288/Kalinowski/Kotyk字面命中0，非279分片全库查重，已有12i/j及15FF-R上游记录继续复用。R8台账写入阻塞未解除，本段仅追加既有检查点，不增加正式来源。

**宋代目录明确记录域外来源假说。** 实读[晁公武《郡齋讀書志》卷14](https://zh.wikisource.org/zh-hant/郡齋讀書志/卷十四) l164–165，三卷《秤星經》不署撰人，以日月五星及罗计炁孛十一曜演十二宫宿度；对来源明言不知、或云天竺梵学，继而引中国古代星占文献为背景，对交初交中及炁孛也分别评价。此为宋代目录传文中的技术描述和当时的印度起源意见，不是确定南印度路线的记载，更非紫微斗数直接抄袭印度的证据。另据[道教文化中心索引](https://zh.daoinfo.org/wiki/秤星靈臺祕要經) l4–6，现存《秤星靈臺秘要經》一卷，与《靈臺經》同卷、正统道藏洞真部众术类薑字号、涵芬楼136、新文丰8、三家本5、提要288。不同书名、卷数与目录年代不得视为同一传本；该索引另提出窦子通及扶风隐者相关题名候选，未作实物校勘。编号体系不一：[识典众术类入口](https://www.shidianguji.com/zh/library/30078) l23分别列靈臺經/秤星靈臺祕要經、涵芬楼影印明正统道藏底本；点击DZ0289实际404，不将目录链接当成目标原页已读。

**断代层。** [《秤星靈臺秘要經》受读](https://zh.wikisource.org/zh-hant/秤星靈臺秘要經) l139第一人称叙乾宁中删节某禳法；索引据此推唐末撰人，乾宁纪年本身不为两首附录歌诀精确断代，也不据叙述认证郭璞、一行或李筌为作者。韦兵[转载研究](https://www.astro-read.com/arcview/252) l13提出晚唐五代洞微古书及梁氏归属，为现代学术假说。清代[《古今圖書集成》經籍典451卷](https://zh.wikisource.org/zh/欽定古今圖書集成/理學彙編/經籍典/第451卷) l1490–1515行年类确列道士梁嗣真《洞微歌》一卷及相邻注《洞微限》一卷，且另列人元百六限；l1460三命类又列《秤星經》一卷。该后出目录是鄭樵条目的可查旁证，未作宋版原叶核查；CTEXT通志略 chapter72736 的检索片段OCR紊乱且直开403，维基通志卷068虽见五行类开头、梁嗣真/洞微未检出，不据此否定原载。书目中相邻题名也不能证明现存文本即梁氏著作。

**十二宫全量机械重放及例证异文。** 实读秤星受读 l186–194，对地支列基础年数：卯15、辰10、巳11、午15、未8、申7、酉11、戌亥子各4.5、丑寅各5；依顺序累积，以虚拟第一岁为标签起点（半开区间仅为研究重放约定），工具层实算十二项：
```json
[["卯",15,1,16],["辰",10,16,26],["巳",11,26,37],["午",15,37,52],["未",8,52,60],["申",7,60,67],["酉",11,67,78],["戌",4.5,78,82.5],["亥",4.5,82.5,87],["子",4.5,87,91.5],["丑",5,91.5,96.5],["寅",5,96.5,101.5]]
```
总100.5年，与[《星學大成》卷7](https://zh.wikisource.org/zh-hant/星學大成_(四庫全書本)/卷07) l116–121十二宫按宫名配给的时长多重集合完全吻合，且按卯起命可复用12j前七宫节点16/26/37/52/60/67/78与濟度金書对应。此为卯宫示范下的对位，不能误将绝对地支位置或虚岁标记认定为所有出生盘唯一执行政策；末五宫名称仍待独立核实。两书受读昼生火在巳例，一处写25，另一处写26/27且注26；累积前两宫25年，首岁标签进入巳为26，因此25和26可能为经过年数与年龄标签差，但27无法由此直接解释，保留异文，未见早刊不得纠字。秤星称百为准、遇善恶增减半，星学大成称百六为100年6月；固定时长基础模型和依据星曜的调整层分开，不把100.5解释为寿命预测或一律100岁。以卯宫15年为例，若仅作单项半数加减算术候选，则增半22.5、减半7.5；适用条件、多个调整顺序及边界未核，不运行断命。

**对应歌诀不是字字相同。** 秤星l176与星学大成l193–206开头同句，均按昼夜及三方主判火土作用，且均以本宫、对照、三合无曜定义空限；但前者计都注出现双鱼壁宿及室奎次等，后者写白羊奎娄，另有歌句差异。按结构记录平行/异文，不断定单向抄传或后见证可无条件补残本。现有[道教组织扫描PDF](https://www.daoist.org/BookSearch%28test%29/list010/a8-019.pdf)题录二经同卷，实际截图index7/印页0190显示的是《靈臺經》十五、十六段及星曜力分，而非目标洞微歌；index11/12截图失败；文本尾部至0193亦未核目标图，不能赋予《秤星》原字权限。保留误命中/访问边界，继续找涵芬楼136或可靠同物件分件。

NEXT：核《通志》原条及一卷/三卷秤星书目关系，核洞微歌原页、白羊/双鱼与宿度的异文，比较七强五弱、三方主、宫度力量分数与希腊化及印度 horoscopic astrology 技术。沿韦兵文中《三辰通載》三十四卷与日本静嘉堂三十卷影抄本开展可访问性核查；与此前南印度方盘、1581古叶及琴堂源流工作保持并行未决。R9查重追加秤星經/秤星经/秤星靈臺祕要經/秤星灵台秘要经/靈臺經/DZ0288/DZ0289/洞微大數休咎歌/洞微限歌/百六吉凶歌/梁嗣真/郡齋讀書志/郡斋读书志/薑字号/涵芬樓136/Kalinowski/Kotyk/三辰通載/三辰通载/錢如璧/钱如璧/静嘉堂/靜嘉堂。未完成全库查重、新证据正式准入或R8台账发布；transmission_impact=NONE，TW-OPEN-0059保持OPEN，正式统计、Matrix、图谱与排盘不变，不终验。


### 12o. 《三辰通載》34/30卷书目、紫炁异文与十变曜差异重放（2026-11-27）

同一大对话基线HEAD `0375be50231964b701b13babd19c28fdd6a0a627`、tree `bbf2bf96f63f2b93d45e286f405d0adf1644b6bc`；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity；六权威blob不变，复用本大对话完整解析及五P0核阅。正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。根647条针对三辰通載/三辰通载/錢如璧/钱如璧/趙江紅/赵江红/250431513/7461522579262537769/7568279811106275371/皕宋樓藏書志/皕宋楼藏书志/聿斯經/聿斯经字面命中0；非279分片全库结果，复用15BZ及12k–n。R8大型台账发布阻塞尚未解除，本段追加已有检查点，不改正式权威JSON。

**书目与实物分层。** [《文獻通考》四库本卷220](https://zh.wikisource.org/zh-hant/文獻通考_(四庫全書本)/卷220) 引陈氏著录嘉禾钱如璧编《三辰通载》34卷。清陆心源[《皕宋樓藏書志》卷51受读](https://www.shidianguji.com/zh/book/CADAL02091390/chapter/1lb03jo5xvbc4)及[CTEXT对应条](https://ctext.org/wiki.pl?chapter=718738&if=gb&remap=gb) l72–75标影写宋刊本30卷，记录卷1–3星宫局格、4–25各曜、26–28清台120格、29洞微百六限、30竹罗三限，推测首尾具备而无缺。两平台同一著作转录非独立实体。赵江红2020《静嘉堂藏孤本〈三辰通载〉考略》（《中国典籍与文化》2020(2):131–144，[期刊平台摘要](https://ccj.pku.edu.cn/Article/info?aid=250431513)）反认为末四卷亡佚、部分文本可在明《星学大成》找回，并判南宋中期成书、清人影宋抄、陆氏旧藏。仅核公开摘要，未读原刊全文或静嘉堂馆藏原叶，后四卷具体篇章、传抄谱系保留待证。日本[1930静嘉堂汉籍分类目录NDL1787678](https://lab.ndl.go.jp/dl/book/1787678?page=331)可定位术数类起于0243.jp2；本轮只核目录导航，未定位书名目标图。国书数据库泛搜索误命中日本著作，不计来源。

**可查正文与载体边界。** [识典《三辰通载》目录7461522579262537769](https://www.shidianguji.com/book/7461522579262537769/chapter/1loio46bnc3kq)及另一书号7568279811106275371目录，前者可访问章节正文、后者目录OCR串列严重；书级直开失败，未确认两数字载体底本是否相同及与静嘉堂影抄本的原件绑定。故以可查转录为候选受读证据，不称原本已核。前者明确卷1含命身宫、十二宫、胎元，卷2七强五弱、昼夜、三方、科名/科甲、官星/催官、十变曜等；卷3强弱、宫曜及格局；书名目录与正文对照优于只据现代术语猜测古法。

**紫微/紫炁的具体异文。** CTEXT上述陆氏藏书志转录卷18–19作天乙紫微星；识典目录及[卷18紫气论](https://www.shidianguji.com/book/7461522579262537769/chapter/1loio4iowrx1m) l8–13明确天乙紫气，称木之余、28个月一宫（原转录句首有讹疑）、28年一周天。12乘28个月=336个月=28年，算术吻合。该定位机制不同于斗数按局数/生日定位紫微；既有18星受读同名紫气线索不得替代具体传承证据。现阶段优先核陆氏目录原图及静嘉堂卷18/19物理字形，不能先判目录原著误字、OCR错误或真正异名，更不能据紫微二字将南宋五星术当作现代十四主星斗数。紫微名称线索与紫炁计算机制分开。

**十干变曜：同结构但不可直接复制。** 复用15BZ《星學大成》[卷1〈变曜歌诀〉](https://zh.wikisource.org/zh-hans/星學大成_(四庫全書本)/卷01) l183–185（十曜次序火孛木金土月水炁计罗、十类禄暗福耗荫贵刑印囚权），按已验证的轮转法，比较《三辰通载》[卷16水星论](https://www.shidianguji.com/book/7461522579262537769/chapter/1lomxidf239cf) 与卷18紫气论显式十干赋值。工具层实际计算按甲乙丙丁戊己庚辛壬癸顺序：
- 水曜：星学轮转[刑,贵,荫,耗,福,暗,禄,权,囚,印]；三辰[刑,贵,印,耗,权,暗,禄,福,囚,荫]；6/10字面一致，丙戊辛癸四干不同。
- 炁曜：星学轮转[印,刑,贵,荫,耗,福,暗,禄,权,囚]；三辰[阴,刑,贵,印,耗,权,暗,禄,福,囚]；6/10字面一致，甲丁己壬四干不同。其中甲阴是否荫/蔭、乙魁刑是否两标签、己权兼催官及壬福兼正魁均属待核语义/原字，不将额外角色合并为十变类别。两曜合计12/20字面一致，不宣告其余八曜的规则。
- [三辰〈定官星／定推官星〉](https://www.shidianguji.com/book/7461522579262537769/chapter/1loio48ilcnqr) l80–94，官星取第十宫主，推官另按十干给定曜，非12l的正官干→天元禄映射。例甲推官金，后者为炁；不把两个不同标题直接判为版本讹误。同页l53–66科名按干五行、科甲按命宫对宫主，与12k的具体输入一致；仍非紫微化科。按角色、输入、输出分别登记候选，勿用后世表默默修正宋书转录。

**洞微规则第三见证。** [三辰卷29起限](https://www.shidianguji.com/book/7461522579262537769/chapter/1lomxizhdeqrz) l10–16给全十二宫时长，15/10/11/15/8/7/11/4.5×3/5×2合100.5年，和12n基础时长同集合；卯命巳火例保留26/27及注文26，与《秤星》25不统一。另[卷29增减及行年小限](https://www.shidianguji.com/book/7461522579262537769/chapter/1lomxizl62kun) l8–18,55–61及后段列不同星曜状态加4/2/1年或减半、交限须考虑出生月日时；小限由1岁命宫起，逆行每年一宫，男女同向，生日交接。以卯命为候选示例，1–4岁卯寅丑子，13岁回卯；不将其当作斗数小限（需独立起法及方向）或四柱小运。增减仅列单状态候选，不推断多曜叠加或采用生日/虚岁统一政策。与12n的统一半数调节候选形成具体差异，后者不可代替此分层法。

NEXT：优先取得赵江红原刊公开全文与静嘉堂原件目录书号/授权公开影像，核陆氏藏书志紫微/紫气原字；逐曜建立10×10表但先定位各曜正文与版本，查《三辰》卷1的聿斯经、琅玕经及旺宫星度、七强五弱宫来源，再对照希腊化/印度技术原典。R9待查重补三辰通載/三辰通载/錢如璧/钱如璧/趙江紅/赵江红/250431513/7461522579262537769/7568279811106275371/皕宋樓藏書志/皕宋楼藏书志/718738/1787678/天乙紫氣/天乙紫微/聿斯經/聿斯经/琅玕經/定推官星/1loio48ilcnqr/1lomxizhdeqrz/1lomxizl62kun。继续保留南印度方盘及其他上游未决事项；未全库查重、未完成R8写入及正式证据准入，transmission_impact=NONE，TW-OPEN-0059保持OPEN，不变正式来源、Matrix、graph或排盘，不终验。


### 12p. 聿斯经—Dorotheus的具体技术平行及《琅玕经》引文边界（2026-11-27）

同一大对话基线HEAD `46d84523f81d76da20467324f0591cdb9d92a0c1`、tree `668dd07a5f7dfa4df244955cb582fd3bf87fba1b`。20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity；六权威绑定未变，复用本对话完整权威解析及五P0核阅。正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。根647条对聿斯/琅玕/Dorotheus/SCIAMVS_15_105/Mak/Kotyk/李彌乾/李弥乾命中0，但13ZW已登记Mak 2014及P4071，实读13ZW报告和其分片复用，不重复登记。279分片全库检索未完成，R8大型台账发布阻塞未解除，本段只追加原检查点。

**书目与译传假说。** 实际核读 Bill M. Mak, *Yusi jing: A Treatise of “Western” Astral Science in Chinese and Its Versified Version Xitian yusi jing*, SCIAMVS 15 (2014), 105–169，[期刊原刊PDF](https://www.sciamvs.org/files/SCIAMVS_15_105-169_Mak.pdf)截图index1/23/24（印页106/128/129）。p106引《新唐书》59（中华书局p1548）贞元785–805李弥乾传自西天竺及译者条、陈辅四门经；另引《通志》68（p801）五卷梵书、汉译二卷及陈辅重修、徐氏续歌、安修睦撰歌诀等相关书目。作品首次著录、译传事件时间与今传版本分开。维基《新唐书》卷59受读对李彌乾/都利的字面find未命中，本轮所核为Mak论文中引录的目录，未见中华书局目标书页或古刻。题名聿/韋/吠/車等转录、译者字形异读待核，不自行补全。Mak p128 Table2对十二宫、三分性与昼夜、旺度、出生第三日月位、Lots及行年比较；p129提出Dorotheus作品经西亚/中亚语言与东方基督教群体传入的模型，特别中古波斯语为候选，非存世汉译底本身份已证。另读 Jeffrey Kotyk [Iranian Elements in Late-Tang Buddhist Astrology](https://www11.ihp.sinica.edu.tw/storage/w2_file/2754DfNUyFU.pdf)提取文本pp35–36，截图index11超时；其结论援引Mak，不能作两次独立原文校勘。Li Su李素与译者身份联系为现代候选，不据此消去目录译者异读。史料的“西天竺”传来地点与著作希腊化知识来源、传递语种、经行路线、南印度盘式各为独立问题。

**七曜旺度的三组精细比较。** Mak p143实际截图（index38）列校订文及校记；p144实际截图（index39）列P4071引句和《瑯玕經》引句。对照[《三辰通載》卷1受读](https://www.shidianguji.com/zh/book/7461522579262537769/chapter/1loio4766bv2h) l104–106，日白羊19、月金牛3、土天秤21与Mak所列Dorotheus I.2三个星座内度数3/3相符。水星双女的二五/三五、金星室/奎为Mak明确标注的校订，不能把其修订文字当原叶；《三辰》水三五为另一传文旁证。火星磨蝎四与七，Mak用中国宿度换算联系28°，该解释不等于四或七直接等于28；木星鬼宿、金星室宿度并非相同坐标表达，需具体宿界及度制。原始360°黄道与365余中国周天度、宿内度、整数星座序须分开。不能未经换算说七项全部精确等同，更不能把星曜旺度等同斗数庙旺表。P4071原有证据为同一写卷（13ZW/14S已定位），Mak p144引P4071r3col5–6的水居双女与XXDC17.2b所署《瑯玕經》平行，后一文另列官职、宫宿条件，非全篇相同；未取得《琅玕经》独立原本，不断定两经为同书。复用[《三辰》另一目录](https://www.shidianguji.com/zh/book/7568279811106275371/chapter/1li0jioc3iux6)的多曜琅玕节要线索，OCR串列不可作校勘。

**行年与Lots的机械重放。** Mak p151截图（index46）XIII的年行由东出命宫、每年一宫、生日交接；同页XXDC7.20b洞微小限明确逆移及不分阴阳，注区别天轮顺行与地盘逆行。与12o三辰小限是具体技术结构平行，不能只比较“顺逆”二字而忽略坐标。取示范命宫卯、地盘逆序，以已满周岁t为非负整数，实际工具层重放t=0,1,2,11,12,13 → 卯寅丑辰卯寅，12年循环；此为受读规则示例，出生时刻交界与岁标签须按具体版本保留，不移植紫微小限。Mak p146截图（index41）VII及注21另列相貌/福德变格：日生从日数至月、夜生反向，再从升起宫计相同距离。以抽象同向索引A、S、M in Z12及零起距离为测试约定，L_day=(A+M-S) mod12, L_night=(A+S-M) mod12。实际三个候选例(A,S,M)=(2,4,8)→6/10，(10,11,1)→0/8，(5,3,3)→5/5；只重放相对距离和昼夜互换，不裁定古文起数含首/含尾、福德宫与相貌名义的全部变体。它依赖日月实际星座及升点，与斗数福德宫/相貌或身宫定位输入不同。Mak的希腊化对读指向技术渊源，仍需独立读Dorotheus校本；本轮未取得希腊语、巴列维语原本或唐代全译本。

NEXT：核《聿斯经》不同引文系统、《琅玕经》在三辰各卷的实际引文题署，核Mak原刊其余校勘及P4071对应原叶的逐字校读，核Dorotheus I.2/IV.1可访问的阿拉伯译文及批判校本；继续印度及伊朗中介、南印度方盘等平行路线。R9待查重追加SCIAMVS_15_105-169_Mak/聿斯經/韋斯經/吠斯經/聿廝經/都利聿斯/西天聿斯/琅玕經/瑯玕經/李彌乾/李弥乾/李素/陳輔/Dorotheus/Carmen Astrologicum/Pahlavi/東方景教/2754DfNUyFU/年度profection/相貌福德/1loio4766bv2h。已有13ZW相关登记优先复用，未完成全库查重、未正式准入或恢复R8台账发布；transmission_impact=NONE，TW-OPEN-0059保持OPEN，不改变正式计数、Matrix、graph或排盘，不终验。


### 12q. 多罗透斯英译本实核与P4071星曜坐标、文本异义反证（2026-11-27）

同一大对话基线HEAD `60aaffa60a240759aa62c689366b50d54186decb`、tree `91b307baf0633991863a841f2f1bbda9c1c67e8a`。20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity；六权威绑定未变，复用本大对话完整权威解析与五P0核阅。正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。实读13ZW来源分片、14S早期命例报告，复用EXT-TIANWEN-13ZW-ISAHAYA-LIN-2017及EXT-TIANWEN-13ZW-MAK-2014、P4071馆目，非新增独立实物。279分片查重及R8大型台账发布仍未完成，本段只追加既有检查点。

**独立于Mak比较表的校译见证。** [Perseus目录](https://catalog.perseus.org/catalog/urn:cts:greekLit:tlg1337.tlg001.opp-ara2)定位Pingree编1976 Leipzig Teubner初版，阿拉伯文本目录页323–330、332–427（非古抄本纪年）。实际核[Skyscript获许可重刊Book I](https://www.skyscript.co.uk/dorotheus1.pdf) index1/显示p2（Teubner pp161–162），I.1日夜三方主与I.2七曜旺度，七项对应太阳白羊19、月金牛3、土天秤21、木巨蟹15、火摩羯28、金双鱼27、水处女15，反向180°为落陷；三项12p对应数字已独立于Mak二手表核实。I.1例白羊三分组日生首日次木末土，夜生首木次日末土；未把三分主序视为中国地支三合或五行局。此是现代英译及重刊影像，非希腊文原卷、巴列维文本或阿拉伯古抄本实读。未复制整段受版权约束的译文。

**P4071数值反证与坐标边界。** 实核Isahaya/Lin 2017 [J-STAGE原刊PDF](https://www.jstage.jst.go.jp/article/historiascientiarum/26/3/26_153/_pdf/-char/en) index9/11/13/14即pp162/164/166/167。Table1所列古代宿度转换后的现代黄经范围、Stella Navigator 10复算范围，均为论文数据而非本轮星历独立复算。实际工具层算术重放：月亮古区间157.21–174.10°与现代294.30–295.07°最小间隔`120.2`°、最大`137.86`°；计都289.29°与候选升交点285.34°相差`3.95`°；紫炁130.63–139.64°覆盖作者近地点137.8°，但独立28年周期模型约123°距区间下界`7.63`°。区间比较只检验数值，不解决历法、坐标、岁差或候选模型真伪。p167作者明确保留紫炁计算不确定，并在注78记载第78、84、96行罗计定义并不始终一致。日本宿曜及七曜攘灾决罗睺升交点、计都远地点的规则与P4071该组罗睺降交点、计都升交点候选不同；月孛远地点候选不与紫微斗数虚拟星安法混同。不以单一位置命中定夺全部行年或统一星曜本体。

**训诂与几何纠偏。** p162注54作者将命宫译作身宫是依据《星学大成》卷6的编辑解释，不能视为古卷原字已纠正；注57将处女与摩羯之间三个中间宫称90°，但两宫起点150°/270°、相距`120`°，标准三合为120°，中间三个整宫共90°与两宫起点间隔120°不可混用；两个行星实际经度仍需原数。注58指出木星宝瓶而火星处女，并非同宫；水火同处女的读法为候选，不直接修原卷。注59保留康遵挪用同一三合关系和失传《聿斯经》异本两种解释。P4071的命图本身缺失，论文表与后世复原均不是存世古代命盘图像。

**2025年研究进展的证据边界。** [葛业静研究转载](https://www.astro-read.com/arcview/241) l11–32,42–52,124–126提供月宿直与佛经宿直、二十八宿—十二宫对应、天运行年复原以及曹延恭身份候选；与13ZW已登记的2025摘要核对，不新增独立出版物。转载有明显文字异常（摘要太阳张与正文太阴张/翼、佛经所引序列不完整），不作原刊校勘或终裁；作者假说包括查《大集经》得月亮位置、单一命例、廿八/卅八讹字、星历表粗略及行年多月覆盖，均保留待原刊与原叶复核。不得据现代天象不符就认定造假或推断预测准确率。

NEXT：优先定位并核校P4071第78/84/96行原叶与《郑氏星案》对应星曜定义，核葛业静2025原刊与《大集经》卷42目标字句，按相同历法/坐标比较星曜实算；追Perseus所列阿拉伯校本及希腊残文、印度旺度和罗计独立定义。继续R8台账发布、R9全库查重、南印度方盘与其他原有上游路线。R9补Perseus URN tlg1337.tlg001.opp-ara2/dorotheus1.pdf/Isahaya/Lin/Entangled Representation/葛業靜/葛业静/astro-read.com/arcview/241/鄭氏星案/郑氏星案/曹延恭。未全库查重及正式准入，transmission_impact=NONE，TW-OPEN-0059保持OPEN，不变正式计数、Matrix、graph、排盘，不终验。


### 12r. 郑氏星案传承归属、存世圆盘影像与子时中分实例（2026-11-27）

同一大对话基线HEAD `b669ec7dfbb28061b519db3a821689797926c73a`、tree `6471b2ff4a36207c20bac9a537e31ec952c820b7`。20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity；六权威绑定不变，复用同一对话完整权威解析及五P0核阅。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。根647条对郑氏星案、温州经籍志、陆位、古今律历考、天经或问、子时中分繁简组合字面命中 `[{"id":"EXT-WIKISOURCE-GUJIN-LULIKAO-V49-DATONG","title":"《古今律历考》卷四十九·万历二十四年丙申岁闰八月朔日食历〈大统〉"},{"id":"EXT-WIKISOURCE-GUJIN-LULIKAO-V50-SHOUSHI-PRECISION","title":"《古今律曆考》卷五十·萬曆三十三年乙巳歲二月望月食曆〈授時〉"},{"id":"EXT-ZIWEI-ZHANGGUO-NIJL-1594","title":"《新編評註通玄先生張果星宗大全》"},{"id":"EXT-ZIWEI-ZHANGGUO-TOHOKU-HIRAYAMA-GUANGXU7","title":"《新編評註通玄先生張果星宗大全》卷之7-8"},{"id":"EXT-ZIWEI-ZHANGGUO-NLC-PRINCETON-NJPX95-B1857","title":"《新編評註通玄先生張果星宗大全》NJPX95-B1857"},{"id":"EXT-WIKISOURCE-XINGYUNLU-V1-SHOUSHI-YING-REVISION","title":"邢雲路《古今律曆考》卷一·授時諸應隨時改革與至元三十一年三應改定說"}]`，279分片全库查重未完。大型台账R8发布阻塞仍未解除，本轮无新正式来源，仅追加既有检查点。

**人物、案例及编纂并非同一时间。** [《古今图书集成》艺术典584](https://zh.wikisource.org/zh-hant/欽定古今圖書集成/博物彙編/藝術典/第584卷) l138陆位序称郑希诚为至元时温州安固人，星案为后人收集批辞；不以序文神异师承为历史事实。清《温州经籍志》[CTEXT chapter157396](https://ctext.org/wiki.pl?chapter=157396&if=gb) 检索片段l41/43转引陆位序，著录《果老星宗》卷十40条、地方志另称占词72张，并明确质疑术家辗转托名及羼窜；直开403，未校原页，不能把72张当存世40案的原全集。复用此前《星命溯源》四库提要的瑞安主簿、沧洲自署，人物生卒与案例归属待证。[《中国星命学中案例的运用》](https://www.ihp.sinica.edu.tw/~medicine/active/years/astro.PDF) l263–314，提取文字称40案、转引李光浦1998 pp301–302复原15案的出生时间从1312-12-27（案32）至1376-02-02（案8），并讨论星案的案例教学功能；截图index8/9中文缺字、仅显示数字及少量西文，非目标正文视觉校勘。该跨度是复原的出生时间、不是著书或施占日期，不断定皆为一人亲批、真实反馈或预测验证。

**实见后世星盘影像及日界证据。** [同一《集成》数字册469页57](https://zh.wikisource.org/wiki/Page:Gujin_Tushu_Jicheng,_Volume_469_(1700-1725).djvu/57)、[页63](https://zh.wikisource.org/wiki/Page:Gujin_Tushu_Jicheng,_Volume_469_(1700-1725).djvu/63)、[页65](https://zh.wikisource.org/wiki/Page:Gujin_Tushu_Jicheng,_Volume_469_(1700-1725).djvu/65) 分别实际打开网页图像链接（1920px请求、工具显示缩图），可见卷584首、陆位序、圆形多层宫度盘及各案干支栏，页57两盘、63及65各三盘，合八个版面图位，不称完整40案或八个独立物理见证。三页均为同一扫描册，边栏中华书局影印；不是元代原图，未核物理底本版次/扫描SHA。页65第一案正文目视可辨子时中分、壬辰癸巳、前四刻等关键字句，与未校电子转录l116相符；完整小字仍未native校勘。关键句为“但子時中分有昨今之異，雖星宿不差，日則有壬辰癸巳之別”，随后明确取前四刻作该案推断；仅证该星案对两种日干支输入的区分，不证现代23/00点时区、100/96刻制、紫微/八字统一换日或全天子时日干政策。工具层六十甲子枚举壬辰index28→癸巳index29；若另按现代通用五鼠遁候选，各自子时为庚子、壬子（研究者条件演算、并非本案原文时柱，也不裁定晚子时另起时干候选）。星曜宿位近似不变与干支标签突变属于不同坐标/运算层；连接既有TW-OPEN-0006作为后出相关术式的旁证候选，保持其原叶和独立换日待证状态，不改Matrix/运行时。页63另见酉末戌初备选，说明不是仅有子时的输入歧义；不得据事后解释推断预测有效。

**四余的历算/占命独立性。** [《古今律历考》四库本卷64](https://zh.wikisource.org/zh-hant/古今律厯考_(四庫全書本)/卷64) 可查检索传文（全页打开成功但目标find未命中，CTEXT对应648365直开403）称罗天首计天尾、孛月行迟点、炁起闰法，炁孛顺行罗计逆行。炁28年一周、孛62日7度、罗计约18年一周为古度制和近似周期，不能当现代360°常数；360/28、360×7/62分别只是条件单位演算，古文本另称62年七周，需核历元、周天365余及岁长。清《天经或问》四库受读检索段解释罗计为对置交点、孛为月行极高点、炁为闰余等候选，并强调非实物，直开可见全览但目标find未命中，不作逐字校勘。该后出历算解释不能倒推P4071或全部郑氏星案定义。星案页63/65文本中确有罗计、月孛、紫炁及宫宿、限路等组合判断，但当前图像小字不足以核完整坐标，未完成单案四余独立星历重算；不宣称验证任何占断应验。

NEXT：优先对页65目标案取native图、转录出生干支和时刻、盘内四余坐标及局部批语，核《温州经籍志》原图、独立明刊《果老星宗》卷十、古今律历考目标叶，分别比较历算节点与占命曜。R9查重补鄭氏星案/郑氏星案/陸位/陆位/溫州經籍志/温州经籍志/157396/Volume 469/子時中分/前四刻/壬辰癸巳/李光浦/古今律厯考/古今律历考/648365/天經或問/天经或问；若新增原叶证据须依R1/R2更新现有风险及权威视图，不以本段取代正式入库。继续保留P4071原字、南印度方盘、R8正式发布与R9全库查重。transmission_impact=NONE，TW-OPEN-0059及0006保持OPEN，正式计数、Matrix、graph、排盘状态不变，不终验。


### 12s. 《張果星宗》卷十独立物件导航与三层夜子规则的证据隔离（2026-11-27）

同一大对话基线HEAD `47e9629c69a4ee0d311ed0bdfefa062dd077ea8e`、tree `1f364ed008acc74df6a91b05ad31034cb98f5eb0`。20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity。六权威绑定不变，复用本对话完整解析及五P0核阅，正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0、core CLOSED。复读12AW/AX/BA及既存NIJL manifest记录；根647条对BD05337528/10020000001145/BD05367609/100238879/01793919655命中EXT-ZIWEI-ZHANGGUO-NIJL-1594，279分片正文未全查，不作新增来源断言。

**分册与不同物件的可执行定位。** [CiNii BD05367609](https://ci.nii.ac.jp/ncid/BD05367609?l=ja) l114–186明确万历甲午1594周氏文光新梓，1593为序年，五册中卷9–10资料号01793921865；卷十内题《新編校正評註通玄先生張果星宗》，与卷九“命格大全”不同。该本已在12AW/BA考据，不重复登记。[CiNii BD05337528](https://ci.nii.ac.jp/ncid/BD05337528) l114–202另列东​​北大学十册本、卷十01793919655、刊年不明、万历21序刊后印、虫损托补；不同尺寸及册数、不同资料号，不将同序年的后印直接等同1594物件。其与NIJL或藤原文库具体映射待馆号核对。[平山文库卷9–10官方记录10020000001145](https://touda.tohoku.ac.jp/collection/database/library/10020000001145) l28–101明确MA/591、MF q06506、资料号00070308498、94幅黑白图，[IIIF manifest](https://touda.tohoku.ac.jp/collection/iiif/metadata/10020000001145/manifest.json) 实际返回JSON及卷9–10元数据，Mirador正文未返回图页；page=55访问失败。此是12AX所核平山同书另一分册，不能视为1594原刊或独立同代证人；该分册网页未给刊年，不把相邻卷的序年自动移作本册实物年。[韩国藏书阁169178](https://jsg.aks.ac.kr/dir/view?dataId=LIB_169178) l45–53万历22、中国木板本、十卷十册、四周双边、上黑鱼尾、25.7×15.5cm，明显不同于BD05367609的四周单边白口单鱼尾、五册24.4×15.4cm；复用12AY旧对象而非新证人，不能据同年断同一雕版。目标叶本轮未获。NIJL既存manifest记录439幅、无structures；实取其中已登记canvas400/420的IIIF服务请求1600px均失败，未建立卷十精确canvas边界，不以失败判缺文。

**重新核读目标例且防止三类命题合并。** [《古今圖書集成》数字册469第65页](https://zh.wikisource.org/wiki/Page:Gujin_Tushu_Jicheng,_Volume_469_(1700-1725).djvu/65) l113–116明确标未校对；本轮实际打开其1920px请求的页面图（工具显示缩图），三幅圆形盘及第一案子时中分、壬辰癸巳、前四刻关键文字可辨。整卷584的网页find对目标语句无命中，但精确单页正面证据存在；不能据整卷网页搜索未命中判原书缺文。区分：
1. 12AW 1594 canvas195经直接物理原页核读，子亥互误的正文和七政历夜子上下四刻注释，是出生时刻辨误与分段机制，未明示上四刻改亥。
2. 12r/本轮《鄭氏星案》后出集成页65，前四刻选昨今不同日干支，是日界机制，并未给出改亥支的普遍规则。未定位1594卷十同案原叶，不提前把后出见证倒填元代或明代。
3. 12AU/AV的1697《三才發秘》反对夜子作亥，及后世紫微全书南洋堂上五刻属昨夜亥时，属于明确但相互竞争的时支分类候选。四刻与五刻亦必须分别核对应刻制。日干变更、时支分类、依日干起时干与星曜位置是四个独立输入/输出层，不把日界证据当作时支亥化的新增票数。TW-OPEN-0006仍OPEN，HPA-ZDATE-006仍MISSING_FROM_PRODUCT，禁止重开排盘或合并候选。

**入库阻塞复审。** 复读11a/b/d/e/f：R8六来源的隔离重放门禁已成功，但候选4,076,303字节ledger blob不在远端，原台账发布未完成；全库直接读取依赖规模庞大，保持旧格式兼容。此轮未找到经验证的正常大blob发布渠道，不重复此前失败的上传，不借用旧CI写权限，不迁移格式。新增检查点仍只能作为待准入研究材料；正式状态不得跟随候选推高。

NEXT：从已定位卷十独立物件取得星案目标原叶；若正常图像路线暂不可用，转入可访问的《大集经》月宿直与P4071具体坐标比较，避免重复目录检索。R9查重补BD05337528/01793919655/BD05367609/01793921865/10020000001145/00070308498/q06506/MA/591/新編校正評註通玄先生張果星宗/PC9A-20/169178/Volume 469；优先复用12AW/AX/AY/BA既有登记。南印度方盘、R8正式发布及R9完整查重继续未决；transmission_impact=NONE，TW-OPEN-0059及0006保持OPEN，正式计数、Matrix、graph及core不变，不终验。


### 12t. 《大集经》黑白月宿直重放与P4071翼宿来源的历法反证（2026-11-27）

同一大对话基线HEAD `1ae0a25d2d775b4869b9e582b456c5b3364c94f1`、tree `1b4b8f4b9e36d48708d0e6cecabc185ca7a100bf`。20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity。六权威绑定不变，复用本对话完整解析及五P0核阅；正式1.1587.0、1499/279、Matrix222/222、graph819/581、59 OPEN五P0、core CLOSED。根647条对T0397/大方等大集/日藏分/大集經/大集经/T1299/大唐月建/黑月/葛业静/葛業靜字面命中0；既有12c与13ZW、14S、12q的T1299及P4071研究复用，279分片未全查，不能据根未命中正式准入。R8大型台账发布阻塞未解除，本轮仅追加检查点。

**取得2025论文更完整的公开文字，修正此前转载局限。** 葛业静《敦煌遗书开宝七年星命书（P.4071）新探》，《敦煌研究》2025(5):100–109，[期刊目录](https://www.qikan.com.cn/article/dhyj20250509.html)、[Academia全文提取](https://www.academia.edu/145350781/) l7、[ResearchGate全文提取](https://www.researchgate.net/publication/398421805_dunhuangyishukaibaoqinianxingmingshuP4071xintanA_New_Exploration_into_Dunhuang_Manuscript_P_4071_a_Horoscope_Text_Dating_to_the_Seventh_Year_of_the_Kaibao_Era) l195–299（p101–102）。两处同一论文数字替身，非独立见证，未取得可截图原刊PDF。原摘要为太阴在翌，而转载astro-read/arcview/241误作太阳在张；原正文经文引用是毕、觜、参、井、鬼、柳、星、张、翼，转载作牛、娄、七日翼等讹。纠正先前仅能依转载之边界，不改旧记录。论文明确将中国后唐长兴元年九月初九与T0397卷42九月黑月九日合翼相联系，但可读p101–102未说明两种月份/黑白分的对应转换；保留为作者可能来源假说而非确证抄用。论文另列积日22073、实泛日15873，差6200；6200/225=27.555555...日，与近点月长度数量级接近，须核《大衍历》单位和真实历元，不能仅据商数认证康遵使用该算法。

**直接核到可复查经文。** [东京大学SAT T0397 p0280b08–17](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&useid=0397_,13,0280) l401–410、[维基文库卷42](https://zh.wikisource.org/wiki/大方等大集經/卷42) l116,132–153及[CBETA衍生Deerpark](https://deerpark.app/cbeta/T0397/42) l63–66相符；同一大正藏/电子传文体系，不计三份独立实物。K0056识典[日藏分具体章](https://www.shidianguji.com/zh/book/K0056/chapter/1kksgbomhnh8q)检索亦同，未核高丽藏原叶。CBETA官网动态页面未加载正文，镜像403不作缺文证据。卷首署那连提耶舍译（传文署“隋”，与北齐翻译年代需书目分层）；此处不据后出电子署名确定物件年代。实际28宿环按昴畢觜參井鬼柳星張翼軫角亢氐房心尾箕斗牛女虛危室辟奎婁胃，明确起昴终胃，黑白月分列。工具层用从一计数和28取模重放：
```json
{"九月黑":{"8":"張","9":"翼","14":"房","15":"心"},"九月白":{"8":"室","9":"辟","14":"畢","15":"觜"},"八月白":{"8":"虛","9":"危","14":"胃","15":"昴"}}
```
其中八月白依据卷42 l132–150逐宿用事，辟/壁、七星/星、觜/嘴异体保留。九月黑14为房也不等于中国九月9日；九月白9为辟而非翼。此为确定性传文查表，不是实际月球黄经复算。

**历法映射反证。** 中研院[2017学术报告纪要](https://mingqing.sinica.edu.tw/mingchingadminweb/SysModule/mvc/friendly_print.aspx?id=565) l34 说明理想年360日与28宿、四个双宿日形成364个宿标签=13×28，且北印度黑先白后、南印度白先黑后，译经适配中国朔望月时须处理月份错位；纪要非完整论证论文。卷42明确十月白3女虛、五月黑2牛女、六月白12牛女、七月白9牛女等四处双宿（SAT0280b27、维基l187/195/200），保留各处字序和原页待核。按此纪要所述月标映射候选，中国九月上半月对应八月白（九日危）；若仅改变同名月份黑白分则九月白九日辟；若直接以中国月日索引黑分才得翼。三种输入映射结果不同。第一种还须核该会议论述具体适用经本、月份起算及康遵实际习惯；不能用现代黑白月定义自动否决古代人为查表，亦不能据翼结果推定康遵故意误读。暂记 CALENDAR_MAPPING_UNRESOLVED；需要原刊、古历法实例、P4071原叶及同体系第二命例作交叉支持。

**T1299独立表的再检验。** [SAT T1299 p0388a19–b23](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?mode=detail&s=&useid=1299_,01) l139–185实际列大唐月建图。九日行12列为畢參鬼星翼角氐心箕牛虚室，按正月至十二月表头取第九列=箕（工具实际索引）；与12c已记录上卷28日周期和下卷27宿算法不一并行保留，不用流行现代宿曜表覆盖古表。经文紧邻讨论宿宽狭、前/并/随合，说明表值与观测天象之间还存在解释层。此处是另一条历日规则，并非P4071房宿或翼宿已证源头；若后续要解释房宿须继续查卷下本命宿算法及实物版本。紫微命身宫、八字历日及天文实测月宿四者不互相替代。

NEXT：核T1299卷下九月初九本命宿算法、日藏分的真实月份换算论证及张姓学者原文，找P4071原叶翌/翼、房日、太阴星等字段与独立同类命例（黑水城ИHB.No.5722《谨算》及日本《宿曜运命勘录》），继续验证域外知识如何被本土改造。R9补T0397/T397/大方等大集經/大方等大集经/日藏分/星宿品/0280b08/0280b15/九月黑月/九日合翼/黑白月/大唐月建圖/0388b02/葛業靜/葛业静/398421805/145350781/5722/謹算/谨算/宿曜運命勘錄/宿曜运命勘录/藏经考/565。保留南印度方盘、明本原叶、R8发布与R9完整查重未决。transmission_impact=NONE，TW-OPEN-0059及0006保持OPEN，正式计数、Matrix、graph和排盘不变，不终验。


### 12u. 《宿曜经》卷下两算法等价重放、P4071宿位分层及日本独立馆藏导航（2026-11-27）

新会话基线HEAD `2d3ca6da8ea87615d55fea2471cbbfc057bd1e11`、tree `27db014bf2dc29f1c2a40d73b5ebaee31c20e7b0`，远端5次提交确认12q–t后续；无指定分支open PR；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity成功，故未使用R2快路径。通过fetch_blob直接解析原current-state、ledger、graph（普通fetch_file空正文），完整解析Matrix、根registry、manifest，docs tree六绑定吻合，复核正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0；逐项读全部P0和TW-OPEN-0059，最新Matrix 12QD不冲突。根647条对T1299/宿曜經/宿曜经/0395b/T21n1299/宿曜運命勘錄/5722/謹算/谨算字面命中0，279分片未全查，不作全库新增断言。R8正式发布仍受阻，继续既有待准入检查点，不改正式状态及六绑定。

**精确复现T1299卷下两算法。** [SAT T1299 0394c17–0395a04、0395b01–08](https://21dzk.l.u-tokyo.ac.jp/SAT/ddb-sat2.php?kaeri=&mode=detail&nonum=&useid=1299_,00,0397) 和[台大数字佛典PDF](https://dlbs.liberal.ntu.edu.tw/FULLTEXT/sutra/T/T21n1299.pdf)实际截图index19/20/21（印刷页19/20/21）核得两幅圆形十二宫宿图、九月望宿昴、27宿排除牛以及顺逆数法、生日数加十三的简算法。图为后出数字传本所载图，不声称唐代物理原图；SAT与台大同传文体系，不计独立物件。图与正文均须分层，西国月名与中国月日之映射另行核实。PDF文字有氏/氐等差异，以SAT及上下文归一作算术重放，保留异文不做古本校定。

27宿环（研究者规范化）昴畢觜參井鬼柳星張翼軫角亢氐房心尾箕斗女虛危室壁奎婁胃。设望宿零基索引 a、日数 d，顺逆算法索引 (a+d-15) mod 27；简算法含起点计一，索引 (a+d+12) mod 27，两式差27。工具实际枚举27个起点×30日=810组，差异0。经文二月13/14/15/16/17日依次翼/軫/角/亢/氐，五项与原例相符；九月初九昴逆六为危；若以八月婁为望宿的另一条件输入，初九为女（仅映射敏感性对照，不认定适用P4071）。两算法等价不证明古历真实月球黄经、宿宽度或占断有效。

**与P4071对照，区分日期术与天文坐标。** 名义九月初九输入：T0397黑月翼、白月辟、T1299卷上月建箕、卷下27宿望宿法危；P4071另载房日兔、太阴翌（翼）及命宫天蝎。葛业静2025 p101–102[公开论文文字](https://www.researchgate.net/publication/398421805_dunhuangyishukaibaoqinianxingmingshuP4071xintanA_New_Exploration_into_Dunhuang_Manuscript_P_4071_a_Horoscope_Text_Dating_to_the_Seventh_Year_of_the_Kaibao_Era) l164–218、303–307区分查表的房宿和另一月位记载；转引钮卫星算女宿1度，非本轮实际星历重算。房日兔属于待追的历日宿直，不能自动等同27宿本命算法或实际太阴经度。P4071命宫取天蝎、对宫金牛为身宫是论文依据该案的解释，不与紫微安命身算法混为一谈。未获写本原叶，不据一值相同认证直接传承。保留CALENDAR_MAPPING_UNRESOLVED。

**可复查第二命例路线。** 葛文参考17为靳志佳《俄藏黑水城文书5722中的十一曜位置探析》，《中国科技史杂志》2021(2):215–224；[2019国家社科项目中期报告](https://www.nopss.gov.cn/n1/2019/1210/c417187-31499412.html)明确该研究前期报告涉及5722坐标、月位来源及西夏历日，仅会议概要，不是原文或原叶。参考18为《宿曜運命勘録》，《続群書類従》第31辑上（1999，葛文引用p436、月位p429）。本轮找到[宫内厅图书寮文库453・2/0695卷908](https://shoryobu.kunaicho.go.jp/Toshoryo/Detail/1000168440695?start=21)，明确收宿曜運命勘録、本命抄、建天全書，宿曜条为模写；文化13年只标本命抄，不倒填整册或宿曜成书日期。馆方直接链接[东大史料编纂所manifest51](https://clioapi.hi.u-tokyo.ac.jp/iiif/81/tdata/zokugun/zokugun0851-0921/51/manifest)、[52](https://clioapi.hi.u-tokyo.ac.jp/iiif/81/tdata/zokugun/zokugun0851-0921/52/manifest)、[53](https://clioapi.hi.u-tokyo.ac.jp/iiif/81/tdata/zokugun/zokugun0851-0921/53/manifest)对应Mirador页面已打开但正文0行，尚未获取目标原叶或manifest正文。图书馆明确出版/翻刻利用需申请，未下载或上传图像。暂作定位证据，不计三本独立实物。

NEXT：先核宫内厅三manifest实际图页、宿曜運命勘録出生日期/本命宿及尾宿4度93分，核5722论文合法公开正文与实物，再比较历日宿直和实际天文坐标。继续原有南印度方盘、明本原叶、R8大blob发布及R9全库查重；R9补T1299/T21n1299/0394c17/0395b04/宿曜經/宿曜经/宿曜運命勘録/宿曜运命勘录/宿曜御運勘錄/1000168440695/453・2/0695/zokugun0851-0921/5722/靳志佳/靳志佳俄藏黑水城文書。transmission_impact=NONE，TW-OPEN-0059及0006保持OPEN，正式计数、Matrix、graph、core不变，不终验。


### 12v. 865年目录直接见证、唐宋西夏四案例技术迁移与洞微百六独立重放（2026-11-27）

同对话基线HEAD `bc16572616b35e0754edd445b1ee8b8b07c08288`、tree `9c6a32d8b79785d69430052d806201f05ec4cf44`，最近3提交及docs tree六权威blob与12u完全一致；20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity成功。沿用本对话12u已完成权威原blob解析、五P0及0059检查，不宣称R2快路径通过。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0；根647条对1078038/6382/5722/T2174A/都利聿斯/都利華斯/三辰通載/三辰通载/秦光永/洞微百六/宿曜御運録/f19736ada27e31239555cf90e2e402ff仅命中中華古籍聯合書目综合查询记录，279分片未全查，不能断定新来源。R8发布阻塞未解除，仅保全待准入检查点。

**日本可定年书目及版本纠偏。** 宗叡《新書寫請來法門等目錄》[CBETA转录 T55n2174A p1111b20–24,c01–06](https://deerpark.app/cbeta/T2174A) 实际读得“都利聿斯經一部五卷”，紧接七曜禳災決、七躍二十八宿曆、七曜曆日；末署唐咸通六年六月至十月长安西明寺求写、日本贞观七年十一月十二日归东寺重勘定（865年，原历日未换现代日期）。这是目录文本的直接证据，未见865年实物；Mak 2014 p108注15作都利華斯經，本次CBETA2026.R2传文为聿，保留异文，待大正藏图像/底本而非径改。传入文献题名和五卷数可证，不等于该批书今存全本或五卷与四门/宋代歌诀同版。复核Mak原刊[SCIAMVS 15 pp114–115](https://www.sciamvs.org/files/SCIAMVS_15_105-169_Mak.pdf)截图index9–10：日本《宿曜運命勘録》对《聿斯经》引文存在改写；原作者保留宗叡五卷与日本引文关联假说，且指出《梵天火罗九曜》题署一行及罗计材料有可疑后入成分。不得将同一论文重复计作独立来源或认为罗计必为原《聿斯经》内容。宫内厅51/52 manifest仍不可读；另定位[NDL 1927年续群书类从第31辑上](https://ndlsearch.ndl.go.jp/books/R100000039-I1078038)，PID1078038、DOI10.11501/1078038、80-221、2010数字化，馆内限定且不属个人/图书馆送信对象，明确BLOCKED_SOURCE_ACCESS；不绕过限制，不据目录find未命中断言无宿曜文本。与宫内厅卷908模写物件、1958/1999引用刊本区别。1927版目标叶尚未读。

**独立现代比较研究与黑水城文本身份。** [秦光永《9—14世纪星命知识在中国的传播与本土化》](https://lwbi.cbpt.cnki.net/portal/journal/portal/client/paper/f19736ada27e31239555cf90e2e402ff)《史林》2025(2):32–42+217，期刊页面实际核摘要及注(43)(44)(68)(73)(75)–(82)，原刊正文未开放；[公开转载](https://www.astro-read.com/zh-hans/arcview/208) l39–78有文体、表1及推运比较，但未核原刊表或西夏原叶。四对象：宿曜運命勘録、宿曜御運録（九曜、出生与行年星位，后者引“本文”不明引聿斯）、康遵974批命课（十一曜、行年与禄马）、谨算5722（十一曜图、星禽术、三方主、三元、洞微大/飞限、行年与大小运）。据秦文，后者主要使用出生盘而非逐年星历；这是四例的二手结构归纳，非整个宋代全部术式已转变。秦注68给出俄藏Инв.№6382《重刻聿斯歌并注》原件线索，照片据作者尚未出版；不得将6382、5722混同，亦不得把同册另一《天险桑星大镜》（转载作大曜）当作独立物理见证。注82指韦兵、秦光永2017《谨算》星命解读 pp249–264；注81英藏359洞微残叶、2018 pp223–227。靳志佳2021 5722十一曜研究仅得目录及2019报告/综述，未获正文/坐标表；原定尾宿4度93分未核。陕西师大[2021学术会议报道](https://his.snnu.edu.cn/info/1511/598871.htm)记录余欣以6382类新材料与谨算、灵台经、静嘉堂三辰通载、希腊波斯星学互证，是独立研究线索但非原叶裁决。秦文提出行年数据可能由翻查/错误星历引起（注80），与钮卫星多命例窜入、葛2025部分行年重放不同；保留三候选，不把某篇作者归因当作已验证历史事实。秦文所述出生盘化不等于紫微/子平由此直接派生。

**《三辰通载》独立传文检验与定年隔离。** [山东大学《子海珍本编·日本卷》目录](https://zhyhb.sdu.edu.cn/info/1116/2247.htm)列据静嘉堂影宋刊本影印；秦注73指现代影印pp479–747；余欣报告称清人影宋抄本，[皕宋楼藏书志卷51](https://www.shidianguji.com/zh/book/CADAL02091390/chapter/1lb03jo5xvbc4) l198–223明确旧目录34卷、此本30卷并推测首尾完具，[文献通考卷220](https://zh.wikisource.org/wiki/文獻通考_(四庫全書本)/卷220)亦34卷。此为卷帙差别而非自动缺失四卷；影宋不等于实物宋刊，具体copy、年代及是否同一版未定。[识典电子传文目录](https://www.shidianguji.com/zh/book/7461522579262537769/chapter/1loio46bnc3kq) l288–321直接显示卷29洞微百六、卷30竹罗三限及西天聿斯经；[卷29起限](https://www.shidianguji.com/book/7461522579262537769/chapter/1lomxizhdeqrz) l10–16与[卷29后段](https://www.shidianguji.com/zh/book/7461522579262537769/chapter/1lomxizl62kun) l8–18、53–61、89–97。未核识典电子传文底本与静嘉堂原物对应，暂不把其转录当宋原叶。按传文起限命15、貌10、福11、官15、迁8、疾7，工具求和66；妻11、财兄各5（“五年强”候选）、田宅子孙奴仆各4.5，合12宫100.5年，与后段“百年六月”一致；“百六”不可自动当106年。原文另有五星增减、生日月时交限、小限从命宫一岁按天轮顺/地盘逆、生日交限、男女同向。区分基本数、星曜增减、宫位移动、交限历日，不用紫微十年大限/八字十年运代入。非实测预测验证。[卷30竹罗三限](https://www.shidianguji.com/zh/book/7461522579262537769/chapter/1lomxj13kcjz7) l17–24,34–72同时记出没昼夜、三方主、七政年数及年纳音沐浴死墓绝，提供同一收本内部多种推限机制并存的传文证据。该章有大观二年戊子岁十二月初八卯时例，未据后出传文将物件断为1108年；部分OCR明显错乱，不强定完整三限算法。

NEXT：按实际底本核静嘉堂三辰通载卷29/30原叶，比较四库星学大成西天聿斯经对应字句与洞微限数；查6382/英藏359合法公开影像与5722相关2017/2021正文，继续南印度方盘及上游跨文明路径。R9查重补1078038/10.11501/1078038/T2174A/1111b20/都利聿斯/都利華斯/6382/5722/359/重刻聿斯歌并注/重刻聿斯經並注/三辰通載/三辰通载/7461522579262537769/1lomxizhdeqrz/1lomxizl62kun/1lomxj13kcjz7/秦光永/韋兵/韦兵/f19736ada27e31239555cf90e2e402ff/皕宋樓/皕宋楼/宿曜御運録/宿曜御運錄/六条有康/余欣/子海珍本編。R8正式发布、R9全库查重、原叶未决；transmission_impact=NONE，0059与0006保持OPEN，正式计数、Matrix、graph、core不变，不终验。


### 12w. 三方主序列跨文明逐项重放、昼夜输入差异及两类运限的并行证据（2026-11-27）

同对话基线HEAD `ea2ded665ad1a2e1cb8561e8432b3b147ffba580`、tree `8e463d57a26c8361e19cf9acfc92de148a9af7c1`，最近3提交与docs tree六权威blob未变，20 Actions中19 success、clean-training-system in_progress，尚无exact-HEAD continuity成功。复用12u已完整解析的权威原blob及五P0/0059核阅，不宣称R2快路径通过。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0。根647对SK1609/1m1qpug7z7qcu/1m1qpugc4h9uj/7568279811106275371/1loio4scflycm/Gansten/Hāyanaratna/851bd22f-55d6-4c20-a2df-5f482875ee69/2020023517/SCIAMVS_15_105-169_Mak/三辰通載/三辰通载/星學大成/星学大成命中既有EXT-WIKISOURCE-XINGXUE-DACHENG-TIANCHU（卷一天厨，非本轮运限正文）。279分片尚未完整查重，不能认定正式新来源。R8发布阻塞未解除，仍追加待准入检查点。

**洞微基本数在两种传文中的对应与年龄口径。** [《三辰通載》卷28识典](https://www.shidianguji.com/zh/book/7461522579262537769/chapter/1loio4scflycm) l467–479、533–584与[《星學大成》总论诸限](https://www.shidianguji.com/zh/book/SK1609/chapter/1m1qpug7z7qcu) l8–16核读，二者同列命15、貌10、福/妻11、官15、迁8、疾7、财兄各5（歌称五年强）、田子奴各4.5，总计100.5。卷28 l578明说财帛兄弟各五年，故12v暂定数获此传文内部直接支持。条件演算：按命貌福官迁疾妻奴子田兄财的读取顺序，连续经过年数边界0,15,25,36,51,59,66,77,81.5,86,90.5,95.5,100.5。这个数组只是基础年数累计，非最终交限日算法，不能把半开年龄区间直接等同传文所称岁数；如正文迁移52–59、疾厄60–66、妻67–78及后段奴仆78岁交前限，涉及岁数起点/边界歧义，保留候选。原文总论中庙度增4年、旺乐增2年，歌中又见四五年、一二年，不能自动归一为唯一修正函数。卷28与前12v所称卷29分节位置有差别，本轮直接引卷28实际文本，不静默改前记录。两电子传文不等于两件已验原物，静嘉堂卷29/30原叶未取。[另一个识典书ID7568279811106275371](https://www.shidianguji.com/zh/book/7568279811106275371/chapter/1li0jioc3iux6)确有三辰通载目录，但尚未核定两个书ID的底本/实物关系，不新增独立票。

**四组昼夜次序的高特异性对照。** [《星學大成》四库传文卷七](https://zh.wikisource.org/zh-hant/星學大成_(四庫全書本)/全覽) l1334–1342、[《三辰通載》卷30](https://www.shidianguji.com/zh/book/7461522579262537769/chapter/1lomxj13kcjz7) l9–24、64–72及[CTEXT卷七](https://ctext.org/wiki.pl?chapter=645726&if=en&remap=gb) l81–82相互定位；后两传文有错字，按可读歌例保留校勘范围。条件采用传统地支与黄道宫对应（戌白羊、酉金牛、申双子、未巨蟹、午狮子、巳双女、辰天秤、卯天蝎、寅人马、丑磨蝎、子宝瓶、亥双鱼），火象寅午戌昼日木土夜木日土，水象亥卯未昼金火月夜火金月，风象申子辰昼土水木夜水土木，土象巳酉丑昼金月火夜月金火。对照Dorotheus Carmen astrologicum I.1（Pingree英译公开转载[卷一](https://unifiedastrology.wordpress.com/sources/hellenistic-sources/carmen-astrologicum-of-dorotheus-book-one/)及[图书目录](https://books.google.com/books/about/Carmen_astrologicum.html?id=XiZhP1MiUbEC)；英译公开传文，未取得阿拉伯原校本目标叶），工具逐组比较8序列/24槽，全部相同。这是比12宫数量/三合名称更强的机械结构对应，但映射、源版本与历史中介仍是独立假设；不新增直接传承边。尤其须区分选择哪个宫组：Dorotheus在不同问题取上升宫、日月所在宫等，竹罗例以丑安命后取巳酉丑组、按实际日出没区分昼夜，卯时因小寒后仍属夜生候选取月金火。此输入选择并非所有技术一律等同。卷30土星起巳的25年丑、26年回寅例及每步5年、奇偶宫跳转为原例待细分，不依据局部例强定全算法。

**直接对照后世合用说明及混融。** 四库传文l1334明确编者赞成同时使用竹罗、洞微及飞限，冲突时竹罗优先、飞限其次且容权衡；该句说明同一编纂系统内并存不同技术，不证明前代已有完全相同的优先顺序或效果验证。卷30与四库卷七一致的另一个星曜年数表水24木30土26金26火28、日月取水火，与局部步长水1火2木3金4土5是两张不同参数表；不混同。另明确将生年纳音沐浴死墓绝四杀作为交限判别条件，直接见证域外星曜规则与本土干支纳音要素在同一传文中合用；不能由此推出四柱十二长生或紫微大限即源于竹罗。

**原刊影像重读及异文约束。** Bill Mak 2014 [SCIAMVS 15 pp141–143](https://www.sciamvs.org/files/SCIAMVS_15_105-169_Mak.pdf)实际截图index36–38，p141并列《西天聿斯经》与《星学大成》卷二三方主歌及Dorotheus I.1/Tetrabiblos I.18；p142注7明确Dorotheus I.6昼夜火土判法与该中文段相反，但I.10/I.26又有相反说，不能据三方表一致推广到所有吉凶规则。p143明确区分原文二五/室与作者校改三五/奎；[识典卷七西天聿斯经](https://www.shidianguji.com/book/SK1609/chapter/1m1qpugc4h9uj) l6仍作二五、室。Mak英译火旺摩羯28度与中文四与七不应直接覆盖，截图中注13另列斗18/21度映射丑宫4/7度；需另核坐标换算及作者解释，保留既有上游旺度争议。此次复用既有Mak论文，不重复登记。

**印度Tājika作为传播方向反例。** [Martin Gansten 2018，隆德大学机构记录](https://lup.lub.lu.se/search/publication/851bd22f-55d6-4c20-a2df-5f482875ee69)，History of Science in South Asia 6:162–199，摘要明确考察13世纪Samarasiṃha与1649年Balabhadra汇编，认为重要上游可能是9世纪阿拉伯语Sahl ibn Bishr。此轮仅摘要，未分析PDF正文。[Gansten 2020《Hāyanaratna》英译公开分节](https://www.wisdomlib.org/hinduism/book/hayanaratna-the-jewel-of-annual-astrology/d/doc1500935.html) l60–103，[LOC目录2020023517](https://www.loc.gov/item/2020023517/)确认梵英校订本、1649年作品年代。该节Tejaḥsiṃha将四组第1/2/3宫分别分昼夜倒置与恒主，Samarasiṃha另将昼或夜主与恒主两者按强弱取其一，所列四组主星与上述希腊/中国三方表同组。相同主星组合不等于同一实际选主算法。这是印度传统内部另一路有年代证据的波斯—阿拉伯语知识适应案例，不等于南印度古吠陀术的全部，亦不能倒推其13–17世纪文本是唐宋中国星命术上游。此处明确不同传播候选并行、非单线印度抄入，不作紫微直接传承结论。

NEXT：优先检索可公开静嘉堂《三辰通載》卷28–30底本及两识典数字对象元数据、黑水城6382/359/5722原叶；进一步比较日月选组三方与紫微三方四正及地支三合的对象/作用域，避免把几何结构等同同一机械规则。补查Gansten 2018原刊及更早梵语/中古波斯和阿拉伯语文本，保留南印度方盘原图优先事项。R9补SK1609/1m1qpug7z7qcu/1m1qpugc4h9uj/7568279811106275371/1loio4scflycm/645726/ Gansten/Hāyanaratna/Hayanaratna/Tājika/Tajika/851bd22f-55d6-4c20-a2df-5f482875ee69/2020023517/Samarasiṃha/Sahl ibn Bishr。R8正式发布与R9全库查重尚未完成，transmission_impact=NONE，0059与0006保持OPEN，正式计数、Matrix、graph、core不变，不终验。


### 12x. 五行三辰与黄道三分的同形异义、紫微三方四正术语范围（2026-11-27）

同对话基线HEAD `325c9715956cf7ab2c97cc4ff468a5435d3b71c3`、tree `bd06931447623e8a6cfcd2458e6d74b5571486c0`；最近3提交及docs tree六权威blob未变，20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity成功。复用同对话12u已完整权威解析与五P0/0059核阅，不冒称R2快路径通过。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0。根647条对淮南子/淮南鴻烈/五行大義/五行大义/三命通會/三命通会/1078787/4468520/SDZJ0170/7356346222958870579/1jvzootg40y05/1jvzootg431ut命中15条，含既有EXT-NAJ-ZWDSQS-MING-1078787、EXT-SHIDIAN-ZWDSQS-LATE-ZI、EXT-SHIDIAN-ZWDSQS-FOUR-TRANSFORMATIONS、EXT-WIKISOURCE-WUXING-DAYI-GANHE；复用对象，279分片未全查，不断言正式新来源。R8大型台账正式发布仍阻塞，只追加待准入材料。

**本土早期五行三辰与后世三合局并非全同。** [《淮南子》天文训电子传文](https://zh.wikisource.org/zh/淮南子/天文訓) l199–209及[CTEXT段18平行文](https://ctext.org/text.pl?if=gb&node=3072&show=parallel)，西汉作品层，未核西汉实物或目标原叶。按生/壮/死记木亥卯未、火寅午戌、土午戌寅、金巳酉丑、水申子辰。土与火共用同一三元集合但起点顺移四位。原文上下文有刑德、历日与八徙，不得据此断汉代已有成熟子平三合化局、完整十二长生或紫微四正。[京都大学人文科学研究所《五行大義》卷二](https://www.zinbun.kyoto-u.ac.jp/~takeda/kyoudou/gogyou/gogyoutaigi/gogyo_gogyo_02_g.html) l13–16、20–22记录土寄旺火乡、四季土各具生死（辰土生子、未土生卯、戌土生午、丑土生酉）、四季各18日及定位旺未墓辰的不同论述；土的生旺死不能自动合为一张唯一表。第八论合l54–55主述干合及日月会次与斗建的六合，不能仅因章节题为论合就把现代三合表归为该段原文。该网页是电子转录而非经验证古本。后世[《三命通會》卷二论支元三合](https://wk.100ke.info/zh-hant/三命通會/卷二) l407–413以申子辰水生旺库为例，要求三字齐备方以三合化局论，四行皆赖土成局，另列辰戌丑未全作土局。此为该收本明确条件，不推广为所有后世流派的唯一半合/合化政策；文本将生日支关系应用于命局、财官印等，需另核该例取丙丁的参照层，勿默认为已严格区分年干/日干。

**结构与语义分离重放。** 十二支按子至亥零基i，三合集合T(i)={i,i+4,i+8} mod12，对宫O(i)=(i+6) mod12，四宫集合T∪O。工具枚举12基点，12/12所属三合正确且四宫各异。以寅为命例，三合寅午戌、对宫申，名义等分黄道映射为人马/狮子/白羊/双子。采用12w传统宫支映射时，四组中国五行与西方四元素依次寅午戌火/火、亥卯未木/水、申子辰水/风、巳酉丑金/土，仅1/4名称相同。元素名称也非物理概念同一证据；空间同形不意味着星曜主宰、成局条件、体用、断法、历史来源同一。120°/180°只表示名义等分宫的角距离，不是中国不等宿宽或实际天体相位的必然数值。

**紫微古籍中‘三方’有不同指称语境。** [识典SDZJ0170卷二骨髓赋注解](https://www.shidianguji.com/zh/book/SDZJ0170/chapter/1jvzootg40y05) l9分别讨论对宫体用、三合源流；l97寅命午戌朝拱及酉命丑巳朝拱；l107列迁移官禄财帛为会命的外三宫。[定富贵贫贱十等论](https://www.shidianguji.com/zh/book/SDZJ0170/chapter/1jvzootg431ut) l9–23同时见三合拱照、三方、三方四正和守照拱冲用语。[卷五谭星要论](https://www.shidianguji.com/zh/mid-page/7356346222958870579) l11明确把迁移、财帛、官禄称三方，另看本命及身、福德；与今天常称本宫加两个三合宫为三方、再加对宫的记法，其最终四宫集合可以一致，但三方一词外延不必相同。另该段把身命迁财官福六宫名八座，身宫可重叠，不能按数字名称擅自补两宫。现代通用定义仅作结构规范化，不以此强改古文。既有[日本国立公文书馆子060-0001/1078787](https://www.digital.archives.go.jp/file/1078787)目录搜索命中，但直开403；本轮未取目标原叶，未证识典转录与公文书馆具体扫描逐页绑定，不把陈摶题署当北宋实物年代、不把同一收本的不同段落计独立版本。维基全览/卷三find出现无命中但检索片段及识典有正面读法，不据搜索失败判原书缺词。

**七政三方主与紫微四宫会照需分开。** [《星學大成》卷七](https://zh.wikisource.org/zh/星學大成_(四庫全書本)/卷07)及[CTEXT](https://ctext.org/wiki.pl?chapter=645726&if=en&remap=gb)明确竹罗三方主为昼夜分组的星曜主宰，并参与推限；紫微上述传文则考宫位已有星曜的守照拱冲，不以三方主序列确定主宰；四柱三合则检测命局实际出现的地支是否构成局，不能因数学上每个支有三合伙伴就当命局已成局。注意[同书卷26](https://zh.wikisource.org/zh-hant/星學大成_(四庫全書本)/卷26)传文另列洞微、小限、竹罗、黄泉急脚优先顺序，与卷七偏重竹罗/飞限的叙述需分章节、体裁和适用任务核查；不得简单确立全书统一排序。卷26检索可见三方俱吉与四正逢凶相对句，但该句未定义四正的精确索引，暂不等同紫微四宫集合。未检验任何预测效力。

NEXT：从术语同形转向十二宫功能名称、排列与命宫定位的比较，追敦煌P4071及西夏5722、唐宿曜文献、七政与紫微的父母/相貌、福德/官禄、兄弟/财帛实际次序。继续核南印度方盘、静嘉堂原叶及独立紫微早本。R9补淮南子/淮南鴻烈/天文訓/天文训/三辰皆木/土生於午/五行大義/五行大义/gogyo_gogyo_02_g/三命通會/三命通会/論支元三合/SDZJ0170/1jvzootg40y05/1jvzootg431ut/7356346222958870579/譚星要論/談星要論/三方四正/1078787/4468520/星學大成卷26。R8发布、R9全库查重与原叶未决；transmission_impact=NONE，0059、0006保持OPEN，正式计数、Matrix、graph、core不变，不终验。


### 12y. 十二人事宫顺序的跨体系对照、命身分离算法及1905印度方盘定位（2026-11-27）

同对话基线HEAD `89786f1de73cf287ccbbc830ea199287ffa8f45e`、tree `85ef2aa1697c2161ea22b9648d410fb5e0cb47f3`；最近3提交与docs tree六权威blob未变，20 Actions中19 success、clean-training-system in_progress，无exact-HEAD continuity成功。复用12u本对话原blob完整解析和五P0/0059核阅，不冒称R2快路径通过。正式1.1587.0、1499/279、222/222、819/581、59 OPEN五P0。根647对brihatjataka00varaiala/brihatjatakavar00iyergoog/doc1501578/Chidambaram/通命十二宮/通命十二宫/P.4071/P4071/星學大成/星学大成/安身命例/4468520/1078787命中既有EXT-WIKISOURCE-ZWDSQS-V2、EXT-NAJ-ZWDSQS-MING-1078787、EXT-WIKISOURCE-XINGXUE-DACHENG-TIANCHU；279分片未完整查重，不认定新正式来源。R8大型台账发布仍阻塞，只追加待准入材料。

**四种人事宫顺序、方向及同义归一。** [Bṛhat Jātaka I.15梵英传文](https://www.wisdomlib.org/hinduism/book/brihat-jataka-by-varahamihira-sanskrit-english/d/doc1501578.html)列从上升宫开始身体、家庭、手足、亲族、子女、敌人、妻、死亡、吉祥、事业、收益、支出；这是第十五偈的主要词义，不代替各宫其他同义及后代印度学派，未核梵文古叶。[葛业静2025论文转载表1](https://www.astro-read.com/arcview/241) l42–51将P4071已失《十一曜见生图》复原为命、财帛、兄弟、田宅、男女、僮仆、夫妻/身、疾厄、迁移、官禄、福德、困穷；支序卯寅丑子亥戌酉申未午巳辰，对应天蝎、人马、摩羯、宝瓶、双鱼、白羊、金牛、双子、巨蟹、狮子、双女、天秤。这个表是研究者复原，不是存世原图；本轮ResearchGate原文地址DisabledError，未核原刊表或写本原叶，且表中太阴等星位存在与早先正文不一致，故不据表定星位。 [《星學大成》四库传文卷04](https://zh.wikisource.org/zh-hant/星學大成_(四庫全書本)/卷04) l117明确命、财帛、兄弟、田宅、男女、奴仆、妻妾、疾厄、迁移、官禄、福德、相貌，并以家庭生活关系、东升西没、天上地下等解释宫序。并不证明相貌一定由困穷改名。 [《紫微斗數全書》卷二](https://zh.wikisource.org/zh-hant/紫微斗數全書/卷二) l137–145直接见命、兄弟、妻妾、子女、财帛、疾厄、迁移、奴仆、官禄、田宅、福德、父母，男女俱逆布。归一男女/子女、僮/奴仆、夫妻/妻妾后，P4071复原与七政传文11/12同序，末宫异；七政与紫微2/12同序（命、福德），逆转且固定命宫也只有4/12（命、妻、疾、迁），实际枚举任意12旋转及两方向最大4/12。后一结果仅反证简单旋转/镜像即可重合，不是统计历史证据或相似概率。四体系均须区别黄道十二宫/支位与从命宫起的功能十二宫，不把印度敌人/奴仆等词强判同义。P4071复原与紫微的功能宫序均可用逆支步长表达，但起点与功能位置不同。

**命身计算是强区分项。** 卷04 l117作者记录其他星家常以太阴为身，同时明确提出以命对宫为身，称其独得；太阳立命、东升/西没解释与实际天文上升度、古代简化推算规则仍需分别建模。不把卷04作者一说推广至七政所有派别。P4071复原卯命酉身相对，仅单例对应，无法证明其每例固定对宫或倒推明代作者规则。紫微卷二安身命例令正月寅起月，生月基点p（子零基，p=(2+m-1) mod12），时支h（子零基），命=(p-h) mod12，身=(p+h) mod12。工具枚举12月×12时=144组：身相对命的顺支差仅0/2/4/6/8/10，各24组；以逆布功能宫定位依次命/福德/官禄/迁移/财帛/夫妻各24组。只有卯酉时身在命对宫，共24/144；子午时同宫，24/144。该枚举是形式空间非实际出生概率，不处理闰月、节气、晚子时或真实天文度数，不是预测检验。两算法不等价，即便存在共同命名亦不能判定直承。紫微全书传文自有闰月政策，历史变体保持独立，不重开排盘。**前一轮聊天示意图校正**（原12x仓库四宫集合正确）：按卷二逆布，寅命时戌为财帛、午为官禄、申为迁移；前轮图中午戌财官标签颠倒，明确纠正，不改12x既有记录。

**南印度方盘延伸证据。** [1905马德拉斯修订增订二版英译本](https://upload.wikimedia.org/wikipedia/commons/c/c2/The_Brihat_jataka_%28IA_brihatjataka00varaiala%29.pdf)电子提取l15–36、60–70可辨N. Chidambaram Aiyar、Thompson & Co.及1905版序，区别1885初版（译者1892年去世，兄弟整理二版）。PDF提取l2159–2161描述方形Rasi Chakra；l2700–2723印页100描述Rasi Chakra及Ashtakavarga方形十二外围格。实际截图请求index0返回25,869,114字节过大，未见目标图像，提取的visual_element不是原页目验；不得称1905实见方盘或倒推6世纪作者原图。 [Commons物件元数据](https://commons.wikimedia.org/wiki/File:The_Brihat_jataka_(IA_brihatjataka00varaiala).pdf)为306页/IA同一数字替身，不计新物件。l1105–1132印页13–14还列Kendra第1/4/7/10、Panapara第2/5/8/11、Apoklima第3/6/9/12，译注标后两项为希腊术语；注意此为译者注非古文断言。与紫微命财官迁第1/5/9/7集合不同，不混同三方四正和印度四角组。下一轮优先从可直接展示的单页图或独立合法影印取1905和1885目标图，并核定南印度地域与最早物件，不能用1905复刻冒认1885或古贝叶。 

NEXT：继续比较早期印度/希腊化十二功能宫文献的术语及次序，寻找有定年中国十二宫结构、命宫规则的实际中间版本，并核1905/1885印度方盘目标原页及EAP贝叶原图。R9补Bṛhat Jātaka/Brihat Jataka/Brihat Jatakā/Varāhamihira/Varaha Mihira/Chidambaram Aiyar/Chidambaram Iyer/brihatjataka00varaiala/brihatjatakavar00iyergoog/doc1501578/Rasi Chakra/Ashtakavarga/通命十二宮/通命十二宫/十一曜見生圖/星學大成卷04/星学大成卷四/命對宮之度為身/安身命例/安十二宮例。R8发布、R9全库查重及古本原叶未决；transmission_impact=NONE，0059及0006保持OPEN，正式计数、Matrix、graph、core不变，不终验。
