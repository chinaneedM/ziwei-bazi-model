# Fusion Chart Historical Provenance Audit R1 — Batch 12NZ

## HPA-ZMINOR-023 月解 / month-based 解神：历史几何与时层身份收束

Status: **HISTORICALLY_SUPPORTED FOR MONTH GEOMETRY / ZIWEI ADOPTION PATH UNRESOLVED / YEAR-MONTH IDENTITIES SEPARATED / NO ALGORITHM REOPEN**

当前 `STAR.JIESHEN` 使用正二申、三四戌、五六子、七八寅、九十辰、十一十二午。Batch 07C 只确认其现代运行时稳定，而未取得合格的前现代来源。

本批找到前现代岁时择日传统的直接文字链。曹震圭《历事明原》把解神定义为“月中善神”，并由《历例》给出同一十二月表；该公开数字转录存在个别 OCR 噪声，因此不拿它单独做字形裁决。康熙五十二年（1713）《御定星历考原》卷三以清晰 received text 完整重录正二申、三四戌、五六子、七八寅、九十辰、十一十二午；《钦定协纪辨方书》卷五再录同表，并解释六阳辰/六阴辰的取冲机制。

因此当前 month-based `STAR.JIESHEN` 的十二个月坐标取得 **12/12 前现代历史几何支持**，`HPA-ZMINOR-023` 可从 `SOURCE_INSUFFICIENT` 升级为 `HISTORICALLY_SUPPORTED`。支持范围只包括月表几何及“月中善神”这一时间层身份；仍不能据此声称该月表在元清时已经属于紫微斗数。

必须继续隔离 year-based 解神。`HPA-ZMINOR-006` 的 received Fullbook 规则以年支运行，项目显示为 `STAR.NIANJIE / 年解`；本批月表以农历月份为输入。前现代历法文本把月神直接称为“解神”，而紫微 received Fullbook 又把年规则称为“解神”，说明同名并不能证明同一对象。项目的“年解”是现代消歧标签，不得倒推为古籍固定命名。

《历事明原》《星历考原》《协纪辨方书》均把定义/表式继续上溯到《总要历》《历例》，但这两个被引来源的具体书目身份、recension 与现存直接规则文本尚未关闭，因此谱系只记录 citation layer，不伪造更早实体见证。

本批不修改 `minor_stars.py`、profile、rule-set/version、算法、fact/computation hash、候选选择或默认值；不产生 algorithm reopen。Matrix 仍为 220/220 audited、10 current missing；provenance defects 40/40；chart algorithm defects/reopens/candidate collapses 0。

下一门：**12OA — HPA-ZMINOR-024 天巫 lunar-month table**。先机械推导古籍“常居月建前二辰”是否与当前四宫月表完全等价，再决定状态，禁止只凭同名升级。

Research: `docs/research/ZIWEI-MONTH-JIESHEN-HISTORICAL-IDENTITY-CLOSURE-R1.json`
Evidence: `docs/research/evidence/batch-12nz/ziwei-month-jieshen-historical-identity-evidence.json`
