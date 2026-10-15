# 12WH：柏林馆1827《野獲編》38张样页元数据的真实内容范围裁决

**采集回执：** [12WG Actions run 38721590423](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38721590423)，job `116377200692`，已 **success**。所用源为柏林馆从DDB正式发出的 PPN334378186X；IIIF Manifest 与METS分别HTTP200，校对回此前12WF同一字节SHA：Manifest 69,638字节 SHA256 `db26dd7d790c66faddc46ce542354396a30a1bb1bba70b9be011e6d57db27b82`，METS 73,209字节 SHA256 `c30688453d2c9540be407805b9c41d88ffc4e716d0bcb8dd0fdea9349c2cb9d8`。保存的原始元数据和全Canvas/Range机器报告位于 [artifact11967090494](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38721590423/artifacts/11967090494)，GitHub上传器报告ZIP SHA256 `0a8595c713fcccdf79330661b72334eaeff7aa689c71e5992cfe4e70c032519b`；**本批没有独立下载ZIP复验压缩包SHA**。

## 一、只看公开样页的结构：终于不再把38张算作“未知内容”

解析 Manifest **38 Canvas + 18 range 标签**，METS具有 **LOGICAL / PHYSICAL 两套structMap**。来源原发文档中能够正向辨识：

- 主书部分：`野獲編　巻首　巻一`、`萬厯野獲編序`、`野獲編分類凡例`、`野獲編總目 (Beispielseiten)`、`列朝 : 告天即位 (Beispielseiten)`；
- 补遗部分：`野獲編　補遺卷一`、`萬歴野獲編補遺小引`、`野獲編補遺巻一目錄 (Beispielseiten)`、`列朝 : 聖祖兼三教 (Beispielseiten)`；
- 其他：封面、书脊、颜色校准页和序凡例等。Canvas标签还出现 `序:1r`／`序:1v`／`凡例:1r`—`2v`。

已在**所列结构标签范围**内证实它们指向卷首／卷一／补遗卷一样页，**并非明确的卷二十〈改造漏刻〉样页**。全文未在记录中自动声明，因为38个图像并未逐张人工细读，页标签没有卷二十也不是纸本内容缺失证明。不从数字馆有“1827”版刻标签直接推断这件纸本刻版状态必为未修初印；不从一个样页物件为东京、京都、1869重校本推断谱系。

## 二、全国古籍普查开放页面的访问边界

同一 12WG 程序通过公开 `https://gjpc.nlc.cn/xlsworkbench/publish` 执行一次限制500kB、12秒的匿名探针，记录为 `ACCESS_OR_SOURCE_PARSE_BOUNDARY_NO_ABSENCE_INFERENCE`：没有成功取得全国普查检索结果，未发起馆藏题名查询，不能声称全国数据没有温州《野獲編》。国家古籍保护中心该库为分批公开；2017温州古籍目录存在，但里面的特定条目页、普查编号及索书号均未取得。

## 三、实际推进

归档的结果用于**停止反复检索柏林同一38张样页作为卷二十来源**，将任务重定向为获取明确的 **Libri sin. 365/372** 原书卷20页，或优先采用东京／京都既有8个物品号确定的原物获取队列。真正的1827初刻与1869重校原叶、源文件SHA256及四处原字校勘仍空缺。

未增加来源注册表项目、谱图关系、历史字形票、运行重开。来源647+57=704，Matrix222/222，修复45/45，谱图252/238，正式批次487，排盘产品CLOSED。
