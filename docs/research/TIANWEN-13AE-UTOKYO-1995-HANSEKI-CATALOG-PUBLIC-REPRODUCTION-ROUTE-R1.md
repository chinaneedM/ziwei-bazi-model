# 天问 13AE｜东京大学1995《总合图书馆汉籍目录》史部与1998勘误：官方原册目录索引获取门禁

## 官方第一方书目资料
东京大学总合图书馆 [官方存储库记录 2010678](https://repository.dl.itc.u-tokyo.ac.jp/records/2010678) 提供《東京大學總合圖書館漢籍目録》，并将：
- 正编正式出版日期标为 **1995-04-20**，史部正文印刷页码 **100–251**；
- 1998-03-30 出版《檢字表正誤表竝補遺》；
- 电子存储库入藏/开放记录为 **2025**，不能倒置为原书刊写年份；
- 史部分为 `kansekimokuroku_11_shibu.pdf` (19.7MB) 和 `kansekimokuroku_12_shibu.pdf` (25.1MB)，补遗另有 `kansekimokuroku_90_errata_1.pdf`。

这里获得的是**独立于 CiNii 联合目录的馆方本馆编制目录之可申请来源路线**，但没有读到《高麗史》的具体条目。当前公开网页对两个史部分卷 PDF 测得 HTTP 429；这是访问限制，不是该目录不收书的反证。

## 版本学目标与证据隔离
13AD 两条联合目录馆藏绑定保持：
- 朝鲜钞本 `BC15670118 / G23:12 / 卷52 0008535809`；
- 朝鲜刊本 `BC15973641 / G23:194 / 卷52 0008542011`。

**需要继续校对的命题**：1995馆方汉籍目录（含1998补遗）能否对这两项提供页码、分类、实物登记和版本学说明。此命题不能用所引PDF的可下载链接、整书出版年代或其他作品的图像来直接裁决。史部原PDF及相关卷/册/页未取得，不断言本书“必然著录”或“未著录”，更不将馆藏目录计为 G893/《高丽史》数值见证。

## 定向安全采集
新增 `scripts/acquire-utokyo-hanseki1995-13ae.py` 和 `.github/workflows/acquire-utokyo-hanseki1995-13ae.yml`，仅访问校方公开发行的三条 PDF URL。每条下载以65MiB封顶，不自动重试429/403，无登录、无伪造持有凭证、无 OCR。成功时记录下载原字节 SHA256 与有无文本层的机械结果（仅为定位候选页），并保存公共文件至 Actions artifact 以供**后续人工原页核对**；失败时记录 HTTP/transport/access 状态。既不由关键词零命中证明目录中没有《高麗史》，也不通过页码或相同书名推断原印独立性。

当前登记源647+扩展92=739。Matrix 222/222，风险11项保留，`TW-OPEN-0005=OPEN`，钞刊两本卷52原字仍未取得，图谱节点/边不变，排盘R1 CLOSED，无算法重开。

机器核验证据：`docs/research/TIANWEN-13AE-UTOKYO-1995-HANSEKI-CATALOG-PUBLIC-REPRODUCTION-ROUTE-R1.json`，来源分片：`docs/research/TIANWEN-13AE-UTOKYO-HANSEKI1995-REPOSITORY-SOURCE-SHARD-R1.json`。
