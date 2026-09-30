# Fusion Chart Historical Provenance Audit R1 — Batch 12JC

## 全国报刊索引 / 中国近代报纸资源全库：当前匿名公开入口与 source-emitted 检索契约边界

Status: **DOCUMENTED PUBLIC ENTRY URLS PROBED / ROOT + HOME + V1 ALL HTTP 412 / NO SOURCE-EMITTED SEARCH FORM / NO SOURCE-EMITTED TARGET-SEARCH LINK / NO TARGET QUERY SUBMITTED / CURRENT UNIVERSITY ACCESS GUIDES DESCRIBE CAMPUS-IP OR VPN/PROXY ACCESS / TARGET PRESENCE OR ABSENCE NOT ADJUDICATED / DIRECT 1951 PP.221–233 STILL NOT REVIEWED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

### 1. Purpose

Batch 12JB 已把《文物参攷資料》1951 Vol.2 no.9 推进到奈良文化財研究所第一方精确单期 item，但赵万里 pp.221–233 仍未取得公开页级对象。

12JC 检查另一个潜在全文/索引面：上海图书馆《全国报刊索引》体系的中国近代报纸/报刊资源平台。目标不是绕过机构授权，而是先回答：

> 当前匿名公开入口是否自己发出一个可以合法继续使用的检索契约？

只有页面自己发出检索表单/链接，后续才允许提交赵万里题名；否则必须停止。

### 2. Documented entry surfaces

当前高校图书馆公开使用说明给出：

- 复旦大学图书馆：`https://www.cnbksy.com/v1`；说明校园网直接访问，校外经 VPN / 图书馆代理；
- 清华大学图书馆 2026 试用说明：`http://www.cnbksy.com/`，明确按校园网 IP 控制；
- 上海大学图书馆资源指南亦列出 `https://www.cnbksy.com/home`。

这些说明只用于确认**公开文档给出的入口与访问模型**，不证明目标文献已经收录。

### 3. Reproducible anonymous probe

Probe workflow:

`.github/workflows/probe-batch-12jc-cnbksy-public-search-contract.yml`

Successful run:

- probe commit: `6af8c874ec8ec71b15e7667428374b13c3d9a8d2`
- workflow run: `36757445087`
- artifact: `11116971947`
- artifact digest: `sha256:cf98bdd869640721fddc9fe8b39719b859ea040b9055a6c4734e031d6f9fdfbf`

Anonymous GET results:

| Documented entry | Status | Forms | Source-emitted candidate search links |
| --- | ---: | ---: | ---: |
| `https://www.cnbksy.com/` | 412 | 0 | 0 |
| `https://www.cnbksy.com/home` | 412 | 0 | 0 |
| `https://www.cnbksy.com/v1` | 412 | 0 | 0 |

No login, account, subscription, VPN, proxy, campus-IP impersonation or guessed API endpoint was used.

### 4. Search-contract adjudication

Because all documented anonymous entry surfaces stop at HTTP 412 and emit neither a public search form nor a target-search link:

```text
CNBKSY_ANONYMOUS_PUBLIC_SEARCH_CONTRACT = NOT_OBSERVED
TARGET_QUERY_SUBMITTED = false
TARGET_TITLE_RESULT_COUNT = NOT_MEASURED
TARGET_ABSENCE_AUTHORIZED = false
```

This is an **access-contract boundary**, not a zero-result search.

Therefore 12JC explicitly forbids:

- saying CNBKSY has no Zhao Wanli article;
- saying CNBKSY has no 1951 issue-9 scan;
- constructing or guessing a private search/API URL;
- using an unrelated institution's VPN/proxy/IP entitlement;
- treating HTTP 412 as a bibliographic negative.

### 5. Relation to existing direct-page gates

The following remain unchanged:

- 2011《赵万里文集》第1卷 p.197: `NOT_REVIEWED`;
- 1951《文物参考资料》第9期 pp.221–233: `NOT_REVIEWED`;
- 1997《北京图书馆馆史资料汇编（二）》pp.446–449: `NOT_REVIEWED`;
- `wwck195109.pdf`: locator known, public bytes/hash not recovered.

12JC adds no text witness and no historical transaction fact.

### 6. Project consequence

- Matrix: 198 rows / 166 audited
- MISSING_FROM_PRODUCT: 10
- provenance metadata defects: 17 / 17 repaired
- chart algorithm defects: 0
- algorithm reopen: 0
- candidate collapse: 0
- transmission graph change: none
- runtime/product change: none

### 7. Next gate

1. Continue new lawful public/institutional **page-level** discovery for 2011 p.197.
2. Continue public-object recovery for 1951 issue 9 / `wwck195109.pdf` without bypassing CNBKSY access control.
3. Continue 1997 pp.446–449 direct-page recovery.
4. Revisit CNBKSY only if a public source-emitted search contract becomes observable or the user supplies legitimate institutional access in a context where its use is explicitly authorized.

Research record: `docs/research/ZIWEI-WENWU-1951-CNBKSY-PUBLIC-SEARCH-CONTRACT-ACCESS-BOUNDARY-R1.json`.
