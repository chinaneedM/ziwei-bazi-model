# 12VX — 哥伦比亚 MARCXML 第111片精确 HEAD 实跑回执

## 真实运行结果
依据 GitHub Actions `verify-yehuobian-12vw-columbia-marc-shard-exact-head` 的 job `115914301391` 原始日志（run `38582081722`，HEAD `c7f59899426144e64fbd779e79e9638491980714`）：

- 下载的官方公开压缩分片：`extract-111.xml.gz`
- 压缩文件字节数：**17,907,901**
- 下载执行环境报告 SHA-256：`655b2dd9e02631b44e4c3c9319a11bd1f9d3d4492b3435575afd3e3102d8b9c5`
- MARC record：**21,553**；限定书名字段命中：**0**
- 工作流 probe 步骤成功，并上传结果归档 artifact **11904401169**（ZIP 元数据597 bytes）。

注意本批**读取了 Actions 原始日志和 artifact 元数据，并未重新取得源 GZIP 或归档 ZIP 原始字节**，不能宣称本批完成二次独立 SHA 校验。源摘要是原执行进程的报告值；原始日志提供了可重复访问的 run/job 指针。

## 负证据的边界
一片无匹配 ≠ 111片无书，也不推翻12VU学术引文中的 Columbia University Libraries 提示；一条 MARC 命中也不能证明源刻1827版印次或卷20原字。
本批不给 Columbia 建立独立古籍证人，不插入九号馆藏原叶队列，不触碰前八项东京/京都等具体馆藏的来源顺序。

## 项目状态
根647 + extension54 =701不变；Matrix222/222，修复45/45，图谱252/238，正式487/latest12QD。新古本目标页0、原字票0、算法重开0，R1产品CLOSED。下一步优先获取古本实体卷20〈改造漏刻〉页面而非盲目跑完110片以制造负性结论。
