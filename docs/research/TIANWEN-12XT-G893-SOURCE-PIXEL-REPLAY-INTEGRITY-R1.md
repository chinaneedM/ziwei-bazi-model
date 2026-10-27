# 天问 12XT — G893 源 JPEG／局部像素摘要离线重放验收

12XS 已记录 3 个目标原页 D16/L101/L124 共 9 处原生像素区域，但仅凭存入仓库的摘要一致，CI **无法自行从真实古籍影像重算证明摘要成立**。本次增设独立可执行脚本 `scripts/replay-g893-12xs-original-pixels-r1.py`，并在本次实际保留的合法原图 ZIP 上执行完整重放。原图 ZIP 全档 SHA-256：`ee9ecf1de3bb6abe5678e0f8ec8383ef985051e77d091ee40840756e57081107`。

执行命令：

```sh
python scripts/replay-g893-12xs-original-pixels-r1.py --archive /path/to/authorized/g893-original-images.zip
```

现场重放结果为 **PASS**：204 张原 JPG 字节摘要 204/204 一致，9 个 ROI 原生 RGB 像素摘要 9/9 一致；同时检查整包 ZIP SHA-256、ZIP CRC、原图 1150×2000 大小、页 ID、表头页与目标页、矩形像素边界及 12XS 的来源限定解释。执行期间 **无 OCR**，不会把像素一致转换为任何目标数值、表义、跨版传承结论。

另有 tests/test_replay_g893_12xs_original_pixels_r1.py 单元测试，仅以合成 RGB 图片验证计算与失败关闭机制；合成图像是工程 fixture，**不是历史文献见证**。目前 GitHub Actions 不持有 33MB 的真实原图 ZIP，因此 CI 能验证脚本逻辑，但不能宣称每次 CI 都完成了真实古籍影像的 204/9 重放；只有传入独立来源真实 ZIP 的离线运行才产生本报告的物理文件验证等级。

上轮状态、原 L114 字段核定及 11 项遗漏台账继续有效；G893 6/6 日次定位、1/6 完整字段核定，跨版本最终机械数值对勘仍是 0/6。来源 706、传承谱252/238、历史 Matrix222/222、排盘 R1 CLOSED、算法重开 0 不变。
