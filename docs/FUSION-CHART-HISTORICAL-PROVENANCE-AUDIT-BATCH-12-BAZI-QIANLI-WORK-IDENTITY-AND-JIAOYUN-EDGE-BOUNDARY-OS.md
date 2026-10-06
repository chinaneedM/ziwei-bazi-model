# Fusion Chart Historical Provenance Audit R1 — Batch 12OS

## Qianli work identity repair and Jiaoyun edge-semantics source boundary

Status: **PROVENANCE DEFECT REPAIRED / EDGE SEMANTICS SOURCE-UNRESOLVED / NO RUNTIME CHANGE**

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
PROV_DEFECT_045=REPAIRED_FORWARD_ONLY
DIRECT_1935_MINGGAO_PHYSICAL_WORK_IDENTITY=CLOSED
DIRECT_1934_1936_MINGXUE_JIANGYI_JIAOYUN_RULE_IDENTITY=RETAINED
QIANLI_EDGE_SEMANTICS=SOURCE_UNRESOLVED
CURRENT_MISSING_FROM_PRODUCT_ROWS=4
ALGORITHM_REOPEN_COUNT=0
```

## 1. Why 12OS changed scope

12OR closed the ordinary Qianli Jiaoyun mechanics from direct 1934 and 1936 physical copies of 《韋千里命學講義》.

While pursuing the remaining invalid-date/leap-month edge rules, 12OS found a separate 1935 NLC physical object titled 《千里命稿》. Direct review plus independent reprint bibliography shows that the original 1935 work and the 1934/1936 instructional work must not be silently collapsed.

## 2. Direct 1935 《千里命稿》 work identity

NLC/Commons binds title 《千里命稿》, author 韋千里著述, publisher 韋氏命苑, date 民國24 / 1935, object 01jh000372 / 10197.

Direct no-OCR review of the cover and sampled early/near-end body leaves shows the body heading 《千里命稿 第一集》 and case-annotation content. Modern Heart & Yi Tang bibliography independently describes 《千里命稿（第一集）》 as first published in 1935 and as a collection of more than one hundred contemporary case annotations; it separately describes 《韋氏命學講義》 as first published in 1934.

Therefore these are separate work identities even though they share an author and close chronology.

## 3. PROV-DEFECT-045

The stable CText source IDs EXT-CTEXT-QIANLI-MINGGAO-YEAR and EXT-CTEXT-QIANLI-MINGGAO-DAYUN previously carried wording that could overstate the physical work identity behind the received passages.

CText labels its Wiki work 《千里命稿》 but declares the base edition unknown. The forward-only repair keeps the stable source IDs, relabels them as received Qianli transcriptions with unbound physical work identity, forbids original-1935 physical authority, keeps direct Jiaoyun mechanics bound to the 1934/1936 《韋千里命學講義》 witnesses, and registers the 1935 《千里命稿 第一集》 object separately.

No chart rule, coordinate, status, runtime profile or default changes.

## 4. Edge-semantics boundary

The 1934/1936 directly reviewed Jiaoyun target section supplies the ordinary worked method but does not state, within that reviewed section, a rule for day 30 landing in a small destination month, an intercalary birth/anchor, or regular-vs-intercalary selection when a destination month number occurs twice.

This is target-section nonattestation only, not whole-book or whole-author absence.

The official 1987 武陵《新編韋千里命學講義》 page confirms a later edition and a TOC containing 起例問答, but exposes no target leaf settling these edge rules. It contributes zero edge-rule vote.

袁樹珊《命理探源》 remains a Republican parallel control only: its explicit 實歷過日時 / 多欠 arithmetic is mechanically distinct from the Qianli nominal-30-day remainder replay. Cross-author borrowing is forbidden.

## 5. Product consequence

The three edge semantics are frozen as SOURCE_UNRESOLVED_AFTER_DIRECT_1934_1936_TARGET_SECTION_AND_CURRENT_PUBLIC_SEARCH_HORIZON.

HPA-DAYUN-CAL-003 and HPA-DAYUN-CAL-004 remain **MISSING_FROM_PRODUCT**.

No Qianli regime descriptor, Bazi historical temporal profile, runtime candidate, product selector, winner, production default or algorithm is added.

Accounting after 12OS: Matrix 222/222 audited; MISSING_FROM_PRODUCT 4; provenance defects 45/45 repaired; historical candidate extensions 14; registries/runtime resolvers 5/5; chart algorithm defects/reopens/candidate collapses 0/0/0.

## 6. Transmission genealogy

12OS explicitly separates 1935 《千里命稿 第一集》 from 1934/1936 《韋千里命學講義》. The CText site-title label is prevented from acting as a shortcut to the 1935 NLC physical object while its base edition remains unknown. No direct copying direction between the two works is asserted.

## 7. Next

**12OT — re-rank the four remaining MISSING_FROM_PRODUCT rows.**

The Qianli edge route must not be repeated unless a materially new edition, target leaf, archive route or wording bridge appears.

Research record: docs/research/QIANLI-WORK-IDENTITY-AND-JIAOYUN-EDGE-BOUNDARY-R1.json.
