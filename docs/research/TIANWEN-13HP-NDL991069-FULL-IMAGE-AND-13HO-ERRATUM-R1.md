# 13HP｜NDL991069 卷52 canvas73 原图与 13HO 坐标前向勘误

通过 [GitHub Actions 40312727158](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40312727158) 从国立国会图书馆来源 IIIF `https://dl.ndl.go.jp/api/iiif/991069/R0000073/full/full/0/default.jpg` 实取 1909 年刊《高麗史》卷52 canvas73 JPEG：**3773×2943**、**1,895,234 bytes**、SHA256 `c5fc1b3aeff9aedb84bc36fff02fad2a865e7c86c9fd1e624f7f18a548f945bb`。产物 artifact `12645481673`，ZIP SHA256 `5fa5a8d197238794d16ed5c3e37e33fe5d74b4838d4d51da27195548c42935e9`，内含整页、旧定位对照裁切、右下表区及 JSON 报告。来源 manifest SHA256 `5ef67e4f84917ffd1eafee2b2da1d22f1aeb68f8d7f2ac441b7d398be19bf674`。馆方 2018 年 [IIIF 官方接口规格](https://dl.ndl.go.jp/static/files/IIIF_interface_En.pdf) 声明最长边 5000px 上限，但本对象 manifest 标注及 full API 实际返回均是 3773px；不得宣称达到未知扫描母件原始分辨率。

## 13HO 勘误：旧题头坐标失效
13HO 只在 1600×1248 预览上保存了十四日 `[1020,590,1098,682]` 和十六日 `[866,589,939,680]`。本轮把它们等比例投射到同源 3773×2943 全幅，**两个旧框都未完整包含被标记的相应日期标题**。旧 13HO JSON 与 MD 原封存档，不静默修订；本批标记 `FORWARD_ONLY_RETRACTION_OF_BAD_DATE_TO_BBOX_ASSOCIATION`，仅撤回错误坐标的证明力，不宣称日期不存在。

重新从右页下半部亲读，逐列日次从右至左为十二、十三、十四、十五、十六、十七日；原幅像素位置：
- 十四日完整题头 `[2805,1595,2898,1760]`，PNG crop SHA256 `cd90bc5f34325c3745ed50cf111a6f97e3bde69444480fc79caf6f2c14a373cb`。
- 十六日完整题头 `[2399,1595,2492,1760]`，PNG crop SHA256 `f71584c8b289f6c54565a34ffb6a8c3d4bb9e7f82ef62fd7a9cfb69f7c5f91fd`。

可从 artifact 内 SHA 固定的整页 JPEG 使用 Pillow 原像素裁切并输出 PNG 重放上述哈希。无 OCR。同日本页第一组紧接的印刷字面分别可读作十四日「五分一九九〇」、十六日「五分一三六二」，**仅是 1909 近代收本的本页字面，季节、技术列、物理祖本、古代单位尚未校明**。

韩国 NIKH 早本夏表十四日「四分六六三〇」属于其独立原照片，不能移植至本1909刊本，更不能外推至台湾 NCL03130 的旧钞／光绪补钞混合原件；后者 D14 全数及尾字继续 NULL。G893 六控、D5〇／五继续 OPEN，13EI 继续 RETRACTED。无新古本见证、无传承边、无排盘算法修改。Matrix222/222、来源761、图谱252/238、遗漏问题11、产品CLOSED、算法重开0、候选合并0不变。
