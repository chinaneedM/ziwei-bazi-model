# 天问 13HR｜NDL991069 第72幅馆方完整图像采集检查点（尚未校读）

**证据状态：ACQUIRED_SOURCE_JPEG_UNREAD**。本检查点只记录馆方图像已实际获得，不升格或复写 13HQ 的文字校读结论；不关闭任何 P0/P1 遗漏问题。

## 唯一来源绑定

- 来源：日本国立国会图书馆公开 IIIF，《高麗史》卷52，1909 年刊本，PID `991069`。
- 入口：`https://dl.ndl.go.jp/api/iiif/991069/manifest.json`；返回字节 SHA-256 `5ef67e4f84917ffd1eafee2b2da1d22f1aeb68f8d7f2ac441b7d398be19bf674`。
- Source-emitted canvas：`https://dl.ndl.go.jp/api/iiif/991069/canvas/72`。
- Source-emitted image service：`https://dl.ndl.go.jp/api/iiif/991069/R0000072`。
- 请求：`https://dl.ndl.go.jp/api/iiif/991069/R0000072/full/full/0/default.jpg`。
- 首次成功工作流：[13HR run 40318641214](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40318641214)，原始产物 artifact `12648046803`，名称 `tianwen-13hr-ndl991069-canvas72-full`；脚本离线单测 4/4 成功、图像获取成功。
- 首次响应 JPEG：`canvas-072-full-provider.jpg`，**3773 × 2943**、**2,974,705 bytes**、SHA-256 `83f76e06aad3ab3d8f1c757c69a8d2d8450086acce6baf71d900b1c0d3ade9cd`。此前 13HQ canvas72 的预览图仅 1600 × 1248，SHA-256 `295a3a839914f51a33c19f6e7cea6c113413d9bcb3c2423c60589bb51bdf5c86`。
- 脚本生成了两个 **approximate_locator_only** 的放大备读 ROI，未执行 OCR、未人工确认坐标对应字形：`winter-heading-context.png` / SHA-256 `48e69fea11f5dedd747b3ee23f7867bd56698f4c8b47a49eabcffbb3d5d21933`；`initial-days-context.png` / SHA-256 `37457a4c5f1ddece3cf39352b6da2c03f75f29242fe651d728827bb32f71fe3a`。另有左叶上下文 PNG SHA-256 `54ed791899d299817c76fb33b191ee307d203bcfa375ce78a35adeab85c91f68`。

## 不可越过的研究边界

本次采集不是校勘，也不生成新的独立物理副本；**同一 1909 刊本的第72/73幅不能算两个古本见证**。13HQ 已在较低分辨率预览上完成的「太陽冬至前後二氣盈初縮末限」及初日至五日文字定位，现获可用于进一步复核的第72幅高分辨率来源图；本批**尚未重审该图的每个字**，不能因分辨率升级就声称已通过复核。

1909 年刊本的冬至相关表与 NIKH 独立夏表、台湾 NCL 03130 第52卷旧钞／光绪补钞仍保持隔离。NCL 原十四日完整字段、尾字、原叶版本层次、古计量单位及 G893 六控仍然未决；13EI 既往误判继续 RETRACTED；算法重开、候选合并、谱系新增均为 0。本次**没有**修改 Matrix、登记来源数或当前项目语义状态，也没有提交任何付费／授权馆藏申请。

## 下一证据动作

从保存的 **原始 JPEG** 重新裁出标题、日次和列名，进行逐字人工校读及 bbox+SHA 绑定；若读数或坐标与 13HQ 不同，必须 forward-only 登记勘误。台湾 NCL 03130 获准原叶仍是更高价值的独立早期证据，不能用此次同源分辨率升级替代。

关联：`TW-OPEN-0005`、`TIANWEN-13HQ-NDL991069-CANVAS72-73-WINTER-SURPLUS-DEFICIT-CONTEXT-R1`。
