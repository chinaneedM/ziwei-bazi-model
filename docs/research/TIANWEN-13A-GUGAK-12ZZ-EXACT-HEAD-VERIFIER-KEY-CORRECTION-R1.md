# 天问13A｜12ZZ 的准确 HEAD CI 字段名误用修正

准确旧 HEAD [8cdb11ba](https://github.com/chinaneedM/ziwei-bazi-model/commit/8cdb11ba966504814b471fdcb99676bd10f5554d) 的 [GitHub Actions 主流程 39131994833](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39131994833) 运行时，12ZZ 的专项校验器错误读取 `historical_inference.media_caption_1454_meaning`，因此以 Python `KeyError` 停止。原机读证据文件自12ZZ提交以来一直使用 `historical_inference.ngc_media_caption_1454_meaning`。

**只修验证程序，不改原始证据**：本批将验证器所需键改成实际证据键，并删除一句冗余且容易误读的布尔组合门控，维持原本严谨的 `1454不得自动定为此实物印刷年`、`1613馆藏页未读取则不判版印` 等门控。

本次失败不是新的古籍异文、算法缺陷或来源冲突；未重新解释国立国乐院6426与6545的日期，也不产生第二份实物见证。项目仍保持来源719、11项P0/P1遗留风险OPEN、G893原图5/6及跨原本0/6，图谱未改变，排盘R1 CLOSED。

下一步必须按新HEAD观察12ZZ专项门控、全量CI、工作台冒烟检验真实结果后，才能宣布本次验收成功。
