# Fusion Chart Historical Provenance Audit R1 — Batch 12IL

## Google Books 公开索引边界：`searchable:false` 禁止把 0 hits 当作阴性文本证据

Status: **VOLUMES API HTTP429 QUOTA=0 / KNOWN JI VOLUME SEARCHWITHINVOLUME2 HTTP200 BUT SEARCHABLE=FALSE / 14 ZERO RESULTS HAVE ZERO ABSENCE VALUE / NO DIRECT PAGE OR SNIPPET / ZERO PRODUCT CHANGE**

### Probe

- Exact probe commit: `3b0d1500eba51be44a76a27098bc43dd0e6eb3d0`.
- Workflow run `36701117083`, job `109840523830`, completed success.
- Anonymous public HTTP only; no account, purchase or access bypass.

### Google Books Volumes API

Ji ISBN/title and Zhao ISBN/title queries all returned HTTP 429 with `RESOURCE_EXHAUSTED`, `RATE_LIMIT_EXCEEDED`, and `defaultPerDayPerProject` quota limit value `0`. This is an environment/API-access boundary, not a zero-result response and not evidence that a volume does not exist.

### Known Ji volume in-book search

On public volume route `bAnzzgEACAAJ`, fourteen high-information `SearchWithinVolume2` queries all returned HTTP 200 JSON with `number_of_results=0` **and** `searchable=false`. Terms include `铁琴铜剑楼`, `收购入藏`, `瞿凤起`, `吴梅`, `涵芬楼`, `周叔弢`, `三百零四`, `五十二种` and six Zhao/Qu controls.

The decisive field is `searchable=false`: zero hits cannot be promoted to textual absence, chapter nonexistence, or page-level negative evidence.

### Adjudication

- Ji Google Books public in-book route: `CLOSED_NONSEARCHABLE_PUBLIC_INDEX`.
- Google Books Volumes API route in this probe environment: `RATE_LIMITED_QUOTA_ZERO_UNRESOLVED`.
- Ji Chapter 9 direct text/page range: unchanged, unresolved/not reviewed.
- Zhao 2011 p.197 and 1951 pp.221–233: unchanged, not reviewed.
- No runtime, algorithm, candidate, transmission-topology or product change.

### Highest next gate

Stop spending cycles on this nonsearchable Ji Google Books route. Return to lawful direct page/object discovery, especially Chapter 9 page-numbered contents/direct scans, Zhao 2011 p.197, and the `wwck195109.pdf` locator through an authoritative/open source.

Research record: `docs/research/ZIWEI-GOOGLE-BOOKS-JI15-NONSEARCHABLE-AND-API-QUOTA-BOUNDARY-R1.json`.
