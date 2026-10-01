# Fusion Chart Historical Provenance Audit R1 — Batch 12LE

## NDL《趙萬里文集》第1卷：item-level access block 收口

Status: **MAIN CONTENT ISOLATED / EXACT OBJECT PRESENT / DIGITAL COLLECTION=0 / INTERNET PUBLIC=0 / REMOTE COPY=0 / NUXT CSS FALSE POSITIVES REJECTED / PHYSICAL-HOLDING-ONLY / DIRECT P197 NOT REVIEWED / ZERO PRODUCT IMPACT**

12LD 已证明 NDL 公共记录没有明显对象级数字访问标记，但页面全局页脚带有“网上阅读 / 获取复制件”等通用帮助链接。12LE 去掉 footer，只审查 item-level 主内容和嵌入记录数据。

主内容仍直接包含：

```text
趙萬里文集
UM11-C247
NDLBibID 023434359
```

而以下对象级访问标志全部为 0：

```text
国立国会図書館デジタルコレクション
デジタルコレクション
インターネット公開
図書館・個人送信
遠隔複写
複写
オンライン
利用登録
ログイン
```

启发式扫描出现两个包含 request/copy 字样的 URL：

```text
/_nuxt/PagesRequestIllText.Cr5cuJ0I.css
/_nuxt/PagesBeforeCartRcopyDialog.CU-8Mr9c.css
```

它们只是 Nuxt CSS 静态组件资源，不是该书的访问链接，更不构成复制资格。嵌入 payload 中仅出现 2 个英文 `copy` 字符串，其他 digital/digitized/online/internet/remote/available 及日文访问词均为 0。

因此：

```text
NDL EXACT PHYSICAL HOLDING = CLOSED
ITEM-SPECIFIC ANONYMOUS DIGITAL ROUTE = NOT EMITTED
DIRECT P197 = NOT REVIEWED
ROUTE STATUS = PHYSICAL_HOLDING_ONLY
```

控制证据：workflow `.github/workflows/probe-batch-12le-ndl-zhao-wenji-item-access-block.yml`; exact head `297a0cf646894d23afc5e6af5240255837c7e206`; run/job/artifact `36876673520 / 110417773346 / 11169027334`; artifact digest `sha256:5d19d8d71529f525ca60a4ecfc8e014a4ec77bb5780994fb2b595dcb7e6a8bf1`。

下一门 12LF 转向上海《文汇报》1951-08-18 primary-text 线索。上海图书馆主管的《全国报刊索引》公开资料表明其报纸资源覆盖至 1951；先只恢复官方公开检索面的表单/脚本/访问边界，不提交赵万里查询。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

Research record: `docs/research/ZIWEI-NDL-ZHAO-WENJI-ITEM-ACCESS-BLOCK-R1.json`.
