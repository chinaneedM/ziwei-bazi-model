# Fusion Chart Historical Provenance Audit R1 — Batch 12KM

## NCPSsd /Literature/articlelist Base64 查询生成语法闭合

Status: **20 SOURCE-EMITTED HOT LINKS / 20 SEARCH ROUNDTRIPS / 20 SEARCHNAME ROUNDTRIPS / 20 FIXED-PARAM MATCHES / QUERY GRAMMAR CLOSED / RESULT ROUTE NOT YET EXECUTED / NO TARGET QUERY / ZERO PRODUCT IMPACT**

12KL 首次从 NCPSsd 首页直接恢复 /Literature/articlelist 路由及 search/searchname 参数名。12KM 不访问该路由，只对首页直接发出的 20 条热词链接做解码与逐字节 round-trip。

全部 20 条都满足同一模板。对任意首页热词 T：

    search = (IKTE="T" OR IKPYTE="T"  OR IKST="T" OR IKET="T" OR IKSE="T")
    searchname = 题名/关键词="T"

两个字符串均按 UTF-8 后做标准 Base64；固定参数为 sType=0、nav=0、nav=0、showBack=true。

校验结果：20 条 search 全部匹配，20 条 searchname 全部匹配，20 条固定参数全部匹配；全部热词均可恢复，整体 all_roundtrip_equal=true。

因此查询生成语法现在是由 20 个第一方样本共同约束并可逐字节复现的合同，不再属于 endpoint/参数猜测。

本批仍没有请求 /Literature/articlelist。下一门 12KN 先重放首页原生“红楼梦”热词链接作为正控，验证 result route 在当前公网面真正可执行；正控通过后才生成赵万里目标查询。

控制证据：workflow .github/workflows/probe-batch-12km-ncpssd-articlelist-base64-roundtrip.yml；exact head a4d831f29204996800f4aae2d4168fd0d6073b4c；run/job/artifact 36862550453 / 110370033920 / 11162660752；artifact digest sha256:b22f441c753d4bb628c0ab9787c83bc1ca7e74ad828bf4044efdbd6f7f060735。

Matrix 仍为 198 / 166 / 10；provenance defects 17/17；algorithm defects / reopen / collapse 均为 0。Transmission Graph 不变。

Research record: docs/research/ZIWEI-NCPSSD-ARTICLELIST-BASE64-GRAMMAR-R1.json.
