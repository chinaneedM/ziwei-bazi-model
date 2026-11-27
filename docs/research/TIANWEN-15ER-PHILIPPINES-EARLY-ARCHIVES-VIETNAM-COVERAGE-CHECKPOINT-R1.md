# 15ER｜菲律宾早期档案定位与越南现有来源覆盖复核

2026-11-27。广度优先检查点；新增候选未正式准入。

## A｜精确远端恢复

HEAD e95eb9333cee274ad9315a63a547ba00a048398b，tree d28a43a30238c47c550cfe43f1b993fd16cfd1b6。六个权威blob逐项与tree绑定相符；在连续性CI排队时直接完整解析六份权威JSON，五项P0原状保留。后取得 [exact HEAD continuity run45930120636](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45930120636) / job140280565817 SUCCESS，父提交54项风险保全PASS，62项ledger、7项R2测试PASS，视图4616字节；旧15EQ请求STALE_CHECKPOINT为预期。此前分页读取284项Actions时247成功、17执行、20排队；不以局部时间快照称全CI完成。来源1390（647+743、261片）、图495/375、Matrix222/222、54 OPEN含P0五项、核心CLOSED。

## B｜菲律宾早期本土调查候选

1. [DLSU机构馆目8290](https://animorepository.dlsu.edu.ph/etd_bachelors/8290/)（L32–60、69–92）：Benito Shiu, Carmen Tan, Cassandra Yap，1989，Courtship and marriage rituals of selected Filipino-Chinese，心理学学士论文；12对华人夫妇及2名媒人、2名astrologers参与访谈。纸本166叶、TU04353、Henry Sy Sr. Hall 12F档案馆。馆目明确全文未开放。可证研究调查包含占星从业者，不可推出这些人使用子平或紫微，亦不可回推首次传入。
2. [DLSU机构馆目17441](https://animorepository.dlsu.edu.ph/etd_bachelors/17441/)（L21–32、46–77）：Wendeline Que Chan, Marjorie In Ching, Judy Siao Sy，1991，A study on the practices of superstitious beliefs among the Filipino-Chinese in courtship and marriage；行为科学学士论文，192叶、TU05380、同馆档案区。页面无实质摘要正文且全文未开放。仅题名/馆目线索；不能声称已核合婚、生辰或具体术法内容。
3. 免费公开全文未获；保留馆藏号及访问边界，不要求用户注册或付费。不新增历史来源/图谱，不将1989/1991直接当作四柱或紫微同期证据。

## C｜1910司法文书的地理与证据反例

[ChanRobles受传判决](https://chanrobles.com/cralaw/1910marchdecisions.php?id=95) G.R. No. 4718, 1910-03-19, 16 Phil 137，Sy Joc Lieng v. Petronila Encarnacion；L103–121多数意见对1847中国婚姻及证词可信度提出异议、婚书未出示；L755–771、991–1004证词提及取女方eight characters及红轿，但地点为Lau Poan/Am Thau等中国村落。[jur.ph受传同案](https://r2.jur.ph/decisions_html/sy-joc-lieng-v-encarnacion.html) L352–375是异议意见，区分1847年中国婚礼主张与1853年菲律宾天主教婚礼。此为同一判决的两个数字载体，不是独立史证；原卷及官刊未核。只能作为华人跨境婚俗在1910年司法文本中的受传线索，不能证明1847年菲律宾本土已有四柱，不能将礼俗取八字当完整子平算法。保留这一反例，避免地理/术法误归属。

1988旅美候选及2015原发布者定位词复用15EQ E/F，仍未完成新增字面查重。当前12词请求覆盖上述两论文、判例、旧跨境和原刊定位。

## D｜越南历史框架：九个已登记分片正文复核

精确manifest blob 5811df962256220d88699f11fd8e30426e2e5630，读取九个按Vietnam/Hannom等题名筛出的分片实际JSON，逐片source_count吻合，共30条：13ZV(10)、14N(1)、14P(2)、15R(3)、15Y(2)、15Z(3)、15AA(4)、15AB(3)、15AC(2)。仅为该具名子集，不能声称全库越南来源只有30条。manifest未见15CY题名分片；此前15CY定位只是线索，另查树中相关文档而非凭路径虚构来源。

- 古代双体系：15Y 2026学术引录黎贵惇《芸臺類語》及范氏家谱；15Z 1820编引与A.909/VHv.1353不同抄本、1996介绍、1994缩微目录；15AA R.118未断年抄本（2009数字化）、2019家谱版本及1990馆号引录、现代越译。18世纪作者论述与现存抄本年代、现代转录严格区分，原目标叶核读仍需依已有未决事项推进。
- 汉喃传统：13ZV R.293、AB.316/552、AB.424、VHb.165等未断年抄本馆目；15R 胜严寺2013移交与TN208/TN213数字记录，不能以2013认定抄成年代。
- 现代紫微：14P Thái Thứ Lang受传1956序年与2012馆藏；14N Nguyễn Phát Lộc 1974序追述1972；15AB Vũ Tài Lục 1973受传自述与旧书商1972说法，以及1970/1972旧书目录；15Y 2011/2012国家书目含中州三合派。保持版年异文及原刊记缺口，不重复准入。
- 现代四柱：15AC 林世德1973西贡作者序受传与1974书商刊年说法，13ZV 2011《子平真詮》越译书目。不能据现代重排PDF确定初版。下一步优先查1950–1970年代四柱独立著述、1990年代后越南本地学术与出版、未登记版本，逐项查重后准入；紫微四柱分开。

## E｜任务边界

TW-OPEN-0054继续OPEN，未取得全文/原页/明确术法的线索不升格。既有54开放问题、五P0、1390来源和图谱均不变；本批仅增加可复查候选和越南已有覆盖核对，不改算法。NEXT：领取15ER查重，按受传司法文书/学位馆目/本土术法边界裁决，若无公开原文则转越南未覆盖年代。
