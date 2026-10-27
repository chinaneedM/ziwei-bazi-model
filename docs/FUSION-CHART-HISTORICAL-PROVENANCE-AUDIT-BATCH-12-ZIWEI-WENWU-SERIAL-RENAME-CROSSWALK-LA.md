# Fusion Chart Historical Provenance Audit R1 — Batch 12LA

## 《文物参考资料》→《文物》：1959 刊名改称 crosswalk 闭合

Status: **CINII PREDECESSOR CLOSED / CINII SUCCESSOR CLOSED / SAME BIBLIOGRAPHIC HISTORY ID / OFFICIAL PUBLISHER RENAME STATEMENT / CARRIER-LABEL TENSION RESOLVED / DIRECT 1951 PAGES STILL NOT REVIEWED / ZERO PRODUCT IMPACT**

12KZ 已把赵万里目标记录锁定到同一个书目束：`1951 / 第9期 / pp.221–233 / 13页`。现代 NCPSsd / 国家图书馆文津显示载体名“文物”，而国家图书馆官方综述与原始 serial 目录显示《文物参考资料》。12LA 不依赖题名相似度，而是直接校准刊名沿革。

CiNii NCID `AA11467834` 记录《文物参攷資料》1950.1–1958.12，1951 为第2卷1–12期，带有 After Rename / Continues by 标记，Bibliographic History ID 为 `41870900`。

CiNii NCID `AN00060837` 记录《文物》自 1959.1 起，1959年第1期同时为总101号，带有 Before Rename / Continues 标记，ISSN `05114772`，Bibliographic History ID 同为 `41870900`。

文物出版社第一方发展史直接记载：`1959年1月，《文物参考资料》月刊改名为《文物》月刊。`

因此：

```text
《文物参考资料》/《文物参攷資料》
  -- 1959-01 rename -->
《文物》
```

对赵万里 1951 记录，历史原期引用仍应写作 **《文物参考资料》**。NCPSsd / 文津的“文物”现在可解释为同一连续刊物链的后继/现代规范化标签，而不是另一种 1951 载体。

本 crosswalk 不证明：1951 原页已经审读；《文汇报》1951-08-18 与期刊版是重刊/修订关系；两载体文字逐字一致；或可用“文物”静默替换所有历史时期的原刊名。

控制证据：workflow `.github/workflows/probe-batch-12la-wenwu-serial-rename-crosswalk.yml`; exact head `9b0e7cf5cf1b4c8bcc361e70235da88120838f10`; run/job/artifact `36870949644 / 110398272473 / 11166419064`; artifact digest `sha256:9418133824dc8378982fcbffb0ebc28a222fabd12e35a8c81ae50223283b27ea`。

下一门回到 primary-text gate：优先取得《文物参考资料》1951 v2 no.9 pp.221–233 的合法公开原页/影像；并行保留上海《文汇报》1951-08-18 与 2011《赵万里文集》第1卷 p.197。

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不新增规则传承边。

Research record: `docs/research/ZIWEI-WENWU-SERIAL-RENAME-CROSSWALK-R1.json`.
