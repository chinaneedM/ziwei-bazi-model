# 天问13AU｜国立公文书馆《高麗史》物理第52册原图三点采集及正文定位

来自精确远端 HEAD `3f6818c60da918808f4efc8af010b1ab30efa8bb` 的 GitHub Actions [13AS运行](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/39375696388) 已成功产生 artifact `12242983635`，原始 ZIP 整体校验值 `9d563f794ae4e7334e7ff549f779fab8977733edee3b40b5cf1e54f17013af18`。本轮直接获取归档并重新 SHA-256 核对第1、2、32幅，结果和原始 `result.json` 一致：页1 `a3120f78...` 994451 B、页2 `b31ad31a...` 988759 B、页32 `13f3eeb5...` 950036 B。原始 manifest 是官方 [IIIF v2清单](https://www.digital.archives.go.jp/api/iiif/4898854/manifest.json)，共32幅。

**无 OCR 的直接视觉复核：** 第1幅为日本公文书馆馆签及封面，上面可辨第52物理册标签；第2幅为封里空白透字；第32幅为封底。三页都不是目标《高麗史》卷52《授時曆》太阳盈缩表，故不能用作D16原字的正反裁决。当前IIIF `full/max/0/native.jpg` 实际提供 3000×2215 JPEG，而Viewer源声明 6500×4800；**不得把JPEG输出说成已取得6500×4800原生JP2**。

本批在独立脚本 `scripts/acquire-najda-goryeosa-13au.py` 和 push-triggered Action 中限制后续样本为manifest中原样列出的第3、第16、第31幅（0-based [2,15,30]），最多三幅、单幅12MB；不猜测URL、不OCR、不把同一物理册图像计为三份独立见证。该样本**提交时尚未执行**，不能凭脚本存在升级target页状态。待精确HEAD run及artifact重新核验后，方可继续卷名/表头/目标栏定位。

证据裁决仍为《高麗史》**物理第52册已绑定官方原图**，不是“内容卷五十二、D16数值已经验证”。TW-OPEN-0005继续OPEN，11项研究缺口保持，来源总数754，Matrix222/222，谱系图252节点238边，无新数值独立投票、无算法重开。
