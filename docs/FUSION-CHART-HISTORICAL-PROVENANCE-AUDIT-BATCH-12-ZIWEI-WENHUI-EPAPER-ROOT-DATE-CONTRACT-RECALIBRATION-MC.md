# Fusion Chart Historical Provenance Audit R1 — Batch 12MC

## 上海《文汇报》官方电子报根入口日期契约再校准

Status: **OFFICIAL ROOT RE-TESTED / CONNECT TIMEOUT / NO HTTP SURFACE / NO DATE CONTRACT / TARGET 1951-08-18 NOT REQUESTED / BRANCH STOPPED PENDING NEW ACCESS MECHANISM / ZERO PRODUCT IMPACT**

12MB 已停止 CNBKSY raw-HTTP 文本检索支线。12MC 回到最核心未决目标之一——上海《文汇报》1951-08-18——但严格遵守 12JO 的门禁：**不按现代 URL 模式拼 1951 历史路径**，先只重测官方电子报根入口 `https://dzb.whb.cn/` 是否能在当前 exact-head runner 上给出新的 redirect/static/source-emitted 日期契约。

控制 run `37023569701` / job `110892443388` / artifact `11234345292`（exact head `a31ae1aee678af027bc9d98c558e48fd586305b2`）只发起匿名 GET，`allow_redirects=false`。结果在 45 秒连接阶段触发 `ConnectTimeout`，没有获得 HTTP status、HTML、form、script 或日期链接。

这与 12JO 的旧边界一致：12JO 对同一 official root 和一个已知现代日期 control 均在控制 runner 上超时。因此 12MC 是**可达性边界复核**，不是“1951 页面不存在”的新证据，也不增加独立历史证据票数。

裁决：

```text
OFFICIAL_ROOT_REACHED = false
SOURCE_EMITTED_DATE_CONTRACT = NOT_OBSERVED
TARGET_1951_08_18_REQUESTED = false
DIRECT_1951_08_18_PAGE = NOT_REVIEWED
TIMEOUT_AS_ABSENCE = FORBIDDEN
WENHUI_EPAPER_RUNNER_BRANCH = STOPPED_PENDING_MATERIALLY_NEW_FIRST_PARTY_ACCESS_MECHANISM
```

不允许继续重复 runner 重试、猜日期路径、关闭 TLS 校验或绕过站点访问机制。

下一门 12MD 转向独立、公开、机构主办的现代学术见证：浙江图书馆《图书馆研究与工作》官方过刊页。12MD 先读取过刊页，再只跟随其 source-emitted `2026 No.4` issue link，盘点肖玲《赵万里与古籍保护》及 PDF/article href；本门不下载 PDF。即便后续关闭《赵万里文集》第一卷 p.197 引用，它也只能作为现代二级学术见证，不能替代 2011 p.197 直页或 1951 原始载体。

控制证据：workflow `.github/workflows/probe-batch-12mc-wenhui-epaper-root-date-contract-recalibration.yml`; run/job/artifact `37023569701 / 110892443388 / 11234345292`; artifact digest `sha256:bce74a374b720f064faf87359ec9cf307ee5dfad7797167d1854473d8296bb15`.

Matrix 保持 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission impact = NONE。

Research record: `docs/research/ZIWEI-WENHUI-EPAPER-ROOT-DATE-CONTRACT-RECALIBRATION-R1.json`.
