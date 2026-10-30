# 天问 13LY｜巴伐利亚州立图书馆《明史》第一至第八册直接链接证据

德国馆方 [《明史》官方题名检索](https://ostasien.digitale-sammlungen.de/discover/titles/M?q=Ming+shi+%28%E6%98%8E%E5%8F%B2%29) 实际返回八项 `Ming shi (明史); 1` 至 `8`。原始网页 **56,460字节**，SHA-256 `f4d775d5e4e4f0d7a9579f109bce0bfa8a26c99a5c0338077e3640bbf4dad53c`，逐项 DOM 解析并保存直接 `href`，不是据 `bsb11166692` 猜测编号。

**第一册**官方直链为 `https://ostasien.digitale-sammlungen.de/view/bsb11166691`。其余第二至第八册均分别在同一网页 DOM 内具备数字对象直链 `bsb11166692` ... `bsb11166698`，完整逐项列表见同名 JSON。先前卷五十一／卷四十六所在第二册对象 `bsb11166692` 得到独立页面交叉核对；八个数字对象并非八个已认证独立刻本。

采集执行：GitHub Actions [13LX 真实原网页取证](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/41063575035)，四项解析范围测试、原 HTML 与报告封存，以及父提交遗漏审计均通过。原始 ZIP 11,927 字节，SHA-256 `a5b4d8f37aadbb79024eb990bd5b4bfd20e49b758d3bc59f076c867be4ac42fe`，已独立保存资料库 `libfile_09c45f8cd2948191a080b6c8727ca824`。

现可推进第一册精确数字对象，而**不能推断该册已经发现卷三十五原叶**。第一册的实体印次、馆藏物理卷册与 IIIF 内容、238977.09／288977.09 任一新读数仍未确认。

下一步使用唯一已核实的第一册数字 ID 请求馆方 IIIF manifest，并只抽取有 SHA 的有限页图索引，定位 `明史卷三十五`。真实原字、版刻损伤、1739 实物印次与 G893 仍各自独立裁决；排盘产品 CLOSED、不重开算法。
