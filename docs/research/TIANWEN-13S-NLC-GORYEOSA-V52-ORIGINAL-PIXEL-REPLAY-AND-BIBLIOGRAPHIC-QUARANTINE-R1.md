# 天问 13S｜《高丽史》卷五十二原件像素重放与“善本書號”线索隔离

13R 所保存的原PDF、单页内嵌PNG的 SHA-256 经本轮重新读取再次一致。对相同三张内嵌源图（PDF第2、16、17页）检测时，初始以灰度 L 模式直接 PNG 编码得到的 SHA 与13R记录不同；逐像素对照却完全相同。确认13R历史 ROI 文件采用 **源图 L → RGB → 裁剪 → PNG 序列化**，其原本登记的三个裁剪 PNG SHA-256 全部重放一致。故它们不是被篡改或未经证明的 SHA；仅是13R没有记下关键的转换顺序和编码格式。

本批新增机器可复核的 `RGB.crop().tobytes()` 像素 SHA-256，同时保留原本 PNG 字节 SHA-256。完整源PDF 64页、19,799,436字节、SHA-256 `2b9e51cc5f44a4d92d3cb4a63318605f78cc8ffb118853036655b65ed279a689`。内嵌源页及裁剪位置信息完整见 [13S JSON](../research/TIANWEN-13S-NLC-GORYEOSA-V52-ORIGINAL-PIXEL-REPLAY-AND-BIBLIOGRAPHIC-QUARANTINE-R1.json)，可经 `scripts/replay-goryeosa-nlc-source-pixels-13s.py` 传入保存的完整PDF重放，不使用OCR。

| PDF页 | 对应13R目视记录 | 灰度源页 SHA 与 13R | RGB PNG裁剪 SHA | 原RGB像素SHA |
|---|---|---|---|---|
| 2 | 志卷第六 | MATCH | MATCH | NEW |
| 16 | 五分一三六二 | MATCH | MATCH | NEW |
| 17 | 八千四百二十四六四〇八 | MATCH | MATCH | NEW |

**馆藏身份的新线索仅为元数据而非实物裁决：** Commons [NLC第40册上传页](https://commons.wikimedia.org/wiki/File:NLC892-411999022809-48456_%E9%AB%98%E9%BA%97%E5%8F%B2_%E7%AC%AC40%E5%86%8A.pdf)记「善本書號 13494」及「抄本、清」。这个字段由上传页面转述，未见国图第一方实物号与馆藏册次的独立核验，**不得**由此宣称一份清代实物的精确年代，更不得判断 NLC 与 CADAL 为不同纸本。同一个文件系列不同扫描册不是多个独立古籍原本。

新增的重放脚本支持离线源PDF核验，Github专用采集Workflow在抓取之后执行像素重放，同时为常规CI提供无需外部网络的证据防火墙测试。图谱、来源总数、排盘算法和确定性排盘R1不发生变更。TW-OPEN-0005 与全部11项遗留问题仍为OPEN。

**下一动作：** 国图第一方记录核查「13494」及数码序列「411999022809」；CADAL02050311目标页独立绑定纸本、版面、藏印；同时继续 D16 历法同栏与少/微术语的未决问题。