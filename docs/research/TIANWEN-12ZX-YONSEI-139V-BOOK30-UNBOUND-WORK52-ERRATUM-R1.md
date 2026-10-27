# 天问 12ZX｜延世本第30册与卷52映射中的两处前向勘误

对已推送的 [12ZW机器证据](./TIANWEN-12ZW-YONSEI-CHOI-SEAL-BOOK30-MANUSCRIPT-PRINT-GRADE-R1.json) 做证据作用域复核后，发现两项字段表达越界。**保留12ZW原件与对应哈希，不回写历史记录**；本文件代表从现在起有效的修正裁决。

1. `physical.printed_work_volume_total=139` 字段名错误。韩国遗产目录所说 **139卷** 是整件馆藏的作品编目总卷数。第30册内的作品卷122、123明确属于后补抄，所以不能将“139卷”表达为“139卷全部以木刻原叶印出”。修正为 `catalog_work_volume_total=139`，而 `original_woodblock_printed_work_volume_total=null`，其余未见原叶的载体类型仍待证。
2. `explicit_book_level_composite.work52_same_book_30=false` 过度否定。目录虽能绑定第30实体册的卷122、123，**尚无完整33册分卷表**，不能从局部事实证明第52卷绝不可能同时在第30册。修正为 `work52_in_physical_book30=null`、`work52_physical_book_number=null`。这不是声称两者确实同册，而是禁止“没有证据”被当作“证据证明没有”。

该勘误不会抹除12ZW实质核实的“崔漢綺藏”目录级藏印、“第30册卷122/123后补抄”的资料事实或“后印时间与版框尺寸推测应分别保存”的判断。

**后续准入标准**：延世馆方完整分册目录＋卷52原叶实物号＋原图URL/页哈希＋D16/D18目标数字直接目视，方可将未知字段改为真/假或加入跨版本对勘。网页检索目录不能充当原书页。G893单源5/6、跨本0/6、11项遗漏OPEN、717条注册来源、0算法重开与排盘R1 CLOSED不变。
