# 天问12TC｜12TB影像配准的可复算工具

新增 `scripts/replay-yehuobian-image-registration-12tc.py`，接受两个**现存已核验的原样JPEG**：

```bash
python -m pip install numpy opencv-python-headless
python scripts/replay-yehuobian-image-registration-12tc.py CADAL_p121.jpg XUXIU_1174_p506.jpg
```

不得传入截图拼图、网页缩略图或重新导出的JPEG；脚本先校验两个SHA256与像素维度，否则失败，不发起外部HTTP访问。图像来源仍为12QE的GitHub artifact `11671393253`、12SW的artifact `11726061430`。

使用注册的裁剪区域、SIFT 4500点、0.75比率检验、RANSAC 3.5像素拟合以及配准后Pearson相关，以复核12TB的人为校勘判断。结果不自带原古籍的独立印次证明，绝不自动追加传承边或赋予夏至一／三刻的年代。

本批只是重放工具，不新增来源、正式历史研究批次或算法变更。