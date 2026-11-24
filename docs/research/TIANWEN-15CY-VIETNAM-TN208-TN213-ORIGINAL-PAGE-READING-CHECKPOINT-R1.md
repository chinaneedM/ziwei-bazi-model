# 15CY｜越南胜严寺 TN208 安星手稿与 TN213 命盘：公开图像阶段性核读

2026-11-24。BREADTH_FIRST_PROVISIONAL_INTERRUPTION_CHECKPOINT；不是完整批次验收。复用15R的已登记同一实物/数字对象，不新增来源或覆盖等级，不修改15R历史快照。此前15R仅定位公开图像入口，现取得可视原页的局部规则证据。抄写年份与2013数字化/移交年份分别记录。

## 1. 对象与可回放的页图

TN208/TNVNPF-110（馆目57页），既有来源 EXT-TIANWEN-15R-VNPF-TN208-ANXINGZIWEI-57P；TN213/TNVNPF-115（馆目90页、公开查看器61页，仍不一致），既有来源 EXT-TIANWEN-15R-VNPF-TN213-CHARTS-90V61。来源分片 docs/research/TIANWEN-15R-VIETNAM-THANGNGHIEM-TN208-TN213-SOURCE-SHARD-R1.json，blob e66e51d6de0d226462b3e40eed0f4bf75c5fb519。

以下链接为提供方JPEG，本轮在线渲染直接目视，未下载图像字节、未获原生分辨率哈希；因此仅为有页界的正例核读，不宣称完整逐字校勘、认证原字终裁或升级原登记等级。页4访问失败，不能据此推断缺页。

| 对象/查看器页 | JPEG | 局部可辨内容及界限 |
|---|---|---|
| TN208 p3 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-003.jpg) | 紫微斗數题头、安陰陽命法；甲丙戊庚壬为阳命、乙丁己辛癸为阴命；下接干支纳音内容。旁注未完整释读。 |
| TN208 p5 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-005.jpg) | 干支纳音续表；未完成60组逐项校勘。 |
| TN208 p6 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-006.jpg) | 安身命法：从寅起正月顺至本生月，以该月起子时逆至生时安命、顺至生时安身；安十二宮例不拘男女俱逆。十二宫次序可辨为命、兄弟、妻妾、子息、財帛、疾厄、遷移、奴仆、官祿、田宅、福、父母。第十一宫简写福，不强改原文。 |
| TN208 p7 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-007.jpg) | 定局例，甲己年丙起寅、乙庚戊、丙辛庚、丁壬壬、戊癸甲的对应线索；以宫干支纳音定五行局。细小夹注未逐字校。 |
| TN208 p8 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-008.jpg) | 定局例续、五行納音、安紫微天府法题头。纳音字形及口诀余文未全部核校。 |
| TN208 p9 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-009.jpg) | 紫對府、紫府相对宫位图及定紫微五局图线索；可辨火六局、金四局、土五局、木三局、水二局，未完整抽取每个生日位置。 |
| TN208 p10 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-110/jpeg/tnvnpf-110-010.jpg) | 金四局、木三局两幅格图及日数栏。所有数字和方向待逐格复核。 |
| TN213 p45 | [原图](https://lib.nomfoundation.org/site_media/nom/TNVNPF_II/tnvnpf-115/jpeg/tnvnpf-115-045.jpg) | 实际十二宫方格命盘、可见星曜与金四局字样；未转录个人姓名或完整生辰。未重放该人的全盘，不推定使用TN208。 |

## 2. 有限的机械重放（非产品测试）

以子=0、寅=2，月序m从1起、时支序h从子0起，p6的候选读法为 a=(2+m-1) mod12，命=(a-h) mod12，身=(a+h) mod12，命宫起逆布十二宫。三个独立虚构输入重放：
- 正月子时：命寅、身寅；
- 二月卯时：命子、身午；
- 十二月亥时：命寅、身子。

该重放只说明该段文字的操作方向和整数索引可执行，不代表整本安星法一致，不证明产品运行时全路径或历法规则，未据此调整算法、Matrix或任何候选盘。

## 3. 证据限界与下一步

根登记647条及218分片的路径/blob对应已核；全分片内容遍历尝试触发工具调用上限，未取得完整扫描结果。已读取与越南相关的九个命名分片，确认本轮两个物件早在15R登记；不声明全局查重完成或不存在其他同源记录。无新来源准入，无原始字节SHA，无版次/师承确认。待完成其余分片针对对象号与题名的检查；优先复核TN208 p4和后续生日安紫微格图、TN213第45页匿名结构及90/61页数边界；再据强证据决定是否正式补充历史纲要和覆盖图。

transmission_impact: 既有TN208手稿和TN213命盘证据在本检查点具有局部可读文字/实际图式，未升级机器图节点、未增任何传承边。拒绝2013=手稿成书年、同一藏书群=同一底本/老师、公式相合=直接承袭的推断。

Matrix222/222、来源1236=647+589（218分片）、图谱462/374、16个风险含五P0均保持；G893最终0/6；确定性核心CLOSED；本检查点非完成批次。
