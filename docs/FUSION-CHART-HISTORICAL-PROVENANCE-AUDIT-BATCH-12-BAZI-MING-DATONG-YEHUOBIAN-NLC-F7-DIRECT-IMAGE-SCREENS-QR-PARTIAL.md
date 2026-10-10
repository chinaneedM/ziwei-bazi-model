# 天问 12QR — 国图 NLC 411999003250 第七数字册旧卷十二开端20页直读

**阶段：12QE仍OPEN；目标〈改造漏刻〉原叶仍UNLOCATED。** 本批为真正逐张打开原页的限定目视筛查，**不是OCR、不是逐字抄录、不是全书缺篇证明**。不增加独立古籍证人，也不修改排盘算法。

## 影像来源与一致性

- 直接下载 GitHub Actions 12QK 原始来源归档：`artifact_id=11674890925`，运行 `38064436808`，第七数字册PDF共110页、来源PDF SHA-256 `540435e7f56bd33f54a5a7dd540b1e3312cb1beae1e18c384d45ab752aaf51b1`（继承12QL的源PDF校验，本轮未重新下载PDF以重算PDF摘要）。
- 对下载归档 `status.json` 中逐项标定的**110张原页JPEG和14张联络表JPEG**复算哈希，114/114匹配，差异0；status.json SHA-256 `fe20b671dee5f97b69933dc27655c3780861954eb32d05a14a945687c526004d`。ZIP本体 SHA-256 `31eb8bf2d27d6a562a676da3eba034e74db173282f5004e5c234547167052f14`。
- 12QP原卷定位器将此数字册PDF p1–47导航至**原卷十二**，p1原卷首可读「萬曆三十七年己酉卷十二」；这不是分类1827重编本的卷十二，也不使数字册成为另一份独立手抄本。

## 本次直接读图的范围

- 分别打开完整原图**第七数字册 p1—p20，共20张**；每一张图与其SHA-256成对写入独立机读证据。观察方式为人工视觉浏览上下文、留意〈改造漏刻〉篇题及此前已证实的关键短语（今宮禁及官府漏箭、北京冬至日出）；未进行每页所有纵行的校勘式转录。
- 原图叙事是万历三十七年开始的编年记录，页内可见官员奏疏、人事、礼部、盗贼、武昌火灾等叙述；本轮**未辨认出直接的目标篇题或可裁决目标短句**。这一表述只意味着20页未产生阳性见证，不能推理该20页每字均已查尽、目标篇段落必定不存在，更不能向后续卷数或整个原本外推。
- 目视检查与源哈希核对严格分开：源图 SHA 可以证明本次面对哪张图，却不能证明看图者已经认全该页文字。

## 队列的前向进展

| 计数 | 12QQ原基线 | 12QR新增后 |
|---|---:|---:|
| 目录来源PDF总页 | 1030 | 1030 |
| 非卷前/终末跋语正文候选 | 1027 | 1027 |
| 已做有边界的目标目视检查的来源页 | 9 | 29 |
| 尚未做目标影像目视检查的正文候选页 | 1019 | **999** |
| 全书逐字校勘 | 否 | 否 |
| 目标篇正证据 | 0 | 0 |

注意：此前九张已查页中第十册 p145 只是结尾跋语，故正文已审读页数是8+20=28；999并非剩余的历史工作全量。**已完成目标目视检查 ≠ 已证明页面缺文**。原始12QQ快照保留不被覆盖；12QR以独立 overlay 重放并限定新增页段。

机读证据：`docs/research/MING-DATONG-YEHUOBIAN-12QR-NLC411999003250-F7-OLD12-TWENTY-DIRECT-IMAGE-SCREENS-R1.json`；脚本：`scripts/yehuobian_nlc_target_review_overlay_12qr.py`；测试：`tests/test_yehuobian_nlc_target_review_overlay_12qr.py`。

执行：

```bash
python scripts/yehuobian_nlc_target_review_overlay_12qr.py
python scripts/yehuobian_nlc_target_review_overlay_12qr.py --queue --fascicle 7 --limit 30
python -m unittest discover -s tests -p 'test_yehuobian_nlc_target_review_overlay_12qr.py' -v
```

**后续**应从f7p21继续，或结合更有针对性的源卷目录线索优先定位；只有直接找到有关标题／段落并核对独立页图，方可开展异文比对。不能因分类1827版卷二十而跳转本抄本原卷二十。保持Matrix222/222、修复45/45、来源647+7=654、MD-G03 OPEN、HPA-DAYUN-CAL-002 MISSING_FROM_PRODUCT、产品R1 CLOSED、算法重开0，需新提交HEAD的CI独立验收。
