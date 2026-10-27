# 天问 12SM — 东京大学善本原页影像的公开范围与获取门槛

**12QE 仍 OPEN：这一检查点新增的是官方影像服务使用条件，不是《野獲編》卷二十〈改造漏刻〉的原叶。**

## 第一方站点和历史政策来源

东京大学东洋文化研究所[数据库目录](https://www.ioc.u-tokyo.ac.jp/database/index.html)直接指向[善本全文影像资料库](https://shanben.ioc.u-tokyo.ac.jp/)。其[官方简介](https://shanben.ioc.u-tokyo.ac.jp/intro.html)明确记载 **截至2009年3月** 的4630项数字化目录（A类4019可公开浏览全部影像，B类611仅公开部分、全文需规定机构范围），以及个人研究、不得任意大量下载和再发布的边界。[官方使用说明](https://shanben.ioc.u-tokyo.ac.jp/help.html)要求**在某册的实际馆藏目录详细记录发现「全文」/「連結文本」**，才可继续定位对应全文页图。

上述是**2005/2009年代官方公开说明**，不是当前2026年数据库项目级实时统计。不能将该界面上存在善本库或馆藏联机目录，推断成这两册书已经拍摄、A类全文公开或可任意再分发。

## 两个准确实体的待验条件

- 1827目录本东京大木文库《野獲編》卷20：CiNii `BC0492354X`，实物 `6403767830`；本库是否包含该物、是否公开目标页、A/B身份均 **UNVERIFIED**。
- 1869目录本东京仓石文库卷19–20：CiNii `BB23196128`，实物 `6403148395`；同样全部 **UNVERIFIED**。
- 只有从上述实体的馆目进入匹配全文入口、读取原始源页、对照页码／版心／目录版本身份后，才可能取得原叶字形。不可通过估猜未公开ID或绕过访问权限。

## 面向下一轮的机械门禁

本批引入 `docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-TARGET-LEAF-ATTESTATION-QUEUE-R1.json` 和 `scripts/verify-yehuobian-physical-leaf-attestation-r1.py`：
- 两件独立馆藏各占1条目标页候选队列；初始**原页0、独立字形票0**。
- 队列增加字形必须明确同一物件身份、HTTPS源页、原页号、原文件和单页SHA-256、四个词字／数字异文位置，以及人工/版式对照记录。
- 机械校验只是**结构与声明完备性检查**，不能替代人工验字、实际影像文件重算哈希、藏本认证或著录权限确认。
- 缺一项者禁止源字入账，不可从“检索不出”“只看少量页”推断整卷/整书缺文。

不新增目录物理见证、版次亲缘边或算法修复。来源表旧根647 + 扩展9 = **656**，其中新1项**机构访问政策来源**非新史料刻本；传承谱248节点／235边原封不动；Matrix222/222、元数据修复45/45、排盘R1 CLOSED、12QE/MD-G03 OPEN。**12SM 是补充研究检查点，不加入正式批次**。

机器证据：`docs/research/MING-DATONG-YEHUOBIAN-12SM-TOKYO-SHANBEN-ACCESS-BOUNDARY-R1.json`，来源分片：`docs/research/MING-DATONG-YEHUOBIAN-12SM-SHANBEN-SOURCE-SHARD-R1.json`。
