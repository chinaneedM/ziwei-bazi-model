# Fusion Chart Historical Provenance Audit R1 — Batch 12MT

## Ziwei Structural R3 借宫投影：流派机械规则与现代闭包分离

Status: **HPA-STRUCT-003 DECOMPOSED / 3 SCHOOL-SPECIFIC CHILD RULES + 1 MODERN CLOSURE RULE / NO ALGORITHM REOPEN**

12MT 审计 `ZIWEI-STRUCTURAL-RUNTIME-V2-R3`。结论不是“R3 整体就是一条古法”，而是：R3 把可在现代中州派材料中直接核对的借星机械规则，包装进现代不可变状态、fail-closed、去重和 hash lineage。

### 1. 可直接归属中州派的机械范围

S06 的 Wang Tingzhi / Zhongzhou normalized route 与已登记外部学校见证支持三条独立规则：

- **HPA-STRUCT-009**：本宫无十四正曜才进入空宫借星；辅佐煞杂曜本身不取消“无正曜”资格；
- **HPA-STRUCT-010**：借星从该宫物理对宫取得，并借入对宫完整星曜集合，而不是只借十四正曜；
- **HPA-STRUCT-011**：建立三方四正之前，四个成员宫各自检查；成员空宫时先向自己的对宫借星，再参加会合。

三条均判为 `SUPPORTED_BUT_SCHOOL_SPECIFIC`。这证明的是现代中州派文本范围，不证明它们是所有紫微流派的唯一方法，也不把作者对“前辈传授”的内部叙述自动升级成独立的早期传承证据。

### 2. 明确属于现代软件闭包的部分

**HPA-STRUCT-012** 单列为 `MODERN_COMPATIBILITY_ONLY`：

- borrowed content 只做 reference projection，不物理搬星；
- projection depth 固定一层，双空对宫 fail closed；
- `ZERO_SECOND_CONTRIBUTION` 防止借照、对照、会照重复形成基础贡献；
- `STRUCTURE_PHYSICAL_KEY` 跨 evaluation view 去重；
- R3 自有 schema / FactHash / ComputationHash / upstream hash binding。

这些设计与 S06 的“不得重复贡献/非物理迁移”语义方向相容，但 hash、immutable object、fail-closed status 和 dedup key 都是现代工程实现，不能倒推为传统术语。

### 3. 实现回放

Released R3 仍覆盖 12 个 evaluation origins × 4 个 neutral member offsets `{0,4,6,8}` = 48 facts；空宫判定域严格取冻结的十四主星生成器；辅助星-only 的宫仍可借；成功借入投影 source 全部 Placement 与 source transformation overlays；对宫也空则不递归。

R3 不命名 +4/+8 为左/右合宫，不激活 R4 三方四正 named semantics，不做吉凶、权重、预测，也不选择其它流派赢家。

### 4. Provenance boundary

S06 的 closure 输出设计包含 `SOURCE_ROOT_ATOM_IDS`，而 released `BorrowClosureMemberFact` 只通过 R3 computation lineage 全局绑定 S06 source refs，没有逐 member-fact 序列化 source-root atom IDs。12MT 将其记录为**来源粒度边界**，不虚构 atom 对应，也不因此改动已冻结 R3 schema/hash；若未来补充，应走 additive provenance sidecar。

### 5. 账本

Matrix **206→210 rows，184→189 audited**；`MISSING_FROM_PRODUCT` 仍为 10；provenance defects **18/18**；chart algorithm defects / reopens / candidate collapses **0**。R3 runtime/schema/hash 不修改，传承图不新增边。

下一门 **12MU**：`HPA-STRUCT-005` R5 borrow-resolved Sanfang/Sizheng composition。

研究记录：`docs/research/ZIWEI-R3-BORROW-PROJECTION-AUDIT-R1.json`；回放摘要：`docs/research/evidence/batch-12mt/borrow-projection-replay.json`。
