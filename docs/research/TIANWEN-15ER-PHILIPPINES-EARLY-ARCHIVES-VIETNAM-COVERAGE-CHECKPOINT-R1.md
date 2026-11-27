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


## F｜15ER精确全库查重领取、证据分级（2026-11-27，前向追加）

HEAD 4cdf19ab964d477ced0efa694b475f4d405d372f / tree a2b58ae34553f94bedc5a05cff1938db51c7ac5e，六绑定逐一匹配。精确 [continuity run45930714486](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45930714486)，job140282430925 SUCCESS，62项ledger、7项R2测试通过。分页Actions瞬时读取259次success记录、16运行、10排队（284 unique；逐页实时变化造成计数快照并非严格同一时刻，不能称全通过），无所见失败；本分支无开放PR。

查询15ER-philippines-early-archives、checkpoint TW-CHECKPOINT-15ER-PROVISIONAL-20261127、request blob de48ed58a42e317c87e5e9fc0fb0fc0370d5a71c、manifest blob 5811df962256220d88699f11fd8e30426e2e5630、scripts/project-context-r2.py blob 3387254ce53ec0a1f1a3b779291e0c40997bf190。PASS，scope ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY，262文件、1390记录。原请求12个逐词计数：TU04353=0；TU05380=0；etd_bachelors/8290=0；etd_bachelors/17441=0；Courtship and marriage rituals of selected Filipino-Chinese=0；A study on the practices of superstitious beliefs among the Filipino-Chinese=0；Sy Joc Lieng=0；Sy Quia=0；G.R. No. 4718=0；Chang Tai Ei=0；la-xpm-1988-07-23-mn-6345-story=0；plan-your-destiny-with-dato-joey-yap=0。matching_files=0、hits=[]、truncated=false。仅字面查重，不自动准入。

裁决：1989 DLSU为占星从业者参与的调查线索（摘要层）；1991 DLSU仅目录层，不能提升成四柱或紫微证明。1910判决为受传文献中的争议中国婚俗，不是菲律宾本地术法；两个判决网站只算同一判决。1988候选为海外从业、全文访问受限；2015原发布者归档对应已准入同一采访，不能新增为独立事件。上述均不计为新增菲律宾本地四柱/紫微独立术法来源；保留所有定位与限制，不关闭TW-OPEN-0054。

## G｜越南四柱出版和教学候选（未查全库、未准入）

1. [Tử Bình Thuyết Minh 69页数字重排](https://www.huyenhocvietnam.vn/upload/attach/hhvn2021745154542q7Lx50.pdf)，PDF标 Microsoft Word，页眉 tuvilyso.com。核PDF第1、67、68页截图（0-based 0、66、67）；第一张从源流/阴阳正文开始，无原刊名页；第67页参考书目列台中1968/1969出版物、台北1972《Tử-Bình chân thuyên》及香港1973《Tử-Bình túy ngôn》，并有署HOA-LƯ的拟刊续作 Tử-Bình bí giải 告示；第68页保留原书页次至103的勘误，与69页重排分页不等。正文L3281–3359有四柱、大运、小运、命宫、胎元及胎息的总结与算例；仅为受传文本范围，不可据OCR/重排表格直接改机械规则。作者身份候选 Đỗ Đình Tuân；[旧书商记录](https://muabansachcu.vn/products/tu-binh-thuyet-minh) L273–283著录1974、自刊、100+页；[另一后出作者序言/书目PDF](https://www.huyenhocvietnam.vn/upload/attach/hhvn2021745224513chx3Bn.pdf) 搜索片段标1975 HOA LƯ，尚未核页，不视为已核正文。两刊年说法未决；未见原刊版权页，不把重排发布日期、书商年代、后出书目混为一谈。参考书目提供越南子平与台港文本接触候选，不证明直接师承、具体版本抄袭、古代源流准确性；续作拟出版不等于实际出版。
2. [越南国家图书馆2022年2月国家书目](https://nlv.gov.vn/dmdocuments/tmqg-02-2022.pdf)，PDF第10/11页（0-based 9/10）截图直接核读：条目125 Tử Bình nhập môn（文本提取误作Tư Bình，影像为Tử Bình），Nguyễn Ngọc Hải编、Nguyễn Văn Chinh校，Hồng Đức，河内，2021，442页，s502625；条目131 Tự xem Bát tự Tứ trụ，Quảng Tuệ，Thanh Hoá，2021，287页，s503300，明确再版。两独立书目条目，不等于两独立传承谱系或两个原书全文；2022目录日期区别于2021版年，再版不能推定初版年。
3. [Học viện lý số 八字子平教学提纲](https://hocvienlyso.org/de_cuong_mon_hoc_bat_tu_tu_binh.html) L62–90、118–126、255–388：公开列格局及日主旺衰流派、节气及地方时、四柱与八宫、行运、在线/线下教学，署讲师 Hoàng Mạnh Trung。可作当代自述课程内容候选；具体发布日期需页面再次核对，不以搜索引擎相对时间反推；非国家认证学历或完成授课的独立证明，非预测效力证据。
4. 后续目录检索优先：Tử Bình Thuyết Minh / Tử-Bình thuyết minh / Đỗ Đình Tuân / Đỗ đình Tuân / Hoa Lư / hhvn2021745154542q7Lx50 / Tử-Bình bí giải / s502625 / s503300 / Nguyễn Ngọc Hải / Quảng Tuệ / de_cuong_mon_hoc_bat_tu_tu_binh / Hoàng Mạnh Trung；必须先做完整登记库字面检索，再做语义/同物件消歧；不以九个具名分片代全库。补1950–1960年代及1990–2000年代，优先机构原目和原刊；当前未找到足以断代的这些时期新证据。

本追加仅为既有检查点的查询结果保全、分级和待核候选，未变更六权威JSON、正式登记量、图谱、开放问题或排盘算法；既有NEXT仍有效（F节领取已完成，G节查重和原刊/出版层核实尚待完成）。所有未决事项继续OPEN；不把此追加当正式15ER准入完成。


## H｜越南1990—2000年代译介、海外研习及本地出版补证（2026-11-27，待全库查重）

同一会话新HEAD 8ad54f1b24c5b5e246d726db554c006ea397db88 / tree 52a4d76fe7033041bce1a58f62cee4943f375d17。上一提交仅追加文档，读取20项Actions时19成功、1运行，无该HEAD连续性workflow；未把上一HEAD成功冒充本HEAD成功。本轮不修改六权威JSON或派生视图，沿用既有15ER开放检查点和已核manifest；新请求触发现有连续性workflow，结果尚待领取。

1. **1996正式机构馆藏（优先候选）**：[胡志明市综合科学图书馆详细馆目45996](https://phucvu.thuvientphcm.gov.vn/Item/ItemDetail/45996)，L34–60、143–158；Thiệu Vĩ Hoa（邵伟华），Nguyễn Văn Mậu译，Dự đoán theo tứ trụ，河内 Văn hóa - Thông tin，1996，404页20cm；MARC001 GSL000048777，馆藏VN 1001/97，GSL_K07。此为可定位机构目录和物件索书记录，不是原书正文/版权页逐字核读，不证1996为越译初版或首次传入；机构列表与详细记录为同一目录，不重复计数。河内文化大学类似书目结果曾返回502，未作为独立确认。
2. **2005版本候选**：[Minh Khai书商目录](https://minhkhai.com.vn/store2/index.aspx?isbn=19268&q=view) L63–80，同题同作者同译者同出版社，2005-05，408页15×21cm，网站字段ISBN 19268仅为页面所示编号（不能当合规ISBN）。简介称20章；1996馆目404页且无章节记录，不可判同版重印或规则修订；仅商目层，不证明1996和2005文字一致。其他同题书商简介称24章，未获原刊，不能合并同名不同内容或据其断版。
3. **海外越文子平研习网络候选**：[Trúc Lâm Tử《Tôi học đoán mệnh khoa Tử Bình》数字传本](https://www.huyenhocvietnam.vn/upload/attach/hhvn2021745224513chx3Bn.pdf)。PDF截图0-based p0核封面署名及San Jose封面设计2003标记，正文L238有2005-01-02页脚；L20832–20861参考书目同时列陈园1994、邵伟华1991/1993、Đỗ đình Tuân 1975、Lâm thế Đức 1973及传统子平书；并述拟续作《Tử Bình Bí giải》作者赴美后未能出版、本人曾在2000年前后寻找作者、家属转述手稿散失或可能在原教学机构。此为数字受传正文的后出私人叙述，不是家属原信/学校档案或原刊证明；封面2003不是确定初版日期，2005页脚不是传播起点，不能认定作者行踪/任教事实或续稿不存在。1974两书商线索与1975作者参考书目仍待原刊。保留越南本地著作、中国大陆现代译介和海外越文读者三类线索，不建立直接师承边。
4. **2018本地出版**：[海防市图书馆2019年8月新书目录第9项](https://thuvienhaiphong.org.vn/tin-tuc/thu-muc-thong-bao-sach-moi-thang-8-2019) L111–122；Lê Văn Triệu，Thực hành dự đoán theo tứ trụ，河内Hồng Đức/Pandabooks，2018，219页，分类133.3TH552H，阅览馆藏DVN.040535，另列流通与外借馆藏。摘要涉及四柱排盘与实践，未核正文，不作算法证据或独立师承判断。出版年和目录年月分存；/node/1771是同一机构内容别名。
5. 1950–1960年代越文四柱独立刊物本轮仍未找到可确认机构馆目或原刊，不能由检索未命中断言不存在；1996之前与1975后连续出版仍有间隙。1998《Can Chi thông luận》及1990/2000其他术数书不据题名直接归入子平主线。

**查重请求**：15ER-vietnam-bazi-publication-24terms，同一checkpoint，manifest 5811df962256220d88699f11fd8e30426e2e5630，24词见原子提交内docs/PROJECT-REGISTRY-QUERY-R2.json。覆盖G/H节具名候选和标识（2018用馆藏号，邵伟华用越文名/书名及馆藏号），12词菲律宾旧结果已在F节永久保全，不重复查询。宽词可能多命中；如truncated须细分或读取完整匹配清单，不能宣称全部无重复。仅在全库查询PASS、语义/载体/版本裁决及原文证据层明确后准入正式来源。暂不改变TW-OPEN-0054及其他开放事项；来源1390、图495/375、Matrix222/222、五P0、核心CLOSED保持不变。
