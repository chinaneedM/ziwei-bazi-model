# 天问历史考据 13FD｜《高麗史》卷52 奎貴5553 官方原图保存路由单页阳性取证

## 来源链与复核锚点

13FC [GitHub Actions #40056037073](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40056037073) 在 NIKH 卷52官方原图阅览器（SHA-256 `25ecd6a4672bdaa29d188409c6c10e1c7050cc7481b54c6f9cf3fb1417f28342`）源码中取得两份**页面明示的官方 JS 文件**。配置文件 SHA-256 `42d967840816a0d21ad8ee9cfa9f9bde8c1ffde59fe49e8a6adf86f6ab6accc8`，主查看器脚本 SHA-256 `87e8a9dfcf57083e2641939bf6fe87f1713245fbb7e8563d3e0128083a221655`。官方代码的 `saveOri()` 组合 `proxyFile`、`filePath` 及 `mode=download`；不依靠猜测路径。

13FD [GitHub Actions #40056191954](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40056191954) 对相同脚本/阅览器 SHA 逐项重核，通过后**只请求一张**页面源数组中的 `kr/052/kr_052_1055.jpg`：

- 官方动作生成 URL：`https://db.history.go.kr/common/imageProxy.do?filePath=/kr/052/kr_052_1055.jpg&mode=download`
- HTTP **200**，返回 **256370 字节**；虽然 HTTP Content-Type 为 `application/x-msdownload`，文件头为 JPEG `FFD8FF`，实际图像尺寸 **1025 × 2000 像素**。
- 完整 SHA-256：`487718d8cf0e92d7a1d498ed72d3d3f42773cb3fa096ab962302a09716897bc6`。
- 可复核 Actions artifact：**12545535910**，含 `probe-result.json` 与 `one-official-save-image.bin`；先前 JS 证据 artifact **12544894866**。

## 无 OCR 原页初审及严格边界

已人工查看获得的 JPEG：为带有传统纵列汉字、节气与数字栏的历史表页影像，**不是可直接证明目标 D5 字形的已定位源页**。取得官方“保存原图”字节不等于已证其物理册、原叶页码或印本版次，更不等于已经逐行校读整卷。文件现代顺序号1055不得自动当作古籍叶码。本轮也未下载剩余22张，未作凭空接口枚举、权限绕过或批量扫描。

原 NCL p74 局部照片读作 D5 `四分〇一七二`，KRDB 编辑正文作 `四分五一七二`。二者仍处于**异源等级冲突而非已决版本异文**；本次新图尚未绑定该 D5 行，零新增原字裁决/零谱系边。

D1—D6「四分／初度」栏位同一性、D4—D6原数尾、夏D30、冬D16、G893六控制目标仍未裁决；13EI错误来源结论保持撤回；NCL清代与1905抄层不合并。

## 状态及下一门禁

Matrix **222/222**，外部史料登记 **761**，谱图 **252节点/238边**，风险 **11项开放或访问受阻**，排盘 R1 **CLOSED**，算法重开 **0**，保持不变。后续仅按出版者明示的图像序列逐页定位卷52指定表格和 D5 行，再从确切物理册叶、图像 SHA、字形局部与邻列行数建立可回放的逐字校勘；一张原图只算同一传本的一份证据，不额外计票。

机器证据：`docs/research/TIANWEN-13FD-NIKH-JUAN52-ONE-PUBLISHER-SAVE-JPEG-SOURCE-GATE-R1.json`。
