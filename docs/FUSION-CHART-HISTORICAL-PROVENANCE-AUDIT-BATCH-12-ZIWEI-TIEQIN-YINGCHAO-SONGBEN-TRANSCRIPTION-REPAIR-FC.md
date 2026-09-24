# Fusion Chart Historical Provenance Audit R1 — Batch 12FC

## 鐵琴清抄本 400dpi 再校：把「影鈔本」前向修正為「影鈔宋本」，但不把書目描述誤作宋代實物年代

Status: **CURRENT COPY-DESCRIPTION METADATA REPAIRED FORWARD-ONLY / 準齋「影鈔宋本」DIRECTLY CLOSED / 銅壺 SAME-PAGE「影鈔宋本」INDEPENDENT CONTROL / PRIOR 12EY AUDIT RECORD PRESERVED / QING BIBLIOGRAPHIC DESCRIPTION != SONG PHYSICAL-COPY DATE / PROVENANCE DEFECT 13/13 REPAIRED / TG-E0103 REVISED / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EY used a 300-dpi direct review and recorded the Zhunzhai copy description as `影鈔本`. Batch 12FB then re-rendered the same Tianyi source window at 400 dpi. The stronger source-bound surface visibly carries one additional decisive glyph: `影鈔宋本`.

The current Registry and Transmission Graph still retained the earlier abbreviated current value. Because those are live research metadata rather than a historical batch snapshot, they must be repaired forward-only.

## 2. Controlling physical evidence

- Tianyi Pavilion Qing manuscript 《鐵琴銅劍樓藏書目錄》, object `330000-1705-0004561 / 善2088`.
- Source PDF SHA-256: `29d6774b33087ee8140d7141ca85bd60d25d1872bc636a33da35be9b75dbfc6f`.
- Target PDF p387, 400-dpi render SHA-256: `1a27cb70651956d59e847f0161e45ccc2749992910f11bda5a2feaa86667b227`.
- Extraction commit `5f12da4b0815c76cebdb9076e09f6ec3658e6c7a`; workflow `35968905286`; artifact `10795545616`, digest `sha256:ddd321789cc420f2342a883efce0ee8e60514b79794a0476de0b783b2f901611`.
- No OCR is final authority.

## 3. Direct p387 re-collation

The immediately preceding Copper entry reads:

    銅壺漏箭制度一卷
    影鈔宋本

The Zhunzhai entry then reads:

    準齋心製几漏圖式一卷
    影鈔宋本
    宋孫逢古撰并序

The Copper entry supplies a same-page independent layout/wording control. The earlier `影鈔本` is therefore an incomplete transcription, not a demonstrated alternative recension reading on this physical surface.

## 4. Forward-only repair

The project does not rewrite Batch 12EY as though the earlier audit never occurred.

    12EY historical record: preserved
    current Registry field: 影鈔本 -> 影鈔宋本
    current Graph field:    影鈔本 -> 影鈔宋本
    correction provenance:  Batch 12FC

Formal provenance metadata defect accounting advances to 13 confirmed / 13 repaired. Matrix row count and audited-row count do not change.

## 5. 「影鈔宋本」chronology firewall

The phrase is evidence about a Qing bibliographic copy-description / asserted copy relationship. It does not prove that the reviewed Tianyi catalog manuscript or the current NLC 1823 Huang-family composite manuscript is a Song physical object; it does not identify a surviving Song exemplar; and it does not physically attest the exact Zhunzhai 25-arrow prose before 1578.

Huang's `原書舊鈔` / `錄副` layers, the exact Song exemplar, copy chain and copy date all remain unresolved.

## 6. Transmission consequence

Batch 12FC adds no new node and no new edge. It strengthens the existing Tianyi physical-copy and Zhunzhai passage nodes and revises `TG-E0103` at evidence/scope level only. No Song-date edge, NLC-1823 same-object edge, 1827 direct-copy edge or Sanming-parent edge is authorized.

## 7. Product firewall

    MATRIX_ROWS=198
    AUDITED_ROWS=166
    MISSING_FROM_PRODUCT=10
    PROVENANCE_DEFECTS=13/13_REPAIRED
    CONFIRMED_CHART_ALGORITHM_DEFECTS=0
    ALGORITHM_REOPEN=0
    CANDIDATE_COLLAPSE=0
    DIRECT_SANMING_PARENT_VOTE_INCREMENT=0
    DETERMINISTIC_PRODUCT=CLOSED

## 8. Next gate

Return to the Batch 12FB object-level gate: independently identify the fourth lower NLC Copper seal or another unique acquisition/shelfmark signature; keep `原書舊鈔`, `錄副`, NLC 1823 and the 1827 Airijinglu source separate until direct evidence joins them. Continue the Yuan person-title, securely pre-1578 exact 25-arrow prose, and independent Sanming/Nanjing-59 lines in parallel.

Research record: `docs/research/ZIWEI-TIEQIN-YINGCHAO-SONGBEN-TRANSCRIPTION-REPAIR-R1.json`.
