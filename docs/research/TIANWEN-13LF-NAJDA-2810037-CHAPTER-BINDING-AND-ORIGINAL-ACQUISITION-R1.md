# 天问 13LF｜日本国档 281-0037《明史》独立馆藏卷册绑定与原扫描获取

## 已取得的证据级别

日本国立公文书馆[馆藏 281-0037](https://www.digital.archives.go.jp/file/3602570) 是旧藏 **昌平坂学問所**、编目为清乾隆刊本的 **120 册**《明史》；上一批直接审读的 [281-0038](https://www.digital.archives.go.jp/file/en/3610285) 为旧藏林家、**112 册**的另一馆藏记录。两份馆藏记录不能直接认作两种版刻。Commons 的 [NAJDA/12 文件清单](https://commons.wikimedia.org/wiki/Commons:Library_back_up_project/file_list/NAJDA/12) 另列 `NAJDA-281-0037 明史1.pdf` 至 `明史120.pdf`。这验证了可访问的**逐册文件索引路线**，不是卷三十五的具体原页证明。

## 明确未完成

- 281-0037 的 **卷三十五在第几册仍未由原页标题绑定**。采样第 10–14 册是待检查范围，不宣称任何一本已包含该卷。
- 未从本馆藏读取十三朔数字、遲疾歷操作句、版心或印次；既不能增加独立传本投票，也不能改写已直接读出的 281-0038/哈佛 **238977.09** 和 CADAL《四库》**288977.09** 的异文格局。
- 清乾隆目录范围不能自动提升为实物 **1739** 年印次确认；PDF 上传年份不是实物年代。

## 机器获取链路

新增脚本 `scripts/probe-tianwen-13lf-naaj-2810037-original.py`、Actions `probe-tianwen-13lf-naaj-2810037-original.yml`：对候选册依次调用 Commons 官方 imageinfo，并以下载文件的 SHA1、字节数、SHA256 和 PDF 页数留存检验，再生成不经 OCR 的原生图片抽样与全册接触表，原文件只保存在 7 日有效 Actions artifact。没有正面人工校勘之前，所有数值与谱系结论严格记为 PENDING。

## 账本与产品边界

此批是 P0 `TW-OPEN-0005` 的新增待查对象路线：Matrix **222/222**；来源注册 **647+118=765**；传承谱 **252 节点/238 边**；**11** 项问题仍未关闭；G893 六项历史数值胜出仍 **0**；确定性排盘 **CLOSED**，算法重开 **0**。

机器记录：`docs/research/TIANWEN-13LF-NAJDA-2810037-CHAPTER-BINDING-AND-ORIGINAL-ACQUISITION-R1.json`。
