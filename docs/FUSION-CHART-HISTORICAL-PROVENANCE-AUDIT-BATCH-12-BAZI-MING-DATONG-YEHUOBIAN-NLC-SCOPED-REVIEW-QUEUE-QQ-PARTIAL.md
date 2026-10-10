# 天问 12QQ — 国图旧二十卷目标篇来源限定人工审读队列

**12QE 仍 OPEN。本批是可重放的人工审读工作清单，不是新增古籍字形证据，也不是全书人工校读完成声明。**

## 继承证据与范围

- NLC411999003250 仍是**一项馆藏**，十册共1030 PDF页，不能因数字册数虚增独立古本。
- 12QP已确认20卷的图像卷首位置：1020页单卷候选、8页左右叶属于不同原卷、2页卷前材料；12QQ继续保留跨卷双叶各自卷号。
- 12QE此前逐张审读第十数字册 p137–145 共九张原图（带图像SHA256），仅局部检索标题与相关段落；p136只为上下文页，**不算九页目标篇查检**。
- f10p145是跋语/抄本结尾，不是已认证卷二十正文；f1p1–2是目录/卷前材料，不纳入正文候选页。
- 因而后续目标篇正文查检候选1030−2−1=1027页；九张原检查页中，正文候选只有p137–144 **8页**，余下正文目标页 **1019页**需要核对原图。并不表示这些1019页从未用于其他项目核读，只是未完成**同一目标篇**的来源范围直接查检。
- 已有20张卷首页仅直接证明卷首标题，不意味着已查遍该页目标篇内容。无独立原图摘要的页会输出null，不得用PDF SHA伪装页图SHA。

## 可重放命令

```bash
python scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py --summary
python scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py --queue --limit 20
python scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py --queue --fascicle 7 --limit 30
python scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py --queue --original-volume 14 --limit 30
python scripts/yehuobian_nlc_scoped_manual_review_queue_12qq.py --fascicle 10 --page 137
python -m unittest discover -s tests -p 'test_yehuobian_nlc_scoped_manual_review_queue_12qq.py' -v
```

队列逐页提供PDF来源SHA256、可用时的页图SHA256、原卷导航候选、双叶左右归属与目标篇查检状态。旧证据限定状态为PRIOR_NINE_PAGE_BOUNDED_CHECK，其他均为TARGET_NOT_MANUALLY_CHECKED，不做整部抄本缺文证明。九页相关字段或源文件SHA发生漂移会触发回归测试失败。

## 实际下一步

按工作清单对原图逐页、逐叶人工检查〈改造漏刻〉篇目，或原文短句（如“今宮禁及官府漏箭”与“北京冬至日出”），记录PDF册页、叶面左右、图像哈希、源版身份和可逐字核读的截图片段。若目标未见，只记录具体直接查看的页范围，绝不能升级为旧二十卷整书无此文。另须独立寻找精准书目绑定1827扶荔山房刻本的该篇原页，避免把1869修刊前言倒作1827同一印次。

本批新增一个脚本、一个回归测试、一个机读摘要和本说明；Matrix维持222/222、修复45/45、来源647+7=654；MD-G03 OPEN、HPA-DAYUN-CAL-002 MISSING_FROM_PRODUCT、产品R1 CLOSED、算法重开0。与12QP相同，**新HEAD提交后的CI必须独立验收。**
