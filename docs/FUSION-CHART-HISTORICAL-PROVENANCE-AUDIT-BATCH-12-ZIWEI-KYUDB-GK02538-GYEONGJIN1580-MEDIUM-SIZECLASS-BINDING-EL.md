# Fusion Chart Historical Provenance Audit R1 — Batch 12EL

## GK02538《大統曆註》× 1580《庚辰年大統曆》：共享字形中字号档绑定与铸造代防火墙

Status: **GYEONGJIN 正/月 MEDIUM INRYEOKJA SIZE CLASS SUPPORTED / SAME-SIZE-CLASS SHARED-GLYPH GATE CLOSED AT NOMINAL CLASS LEVEL / PHYSICAL-SCALE FORM NORMALIZATION NOT YET CLOSED / CASTING GENERATION UNRESOLVED / EXACT IMPRESSION YEAR UNRESOLVED / NO RUNTIME CHANGE**

## 1. Why this batch

12EK fixed the exact source bytes and pixel crops for shared `正/月` glyphs, but deliberately left the 1580 size class unresolved.

12EL closes that missing size-class bridge only.

## 2. Institutional type-size control

The National Science Museum of Korea's printing-type record identifies `인력자` as the iron calendar type used by Gwansanggam and directly presents `인력자_경진년대통력` as its example.

It gives two physical size classes:

```text
medium  1.2 × 0.8 cm
small   0.5 × 0.4 cm
```

The Korea Heritage Portal independently identifies the surviving `庚辰年大統曆` as a Gwansanggam movable-type calendar and as the earliest surviving book printed with Gwansanggam `印曆字`.

These are institutional/bibliographic controls; neither source identifies an individual metal sort or casting generation.

## 3. Binding the 12EK crops to a size class

12EK already hash-locked the exact 1580 tail image and the fixed manual crops:

```text
source SHA256 306b8f03949850c0cedd9575263208ccbd9dc8e6465165b13406ef1918788590
正 [698,565,754,625]
月 [698,620,754,680]
manual context: 正/月/大 printed heading column
```

Direct visual review places these characters in the visibly larger heading class, distinct from the dense small body text on the same calendar page.

Given the institutional two-size Inryeokja control, the larger target class is therefore bound to the **medium** class at object-layout level.

```text
1580 target size class                    MEDIUM SUPPORTED
exact printed-glyph caliper measurement   NO
photo perspective fully rectified         NO
same individual metal sort                NOT PROVED
same casting generation                   NOT PROVED
```

## 4. Cross-object consequence

12EI already established that GK02538's nominal 25.3 cm / 21-character pitch is compatible with the official 1.2 cm medium Inryeokja height.

12EL now permits the following narrowly scoped statement:

```text
GK02538 target class     nominal medium-compatible
1580 正/月 target class  medium-class supported
same-size-class shared-glyph comparison gate  CLOSED AT NOMINAL CLASS LEVEL
```

It does **not** yet permit type-form identity adjudication because source photography, perspective, inking, wear, paper deformation and scan processing remain uncontrolled.

## 5. Chronology / product consequence

GK02538 subtype, casting generation and exact surviving-copy impression year remain unresolved. Secure pre-1578 surviving physical impression remains false. Exact Sanming-parent vote increment remains 0.

Matrix 198 / audited 166 / MISSING_FROM_PRODUCT 10 / provenance defects 12/12 repaired / chart algorithm defect 0 / reopen 0 / candidate collapse 0. Deterministic product remains CLOSED.

## 6. Next gate

1. add more medium-class shared glyphs and normalize by physical scale before form adjudication;
2. recover object-level subtype/casting diagnostics from Kim Sang-Ho 1987 or equivalent authoritative typographic research;
3. continue the independent pre-1578 Rainwater + Dahan fingerprint / threshold-operator search.

Research record: `docs/research/ZIWEI-KYUDB-GK02538-GYEONGJIN1580-MEDIUM-SIZECLASS-BINDING-R1.json`.
