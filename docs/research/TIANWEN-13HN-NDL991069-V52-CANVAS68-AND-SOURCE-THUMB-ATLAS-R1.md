# 天問 13HN — NDL991069 原生 IIIF 第52卷 canvas68 已核實

13HM 的 [GitHub Actions 原生 IIIF 探針](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40275833145) 在指定 HEAD 直接讀取 1909 年《高麗史》第2冊的官方 manifest，HTTP 200，原始 SHA-256 為 5ef67e4f84917ffd1eafee2b2da1d22f1aeb68f8d7f2ac441b7d398be19bf674，含 395 個 canvas。館方目錄項「第六　高麗史五十二」原生綁定 1-based canvas68（ https://dl.ndl.go.jp/api/iiif/991069/canvas/68 ）。這是第52卷的**目錄起點**，不是某日的數值原字。

本批新增可在 GitHub Actions 自動運行的 source-scoped image atlas：先從同一館方 IIIF manifest 查找卷52的起點及下一卷目錄邊界，再僅透過 manifest 自身提供的 image service 生成標準 IIIF 1600px 縮覽，不做任意 URL 猜測、OCR 或帳號存取。最多取20張圖，逐頁保存 URL、HTTP狀態、字節數和 SHA-256；失敗仍保留可稽的邊界報告。

縮覽只用於原葉定位；既有 NIKH photo4 夏表14日「四分六六三〇」仍只見證該 NIKH 照片；台灣 NCL03130 舊鈔及光緒補鈔層次不明、D14全數及末字不明；G893六數、D5〇/五、古單位與四分/初度同一性仍不決，13EI 維持撤回。NDL1909印本屬近代 received witness，不能自動增加古籍物理見證票。

本批保存 222/222 歷史矩陣、761登記史料、252節點/238邊、11風險與排盤 CLOSED，算法重開0、候選坍縮0。下一步讀取 13HN 的實際畫布 artifact，選定原圖及原字位置後再做高解析像素校勘。