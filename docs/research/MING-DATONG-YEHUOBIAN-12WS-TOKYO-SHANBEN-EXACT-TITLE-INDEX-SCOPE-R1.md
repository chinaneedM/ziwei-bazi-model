# 12WS — 东京大学善本影像库来源级确切书名检索范围核定

此次不是重复寻址。12WP 在 exact HEAD Actions [38740016745](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38740016745) 真实采集6个官方页面及两条 CiNii，工件 `11975441446` ZIP SHA-256 `2ce0473b68ad...`；12WQ 在 [38740430429](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38740430429) 取得馆方首页实际连接的 `list.php`，记录索引首页3889笔/195页和确切 POST 表单；12WR 在 [38740731265](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/38740731265) 对该来源明确提供的表单执行唯一一次 `str=野獲編&col=ti` 查询，官方返回 **「共 0 筆，目前 1 / 1 頁」及「無任何資料」**。三工件 ZIP 哈希独立复算与 Github 报告一致，8份HTML原始字节 SHA256 逐件一致；没有OCR、模拟馆藏或下载原书页图。

先前 12WR 原解析字段 `visible_text_contains_exact_target_title=true` 是**网页内嵌JavaScript回显查询词**而非命中，故本轮前向修正为专门解析 `actual_index_result_count_from_visible_count=0` 和 `actual_result_table_explicit_no_rows=true`，补负向测试；不改 12WR 原工件。

此项“0结果”只适用于东文研特设**善本全文影像选择性索引**的这次确切关键词搜索。不能由此推论东大无《野獲編》、馆藏两个物件不在、1827/1869原刊本不存在，亦不能自动对旧2009年A/B访问政策推断现在的具体权限。

CiNii书目仍明确：
- 1827年扶荔山房本，NCID `BC0492354X`，大木文库卷20 item `6403767830`。
- 1869年同治八年重校本，NCID `BB23196128`，仓石文库卷19–20 item `6403148395`。

下一步不再搜索这个已记录零命中的专项索引，而从各馆藏物件本身取得**馆方批准/发行的独立原卷20《改造漏刻》页图**、可核实的藏书印记/牌记、确切印次及源页 SHA256，再重审宮禁/宮漏・官漏/辰初与戌初刻等四处异文。来源登记不新增：647+58=705；Matrix222/222、修复45/45、图谱252节点238边、正式487批；零新增古印本投票，排盘产品 CLOSED，算法重开0。
