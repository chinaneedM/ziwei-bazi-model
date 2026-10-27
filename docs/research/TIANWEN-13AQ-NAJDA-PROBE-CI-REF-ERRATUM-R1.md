# 天问 13AQ｜13AP 严格来源路径勘误与 NAJ 第一方目录访问实测

## 修复已发现的精确 HEAD CI 失败

13AP 将脚本、测试和 workflow（共3个工程文件）加入遗漏台账 `source_refs`；当时 `verify-research-omission-risk-ledger-r1.py` 将该字段约束为 **`docs/`** 开头，因而两项13AP精确HEAD校验失败。不能删去旧登记、改写旧提交或一概放宽来源路径。

本批引入**仅 TW-OPEN-0005 且仅3条已知稳定路径**的辅助执行文件例外，不允许其他 issue 注入任何非文献路径，不允许 `..` 逃逸。代码辅助文件仍不具备历史原页字形权威；证据根本文档继续落 `docs/research/`。

## 已运行的定向探测结果

13AP 的 [最新单独 Actions 探测](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39373628730) 在 GitHub runner 成功获取 `282-0006` 馆方第一方检索列表 HTML，HTTP200、**703538字节**，SHA256 **`76f8cc07b783b65844470770a3a786dee0688510e4cdd6ff85b8f9938be7ab4e`**，归档证据 artifact `najda-goryeosa-13ap-source-index`。

严格原样解析**没有找到**标题为「高麗史５２」且通过HTML `<a href="/item/...">` 直接发出的单件地址。这仅表示本次解析策略未找到可跟随链接；不意味着第52册不存在、馆方没有影像、数字化未完成，也不能据此把“未知”变成阴性证明。原始 HTML 保存在同运行 artifact，尚需另行检查页面是否使用 JS 链接或其他源发出关系，不得猜测数值ID。

`282-0006` 的实体册次→正文卷次依旧未知。第16日原字未获得，所有11项研究问题仍开放，Matrix222/222、注册754、传承图252/238、确定性排盘 R1 CLOSED。

机器记录：`docs/research/TIANWEN-13AQ-NAJDA-PROBE-CI-REF-ERRATUM-R1.json`。
