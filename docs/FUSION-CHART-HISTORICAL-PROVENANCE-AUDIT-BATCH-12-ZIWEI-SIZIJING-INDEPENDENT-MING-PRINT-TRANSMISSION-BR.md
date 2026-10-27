# Fusion Chart Historical Provenance Audit R1 — Batch 12BR

## 《四字經》獨立明刊傳本線：臺灣國圖單行本、1597《夷門廣牘》本與《永樂大典》卷18764文本橋

Status: **INDEPENDENT MING-PRINT SIZIJING TRANSMISSION CONFIRMED / TAIWAN NCL HOLDS MING-WANLI JINLING JINGSHAN-SHULIN ONE-JUAN SIZIJING WITH 21-PAGE PUBLIC SCAN / NLC YIMEN-GUANGDU 1597 PHYSICAL-SCAN LINE CONTAINS SIZIJING / CTEXT AUTOMATIC OCR OF YIMEN BASE PRESERVES THE SAME LONG STRUCTURAL SEQUENCE AS YONGLE-DADIAN 四字經序 / LATER UNIT LABEL 唐明皇論 VERSUS YONGLE LABEL 四字經序 PRESERVED / OCR VARIANTS 古人~古經, 雨落~雨露, 亥子丑寅~子丑寅亥 NOT GLYPH-ADJUDICATED / TANG 德行禪師 RESPONSIBILITY STATEMENT NOT TANG-DATE PROOF / TAIWAN SINGLE-ITEM VS NLC YIMEN EDITION IDENTITY NOT PROVED / NO DIRECT NO-OCR TARGET-LEAF COLLATION / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BQ established that 《永樂大典》卷18764 preserves a pre-1581 textual bridge for inclement birth-time uncertainty under `前定數 → 諸家序 → 四字經序`, while keeping the extant physical-recension layer (Jiajing duplicate) separate from the Yongle compilation layer.

Batch 12BR asks the next philological question: does a separately transmitted work titled 《四字經》 survive outside 《永樂大典》, and does its opening textual unit preserve the same extended sequence rather than merely one proverbial phrase?

The answer is yes at the transmission/text-family level. Exact glyph adjudication remains open.

## 2. Taiwan National Central Library single-title witness

Taiwan's National Central Library catalog records:

- title: `四字經`
- responsibility: `(唐)德行禪師撰`
- edition: `明萬曆間(1573-1620)金陵荊山書林刊本`
- extent: `一卷`
- book/registration number: `15275-0058`
- class: `子部-術數類-命相之屬`

The public Commons derivative explicitly identifies the NCL source and exposes a 21-page scan of this object.

Evidence URLs: `https://catalog.digitalarchives.tw/item/00/08/6f/c0.html` and `https://commons.wikimedia.org/wiki/File:NCL-15275-0058_%E5%9B%9B%E5%AD%97%E7%B6%93.pdf`.

The responsibility statement `(唐)德行禪師撰` is a catalog/title-page tradition. Batch 12BR does **not** convert it into an authenticated Tang composition date.

## 3. 1597 《夷門廣牘》 physical-print line

The National Library of China sourced Commons record for `《夷門廣牘一百○六種》第10冊` gives publication as `荊山書林明萬曆25年[1597]` and its internal content listing includes `四字經` between `相法十六篇` and `土牛經`.

Wikisource independently indexes `明刻本夷門廣牘26.djvu` as a 108-page scan, year 1597, containing `相法十六篇 / 四字經 / 土牛經 / 天文占驗`.

Evidence URLs: `https://commons.wikimedia.org/wiki/File:NLC892-411999013864-69586_%E5%A4%B7%E9%96%80%E5%BB%A3%E7%89%98%E4%B8%80%E7%99%BE%E2%97%8B%E5%85%AD%E7%A8%AE_%E7%AC%AC10%E5%86%8A.pdf` and `https://zh.wikisource.org/wiki/Index:%E6%98%8E%E5%88%BB%E6%9C%AC%E5%A4%B7%E9%96%80%E5%BB%A3%E7%89%9826.djvu`.

This proves a securely dated late-Ming printed transmission of a work titled 《四字經》. It does not by itself prove that the Taiwan NCL single-title object and the NLC 《夷門廣牘》 object are the same impression, same physical copy, or even a separable/disbound instance of one edition.

## 4. CText 《夷門廣牘》-base OCR and long-sequence correspondence

CText explicitly labels the electronic base as `《夷門廣牘》本《相法十六篇 四字經 土牛經 天文占驗》` and marks the relevant text as automatically transcribed with OCR.

Its opening unit is titled `唐明皇論`. Although heavily corrupted at individual glyph level, the OCR preserves the following distinctive sequence in the same order:

```text
人生天地間 / 造化皆由命數
八字超群 / 五行衰絕
草木—四季—榮枯
日月—晝夜—盈虧
雪/風/雲/雨 + 禽獸舟航
同時共數 + 富貴壽夭
亥子丑寅四時難分
古人云 + 天陰雨落難定 + 便是神仙也有差
旦夕時刻 + 月運長短
```

Compare Batch 12BQ's 《永樂大典》 `四字經序`, which preserves the same extended architecture, including `同時共數`, the four difficult hours, and `古經云天陰雨露時難定便是神仙也有差`.

Evidence URL: `https://ctext.org/wiki.pl?chapter=871842&if=en`.

The length and ordering of shared anchors are sufficient to classify the texts as the same **Sizijing transmission/text family at structural level**, not merely independent reuse of the short inclement-weather proverb.

## 5. Title-layer and variant firewall

The two witnesses label the unit differently:

```text
Yongle-Dadian compilation witness: 四字經序
Yimen-Guangdu OCR witness:         唐明皇論
```

Batch 12BR preserves this as a recension/title-layer difference. It does not silently normalize the headings.

Likewise these apparent variants remain **unadjudicated** because the Yimen text is currently being read through automatic OCR rather than direct target-leaf collation:

```text
永樂大典 transcription: 古經云 / 天陰雨露時難定 / 子丑寅亥
夷門廣牘 OCR:          古人云 / 天陰雨落難定 / 亥子丑寅
```

No stemmatic conclusion may rely on those exact glyph differences until the corresponding Ming-print page is directly read.

## 6. Downstream facsimile continuity

NDL/CiNii bibliographic records for modern `四字經 . 李虚中命書 . 珞琭子三命消息賦註` explicitly note that `四字經` was reproduced from the `夷門廣牘` edition (`據夷門廣牘本影印`). This is useful downstream transmission control only; it is not another independent early witness.

Evidence URL: `https://ndlsearch.ndl.go.jp/books/R100000136-I1970023484950143408`.

## 7. Effect on HPA-ZDATE-006

- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`
- independently surviving Ming-print Sizijing transmission confirmed: `true`
- securely dated Yimen-Guangdu print witness: `1597`
- independent physical holding routes located: `2` (Taiwan NCL single-title object; NLC Yimen-Guangdu object)
- independent edition count increment: `0` pending edition-identity adjudication
- direct Ming-print target-page glyph witness: `0`
- Hai-branch glyph/mechanical vote: `0`
- Fullbook cloudy/rain current-time acquisition mechanism closed: `false`
- runtime winner: `false`
- candidate collapse: `false`
- algorithm reopen: `false`

Counts remain `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 8. Next gate

The next admissible work is now much narrower:

1. directly collate the opening `唐明皇論` leaf in either the Taiwan NCL Ming-Wanli scan or the 1597 NLC/Yimen scan;
2. adjudicate `古人/古經`, `雨落/雨露`, and the four-hour ordering from physical glyphs rather than OCR;
3. determine whether the Taiwan NCL single-title witness is edition-identical with, extracted from, or textually independent of the 1597 《夷門廣牘》 impression;
4. separately continue the Fullbook operational-current-time question. The Sizijing evidence concerns difficulty of determining birth hour under inclement conditions, not a complete time-acquisition mechanism.

Research record: `docs/research/ZIWEI-SIZIJING-INDEPENDENT-MING-PRINT-TRANSMISSION-R1.json`.
