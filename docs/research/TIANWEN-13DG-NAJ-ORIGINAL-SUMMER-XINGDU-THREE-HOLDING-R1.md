# 天问 13DG — 日本国立公文书馆（NAJ）同表原叶三馆对照

**本批新实证：** 从已验收的 [NAJ 13BA 图像归档](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39410644745) 取回原始 `高麗史５１` 第 27 幅 JPEG，依第一方馆藏 IIIF manifest SHA 校核实际原图，人工逐字复查夏至表行度，不使用 OCR。

NAJ 源对象：`282-0006-0051` / [官方物件 4898853](https://www.digital.archives.go.jp/item/4898853)，manifest 36 canvas SHA `3f38f528...`；原始第 27 幅 JPEG 1021783 bytes、3000×2215，原 bytes SHA `3a1cdf95c11d29e06041de00b8cc56e158775cdfc058ecce46fe5f796a5e606b`，原生 RGB SHA `333a05cd333353607b8ed082bc4c70b0ea07dcd2d5e83ad63ba9e0d4641a8d62`。归档 artifact 12258588506，ZIP SHA `320b0e09...bad8b6`；各行日次标题、字段裁剪具体 bbox + RGB SHA 见 [JSON 底稿](docs/research/TIANWEN-13DG-NAJ-ORIGINAL-SUMMER-XINGDU-THREE-HOLDING-R1.json)。

| 实际日次标题 | NAJ 原叶「行度」原字与数值 | 早稻田同日次原叶 | 1909 年同数值的标题日次 |
|---|---|---|---|
| 二十八日 | 初度九十六四〇六二 = 0.964062 | 同 | 二十七日 |
| **二十九日** | **初度九十九四五四九 = 0.994549** | **同** | **二十八日** |
| 三十日 | 初度九十六五〇三八 = 0.965038 | 同 | 二十九日 |

这证实「九十九四五四九」不只存在 1909 年晚印本，亦见于 NAJ 现存抄本与早稻田藏本的**原始图像**。但此处三者数值顺序一致、各本日次标题并不一概相同；仅限三行三栏的局部 field-specific 对应，不能据此推出全表机械换日法。**三份馆藏实物／描述来源 ≠ 三个独立传承票；未判定祖本错误起源。**

本轮 [13DF 官方来源重取](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39876177996) 对 NAJ 第19幅接口出现 HTTP 403，属于当次匿名访问边界，不是第27幅实物不存在。13BA 先前已通过原始影像下载、保存 SHA，本批复读的是其可复现归档，没有假报新鲜馆方访问成功。

原始 13DB 数理候选「初度九十六四五四九」依然**没有**在三馆相应原字中得到支持。冬至 D16 `5.1362` 原字与推算 `5.2362` 是另一独立问题。保持 NAJ/Waseda/1909 源流、台湾 NCL 208/03130 清抄与 1905 补写层的版本考据开放。

基数不变：Matrix 222/222，源754、传承图252/238、风险11、算法重开0、确定性排盘 CLOSED。
