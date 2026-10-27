# Fusion Chart Historical Provenance Audit R1 — Batch 12FD

## 國圖 1823《銅壺漏箭制度》卷首第四印：直接閉合「鐵琴銅劍樓」收藏印，但不把收藏印誤作唯一物件編號

Status: **NLC1823 LOWER TIEQIN COLLECTION SEAL DIRECTLY CLOSED / 鐵琴銅劍樓 COLLECTION PROVENANCE CLOSED / INDEPENDENT NCL SEAL-NAME + FIGURE CONTROL / EXACT TIEQIN-CATALOGUED UNIQUE PHYSICAL OBJECT IDENTITY VERY STRONGLY SUPPORTED BUT NOT COLLAPSED / HUANG 原書舊鈔・錄副 FIREWALL PRESERVED / NO PRE-1578 RULE CLOSURE / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12FB closed a compound Tieqin catalog fingerprint for the Copper/Zhunzhai object:

- 《銅壺漏箭制度》 + 《準齋心製几漏圖式》;
- 合裝一冊;
- 郡中黃氏舊藏;
- 蕘翁有跋;
- Copper volume head: 士禮居藏 / 黃印丕烈 / 蕘圃.

The current NLC/Xuxiu1031 1823 object directly matched those first three Huang seals, but one lower long rectangular seal was still unresolved. Batch 12FC then returned that unresolved seal as the highest object-level gate.

The question is narrow:

> What does that lower seal actually read, and does it uniquely identify the current NLC 1823 object with the copy described in the Tieqin catalog?

## 2. Source-bound extraction

Controlling target remains the public reproduction of the NLC-held Qing Daoguang-3 Huang Shiliju composite manuscript in 《續修四庫全書》第1031冊:

- source PDF SHA-256: 07348e40ec26ca38efe9c9736a69c403c61f9b07a2c89a847fc68d00ce6d8c25;
- target PDF page: p78, Copper title page;
- prior 220-dpi p78 SHA-256: 43f91f0d11eb88a014bb1a5fe53bc5ec696df540cfc2318cc9e80ba04e4c1329.

A dedicated source-bound extraction workflow now magnifies the fixed page for seal review:

- workflow file: .github/workflows/extract-xuxiu1031-p78-seal-column.yml;
- controlling commit: 3692539a7d9b3e47e93568211fee472a2c336237;
- workflow run: 36002988836;
- artifact: 10809201996;
- artifact digest: sha256:ac7e01957bd7f0e4c8a741cffbe3daf02aabd795b99daa6da477048f76c42e4a;
- 600-dpi render SHA-256: e302f09b20bf716415f19b8affaa079e3e30e63bada2087bc77680b898194a41;
- full seal-column crop SHA-256: 449af987bb2e20ac18ab5eeb5efb1964e8944d211fb6998dc9033c8ae29cb4e1;
- lower-seal review crop SHA-256: d8d48d3f3f05a9a7babd344bbf438d36ea03312de3b42387e5f79029f665876b.

The 600-dpi render is an inspection magnification of the same hash-locked PDF page. It is **not** treated as newly recovered native scan information. No OCR is final authority and no generative enhancement is used.

The first extraction attempt failed only because Pillow's image-size guard rejected the 600-dpi render; the source download/hash and PDF render had succeeded. The workflow was then forward-only repaired and the controlling extraction completed successfully.

## 3. Direct p78 seal reading

The current p78 Copper title page preserves the already-closed Huang seal set:

    士禮居藏
    黃印丕烈
    蕘圃

The lower long rectangular collector's seal can now be directly read as:

    鐵琴銅劍樓

Therefore:

    NLC1823 lower seal identity
        = 鐵琴銅劍樓
        = CLOSED

## 4. Independent seal controls

The target-page reading is not accepted merely because the expected owner is known.

Two independent National Central Library controls are used:

1. NCL's official catalog record for 《三曆撮要》 explicitly lists 「鐵琴銅/劍樓」白文長方印.
2. Zhang Wei-tung's NCL journal study, 〈古籍裡的風景—國家圖書館的藏書印記初探〉, Figure 36 explicitly labels the physical seal reproduced from 《三曆撮要》 as Qu Yong's 「鐵琴銅劍樓」藏書印.

These controls establish the seal name/form independently of the target object's expected provenance. They are comparator evidence, not a claim that 《三曆撮要》 and the current Copper/Zhunzhai manuscript are the same object.

## 5. Provenance conclusion

The direct seal closes a new layer:

    current NLC 1823 Copper/Zhunzhai composite object
        -> later entered / was marked by
    鐵琴銅劍樓 collection

        = CLOSED

This materially strengthens Batch 12FB, because the current physical object now carries:

- the same Huang seal trio that the Tieqin catalog records for Copper;
- the Copper/Zhunzhai paired composite structure;
- Huang/Raoweng paratext;
- and an actual 鐵琴銅劍樓 later-collection mark.

## 6. Why exact unique-object collapse is still withheld

The seal is highly probative provenance evidence, but it is still a **collection mark**, not a unique item number.

Huang Pilie's 1823 paratext independently proves more than one copy layer existed:

    原書舊鈔
        !=
    錄副

Therefore the strongest safe object-identity statement is:

    current NLC 1823 object
        ==
    specific composite object described by the reviewed Tieqin catalog entry

        = VERY_STRONGLY_SUPPORTED_NOT_FORMALLY_UNIQUE_OBJECT_CLOSED

A formal unique-object collapse still requires one-object evidence such as:

- a unique Tieqin-era shelfmark or acquisition/donation crosswalk;
- a uniquely matching binding repair, paper defect or annotation;
- or another physical marker incapable of being shared across multiple Qu/Huang holdings.

No SAME_OBJECT graph edge is invented.

## 7. Copy-layer, chronology and rule firewalls

This batch does **not** decide:

- whether the current 1823 object is Huang's 原書舊鈔 or 錄副;
- whether it is exactly Zhang Jinwu's 1827 從吳門黃氏藏舊抄本;
- whether a surviving Song physical exemplar exists;
- whether the exact 25-arrow prose is physically attested before 1578;
- whether the Yuan 1281 Yanling Sun Fengji is exactly the Zhunzhai author;
- whether Zhunzhai is a direct parent of the Sanming/Yueling table.

Thus:

    direct Sanming-parent vote increment = 0
    algorithm reopen = 0
    candidate collapse = 0

## 8. Transmission-genealogy consequence

Batch 12FD adds:

- PASSAGE-NLC1823-COPPER-TIEQIN-OWNERSHIP-SEAL;
- TG-E0107: the NLC 1823 physical-copy node **ATTESTS** the direct Tieqin ownership-seal passage.

It strengthens the NLC 1823 physical-copy node and the existing Tieqin catalog composite-fingerprint route, but deliberately does not create a same-object or direct-copy edge.

## 9. Project accounting

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=13/13_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
    DETERMINISTIC_PRODUCT=CLOSED

No provenance-defect increment is counted: UNADJUDICATED -> identified by new evidence is normal research progress, not correction of a previously false metadata assertion.

## 10. Next gate

1. Search Tieqin/NLC acquisition, donation and shelfmark records for a unique one-object crosswalk beyond the collection seal.
2. Keep Huang 原書舊鈔 / 錄副 and the 1827 Airijinglu source-copy identities separate.
3. Continue Yuan person-title and securely pre-1578 exact 25-arrow prose searches.
4. Keep the independent Sanming/Yueling Dahan-Rainwater and Nanjing-59 lines active.

Research record: docs/research/ZIWEI-NLC1823-TIEQIN-SEAL-PROVENANCE-CONTROL-R1.json.
