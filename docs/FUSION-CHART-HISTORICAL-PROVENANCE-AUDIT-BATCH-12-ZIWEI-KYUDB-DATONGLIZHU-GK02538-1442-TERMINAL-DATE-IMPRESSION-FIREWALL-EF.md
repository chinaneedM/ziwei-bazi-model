# Fusion Chart Historical Provenance Audit R1 — Batch 12EF

## 奎章閣 GK02538_00《大統曆註》：正統七年十二月終端日期與刊年防火牆

Status: **DIRECT 1442 TERMINAL INTERNAL DATE CLOSED / TERMINAL TEXTUAL LAYER NOT BEFORE 1442 / EXACT SURVIVING-COPY IMPRESSION YEAR STILL UNRESOLVED / NO EXPLICIT 印出 ADJACENT TO THE 1442 LINE / ZERO SANMING-PARENT VOTE / NO RUNTIME CHANGE**

## 1. Why this batch

Batch 12EE directly recovered the 1434 金鑌 type-casting postface on GK02538 p057a-p057b, but correctly kept the surviving copy's impression year unresolved because Kyujanggak still catalogs the object as `刊年未詳`.

The same direct p057b image contains a second, separately printed chronological line at the far left:

```text
正統七年十二月日
```

12EE intentionally left its referent unresolved. 12EF adjudicates only the chronology that this physical line safely supports.

## 2. Direct physical control

Object identity remains:

```text
provider       Kyujanggak Institute for Korean Studies, Seoul National University
item_cd        CSP
book_cd        GK02538_00
call number    奎2538-v.1-4
title          大統曆註
edition        觀象監活字
catalog year   刊年未詳
extent         12卷 4冊
microfilm      M/F83-16-89-D
```

The reused source-bound Batch 12EE artifact is workflow run `35516795637`, artifact `10606724326`, digest:

```text
sha256:407a937f452431c1adcd6fb46c10b4446bf2e3e08b1f2e1bc727b9683fb59349
```

Direct no-OCR review of volume 4 p057b, SHA-256:

```text
9bf50977f2ab0cbe21b326bd4ec1eaa20493dc93a47917ee291695f8df90232b
```

shows the 1434 金鑌 postface closing with `宣德九年九月日` / `臣金鑌拜手稽首敬跋`, and a separate printed column:

```text
正統七年十二月日
```

The next acquired leaves, p058a-p058b, are blank.

## 3. What 1442 closes — and what it does not

`正統七年` corresponds to 1442. Therefore the reviewed terminal textual layer directly reproduces an internal date of 1442.

The safe chronology is:

```text
1434 = 金鑌 type-casting / new-type printing-event postface date
1442 = separately printed terminal internal date on the reviewed leaf
surviving GK02538 impression year = still unresolved
```

This supports a textual terminus post quem for the terminal layer:

```text
TERMINAL_TEXTUAL_LAYER_NOT_BEFORE_1442 = TRUE
```

It does **not** authorize:

```text
GK02538 WAS DEFINITELY PRINTED IN 1442 = FALSE
正統七年十二月日 IS PROVED TO MEAN 印出 = FALSE
ALL CALENDAR RULES WERE COMPOSED IN 1442 = FALSE
```

No adjacent `印出` marker is visible on p057b. The catalog remains `刊年未詳`.

## 4. Comparative colophon controls

Two external controls sharpen this firewall without replacing the physical GK02538 image.

The Academy of Korean Studies encyclopedia entry for 《大統曆註》 states that the 金鑌 postface was written in 1434, but that its content concerns type casting rather than the Datong calendar. This independently supports keeping the 1434 date scoped to the type-event postface.

A Keio Momijiyama-bunko record for a different 甲寅字 book preserves the same class of 1434 金鑌 type-casting postface and then separately records:

```text
正統元年十一月日 印出
```

This is a useful comparative convention: a type-history postface and an object-specific printing statement can be separate. It does **not** prove that GK02538's bare `正統七年十二月日` has the same function.

## 5. Transmission consequence

12EF strengthens one existing graph node:

```text
PHYSICAL-COPY-KYUDB-DATONGLIZHU-GK02538-GWANSANGGAM-MOVABLETYPE
```

with a directly observed 1442 internal terminal date.

No direct-copy edge is added. No existing non-edge is reversed. The exact Sanming-parent vote increment remains zero.

The recensional conclusion from 12EE remains controlling:

- GK02538 and GK02426 are distinct physical recensions;
- GK02538's Rainwater and Dahan fingerprint does not exactly match Sanming/Yueling;
- a common-recensional-family candidate is possible, but direct copy direction is unproved.

## 6. Product consequence

No deterministic chart algorithm changes.

```text
Matrix rows                 198
Audited rows                166
MISSING_FROM_PRODUCT         10
Provenance defects          12 / 12 repaired
Chart algorithm defects      0
Algorithm reopen             0
Candidate collapse           0
DETERMINISTIC PRODUCT        CLOSED
```

## 7. Next gate

The next highest-value work is:

1. resolve the function of `正統七年十二月日` through copy/type/bibliographic evidence, without assuming the missing word `印出`;
2. continue the search for a securely pre-1578 witness carrying the exact combined `雨水 -> 後四日` and `大寒 十三後日` fingerprint;
3. continue the search for an explicit operator connecting `冬至餘…已上為退` state thresholds to whole-ke output.

Research record: `docs/research/ZIWEI-KYUDB-DATONGLIZHU-GK02538-1442-TERMINAL-DATE-IMPRESSION-FIREWALL-R1.json`.
