# Fusion Chart Historical Provenance Audit R1 — Batch 12MS

## 四柱本命总生成：年/月/日/时规则分解

Status: **HPA-BAZI-001 DECOMPOSED / 5 CHILD RULES AUDITED / NATAL COMPOSER MODERN_COMPATIBILITY_ONLY / NO ALGORITHM REOPEN**

12MS 不再把“四柱本命生成”视为一条不可拆的古典规则。现行 `BAZI-NATAL-GENERATOR-V1` 只是把已经解析出的年、月、日、时坐标组合成一个现代软件对象；历史权威必须留在各自的边界、干支循环与起干规则上。

### 五个此前未独立登记的子规则

| Rule | 机械范围 | 审计结论 |
| --- | --- | --- |
| HPA-BAZI-016 | 已选 pillar-year 整数 → 六十年干支身份 | MODERN_COMPATIBILITY_ONLY |
| HPA-BAZI-017 | 五虎遁：年干 → 寅月起干并逐月顺推 | HISTORICALLY_SUPPORTED |
| HPA-BAZI-018 | 已选 effective Gregorian date → JDN → 六十日干支 | MODERN_COMPATIBILITY_ONLY |
| HPA-BAZI-019 | 已选 local apparent-solar clock → 十二时支 | MODERN_COMPATIBILITY_ONLY |
| HPA-BAZI-020 | 五鼠遁：显式日干来源 → 子时起干并逐时顺推 | HISTORICALLY_SUPPORTED |

五虎遁已有宋代《五行精纪》路线，明《神峰通考》“起八字诀”又把年上遁月、日上遁时并列保存；清《御定星厯考原》同时保存五虎、五鼠并解释六十月/六十时循环。五鼠运行时对 10 日干 × 12 时支逐项回放，不由本批选择晚子时的“哪一天日干”。

### 现代坐标桥与古典规则防火墙

年干支的 `(pillar_year-4)%60`、日干支的 Gregorian/JDN 桥和固定现代时钟→双时辰投影均登记为现代坐标实现，而不是伪装成古籍原有公式。GB/T 33661-2017 只用于现代六十循环校准；它不能反推成八字立春界或晚子时裁决。

HPA-BAZI-019 只描述“当前选定 clock 的机械投影”。明《卜筮全书》的《定寅时法》保留季节性时刻判断，因此前现代时制不应被静默等同于今天固定钟表区间。

### 既有争议继续保留

- 年/月界继续由 HPA-BTIME-001..004 管理；
- 日界继续保留 HPA-TIME-007 的 MIDNIGHT / ZI_START_23；
- 晚子时日干来源继续保留 HPA-TIME-008 的三个候选；
- HPA-TIME-003 local apparent solar time 仍是现代时间坐标，不被 12MS 升格为古典唯一标准。

因此 HPA-BAZI-001 本身改判为 `MODERN_COMPATIBILITY_ONLY`：不是否定四柱传统，而是拒绝把现代 Natal bundle 当成一条单独的古典教义。

### 账本

Matrix **201→206 rows，178→184 audited**；当前 `MISSING_FROM_PRODUCT` 仍为 10；provenance metadata defects **17/17**；chart algorithm defects / reopens / candidate collapses **0**。运行时、schema、hash 版本均不修改。

传承图不新增边：本批没有裁定新的物理版本祖先、抄传关系或学派继承关系。

下一门 **12MT**：`HPA-STRUCT-003` Structural R3 borrow projection。

研究记录：`docs/research/BAZI-NATAL-FOUR-PILLAR-COMPOSITION-AUDIT-R1.json`；回放控制：`docs/research/evidence/batch-12ms/natal-pillar-replay.json`。
