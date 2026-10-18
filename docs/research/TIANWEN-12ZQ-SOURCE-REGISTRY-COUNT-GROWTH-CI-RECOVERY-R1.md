# 天问12ZQ｜历史源数快照与实时来源登记混淆：CI 修复记录

## 事故源及直接日志

在 `261fe45f69d2cab2d3b2b1bd72d2781f8a21f813` 上，12ZP 新增的四条官方《朝鲜王朝实录》数字转录来源由 GitHub 的完整性校验合法纳入分片；来源联集由**647根 +59扩展 =706**增长为**647根 +63扩展 =710**，根库未变。由于此前将历史快照数量 706 误写为**实时当前数量**，四条工作流出现固定计数假失败：

- [主 CI 39119468197](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39119468197)：12XW 关卡 `Matrix/source registry scope changed`；
- [东京 12XC 39119464820](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39119464820)：`current union`；
- [东京 12XD 39119465425](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39119465425)：`registry state`；
- [东京 12XF 39119467760](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39119467760)：`registry counts`。

四个失败日志中项目连续性与来源分片完整性检测均先行 PASS，后续旧关卡仅因当前库合法增长而失败；**这不构成东京书籍访问失败、史料失真或算法缺陷**。

## 修复的九个校验脚本

- `verify-g893-cross-ledger-live-stage-12xw.py`、`verify-g893-l124-live-stage-r1.py`、`verify-g893-l101-direct-field-12xz.py`；
- `verify-yehuobian-12wz-tokyo-seven-firstparty-catalog.py`、`verify-yehuobian-original-folio-intake-12xd.py`、`verify-yehuobian-original-folio-intake-12xg.py`；
- `verify-yehuobian-tokyo-reproduction-dossier-12xc.py`、`verify-yehuobian-utokyo-digital-access-12xf.py`；
- `verify-goryeosa-royal-annals-publication-12zp.py`（对下次新来源增长也具前向兼容性）。

**新门禁合同：**

1. 历史研究记录中 `647/59/706` 的记录永远保持原值且受检。
2. 当前来源数量不再伪装成旧快照值，而必须与当前 `PROJECT-CURRENT-STATE-R1.json` 及哈希校验的来源注册分片 manifest 一致，且不得低于历史数量。
3. 没有 manifest 参数的历史专项门禁仅检查不低于旧基线；实际的当前计数真实性由完整 `verify-historical-source-registry-extensions-r1.py`、连续性状态门禁验证。
4. 文本原字、库号、目标页、手工图片 SHA、目录身份、零独立原件投票和非预测边界均未放宽。
5. 本批只修复 CI 逻辑，不改写任何历史证据文件，不新增来源或传承边。

现存历史审计矩阵仍为**222/222**、元数据修复**45/45**、开放研究风险**11项**；G893原本直接控数仍**5/6**、跨独立原件裁决**0/6**、传承谱**252节点238边**、产品R1继续**CLOSED**。新 HEAD 的 Actions 执行结果应单独检查，不能由提交成功推定全部 PASS。
