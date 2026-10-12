# 12UR — CText 原扫描目录的影像身份门禁：不将 OCR 或柏林样张算作新古籍原叶

## 公开资料与当前可核实边界

[CText 扫描本目录](https://ctext.org/wiki.pl?if=en&res=1946940) 的搜索公开索引注明该书文本由对应扫描影像自动 OCR 生成，目录第十六册「十六v19~20」下列有三十卷分类本卷二十「改造漏刻」。仓库之前只有 CText [晚出章节文本](https://ctext.org/wiki.pl?chapter=418967&if=gb) 注册为现代接受文本，不能断定后者与前者 OCR/扫描影像同一实物。本轮直接打开 CText 对象页返回 HTTP403，未拿到源发的页面影像 URL、完整页图，也未确认具体版本/物理书架号。

[柏林国家图书馆 1827《野獲編》](https://www.deutsche-digitale-bibliothek.de/item/WBXTVCN6VMFVV7ESZ7QLCGP4GFJ22IA7) 和一手 [SBB 数字 IIIF 说明](https://lab.sbb.berlin/dc/?lang=en) 亦复核。**注意：本项目 12PZ 曾成功抓取柏林 SBB PPN334378186X 的 38/38 张 Beispielseiten 展示页，人工已经读完并哈希核验；这些样张没有目标篇，但不能认为完整1827印本没有目标篇。** 已有根注册 `EXT-SBB-DDB-PPN334378186X-YEHUOBIAN-1827-BERLIN-SAMPLES`，本轮不再追加一次。

本轮只新增前瞻性源链接核验工具：访问**这两个已公开 URL**，记录 HTTP 响应与源页面发出的同域疑似影像链接，禁止猜测书目ID、登录、绕过反爬以及直接下载图像。返回 HTTP403/超时只算本次环境访问边界，不算本书没有影像。探测结果通过 GitHub Actions artifact 保存，供下一步判断是否能建立扫描页索引。

## 不能越过的证据边界

OCR文本、已现代整理文本、目录中的「卷二十」及潜在扫描链接，都不是已认证原叶的四字/时刻异文。必须先明确影像对象、原件或数字来源、卷20精确目标页、文件SHA256及与CADAL/续修四库源影的独立性，才可进入字形校勘。

本轮无新历史来源注册、无版心/原叶或独立历史投票、无算法重开：来源647+40=687，Matrix222/222、元数据修复45/45、谱图250节点/237边、正式批次487 latest12QD，MD-G03与12QE保持OPEN、确定性排盘R1 CLOSED。
