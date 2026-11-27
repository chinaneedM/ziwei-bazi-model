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
