# 天问 13KI：上海馆题名《授時歷故四卷》97页数字源取证与刻抄本防混淆

## 已取得的确定性事实

- Wikimedia Commons [文件页](https://commons.wikimedia.org/wiki/File:Shanghai_%E6%8E%88%E6%99%82%E6%AD%B7%E6%95%85%E5%9B%9B%E5%8D%B7.pdf) 列《授時歷故四卷》，自述来自上海图书馆，2024-04-20 上传，载原名 `dGJ2300966.pdf`，并记录 97 页、14,376,480 字节和 SHA-1 `73c2017bb9eb109edf069f9563c397e7fcb2cba4`。
- [13KI GitHub Actions](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40858637903) 已经 **success**：通过 exact source bytes 下载、SHA-1 和文件大小对照，得到 PDF SHA-256 `c524693e7bad502d222a1444d688cc7d63ca4a4037d7d4e08cee4aa94f9adbae`，确认 97 页；无 OCR 生成 7 份页图索引及9张抽样页图。
- Artifact [12890397318](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40858637903/artifacts/12890397318) 内含源 PDF 与索引；ZIP SHA-256 `1328eaca52cf8c692edf397ee76aedad90c8d63bbea1b8bba8ae48772ddd835d`。
- Commons 首页公开预览显示手写题签、题记及钤印痕迹，但**只有首页预览已直接目视**；不能把“97 页已下载”和“97 页逐字校勘完成”画等号。

## 有关具体版本的独立证据边界

- [一份上海馆二手书目](https://m.guoxuedashi.com/shumu/gj-1931574qy.html) 登记清抄本，附黄宗羲撰、曹元忠校、宋景昌跋。
- [另一份上海馆二手书目](https://www.guoxuedashi.com/shumu/gj-2026002re.html) 登记 1923 年刻本。二者不能仅据同名合并为同一实物。
- [浙江师大藏 1923 嘉业堂刻本书目](https://www.guoxuedashi.com/shumu/gj-3213822hz.html) 和 [CiNii 1982 后印本](https://ge.nii.ac.jp/ncid/BA68484081) 分别是其他具体馆藏／版本线索；均不能直接认证 Commons 文件 `dGJ2300966` 的版次或原字。

## 特意不作的历史裁判

**13KG** 的哈佛《明史》卷33两处原印文字已获源图绑定，保持不变；**13KI** 尚未定位这份上海扫描的卷四〈月離曆〉目标原叶，因此黄氏「益加損減」、尾数字「五十纖」和「一百六十七限」均仍为未对原叶确认的候选。当前不存在黄氏与《明史》原印跨本版本文字裁决，也没有归咎 OCR 的证据链。

Registry 新增 **一条隔离数字来源**，不是新增一件已经辨明版本的独立清代实物。研究风险11项继续开放；G893 六组跨本数值终裁 0，传承谱新增边0，算法重开0，排盘 R1 **CLOSED**。

机器证据：`docs/research/TIANWEN-13KI-SHANGHAI-HUANG-97PAGE-DIGITAL-ACQUISITION-R1.json`。下一批须先依据源 PDF 页图索引定位卷四，随后原页高分辨率逐字核读；独立取得上海馆物品级目录映射，避免同题名跨版本污染。
