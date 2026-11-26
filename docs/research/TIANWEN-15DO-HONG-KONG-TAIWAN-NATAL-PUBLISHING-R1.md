# 15DO｜战后香港、台南命理出版与日本馆藏（有界完成）

2026-11-26。启动HEAD `4ef398568f548d89177ae95d961bc8df4a8f1d65`、tree `5a62ce5d3dd8e0b2a67eadc3ef8e7b3c7c91d0f0`。[精确HEAD连续性CI](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/45768440266)成功，job139734974421；62项风险测试及7项R2测试通过，视图4809 UTF-8字节；6/6绑定一致。Actions动态分页出现283/285项去重计数，独立查询failure=0，未声称全通过。全部五项P0保持。原临时检查点见[15DO provisional](TIANWEN-15DO-HONG-KONG-TAIWAN-NATAL-PUBLISHING-CHECKPOINT-R1.md)。

## 一、字面全库查重

精确HEAD CI 2026-11-26T06:29:16.8028642Z 实际输出如下（request和manifest blob复核一致）；根647、233分片640，共234文件1287条，18词均零命中，无截断。字面查重不是语义、版本或物理本的穷尽鉴定。

```json
{"query_id":"15DO-regional-publishing-dedup-r2-20261126","checkpoint_id":"TW-CHECKPOINT-15DO-PROVISIONAL-20261126","request_blob_sha":"76fc041d43f3fc8bfc05a46a8f8d828a7dd34db5","registry_manifest_blob_sha":"b2ce5bfa7ab2e8d01a9ddbe68fbc630494f282d0","status":"PASS","scope":"ALL_REGISTERED_ROOT_AND_SHARDS_LITERAL_ONLY","files":234,"records":1287,"matching_files":0,"per_term_matching_files":{"42347":0,"365178091":0,"BA61461510":0,"90005239760":0,"香港實學書店":0,"香港实学书店":0,"BB26426235":0,"BB26426122":0,"0020180035342":0,"孔日昌":0,"紫微斗數新解":0,"紫微斗数新解":0,"9789576475412":0,"000454968":0,"神峯命理新解":0,"神峰命理新解":0,"9789888317073":0,"Yiy6CgAAQBAJ":0},"hits":[],"truncated":false}
```

## 二、准入三条分层来源

- [CiNii BA61461510](https://ci.nii.ac.jp/ncid/BA61461510) L108–156直接复核：東海樂吾評註、香港實學書店、1955.8、4+273页、19cm，大阪大学外国学图书馆伊地智文库90005239760。与既有1937 NLC目录/序文所系数字替身及2015重刊自述不合并，不断定先后直印或同底本。大阪地方OPAC前次403，未得原刊记。
- [CiNii BB26426235](https://ci.nii.ac.jp/ncid/BB26426235) L108–164直接复核：孔日昌編著、台南西北出版社、1979.7、6+228页、19cm、琉球大学0020180035342；[母书目BB26426122](https://ci.nii.ac.jp/ncid/BB26426122) L108–144无独立年，不作额外独立实物。琉球大学单独OPAC本轮返回403，不绕过。1979是书目出版月，不是已核刊记或首版日期。
- [三民现代商品书目](https://www.sanmin.com.tw/product/index/000454968) L88–136直接复核：ISBN9789576475412、2006-01-01、西北、孔日昌、平装，商品名附命相叢書，简介述星曜十二宫五行生克。仅现代著录与简介，非1979原文、具体排盘规则或实务；与1979《星相叢書：無師自通》关系待核，不购绝版或付费书。

暂不单独准入无版年点字书目、1984旧书摘录、2015重刊比较；不因18词零命中自动把所有候选升级为可靠原始来源。两条CiNii edition节点独立入图，不连直接传承边。香港与台湾出版及日本馆藏为地域分层证据，不证明其实际传播规模、翻译、共同师承或民国同期紫微实践。

## 三、状态

有界完成15DO；TW-OPEN-0032/0033及全部旧风险保持OPEN/原状态。来源1290=647+643/234；图470/375、Matrix222/222、33开放风险含五P0、确定性核心CLOSED。下轮优先独立可定年民国紫微实务、地域传播及双体系历史骨架；原刊记/宏道堂/广告对象/1979与2006关系等仅在新合法免费免账号证据出现时恢复。
