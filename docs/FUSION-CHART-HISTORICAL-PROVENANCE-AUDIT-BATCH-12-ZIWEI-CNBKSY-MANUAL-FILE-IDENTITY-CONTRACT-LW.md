# Fusion Chart Historical Provenance Audit R1 — Batch 12LW

## 全国报刊索引：老/新平台用户手册文件格式身份

Status: **BOTH TEXT-BOUND OBJECTS ARE OOXML/ZIP DOCX / OLD VISIBLE .doc LABEL STALE / NO FULL MANUAL PARSE / ZERO PRODUCT IMPACT**

控制 run `36893554861` / job `110474819282` / artifact `11179105119` 在 exact head `03fc4ae73445643e0538edbd25636d25ba8fcd0b` 上，仅对 12LV 已有文本绑定的两份主手册发送 `Range: bytes=0-8191` GET；不跟随重定向，每个对象最多读取 8192 bytes，不解析正文。

老平台对象 `https://www.cnbksy.com/common/uploadFile/5efc186123b099148b42c395` 返回 HTTP 200，Content-Disposition 解码为 `平台用户手册.docx`；前缀 magic 为 `50 4b 03 04`（ZIP），不是 OLE CFB `d0 cf 11 e0 a1 b1 1a e1`。因此页面可见“平台用户手册（老平台）.doc”中的 `.doc` 是陈旧/不准确展示标签，实际对象按文件证据裁决为 OOXML/ZIP `.docx`。

新平台对象 `https://www.cnbksy.com/common/uploadFile/65e9592f7fa00c5f66cdb1f5` 返回 HTTP 200，MIME 为 OOXML Word 文档，Content-Disposition 解码为 `平台用户手册（新平台）.docx`，同样以 ZIP magic 开头。

本门没有检查 12LV 的空锚点或图标对象，也没有展开任一手册正文。下一门 12LX 只获取**新平台**主手册，先验证 OOXML 包结构，再从 `word/document.xml` 本地提取检索语义的词频与有限上下文；仍不调用任何实际检索接口。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-MANUAL-FILE-IDENTITY-CONTRACT-R1.json`.
