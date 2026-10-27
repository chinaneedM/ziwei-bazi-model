# 天问历史考据 13IV：韩国国家遗产厅 XML 官方原文路线及1482年代作用域

**当前结果不是已获得2114-2官方指定说明全文**。本批先独立发现国家遗产厅第一方开放 API 文档，给出重放端点与不越权的取证门禁；并复核首尔大学奎章阁馆藏引论明确称1482年二月梁诚之上疏促印是**推测**，不可把遗产门户的时代字段直接视为现存某册的确切印次。

* 国家遗产厅官方开放接口说明：https://khs.go.kr/html/HtmlPage.do?mn=NS_04_04_03&pg=%2Fpublicinfo%2Fpbinfo3_0201.jsp；所载详细查询路径 `http://www.khs.go.kr/cha/SearchKindOpenapiDt.do`，必填 `ccbaKdcd` / `ccbaAsno` / `ccbaCtcd`，结果为 XML。采集脚本只用从官方2114-2记录显现的编号`21140200`、`0021140000200`，`ccbaKdcd=12`，`ccbaCtcd=11`；只访问 HTTPS，不自动降级 HTTP，不枚举或绕过权限。
* 官方遗产门户：https://heritage.go.kr/heri/cul/culSelectDetail.do?ccbaAsno=0021140000200&ccbaCpno=1121121140200&pageNo=1_1_1_1&sngl=Y。直接索引有`98권 32책`、`1482년(성종13)`；韩文指定说明长文本尚不能直接访问，之前第三方转载保持次级。
* 首尔大学奎章阁第一方考证文字：https://kyudb.snu.ac.kr/book/view.do?book_cd=GK03269_00&notes=basic。1482年的判断为「추측될 뿐이다」（仅仅是推测），且现存古活字刊印的确年仍未知；与现代遗产目录时期栏目不自动构成物理实物年代矛盾。
* 承接 13IO、13IT、13IU：奎5553第29册⇒卷81–83的映射依然 `RETRACTED_UNBOUND`；奎5554书目页所列奎5553缩微编号仍只属于目录字段，没见到独立实物原图。本批无新原始古页、数值、书叶字形或谱图边。

机器记录：`docs/research/TIANWEN-13IV-KHS-OFFICIAL-DESCRIPTION-XML-1482-SCOPE-R1.json`。可复验 Python 探针：`scripts/probe-tianwen-13iv-khs-heritage-xml.py`；CI 将归档有限的 HTTP/XML 哈希及来源判定，不能以一次流程success冒充第一方原文已经取得。
