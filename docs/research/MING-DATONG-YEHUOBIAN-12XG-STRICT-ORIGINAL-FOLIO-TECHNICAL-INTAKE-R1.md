# 12XG — 原叶接收技术漏洞修复：真实解码、官方域名及鉴证边界

本批修复 **12XD 已知真实输入可信性不足**，不增加任何清代版本的古刻证据。

原 12XD 的 `check_receipt()` 曾接受任意以 `https://` 开头的来源 URL，以及 **只有 PNG/JPEG/PDF/TIFF 文件头、无法真正打开的伪文件**；如果提交者同时填写对应哈希，旧程序会输出 `METADATA_COMPLETE_PENDING_HUMAN_PAGE_AND_PLATE_REVIEW`。该标志原本从未代表确证古籍，但仍可能误导未来导入操作。

## 本轮前瞻修复

- 原版机器账本原封不动保存；修改 12XD **生产 CLI** 使有 `--image-file/--receipt-json` 时必须调用新 **12XG 严格校验器**。
- 继续保留已有的条码、馆方请号、卷、篇、原始文件字节数与 SHA-256 交叉检查；但不再仅凭自填哈希/格式文件头就认为文件通过图像完整性核验。
- URL 必须是 `https` 且 hostname 精确为东京大学馆方 `ioc.u-tokyo.ac.jp` 或 `www.ioc.u-tokyo.ac.jp`；拒绝攻击者后缀域名、用户名混淆、控制字符、非标准端口、片段；对多层百分号编码的 1959 排印本已知图片路径作拒绝。
- 新程序使用 Pillow 的 `verify()` 和 `load()` **分别检查图片容器结构与实际像素解码**，记录格式与像素尺寸，并限制过大像素对象。支持 PNG、JPEG、单页 TIFF；PDF 因可能是多页或非原图，必须先有独立页映射/提取流程，不以 PDF 头自动放行。
- 如馆方采用馆外文件交付链接，先标为 `QUARANTINE_PENDING_INDEPENDENT_STAFF_COPY_BINDING`，之后需明确有出处的馆员回执和网址归属桥梁，不因 URL 是 HTTPS 就自动放行。
- 即使所有技术检查成功，返回状态亦仅为 `TECHNICAL_BINARY_AND_URL_CONSISTENCY_ONLY_PENDING_INDEPENDENT_CUSTODY_AND_GLYPH_REVIEW`，明确**未独立核验馆方回执真伪、复制许可、实物印次或四处异文字形**。

## 回归测试

新增覆盖伪 PNG、恶意后缀域名、URL userinfo 混淆、错误端口、百分号编码现代本路径、PDF 误当原刻单页、可正常解码的 PNG/JPEG、损坏图片、自报告伪授权及 1827/1869 条码串用的多项负例。测试图像均由程序合成，**非古籍影像、没有独立古刻票**。CI 精确 HEAD 验证原有 12XD 和新 12XG，固定由 12XG 的真实 CLI 入口驱动。

本批不新增注册来源：源 647+59=706、Matrix 222/222、修复 45/45、谱图 252/238、正式 487 批、古籍页零、古刻票零、算法重开零。来源范围见 `docs/research/MING-DATONG-YEHUOBIAN-12XG-STRICT-ORIGINAL-FOLIO-TECHNICAL-INTAKE-R1.json`。
