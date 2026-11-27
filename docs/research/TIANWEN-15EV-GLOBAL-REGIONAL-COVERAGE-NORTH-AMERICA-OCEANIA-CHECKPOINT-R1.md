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
