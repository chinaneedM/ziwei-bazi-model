# Fusion Chart Historical Provenance Audit R1 — Batch 12MI

## 《文物参考资料》第 19–24 号 Google Books 定位与年份边界

Status: **NEW GOOGLE VOLUME LOCATOR / YEAR AND UCD COPY ID UNBOUND / TARGET ORIGINAL TEXT NOT REVIEWED**

Google Books 的第 59–64 号记录通过其他版本链接给出新对象 `-RGcXtePnoQC`。公开书目页明确列出“文物参考資料, Ausgaben 19-24”、China. 文物局、原藏 University of California、数字化日期 2024-06-14；没有出版年或 UC Davis 条码。数字化日期不能当作刊年，泛称加州大学不能替代 UCD 具体副本身份。共同号段也不能替代条码对应。

页面词云含“永樂大典”，只能说明索引词存在，不能识别赵万里文章或证明页码。跟随这一实际 source-emitted 链接时，检索工具报告 Google sorry 重定向后的不可重试错误；没有取得片段，也不把工具错误包装成原站 HTTP 状态。

### 可见图像的范围

实际 source-emitted frontcover 链接返回一张 7506 字节 JPEG 缩略图，SHA-256 `a917bbddeecf0a004b391eda3b65a75b06602f8a49c0fbb6b273fbcaacb5837d`。已视觉检查：小幅竖排中文列表页；不足以辨读出版年月或闭合目标期号。只记一张缩略图检查，不宣称零图像，也不宣称核读 pp.221–233。没有构造高倍率、其他页或未发表接口。

### 访问结果与控制

| 路径 | 实际结果 | 可支持结论 |
| --- | --- | --- |
| HathiTrust OCLC647437409 | 403，239 字节 | 数字对应记录查询受阻 |
| HathiTrust 已知正控制 OCLC424023 | 同一 403、同字节摘要 | 不能据目标失败推断记录不存在 |
| Google 普通书目页，本地 HTTP | 429 / CAPTCHA 重定向 | 本地访问边界；检索服务另能读到书目摘要 |
| Google source-emitted EndNote 导出 | 429 / CAPTCHA | 未取得书目导出 |
| 官方文档支持的 Google Volume GET | 429 / RESOURCE_EXHAUSTED | 服务配额边界，未取得 API volume 对象 |
| NLA 1841982 | 200 / Anubis challenge | 状态 200 不等于目录内容已取得 |

前四项中的 HathiTrust 两次、EndNote 和 NLA 采集发生在 12MH 提交前，作为下一批预检；本批首次保存，未冒充本次重新执行或 12MH 证据。正控制、EndNote、NLA 的精确采集秒未保存，明确只记当日。未重试这些失败路径或处理挑战。

### 裁决与下一门

新增的是 Google 合订本定位，年份、UCD 副本对应和 1951 卷二第九期仍未决。直接 pp.221–233、2011《赵万里文集》p.197、上海《文汇报》1951-08-18 仍未核读。证据票增量 0，历史文本谱系不变，排盘 CLOSED；计数维持 198 / 166 / 10，来源缺陷 17/17 已修复，算法缺陷/重开/候选折叠均为 0。

12MJ 回到已有精确期号的机构馆藏线索，先去重既有奈良文化财研究所及日本馆藏研究，再查是否有实质新增的第一方公开数字化/页级访问机制。若没有新机制，应将匿名原刊恢复分支收束为访问未决；不重复相同挑战、配额或 403 路径。

研究记录及证据分别为 `docs/research/ZIWEI-WENWU1951-GOOGLE-AGGREGATE-YEAR-BOUNDARY-R1.json` 和 `docs/research/evidence/batch-12mi/`。书目观察 JSON 是明确标注的结构化检索摘要，非原站 HTML；访问失败保存事实、字节数和摘要，完整挑战页面不入仓库。
