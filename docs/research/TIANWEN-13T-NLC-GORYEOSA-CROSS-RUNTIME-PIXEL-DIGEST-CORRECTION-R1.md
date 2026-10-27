# 天问 13T｜《高丽史》13S 跨环境图像校验错误修正（保留历史证据）

**本次是原图重放门禁的技术缺陷修复，不是发现古本原字有新异文。**

13S 提交 `a5ace234ec69` 的独立图像采集工作流 [39203880339](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39203880339) 已经成功重新获取和校验源PDF的 SHA-256；在第二步 13S 重放时失败，现场 Python Traceback 定位：`doc.extract_image(xref)["image"]` 返回的 PNG 字节哈希与本地 13R 首次封存哈希不一致。这些 PNG 字节可能经当前 PyMuPDF 实现重新封装，不能无条件视为物理PDF内原始不变的编码字节。上一轮仅通过统一 RGB crop 方式解决 Pillow L/RGB 容器差异，还没有解决 PyMuPDF 版本间图像提取编码差异。

新增前向修复，不改写 13R / 13S 历史记录：

- 完整源 PDF 的 SHA-256 仍是最强**文件字节级身份**。
- 使用 `fitz.Pixmap(doc,xref).samples` 获取源 PDF 该对象的**已解码灰度像素**，校验 SHA-256、宽高、xref、灰度通道及行跨度。
- 用 Pillow 对灰度样本转 RGB，按原 13R 像素坐标裁剪，检验 RGB 原始像素字节 SHA-256。
- 原先导出的源页 PNG 和 ROI PNG SHA 保留为**产生它们的历史环境的编码记录**，在不同运行环境下不再作为失败条件；它们仍可以在同一旧环境原样复现。
- 归档中的 13R D16「五分一三六二」、D18「八千四百二十四六四〇八」均不因此更改；不据此新增任何纸本证据票。

具体解码像素哈希三项见机器证据 `docs/research/TIANWEN-13T-NLC-GORYEOSA-CROSS-RUNTIME-PIXEL-DIGEST-CORRECTION-R1.json`。修复后在同一独立采集工作流重跑，并上传含结果 JSON 的新 artifact；只有该 exact-HEAD Actions 通过才能声明跨运行环境校验成功。

国图第一方物品号、抄本印年、与 CADAL 的独立实物关系仍未解决，TW-OPEN-0005 及全部11个研究风险保持未结；来源647+87、Matrix222/222、传承谱252/238、确定性排盘R1 CLOSED、算法重开0。