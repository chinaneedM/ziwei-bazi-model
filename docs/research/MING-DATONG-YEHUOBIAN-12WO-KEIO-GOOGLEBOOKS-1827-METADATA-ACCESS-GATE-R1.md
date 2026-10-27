# 12WO：Google Books／庆应义塾书目线索的429访问边界，不得提升原印本票

2026-10-15 公开搜索返回 Google Books 题名《野獲編》、数字对象 `VAWHNTyDZC8C`，检索摘要列“姚氏扶荔山房，1827；Original from Keio University；Digitized Aug 12, 2010”。这仅是**发现线索**，不是已经从 Google 官方 Volume API 验证的馆藏目录项，也无庆应原书条码／卷20影像。

12WN 使用官方文档定义的公共 exact-ID `books.volumes.get` 路线，不枚举猜测文档、图片、登录或验证接口。初次确切 HEAD `3a81e17829b0ce3282df43147df9b6c4b51d0fe2` 的 Actions [run 38730460404](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38730460404) ：静态合约 verify=success；真实 capture=**failure**，HTTP **429 Too Many Requests**。Artifact `11969904093` 提供真实 `capture-error.json`，ZIP 287字节，GitHub 报告 SHA256 `8f117a1565cf50b2d13497293008ed02ef65bc3ebcaa07169f999e2bf76879ec`，已经独立下载重算一致；错误文件 166 字节 SHA256 `3c779cc912e0eebcff2c61aeb7fc5f919795a9e76103d73585596be7359cb89e`。

不得由429推论“庆应无原书”“第20卷缺失”“1827原本无法得到”；亦不得让索引摘要提升为原叶原字或独立183/1869印本投票。此次来源登记新增0、705保持、算法0。已将 12WN 外部采集改为 **workflow_dispatch-only**，禁止状态文件每次更新引发重复429；CI仍持续测试精准 Google ID、请求限额与反考据过推断。

真正前进条件：提供 **馆方确切 item／shelfmark** 与 **卷20〈改造漏刻〉可核图片**，然后四处异文（宮禁／宮漏・官漏／辰初刻／戌初刻）按版本页内判读。先前东京大木文库1827 `BC0492354X/6403767830`、东京倉石文庫1869 `BB23196128/6403148395` 等已经明确目录身份，仍是独立版刻目标最直接路线。

参考目录入口：[Google Books](https://books.google.com/books/about/%E9%87%8E%E7%8D%B2%E7%B7%A8.html?id=VAWHNTyDZC8C)；[庆应大学图书馆馆藏专题](https://www.lib.keio.ac.jp/collection/index.html)。这两个入口均不单独见证卷20原字形。
