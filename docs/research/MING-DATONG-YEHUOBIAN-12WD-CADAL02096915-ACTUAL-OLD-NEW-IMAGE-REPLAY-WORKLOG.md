# 12WD：CADAL02096915 旧、新上传原始文件及目标页对照

12WC运行[38684377172](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38684377172)，job 116255845608，成功保存Commons自身API发出的两份原始DjVu及图页；[artifact11948889363](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38684377172/artifacts/11948889363)由Github报告7,065,704字节、ZIP-SHA256 `737efeb074c114eaf8c4df955080b037d531e349d10d1feb0e07103d63da2408`。ZIP**未在独立环境重下载验哈希**。

旧名`野獲編(十六).djvu`原件 **3,400,790字节，135页**，运行器SHA256 `c9cbad43811efa7ddd737bd0997bf663b5a84d825202dc4ca2e0dcaecb81448e`；带CADAL编号新名原件 **3,495,009字节，135页**，SHA256 `262edac806b90c984d5f0c4fce1bc150a974ebd574d847738a08a00cad39640d`，与先前12VZ相同。

DjVu页121及122的**精确灰度像素SHA不相同**；256×384图像归一后的8-bit灰度平均绝对差分别为 **0.04801**、**0.03985**（0..255尺度）。这为选定页面是极接近的数字扫描内容提供强度有限的正证；并不证明精确字节同一、全册相同、实物版心相同、独立纸本或1827/1869印次。无OCR、无新人工古籍字形核读，所有历史印本投票仍为0。

本次完成取证后，12WC昂贵的双源原文件下载工作流调整为 **仅手动workflow_dispatch运行capture**，普通push继续执行验证，不反复下载相同资料。根来源647+扩展57=704，Matrix222/222，修复45/45，图谱252/238，正式批次487，排盘CLOSED。下一实证任务仍是馆方可识别的1827与1869卷二十〈改造漏刻〉原叶。
