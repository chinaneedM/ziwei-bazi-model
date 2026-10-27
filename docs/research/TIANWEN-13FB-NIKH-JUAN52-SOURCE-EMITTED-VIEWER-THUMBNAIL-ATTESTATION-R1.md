# 天问历史考据 13FB｜《高丽史》卷52奎貴5553官方阅览器与两张缩略图的实取证

## 本轮首次阳性取证的边界

GitHub Actions [40055193124](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40055193124) 以只读方式取得卷52文章的官方原文图像阅览器 HTML。其页面 http=200，长度 22,767 字节，SHA256 `25ecd6a4672bdaa29d188409c6c10e1c7050cc7481b54c6f9cf3fb1417f28342`。阅览器地址由 NIKH 官方文章 `fnImageViewerPopup('kr_052_0010_0010_0020_0020','kr_052_1055')` 菜单和官方脚本 `nikhhdb.js` 生成，而非猜接口。

阅览器 HTML 直接呈现23个连续*数字文件标识*，`kr_052_1055.jpg` 至 `kr_052_1077.jpg`，以及 `mode=thumb` 缩略图链接。注意：数字文件序列不等于古籍叶码，更不等于46实物册中的卷52所在册。

本轮至多尝试前三张官方明示的 URL，实际两张JPEG通过文件头校验并获得 SHA-256；另一张仅遇 RemoteDisconnected，不得将传输失败解释为缺页或缺载本。

| 试验 | 结果 | 字节数 | SHA256 |
|---|---|---:|---|
| kr_052_1055.jpg | 200, JPEG | 2134 | 712067426574f5496d39de24a619a6f930bb059fb58c91e40941f5984d1d51d3 |
| kr_052_1056.jpg | RemoteDisconnected | 0 | NULL |
| kr_052_1057.jpg | 200, JPEG | 2217 | 1351f2cf029bd01ba2915c77d2b16a10eb47415df987e8fc0c9671f09f9be26a |

本轮两张图只是站点缩略图，**并未取得支持逐字判读的高分辨率原始书叶照片**。不能以页面正文编辑汉字或缩略图推定「五」替代 NCL p74 上局部印迹所见「〇」。必须继续绑定源书具体实体卷册、叶码、源图及 SHA，并进行无 OCR 直接校勘。

## 不增加虚假的独立来源

本次只是对13FA已登记的 NIKH—奎貴5553 路由作来源像素等级升级，并非新增另一古籍版本。因此外部来源总数仍为761，Matrix222/222、谱252/238，11 OPEN/BLOCKED，产品 CLOSED、算法重开0。G893六项原字、冬D16／夏D30完整历史数值继续未知，13EI撤回保持。

机器证据：`docs/research/TIANWEN-13FB-NIKH-JUAN52-SOURCE-EMITTED-VIEWER-THUMBNAIL-ATTESTATION-R1.json`。
