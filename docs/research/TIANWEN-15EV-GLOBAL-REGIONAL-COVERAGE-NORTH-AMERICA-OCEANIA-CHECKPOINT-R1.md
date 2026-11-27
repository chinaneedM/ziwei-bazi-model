# 天问 15EV｜全球地域覆盖复盘与北美、大洋洲候选（早期中断检查点，2026-11-27）

## 恢复及边界
基线 HEAD cbc06d306aae40c9a881c88766fc5b5698d264b1，tree 6676ff626f6016400688ef2b9eecaeb91a4fa134。六R2绑定与docs tree逐一相符，exact continuity run45937867597 SUCCESS；285项Actions在恢复时284成功、clean-training-system仍运行。无相关open PR；五P0全部保留。常规大state fetch_file返回空正文，使用精确blob解析。工具曾误输出100项workflow名称及过长协议全文，需继续白名单压缩。权威state/ledger原子写入遭遇h2连接错误，重查HEAD未移动；本次仅保存早期中断检查点，不宣称正式研究单元/风险登记或查重已经完成。

## 地域覆盖导航（双纲、atlas、15BL及15EU有界复盘）
| 地域 | 紫微 | 四柱 | 限界 |
|---|---|---|---|
| 中国、朝鲜/韩国、日本、港台 | 既有分期证据 | 既有分期证据 | 15BL，早期机械链未证 |
| 东南亚11地 | 15ET/EU有界 | 15ET/EU有界 | 缅柬老文莱东帝汶等缺口保留 |
| 美国 | 14O越文重印；AFSI教材及招生候选 | AFSI具名课程候选 | 出版、保藏、教材、招生、实开分开 |
| 加拿大 | 数字借阅候选 | 同载体待核具体术式 | 馆藏非当地出版教学 |
| 澳大利亚 | 待专项 | 具名官方培训注册与原课纲候选 | 注册不等于实开、职业许可或预测有效 |
| 欧洲/俄罗斯 | 海外保存材料及巴黎序候选 | 海外保存材料及巴黎序候选 | 法国敦煌卷、英国藏朝鲜刊本、俄藏星学大成不证明当地目标术式；巴黎序不等于当地印刷或教学 |
| 新西兰及其他太平洋地域 | 未专项复核 | 未专项复核 | 不以澳洲代全域 |
| 拉美、非洲、中西亚/南亚 | 未专项复核 | 未专项复核 | 不以风水生肖或一般占星代目标术式 |

此为既有纲要的覆盖导航，不是全库无证据判断或全球传播完成。

## 公开候选与核读
- [AFSI 2007-08-09公告](https://www.amfengshui.com/chinese-astrology-class-zi-wei-dou-shu/)：具名Lorraine Wilcox，Monterey Park, California，拟10月29–31日AS201紫微课程，AS101干支历法先修；明确十二人生领域、星曜和十年/年/月层次。报名不足可取消，故不作实开证据。页面尾有无关商业垃圾文本，发布日期及原载需独立存档核证；不采信宋代起源宣传。
- [AFSI Zi Wei Dou Shu Astrology 3](https://www.amfengshui.com/wp-content/uploads/woocommerce_uploads/2014/07/ZiWeiDouShu3.pdf)：正文2006版权；2014/07只是上传路径。直接渲染第20幅（印页3-15）有天巫、天月、阴煞、三台八座、恩光天贵的中英文对照及宫位解释；印页3-20十干四化表见文字抽取，尚未单独渲染目标表。教材与公告同机构，不作独立师承见证。不入仓原教材。
- [澳国家培训注册11079NAT](https://training.gov.au/training/details/11079NAT?taleMappings-orderBy=StartDate-asc)检索结果列NAT11079004自2021-07-01 current；[VU20815](https://training.gov.au/training/details/VU20815)检索结果具名Four Pillars与22194VIC。[21929VIC](https://training.gov.au/training/details/21929VIC)及22194VIC直接页面无可读正文，暂不裁决起止日期或替代关系。
- [Australian College of Environmental Studies NAT11079004](https://aces.edu.au/wp-content/uploads/2022/07/UOC-NAT11079004-Chinese-Astrology.pdf) 第1幅（印页0）直接渲染核读：明确Four Pillars of Destiny、出生日期时间地点、万年历排四柱、大运/流年、Self Element强弱与喜忌五行。页脚2022 accreditation文件路径不等于首次开班；原页明确无特定职业许可要求，不外推科学有效或法定许可。
- [Toronto Public Library OverDrive](https://toronto.overdrive.com/library/whodunnit/media/642458) 检索候选The Definitive Book of Chinese Astrology，介绍具名Zi Wei Dou Shu与四组生肖；待核书端及是否具名子平机械内容。不证明加拿大当地作者、出版或实际授课。

## 未决恢复任务（拟新风险，未正式赋号）
美国2006教材制作/首发、2007实开及独立师承；澳大利亚早期资格注册的生效/替代、实际授课考核和独立紫微材料；加拿大当地出版教学；欧洲、拉美、非洲、中西亚/南亚及太平洋其他地区具名术式史证。下一轮先恢复并原子登记风险、状态和R2视图；与当前manifest 359757ac503e50e3e81014df51d987a6fffc2574绑定创建精确全库查重请求，词项：
American Feng Shui Institute；amfengshui.com；Lorraine Wilcox；Monterey Park；Zi Wei Dou Shu Astrology 3；ZiWeiDouShu3.pdf；Australian College of Environmental Studies；aces.edu.au；21929VIC；22194VIC；VU20815；11079NAT；NAT11079004；The Definitive Book of Chinese Astrology；toronto.overdrive.com；Toronto Public Library。
查询未执行、未声称零命中；按实际结果语义去重再裁决准入。当前权威state仍1.1542.0，正式来源1406/264片，图495/375，Matrix222/222，57正式开放风险含五P0，排盘CLOSED。保持15EU已正式准入的结论，不覆写历史。


## 正式恢复登记（2026-11-27）
本轮从81e34496恢复，六绑定一致；20项Actions中19成功、一项运行中，未见该HEAD连续性workflow，不能借用上一HEAD成功作为新HEAD验收。分离大型blob写入，保持同一原子tree/commit发布，正式登记TW-OPEN-0058、state 1.1543.0及R2视图，并提交16词全库查询请求。查询待CI，不作零命中或正式来源准入。现有1406来源、495/375图谱、222/222 Matrix、58开放风险含五P0、排盘CLOSED。下一步：领取15EV全库字面查重，核实美国AFSI 2006教材与2007招生页、澳大利亚21929VIC/22194VIC与NAT11079004官方注册和原课程规格、加拿大数字借阅记录的出版/保藏/授课边界；语义查重后有界准入，继续欧洲、南美、非洲及其他亚太空白。排盘CLOSED。


## 15EV 正式准入（2026-11-27）
精确HEAD c2b90fb43bb475c2b7df06cb86e5015bb750af8b，continuity run45939438558 / job140310103409 SUCCESS；62 ledger、7 R2 tests。query_id 15EV-global-north-america-oceania-identity，checkpoint TW-CHECKPOINT-15EV-PROVISIONAL-20261127，request blob 7e3cef81522ddc75567e2136683b98431e5e7f7c，manifest 359757ac503e50e3e81014df51d987a6fffc2574，verifier script 3387254ce53ec0a1f1a3b779291e0c40997bf190。ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY：PASS，265文件/1406记录，原请求全部16词逐项0、matching_files=0、hits=[]、truncated=false。字面查重不证明语义全覆盖；依载体、课程号、版本和地域复核后正式准入六条。恢复时285项Actions中284成功、clean-training-system运行中，不记全绿。

- AFSI教材第0、24、25幅直接核图：2006版权、AS211中级教材、印页3-20十干四化全表、3-21示例，生年/大限/流年层次区分。与2007网页AS201招生是不同课程，不作同一开班或独立师承。教材版权限制，未复制原PDF入库；未获取原始字节hash，非古籍字形权威。公告附带垃圾内容排除，实开与原始时间待证。
- 澳洲VU20815官方索引给出2012-01-01至2016-12-31有效期并列22194VIC；11079NAT课程2021-07-01至2026-06-30，已非current，单位NAT11079004另标current；10189NAT是该课程前版。21929VIC仅由通用单位交叉索引见名，不单独登记。ACES原三页逐页核图：明列四柱、Self Element、喜忌、大运及年柱、五类关系、至少一个排盘案例的考核要求；第1印页CFSCAR401等效映射，不由此推断与VU20815同师承。非实际授课或预测有效证据。
- 多伦多OverDrive直接正文89–128行：Shelly Wu、Red Wheel Weiser、2010-01-21电子发行、ISBN 9781601637550；介绍具名紫微及四组生辰干支。美国纸本2010书目为不同ISBN的关联候选，未独立查重，不另登记。不将电子发行日期当加拿大入藏、当地印刷或实务日期。

[六条来源](./TIANWEN-15EV-NORTH-AMERICA-OCEANIA-SOURCE-SHARD-R1.json)有界正式登记。TW-OPEN-0058 OPEN，五P0不变，图495/375、Matrix222/222、来源1412（647+765/265片），排盘CLOSED。NEXT：欧洲具名两术的独立出版、教学与实践框架，先英国、法国、德国及其他地区；北美及澳洲早期活动、传承与实开仍待查。


## 15EV 前向状态枚举勘误（2026-11-27）
163f496e精确HEAD连续性run45940164993/job140312413005失败：unrecognized source verification status。澳大利亚VU20815与11079NAT两记录误用了CATALOG_METADATA_VERIFIED，现按既有验证器改为BIBLIOGRAPHIC_METADATA_ONLY；原blob 0bc34a28d86a353a53bcbd3252365a92f7bfe586保留于历史，修正blob d3c1a6232f6542227d4901177468fbd53d58f3de。未放宽门禁，未改变来源数量、内容范围、图谱、排盘或语义状态；manifest与R2绑定同步。启动时285项CI中61失败，已定位共享来源门禁的直接错误，但其余失败是否同根因仍由修复后精确HEAD验收确认。NEXT先核新CI，再进入15EW。
