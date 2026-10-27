# 天问 13GT — 13GS 后 exact-HEAD CI 失败恢复（研究行动前缀同步）

**故障观察**：新提交 `e0847b1aae208bf8cdf36df2b3e084277cbcf104` 的 13GS 源像素几何专项 Actions `40194213247` 已成功，但原有 13GE、13FH、13FN、13GB、13GG、13FI、13FG、13FM、13FK、13GA 等多条工作流失败。现场 Python traceback 均在相同条件 `issue["next_action"].startswith(ledger["binding"]["latest_research_focus_prefix"]+" CURRENT ACTION:")`；13GS 版本已把 latest prefix 更新到 13GS，而 TW-OPEN-0005 `next_action` 仍为 13GR 开头。属于**研究交接账本即时行动文字与版本绑定不一致**，不是古籍原字发生变化。

**修复**：发布前瞻变更，将 `TW-OPEN-0005.next_action` 改为随本批 `13GT CURRENT ACTION:` 严格同步；在原 `history` 末尾保存 prior 值、变更理由与新证据引用，并完整保留 11 项历史风险。同步 PROJECT-CURRENT-STATE schema `1.849.0` 和遗漏账本 binding/checkpoint。不重写先前 13GR／13GS 源像素图、观测、测试和字形 null。

**边界**：此修复不构成源图字形裁决。十四日完整「四分」数值与末位依旧 NULL；第九／三十日、D5「〇／五」、G893 六处、古代单位仍 OPEN；一份现代数字影像仅是一份证据替身；Matrix 222/222、来源 761、传承图 252/238，零算法重开及零候选坍缩。**新 HEAD 的 exact-HEAD Actions 必须重新检查**；修复前一次失败不得被当成成功。

恢复工作记录：<https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40194213247>；原始几何证据为 `docs/research/TIANWEN-13GS-NLC-P74-D14-GEOMETRIC-LANE-CONTINUITY-R1.json`。
