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
