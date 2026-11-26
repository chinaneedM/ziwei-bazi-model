# 15DZ：1935上海星命自学教材与派别分类（待准入检查点）

2026-11-26；父HEAD `c8461e456be4da6e8f496c616945819bd20125a3`、tree `a836a9ceedc2290ff8df556efa7d52cf04d459ad`。[精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45818426971) 62+7测试通过，准入后完整库复查245文件/1322记录/20词、2匹配文件、无截断（见15DY追加核验）。其他工作流汇总202成功、66排队、17运行，暂无已知失败，未全绿。五P0保持原状，核心CLOSED。

## 1. 1935上海出版物：四柱教材的实际传播载体

[NLC衍生目录总表](https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/NLC/民國圖書/PD2022/02) 705–717行列《醫卜星相百日通》同一组07jh011656的13数字分卷；[5161馆录衍生详目](https://commons.wikimedia.org/wiki/File:NLC416-07jh011656-5161_醫卜星相百日通_第1卷.pdf) 报民國24[1935]、中央書店总发行（上海）、两册。原图[卷1 PDF](https://upload.wikimedia.org/wikipedia/commons/5/5a/NLC416-07jh011656-5161_%E9%86%AB%E5%8D%9C%E6%98%9F%E7%9B%B8%E7%99%BE%E6%97%A5%E9%80%9A_%E7%AC%AC1%E5%8D%B7.pdf) 零基p0封面题《醫卜星相百日通》、江湖奇術、上海中央書店印行；p2书端上册标“江湖奇術無師自通”，p3上册十科总目，p4醫術目录署上海國醫學社編輯。p1为手写编号，无确切刊年。1935为目录年，本次未核原刊记，不称原页独立定年。

[第12卷5252详目](https://commons.wikimedia.org/wiki/File:NLC416-07jh011656-5252_醫卜星相百日通_第12卷.pdf) 同样报1935，目录编者字段“國醫學社 星命研究社編輯”。[原PDF](https://upload.wikimedia.org/wikipedia/commons/6/64/NLC416-07jh011656-5252_%E9%86%AB%E5%8D%9C%E6%98%9F%E7%9B%B8%E7%99%BE%E6%97%A5%E9%80%9A_%E7%AC%AC12%E5%8D%B7.pdf) 106页；零基p0目录与p8正文印页1明署“上海星相研究社編輯”，原图“星相”与目录“星命”有异，保留原图读法，不将名称相近的组织自动合并。p0–3、6–7为所检目录，涵盖四柱入门、命宫、大小运、小限、神煞、十神、格局及风水；p8–9正文印页1–2为星命原始、算命派别及起八字诀，p10印页3为推年掌诀图。版面原见，未保存独立PDF/页hash，不授机械规则权威。

## 2. 术数分类的证据边界

印页1–2叙李虚中与徐子平的对照，并认为子平法以日干为主；编者将多种江湖算命门类区分正/别派，强调无论何派仍需研读，且将其归到子平法的解释框架。只记录该编者自述，不把其起源叙事、正旁派等级或全行业覆盖当成客观史实。所核这两页没有明确“紫微斗数”题名；不能推论整个13数字分卷均无紫微，也不能将铁板算命或星命统称等同紫微斗数。起八字诀谈年月日时衔接和子时边界；此处不做规则完整校勘、裁决或算法重开。目录小限/命宫同名术语并不证明与紫微计算同法。教材书端“无师自通”直接支持市场化自学材料定位，不证明实际读者数量、教学班或师承。

[类别](https://commons.wikimedia.org/wiki/Category:醫卜星相百日通) 另列NLC416-15jh007701-98980（312页），直接详情访问失败；不是已核独立版本或第二票。卷1/12是同一组分卷，并非两独立古本。2013年[后出出版说明](https://store.showwe.tw/books.aspx?b=2566) 将王裁珊紫微著作并列为民国命理发展背景，不能据此反投1935原书紫微内容。[1949张开卷Google Books](https://books.google.com/books?id=B6fMT-qWC7wC)及[1953书目](https://books.google.com/books/about/%E6%96%97%E6%95%B8%E5%91%BD%E7%90%86%E6%96%B0%E7%B7%A8.html?id=45ArtAEACAAJ) 各报152页、《斗數命理新編》及紫微斗數命理硏究社；仅目录待查重，未得原书端或实际从业记录。未找到经核实的同期紫微报刊命例，不作缺席论。

## 3. 准入待办

在当前manifest绑定请求中同时检索原书、异文编社名、各数字物件号及张开卷书目ID；待完整CI查询结果及语义去重再决定是否准入。保留43开放风险及五P0、来源1322（647+675／244分片）、图474/375、Matrix222/222、核心CLOSED；不增加未核源或传承边。下一步核收查重、查原刊记与另本身份、继续独立民国紫微实务和区域报刊传播。

## 四、15DZ正式准入：原刊记补证与语义去重（2026-11-26）

父HEAD `5f3cd05e6f3fb8ba28c44aef96f6fff13b07ec87`、tree `f3e74fde748f240dd5800c75cadbe27c94b87b41`，[连续性CI run45819234130](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45819234130)，job139906850592，62项遗漏及7项R2测试通过。query_id=15DZ-shanghai-1935-xingming-dedup-r2-20261126，checkpoint_id=TW-CHECKPOINT-15DZ-PROVISIONAL-20261126，request blob `308f115faea27d35729564c030a71af71c1eefd6`，manifest blob `56279401774cae5a2f799affef2c8a7a147c4ce8`，verifier blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。PASS，scope=ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY，files245、records1322、matching_files6、truncated=false；20词中5252命中3文件，5161、星相研究社、B6fMT-qWC7wC、45ArtAEACAAJ、斗數命理新編、張開卷、张开卷各1，其余12词0。六文件实际对象逐一复核：root数值为张果资源号及其他哈希/工件号、13RW为CADAL01025252钱大昕、15DX为52526三友堂书目；13ZS已登记张开卷1949及1953各平台书目并有1972记录，15DQ为2012回顾，不重复登记；15V EXT-TIANWEN-15V-NLC416-1937-YUAN-MINGLITANYUAN 为袁树珊另一作品和上海星相研究社著录，仅相近编社名，不能认定与本书同一对象或组织。不是外部资料穷尽。父HEAD统计73成功/198排队/13运行，暂无已知失败，未全绿。

重新核见[5161 p2](https://upload.wikimedia.org/wikipedia/commons/5/5a/NLC416-07jh011656-5161_%E9%86%AB%E5%8D%9C%E6%98%9F%E7%9B%B8%E7%99%BE%E6%97%A5%E9%80%9A_%E7%AC%AC1%E5%8D%B7.pdf)及[5252 p0、8、9](https://upload.wikimedia.org/wikipedia/commons/6/64/NLC416-07jh011656-5252_%E9%86%AB%E5%8D%9C%E6%98%9F%E7%9B%B8%E7%99%BE%E6%97%A5%E9%80%9A_%E7%AC%AC12%E5%8D%B7.pdf)。新增直接原图证据：[第13数字分卷馆录](https://commons.wikimedia.org/wiki/File:NLC416-07jh011656-5253_醫卜星相百日通_第13卷.pdf)，[104页PDF](https://upload.wikimedia.org/wikipedia/commons/0/02/NLC416-07jh011656-5253_%E9%86%AB%E5%8D%9C%E6%98%9F%E7%9B%B8%E7%99%BE%E6%97%A5%E9%80%9A_%E7%AC%AC13%E5%8D%B7.pdf) 零基p102刊记，直接核读“民國二十四年八月再版”、全二冊、定價三元五角、出版者中央書店、總發行所上海四馬路世界里中央書店及“全國各大書坊均有代售”；编者列國醫學社和星命研究社，而5252 p0、p8为上海星相研究社。p103为封底，p0为相法目录。初版时间、校订者名字的精确字形、同一组织身份不作未证断定。全国代售为出版宣传，不证明实际成交。另[98980 PDF](https://upload.wikimedia.org/wikipedia/commons/9/9f/NLC416-15jh007701-98980_%E9%86%AB%E5%8D%9C%E6%98%9F%E7%9B%B8%E7%99%BE%E6%97%A5%E9%80%9A.pdf) 本次正文可抽取并见相似目录，零基0、311截图因14838603 bytes过大失败；此前访问限制有部分改善，但原页与版本仍未核，不能追加独立实物票。

正式准入一个NLC07jh011656出版组记录，5161/5252/5253是同组互补分卷，不增加三个独立来源，BIBLIOGRAPHIC_METADATA_ONLY；虽有直接原图刊记、书端、分类正文，未独立保存PDF/页hash，非机械规则字形权威。1935年8月再版由原图核定，不再只是目录所报；书籍实际初版未定。未确认紫微实践、规则传承、教学班或实际交易。新增TW-OPEN-0044保留上述身份问题，来源1323（647+676／245片），44开放含五P0，Matrix222/222，图474/375，核心CLOSED。新manifest绑定准入后查询含5253、地址和刊记用语，待精确HEAD CI。下一步独立定年民国紫微命例及地区报刊。
