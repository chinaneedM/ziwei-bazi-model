# 天问 12QF 阶段检查点：CADAL 首册直读 1606／1700／1827／1869 四层时间

**状态：PARTIAL_CHECKPOINT_NOT_CLOSED_12QE。** 研究对象是 CADAL《野獲編》数字第一分册的卷首影像，不等于同书第十六分册、1827 藏本或 1869 重刊实物已经被一一绑定。本轮没有 OCR、没有自动算法转换、没有改写旧批次判断。

## 物理页图与四个不同年代

公开扫描件 [CADAL02096900](https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/CADAL/10) 第一分册的原图，经 [Actions 38061453837](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38061453837) 下载并按 SHA-256 711dc16b17d139612fbe852dc99869bb709b85c161440dfc7618ee1dbd6f38fa 验证，大小 2,833,699 字节，共 115 页，生成原页采样与联络表（artifact 11673980170，sha256 1b1d4d944b34960a5024e9ed99481926bfe5ab7c0e73f1731ae869a055ff4751）。

直接无 OCR 目视校勘：

| 直接页码（1-based） | 原页可以核见的时间文字 | 严格限界 |
|---|---|---|
| p7 | 萬曆三十四年丙午仲冬日沈德符題於甕汲軒 | 1606 作者序跋，不是这份扫描实体的物理年代 |
| p10 | 康熙庚辰八月桐鄉錢枋識 | 1700 编校序言日期，不是必定的刊行年代 |
| p5 | 道光七年歲次丁亥春三月錢塘姚祖恩笏園氏識於羊城邸寓之扶荔山房 | 1827 姚祖恩序，不等于此份扫描一定是1827初印 |
| p5 | **同治八年己巳春月重校刊補** | **1869 重校刊补说明已存在于当前所见卷首页图内**，且与1827序位于同一张扫描页 |

与上述日期有关的原页图哈希：p5 `c82c3818832fa91b012994576cc3cfc0b3d2f5660145f521d3acea5cbf1cfbba`、p7 `4707eae743c81fe31bf138678b8a0ff3abca90c14f41efa41d9ba1db379e8e1d`、p10 `dad8fd03b6eceb08a0c9212f5751a11a18e7bf15608ac83af3223e3a09d3fc27`。

**重要修订：** 12QE 第十六分册〈改造漏刻〉直接影像所见 `辰初二刻／戌初三刻` 已经可靠记录为该页的字形。首册的新读法证明该数字系列至少存在包含 1869 重校文字的卷首对象；但**尚不能仅从同在 Commons/CADAL 顺序编号推论两分册属于同一实体印次，不能直接标注第十六分册为1869重印，也不能倒称它已经证实1827初印的数字原貌**。

## 网络转录只能协助定位

CText [首册卷首](https://ctext.org/wiki.pl?chapter=155900&if=gb) 收录相同1827/1869语句，且其[第十六分册结构](https://ctext.org/wiki.pl?chapter=418967&if=gb) 使用「十六v19~20」标题并标明 OCR 底稿。当前**没有** CText 对应原图哈希和 CADAL 源文件完全等同的独立证实。网页转录不能重复计作独立实物投票；即使网站文字是「戌初二刻」，也不能覆盖目标原图「戌初三刻」。

## 下一工作、传承边界及产品约束

1. 追查具有具体原件编号的1827刻本第20卷〈改造漏刻〉原页，与具有1869说明的首册及 CADAL 第十六分册分别绑定后再判定晚出校改内容。
2. 优先寻找原二十卷独立手稿同篇是否出现，严格保留原二十卷与后编三十卷重排的章名对应差异。
3. 研究传承图的本轮结论为「关系未证」：没有证明 CADAL 第一分册与第十六分册为一实体印次，没有证明 1827→1869目标页直接改版关系，不推定1447改造完成或1450历时标准。

Historical Matrix 仍为 **222/222**；来源元数据已修 **45/45**；确认排盘算法缺陷 **0**；`MD-G03=OPEN_BLOCKING_GENERAL_ADAPTER`、`HPA-DAYUN-CAL-002=MISSING_FROM_PRODUCT`、`DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`。12QE 仍 OPEN、算法不重开。机读校勘链见 `docs/research/MING-DATONG-YEHUOBIAN-12QF-CADAL-FIRST-PREFACE-DIRECT-DATES-R1.json`。
