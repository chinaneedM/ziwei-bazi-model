# 天问 13CR｜NCL03130《高丽史》24分件目录与书首朱记影像采集门禁

本次重新浏览 Wikimedia Commons 的《高麗史》媒体分类及其「國家圖書館」备份索引，见到命名为 **NCL-03130 01–24 高麗史.pdf** 的连续 **24 个公开PDF分件**。分类列表标注第01分件 **204页**，第24分件 **73页**；每个分件页数已抄录至同批JSON。Commons转录的 NCL 书目则写 **40冊 / 208 03130**。24个数字分件 ≠ 40册实体，不得以二者的数量差异推断有16册失踪，也不能把「08」推为卷五十二。

**当前新增的是真实、具体的公开影像入口定位，不是读到原始朱笔清单。** 按13CQ所记吴重熹题记转录「缺卷朱記于首」，第01分件的书首是优先采集与人工视觉核读目标；书首是否确实在该PDF、出现于第几页均未判明。只有拿到页图、PDF SHA-256、页码以及源数字对象的页图哈希，才能将“朱记”升级为直接图像事实；还必须找到 208/03130 馆方原生目录记录以核对 Commons 镜像是否真的绑定那一实物。

## 本轮新增工程交付

- `docs/research/TIANWEN-13CR-NCL03130-COMMONS-24PART-FRONT-INTAKE-R1.json`：24分件/页数目录和物理册、扫描分件、工作卷数之间的证据防火墙。
- `scripts/acquire-ncl03130-front-13cr.py`：**仅从公开Commons合法重定向**取第01分件，下载须受字节上限和PDF魔数验证；使用PyMuPDF输出不含OCR的全页微缩联络图、前12页预览、带图像SHA-256的机器清单。失败记录访问边界，不能报告“原书不存在”。
- `.github/workflows/acquire-ncl03130-front-13cr.yml`：隔离的研究原图获取工作流（不与核心排盘CI结果混淆），归档供后续**人工**复核；此处提交不代表已成功取得或阅览PDF。

## 尚未越过的证据门槛

**FRONT**：第01分件中真实原书书首红字所在页，待图像检索确认；**JUAN52**：缺卷清单是否明载卷五十二，仍为「缺／不缺／不可读」三分支；**STRATA**：卷五十二旧钞／1905年丁氏补钞实叶归属未定；**GLYPHS**：未核读台湾本D16的物理原字；**LINEAGE**：不能新增第三独立古本投票。

原Waseda/NAJ印本 D16 日差 `5.1362` 不受影响；`5.2362` 是数值推导候选、非原字。本次对 Matrix 222/222、外源754、谱系252节点/238边、11项风险、排盘产品CLOSED和算法0重开均无修改。

资料入口：[Commons类别](https://commons.wikimedia.org/wiki/Category:%E9%AB%98%E9%BA%97%E5%8F%B2)、[NCL备份总目录](https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/Rare_Books_%26_Special_Collections,_National_Central_Library/%E5%8F%A4%E7%B1%8D%E8%88%87%E7%89%B9%E8%97%8F1)、[01分件](https://commons.wikimedia.org/wiki/File:NCL-03130_01_%E9%AB%98%E9%BA%97%E5%8F%B2.pdf)。
