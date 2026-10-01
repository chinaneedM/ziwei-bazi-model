# Fusion Chart Historical Provenance Audit R1 — Batch 12JY

## 国图《永乐大典》综述：12JK 同一数字对象重放与去重控制

Status: **EXACT SAME PDF AS 12JK / URL+BYTES+PAGES+SHA256 IDENTICAL / TEXT-LAYER REPLAY PASS / ZERO NEW INDEPENDENT WITNESS / NO DOUBLE COUNT / ZERO PRODUCT IMPACT**

### 1. 对象去重

12JY 与 12JK 的 PDF URL、755,701 bytes、17 pages、SHA-256 `08bf6adcf9a2d200128a80b26156f9de06731094426a116c44ae02386822af20` 完全一致，因此 `NEW_INDEPENDENT_SOURCE=false`、`INDEPENDENT_EVIDENCE_VOTE_INCREMENT=0`。

### 2. 重放结果

pypdf 6.1.1、无 OCR，再次观察到刘鹏 / 国家图书馆古籍馆、赵万里、《永乐大典展览的意义——一九五一年八月北京图书馆举办》、《文物参考资料》1951年第9期、221–233页。该结果提高重放可靠性，不增加来源独立性。1951 原期页面与 2011《赵万里文集》第1卷 p.197 仍未直接审读。

### 3. 控制证据

- workflow: `.github/workflows/probe-batch-12jy-nlc-yongle-review-zhao-bibliography.yml`
- controlling head: `3062fdc5d9ae6cc9c97af7c2cfe7fe8748f54b1a`
- successful run/job/artifact: `36847389443 / 110320683285 / 11153598753`
- artifact digest: `sha256:d48f3e3d55e8e02c9363627a6b10519dbae4e1f0c9a614217345148a59cbf1b6`
- superseded failed probe run: `36846917167`

### 4. 防火墙与项目影响

同一 URL + bytes + pages + SHA-256 对象不得因重复下载或换工作流而变成第二票。Transmission Graph 不新增节点/边。Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。

### 5. 下一门

停止对同一现代 PDF 的重复加权，继续直接恢复上海《文汇报》1951-08-18、《文物参考资料》1951年第9期 pp.221–233 与 2011《赵万里文集》第1卷 p.197。

Research record: `docs/research/ZIWEI-NLC-YONGLE-REVIEW-JK-SAME-OBJECT-REPLAY-DEDUP-R1.json`.
