# 15DW：民国道藏再刊与香港特藏目录——待准入检查点

2026-11-26。启动 HEAD `4c3e4a510516147e976f68aed5fa71ad0a716e23`；tree `a5ded4e62d7748d1234860db2b29e9c4fee0ea46`；[精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45810973098) 成功。其余流程最后一次检查284/285成功，clean-training-system仍运行；不把未完成项写为成功。此前原始六文件解析与241分片树绑定一致。研究范围为广度历史框架，不改算法。

## 1. 1923–1926 上海道藏影印条目

[国家图书馆联合目录 rarecatx0428879](https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=1&item=1b36e75d6cb348bcafa51089508d41ccfDI3ODUxNA2.T5_fvtPg0BL_gp0oecUpf3kBMYmGj_Zu9aAWwhejGlk_&page=3538) 详目34–48行著录《紫微斗數》三卷，影印本，上海，民国12–15年，1册（1114），丛书《正統道藏》，现藏中国国家图书馆。是近代道藏再刊及书目定位的候选证据，而非独立新编民国紫微术书。1923–26是目录给出的范围，不证明具体卷册印年、原始成书年、实务流行或新传承关系。未见目标藏本书端和原叶；待查重及与其他道藏影印记录/同一物理本的辨析。

## 2. 排除已知《斗數觀測錄》重复对象

[14E](TIANWEN-14E-REPUBLICAN-FEIXING-TAIWAN-1972-PUBLICATION-SCOPE-R1.md) 已精确著录 rarecatx0455448 及 [NLC416-12jh004539-48693](https://commons.wikimedia.org/wiki/File:NLC416-12jh004539-48693_華山陳希夷先生飛星紫微斗數原旨.pdf)，[15DH](TIANWEN-15DH-REPUBLICAN-ZIWEI-GUANCELU-DATED-PRACTICE-R1.md) 已将案内年代锚到1938。此次重看0基PDF p0–5、p114–115；p0《斗數觀測錄》、p1外题和馆藏标识、p2–3序文及雷迅氏录、p4原序、p114勘误表可见；未获得新增出版刊记。p114存在误正表，不能证明1948印本身份。雷必变与雷迅氏署名关系不因现代营销或同题而合并。不是独立新见证，不重复准入或重做案内历日计算。TW-OPEN-0026仍OPEN。

## 3. 香港另一特藏目录

[HKPL LAU Wai-mai Collection PDF](https://www.hkpl.gov.hk/tc/common/attachments/extension-activities/about%20us/LAU%20Wai-mai%20Collection.pdf) 可读取文本；印页25末与26首分别著录陆斌兆编著、王亭之补注、香港博益1986年《紫微斗數講義》1安星法、2星曜性质上，索书号292.22/7403。PDF文本抽取标题作“劉唯漢文庫”，馆方[特藏介绍](https://www2.hkpl.gov.hk/tc/reference/special/dccc.html)作“劉唯邁文庫”，原页截图因PDF超过10MB失败，原字以待核保留；本检查点用提供方英文文件名唯一定位。与[15X金庸文库既有目录记录](../FUSION-CHART-HISTORICAL-PROVENANCE-SOURCE-REGISTRY-EXTENSIONS-R1.json)所著录1986版相容，不增加出版版次数；是否独立物理本、第三册、条码、购藏时间、原刊记不明。仅两册文字已定位，不据未观察页断言第三册不存在。TW-OPEN-0036继续保留藏本及收藏年代边界。

## 4. 恢复与后续

以绑定当前manifest的R2请求完成全库字面查重，随后核对命中对象。仅候选，不准入新来源，不关闭问题，不新增传承边；不据目录重印推论民国职业实务。P0五项及39开放问题不变，Matrix222/222，来源1316，241分片，图474/375，排盘核心CLOSED。1923–26具体印次与物件身份作为本检查点待裁决线索，查重后若属新未决问题纳入风险台账；不得因暂未准入而遗漏。

## 5. 准入裁决（2026-11-26，同一正式提交追加）

前一HEAD `4c3e4a510516147e976f68aed5fa71ad0a716e23` 精确285/285 Actions全部成功（最后完成[clean-training-system](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45810970524)）；原拟提交 `bbba867c87db31c529def46d4e11ba331f20f8aa` 尚未更新分支。本轮直接从正式父HEAD组合一次准入提交，避免另触发一轮285项CI，不覆盖已有分支历史。

连接器实际从精确manifest `cbe30b19dad3e035c0f12e61d35fcd98b79a30ac` 和原拟请求blob `1bec889cbe6e5864feab8c1d26bade2ab3727661` 读取全部根及分片。根647条无匹配；241片均成功读正文、解析JSON、核schema和记录数，分批记录数29,25,29,30,21,19,87,50,37,60,46,53,57,73,47,6合计669，无漏片或截断；此前manifest逐片与精确树blob绑定相符。对请求20字面词使用原JSON和解码后重新序列化文本搜索，不声称语义穷尽，也不是CI日志的PASS。六片命中（零基索引及词）：101 13ZS 斗數觀測錄；112 14E rarecatx0455448/12jh004539/48693/斗數觀測錄/雷迅；153 15X 292.22/紫微斗數講義；159 15AD LAU Wai-mai/LAU%20Wai-mai/劉唯漢/紫微斗數講義；175 15BF 紫微斗數講義；226 15DH 12jh004539/48693/斗數觀測錄/雷迅。其他235片零匹配。rarecatx0428879、DI3ODUxNA2均无字面命中。全文检索后读上述六片具体记录：15AD已登记完全相同香港目录PDF（EXT-TIANWEN-15AD-HKPL-LAU-WAIMAI-ZIWEI-CATALOG），严格排除重复；14E及15DH已涵盖民国观测录藏本及样本，15X、15BF等为其他相关材料，不新增来源或传承关系。

[完整国图详情定位](https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?HasImage=&SourceID=1&item=1b36e75d6cb348bcafa51089508d41ccfDI3ODUxNA2.T5_fvtPg0BL_gp0oecUpf3kBMYmGj_Zu9aAWwhejGlk_&page=3538&sourceWhereString=&whereString=IChOVUxMSUYoQ3JlYXRlcl9OYW1lLCAnICcpIGlzIE5VTEwgYW5kIE5VTExJRihEb2N1bWVudF9Xcml0ZXIsICcgJykgaXMgTlVMTCBhbmQgTlVMTElGKEpvdXJuYWxfV3JpdGVyLCAnICcpIGlzIE5VTEwgKSA1.cHNKVlDaZLqmac_B_QboEZhR4vv4gJ8MEx7vCx6fK8U_)再次检索显示rarecatx0428879、题名、三卷、影印、上海、民国12–15年、1册（1114）、正統道藏、现藏中国国家图书馆；本次缩短参数的直接URL访问失败，保留完整详情检索定位，未见原书。准入**仅一条新的目录定位对象**，不证明是不同物理本或不同影印版；原书端及具体版次、文本关系未核，登记TW-OPEN-0040。来源1317=647+670／242片，40开放风险含五P0，Matrix222/222、图474/375、核心CLOSED。分片：docs/research/TIANWEN-15DW-REPUBLICAN-DAOZANG-REPRINT-SOURCE-SHARD-R1.json。新请求绑定准入后的manifest，在同一提交的精确HEAD连续性门禁复核全库（预期新条目命中）；未领取CI前不得声称本提交验收通过。
