# Fusion Chart Historical Provenance Audit R1 — Batch 12HH

## 《文物参考资料》1951年第9期：赵万里原刊的精确实体馆藏路线

Status: **ORIGINAL 1951 SERIAL NUMBERING CLOSED / V2N9 TARGET ISSUE CLOSED / OSAKA METROPOLITAN UNIVERSITY FIRST-PARTY EXACT-ISSUE HOLDING CLOSED / FOUR ADDITIONAL CINII EXACT-ISSUE HOLDINGS CLOSED / DIRECT PP221–233 TEXT NOT REVIEWED / REMAINING FOUR DING TITLES UNRESOLVED / ZERO PRODUCT, MATRIX, RUNTIME OR GENEALOGY CHANGE**

## 1. Why this batch matters

12HF located Zhao Wanli's 1951 article bibliographically and 12HG closed a later collected-text route through `《赵万里文集》第1卷` p.197.

The missing access question was whether the **original 1951 journal issue itself** can be bound to concrete physical holdings.

## 2. Original article locator

The National Library of China review carried forward from 12HF gives:

```text
赵万里
《永乐大典展览的意义——一九五一年八月北京图书馆举办》
《文物参考资料》
1951年第9期
pp.221–233
```

This batch does not upgrade that bibliographic locator into direct page-text review.

## 3. Serial identity and issue numbering

CiNii serial record `NCID AA11467834` identifies the original serial as `《文物参攷資料》`, with variant title `《文物参考資料》`.

The 1951 run is explicitly numbered:

```text
2巻1期 (1951.1) – 2巻12期 (1951.12)
```

Therefore:

```text
NLC "1951年第9期"
  == serial volume 2 issue 9
```

at the issue-numbering level.

## 4. First-party exact issue holding

大阪公立大学杉本図書館's own OPAC records:

```text
1950,
1951(1-7, 9-12),
1952-1957,
1958(1-4, 6-12)
```

Local bibliography ID: `SB00000024`.

Issue 9 is explicitly present.

```text
ORIGINAL_1951_V2N9_PHYSICAL_HOLDING
  = CLOSED_FIRST_PARTY_OMU_OPAC
```

## 5. Additional exact-issue routes from CiNii

CiNii independently lists:

```text
京都大学 桂図書館          2(1,3,5-12)
同志社大学 図書館 史学    2(2-12)
早稲田大学 戸山図書館    1951(2-4,6-12)
愛媛大学 図書館            2(6-12)
```

Every one of those explicit ranges includes issue 9.

These are physical holding routes, not page images and not copy entitlements.

## 6. Direct-text boundary

The project still has **not** directly reviewed Zhao pp.221–233 in the 1951 issue.

```text
ORIGINAL_1951_ARTICLE_PAGES_DIRECTLY_REVIEWED = false
ORIGINAL_DING_SIX_WORDING_DIRECTLY_COLLATED = false
DIGITAL_SCAN_BYTES_RECOVERED = false
COPY_REQUEST_SENT = false
ILL_REQUEST_SENT = false
LIBRARY_ACCOUNT_ACTION = false
IDENTITY_TRANSMITTED = false
FEE_INCURRED = false
```

The NLC first-party PDF used for the article locator was text-readable; screenshot retrieval for the relevant PDF page timed out in the current research session, so this batch makes no new visual-glyph claim from that review.

## 7. Relation to HF / HG

HF remains:

```text
DING_HUIKANG_SIX_TOTAL = CLOSED_AT_QUOTATION_BRIDGE_LEVEL
NAMED = 东家杂记 / 太平乐府
REMAINING_FOUR = UNRESOLVED
```

HG remains:

```text
2011 《赵万里文集》第1卷 p.197 physical route = CLOSED
direct p.197 text = NOT_REVIEWED
```

12HH's new increment is specifically:

```text
ORIGINAL_1951_VOLUME2_ISSUE9_PHYSICAL_ROUTES = CLOSED
```

No claim is made yet that the 1951 original and 2011 collected-text wording are letter-for-letter identical.

## 8. Target firewall

Neither the reviewed catalog records nor issue holdings name:

- 《铜壶漏箭制度》;
- 《准斋心制几漏图式》;
- 3482 / 3483;
- 03482 / 03483.

Thus the target's membership in the Ding six remains unresolved.

## 9. Product / genealogy consequence

```text
NODES_ADDED=0
EDGES_ADDED=0
ACQUISITION_EDGE_AUTHORIZED=false
RUNTIME_RULE_CHANGE=false
ALGORITHM_REOPEN=false
CANDIDATE_COLLAPSE=false
MATRIX_COUNT_CHANGE=false
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
```

Accounting remains `198 / 166 / 10`, provenance metadata defects `14 / 14 repaired`, chart algorithm defects `0`.

## 10. Highest next gate

1. Directly inspect original 1951 v2 no.9 pp.221–233 under lawful library access.
2. Compare the exact six-title wording with 2011 `《赵万里文集》第1卷` p.197.
3. Recover the remaining four Ding titles before merging HC/HF traditions.
4. Continue 2018 pp.309–310, 1997 pp.446–449, Ji chapter 9, 2004 p.335/final `《編后記》`, and the 2010 supplement route.

Research record: `docs/research/ZIWEI-WENWU-CANKAO-1951-V2N9-ZHAO-WANLI-ORIGINAL-ISSUE-PHYSICAL-HOLDINGS-R1.json`.
