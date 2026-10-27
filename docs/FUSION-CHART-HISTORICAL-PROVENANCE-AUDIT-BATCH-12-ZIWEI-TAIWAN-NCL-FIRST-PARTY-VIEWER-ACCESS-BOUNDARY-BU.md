# Fusion Chart Historical Provenance Audit R1 — Batch 12BU

## 臺灣國圖 15275-0058 第一方影像瀏覽路徑與人機驗證邊界

Status: **CURRENT TAIWAN NCL FIRST-PARTY RBOOK RECORD DIRECTLY BOUND TO 四字經 / 15275-0058 / MING-WANLI JINLING JINGSHAN-SHULIN EDITION / RECORD EXPOSES AN IMAGE-VIEWER TARGET FOR THE SAME ITEM / IMAGE ENTRY IS GUARDED BY A PUZZLE CAPTCHA / DIRECT GET OF THE VIEWER URL WITHOUT SUCCESSFUL HUMAN VERIFICATION RETURNS THE DETAIL SURFACE, NOT IMAGEC PAGE LINKS / NO CAPTCHA BYPASS OR AUTOMATED SOLVING ATTEMPTED / FIRST-PARTY TARGET-LEAF IMAGE ACCESS REMAINS HUMAN-VERIFICATION-BOUNDARY / BATCH-12BT PUBLIC-SCAN LACUNA THEREFORE NOT YET CLOSED / HPA-ZDATE-006 STILL MISSING_FROM_PRODUCT / HAI-BRANCH MECHANICAL VOTE +0 / NO RUNTIME WINNER / NO CANDIDATE COLLAPSE / NO ALGORITHM REOPEN**

## 1. Scope

Batch 12BT established that the 21-page Commons derivative of Taiwan NCL 15275-0058 omits the `唐明皇論` body leaf even though the physical TOC lists that unit. Batch 12BU tests the current first-party NCL `rbook.ncl.edu.tw` record and viewer contract without bypassing access controls.

Exact probe chain:

- first-party record: `https://rbook.ncl.edu.tw/NCLSearch/Search/SearchDetail?item=4f498ed65b97408aaf74cfcc1bec50abfDU0NDQ40.ug9YiJNB_UJXAc_XtEgviCIhdiQ0ZG3qjeyuaPAXm5Q_&page=&SourceID=1&HasImage=`;
- probe commit/tree: `3a78c8886d86db7b1904bcaaff4ee6b3c11d6457` / `367683b259f6fe8c935222040711b9dfdd54f996`;
- successful workflow run: `34826374689`;
- artifact: `10340003938`, digest `sha256:8f76217d9614eda5f291614cae43fa0b6d58dbe68e388ec2b6ccbceb6f57517a`;
- catalog HTML SHA-256: `b1ae87e2742faa16e5df46dea2f4693a2fd5ecf5c4db96ef9e0d52d30a2619d2`;
- direct image=1 / SourceID=1 HTML SHA-256: `24512ba9983778f8cdad16c0ec944019cd0880dc7c4a18f6daf623f640f800d4`;
- direct image=1 / blank-SourceID HTML SHA-256: `e33d8e23c4db3da68de42eacd27ed2b7739570ff18479af0555948eac92569b8`.

## 2. Current first-party record and viewer binding

The first-party detail HTML directly binds:

- title `四字經`;
- book/accession number `15275-0058`;
- source `古籍影像檢索資料庫`;
- owner `國家圖書館`;
- a thumbnail route under `/NCLSearch/WaterMark/GetMinImage?...`;
- hidden viewer target `/NCLSearch/Search/SearchDetail?item=4f498ed65b97408aaf74cfcc1bec50abfDU0NDQ40.ug9YiJNB_UJXAc_XtEgviCIhdiQ0ZG3qjeyuaPAXm5Q_&image=1&page=&SourceID=1&HasImage=`.

The viewer link does not navigate immediately. Its click handler opens a puzzle-captcha modal. The official page initializes the challenge with:

```text
/NCLSearch/Users/GenerateCaptcha
/NCLSearch/Users/VerifyCaptcha
```

Only the configured success callback navigates to the hidden viewer URL.

## 3. No access-control bypass

Direct unauthenticated HTTP GETs to the image=1 URL returned HTTP 200, but the returned HTML contains no `.ImageC` page entries and no exposed target-page image list. The downloaded first-party `imageControl.js` shows that an admitted viewer would normally enumerate `.ImageC` page links and request per-image watermark tokens through `../Watermark/getToken`; those admitted-viewer structures were not present in the direct GET response.

The captcha JavaScript explicitly implements interactive puzzle movement/rotation and verification. This research batch does **not** call the verification endpoint with fabricated solutions, infer challenge answers, replay another session, or otherwise bypass the human-verification gate.

Therefore the current result is an access boundary, not a negative holding result:

```text
FIRST_PARTY_VIEWER_ROUTE_EXISTS
HUMAN_PUZZLE_VERIFICATION_REQUIRED_BEFORE_IMAGE_ENUMERATION
TARGET_BODY_LEAF_PRESENCE_IN_FIRST_PARTY_VIEWER = UNRESOLVED
```

## 4. Effect on Batch 12BT and HPA-ZDATE-006

The current first-party record strengthens object identity and proves that NCL advertises an image-browse path for this exact holding. It does not yet reveal whether that viewer contains additional pages omitted from the 21-page Commons derivative.

Consequently:

- Batch 12BT `PUBLIC_SCAN_LACUNA` remains valid;
- first-party target body leaf presence remains `UNRESOLVED_AT_HUMAN_VERIFICATION_BOUNDARY`;
- Taiwan direct target-variant glyph increment remains `0`;
- `HPA-ZDATE-006 = MISSING_FROM_PRODUCT`;
- Hai-branch mechanical vote increment: `0`;
- runtime winner selected: `false`;
- candidate collapsed: `false`;
- algorithm reopen authorized: `false`.

Global accounting remains `198 rows / 166 audited / 10 MISSING_FROM_PRODUCT / 14 cumulative missing candidate families`; provenance defects remain `11/11`; chart algorithm defect/reopen/collapse remain `0/0/0`.

## 5. Next gate

1. Continue research without bypassing the NCL captcha: seek another lawful first-party/derivative route that exposes the omitted Taiwan target leaf.
2. In parallel, directly locate/collate a physical or facsimile Yongle-Dadian target leaf for the `古經/古人`, `雨露/雨落`, and hour-order loci.
3. Only if these public routes are exhausted and the Taiwan target leaf remains uniquely valuable should a human-operated NCL viewer session be requested as an explicit external-interaction step.

Research record: `docs/research/ZIWEI-TAIWAN-NCL-FIRST-PARTY-VIEWER-ACCESS-BOUNDARY-R1.json`.
