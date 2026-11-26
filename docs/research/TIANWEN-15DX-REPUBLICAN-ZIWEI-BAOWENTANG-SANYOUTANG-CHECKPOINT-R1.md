# 15DX：民国紫微斗数书目再刊与古籍销售目录（待准入检查点）

2026-11-26；父HEAD `ae4dcec8b66b6ba858bb28d5e4fd8b1a47bcd584`，tree `fe6bfea1bf5210ac1e913626ce38d193d034c089`。精确HEAD连续性CI [45814234272](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45814234272) 成功；全部285项中284成功，clean-training-system [45814234430](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45814234430) 在复查时仍运行，不能声称全部成功。五项P0保持原状态；广度优先，排盘核心CLOSED。

## 1. 1929年九月国立北平图书馆月刊

[公开原刊扫描](<https://upload.wikimedia.org/wikipedia/commons/f/f3/NLC404-01J000024-72809_%E5%8C%97%E4%BA%AC%E5%9C%96%E6%9B%B8%E9%A4%A8%E6%9C%88%E5%88%8A_1929%E5%B9%B43%E5%8D%B73%E6%9C%9F.pdf>)，NLC404-01J000024-72809，第三卷第三号。核读PDF零基 p0 封面“國立北平圖書館月刊”“民國十八年九月”，目录标明“晁氏寶文堂書目”；p109（印页404）为该书目相邻页；p110（印页405）上半区首排自右第五栏“紫微斗數”，邻右“開門吉方圖”、邻左“靈棋數新刻”。只采这一可辨题名，不扩张OCR中其他字形；[ctext条目](https://ctext.org/wiki.pl?chapter=239784&if=gb) 可对照同名书目第118项，但电子文字可能同源。民国刊载的是明代书目，不是1929年新增紫微实务、书籍现藏或师承证据。原著成书、底本版本及影印物件分开；不能把重刊当独立明代史料见证。

## 2. 1937年三月三友堂书目

[公开原刊扫描](<https://upload.wikimedia.org/wikipedia/commons/e/e8/NLC511-023031404016073-52526_%E4%B8%89%E5%8F%8B%E5%A0%82%E6%9B%B8%E7%9B%AE._%E7%AC%AC3%E6%9C%9F.pdf>)，NLC511-023031404016073-52526。PDF零基p1（印页1）“三友堂書目 第三期 民國二十六年三月訂”。PDF零基p129（印页129）子部術數類，第1610号，右起第六栏，核读：
- 書名：紫微斗數六卷
- 署名：宋陳希夷
- 版式：小板
- 紙冊：竹紙四本
- 價格：八角

原页连续编号1605–1617，自动文本错误地标为1905–1917并称为年份；实际1610为条目编号而非出版年，且该处未标出版年代。日期是1937年书目编订时间，不是所售书的刊刻年。作为当时销售目录的直接题名、卷册、版式及标价证据，区别于现代书商回顾；不证明成交、发行量、现存物件、作者真实身份、某六卷本具体版次或其排盘机制。尚未核见目标书的书端、刊记、原叶、书商地址和实物；不能与全书/全集或明代其他六卷著录径直合并。截图为实际核读的原刊数字替身；未独立重算PDF哈希，不声称完成整刊逐字校勘。

## 3. 查重与准入界限

两份原刊扫描及目标页已定位；提交绑定现有manifest的R2字面检索，须在精确HEAD CI取得结果后核对所有命中、区分同一刊物数字替身、明代目录原作及民国再刊、书商所列书与实物。若已有同一对象，复用并追加原页定位，不重复计数。保留本检查点未决线索，不增加正式来源、图谱节点/边或关闭风险。40项开放问题、五项P0、Matrix222/222、来源1317（647+670／242片）、图474/375及核心CLOSED不变。TW-OPEN-0026、0036、0040保留。下一步先核收查重，按原页证据范围准入或排除，再继续独立民国实务史料。

## 4. 15DX正式准入及复核（2026-11-26）

父HEAD `b130304fbc7a935af45147755d349f408fc05349`、tree `c5bb8104489ad465816a6d27afb10b133f8ac6c9`。[连续性CI run45815822649](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45815822649)，job139895161107，实际日志 query_id=15DX-republican-baowentang-sanyoutang-dedup-r2-20261126，checkpoint_id=TW-CHECKPOINT-15DX-PROVISIONAL-20261126，request blob `e88f4ed003b23afbd2368cd0e5d4aabe3a12fa51`，manifest blob `5de85305cacc949751aa29c4fd6137db1166e475`，verifier script blob `3387254ce53ec0a1f1a3b779291e0c40997bf190`。status=PASS，scope=ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY，files243、records1317、matching_files0、18个原请求词逐词均0、hits=[]、truncated=false。该结果是完整登记库字面查询，不宣称外部史料穷尽；两个候选不同刊物、不同刊期及数字物件号，不是彼此重复，也不将明代原目录与1929重刊视为两个独立明代证人。父HEAD全285项复核284成功，clean-training-system run45815825330仍运行，无已知失败。

再次打开两份原刊扫描：1929 PDF p0与p110；1937 PDF p1与p129；关键原字与编号重核相符。另见1937 p0封面署“陳垣”及印章，仅支持封面题签署名，不能认定陈垣编写书目、拥有该斗数书或从事命理。p264为末页补目，p265为封底，所查页未见地址，不作整刊无地址结论。1936年第二期[后出目录](https://www.guoxuedashi.com/shumu/gj-3045324vk.html)著录北平三友堂；2006年[书业回顾](https://news.sina.cn/sa/2006-05-22/detail-ikknscsk0254464.d.html)称其与文奎堂比邻、经营者高新元；仅作北平区域待核旁证，尚未核当年营业地址、同期账簿或第二期原页，二者不单独准入、不新增师承边。

正式准入两个独立**出版目录对象**，仅以目录级权威登记（BIBLIOGRAPHIC_METADATA_ONLY，physical_glyph_authority=false），虽核见目录原图，不是目标紫微术书原页，更无完整PDF及原页独立哈希，故不升级机械规则证据等级。新增分片 `docs/research/TIANWEN-15DX-REPUBLICAN-ZIWEI-CATALOGUES-SOURCE-SHARD-R1.json`；新风险TW-OPEN-0041、0042分别保留明代目录底本和1937六卷本及交易/地点身份，五P0和此前全部开放项不变。来源1319=647+672／243片，风险42，Matrix222/222，图474/375，确定性核心CLOSED。新请求与准入后manifest绑定，待本HEAD精确CI重验。
