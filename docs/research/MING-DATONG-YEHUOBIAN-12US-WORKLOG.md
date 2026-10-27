# 12US — CText 两个 HTTP200 同正文的访问外壳纠错

12UR [GitHub Actions](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38260357120) 成功执行只查询两个已发布 URL 的只读探针，留存 artifact 11752122669（ZIP SHA256 d75805d4c10974317214f5fb4f228adf716fcabb6672d068013984772627a1e5）。

原始日志显示：书目 `res=1946940` 与文章 `chapter=418967` 均 HTTP200 `text/html`，但**完整响应正文 SHA256 都是 `4f323319db2cfd81d5d8106ab0f3cdbf21aaf8a17f2d187347961c569bbc1d73`，源发疑似扫描链接数0**。故旧探针 `PUBLIC_HTML_METADATA_ONLY` 不应理解成两页原始内容均已独立访问。具体原因（反爬页、统一模板、其他中间层）目前**不可断言**。

12US 在原脚本中新增独立跨 URL 内容指纹判定：不同公开目标请求返回字节完全一致的 HTML 时，结果标为 `AMBIGUOUS_IDENTICAL_HTML_SHELL`，并明确 **source_item_identity_proven=false**；即使两个页面内容不同，也不能单凭 HTTP200 宣称原叶得到认证。新增两条回归测试，保留上轮 12UR 的原始报告不覆盖。新 HEAD 的专项 workflow 会再生成一个独立结果 artifact。

未下载任何古籍原叶，未取得〈改造漏刻〉原文，新增来源数0。状态为 Matrix222/222，修复45/45，注册647+40=687，谱图250/237，正式批487，12QE/MD-G03 OPEN，产品 CLOSED、算法重开0。
