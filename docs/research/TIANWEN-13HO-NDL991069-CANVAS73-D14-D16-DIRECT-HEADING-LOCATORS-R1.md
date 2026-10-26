# 天問 13HO｜1909 NDL《高麗史》卷52 canvas73 的十四日／十六日直接日次定位

本批不是再進行泛用目錄搜索，而是**讀取並以 SHA256 核對 13HN 在 GitHub Actions 真正取得的原圖縮覽 ZIP**。受檢 zip artifact: [13HN run 40276733041](https://github.com/chinaneedM/ziwei-bazi-model/actions/runs/40276733041)，artifact ID `12630338053`，ZIP SHA256 `f0776fc9d679ac72c481241edb08010be889413ad15f8b36c8d25427726de69d`。官方 manifest（SHA256 `5ef67e4f…674`）共 395 canvases，卷52從第68幅起、下一卷自第91幅起；13HN 共實取第68至87幅共20張預覽。

## 已源圖定位的唯一新事實

1909年日本國會圖書館本第2冊的來源 IIIF [canvas73 1600px 預覽](https://dl.ndl.go.jp/api/iiif/991069/R0000073/full/1600,/0/default.jpg) 實際 JPEG 為457,808 bytes、**1600 × 1248**、SHA256 `1e6ea3b9a7a6e9177c0837d11c8e37e1a2d9c1b18b5fe1421a7fe83739a58477`。無旋轉、無 OCR，直接檢視右葉下半部日次表：

- 「十四日」原始預覽座標 `xyxy=[1020,590,1098,682]`，直接見到標頭。
- 「十六日」原始預覽座標 `xyxy=[866,589,939,680]`，直接見到標頭。

這是 **2個日次位置的正面物理排版證據**，不是2條可引用數值，也不是2個獨立版本。其他版本所稱「夏表、四分、初度」的同欄/同單位尚未建立，**不能**因為本頁有「十四日」就複製 NIKH 照片中的「四分六六三〇」，亦不能用算術補足 D16 正確祖文。

## 原圖鏈與證據限制

來源 NDL `991069` 是**1909近代刊本**（received printed witness）；其 4 個 Commons PDF 分件只是一個數位物件，不構成四份實物傳承。2026-10-26 13HN 來源預覽不等於完整 5893 像素原圖。未核讀同日完整數列、欄表題、單位或刊本之間的祖承，故 G893 六控、D5〇/五、13EI 撤回狀態及台灣 NCL03130 第52卷舊鈔/光緒補鈔層次均維持原狀。

同時已核實 13HN 精確 HEAD 的 `verify-tianwen-13hb-source-photo-d14` 第一次失敗僅為對韓國官方既有照片的 **25秒來源連線超時**。其本地證據腳本與8個單元測試已成功；只重跑失敗 job 的第二次 attempt 結論 success。完整工作流 203/203 成功，既有圖片不重新斷代、不撤回其來源限定的實際原字讀法，也不以重跑消除先前超時記錄。

### 前瞻門禁

下次僅對經 NDL 原清單發出的 canvas73 做原尺寸直讀，確認14/16日數值所屬 **season/column/units** 後才討論與早期 Waseda/NAJ 的嚴格同欄對照。台灣 NCL03130 書號、物理葉及研究高清許可仍分線取證。

Matrix 222/222，sources 761，graph 252/238，issues 11，chart CLOSED，算法重開 0，候選合併 0。機器證據：`docs/research/TIANWEN-13HO-NDL991069-CANVAS73-D14-D16-DIRECT-HEADING-LOCATORS-R1.json`。
