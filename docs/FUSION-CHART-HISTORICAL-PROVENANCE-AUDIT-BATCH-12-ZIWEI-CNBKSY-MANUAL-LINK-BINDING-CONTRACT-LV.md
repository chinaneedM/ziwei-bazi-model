# Fusion Chart Historical Provenance Audit R1 — Batch 12LV

## 全国报刊索引：老/新平台用户手册锚文本—文件绑定

Status: **TEXT-BEARING MANUAL HREFS CLOSED / OLD .doc↔.docx TENSION PRESERVED / EMPTY ANCHORS+ICONS SEPARATED / NO DOWNLOAD / ZERO PRODUCT IMPACT**

控制 run `36893032541` / job `110473087527` / artifact `11178090449` 在 exact head `29615172edf2ae81ff1226a121147141b4f17fc1` 上重取节点 161，仅静态解析 HTML，不跟随任何链接。

老平台：可见锚文本 `平台用户手册（老平台）.doc` 明确绑定 `/common/uploadFile/5efc186123b099148b42c395`。但同一 <a> 的 `title/textvalue` 写作“平台用户手册（老平台）.docx”，所以扩展名身份必须保持 **UNRESOLVED**，不能按可见文字或 HTML 属性择一归一化。

新平台：可见锚文本 `平台用户手册（新平台）.docx` 明确绑定 `https://www.cnbksy.com/common/uploadFile/65e9592f7fa00c5f66cdb1f5`，HTML title 与可见文字一致。

另有一个空锚点 `https://www.cnbksy.com/common/uploadFile/65c1fb6bf74f7f939f8cec86`，HTML title 为“平台用户手册.docx”；它没有可见锚文本，因此保持 auxiliary，不得替代“新平台”主绑定。另有 `/common/uploadFile/65d85a357fa00c579dfdc79e` 作为 <img>，alt=`icon_txt.gif`，属于图标上下文，不得当成手册主体。JSON 顶层 `linkUrl/linkItemId` 均为 null。

下一门 12LW 只对老/新两个**有文本绑定**的 href 做有界 Range GET：不跟随重定向，只记录响应头、Content-Disposition/Range/Length、前缀 SHA-256 与 magic；不解析正文。先让文件本身裁决老平台到底是 OLE `.doc`、OOXML `.docx` 或其他格式。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-CNBKSY-MANUAL-LINK-BINDING-CONTRACT-R1.json`.
