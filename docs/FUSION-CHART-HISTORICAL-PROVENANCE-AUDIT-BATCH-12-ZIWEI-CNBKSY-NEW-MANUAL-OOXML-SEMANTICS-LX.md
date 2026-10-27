# Fusion Chart Historical Provenance Audit R1 — Batch 12LX

## 全国报刊索引：新平台官方用户手册 OOXML 检索语义

Status: **2024 NEW-PLATFORM OFFICIAL MANUAL CLOSED / ORDINARY+ADVANCED+PROFESSIONAL SEARCH DOCUMENTED / FIELD-CODE TABLE VALUES STILL OPEN / NO SEARCH EXECUTION / ZERO PRODUCT IMPACT**

控制 run `36894241310` / job `110477103951` / artifact `11179100973` 在 exact head `97e5a720cebf5e9357be1fa62ebcaa1a4c95ca37` 上，只下载 12LV/LW 已绑定并确认格式的新平台手册 `https://www.cnbksy.com/common/uploadFile/65e9592f7fa00c5f66cdb1f5`，不跟随重定向、不调用任何检索 endpoint。

文件为 23,137,465 bytes，SHA-256 `51cdcd228ae5cc64708399fd0454c6629606a1fbe3364bd2079eec69742f5dcc`；OOXML ZIP 共 87 members，`[Content_Types].xml` 与 `word/document.xml` 均存在，后者 SHA-256 `daca1f2072457d63360655c44965afe6ab1a04780722ff38c92b8e9d91e347e3`。Core properties：creator=`Apache POI`，created=`2024-02-06T05:23:00Z`，modified=`2024-03-07T05:17:00Z`，lastModifiedBy=`王琳璘`。

本地提取正文 182 paragraphs / 4706 chars / SHA-256 `c2b2e343a49ece944590f03cc60cb03db7a93049011cc6b1ac4c8b744305de2`。手册明确描述新版平台于 2024 年春季推出，并列出普通检索、高级检索、专业检索等功能。

高级检索：不同正文/图片/广告页签可用字段不同；可用全字段或题名、作者、文献来源等单字段，可限制时间区间并选择精确/模糊方式；条件可增删，关系为“与/或/非”。专业检索：不同类别使用不同字段代码表，以 Solr 检索表达式进行查询，按“字段代码:内容”书写，多条件用 `AND` 拼接。

关键限制：段落文本没有给出实际字段代码值。示例文字中还出现“提名”“刊名/报名”等疑似编辑/排版文字，必须原样保留，不能擅自校正成字段代码。因此 12LX 只闭合**操作语义**，不闭合专业检索字段代码表，更不据此执行目标检索。

下一门 12LY 只在同一官方 DOCX 内定位 `4.3 专业检索` 到 `4.4 检索结果可视化` 之间的 OOXML drawing/image 关系，导出该节局部媒体及结构清单；不 OCR、不调用检索接口。若字段代码表确实是截图，再以图像证据单独审计。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-NEW-MANUAL-OOXML-SEMANTICS-R1.json`.
