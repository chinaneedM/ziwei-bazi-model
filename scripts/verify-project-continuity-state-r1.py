#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "docs" / "PROJECT-CURRENT-STATE-R1.json"
PROTOCOL = ROOT / "docs" / "PROJECT-CONTINUITY-PROTOCOL-R1.md"
AUTHORITY = ROOT / "docs" / "FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md"
MATRIX = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-MATRIX-R1.json"
SOURCE_REGISTRY = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-EXTERNAL-SOURCE-REGISTRY-R1.json"
IDENTITY_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-1940-PRECIOUS-CATALOG-U.md"
IDENTITY_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-1940-PRECIOUS-CATALOG-IDENTIFIER-BINDING-R1.json"
MF_PDF_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-MF-PDF-ROUTE-V.md"
MF_PDF_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-MF-PDF-ROUTE-R1.json"
ARTICLE_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-LEE-JING-1998-OFFICIAL-ARCHIVE-W.md"
ARTICLE_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "G893-LEE-JING-1998-OFFICIAL-JOURNAL-ARCHIVE-R1.json"
LATEST_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-11-BAZI-G893-OFFICIAL-REPRODUCTION-ROUTE-X.md"
LATEST_MACHINE_EVIDENCE = ROOT / "docs" / "research" / "KYUJANGGAK-G893-OFFICIAL-REPRODUCTION-ROUTE-R1.json"
ZIWEI_LATE_ZI_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A.md"
ZIWEI_LATE_ZI_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-NANYANGTANG-LATE-ZI-DIRECT-COLLATION-R1.json"
ZIWEI_TIMEKEEPING_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B.md"
ZIWEI_TIMEKEEPING_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-LATE-ZI-TIMEKEEPING-COLLATION-R1.json"
ZIWEI_EDITION_ROUTES_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C.md"
ZIWEI_EDITION_ROUTES_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-R1.json"
ZIWEI_WENGUANG_INDEX_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D.md"
ZIWEI_WENGUANG_INDEX_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-WENGUANG-GOOGLE-INDEX-PREVIEW-R1.json"
ZIWEI_JINGLUNTANG_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E.md"
ZIWEI_JINGLUNTANG_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-R1.json"
ZIWEI_POST_E_ROUTES_BATCH = ROOT / "docs" / "FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-F.md"
ZIWEI_POST_E_ROUTES_EVIDENCE = ROOT / "docs" / "research" / "ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-R1.json"
ZIWEI_QUANJI_LATE_ZI_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G.md"
ZIWEI_QUANJI_LATE_ZI_EVIDENCE = ROOT / "docs/research/ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json"
ZIWEI_JAPAN_MING_FULLBOOK_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-H.md"
ZIWEI_JAPAN_MING_FULLBOOK_EVIDENCE = ROOT / "docs/research/ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-R1.json"
ZIWEI_LATE_ZI_DEDUP_LOCATOR_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-I.md"
ZIWEI_LATE_ZI_DEDUP_LOCATOR_EVIDENCE = ROOT / "docs/research/ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-R1.json"
ZIWEI_GUANGYI_PHYSICAL_SET_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-J.md"
ZIWEI_GUANGYI_PHYSICAL_SET_EVIDENCE = ROOT / "docs/research/ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-R1.json"
ZIWEI_WENGUANG_BASE_COPY_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-K.md"
ZIWEI_WENGUANG_BASE_COPY_EVIDENCE = ROOT / "docs/research/ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-R1.json"
ZIWEI_KANGJIE_TYPESET_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-L.md"
ZIWEI_KANGJIE_TYPESET_EVIDENCE = ROOT / "docs/research/ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-R1.json"
ZIWEI_MINGJINGGE_SNU_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M.md"
ZIWEI_MINGJINGGE_SNU_EVIDENCE = ROOT / "docs/research/ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-R1.json"
ZIWEI_MINGJINGGE_HANYANG_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N.md"
ZIWEI_MINGJINGGE_HANYANG_EVIDENCE = ROOT / "docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json"
ZIWEI_KOREA_UNIVERSITY_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-O.md"
ZIWEI_KOREA_UNIVERSITY_EVIDENCE = ROOT / "docs/research/ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-R1.json"
ZIWEI_WEIJINGTANG_HANAUCTION_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-P.md"
ZIWEI_WEIJINGTANG_HANAUCTION_EVIDENCE = ROOT / "docs/research/ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json"
ZIWEI_KOSTMA_SCRIBD_FOZHU_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-Q.md"
ZIWEI_KOSTMA_SCRIBD_FOZHU_EVIDENCE = ROOT / "docs/research/ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-R1.json"
ZIWEI_TOYO_DETAIL_PROVENANCE_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R.md"
ZIWEI_TOYO_DETAIL_PROVENANCE_EVIDENCE = ROOT / "docs/research/ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R1.json"
ZIWEI_TOYO_MEDIA_REPOSITORY_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S.md"
ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE = ROOT / "docs/research/ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-R1.json"
ZIWEI_NAIKAKU_LINEAGE_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-T.md"
ZIWEI_NAIKAKU_LINEAGE_EVIDENCE = ROOT / "docs/research/ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-R1.json"
ZIWEI_NAIKAKU_1971_CATALOG_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-U.md"
ZIWEI_NAIKAKU_1971_CATALOG_EVIDENCE = ROOT / "docs/research/ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-R1.json"
ZIWEI_NAIKAKU_1971_PAGE_BOUNDARY_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-V.md"
ZIWEI_NAIKAKU_1971_PAGE_BOUNDARY_EVIDENCE = ROOT / "docs/research/ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-R1.json"
ZIWEI_SNU_QUARK_FOZHU_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-W.md"
ZIWEI_SNU_QUARK_FOZHU_EVIDENCE = ROOT / "docs/research/ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-R1.json"
ZIWEI_JIWEN_DAYUAN_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-X.md"
ZIWEI_JIWEN_DAYUAN_EVIDENCE = ROOT / "docs/research/ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-R1.json"
ZIWEI_NCC_JIWEN_DAYUAN_REVIEW_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-NCC-JIWEN-DAYUAN-DIRECT-SAMPLE-REVIEW-AND-KAMO-ACCESS-CONTROL-Y.md"
ZIWEI_NCC_JIWEN_DAYUAN_REVIEW_EVIDENCE = ROOT / "docs/research/ZIWEI-NCC-JIWEN-DAYUAN-PUBLIC-SAMPLE-VISUAL-REVIEW-R1.json"
ZIWEI_KAMO_ACCESS_EVIDENCE = ROOT / "docs/research/ZIWEI-KAMO-4174-03-04-PUBLIC-ROUTE-ACCESS-CONTROL-R1.json"
ZIWEI_KOREA_CNTS_LATE_ZI_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-Z.md"
ZIWEI_KOREA_CNTS_LATE_ZI_EVIDENCE = ROOT / "docs/research/ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-R1.json"

ZIWEI_HUIXIAN_CATALOG_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-HUIXIAN-MUSEUM-OFFICIAL-ILLUSTRATED-CATALOG-ROUTE-AA.md"
ZIWEI_HUIXIAN_CATALOG_EVIDENCE = ROOT / "docs/research/ZIWEI-HUIXIAN-MUSEUM-OFFICIAL-ILLUSTRATED-CATALOG-ROUTE-R1.json"
ZIWEI_JINGSHUTANG_ARTRON_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-AB.md"
ZIWEI_JINGSHUTANG_ARTRON_EVIDENCE = ROOT / "docs/research/ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-R1.json"
ZIWEI_WENGUANG_PT165_RESPONSE_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-AC.md"
ZIWEI_WENGUANG_PT165_RESPONSE_EVIDENCE = ROOT / "docs/research/ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-R1.json"
ZIWEI_SANFENGE_QUARK_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD.md"
ZIWEI_SANFENGE_QUARK_EVIDENCE = ROOT / "docs/research/ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-R1.json"
ZIWEI_REPUBLIC_ROUTES_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-AE.md"
ZIWEI_REPUBLIC_ROUTES_EVIDENCE = ROOT / "docs/research/ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-R1.json"
ZIWEI_YULGOK_GUANGYI_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-AF.md"
ZIWEI_YULGOK_GUANGYI_EVIDENCE = ROOT / "docs/research/ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-R1.json"
ZIWEI_JIAOJINGSHANFANG_HANAUCTION_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-AG.md"
ZIWEI_JIAOJINGSHANFANG_HANAUCTION_EVIDENCE = ROOT / "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json"
ZIWEI_JIAOJINGSHANFANG_DETAIL_PHOTO_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-AH.md"
ZIWEI_JIAOJINGSHANFANG_DETAIL_PHOTO_EVIDENCE = ROOT / "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-R1.json"
ZIWEI_LATE_ZI_TIME_COORDINATE_AI_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-AI.md"
ZIWEI_LATE_ZI_TIME_COORDINATE_AI_EVIDENCE = ROOT / "docs/research/ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json"
ZIWEI_FULLBOOK_LUOJING_AJ_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-AJ.md"
ZIWEI_FULLBOOK_LUOJING_AJ_EVIDENCE = ROOT / "docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json"
ZIWEI_GAOHOU_MENGQIU_AK_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-AK.md"
ZIWEI_GAOHOU_MENGQIU_AK_EVIDENCE = ROOT / "docs/research/ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-R1.json"
ZIWEI_KOREA_CNTS_AL_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-AL.md"
ZIWEI_KOREA_CNTS_AL_EVIDENCE = ROOT / "docs/research/ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-R1.json"
ZIWEI_RENZI_XUZHI_AM_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-AM.md"
ZIWEI_RENZI_XUZHI_AM_EVIDENCE = ROOT / "docs/research/ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-R1.json"
ZIWEI_WANXIAOLU_AN_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-WANXIAOLU-TIME-MOUNTAIN-BRIDGE-AN.md"
ZIWEI_WANXIAOLU_AN_EVIDENCE = ROOT / "docs/research/ZIWEI-WANXIAOLU-TIME-MOUNTAIN-BRIDGE-R1.json"
ZIWEI_JIELAN_AO_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-AO.md"
ZIWEI_JIELAN_AO_EVIDENCE = ROOT / "docs/research/ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-R1.json"
ZIWEI_JIELAN_AP_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-AP.md"
ZIWEI_JIELAN_AP_EVIDENCE = ROOT / "docs/research/ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-R1.json"
ZIWEI_JIELAN_AQ_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-AQ.md"
ZIWEI_JIELAN_AQ_EVIDENCE = ROOT / "docs/research/ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-R1.json"
ZIWEI_JIELAN_AR_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-AR.md"
ZIWEI_JIELAN_AR_EVIDENCE = ROOT / "docs/research/ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-R1.json"
ZIWEI_TUSHUBIAN_AS_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-TUSHUBIAN-1613-TIMEKEEPING-RECENSION-MAPPING-AS.md"
ZIWEI_TUSHUBIAN_AS_EVIDENCE = ROOT / "docs/research/ZIWEI-TUSHUBIAN-1613-TIMEKEEPING-RECENSION-MAPPING-R1.json"
ZIWEI_SANMING_AT_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANMING-TONGHUI-1578-TIMEKEEPING-PHYSICAL-COLLATION-AT.md"
ZIWEI_SANMING_AT_EVIDENCE = ROOT / "docs/research/ZIWEI-SANMING-TONGHUI-1578-TIMEKEEPING-PHYSICAL-COLLATION-R1.json"
ZIWEI_SANCAI_AU_BATCH = ROOT / "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANCAI-1697-NIGHT-ZI-HAI-CONTROVERSY-AU.md"
ZIWEI_SANCAI_AU_EVIDENCE = ROOT / "docs/research/ZIWEI-SANCAI-1697-NIGHT-ZI-HAI-CONTROVERSY-R1.json"

EXPECTED_BRANCH = "agent/fusion-chart-core-r1-20260822"
EXPECTED_S00_S19_STATUS = "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY"
SUPPLEMENTAL_BATCH_IDS = [
    "BATCH-11-BAZI-G893-1912-1920-PRECIOUS-CATALOG-T",
    "BATCH-11-BAZI-G893-1940-PRECIOUS-CATALOG-U",
    "BATCH-11-BAZI-G893-MF-PDF-ROUTE-V",
    "BATCH-11-BAZI-G893-LEE-JING-1998-OFFICIAL-ARCHIVE-W",
    "BATCH-11-BAZI-G893-OFFICIAL-REPRODUCTION-ROUTE-X",
    "BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A",
    "BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B",
    "BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C",
    "BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D",
    "BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E",
    "BATCH-12-ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-F",
    "BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G",
    "BATCH-12-ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-H",
    "BATCH-12-ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-I",
    "BATCH-12-ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-J",
    "BATCH-12-ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-K",
    "BATCH-12-ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-L",
    "BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M",
    "BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N",
    "BATCH-12-ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-O",
    "BATCH-12-ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-P",
    "BATCH-12-ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-Q",
    "BATCH-12-ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R",
    "BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S",
    "BATCH-12-ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-T",
    "BATCH-12-ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-U",
    "BATCH-12-ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-V",
    "BATCH-12-ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-W",
    "BATCH-12-ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-X",
    "BATCH-12-ZIWEI-NCC-JIWEN-DAYUAN-DIRECT-SAMPLE-REVIEW-AND-KAMO-ACCESS-CONTROL-Y",
    "BATCH-12-ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-Z",
    "BATCH-12-ZIWEI-HUIXIAN-MUSEUM-OFFICIAL-ILLUSTRATED-CATALOG-ROUTE-AA",
    "BATCH-12-ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-AB",
    "BATCH-12-ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-AC",
    "BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD",
    "BATCH-12-ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-AE",
    "BATCH-12-ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-AF",
    "BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-AG",
    "BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-AH",
    "BATCH-12-ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-AI",
    "BATCH-12-ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-AJ",
    "BATCH-12-ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-AK",
    "BATCH-12-ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-AL",
    "BATCH-12-ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-AM",
    "BATCH-12-ZIWEI-WANXIAOLU-TIME-MOUNTAIN-BRIDGE-AN",
    "BATCH-12-ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-AO",
    "BATCH-12-ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-AP",
    "BATCH-12-ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-AQ",
    "BATCH-12-ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-AR",
    "BATCH-12-ZIWEI-TUSHUBIAN-1613-TIMEKEEPING-RECENSION-MAPPING-AS",
    "BATCH-12-ZIWEI-SANMING-TONGHUI-1578-TIMEKEEPING-PHYSICAL-COLLATION-AT",
    "BATCH-12-ZIWEI-SANCAI-1697-NIGHT-ZI-HAI-CONTROVERSY-AU",
]
LATEST_BATCH_ID = SUPPLEMENTAL_BATCH_IDS[-1]
LATEST_BATCH_DOC = "docs/FUSION-CHART-HISTORICAL-PROVENANCE-AUDIT-BATCH-12-ZIWEI-SANCAI-1697-NIGHT-ZI-HAI-CONTROVERSY-AU.md"


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    for path in (ZIWEI_SANCAI_AU_BATCH, ZIWEI_SANCAI_AU_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AU continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_SANMING_AT_BATCH, ZIWEI_SANMING_AT_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AT continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_TUSHUBIAN_AS_BATCH, ZIWEI_TUSHUBIAN_AS_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AS continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_JIELAN_AR_BATCH, ZIWEI_JIELAN_AR_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AR continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_JIELAN_AQ_BATCH, ZIWEI_JIELAN_AQ_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AQ continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_JIELAN_AP_BATCH, ZIWEI_JIELAN_AP_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AP continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_JIELAN_AO_BATCH, ZIWEI_JIELAN_AO_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AO continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_WANXIAOLU_AN_BATCH, ZIWEI_WANXIAOLU_AN_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AN continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_RENZI_XUZHI_AM_BATCH, ZIWEI_RENZI_XUZHI_AM_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AM continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_KOREA_CNTS_AL_BATCH, ZIWEI_KOREA_CNTS_AL_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AL continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_GAOHOU_MENGQIU_AK_BATCH, ZIWEI_GAOHOU_MENGQIU_AK_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AK continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_FULLBOOK_LUOJING_AJ_BATCH, ZIWEI_FULLBOOK_LUOJING_AJ_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AJ continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_LATE_ZI_TIME_COORDINATE_AI_BATCH, ZIWEI_LATE_ZI_TIME_COORDINATE_AI_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AI continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (ZIWEI_JIAOJINGSHANFANG_DETAIL_PHOTO_BATCH, ZIWEI_JIAOJINGSHANFANG_DETAIL_PHOTO_EVIDENCE):
        if not path.is_file():
            fail(f"Batch 12AH continuity artifact missing: {path.relative_to(ROOT)}")

    for path in (STATE, PROTOCOL, AUTHORITY, MATRIX, SOURCE_REGISTRY, IDENTITY_BATCH, IDENTITY_MACHINE_EVIDENCE, MF_PDF_BATCH, MF_PDF_MACHINE_EVIDENCE, ARTICLE_BATCH, ARTICLE_MACHINE_EVIDENCE, LATEST_BATCH, LATEST_MACHINE_EVIDENCE, ZIWEI_LATE_ZI_BATCH, ZIWEI_LATE_ZI_EVIDENCE, ZIWEI_TIMEKEEPING_BATCH, ZIWEI_TIMEKEEPING_EVIDENCE, ZIWEI_EDITION_ROUTES_BATCH, ZIWEI_EDITION_ROUTES_EVIDENCE, ZIWEI_WENGUANG_INDEX_BATCH, ZIWEI_WENGUANG_INDEX_EVIDENCE, ZIWEI_JINGLUNTANG_BATCH, ZIWEI_JINGLUNTANG_EVIDENCE, ZIWEI_POST_E_ROUTES_BATCH, ZIWEI_POST_E_ROUTES_EVIDENCE, ZIWEI_QUANJI_LATE_ZI_BATCH, ZIWEI_QUANJI_LATE_ZI_EVIDENCE, ZIWEI_JAPAN_MING_FULLBOOK_BATCH, ZIWEI_JAPAN_MING_FULLBOOK_EVIDENCE, ZIWEI_LATE_ZI_DEDUP_LOCATOR_BATCH, ZIWEI_LATE_ZI_DEDUP_LOCATOR_EVIDENCE, ZIWEI_GUANGYI_PHYSICAL_SET_BATCH, ZIWEI_GUANGYI_PHYSICAL_SET_EVIDENCE, ZIWEI_WENGUANG_BASE_COPY_BATCH, ZIWEI_WENGUANG_BASE_COPY_EVIDENCE, ZIWEI_KANGJIE_TYPESET_BATCH, ZIWEI_KANGJIE_TYPESET_EVIDENCE, ZIWEI_MINGJINGGE_SNU_BATCH, ZIWEI_MINGJINGGE_SNU_EVIDENCE, ZIWEI_MINGJINGGE_HANYANG_BATCH, ZIWEI_MINGJINGGE_HANYANG_EVIDENCE, ZIWEI_KOREA_UNIVERSITY_BATCH, ZIWEI_KOREA_UNIVERSITY_EVIDENCE, ZIWEI_WEIJINGTANG_HANAUCTION_BATCH, ZIWEI_WEIJINGTANG_HANAUCTION_EVIDENCE, ZIWEI_KOSTMA_SCRIBD_FOZHU_BATCH, ZIWEI_KOSTMA_SCRIBD_FOZHU_EVIDENCE, ZIWEI_TOYO_DETAIL_PROVENANCE_BATCH, ZIWEI_TOYO_DETAIL_PROVENANCE_EVIDENCE, ZIWEI_TOYO_MEDIA_REPOSITORY_BATCH, ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE, ZIWEI_NAIKAKU_LINEAGE_BATCH, ZIWEI_NAIKAKU_LINEAGE_EVIDENCE, ZIWEI_NAIKAKU_1971_CATALOG_BATCH, ZIWEI_NAIKAKU_1971_CATALOG_EVIDENCE, ZIWEI_NAIKAKU_1971_PAGE_BOUNDARY_BATCH, ZIWEI_NAIKAKU_1971_PAGE_BOUNDARY_EVIDENCE, ZIWEI_SNU_QUARK_FOZHU_BATCH, ZIWEI_SNU_QUARK_FOZHU_EVIDENCE, ZIWEI_JIWEN_DAYUAN_BATCH, ZIWEI_JIWEN_DAYUAN_EVIDENCE, ZIWEI_NCC_JIWEN_DAYUAN_REVIEW_BATCH, ZIWEI_NCC_JIWEN_DAYUAN_REVIEW_EVIDENCE, ZIWEI_KAMO_ACCESS_EVIDENCE, ZIWEI_KOREA_CNTS_LATE_ZI_BATCH, ZIWEI_KOREA_CNTS_LATE_ZI_EVIDENCE):
        if not path.is_file():
            fail(f"continuity artifact missing: {path.relative_to(ROOT)}")

    state = json.loads(STATE.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    registry = json.loads(SOURCE_REGISTRY.read_text(encoding="utf-8"))
    identity_evidence = json.loads(IDENTITY_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    mf_pdf_evidence = json.loads(MF_PDF_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    article_evidence = json.loads(ARTICLE_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    evidence = json.loads(LATEST_MACHINE_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_late_zi_evidence = json.loads(ZIWEI_LATE_ZI_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_timekeeping_evidence = json.loads(ZIWEI_TIMEKEEPING_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_edition_routes_evidence = json.loads(ZIWEI_EDITION_ROUTES_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_wenguang_index_evidence = json.loads(ZIWEI_WENGUANG_INDEX_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jingluntang_evidence = json.loads(ZIWEI_JINGLUNTANG_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_post_e_routes_evidence = json.loads(ZIWEI_POST_E_ROUTES_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_quanji_late_zi_evidence = json.loads(ZIWEI_QUANJI_LATE_ZI_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_japan_ming_fullbook_evidence = json.loads(ZIWEI_JAPAN_MING_FULLBOOK_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_late_zi_dedup_locator_evidence = json.loads(ZIWEI_LATE_ZI_DEDUP_LOCATOR_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_guangyi_physical_set_evidence = json.loads(ZIWEI_GUANGYI_PHYSICAL_SET_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_wenguang_base_copy_evidence = json.loads(ZIWEI_WENGUANG_BASE_COPY_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_kangjie_typeset_evidence = json.loads(ZIWEI_KANGJIE_TYPESET_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_mingjingge_snu_evidence = json.loads(ZIWEI_MINGJINGGE_SNU_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_mingjingge_hanyang_evidence = json.loads(ZIWEI_MINGJINGGE_HANYANG_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_korea_university_evidence = json.loads(ZIWEI_KOREA_UNIVERSITY_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_weijingtang_hanauction_evidence = json.loads(ZIWEI_WEIJINGTANG_HANAUCTION_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_kostma_scribd_fozhu_evidence = json.loads(ZIWEI_KOSTMA_SCRIBD_FOZHU_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_toyo_detail_provenance_evidence = json.loads(ZIWEI_TOYO_DETAIL_PROVENANCE_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_toyo_media_repository_evidence = json.loads(ZIWEI_TOYO_MEDIA_REPOSITORY_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_naikaku_lineage_evidence = json.loads(ZIWEI_NAIKAKU_LINEAGE_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_naikaku_1971_catalog_evidence = json.loads(ZIWEI_NAIKAKU_1971_CATALOG_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_naikaku_1971_page_boundary_evidence = json.loads(ZIWEI_NAIKAKU_1971_PAGE_BOUNDARY_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_snu_quark_fozhu_evidence = json.loads(ZIWEI_SNU_QUARK_FOZHU_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jiwen_dayuan_evidence = json.loads(ZIWEI_JIWEN_DAYUAN_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_ncc_jiwen_dayuan_review_evidence = json.loads(ZIWEI_NCC_JIWEN_DAYUAN_REVIEW_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_kamo_access_evidence = json.loads(ZIWEI_KAMO_ACCESS_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_korea_cnts_late_zi_evidence = json.loads(ZIWEI_KOREA_CNTS_LATE_ZI_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_huixian_catalog_evidence = json.loads(ZIWEI_HUIXIAN_CATALOG_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jingshutang_artron_evidence = json.loads(ZIWEI_JINGSHUTANG_ARTRON_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_wenguang_pt165_response_evidence = json.loads(ZIWEI_WENGUANG_PT165_RESPONSE_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_sanfenge_quark_evidence = json.loads(ZIWEI_SANFENGE_QUARK_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_republic_routes_evidence = json.loads(ZIWEI_REPUBLIC_ROUTES_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_yulgok_guangyi_evidence = json.loads(ZIWEI_YULGOK_GUANGYI_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jiaojingshanfang_hanauction_evidence = json.loads(ZIWEI_JIAOJINGSHANFANG_HANAUCTION_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jiaojingshanfang_detail_photo_evidence = json.loads(ZIWEI_JIAOJINGSHANFANG_DETAIL_PHOTO_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_late_zi_time_coordinate_ai_evidence = json.loads(ZIWEI_LATE_ZI_TIME_COORDINATE_AI_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_fullbook_luojing_aj_evidence = json.loads(ZIWEI_FULLBOOK_LUOJING_AJ_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_gaohou_mengqiu_ak_evidence = json.loads(ZIWEI_GAOHOU_MENGQIU_AK_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_korea_cnts_al_evidence = json.loads(ZIWEI_KOREA_CNTS_AL_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_renzi_xuzhi_am_evidence = json.loads(ZIWEI_RENZI_XUZHI_AM_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_wanxiaolu_an_evidence = json.loads(ZIWEI_WANXIAOLU_AN_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jielan_ao_evidence = json.loads(ZIWEI_JIELAN_AO_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jielan_ap_evidence = json.loads(ZIWEI_JIELAN_AP_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jielan_aq_evidence = json.loads(ZIWEI_JIELAN_AQ_EVIDENCE.read_text(encoding="utf-8"))
    ziwei_jielan_ar_evidence = json.loads(ZIWEI_JIELAN_AR_EVIDENCE.read_text(encoding="utf-8"))

    if state.get("schema") != "ZIWEI-BAZI-PROJECT-CURRENT-STATE-R1":
        fail("project current-state schema mismatch")
    if state.get("development_branch") != EXPECTED_BRANCH:
        fail("project current-state branch mismatch")
    if state.get("github_remote_is_only_live_state_source") is not True:
        fail("GitHub live remote is not declared as the only live state source")
    if state.get("embedded_commit_sha_is_authoritative") is not False:
        fail("current-state file must not treat an embedded SHA as authoritative")
    if state.get("startup_requires_live_remote_refresh") is not True:
        fail("new-chat startup must require live remote refresh")

    authority = state.get("source_authority_policy", {})
    required_authority = {
        "s00_s19_status": EXPECTED_S00_S19_STATUS,
        "canonical_path_semantics": "LEGACY_STORAGE_AND_FREEZE_IDENTITY_NOT_EPISTEMIC_TRUTH",
        "modern_software_status": "COMPATIBILITY_WITNESS_ONLY",
        "philology_required": True,
        "terminology_normalization_policy": "CONTEXTUAL_PHILOLOGY_BEFORE_MECHANICAL_RULE_IDENTITY",
        "homonym_policy": "SAME_NAME_DOES_NOT_IMPLY_SAME_RULE_OR_SYSTEM",
        "research_scope_policy": "OPEN_ENDED_CROSS_EDITION_CROSS_REGION_CROSS_LANGUAGE_CROSS_DISCIPLINE",
        "first_source_stop_policy": "FORBIDDEN_WHEN_MATERIAL_ADDITIONAL_WITNESSES_ARE_SEARCHABLE",
    }
    for key, expected in required_authority.items():
        if authority.get(key) != expected:
            fail(f"research authority policy regressed for {key}")
    if "EVIDENCE_WEIGHTED_NOT_SOURCE_COUNT" not in authority.get("conflict_adjudication_policy", ""):
        fail("evidence-weighted conflict adjudication policy regressed")
    if "DO_NOT_FALSELY_EQUALIZE_DEMONSTRATED_TRANSMISSION_ERRORS" not in authority.get("candidate_preservation_policy", ""):
        fail("false-equivalence prohibition regressed")

    if "PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY" not in matrix.get("canonical_source_policy", ""):
        fail("historical matrix still treats S00-S19 as unquestioned authority")
    if matrix.get("research_authority_policy_doc") != "docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md":
        fail("historical matrix is not bound to research authority policy")
    if "not infallible historical authority" not in registry.get("authority_policy", ""):
        fail("external source registry authority policy regressed")
    if registry.get("research_authority_policy_doc") != "docs/FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md":
        fail("external source registry is not bound to research authority policy")

    source_ids = {item.get("source_id") for item in registry.get("sources", ())}
    required_sources = (
        "EXT-NDL-OGAWA-SHOUSHI-LICHENG-1673",
        "EXT-KYUSHU-OGAWA-SHOUSHI-LICHENG-1673",
        "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893",
        "EXT-LI-LIANG-SUNRISE-TABLES-2022",
        "EXT-KYUJANGGAK-CHILJEONGSAN-NAEPYEON-G894-1444",
        "EXT-NIKH-SEJONG-SILLOK-V156-CHILJEONGSAN-TABLES",
        "EXT-NIKH-CHILJEONGSAN-HISTORY-1444",
        "EXT-KYUJANGGAK-PRECIOUS-BOOK-RELATIONS-1940",
        "EXT-GOOGLE-BOOKS-JIELAN-WENCHENGTANG-COLLATION-INDEX",
        "EXT-DESTINYNET-ZWDSQJ-LATE-ZI-RECEIVED-TRANSCRIPTION",
        "EXT-TOYO-BUNKO-ZWDSQJ-VII-3-157",
        "EXT-NCKU-CHEN-2021-ZIWEI-EDITION-GENEALOGY",
        "EXT-SDU-ZIHAI-NAIKAKU-ZWDSQS-FACSIMILE",
        "EXT-NAJ-ZWDSQS-MING-1078787",
        "EXT-GOOGLE-BOOKS-JIELAN-LIANYUANGE-QUANJI-INDEX",
        "EXT-XINYITANG-JIELAN-LIANYUANGE-QUANJI-COLLATION",
        "EXT-DALIAN-LIB-ZWDSQS-GUANGYI-MINGUO",
        "EXT-GUOXUEDASHI-ZWDSQS-WENCHENGTANG-LIAONING-LOCATOR",
        "EXT-NANKAI-LNLIB-GUJI-LEGACY-ROUTE",
        "EXT-GOOGLE-BOOKS-ZIHAI-ZWDSQS-STANDALONE-2016",
        "EXT-GOOGLE-BOOKS-PAN-ZWDSQS-GUJUE-BIANZHENG-2017",
        "EXT-SHUGE-ZWDSQS-NAIKAKU-PUBLIC-FACSIMILE-ROUTE",
        "EXT-YETNAL-ZWDSQS-GUANGYI-PHYSICAL-SET",
        "EXT-SANMIN-ZWDSQS-WENGUANG-PUBLIC-SAMPLES-2017",
        "EXT-XUELIN-KANGJIE-ZIWEI-MODERN-TYPESET",
        "EXT-SNU-ILSA-MINGJINGGE-ZWDSQJ-DIGITIZATION-DERIVATIVE",
        "EXT-AKS-SILLOKWIKI-HANYANG-MINGJINGGE-ZWDSQJ-HOLDING",
        "EXT-KOREA-NLK-CNTS-00047996572-ZIWEIDOUSHUFANGSHU",
        "EXT-SANFENGE-ZWDSQS-V4-QUARK-PUBLIC-SHARE",
        "EXT-KONGFZ-HUIWENTANG-REPUBLIC-ZWDSQS-PHYSICAL",
        "EXT-SHUCANG-JINZHANG-REPUBLIC-ZWDSQS-CATALOG",
        "EXT-XINYI-JINYUAN-ZWDSQS-MODERN-TOC",
        "EXT-YULGOK-B005-B00320-GUANGYI-ZWDSQS",
        "EXT-HANAUCTION-JIAOJINGSHANFANG-ZWDSQS-PHYSICAL",
        "EXT-CTEXT-MINGSHI-ASTRONOMY-DINGSHI-SOLAR-STELLAR",
        "EXT-SHIDIAN-SIKU-LUOJING-DINGMENZHEN-CATALOG",
        "EXT-SHIDIAN-XU-ZHIMO-LUOJING-DINGMENZHEN-MING",
        "EXT-CTEXT-HUANGMING-JINGSHI-WENBIAN-V493-DINGSHI-LUOJING",
        "EXT-SHIDIAN-XINFA-SUANSHU-V1-DINGSHI-LUOJING",
        "EXT-CTEXT-GAOHOU-MENGQIU-OCR",
        "EXT-SHIDIAN-GAOHOU-MENGQIU-V3",
        "EXT-WASEDA-GAOHOU-MENGQIU-1807-1809",
        "EXT-CINII-BB17866565-RENZI-XUZHI-1583",
        "EXT-COMMONS-GGZBCK411-RENZI-XUZHI-1569-1583",
        "EXT-CTEXT-RENZI-XUZHI-ZHENGZHEN-FENGZHEN",
        "EXT-CTEXT-WANXIAOLU-DINGSHI-RESOURCE437415",
        "EXT-SHIDIAN-WANLIXUDAOZANG-WANXIAOLU-DINGSHI",
    )
    for source_id in required_sources:
        if source_id not in source_ids:
            fail(f"required continuity source witness missing: {source_id}")

    # Batch 12AD Sanfenge provider/share route: locator closure only, zero textual votes.
    if not ZIWEI_SANFENGE_QUARK_BATCH.is_file() or not ZIWEI_SANFENGE_QUARK_EVIDENCE.is_file():
        fail("Batch 12AD continuity artifacts missing")
    if ziwei_sanfenge_quark_evidence.get("batch_id") != "BATCH-12-ZIWEI-SANFENGE-QUARK-VOLUME4-PUBLIC-SHARE-ROUTE-AD":
        fail("Batch 12AD evidence identity mismatch")
    p12ad = ziwei_sanfenge_quark_evidence.get("sanfenge_provider_page", {})
    records12ad = {r.get("article_id"): r for r in p12ad.get("direct_provider_records", ())}
    if records12ad.get(212163, {}).get("source_emitted_public_share") != "https://pan.quark.cn/s/6956a639be12":
        fail("Batch 12AD volume-four provider/share binding regressed")
    if records12ad.get(212173, {}).get("source_emitted_public_share") != "https://pan.quark.cn/s/9f7f6a4e7730":
        fail("Batch 12AD four-volume provider/share binding regressed")
    q12ad = ziwei_sanfenge_quark_evidence.get("quark_public_share_probe", {})
    if q12ad.get("volume4_share", {}).get("direct_pdf_bytes_observed") is not False:
        fail("Batch 12AD public-share byte boundary regressed")
    a12ad = ziwei_sanfenge_quark_evidence.get("adjudication", {})
    if a12ad.get("independent_textual_witness_increment") != 0 or a12ad.get("independent_hai_glyph_witness_increment") != 0 or a12ad.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AD witness/algorithm firewall regressed")
    row12ad = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ad or row12ad.get("sanfenge_volume4_article_id") != 212163 or row12ad.get("independent_hai_glyph_witness_count_added_batch_12ad") != 0:
        fail("Batch 12AD Matrix binding regressed")

    # Batch 12AE Republic Huiwentang/Jinzhang routes: edition identity only, zero target votes.
    if not ZIWEI_REPUBLIC_ROUTES_BATCH.is_file() or not ZIWEI_REPUBLIC_ROUTES_EVIDENCE.is_file():
        fail("Batch 12AE continuity artifacts missing")
    if ziwei_republic_routes_evidence.get("batch_id") != "BATCH-12-ZIWEI-REPUBLIC-HUIWENTANG-JINZHANG-ROUTES-AE":
        fail("Batch 12AE evidence identity mismatch")
    h12ae = ziwei_republic_routes_evidence.get("huiwentang_kongfz", {})
    if h12ae.get("direct_physical_title_image", {}).get("sha256") != "767f5d01986c8f4a2b655699fce7af50917afd76a34e321ecf8254e6e09a0e9a":
        fail("Batch 12AE Huiwentang physical-image binding regressed")
    if "上海會文堂書局印行" not in h12ae.get("direct_physical_title_image", {}).get("direct_no_ocr_reading", []):
        fail("Batch 12AE Huiwentang imprint reading regressed")
    j12ae = ziwei_republic_routes_evidence.get("jinzhang_routes", {}).get("shucang_catalog", {})
    if j12ae.get("volume") != 59 or j12ae.get("start_page") != 333:
        fail("Batch 12AE Jinzhang Shucang catalog binding regressed")
    a12ae = ziwei_republic_routes_evidence.get("adjudication", {})
    if a12ae.get("independent_target_text_witness_increment") != 0 or a12ae.get("independent_hai_glyph_witness_increment") != 0 or a12ae.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AE witness/algorithm firewall regressed")
    row12ae = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ae or row12ae.get("huiwentang_physical_imprint_direct_reading") != "上海會文堂書局印行" or row12ae.get("independent_hai_glyph_witness_count_added_batch_12ae") != 0:
        fail("Batch 12AE Matrix binding regressed")

    # Batch 12AF Guangyi/Yulgok direct target collation: second direct Fullbook physical Hai witness, no algorithm reopen.
    if not ZIWEI_YULGOK_GUANGYI_BATCH.is_file() or not ZIWEI_YULGOK_GUANGYI_EVIDENCE.is_file():
        fail("Batch 12AF continuity artifacts missing")
    if ziwei_yulgok_guangyi_evidence.get("batch_id") != "BATCH-12-ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-AF":
        fail("Batch 12AF evidence identity mismatch")
    tree12af = ziwei_yulgok_guangyi_evidence.get("source_emitted_tree_binding", {})
    if tree12af.get("workflow_run_id") != 34315414878 or tree12af.get("artifact_id") != 10089871530:
        fail("Batch 12AF source-tree execution binding regressed")
    if tree12af.get("exact_data_ids") != ["B005_01_B00320_001", "B005_01_B00320_002", "B005_01_B00320_003", "B005_01_B00320_004"]:
        fail("Batch 12AF exact four-book dataId binding regressed")
    cap12af = ziwei_yulgok_guangyi_evidence.get("four_volume_manifest_capture", {})
    if cap12af.get("artifact_id") != 10089901168 or cap12af.get("total_source_manifest_images") != 19 or cap12af.get("all_manifest_images_fetched") is not True:
        fail("Batch 12AF four-volume manifest capture regressed")
    imp12af = ziwei_yulgok_guangyi_evidence.get("direct_physical_imprint_no_ocr", {})
    if imp12af.get("image_sha256") != "2a714616b5d4a33642003658516fc7d109b1f33a13892ff93604f07ab38ddf67" or imp12af.get("publisher_imprint") != "上海廣益書局印行":
        fail("Batch 12AF Guangyi imprint binding regressed")
    if imp12af.get("direct_ocr_used") is not False:
        fail("Batch 12AF imprint no-OCR boundary regressed")
    target12af = ziwei_yulgok_guangyi_evidence.get("direct_target_leaf_no_ocr", {})
    if target12af.get("image_sha256") != "2d1fc5ce8459d3696166b0471b2075fee247ede94b73eb833d435fe54ee847e0":
        fail("Batch 12AF target image digest regressed")
    if target12af.get("visible_juan") != 3 or target12af.get("target_heading") != "論人生時要審的確":
        fail("Batch 12AF target location binding regressed")
    if target12af.get("decisive_direct_reading") != "如子時有十刻上五刻屬昨夜亥時下五刻屬今日子時":
        fail("Batch 12AF decisive direct reading regressed")
    if target12af.get("explicit_previous_night_hai_phrase") != "昨夜亥時" or target12af.get("explicit_current_day_zi_phrase") != "今日子時":
        fail("Batch 12AF direct Hai/Zi phrase binding regressed")
    if target12af.get("direct_ocr_used") is not False:
        fail("Batch 12AF target no-OCR boundary regressed")
    indep12af = ziwei_yulgok_guangyi_evidence.get("evidence_independence", {})
    if indep12af.get("direct_fullbook_physical_target_text_witness_increment") != 1 or indep12af.get("independent_hai_glyph_witness_increment") != 1:
        fail("Batch 12AF physical/Hai witness accounting regressed")
    if indep12af.get("stemmatically_independent_branch_increment") != 0:
        fail("Batch 12AF stemmatic-independence firewall regressed")
    ad12af = ziwei_yulgok_guangyi_evidence.get("adjudication", {})
    if ad12af.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or ad12af.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AF HPA/algorithm firewall regressed")
    if ad12af.get("within_fullbook_hai_glyph_stability") != "CONFIRMED_ACROSS_NANYANGTANG_AND_GUANGYI_DIRECT_PHYSICAL_EDITIONS":
        fail("Batch 12AF cross-edition agreement binding regressed")
    if ad12af.get("global_all_fullbook_edition_stability") != "NOT_CLAIMED":
        fail("Batch 12AF global-stability firewall regressed")
    row12af = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12af or row12af.get("batch_12af_guangyi_yulgok_direct_collation_artifact") != "docs/research/ZIWEI-GUANGYI-YULGOK-DIRECT-LATE-ZI-COLLATION-R1.json":
        fail("Batch 12AF Matrix artifact binding regressed")
    if row12af.get("independent_hai_glyph_witness_count_added_batch_12af") != 1 or row12af.get("direct_fullbook_physical_target_text_witness_count_added_batch_12af") != 1:
        fail("Batch 12AF Matrix witness accounting regressed")
    src12af = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-YULGOK-B005-B00320-GUANGYI-ZWDSQS"), None)
    if not src12af or src12af.get("target_image_sha256") != "2d1fc5ce8459d3696166b0471b2075fee247ede94b73eb833d435fe54ee847e0":
        fail("Batch 12AF registry source/target binding regressed")
    if src12af.get("independent_hai_glyph_witness_increment") != 1 or src12af.get("stemmatic_independence_claimed") is not False:
        fail("Batch 12AF registry witness/stemma firewall regressed")


    # Batch 12AG Jiaojingshanfang/Hanauction: physical-edition locator only, target page not visually adjudicated.
    if not ZIWEI_JIAOJINGSHANFANG_HANAUCTION_BATCH.is_file() or not ZIWEI_JIAOJINGSHANFANG_HANAUCTION_EVIDENCE.is_file():
        fail("Batch 12AG continuity artifacts missing")
    if ziwei_jiaojingshanfang_hanauction_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-AG":
        fail("Batch 12AG evidence identity mismatch")
    probe12ag = ziwei_jiaojingshanfang_hanauction_evidence.get("controlling_probe", {})
    if probe12ag.get("workflow_run_id") != 34319318823 or probe12ag.get("artifact_id") != 10091275632:
        fail("Batch 12AG controlling probe binding regressed")
    if probe12ag.get("artifact_zip_sha256") != "c348dc9207c5932421e58ca0b01160827a5468a9b7160ba2f6e28e0aacfdfdf1":
        fail("Batch 12AG artifact digest regressed")
    routes12ag = {r.get("route_key"): r for r in ziwei_jiaojingshanfang_hanauction_evidence.get("public_auction_routes", ())}
    if routes12ag.get("HAN-227-127", {}).get("stable_object_id") != "101926":
        fail("Batch 12AG 2026 stable-object binding regressed")
    if routes12ag.get("HAN-65-173", {}).get("stable_object_id") != "27427":
        fail("Batch 12AG 2012 stable-object binding regressed")
    photos12ag = routes12ag.get("HAN-65-173", {}).get("source_emitted_exact_detail_photo_objects", ())
    if [p.get("sha256") for p in photos12ag] != [
        "c8705995aa695ba7ef285be939960bcef69516aed749937b00b309cf0df321c2",
        "a22d0017171dd0893019b551f9c986de3f89f6c16d2840260ffe8e3a3f685260",
    ]:
        fail("Batch 12AG exact-detail image identity regressed")
    if routes12ag.get("HAN-65-173", {}).get("source_emitted_detail_photos_direct_visual_review_completed") is not False:
        fail("Batch 12AG unreviewed-image firewall regressed")
    gene12ag = ziwei_jiaojingshanfang_hanauction_evidence.get("scholarly_genealogy_control", {})
    if gene12ag.get("source_id") != "EXT-NCKU-CHEN-2021-ZIWEI-EDITION-GENEALOGY" or gene12ag.get("stemmatic_independence_from_nanyangtang_or_guangyi") != "NOT_CLAIMED":
        fail("Batch 12AG scholarly genealogy/stemma firewall regressed")
    indep12ag = ziwei_jiaojingshanfang_hanauction_evidence.get("evidence_independence", {})
    if indep12ag.get("direct_target_text_witness_increment") != 0 or indep12ag.get("independent_hai_glyph_witness_increment") != 0 or indep12ag.get("stemmatically_independent_branch_increment") != 0:
        fail("Batch 12AG witness/stemma accounting regressed")
    ad12ag = ziwei_jiaojingshanfang_hanauction_evidence.get("adjudication", {})
    if ad12ag.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or ad12ag.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AG HPA/algorithm firewall regressed")
    if ad12ag.get("target_page_status") != "PENDING_DIRECT_VISUAL_TARGET_PAGE" or ad12ag.get("target_hai_glyph_status") != "NOT_OBSERVED":
        fail("Batch 12AG target-page/Hai boundary regressed")
    row12ag = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ag or row12ag.get("batch_12ag_jiaojingshanfang_hanauction_physical_edition_artifact") != "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json":
        fail("Batch 12AG Matrix artifact binding regressed")
    if row12ag.get("independent_textual_witness_count_added_batch_12ag") != 0 or row12ag.get("independent_hai_glyph_witness_count_added_batch_12ag") != 0:
        fail("Batch 12AG Matrix witness firewall regressed")
    src12ag = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-HANAUCTION-JIAOJINGSHANFANG-ZWDSQS-PHYSICAL"), None)
    if not src12ag or src12ag.get("direct_target_page_observed") is not False or src12ag.get("stemmatic_independence_claimed") is not False:
        fail("Batch 12AG registry authority/stemma boundary regressed")
    if src12ag.get("independent_target_text_witness_increment") != 0 or src12ag.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12AG registry witness accounting regressed")

    # Batch 12AH Jiaojingshanfang/Hanauction: direct media-scope correction.
    if ziwei_jiaojingshanfang_detail_photo_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-AH":
        fail("Batch 12AH evidence identity mismatch")
    src_archive12ah = ziwei_jiaojingshanfang_detail_photo_evidence.get("source_archive_binding", {})
    if src_archive12ah.get("workflow_run_id") != 34319318823 or src_archive12ah.get("artifact_id") != 10091275632:
        fail("Batch 12AH parent archive binding regressed")
    if src_archive12ah.get("artifact_zip_sha256") != "c348dc9207c5932421e58ca0b01160827a5468a9b7160ba2f6e28e0aacfdfdf1":
        fail("Batch 12AH parent artifact digest regressed")
    if src_archive12ah.get("artifact_member_browser_html_sha256") != "93e6d80fd3d65e58fccd81a683cdfcd013d1aff8eabadc934c7aca764d2fec65":
        fail("Batch 12AH browser HTML binding regressed")
    media12ah = ziwei_jiaojingshanfang_detail_photo_evidence.get("adjudicated_media", ())
    if [m.get("sha256") for m in media12ah] != [
        "c8705995aa695ba7ef285be939960bcef69516aed749937b00b309cf0df321c2",
        "a22d0017171dd0893019b551f9c986de3f89f6c16d2840260ffe8e3a3f685260",
    ]:
        fail("Batch 12AH media hash binding regressed")
    if any(m.get("target_object_specific") is not False or m.get("target_book_page") is not False for m in media12ah):
        fail("Batch 12AH target-object media firewall regressed")
    defect12ah = ziwei_jiaojingshanfang_detail_photo_evidence.get("provenance_defect", {})
    if defect12ah.get("defect_id") != "PROV-DEFECT-010" or defect12ah.get("repair_status") != "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AH":
        fail("Batch 12AH provenance defect repair binding regressed")
    effect12ah = ziwei_jiaojingshanfang_detail_photo_evidence.get("evidence_effect", {})
    if effect12ah.get("target_page_status") != "PENDING_DIRECT_VISUAL_TARGET_PAGE" or effect12ah.get("direct_target_text_witness_increment") != 0 or effect12ah.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12AH target-page/witness firewall regressed")
    row12ah = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ah or row12ah.get("batch_12ah_jiaojingshanfang_detail_photo_visual_adjudication_artifact") != "docs/research/ZIWEI-JIAOJINGSHANFANG-HANAUCTION-DETAIL-PHOTO-VISUAL-ADJUDICATION-R1.json":
        fail("Batch 12AH Matrix artifact binding regressed")
    if row12ah.get("defect_id") != "PROV-DEFECT-010" or row12ah.get("repair_status") != "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AH":
        fail("Batch 12AH Matrix provenance-defect repair regressed")
    if row12ah.get("jiaojingshanfang_2012_detail_photo_visual_review_status") != "DIRECTLY_REVIEWED_AND_RECLASSIFIED_AS_AUCTION_EVENT_MEDIA_NOT_TARGET_OBJECT":
        fail("Batch 12AH Matrix visual adjudication regressed")
    src12ah = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-HANAUCTION-JIAOJINGSHANFANG-ZWDSQS-PHYSICAL"), None)
    if not src12ah or src12ah.get("direct_visual_review_of_2012_detail_photos_completed") is not True:
        fail("Batch 12AH registry visual-review status regressed")
    if src12ah.get("media_scope_classification") != "AUCTION_ROUND_EVENT_SCENERY_VIDEO_THUMBNAILS_NOT_TARGET_OBJECT_PHOTOS":
        fail("Batch 12AH registry media-scope repair regressed")
    if src12ah.get("provenance_defect_id") != "PROV-DEFECT-010" or src12ah.get("provenance_defect_repair_status") != "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AH":
        fail("Batch 12AH registry provenance defect binding regressed")

    # Batch 12AI Ziwei late-Zi time-coordinate narrowing.
    if ziwei_late_zi_time_coordinate_ai_evidence.get("batch_id") != "BATCH-12-ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-AI":
        fail("Batch 12AI evidence identity mismatch")
    probe12ai = ziwei_late_zi_time_coordinate_ai_evidence.get("controlling_probe", {})
    if probe12ai.get("workflow_run_id") != 34322850489 or probe12ai.get("artifact_id") != 10092539912:
        fail("Batch 12AI controlling probe binding regressed")
    if probe12ai.get("artifact_zip_sha256") != "9e3151f558b6425586fc2e2c593f5a01f82529f42f6cbd7e8f3e3973fc6df98f":
        fail("Batch 12AI artifact digest regressed")
    witnesses12ai = {w.get("source_id"): w for w in ziwei_late_zi_time_coordinate_ai_evidence.get("witnesses", ())}
    if witnesses12ai.get("EXT-CTEXT-MINGSHI-ASTRONOMY-DINGSHI-SOLAR-STELLAR", {}).get("response_sha256") != "157eac2885f6bd3e6c72899f90539e4dd817cf63099c6e17508a8fc419293c16":
        fail("Batch 12AI Ming time-determination response binding regressed")
    if witnesses12ai.get("EXT-CTEXT-MINGSHI-ASTRONOMY-BEIJING-NANJING-CLOCK", {}).get("response_sha256") != "9c70e872519a96ff0bf034bb53a760538e574c99cbdb331b75457fb1c3405f7f":
        fail("Batch 12AI Ming geography response binding regressed")
    if witnesses12ai.get("EXT-USNO-EQUATION-OF-TIME", {}).get("response_sha256") != "ae81510e2c00f993413f0593c4706836c6635b57a4b2eac7e11b7de85deee768":
        fail("Batch 12AI USNO response binding regressed")
    phil12ai = ziwei_late_zi_time_coordinate_ai_evidence.get("philological_and_coordinate_adjudication", {})
    if phil12ai.get("normalized_mechanical_concept") != "LOCAL_OBSERVATIONAL_ASTRONOMICAL_TIME_COORDINATE":
        fail("Batch 12AI historical coordinate family regressed")
    if phil12ai.get("daytime_instrument_family") != "SUNDIAL_TRUE_SUN" or phil12ai.get("nighttime_instrument_family") != "STELLAR_TIME_READING_WITH_CLEPSYDRA_AS_SUPPLEMENT":
        fail("Batch 12AI day/night historical time basis regressed")
    if phil12ai.get("local_apparent_solar_time_status") != "STRONGEST_MODERN_TRANSLATION_OF_DAYTIME_SUNDIAL_READOUT_AT_A_LOCATION":
        fail("Batch 12AI apparent-solar translation boundary regressed")
    eff12ai = ziwei_late_zi_time_coordinate_ai_evidence.get("hpa_zdate_006_effect", {})
    if eff12ai.get("status") != "MISSING_FROM_PRODUCT" or eff12ai.get("runtime_time_standard_binding") != "PARTIALLY_NARROWED_NOT_CLOSED":
        fail("Batch 12AI HPA/runtime state regressed")
    if eff12ai.get("candidate_selected") is not False or eff12ai.get("candidate_collapsed") is not False or eff12ai.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AI candidate/algorithm firewall regressed")
    row12ai = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ai or row12ai.get("batch_12ai_ziwei_late_zi_time_coordinate_artifact") != "docs/research/ZIWEI-LATE-ZI-HISTORICAL-TIME-COORDINATE-NARROWING-R1.json":
        fail("Batch 12AI Matrix artifact binding regressed")
    if row12ai.get("historical_time_coordinate_family") != "LOCAL_OBSERVATIONAL_ASTRONOMICAL_TIME_COORDINATE":
        fail("Batch 12AI Matrix historical time-coordinate family regressed")
    if row12ai.get("runtime_time_standard_binding_status_batch_12ai") != "PARTIALLY_NARROWED_NOT_CLOSED":
        fail("Batch 12AI Matrix batch-scoped runtime binding regressed")
    if row12ai.get("local_apparent_solar_time_historical_binding") != "STRONGEST_MODERN_DAYTIME_TRANSLATION_NOT_NATAL_RUNTIME_WINNER":
        fail("Batch 12AI Matrix apparent-solar authority firewall regressed")
    if row12ai.get("independent_textual_witness_count_added_batch_12ai") != 0 or row12ai.get("independent_hai_glyph_witness_count_added_batch_12ai") != 0:
        fail("Batch 12AI witness accounting regressed")
    src12ai = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-CTEXT-MINGSHI-ASTRONOMY-DINGSHI-SOLAR-STELLAR"), None)
    if not src12ai or src12ai.get("source_role") != "RECEIVED_INSTITUTIONAL_WITNESS_FOR_MING_SOLAR_STELLAR_TIME_DETERMINATION_NOT_ZIWEI_DOCTRINE":
        fail("Batch 12AI registry source scope regressed")
    mp12ai = src12ai.get("machine_probe", {})
    if mp12ai.get("workflow_run_id") != 34322850489 or mp12ai.get("response_sha256") != "157eac2885f6bd3e6c72899f90539e4dd817cf63099c6e17508a8fc419293c16":
        fail("Batch 12AI registry machine binding regressed")

    # Batch 12AJ Fullbook Luojing semantics.
    if ziwei_fullbook_luojing_aj_evidence.get("batch_id") != "BATCH-12-ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-AJ":
        fail("Batch 12AJ evidence identity mismatch")
    probe12aj = ziwei_fullbook_luojing_aj_evidence.get("controlling_probe", {})
    if probe12aj.get("workflow_run_id") != 34325691911 or probe12aj.get("artifact_id") != 10093682981:
        fail("Batch 12AJ controlling probe binding regressed")
    if probe12aj.get("artifact_zip_sha256") != "4374cfdb3bcdf6c36f939eb7168826d424b103d2cb42ea1722193f1ca38c9e95" or probe12aj.get("all_decisive_control_terms_hit") is not True:
        fail("Batch 12AJ stabilized probe gate regressed")
    full12aj = ziwei_fullbook_luojing_aj_evidence.get("fullbook_direct_physical_phrase_collation", {})
    if full12aj.get("agreement_status") != "DIRECT_PHYSICAL_FULLBOOK_NANYANGTANG_AND_GUANGYI_AGREE_ON_LUOJING_SENTENCE":
        fail("Batch 12AJ Fullbook Luojing physical-edition agreement regressed")
    if full12aj.get("new_independent_text_witness_increment") != 0:
        fail("Batch 12AJ double-counting firewall regressed")
    phil12aj = ziwei_fullbook_luojing_aj_evidence.get("philological_adjudication", {})
    if phil12aj.get("historically_attested_mechanical_concept") != "MAGNETIC_COMPASS_DIRECTION_AND_MERIDIAN_ORIENTATION_INSTRUMENT_FAMILY":
        fail("Batch 12AJ Luojing mechanical concept regressed")
    if phil12aj.get("standalone_clock_or_timepiece_equivalence") != "REJECTED_BY_CONTEMPORANEOUS_TECHNICAL_CONTROL":
        fail("Batch 12AJ Luojing standalone-clock firewall regressed")
    if phil12aj.get("direct_equivalence_to_true_or_apparent_solar_time") != "NOT_ESTABLISHED":
        fail("Batch 12AJ Luojing solar-time inference firewall regressed")
    eff12aj = ziwei_fullbook_luojing_aj_evidence.get("hpa_zdate_006_effect", {})
    if eff12aj.get("audit_status") != "MISSING_FROM_PRODUCT" or eff12aj.get("runtime_time_standard_binding_status") != "PARTIALLY_NARROWED_WITH_FULLBOOK_INSTRUMENT_SEMANTIC_TENSION_NOT_CLOSED":
        fail("Batch 12AJ HPA/runtime state regressed")
    if eff12aj.get("local_apparent_solar_time_winner_selected") is not False or eff12aj.get("luojing_means_true_solar_time") is not False:
        fail("Batch 12AJ true/apparent-solar winner firewall regressed")
    if eff12aj.get("candidate_selected") is not False or eff12aj.get("candidate_collapsed") is not False or eff12aj.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AJ candidate/algorithm firewall regressed")
    row12aj = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12aj or row12aj.get("batch_12aj_fullbook_luojing_timekeeping_semantics_artifact") != "docs/research/ZIWEI-FULLBOOK-LUOJING-TIMEKEEPING-SEMANTICS-R1.json":
        fail("Batch 12AJ Matrix artifact binding regressed")
    if row12aj.get("fullbook_luojing_phrase_direct_physical_edition_agreement") != "CONFIRMED_NANYANGTANG_AND_GUANGYI":
        fail("Batch 12AJ Matrix physical phrase agreement regressed")
    if row12aj.get("fullbook_luojing_standalone_timekeeper_equivalence") != "REJECTED_BY_CONTEMPORANEOUS_TECHNICAL_CONTROL":
        fail("Batch 12AJ Matrix standalone-timekeeper firewall regressed")
    if row12aj.get("runtime_time_standard_binding_status_batch_12aj") != "PARTIALLY_NARROWED_WITH_FULLBOOK_INSTRUMENT_SEMANTIC_TENSION_NOT_CLOSED":
        fail("Batch 12AJ Matrix batch-scoped runtime state regressed")
    if row12aj.get("local_apparent_solar_time_runtime_winner_selected") is not False or row12aj.get("luojing_means_true_solar_time") is not False:
        fail("Batch 12AJ Matrix solar-time winner firewall regressed")
    if row12aj.get("independent_textual_witness_count_added_batch_12aj") != 0 or row12aj.get("independent_hai_glyph_witness_count_added_batch_12aj") != 0:
        fail("Batch 12AJ Matrix witness double-counting firewall regressed")
    if row12aj.get("batch_12aj_primary_timekeeping_technical_control_source_id") != "EXT-SHIDIAN-XINFA-SUANSHU-V1-DINGSHI-LUOJING":
        fail("Batch 12AJ primary technical-control source hierarchy regressed")
    if row12aj.get("batch_12aj_same_memorial_transmission_control_source_id") != "EXT-CTEXT-HUANGMING-JINGSHI-WENBIAN-V493-DINGSHI-LUOJING" or row12aj.get("batch_12aj_same_memorial_double_count_forbidden") is not True:
        fail("Batch 12AJ same-memorial transmission/dedup firewall regressed")
    sources12aj = {s.get("source_id"): s for s in registry.get("sources", ())}
    for sid in (
        "EXT-CTEXT-HUANGMING-JINGSHI-WENBIAN-V493-DINGSHI-LUOJING",
        "EXT-SHIDIAN-XINFA-SUANSHU-V1-DINGSHI-LUOJING",
        "EXT-SHIDIAN-XU-ZHIMO-LUOJING-DINGMENZHEN-MING",
    ):
        src = sources12aj.get(sid)
        if not src or src.get("machine_probe", {}).get("workflow_run_id") != 34325691911:
            fail(f"Batch 12AJ registry source/probe binding regressed: {sid}")
        if src.get("machine_probe", {}).get("artifact_zip_sha256") != "4374cfdb3bcdf6c36f939eb7168826d424b103d2cb42ea1722193f1ca38c9e95":
            fail(f"Batch 12AJ registry artifact digest regressed: {sid}")

    # Batch 12AK Gaohou Mengqiu operational bridge.
    if ziwei_gaohou_mengqiu_ak_evidence.get("batch_id") != "BATCH-12-ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-AK":
        fail("Batch 12AK evidence identity mismatch")
    probe12ak = ziwei_gaohou_mengqiu_ak_evidence.get("controlling_probe", {})
    if probe12ak.get("workflow_run_id") != 34327928353 or probe12ak.get("artifact_id") != 10094524731:
        fail("Batch 12AK controlling probe binding regressed")
    if probe12ak.get("artifact_zip_sha256") != "cf81d001e0a2022afd560f3fedc060aefbc8ecdc8bc9b14fb88f745b0633dec8":
        fail("Batch 12AK artifact digest regressed")
    gates12ak = probe12ak.get("semantic_gates", {})
    if not gates12ak or not all(gates12ak.values()):
        fail("Batch 12AK semantic gate regressed")
    phys12ak = ziwei_gaohou_mengqiu_ak_evidence.get("primary_physical_source", {})
    if phys12ak.get("source_id") != "EXT-WASEDA-GAOHOU-MENGQIU-1807-1809":
        fail("Batch 12AK primary physical source identity regressed")
    if phys12ak.get("source_emitted_not_guessed") is not True:
        fail("Batch 12AK source-emitted Waseda route firewall regressed")
    if phys12ak.get("pdf_sha256") != "53ee7b0e59fbb92304af08d6f1b58226bee6fff85f23e5b43e830b76b967f1e4" or phys12ak.get("pdf_page_count") != 221:
        fail("Batch 12AK Waseda PDF identity regressed")
    direct12ak = {x.get("pdf_page_1_based"): x for x in ziwei_gaohou_mengqiu_ak_evidence.get("direct_physical_collation", ()) if x.get("pdf_page_1_based")}
    if direct12ak.get(143, {}).get("direct_heading") != "一曰羅經平晷":
        fail("Batch 12AK direct 羅經平晷 page binding regressed")
    if direct12ak.get(195, {}).get("decisive_direct_reading") != "余既述日晷諸法以測晝時復述星月儀表諸法以測夜時而于陰雨晦冥之時尚未之及因輯是編所以辨子亥定支干非以供陳設玩好也":
        fail("Batch 12AK direct inclement Zi/Hai reading regressed")
    bridge12ak = ziwei_gaohou_mengqiu_ak_evidence.get("operational_bridge_adjudication", {})
    if bridge12ak.get("relation_to_fullbook") != "LATER_OPERATIONAL_BRIDGE_NOT_FULLBOOK_AUTHORIAL_OR_MING_CLOCK_SPECIFICATION":
        fail("Batch 12AK historical-scope firewall regressed")
    if bridge12ak.get("fullbook_luojing_phrase_explained_as_exact_procedure") is not False or bridge12ak.get("fullbook_inheritance_proven") is not False:
        fail("Batch 12AK Fullbook inheritance firewall regressed")
    eff12ak = ziwei_gaohou_mengqiu_ak_evidence.get("hpa_zdate_006_effect", {})
    if eff12ak.get("audit_status") != "MISSING_FROM_PRODUCT" or eff12ak.get("runtime_time_standard_binding_status") != "LATER_OPERATIONAL_BRIDGE_CONFIRMED_FULLBOOK_SOURCE_SPECIFIC_BINDING_STILL_OPEN":
        fail("Batch 12AK HPA/runtime state regressed")
    if eff12ak.get("candidate_selected") is not False or eff12ak.get("candidate_collapsed") is not False or eff12ak.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AK candidate/algorithm firewall regressed")
    row12ak = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ak or row12ak.get("batch_12ak_gaohou_mengqiu_operational_bridge_artifact") != "docs/research/ZIWEI-GAOHOU-MENGQIU-OPERATIONAL-BRIDGE-R1.json":
        fail("Batch 12AK Matrix artifact binding regressed")
    if row12ak.get("batch_12ak_primary_physical_source_id") != "EXT-WASEDA-GAOHOU-MENGQIU-1807-1809":
        fail("Batch 12AK Matrix primary physical source regressed")
    if row12ak.get("batch_12ak_luojing_pinggui_status") != "DIRECT_PHYSICAL_CONFIRMED_COMPASS_ORIENTATION_COMPONENT_INSIDE_SUNDIAL":
        fail("Batch 12AK Matrix Luojing-pinggui adjudication regressed")
    if row12ak.get("batch_12ak_inclement_zi_hai_status") != "DIRECT_PHYSICAL_CONFIRMED_CLOCK_SECTION_PURPOSE_INCLUDES_INCLEMENT_DARK_CONDITIONS_AND_BIAN_ZI_HAI_DING_ZHIGAN":
        fail("Batch 12AK Matrix inclement Zi/Hai adjudication regressed")
    if row12ak.get("batch_12ak_fullbook_inheritance_proven") is not False:
        fail("Batch 12AK Matrix Fullbook inheritance firewall regressed")
    if row12ak.get("runtime_time_standard_binding_status_batch_12ak") != "LATER_OPERATIONAL_BRIDGE_CONFIRMED_FULLBOOK_SOURCE_SPECIFIC_BINDING_STILL_OPEN":
        fail("Batch 12AK Matrix batch-scoped runtime binding regressed")
    if row12ak.get("independent_textual_witness_count_added_batch_12ak") != 0 or row12ak.get("independent_hai_glyph_witness_count_added_batch_12ak") != 0:
        fail("Batch 12AK Matrix Fullbook witness firewall regressed")
    sources12ak = {s.get("source_id"): s for s in registry.get("sources", ())}
    waseda12ak = sources12ak.get("EXT-WASEDA-GAOHOU-MENGQIU-1807-1809")
    if not waseda12ak or waseda12ak.get("pdf_sha256") != "53ee7b0e59fbb92304af08d6f1b58226bee6fff85f23e5b43e830b76b967f1e4":
        fail("Batch 12AK Waseda registry source regressed")
    if waseda12ak.get("machine_probe", {}).get("artifact_zip_sha256") != "cf81d001e0a2022afd560f3fedc060aefbc8ecdc8bc9b14fb88f745b0633dec8":
        fail("Batch 12AK Waseda registry artifact binding regressed")
    shidian12ak = sources12ak.get("EXT-SHIDIAN-GAOHOU-MENGQIU-V3")
    if not shidian12ak or shidian12ak.get("independent_physical_witness_increment") != 0:
        fail("Batch 12AK Shidian double-counting firewall regressed")
    ctext12ak = sources12ak.get("EXT-CTEXT-GAOHOU-MENGQIU-OCR")
    if not ctext12ak or ctext12ak.get("source_role") != "OCR_DISCOVERY_AND_CROSSCHECK_ONLY_NO_GLYPH_LEVEL_AUTHORITY":
        fail("Batch 12AK OCR authority firewall regressed")

    # Batch 12AL Korea CNTS full target-section re-collation.
    if ziwei_korea_cnts_al_evidence.get("batch_id") != "BATCH-12-ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-AL":
        fail("Batch 12AL evidence identity mismatch")
    inherited12al = ziwei_korea_cnts_al_evidence.get("inherited_acquisition", {})
    if inherited12al.get("workflow_run_id") != 34247945308 or inherited12al.get("artifact_id") != 10064784871:
        fail("Batch 12AL inherited Korea acquisition binding regressed")
    if inherited12al.get("artifact_zip_sha256") != "64b1729df1523991a4ac764e8a4672cf7b6edeb41f94b56a47da49d5b17a6f95":
        fail("Batch 12AL inherited artifact digest regressed")
    source12al = ziwei_korea_cnts_al_evidence.get("source_object", {})
    if source12al.get("pdf_sha256") != "b21bbf3e2c7cdada4153f847ff9f359dbb29e71998e1f931417d108b571b23c3" or source12al.get("pdf_page_count") != 153:
        fail("Batch 12AL Korea physical source identity regressed")
    recoll12al = ziwei_korea_cnts_al_evidence.get("direct_adjacent_page_recollation_no_ocr", {})
    p125_12al = recoll12al.get("pdf_page_125", {})
    p126_12al = recoll12al.get("pdf_page_126", {})
    if p125_12al.get("direct_target_reading") != "命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜":
        fail("Batch 12AL direct p125 target reading regressed")
    if p125_12al.get("explicit_hai_glyph_observed") is not False or p125_12al.get("fullbook_luojing_clause_observed_after_target") is not False:
        fail("Batch 12AL p125 Hai/Luojing variant firewall regressed")
    if p125_12al.get("page_local_negative_scope") != "AUTHORIZED_ONLY_FOR_THE_TARGET_LOCATION_AND_REMAINING_ADJACENT_TEXT_ON_P125; NOT_A_WHOLE_MANUSCRIPT_NEGATIVE":
        fail("Batch 12AL negative-scope firewall regressed")
    if p126_12al.get("fullbook_luojing_clause_continuation_observed") is not False:
        fail("Batch 12AL p126 continuation adjudication regressed")
    cross12al = ziwei_korea_cnts_al_evidence.get("cross_transmission_comparison", {})
    if cross12al.get("explicit_hai_reclassification_universal") is not False or cross12al.get("fullbook_luojing_clause_universal_across_broader_ziwei_transmission") is not False:
        fail("Batch 12AL broader-transmission universality firewall regressed")
    if cross12al.get("within_reviewed_fullbook_physical_routes_luojing_clause_stability") != "CONFIRMED_NANYANGTANG_AND_GUANGYI":
        fail("Batch 12AL Fullbook within-family stability regressed")
    phil12al = ziwei_korea_cnts_al_evidence.get("philological_adjudication", {})
    if phil12al.get("fullbook_luojing_clause_interpolation_claim_authorized") is not False or phil12al.get("korea_manuscript_omission_error_claim_authorized") is not False:
        fail("Batch 12AL interpolation/error claim firewall regressed")
    indep12al = ziwei_korea_cnts_al_evidence.get("evidence_independence", {})
    if indep12al.get("new_physical_witness_increment") != 0 or indep12al.get("new_target_section_clause_variant_dimension_increment") != 1:
        fail("Batch 12AL evidence independence accounting regressed")
    eff12al = ziwei_korea_cnts_al_evidence.get("hpa_zdate_006_effect", {})
    if eff12al.get("audit_status") != "MISSING_FROM_PRODUCT" or eff12al.get("runtime_time_standard_binding_status") != "BROADER_ZIWEI_TRANSMISSION_VARIANT_CONFIRMED_FULLBOOK_OPERATIONAL_PROCEDURE_REMAINS_SOURCE_SCOPED_AND_RUNTIME_UNRESOLVED":
        fail("Batch 12AL HPA/runtime state regressed")
    if eff12al.get("candidate_selected") is not False or eff12al.get("candidate_collapsed") is not False or eff12al.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AL candidate/algorithm firewall regressed")
    row12al = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12al or row12al.get("batch_12al_korea_cnts_full_target_section_recollation_artifact") != "docs/research/ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-R1.json":
        fail("Batch 12AL Matrix artifact binding regressed")
    if row12al.get("batch_12al_korea_same_physical_object_recount_forbidden") is not True or row12al.get("batch_12al_new_physical_witness_increment") != 0:
        fail("Batch 12AL Matrix same-object recount firewall regressed")
    if row12al.get("batch_12al_korea_fullbook_luojing_clause_at_target_location") is not False or row12al.get("batch_12al_korea_p126_target_continuation") is not False:
        fail("Batch 12AL Matrix target-section variant regressed")
    if row12al.get("batch_12al_fullbook_interpolation_claim_authorized") is not False or row12al.get("batch_12al_korea_omission_error_claim_authorized") is not False:
        fail("Batch 12AL Matrix interpolation/error firewall regressed")
    if row12al.get("runtime_time_standard_binding_status_batch_12al") != "BROADER_ZIWEI_TRANSMISSION_VARIANT_CONFIRMED_FULLBOOK_OPERATIONAL_PROCEDURE_REMAINS_SOURCE_SCOPED_AND_RUNTIME_UNRESOLVED":
        fail("Batch 12AL Matrix historical runtime snapshot regressed")
    if row12al.get("candidate_selected_batch_12al") is not False or row12al.get("candidate_collapsed_batch_12al") is not False:
        fail("Batch 12AL Matrix candidate firewall regressed")
    korea12al = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-KOREA-NLK-CNTS-00047996572-ZIWEIDOUSHUFANGSHU"), None)
    if not korea12al or korea12al.get("target_section_recollation_artifact") != "docs/research/ZIWEI-KOREA-CNTS-FULL-TARGET-SECTION-RECOLLATION-R1.json":
        fail("Batch 12AL Korea registry artifact binding regressed")
    if korea12al.get("same_physical_object_recount_forbidden") is not True:
        fail("Batch 12AL Korea registry recount firewall regressed")
    if korea12al.get("target_location_negative_scope") != "P125_TARGET_LOCATION_PLUS_ADJACENT_P126_ONLY_NOT_WHOLE_MANUSCRIPT":
        fail("Batch 12AL Korea registry negative scope regressed")

    # Batch 12AM early-Ming shushu Luojing/gnomon semantic bridge.
    if ziwei_renzi_xuzhi_am_evidence.get("batch_id") != "BATCH-12-ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-AM":
        fail("Batch 12AM evidence identity mismatch")
    probe12am = ziwei_renzi_xuzhi_am_evidence.get("controlling_probe", {})
    if probe12am.get("workflow_run_id") != 34332573715 or probe12am.get("artifact_id") != 10096390533:
        fail("Batch 12AM controlling probe binding regressed")
    if probe12am.get("artifact_zip_sha256") != "b79fb61aa46624a601c97fff386fb5090afeb4aaa8dd07f382e9c3f5cf6977b6":
        fail("Batch 12AM artifact digest regressed")
    if not all(probe12am.get("semantic_gates", {}).values()):
        fail("Batch 12AM semantic gates regressed")
    phys12am = ziwei_renzi_xuzhi_am_evidence.get("primary_physical_scan", {})
    if phys12am.get("pdf_sha256") != "80de366d62066bf73046834771a43976fdf353de6ea1704d06c46dfa568a44ba" or phys12am.get("pdf_page_count") != 510:
        fail("Batch 12AM physical facsimile identity regressed")
    if phys12am.get("source_emitted_not_guessed") is not True or phys12am.get("direct_visual_review_no_ocr") is not True:
        fail("Batch 12AM source-emitted/no-OCR firewall regressed")
    direct12am = {x.get("pdf_page_1_based"): x for x in ziwei_renzi_xuzhi_am_evidence.get("direct_physical_collation", ())}
    if direct12am.get(415, {}).get("direct_heading") != "正針縫針":
        fail("Batch 12AM direct 正針縫針 heading regressed")
    decisive12am = direct12am.get(416, {}).get("decisive_direct_readings", ())
    for phrase in ("臬測以景針以氣故不能符", "推七政之纏次皆准於臬"):
        if phrase not in decisive12am:
            fail(f"Batch 12AM direct physical reading regressed: {phrase}")
    phil12am = ziwei_renzi_xuzhi_am_evidence.get("philological_mechanical_adjudication", {})
    if phil12am.get("luojing_standalone_clock_equivalence") is not False or phil12am.get("fullbook_inclement_time_generation_procedure_closed") is not False:
        fail("Batch 12AM clock/procedure firewall regressed")
    if phil12am.get("luojing_equals_true_solar_time") is not False or phil12am.get("luojing_equals_local_apparent_solar_runtime") is not False:
        fail("Batch 12AM solar-runtime normalization firewall regressed")
    eff12am = ziwei_renzi_xuzhi_am_evidence.get("hpa_zdate_006_effect", {})
    expected12am = "EARLY_MING_SHUSHU_GNOMON_NEEDLE_SEMANTIC_SEPARATION_CONFIRMED_FULLBOOK_INCLEMENT_TIME_REALIZATION_AND_RUNTIME_BINDING_STILL_OPEN"
    if eff12am.get("audit_status") != "MISSING_FROM_PRODUCT" or eff12am.get("runtime_time_standard_binding_status") != expected12am:
        fail("Batch 12AM HPA/runtime state regressed")
    if eff12am.get("candidate_selected") is not False or eff12am.get("candidate_collapsed") is not False or eff12am.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AM candidate/algorithm firewall regressed")
    row12am = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12am or row12am.get("batch_12am_renzi_xuzhi_luojing_gnomon_bridge_artifact") != "docs/research/ZIWEI-RENZI-XUZHI-LUOJING-GNOMON-BRIDGE-R1.json":
        fail("Batch 12AM Matrix artifact binding regressed")
    if row12am.get("batch_12am_pdf_sha256") != "80de366d62066bf73046834771a43976fdf353de6ea1704d06c46dfa568a44ba" or row12am.get("batch_12am_pdf_page_count") != 510:
        fail("Batch 12AM Matrix physical source binding regressed")
    if row12am.get("batch_12am_decisive_direct_readings") != ["臬測以景針以氣故不能符", "推七政之纏次皆准於臬"]:
        fail("Batch 12AM Matrix decisive reading regressed")
    if row12am.get("batch_12am_fullbook_inclement_time_generation_procedure_closed") is not False:
        fail("Batch 12AM Matrix unresolved-procedure firewall regressed")
    if row12am.get("runtime_time_standard_binding_status_batch_12am") != expected12am:
        fail("Batch 12AM Matrix historical runtime snapshot regressed")
    if row12am.get("candidate_selected_batch_12am") is not False or row12am.get("candidate_collapsed_batch_12am") is not False:
        fail("Batch 12AM Matrix candidate firewall regressed")
    sources12am = {src.get("source_id"): src for src in registry.get("sources", ())}
    physical12am = sources12am.get("EXT-COMMONS-GGZBCK411-RENZI-XUZHI-1569-1583")
    if not physical12am or physical12am.get("pdf_sha256") != "80de366d62066bf73046834771a43976fdf353de6ea1704d06c46dfa568a44ba":
        fail("Batch 12AM registry physical source regressed")
    if physical12am.get("target_leaf_printing_phase") != "UNRESOLVED_WITHIN_LONGQING_3_WANLI_11_COMPOSITE_EDITION":
        fail("Batch 12AM printing-phase firewall regressed")
    cinii12am = sources12am.get("EXT-CINII-BB17866565-RENZI-XUZHI-1583")
    if not cinii12am or cinii12am.get("exact_physical_copy_identity_to_commons_scan") != "NOT_ESTABLISHED":
        fail("Batch 12AM CiNii exact-copy firewall regressed")
    ctext12am = sources12am.get("EXT-CTEXT-RENZI-XUZHI-ZHENGZHEN-FENGZHEN")
    if not ctext12am or ctext12am.get("glyph_authority") is not False or ctext12am.get("independent_physical_witness_increment") != 0:
        fail("Batch 12AM transcription authority firewall regressed")

    # Batch 12AN Ming shushu time-mountain bridge.
    if ziwei_wanxiaolu_an_evidence.get("batch_id") != "BATCH-12-ZIWEI-WANXIAOLU-TIME-MOUNTAIN-BRIDGE-AN":
        fail("Batch 12AN evidence identity mismatch")
    router12an = ziwei_wanxiaolu_an_evidence.get("controlling_probes", {}).get("shidian_router_page_map", {})
    if router12an.get("workflow_run_id") != 34339848620 or router12an.get("artifact_id") != 10099257417 or router12an.get("artifact_zip_sha256") != "aed5ca502e3c41f14f0e4304cf60bf0816d77c54504dcec67d9c35455271466b":
        fail("Batch 12AN router probe binding regressed")
    ctext12an=ziwei_wanxiaolu_an_evidence.get("ctext_source", {})
    if ctext12an.get("source_emitted_target_page_url") != "https://ctext.org/library.pl?if=gb&file=100720&page=144" or ctext12an.get("target_page_number_guessed") is not False or ctext12an.get("glyph_authority_claimed") is not False:
        fail("Batch 12AN CText locator/glyph firewall regressed")
    shidian12an=ziwei_wanxiaolu_an_evidence.get("shidian_source", {})
    if shidian12an.get("source_metadata", {}).get("edition") != "內府明萬曆35年刻本" or shidian12an.get("source_metadata", {}).get("image_source") != "國家圖書館":
        fail("Batch 12AN Shidian edition binding regressed")
    if shidian12an.get("target_source_emitted_global_page_span") != [5607, 5611] or shidian12an.get("direct_target_image_bytes_observed") is not False or shidian12an.get("glyph_authority_claimed") is not False:
        fail("Batch 12AN page-map/evidence firewall regressed")
    adj12an=ziwei_wanxiaolu_an_evidence.get("adjudication", {})
    if adj12an.get("twenty_four_mountain_ring_can_encode_time_sector_coordinates") is not True or adj12an.get("actual_time_determination_is_solar_or_astronomical_reference_anchored_in_this_witness") is not True:
        fail("Batch 12AN semantic bridge regressed")
    if adj12an.get("magnetic_needle_is_standalone_clock") is not False or adj12an.get("fullbook_cloudy_rainy_time_generation_chain_closed") is not False:
        fail("Batch 12AN clock/inclement firewall regressed")
    row12an=next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    expected12an="MING_SHUSHU_24_MOUNTAIN_TIME_SECTOR_MAPPING_CONFIRMED_SOLAR_ASTRONOMICAL_ANCHOR_REMAINS_REQUIRED_FULLBOOK_INCLEMENT_CHAIN_AND_RUNTIME_BINDING_STILL_OPEN"
    if not row12an or row12an.get("runtime_time_standard_binding_status_batch_12an") != expected12an or row12an.get("audit_status") != "MISSING_FROM_PRODUCT":
        fail("Batch 12AN historical Matrix snapshot regressed")
    if row12an.get("batch_12an_direct_target_glyph_authority") is not False or row12an.get("batch_12an_fullbook_inclement_time_generation_chain_closed") is not False:
        fail("Batch 12AN Matrix evidence firewall regressed")
    if row12an.get("candidate_selected_batch_12an") is not False or row12an.get("candidate_collapsed_batch_12an") is not False or row12an.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AN candidate/algorithm firewall regressed")


    # Batch 12AO complete-current-public-transcription early-Ziwei boundary.
    if ziwei_jielan_ao_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIELAN-INCLEMENT-TIME-ACQUISITION-AO":
        fail("Batch 12AO evidence identity mismatch")
    probe12ao = ziwei_jielan_ao_evidence.get("probes", {}).get("jielan_full_pagination_probe", {})
    if probe12ao.get("workflow_run_id") != 34341036879 or probe12ao.get("artifact_id") != 10099727992 or probe12ao.get("artifact_zip_sha256") != "75cf90fcfbdf4df9728dfec0bbc5c7d69c23e40922001a78e4421beeef3cb7fd":
        fail("Batch 12AO controlling pagination probe binding regressed")
    surface12ao = ziwei_jielan_ao_evidence.get("jielan_1581_public_transcription_surface", {})
    if surface12ao.get("fetched_page_numbers") != [1, 2, 3, 4, 5] or surface12ao.get("all_source_discovered_pages_1_to_5_fetched") is not True:
        fail("Batch 12AO source-emitted pagination coverage regressed")
    if surface12ao.get("declared_chapter_count") != 246 or surface12ao.get("declared_character_count") != 67533:
        fail("Batch 12AO declared public-surface inventory regressed")
    if not all(surface12ao.get("positive_control_terms", {}).values()) or any(surface12ao.get("inclement_luojing_term_hits", {}).values()):
        fail("Batch 12AO positive-control/nonattestation surface regressed")
    if surface12ao.get("whole_1581_physical_book_negative_authorized") is not False or surface12ao.get("glyph_authority_claimed") is not False or surface12ao.get("interpolation_claim_authorized") is not False:
        fail("Batch 12AO physical-negative/glyph/interpolation firewall regressed")
    adj12ao = ziwei_jielan_ao_evidence.get("adjudication", {})
    if adj12ao.get("fullbook_clause_remains_source_scoped") is not True or adj12ao.get("ming_technical_inclement_time_input_is_clepsydra_not_compass") is not True:
        fail("Batch 12AO source-scope/technical-control adjudication regressed")
    if adj12ao.get("fullbook_inclement_current_time_acquisition_mechanism_closed") is not False or adj12ao.get("runtime_standard_selected") is not False or adj12ao.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AO unresolved-runtime/algorithm firewall regressed")
    jielan12ao = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-ZIWEI-JIELAN-1581"), None)
    if not jielan12ao or jielan12ao.get("public_transcription_source_emitted_pagination_pages") != [1, 2, 3, 4, 5]:
        fail("Batch 12AO registry pagination binding regressed")
    if jielan12ao.get("public_transcription_inclement_luojing_terms_attested") is not False or jielan12ao.get("whole_1581_physical_book_negative_authorized") is not False or jielan12ao.get("glyph_authority") is not False:
        fail("Batch 12AO registry authority firewall regressed")
    row12ao = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    expected12ao = "EARLY_1581_JIELAN_COMPLETE_PUBLIC_TRANSCRIPTION_NONATTESTATION_CONFIRMED_FULLBOOK_INCLEMENT_LUOJING_CLAUSE_REMAINS_SOURCE_SCOPED_AND_CLOCK_INPUT_UNRESOLVED"
    if not row12ao or row12ao.get("runtime_time_standard_binding_status_batch_12ao") != expected12ao or row12ao.get("audit_status") != "MISSING_FROM_PRODUCT":
        fail("Batch 12AO historical Matrix snapshot regressed")
    if row12ao.get("candidate_selected_batch_12ao") is not False or row12ao.get("candidate_collapsed_batch_12ao") is not False or row12ao.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AO candidate/algorithm firewall regressed")

    # Batch 12AP evidence-scope correction after the AO aggregate-page probe.
    if ziwei_jielan_ap_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIELAN-BIRTH-TIME-CHAPTER-SCOPE-CORRECTION-AP":
        fail("Batch 12AP evidence identity mismatch")
    p12ap = ziwei_jielan_ap_evidence.get("probes", {}).get("ap_r1", {})
    if p12ap.get("workflow_run_id") != 34342819087 or p12ap.get("artifact_id") != 10100441781 or p12ap.get("artifact_zip_sha256") != "6bf56986a8a594c759e088521496ed9c43944c87b11b29e0a4fd489868b483c8":
        fail("Batch 12AP controlling PT49 probe binding regressed")
    idx12ap = ziwei_jielan_ap_evidence.get("google_books_jielan_index", {})
    if idx12ap.get("inclement_query_source_emitted_page_ids") != ["PT49"] or idx12ap.get("pt49_index_attested_heading") != "論十二生時難定訣":
        fail("Batch 12AP PT49 index localization regressed")
    adj12ap = ziwei_jielan_ap_evidence.get("adjudication", {})
    if adj12ap.get("jielan_inclement_birth_time_discussion_public_index_attested") is not True or adj12ap.get("batch12ao_transmission_variant_inference_retracted") is not True:
        fail("Batch 12AP scope repair adjudication regressed")
    if adj12ap.get("pt49_physical_glyph_authority_obtained") is not False or adj12ap.get("runtime_standard_selected") is not False or adj12ap.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AP physical/runtime/algorithm firewall regressed")
    row12ap = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    expected12ap = "JIELAN_INCLEMENT_BIRTH_TIME_DISCUSSION_INDEX_ATTESTED_AO_PAGINATION_SCOPE_CORRECTED_FULLBOOK_LUOJING_CLAUSE_AND_INCLEMENT_CLOCK_INPUT_STILL_UNRESOLVED"
    if not row12ap or row12ap.get("runtime_time_standard_binding_status") != expected12ap or row12ap.get("runtime_time_standard_binding_status_batch_12ap") != expected12ap or row12ap.get("audit_status") != "MISSING_FROM_PRODUCT":
        fail("Batch 12AP current Matrix state regressed")
    if row12ap.get("batch_12ap_prov_defect_id") != "PROV-DEFECT-011" or row12ap.get("batch_12ap_repair_status") != "REPAIRED_FORWARD_ONLY_DURING_BATCH_12AP":
        fail("Batch 12AP provenance repair state regressed")
    if row12ap.get("candidate_selected_batch_12ap") is not False or row12ap.get("candidate_collapsed_batch_12ap") is not False or row12ap.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AP candidate/algorithm firewall regressed")
    if matrix.get("audit_summary", {}).get("confirmed_provenance_metadata_defect_count") != 11 or matrix.get("audit_summary", {}).get("repaired_provenance_metadata_defect_count") != 11:
        fail("Batch 12AP provenance defect accounting regressed")

    # Batch 12AQ direct printed-bibliography imprint reconciliation.
    if ziwei_jielan_aq_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIELAN-BIBLIOGRAPHIC-IMPRINT-RECONCILIATION-AQ":
        fail("Batch 12AQ evidence identity mismatch")
    aq_probe = ziwei_jielan_aq_evidence.get("controlling_probe", {})
    if aq_probe.get("workflow_run_id") != 34350629959 or aq_probe.get("artifact_id") != 10103542053 or aq_probe.get("artifact_zip_sha256") != "c50fff947d5adf8e4eb9109d7d00485dbe7d04a7767090ca6e9109603b8c7f88":
        fail("Batch 12AQ controlling probe binding regressed")
    aq_scan = ziwei_jielan_aq_evidence.get("direct_bibliographic_scan", {})
    if aq_scan.get("target_pdf_page_1_based") != 40 or aq_scan.get("catalog_item_number") != 4051:
        fail("Batch 12AQ direct bibliography locator regressed")
    aq_read = aq_scan.get("direct_visual_reading", {})
    if aq_read.get("edition_imprint") != "明萬曆九年金陵書坊王洛川刻本" or aq_read.get("imprint_name") != "王洛川":
        fail("Batch 12AQ direct imprint reading regressed")
    if aq_scan.get("ocr_used_for_final_glyph_adjudication") is not False:
        fail("Batch 12AQ OCR firewall regressed")
    aq_conflict = ziwei_jielan_aq_evidence.get("search_surface_conflict", {})
    if aq_conflict.get("surfaced_reading") != "明萬曆九年金陵書坊王德川刻本" or aq_conflict.get("surfaced_item_number") != 4052:
        fail("Batch 12AQ search-surface conflict record regressed")
    if aq_conflict.get("adjudication") != "REJECTED_AS_SEARCH_INDEX_OCR_AND_TABLE_ALIGNMENT_ARTIFACT" or aq_conflict.get("search_surface_is_glyph_authority") is not False:
        fail("Batch 12AQ search-surface authority firewall regressed")
    aq_adj = ziwei_jielan_aq_evidence.get("adjudication", {})
    if aq_adj.get("current_registry_imprint_wang_luochuan_supported") is not True or aq_adj.get("current_registry_should_change_to_wang_dechuan") is not False:
        fail("Batch 12AQ registry-imprint adjudication regressed")
    if aq_adj.get("repository_provenance_metadata_defect_increment") != 0 or aq_adj.get("chart_algorithm_defect_increment") != 0 or aq_adj.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AQ defect/algorithm firewall regressed")
    aq_catalog = next((x for x in registry.get("sources", ()) if x.get("source_id") == "EXT-CHINESE-RARE-BOOKS-CATALOG-JIELAN-4051"), None)
    aq_ncl = next((x for x in registry.get("sources", ()) if x.get("source_id") == "EXT-NCL-WANGSHI-LUOCHUAN-XUANHE"), None)
    aq_jielan = next((x for x in registry.get("sources", ()) if x.get("source_id") == "EXT-ZIWEI-JIELAN-1581"), None)
    if aq_catalog is None or aq_ncl is None or aq_jielan is None:
        fail("Batch 12AQ registry sources missing")
    if aq_catalog.get("catalog_item_number") != 4051 or aq_catalog.get("direct_visual_imprint") != "明萬曆九年金陵書坊王洛川刻本" or aq_catalog.get("ocr_used_for_final_glyph_adjudication") is not False:
        fail("Batch 12AQ direct catalog registry binding regressed")
    if aq_ncl.get("direct_catalog_term") != "明金陵王氏洛川校刊本":
        fail("Batch 12AQ NCL bookseller-name control regressed")
    aq_binding = aq_jielan.get("batch_12aq_direct_bibliography_confirmation", {})
    if aq_binding.get("catalog_item_number") != 4051 or aq_binding.get("direct_visual_imprint") != "明萬曆九年金陵書坊王洛川刻本" or aq_binding.get("search_surface_wang_dechuan_rejected") is not True:
        fail("Batch 12AQ Jielan registry confirmation regressed")
    row12aq = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    expected12aq = "JIELAN_INCLEMENT_BIRTH_TIME_DISCUSSION_INDEX_ATTESTED_AO_PAGINATION_SCOPE_CORRECTED_FULLBOOK_LUOJING_CLAUSE_AND_INCLEMENT_CLOCK_INPUT_STILL_UNRESOLVED"
    if not row12aq or row12aq.get("runtime_time_standard_binding_status") != expected12aq or row12aq.get("audit_status") != "MISSING_FROM_PRODUCT" or row12aq.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AQ unexpectedly changed HPA-ZDATE-006")
    if matrix.get("audit_summary", {}).get("confirmed_provenance_metadata_defect_count") != 11 or matrix.get("audit_summary", {}).get("repaired_provenance_metadata_defect_count") != 11:
        fail("Batch 12AQ provenance accounting should remain 11/11")

    # Batch 12AR closes the reviewed public PT49 preview access surface without glyph promotion.
    if ziwei_jielan_ar_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIELAN-PT49-PUBLIC-PREVIEW-ACCESS-BOUNDARY-AR":
        fail("Batch 12AR evidence identity mismatch")
    probes12ar = ziwei_jielan_ar_evidence.get("probes", {})
    r4 = probes12ar.get("ar_r4_direct_pt49_source_emitted_image", {})
    if r4.get("workflow_run_id") != 34353510199 or r4.get("artifact_id") != 10104715354 or r4.get("artifact_zip_sha256") != "52c968a601a56732f293d2f25318d8d70ae6dc4f2e588baeee077e51ada6b1ed":
        fail("Batch 12AR controlling direct-image probe binding regressed")
    play12ar = ziwei_jielan_ar_evidence.get("direct_play_reader_adjudication", {})
    if play12ar.get("pt48_response_sha256") != "4d95bcc7a8c14d842d1d735faa83cfbb33cc16773cc35ddb4ef18d3c679d95d0":
        fail("Batch 12AR PT48 positive-control image binding regressed")
    if play12ar.get("pt48_manual_visual_review") != "GENUINE_JIELAN_FACSIMILE_PAGE_IMAGE":
        fail("Batch 12AR PT48 visual positive control regressed")
    if play12ar.get("pt49_response_sha256") != "3efa8c43e5b4348f303a528c81adf435f0111ea752fe9f0f6241478b60987fa6" or play12ar.get("pt50_response_sha256") != "3efa8c43e5b4348f303a528c81adf435f0111ea752fe9f0f6241478b60987fa6":
        fail("Batch 12AR PT49/PT50 placeholder hash binding regressed")
    if play12ar.get("pt49_manual_visual_review") != "VISIBLE_IMAGE_NOT_AVAILABLE_PLACEHOLDER_NOT_BOOK_PAGE" or play12ar.get("pt50_manual_visual_review") != "VISIBLE_IMAGE_NOT_AVAILABLE_PLACEHOLDER_NOT_BOOK_PAGE":
        fail("Batch 12AR placeholder visual adjudication regressed")
    if play12ar.get("pt49_physical_page_observed") is not False or play12ar.get("pt49_physical_glyph_authority") is not False:
        fail("Batch 12AR physical-glyph firewall regressed")
    adj12ar = ziwei_jielan_ar_evidence.get("adjudication", {})
    if adj12ar.get("reviewed_google_public_preview_surface_closed_for_current_routes") is not True or adj12ar.get("google_public_preview_can_supply_pt49_physical_glyphs") is not False:
        fail("Batch 12AR public-preview closure adjudication regressed")
    if adj12ar.get("repository_provenance_metadata_defect_increment") != 0 or adj12ar.get("chart_algorithm_defect_increment") != 0 or adj12ar.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AR defect/algorithm firewall regressed")
    preview12ar = next((x for x in registry.get("sources", ()) if x.get("source_id") == "EXT-GOOGLE-PLAY-JIELAN-PT49-PREVIEW-BOUNDARY"), None)
    gb12ar = next((x for x in registry.get("sources", ()) if x.get("source_id") == "EXT-GOOGLE-BOOKS-JIELAN-PT49-INCLEMENT-BIRTH-TIME-INDEX"), None)
    if preview12ar is None or gb12ar is None:
        fail("Batch 12AR registry sources missing")
    if preview12ar.get("pt49_signed_image_url_source_emitted") is not True or preview12ar.get("pt49_placeholder_sha256") != "3efa8c43e5b4348f303a528c81adf435f0111ea752fe9f0f6241478b60987fa6" or preview12ar.get("glyph_authority") is not False:
        fail("Batch 12AR preview-boundary registry binding regressed")
    gb_boundary = gb12ar.get("batch_12ar_public_preview_boundary", {})
    if gb_boundary.get("pt49_response_visual_status") != "IMAGE_NOT_AVAILABLE_PLACEHOLDER" or gb_boundary.get("pt49_physical_glyph_authority") is not False:
        fail("Batch 12AR Google Books registry boundary regressed")
    row12ar = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    expected_current = "JIELAN_INCLEMENT_BIRTH_TIME_DISCUSSION_INDEX_ATTESTED_AO_PAGINATION_SCOPE_CORRECTED_FULLBOOK_LUOJING_CLAUSE_AND_INCLEMENT_CLOCK_INPUT_STILL_UNRESOLVED"
    expected_ar = "GOOGLE_PUBLIC_PREVIEW_PT49_INDEX_AND_SIGNED_IMAGE_URL_ATTESTED_TARGET_IMAGE_RETURNS_PLACEHOLDER_FULLBOOK_INCLEMENT_CLOCK_INPUT_STILL_UNRESOLVED"
    if not row12ar or row12ar.get("runtime_time_standard_binding_status") != expected_current or row12ar.get("runtime_time_standard_binding_status_batch_12ar") != expected_ar:
        fail("Batch 12AR Matrix runtime/access boundary regressed")
    if row12ar.get("batch_12ar_pt49_physical_glyph_authority") is not False or row12ar.get("candidate_selected_batch_12ar") is not False or row12ar.get("candidate_collapsed_batch_12ar") is not False or row12ar.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AR candidate/algorithm firewall regressed")
    if matrix.get("audit_summary", {}).get("confirmed_provenance_metadata_defect_count") != 11 or matrix.get("audit_summary", {}).get("repaired_provenance_metadata_defect_count") != 11:
        fail("Batch 12AR provenance accounting should remain 11/11")

    invariants = state.get("invariants", {})
    if invariants.get("deterministic_fusion_chart_product_r1") != matrix.get("deterministic_product_state"):
        fail("deterministic product state drift between current-state and matrix")
    if invariants.get("ziwei_self_inward_transformation_direction") != matrix.get("self_inward_transformation_state"):
        fail("self/inward transformation state drift between current-state and matrix")

    matrix_summary = matrix.get("inventory_summary", {})
    audit_summary = matrix.get("audit_summary", {})
    audit_state = state.get("historical_audit", {})
    parity = {
        "row_count": matrix_summary.get("row_count"),
        "audited_row_count": matrix_summary.get("audited_row_count"),
        "confirmed_provenance_metadata_defect_count": audit_summary.get("confirmed_provenance_metadata_defect_count"),
        "repaired_provenance_metadata_defect_count": audit_summary.get("repaired_provenance_metadata_defect_count"),
        "historical_candidate_registry_count": audit_summary.get("historical_candidate_registry_count"),
        "historical_candidate_runtime_resolver_count": audit_summary.get("historical_candidate_runtime_resolver_count"),
        "identified_missing_candidate_family_count": audit_summary.get("identified_missing_candidate_family_count"),
    }
    for key, expected in parity.items():
        if audit_state.get(key) != expected:
            fail(f"current-state historical audit parity mismatch for {key}: state={audit_state.get(key)!r} matrix={expected!r}")

    # Provenance/access-only batches can advance without changing any Matrix row.
    # The Matrix batch ledger remains an exact prefix; state may append explicitly
    # documented zero-row-effect batches after that prefix.
    matrix_batches = matrix.get("historical_research_batches", [])
    state_batches = audit_state.get("completed_batches", [])
    if state_batches[: len(matrix_batches)] != matrix_batches:
        fail("current-state completed batch prefix differs from Historical Audit Matrix")
    if state_batches[len(matrix_batches) :] != SUPPLEMENTAL_BATCH_IDS:
        fail("unexpected supplemental provenance/access batch list after Historical Audit Matrix prefix")
    if audit_state.get("latest_batch_doc") != LATEST_BATCH_DOC:
        fail(f"current-state latest batch drift: {audit_state.get('latest_batch_doc')!r}")

    # Batch 11U remains the controlling catalog-item identity gate.
    if identity_evidence.get("status") != "DIRECT_NO_OCR_1940_PRECIOUS_BOOK_NUMBER_893_BINDING_CLOSES_CATALOG_ITEM_CONTINUITY":
        fail("Batch 11U machine evidence status mismatch")
    source_object = identity_evidence.get("source_object", {})
    if source_object.get("book_cd") != "GK26786_00" or source_object.get("item_cd") != "BBG":
        fail("Batch 11U 1940 provider-object binding regressed")
    if source_object.get("renderer_page_count") != 148 or source_object.get("ocr_used") is not False:
        fail("Batch 11U 1940 renderer/no-OCR controls regressed")
    header = identity_evidence.get("internal_catalog_header", {})
    if header.get("page_id") != "0125" or header.get("visible_title") != "奎章閣貴重圖書目錄":
        fail("Batch 11U internal precious-catalog header binding regressed")
    for field in ("書名", "圖書番號", "冊數", "備考"):
        if field not in header.get("visible_field_headers", ()):
            fail(f"Batch 11U lost direct table-field header: {field}")
    entry = identity_evidence.get("direct_entry_binding", {})
    target_entry = entry.get("target_entry", {})
    adjacent = entry.get("adjacent_control_entry", {})
    if entry.get("page_id") != "0129":
        fail("Batch 11U target-entry page binding regressed")
    if target_entry.get("title") != "授時曆立成" or target_entry.get("book_number") != 893 or target_entry.get("volume_count") != 1:
        fail("Batch 11U 授時曆立成 / 圖書番號 893 direct reading regressed")
    if adjacent.get("title") != "授時曆捷法立成" or adjacent.get("book_number") != 892:
        fail("Batch 11U adjacent Kang-Bo control regressed")
    current_binding = identity_evidence.get("current_object_binding", {})
    if current_binding.get("current_catalog_identifier") != "奎貴893" or current_binding.get("current_book_cd") != "GK00893_00":
        fail("Batch 11U current G893 binding regressed")
    if current_binding.get("exact_item_continuity_to_current_gk00893_00") != "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL":
        fail("Batch 11U catalog-item continuity closure regressed")
    control_1930 = identity_evidence.get("1930_control", {})
    if control_1930.get("generic_numeric_order_893_as_current_precious_893") != "DISPROVEN_BY_DIRECT_1930_PAGE_READING":
        fail("Batch 11U 1930 generic-number disproof regressed")
    if identity_evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11U G893 target-page fail-closed status regressed")

    if mf_pdf_evidence.get("status") != "DIRECT_MF_PDF_ROUTE_CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED":
        fail("Batch 11V machine mf_pdf_evidence status mismatch")
    if mf_pdf_evidence.get("book_cd") != "GK00893_00" or mf_pdf_evidence.get("item_cd") != "SIC" or mf_pdf_evidence.get("volume_id") != "0001":
        fail("Batch 11V G893 object/volume binding regressed")
    if mf_pdf_evidence.get("catalog_identifier") != "奎貴893" or mf_pdf_evidence.get("title") != "授時曆立成":
        fail("Batch 11V G893 title/catalog binding regressed")
    if mf_pdf_evidence.get("microfilm_number") != "M/F73-102-37-A":
        fail("Batch 11V microfilm catalog number regressed")
    if mf_pdf_evidence.get("ocr_used") is not False:
        fail("Batch 11V no-OCR boundary regressed")

    probe = mf_pdf_evidence.get("direct_provider_probe", {})
    initial = probe.get("initial_list_probe", {})
    returned = initial.get("returned_volume", {})
    if initial.get("workflow_run_id") != 34044864073 or initial.get("artifact_id") != 9992787144:
        fail("Batch 11V initial M/F list probe provenance regressed")
    if initial.get("list_transport_http_200") is not True or initial.get("list_result") != "ERROR - DIR NOT EXIST":
        fail("Batch 11V M/F list route result regressed")
    expected_returned = {
        "CALL_NUM": "奎貴893",
        "ORI_TIT": "授時曆立成",
        "BOOK_CD": "GK00893_00",
        "ITEM_CD": "SIC",
        "VOL_NO": "0001",
    }
    for key, expected in expected_returned.items():
        if returned.get(key) != expected:
            fail(f"Batch 11V returned G893 volume metadata regressed for {key}")
    if returned.get("IS_PDF") is not None:
        fail("Batch 11V unexpectedly claims an IS_PDF value")

    direct = probe.get("direct_pdf_control", {})
    if direct.get("workflow_run_id") != 34044991699 or direct.get("artifact_id") != 9992817769:
        fail("Batch 11V direct-PDF control provenance regressed")
    if direct.get("list_result") != "ERROR - DIR NOT EXIST" or direct.get("is_pdf_values") != [None]:
        fail("Batch 11V direct-PDF list-state regressed")
    if direct.get("direct_transport_http_200") is not True:
        fail("Batch 11V direct mfPdf transport no longer records HTTP 200")
    if direct.get("direct_pdf_magic") is not False or direct.get("direct_pdf_returned") is not False:
        fail("Batch 11V must remain closed unless a real PDF object is directly observed")

    adjudication = mf_pdf_evidence.get("adjudication", {})
    if adjudication.get("mf_pdf_route_status") != "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED":
        fail("Batch 11V route closure state regressed")
    if adjudication.get("renderer_route_retried") is not False:
        fail("Batch 11V must remain a distinct M/F route, not a renderer retry")
    if mf_pdf_evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11V G893 target-page fail-closed status regressed")

    boundaries = mf_pdf_evidence.get("epistemic_boundaries", {})
    required_boundaries = {
        "mf_pdf_ui_marker_as_downloadable_pdf_proof": "FORBIDDEN",
        "microfilm_catalog_number_as_online_pdf_presence": "FORBIDDEN",
        "error_dir_not_exist_as_physical_microfilm_absence": "FORBIDDEN",
        "returned_thumbnail_filename_as_target_folio_binding": "FORBIDDEN",
        "technical_endpoint_success_as_target_glyph_authority": "FORBIDDEN",
    }
    for key, expected in required_boundaries.items():
        if boundaries.get(key) != expected:
            fail(f"Batch 11V epistemic boundary regressed: {key}")

    # Batch 11W upgrades the 1998 specialist paper to a direct official record/abstract witness.
    if article_evidence.get("status") != "DIRECT_OFFICIAL_JOURNAL_RECORD_AND_ABSTRACT_BOUND_FULLTEXT_REMAINS_CNKI_ROUTED_NO_TARGET_PAGE_EXPOSED":
        fail("Batch 11W machine article_evidence status mismatch")
    archive = article_evidence.get("official_archive", {})
    if archive.get("paper_uuid") != "5c4276d953bd47ca2679c70209d179cf":
        fail("Batch 11W official paper UUID regressed")
    if archive.get("title") != "朝鲜奎章阁本的《授时历立成》" or archive.get("authors") != ["李银姬", "景冰"]:
        fail("Batch 11W title/author identity regressed")
    if archive.get("year_id") != "adaf0591-da7f-47b1-a26b-f97893bc2011" or archive.get("issue_id") != "081bfc10-b643-4702-9389-346193d8815e":
        fail("Batch 11W official 1998-02 issue binding regressed")
    if archive.get("cnki_node_id") != "ZGKS802.008":
        fail("Batch 11W CNKI node binding regressed")
    if archive.get("paper_html_sha256") != "e36670c425afd627551d25acec219eb1b4c7cb4285edef6aceff83adaf454825":
        fail("Batch 11W official paper HTML digest regressed")
    access = article_evidence.get("access_boundary", {})
    if access.get("official_portal_abstract_visible") is not True or access.get("official_portal_references_visible") is not True:
        fail("Batch 11W direct official abstract/reference surface regressed")
    if access.get("official_portal_fulltext_visible") is not False or access.get("full_article_directly_retrieved") is not False:
        fail("Batch 11W must not claim direct full-article retrieval")
    if access.get("public_target_figure_exposed_on_official_portal") is not False:
        fail("Batch 11W must not claim a public target figure")
    if article_evidence.get("paywall_or_auth_bypass_attempted") is not False:
        fail("Batch 11W access-boundary control regressed")
    if article_evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11W G893 target-page fail-closed status regressed")

    lee_source = next(
        (item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-LEE-JING-KYUJANGGAK-SHOUSHI-LICHENG-1998"),
        None,
    )
    if not lee_source:
        fail("Batch 11W Lee/Jing source registry entry missing")
    official_binding = lee_source.get("official_archive_binding", {})
    if official_binding.get("paper_uuid") != "5c4276d953bd47ca2679c70209d179cf" or official_binding.get("cnki_node_id") != "ZGKS802.008":
        fail("Batch 11W source-registry official archive binding regressed")
    if lee_source.get("target_effect") != "NONE_ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11W source-registry target-effect boundary regressed")

    # Batch 11X binds the official institutional reproduction route without claiming fulfillment.
    if evidence.get("status") != "OFFICIAL_REPRODUCTION_APPLICATION_ROUTE_DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED":
        fail("Batch 11X machine evidence status mismatch")
    obj = evidence.get("g893_object", {})
    if obj.get("catalog_identifier") != "奎貴893" or obj.get("book_cd") != "GK00893_00":
        fail("Batch 11X G893 object identity regressed")
    if obj.get("microfilm_number") != "M/F73-102-37-A" or obj.get("reproduction_request_ui_visible") is not True:
        fail("Batch 11X object-specific reproduction route regressed")
    service = evidence.get("official_service_notice", {}).get("direct_observations", {})
    if service.get("microfilm_method") != "MICROFILM_SCAN_PDF_UPLOADED_TO_HOMEPAGE":
        fail("Batch 11X official microfilm PDF publication method regressed")
    if service.get("procedure") != ["HOMEPAGE", "SEARCH_MATERIAL", "REPRODUCTION_REQUEST", "CHECK_APPROVAL_EMAIL"]:
        fail("Batch 11X official application procedure regressed")
    if service.get("normal_processing_period") != "WITHIN_2_WEEKS_OF_APPLICATION_UNLESS_DELAY_SEPARATELY_NOTIFIED":
        fail("Batch 11X processing-period statement regressed")
    nonmember = evidence.get("nonmember_cart_surface", {})
    if nonmember.get("observed_service_change_effective_date") != "2024-02-01":
        fail("Batch 11X 2024 service-change date regressed")
    if "MICROFILM_SCAN_PDF" not in nonmember.get("observed_change", ""):
        fail("Batch 11X non-member PDF-publication transition regressed")
    if evidence.get("external_application_submitted") is not False or evidence.get("approval_received") is not False:
        fail("Batch 11X must not claim a submitted or approved request")
    route = evidence.get("route_adjudication", {})
    if route.get("g893_request_acceptance") != "UNTESTED" or route.get("whole_volume_vs_selected_pages") != "UNRESOLVED_UNTIL_REQUEST_FORM_OR_APPROVAL":
        fail("Batch 11X fulfillment uncertainty regressed")
    if route.get("fee_or_charge") != "NOT_STATED_IN_REVIEWED_OFFICIAL_NOTICE_DO_NOT_INFER_FREE":
        fail("Batch 11X fee boundary regressed")
    if evidence.get("target_status") != "ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11X target-page fail-closed status regressed")
    g893_source = next(
        (item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-KYUJANGGAK-SHOUSHI-LICHENG-G893"),
        None,
    )
    if not g893_source:
        fail("Batch 11X G893 registry source missing")
    reproduction = g893_source.get("official_reproduction_route", {})
    if reproduction.get("status") != "DIRECTLY_CONFIRMED_REQUEST_NOT_SUBMITTED" or reproduction.get("request_submitted") is not False:
        fail("Batch 11X registry reproduction route regressed")
    if reproduction.get("target_effect") != "NONE_ALL_SIX_PENDING_DIRECT_TARGET_PAGE":
        fail("Batch 11X registry target boundary regressed")

    if ziwei_late_zi_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-LATE-ZI-FACSIMILE-A":
        fail("Batch 12A Ziwei late-Zi evidence batch identity mismatch")
    source_obj = ziwei_late_zi_evidence.get("source_object", {})
    if source_obj.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7" or source_obj.get("pdf_page_count") != 527:
        fail("Batch 12A Ziwei Fullbook PDF identity regressed")
    direct = ziwei_late_zi_evidence.get("direct_collation", {})
    if direct.get("pdf_page_1_based") != 320 or direct.get("heading") != "論人生時要審的確":
        fail("Batch 12A target-section binding regressed")
    if direct.get("s01_claimed_sentence_status") != "NOT_OBSERVED_ON_DIRECT_TARGET_SECTION_PAGE" or direct.get("whole_volume_negative_claim_authorized") is not False:
        fail("Batch 12A S01 exact-quotation scope firewall regressed")
    philology = ziwei_late_zi_evidence.get("philological_adjudication", {})
    if philology.get("candidate_method_id") != "NANYANGTANG-FULLBOOK-ZI-TEN-KE-HAI-SPLIT-R1":
        fail("Batch 12A candidate identity regressed")
    if philology.get("runtime_capability_status") != "MISSING_FROM_PRODUCT" or philology.get("runtime_selection_authorized") is not False:
        fail("Batch 12A missing-product / no-selection boundary regressed")
    nanyang_source = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-ZIWEI-QUANSHU-NANYANGTANG-SCAN"), None)
    if not nanyang_source or nanyang_source.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7":
        fail("Batch 12A external-source registry binding regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12A HPA-ZDATE-006 continuity boundary regressed")

    if ziwei_timekeeping_evidence.get("batch_id") != "BATCH-12-ZIWEI-LATE-ZI-TIMEKEEPING-B":
        fail("Batch 12B Ziwei timekeeping evidence batch identity mismatch")
    adjudication = ziwei_timekeeping_evidence.get("adjudication", {})
    if adjudication.get("upper_half_orientation") != "BEFORE_MIDNIGHT_PREVIOUS_DAY" or adjudication.get("lower_half_orientation") != "AFTER_MIDNIGHT_CURRENT_DAY":
        fail("Batch 12B generic upper/lower-half orientation regressed")
    if adjudication.get("ten_ke_equal_duration_interpretation") != "REJECTED":
        fail("Batch 12B ten-ke equal-duration interpretation firewall regressed")
    if adjudication.get("runtime_time_standard_binding") != "UNRESOLVED":
        fail("Batch 12B runtime time-standard was prematurely selected")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("timekeeping_orientation_status") != "CLOSED_AT_GENERIC_FIXED_SHICHEN_LEVEL":
        fail("Batch 12B matrix timekeeping status regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12B candidate/product boundary regressed")

    if ziwei_edition_routes_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-INDEPENDENT-EDITION-ROUTES-C":
        fail("Batch 12C Ziwei edition-route evidence batch identity mismatch")
    route_workflow = ziwei_edition_routes_evidence.get("research_workflow", {})
    if route_workflow.get("workflow_run_id") != 34120317222 or route_workflow.get("artifact_id") != 10017909080:
        fail("Batch 12C exact workflow/artifact provenance regressed")
    wenguang = ziwei_edition_routes_evidence.get("heart_one_wenguangtang_facsimile", {})
    if wenguang.get("isbn") != "9789888266944" or wenguang.get("official_probe", {}).get("http_status") != 200:
        fail("Batch 12C Wenguangtang facsimile identity regressed")
    if {row.get("name") for row in wenguang.get("publisher_described_base_copies", ())} != {"敦化堂刊本", "繼述堂刊本"}:
        fail("Batch 12C Dunhuatang/Jishutang base-copy identity regressed")
    wencheng = ziwei_edition_routes_evidence.get("wenchengtang_route", {})
    if wencheng.get("relation_to_wenguangtang_family") != "SEPARATE_QING_FULLBOOK_EDITION_ROUTE":
        fail("Batch 12C Wenchengtang independence boundary regressed")
    preview = ziwei_edition_routes_evidence.get("public_preview_controls", {}).get("books_preview_image_urls", {})
    if preview.get("attempted_count") != 13 or preview.get("http_403_count") != 13 or preview.get("saved_image_count") != 0:
        fail("Batch 12C public-preview access controls regressed")
    route_adjudication = ziwei_edition_routes_evidence.get("adjudication", {})
    if route_adjudication.get("independent_physical_target_page_status") != "NO_INDEPENDENT_TARGET_PAGE_OBSERVED":
        fail("Batch 12C incorrectly claims a physical target page")
    if route_adjudication.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12C HAI glyph stability boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or "NANYANGTANG_AND_GUANGYI_DIRECT_PHYSICAL_FULLBOOK_EDITIONS_BOTH_HAVE" not in nanyang_row.get("hai_glyph_cross_edition_status", ""):
        fail("Batch 12AF matrix Nanyangtang/Guangyi HAI agreement regressed")
    if "GLOBAL_ALL_FULLBOOK_EDITION_STABILITY_NOT_CLAIMED" not in nanyang_row.get("hai_glyph_cross_edition_status", ""):
        fail("Batch 12AF matrix global Fullbook stability firewall regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12C candidate/product boundary regressed")

    if ziwei_wenguang_index_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-WENGUANG-INDEX-PREVIEW-D":
        fail("Batch 12D Ziwei Wenguang index evidence batch identity mismatch")
    distribution = ziwei_wenguang_index_evidence.get("distribution_volume", {})
    if distribution.get("volume_id") != "aIRbDgAAQBAJ" or distribution.get("isbn") != "9789888266944" or distribution.get("declared_page_count") != 266:
        fail("Batch 12D Google distribution identity regressed")
    search_index = ziwei_wenguang_index_evidence.get("public_search_index", {})
    if search_index.get("workflow_run_id") != 34121750009 or search_index.get("artifact_id") != 10018452113:
        fail("Batch 12D search-index provenance regressed")
    if search_index.get("target_heading_query", {}).get("target_page_id") != "PT165":
        fail("Batch 12D target PT165 binding regressed")
    reading = search_index.get("target_index_reading", "")
    if "上五刻" not in reading or "下五刻" not in reading or "亥時" not in reading:
        fail("Batch 12D target index text regressed")
    if search_index.get("target_index_reading_authority") != "SEARCH_INDEX_TEXT_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY":
        fail("Batch 12D index/glyph authority boundary regressed")
    if search_index.get("negative_textual_claim_authorized") is not False:
        fail("Batch 12D zero-result negative-proof firewall regressed")
    viewer = ziwei_wenguang_index_evidence.get("embedded_viewer_control", {})
    if viewer.get("workflow_run_id") != 34123161798 or viewer.get("artifact_id") != 10019011766:
        fail("Batch 12D Embedded Viewer provenance regressed")
    if viewer.get("go_to_pt165_returned") is not True or viewer.get("after_page_id") != "PT166" or viewer.get("target_page_directly_observed") is not False:
        fail("Batch 12D viewer fail-closed state regressed")
    adjudication12d = ziwei_wenguang_index_evidence.get("adjudication", {})
    if adjudication12d.get("pt165_base_copy_identity") != "UNRESOLVED_DUNHUATANG_VS_JISHUTANG":
        fail("Batch 12D PT165 base-copy identity was prematurely closed")
    if adjudication12d.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12D HAI glyph stability boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("combined_facsimile_volume_id") != "aIRbDgAAQBAJ" or nanyang_row.get("combined_facsimile_target_index_page_id") != "PT165":
        fail("Batch 12D matrix Google index binding regressed")
    if nanyang_row.get("combined_facsimile_target_image_status") != "PUBLIC_EMBEDDED_VIEWER_DID_NOT_DISPLAY_TARGET_GLYPHS":
        fail("Batch 12D matrix viewer boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12D candidate/product boundary regressed")

    if ziwei_jingluntang_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-JINGLUNTANG-PHYSICAL-ROUTE-E":
        fail("Batch 12E Ziwei Jingluntang evidence batch identity mismatch")
    shlib = ziwei_jingluntang_evidence.get("shanghai_library", {})
    if shlib.get("instance_id") != "1pjr6vy1ffsq3l1y" or shlib.get("identifier") != "子30814110" or shlib.get("edition_label") != "清經綸堂刻本":
        fail("Batch 12E SHLIB Jingluntang identity regressed")
    if shlib.get("public_content_negotiation", {}).get("jsonld", {}).get("http_status") != 200:
        fail("Batch 12E SHLIB JSON-LD route regressed")
    if shlib.get("anonymous_route_controls", {}).get("dhapi_pdfview_root", {}).get("http_status") != 412:
        fail("Batch 12E SHLIB anonymous digital-object boundary regressed")
    token_scan = shlib.get("public_metadata_token_scan", {})
    if any(token_scan.get(key) for key in ("iiif", "manifest", "itemid", "itemId", "dhapi", "pdfview")):
        fail("Batch 12E SHLIB metadata unexpectedly exposes a page object")
    kumyo = ziwei_jingluntang_evidence.get("kumyo_physical_copy", {})
    if kumyo.get("auction_no") != "BBAA18036" or kumyo.get("unique_embedded_physical_image_count") != 8:
        fail("Batch 12E Kumyo physical-copy identity regressed")
    if len(kumyo.get("unique_image_sha256", ())) != 8 or len(set(kumyo.get("unique_image_sha256", ()))) != 8:
        fail("Batch 12E Kumyo unique image digest set regressed")
    if kumyo.get("jingluntang_label_visibly_observed") is not True:
        fail("Batch 12E Kumyo Jingluntang label visual-review boundary regressed")
    if kumyo.get("target_heading_observed") is not False or kumyo.get("target_hai_glyph_observed") is not False:
        fail("Batch 12E incorrectly claims the late-Zi target page")
    adjudication12e = ziwei_jingluntang_evidence.get("adjudication", {})
    if adjudication12e.get("jingluntang_edition_family_identity") != "CLOSED_AT_LIBRARY_AND_PUBLIC_PHYSICAL_COPY_LEVEL":
        fail("Batch 12E Jingluntang identity closure regressed")
    if adjudication12e.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12E HAI glyph stability boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or "子30814110" not in nanyang_row.get("jingluntang_library_instance", ""):
        fail("Batch 12E matrix Jingluntang binding regressed")
    if nanyang_row.get("jingluntang_public_image_review_status") != "EIGHT_UNIQUE_PHYSICAL_IMAGES_DIRECTLY_REVIEWED_NO_TARGET_SECTION":
        fail("Batch 12E matrix physical-image review boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12E candidate/product boundary regressed")


    if ziwei_post_e_routes_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-F":
        fail("Batch 12F post-12E route evidence batch identity mismatch")
    liaoning12f = ziwei_post_e_routes_evidence.get("liaoning_wenchengtang_route", {})
    institutional12f = liaoning12f.get("institutional_route_witness", {})
    locator12f = liaoning12f.get("secondary_locator", {})
    if institutional12f.get("http_status") != 200 or institutional12f.get("legacy_catalog_route_bound") is not True:
        fail("Batch 12F Liaoning institutional route binding regressed")
    if locator12f.get("authority") != "SECONDARY_CATALOG_LOCATOR_ONLY_NOT_LIBRARY_PRIMARY_RECORD":
        fail("Batch 12F Liaoning secondary-locator authority ceiling regressed")
    if liaoning12f.get("target_page_observed") is not False or "OFFICIAL_LIAONING_TARGET_RECORD_NOT_RETRIEVED" not in liaoning12f.get("adjudication", ""):
        fail("Batch 12F Liaoning target-record boundary regressed")
    dalian12f = ziwei_post_e_routes_evidence.get("dalian_guangyi_route", {})
    direct12f = dalian12f.get("direct_catalog_identity", {})
    if dalian12f.get("direct_item_http_status") != 200 or direct12f.get("edition") != "石印本" or direct12f.get("publication_statement") != "廣益書局 民國":
        fail("Batch 12F Dalian official Guangyi identity regressed")
    if direct12f.get("juan") != "四卷" or direct12f.get("physical_form") != "四冊一函":
        fail("Batch 12F Dalian physical-form identity regressed")
    image12f = dalian12f.get("public_image_candidate_review", {})
    if image12f.get("successfully_saved_image_count") != 6 or image12f.get("direct_visual_review_completed") is not True:
        fail("Batch 12F Dalian image visual-review count regressed")
    if image12f.get("classification") != "ALL_SIX_SAVED_IMAGES_ARE_SITE_UI_ASSETS_NOT_BOOK_PAGES" or image12f.get("target_page_observed") is not False:
        fail("Batch 12F Dalian UI-asset/book-page firewall regressed")
    search12f = dalian12f.get("published_get_form_search_control", {})
    if search12f.get("query_count") != 14 or search12f.get("negative_catalog_conclusion_authorized") is not False:
        fail("Batch 12F Dalian search-control boundary regressed")
    if search12f.get("every_query_term_present_in_returned_text") is not False or search12f.get("every_query_ziwei_present_in_returned_text") is not False:
        fail("Batch 12F Dalian returned-page query-reflection control regressed")
    jielan12f = ziwei_post_e_routes_evidence.get("jielan_wenchengtang_collation_index", {})
    if jielan12f.get("volume_id") != "rZRcCwAAQBAJ" or jielan12f.get("authority_ceiling") != "EDITORIAL_COLLATION_AND_SEARCH_INDEX_ONLY_NOT_DIRECT_WENCHENGTANG_GLYPH":
        fail("Batch 12F Jielan/Wenchengtang authority ceiling regressed")
    controls12f = jielan12f.get("controls", {})
    if controls12f.get("wenchengtang_result_counts") != [1, 1, 1] or controls12f.get("wenchengtang_page_ids") != ["PT176"]:
        fail("Batch 12F Jielan Wenchengtang PT176 index binding regressed")
    if controls12f.get("exact_target_heading_result_counts") != [0, 0, 0] or jielan12f.get("zero_results_as_negative_proof_authorized") is not False:
        fail("Batch 12F zero-result negative-proof firewall regressed")
    adjudication12f = ziwei_post_e_routes_evidence.get("adjudication", {})
    if adjudication12f.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adjudication12f.get("hai_glyph_stability_across_physical_editions") != "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES":
        fail("Batch 12F HPA-ZDATE-006 fail-closed state regressed")
    if adjudication12f.get("algorithm_reopen_authorized") is not False or adjudication12f.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12F algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("batch_12f_route_artifact") != "docs/research/ZIWEI-QUANSHU-WENCHENGTANG-DALIAN-COLLATION-ROUTES-R1.json":
        fail("Batch 12F matrix route-artifact binding regressed")
    if nanyang_row.get("wenchengtang_target_late_zi_glyph_status") != "NOT_DIRECTLY_OBSERVED":
        fail("Batch 12F matrix Wenchengtang glyph boundary regressed")
    if nanyang_row.get("audit_status") != "MISSING_FROM_PRODUCT" or nanyang_row.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12F candidate/product boundary regressed")


    if ziwei_quanji_late_zi_evidence.get("batch_id") != "BATCH-12-ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-G":
        fail("Batch 12G Quanji evidence batch identity mismatch")
    pub12g = ziwei_quanji_late_zi_evidence.get("publisher_lianyuange_route", {})
    if pub12g.get("http_status") != 200 or pub12g.get("lianyuange_present") is not True or pub12g.get("quanji_present") is not True:
        fail("Batch 12G Lianyuange publisher-route binding regressed")
    idx12g = ziwei_quanji_late_zi_evidence.get("google_books_jielan_index", {})
    if idx12g.get("volume_id") != "rZRcCwAAQBAJ" or idx12g.get("workflow_run_id") != 34133129317 or idx12g.get("artifact_id") != 10022892119:
        fail("Batch 12G Google Books provenance regressed")
    if idx12g.get("lianyuange_query", {}).get("page_ids") != ["PT176", "PT177"]:
        fail("Batch 12G Lianyuange PT176/PT177 index binding regressed")
    anomaly12g = idx12g.get("ten_ke_query_anomaly", {})
    if anomaly12g.get("page_id") != "PT88" or anomaly12g.get("snippet_contains_query_term") is not False or anomaly12g.get("positive_target_evidence_authorized") is not False:
        fail("Batch 12G ten-ke index-mismatch firewall regressed")
    if idx12g.get("zero_result_as_negative_textual_proof") != "FORBIDDEN" or idx12g.get("physical_lianyuange_target_page_observed") is not False:
        fail("Batch 12G index/physical target fail-closed boundary regressed")
    rec12g = ziwei_quanji_late_zi_evidence.get("received_quanji_transcription_control", {})
    if rec12g.get("authority") != "SECONDARY_RECEIVED_TRANSCRIPTION_ONLY_NOT_PHYSICAL_GLYPH_AUTHORITY":
        fail("Batch 12G received-transcription authority ceiling regressed")
    controls12g = rec12g.get("controls", {})
    for key in ("ten_ke_present", "upper_five_previous_night_present", "lower_five_current_night_zi_present"):
        if controls12g.get(key) is not True:
            fail(f"Batch 12G received Quanji control missing: {key}")
    phil12g = ziwei_quanji_late_zi_evidence.get("philological_adjudication", {})
    if phil12g.get("relation_to_nanyangtang_fullbook") != "PARALLEL_BUT_NOT_MECHANICALLY_IDENTICAL":
        fail("Batch 12G philological relation regressed")
    if phil12g.get("new_candidate_row_authorized") is not False or phil12g.get("hpa_zdate_006_reclassification_authorized") is not False:
        fail("Batch 12G candidate/reclassification firewall regressed")
    adj12g = ziwei_quanji_late_zi_evidence.get("adjudication", {})
    if adj12g.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12g.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12G product/algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("quanji_lianyuange_collation_artifact") != "docs/research/ZIWEI-QUANJI-LIANYUANGE-LATE-ZI-COLLATION-R1.json":
        fail("Batch 12G Matrix Quanji artifact binding regressed")
    if nanyang_row.get("quanji_candidate_formalization_status") != "NOT_AUTHORIZED_PENDING_DIRECT_PHYSICAL_TARGET_PAGE":
        fail("Batch 12G Matrix candidate-formalization boundary regressed")


    if ziwei_japan_ming_fullbook_evidence.get("batch_id") != "BATCH-12-ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-H":
        fail("Batch 12H Japan Ming Fullbook evidence batch identity mismatch")
    naj12h = ziwei_japan_ming_fullbook_evidence.get("national_archives_japan", {})
    idx12h = naj12h.get("official_public_search_index_observation", {})
    if idx12h.get("call_number") != "子０６０－０００１" or idx12h.get("bibliographic_label") != "刊本:明:::" or idx12h.get("quantity") != "2冊":
        fail("Batch 12H NAJ Ming Fullbook identity regressed")
    if idx12h.get("first_item", {}).get("id") != "4468520" or idx12h.get("first_item", {}).get("access_class") != "公開":
        fail("Batch 12H NAJ first digital-item binding regressed")
    runner12h = naj12h.get("github_runner_route_probe", {})
    if runner12h.get("workflow_run_id") != 34134081787 or runner12h.get("artifact_id") != 10023248966:
        fail("Batch 12H NAJ runner provenance regressed")
    if runner12h.get("all_routes_http_status") != 403 or runner12h.get("adjudication") != "GITHUB_RUNNER_ACCESS_BOUNDARY_ONLY_NOT_ARCHIVE_CONTENT_ABSENCE":
        fail("Batch 12H NAJ runner-access boundary regressed")
    sdu12h = ziwei_japan_ming_fullbook_evidence.get("sdu_formal_facsimile_route", {})
    if sdu12h.get("direct_workflow_capture", {}).get("workflow_run_id") != 34134328002 or sdu12h.get("direct_workflow_capture", {}).get("artifact_id") != 10023353526:
        fail("Batch 12H SDU facsimile provenance regressed")
    statement12h = sdu12h.get("direct_catalog_statement", {})
    if statement12h.get("work") != "《新鋟希夷陳先生紫微斗數全書》七卷" or statement12h.get("base_copy") != "據内閣文庫藏明刊本" or statement12h.get("reproduction") != "影印":
        fail("Batch 12H SDU formal facsimile statement regressed")
    ncku12h = ziwei_japan_ming_fullbook_evidence.get("ncku_scholarly_genealogy", {})
    if ncku12h.get("direct_pdf_capture", {}).get("sha256") != "17d0089c3328253230cb2f110ac40527abe41fbb97183483215a5e633e5b2e2e":
        fail("Batch 12H NCKU PDF binding regressed")
    if ncku12h.get("visual_review", {}).get("ocr_used") is not False or ncku12h.get("visual_review", {}).get("reviewed_printed_pages") != [60, 61]:
        fail("Batch 12H NCKU no-OCR visual-review boundary regressed")
    toyo12h = ziwei_japan_ming_fullbook_evidence.get("toyo_bunko_quanji_catalog_control", {})
    if toyo12h.get("official_catalog_controls", {}).get("callmark") != "VII-3-157":
        fail("Batch 12H Toyo callmark regressed")
    labels12h = [x.get("publication_label") for x in toyo12h.get("official_catalog_controls", {}).get("entries", [])]
    if "鈔本" not in labels12h or "寫本" not in labels12h:
        fail("Batch 12H Toyo manuscript/copy labels regressed")
    if not toyo12h.get("discrepancy_with_ncku_print_genealogy", "").startswith("PRESERVE_UNRESOLVED"):
        fail("Batch 12H Toyo/NCKU provenance discrepancy was prematurely collapsed")
    adj12h = ziwei_japan_ming_fullbook_evidence.get("adjudication", {})
    if adj12h.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12h.get("japan_target_page") != "NOT_OBSERVED":
        fail("Batch 12H target-page/product boundary regressed")
    if adj12h.get("algorithm_reopen_authorized") is not False or adj12h.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12H algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("japan_ming_fullbook_route_artifact") != "docs/research/ZIWEI-JAPAN-MING-FULLBOOK-FACSIMILE-ROUTES-R1.json":
        fail("Batch 12H Matrix Japan route binding regressed")
    if nanyang_row.get("japan_target_late_zi_page_status") != "NOT_OBSERVED":
        fail("Batch 12H Matrix target-page boundary regressed")

    # Batch 12I closes post-12H duplicate-lineage and locator controls without adding a target glyph witness.
    if ziwei_late_zi_dedup_locator_evidence.get("batch_id") != "BATCH-12-ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-I":
        fail("Batch 12I evidence batch identity mismatch")
    dedup12i = ziwei_late_zi_dedup_locator_evidence.get("nanyangtang_naaj_copy_dedup", {})
    if dedup12i.get("independent_witness_count_policy") != "DO_NOT_DOUBLE_COUNT_SAME_PHYSICAL_COPY_OR_DIGITIZATION_LINEAGE":
        fail("Batch 12I duplicate-lineage witness-count firewall regressed")
    if dedup12i.get("direct_hai_glyph_witness_count_added") != 0:
        fail("Batch 12I incorrectly added a duplicate Hai-glyph witness")
    zihai12i = ziwei_late_zi_dedup_locator_evidence.get("zihai_google_books_locator", {})
    standalone12i = zihai12i.get("standalone_target_fullbook", {})
    if standalone12i.get("google_books_volume_id") != "kxdy0QEACAAJ" or standalone12i.get("target_page_observed") is not False:
        fail("Batch 12I standalone Zihai Fullbook locator boundary regressed")
    if zihai12i.get("formal_set", {}).get("exact_set_subvolume") != "UNRESOLVED":
        fail("Batch 12I prematurely resolved the Zihai set subvolume")
    wenguang12i = ziwei_late_zi_dedup_locator_evidence.get("wenguang_secondary_comparison_locator", {})
    if wenguang12i.get("google_books_volume_id") != "RISpDgAAQBAJ" or wenguang12i.get("target_late_zi_reading_obtained") is not False:
        fail("Batch 12I Wenguang locator was promoted beyond evidence")
    if wenguang12i.get("unrelated_hai_hits_count_as_late_zi_evidence") is not False:
        fail("Batch 12I unrelated Hai-hour hits were misclassified")
    shidian12i = ziwei_late_zi_dedup_locator_evidence.get("shidian_public_target_page_api_control", {})
    if shidian12i.get("workflow_run_id") != 34138050721 or shidian12i.get("artifact_id") != 10024763004:
        fail("Batch 12I Shidian workflow provenance regressed")
    if shidian12i.get("returned_url_candidate_count") != 0 or shidian12i.get("saved_image_count") != 0:
        fail("Batch 12I unexpectedly claims a returned Shidian image")
    if shidian12i.get("target_physical_page_directly_observed") is not False:
        fail("Batch 12I must not claim direct Shidian target-page glyph observation")
    adj12i = ziwei_late_zi_dedup_locator_evidence.get("adjudication", {})
    if adj12i.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12i.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12I HPA-ZDATE-006 product/evidence boundary regressed")
    if adj12i.get("algorithm_reopen_authorized") is not False or adj12i.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12I algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("batch_12i_dedup_locator_artifact") != "docs/research/ZIWEI-LATE-ZI-DEDUP-LOCATOR-CONTROLS-R1.json":
        fail("Batch 12I Matrix artifact binding regressed")
    if nanyang_row.get("nanyang_naaj_independent_witness_count_policy") != "DO_NOT_DOUBLE_COUNT_SAME_PHYSICAL_COPY_OR_DIGITIZATION_LINEAGE":
        fail("Batch 12I Matrix duplicate-lineage policy regressed")
    if nanyang_row.get("shidian_public_image_object_status") != "NOT_RETURNED":
        fail("Batch 12I Matrix Shidian image boundary regressed")

    # Batch 12J closes a public photographed Guangyi physical-set route without promoting it to target-glyph or independent-stemma authority.
    if ziwei_guangyi_physical_set_evidence.get("batch_id") != "BATCH-12-ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-J":
        fail("Batch 12J evidence batch identity mismatch")
    rw12j = ziwei_guangyi_physical_set_evidence.get("research_workflow", {})
    if rw12j.get("workflow_run_id") != 34140027356 or rw12j.get("artifact_id") != 10025522997:
        fail("Batch 12J research provenance regressed")
    if rw12j.get("artifact_zip_sha256") != "35be2589ac50228eab9a03a77401ad283fb40be1981d4f4bddeab9bd42c06485":
        fail("Batch 12J research artifact digest regressed")
    physical12j = ziwei_guangyi_physical_set_evidence.get("yetnal_public_physical_set", {})
    if physical12j.get("item_http_status") != 200 or len(physical12j.get("image_objects", ())) != 4:
        fail("Batch 12J public physical-set capture regressed")
    visual12j = physical12j.get("direct_visual_review_no_ocr", {})
    if visual12j.get("completed") is not True or visual12j.get("target_section_observed") is not False or visual12j.get("target_hai_glyph_observed") is not False:
        fail("Batch 12J visual target-page boundary regressed")
    if "上海廣益書局印行" not in visual12j.get("image_1", "") or "上海廣益書局印行" not in visual12j.get("image_3", ""):
        fail("Batch 12J direct Guangyi imprint controls regressed")
    bridge12j = ziwei_guangyi_physical_set_evidence.get("batch_12f_dalian_catalog_bridge", {})
    if bridge12j.get("exact_bridge_status") != "UNRESOLVED_PENDING_COLOPHON_DATE_OR_OTHER_PRINTING_SPECIFIC_CONTROL":
        fail("Batch 12J exact Dalian/physical-set identity was prematurely closed")
    phil12j = ziwei_guangyi_physical_set_evidence.get("title_philology", {})
    if phil12j.get("silent_normalization_authorized") is not False or "紫薇斗數全書" not in phil12j.get("photographed_title_surface", ()):
        fail("Batch 12J photographed title-surface philology regressed")
    ncku12j = ziwei_guangyi_physical_set_evidence.get("ncku_genealogy_control", {})
    if ncku12j.get("guangyi_as_fully_independent_textual_stemma_branch") is not False:
        fail("Batch 12J Guangyi stemmatic-dependence firewall regressed")
    adj12j = ziwei_guangyi_physical_set_evidence.get("adjudication", {})
    if adj12j.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12j.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12J HPA-ZDATE-006 evidence boundary regressed")
    if adj12j.get("algorithm_reopen_authorized") is not False or adj12j.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12J algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("guangyi_physical_set_collation_artifact") != "docs/research/ZIWEI-GUANGYI-PHYSICAL-SET-COLLATION-R1.json":
        fail("Batch 12J Matrix artifact binding regressed")
    if nanyang_row.get("guangyi_target_late_zi_page_status") != "NOT_OBSERVED":
        fail("Batch 12J Matrix target-page boundary regressed")
    if nanyang_row.get("guangyi_exact_dalian_catalog_item_bridge") != "UNRESOLVED":
        fail("Batch 12J Matrix exact-item bridge was prematurely closed")

    # Batch 12K locks the combined-Wenguang PT165 provenance boundary.
    if ziwei_wenguang_base_copy_evidence.get("batch_id") != "BATCH-12-ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-K":
        fail("Batch 12K evidence batch identity mismatch")
    rw12k = ziwei_wenguang_base_copy_evidence.get("research_workflow", {})
    if rw12k.get("workflow_run_id") != 34174455835 or rw12k.get("artifact_id") != 10036772401:
        fail("Batch 12K research provenance regressed")
    if rw12k.get("artifact_zip_sha256") != "a5116e6a644fdb1ddd282296c853248fcb2d20ee3f4a7757ba32cef624a68a75":
        fail("Batch 12K artifact digest regressed")
    samples12k = ziwei_wenguang_base_copy_evidence.get("sanmin_public_color_samples", {})
    if samples12k.get("image_count") != 8 or len(samples12k.get("images", ())) != 8:
        fail("Batch 12K Sanmin sample count regressed")
    visual12k = samples12k.get("direct_visual_review_no_ocr", {})
    if visual12k.get("completed") is not True or visual12k.get("target_heading_observed") is not False or visual12k.get("target_hai_glyph_observed") is not False:
        fail("Batch 12K visual target-page boundary regressed")
    if visual12k.get("conspicuous_red_collation_marks_visible_on_samples") != [4, 6]:
        fail("Batch 12K reviewed red-mark controls regressed")
    index12k = ziwei_wenguang_base_copy_evidence.get("google_books_fresh_index_controls", {})
    q12k = index12k.get("queries", {})
    if q12k.get("敦化堂藏板", {}).get("page_ids") != ["PT10", "PT11"]:
        fail("Batch 12K Dunhuatang index controls regressed")
    if q12k.get("繼述堂藏板", {}).get("page_ids") != ["PT10"]:
        fail("Batch 12K Jishutang index control regressed")
    if q12k.get("論人生時要審的確", {}).get("page_ids") != ["PT16", "PT165"]:
        fail("Batch 12K target heading index control regressed")
    if q12k.get("上五刻", {}).get("page_ids") != ["PT165"] or q12k.get("下五刻", {}).get("page_ids") != ["PT165"]:
        fail("Batch 12K target phrase index controls regressed")
    prov12k = ziwei_wenguang_base_copy_evidence.get("provenance_adjudication", {})
    if prov12k.get("pt165_base_copy_identity") != "UNRESOLVED_DUNHUATANG_VS_JISHUTANG":
        fail("Batch 12K PT165 base-copy identity was prematurely selected")
    if prov12k.get("positional_page_range_assignment_authorized") is not False or prov12k.get("red_collation_marks_as_exclusive_jishutang_identifier_authorized") is not False:
        fail("Batch 12K provenance inference firewalls regressed")
    adj12k = ziwei_wenguang_base_copy_evidence.get("adjudication", {})
    if adj12k.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12k.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12K HPA-ZDATE-006 boundary regressed")
    if adj12k.get("algorithm_reopen_authorized") is not False or adj12k.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12K algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("wenguang_public_sample_base_copy_artifact") != "docs/research/ZIWEI-WENGUANG-PUBLIC-SAMPLE-BASE-COPY-PROVENANCE-R1.json":
        fail("Batch 12K Matrix artifact binding regressed")
    if nanyang_row.get("wenguang_pt165_base_copy_identity") != "UNRESOLVED_DUNHUATANG_VS_JISHUTANG":
        fail("Batch 12K Matrix PT165 provenance boundary regressed")

    # Batch 12L preserves a modern typeset received-text witness without inflating old-edition glyph evidence.
    if ziwei_kangjie_typeset_evidence.get("batch_id") != "BATCH-12-ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-L":
        fail("Batch 12L evidence batch identity mismatch")
    src12l = ziwei_kangjie_typeset_evidence.get("source_object", {})
    if src12l.get("pdf_sha256") != "0bbb04a3d274f192f16e1d519fa91f31dc48fab0e440e16ee04109393830cbf8" or src12l.get("pdf_page_count") != 345:
        fail("Batch 12L source PDF identity regressed")
    ident12l = src12l.get("source_identity_direct_visual", {})
    if ident12l.get("title") != "康节说易全书·紫微斗数" or ident12l.get("editor_surface") != "陈明点校" or ident12l.get("publisher_surface") != "学林出版社":
        fail("Batch 12L modern source identity regressed")
    if ident12l.get("format") != "MODERN_TYPESET_NOT_OLD_EDITION_FACSIMILE":
        fail("Batch 12L source format was promoted beyond evidence")
    acq12l = ziwei_kangjie_typeset_evidence.get("acquisition_provenance", {})
    if acq12l.get("frontmatter_probe", {}).get("workflow_run_id") != 34174856657 or acq12l.get("frontmatter_probe", {}).get("artifact_id") != 10036898985:
        fail("Batch 12L frontmatter provenance regressed")
    if acq12l.get("target_page_probe", {}).get("workflow_run_id") != 34175090423 or acq12l.get("target_page_probe", {}).get("artifact_id") != 10036973127:
        fail("Batch 12L target-page provenance regressed")
    mapping12l = ziwei_kangjie_typeset_evidence.get("toc_and_page_mapping", {})
    if mapping12l.get("target_pdf_page_1_based") != 165 or mapping12l.get("target_render_sha256") != "eded525967698552a199b21f0c886043402f8dde3b4b74ca6ef621ab23542824":
        fail("Batch 12L target page/hash binding regressed")
    if mapping12l.get("finite_offset_controls", {}).get("pdf_165_printed_page") != 151:
        fail("Batch 12L PDF-to-printed-page map regressed")
    vis12l = ziwei_kangjie_typeset_evidence.get("direct_visual_target_review_no_ocr", {})
    if vis12l.get("completed") is not True or vis12l.get("target_heading") != "论人生日时要审的确":
        fail("Batch 12L direct target visual review regressed")
    if vis12l.get("upper_five_hai_reading_directly_observed") is not True or vis12l.get("lower_five_current_zi_reading_directly_observed") is not True:
        fail("Batch 12L received-text Hai/Zi reading regressed")
    if vis12l.get("old_edition_photographic_glyph_directly_observed") is not False:
        fail("Batch 12L must not claim old-edition photographic glyph authority")
    adj12l = ziwei_kangjie_typeset_evidence.get("adjudication", {})
    if adj12l.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12l.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12L HPA-ZDATE-006 evidence boundary regressed")
    if adj12l.get("algorithm_reopen_authorized") is not False or adj12l.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12L algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("kangjie_modern_typeset_late_zi_artifact") != "docs/research/ZIWEI-KANGJIE-MODERN-TYPESET-LATE-ZI-WITNESS-R1.json":
        fail("Batch 12L Matrix artifact binding regressed")
    if nanyang_row.get("kangjie_independent_old_edition_witness_count_added") != 0:
        fail("Batch 12L Matrix witness-count firewall regressed")

    # Batch 12M binds the SNU Ilsa 1870 Mingjingge physical-copy/digitization lineage without inventing a target page.
    if ziwei_mingjingge_snu_evidence.get("batch_id") != "BATCH-12-ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-M":
        fail("Batch 12M evidence batch identity mismatch")
    obj12m = ziwei_mingjingge_snu_evidence.get("historical_object", {})
    if obj12m.get("stated_year") != 1870 or obj12m.get("target_volume") != 4 or obj12m.get("target_section") != "五凶神":
        fail("Batch 12M historical object scope regressed")
    snu12m = ziwei_mingjingge_snu_evidence.get("snu_ilsa_copy", {})
    if snu12m.get("call_number_family") != "一簑古523.5-J562b-v.1-6":
        fail("Batch 12M SNU Ilsa call-number binding regressed")
    v112m = snu12m.get("v1_public_physical_controls", {})
    if v112m.get("artifact_id") != 10037255041 or v112m.get("artifact_zip_sha256") != "ba43bff36ac1e01e1c693218504bbed4759edb1e5937186ae8052eb887711a2c":
        fail("Batch 12M v1 physical provenance regressed")
    if v112m.get("cover", {}).get("sha256") != "699da0ece518e51fb409cb6f289458b5324823ed592c2b31c447426c70f67342":
        fail("Batch 12M v1 cover hash regressed")
    if v112m.get("title_imprint", {}).get("sha256") != "e4868cacb6c8608d69c65af327b7f873506974d930c38c2601f5b5d027981311":
        fail("Batch 12M title/imprint hash regressed")
    v412m = snu12m.get("v4_public_controls", {})
    if v412m.get("five_xiong_shen_target_page_observed") is not False or v412m.get("late_zi_target_line_observed") is not False:
        fail("Batch 12M v4 target page was prematurely claimed")
    pages12m = v412m.get("directly_reviewed_pages", [])
    if [p.get("public_page_label") for p in pages12m] != ["0001","0002","0003","0004","0005"]:
        fail("Batch 12M v4 public page set regressed")
    if pages12m[0].get("sha256") != "e0a1b490d64c4fc189215c7c533ac8bd16a56cecc41a93744e26be2659168548":
        fail("Batch 12M v4 cover hash regressed")
    dedup12m = ziwei_mingjingge_snu_evidence.get("mirror_deduplication", {})
    if dedup12m.get("rule") != "DO_NOT_DOUBLE_COUNT_SAME_PHYSICAL_COPY_OR_DIGITIZATION_LINEAGE" or dedup12m.get("independent_votes_from_these_routes") != 0:
        fail("Batch 12M mirror dedup firewall regressed")
    scribd12m = ziwei_mingjingge_snu_evidence.get("scribd_access_control", {})
    if scribd12m.get("browser_probe", {}).get("title") != "Client Challenge" or scribd12m.get("browser_probe", {}).get("captcha_bypass_attempted") is not False:
        fail("Batch 12M Scribd CAPTCHA boundary regressed")
    kyudb12m = ziwei_mingjingge_snu_evidence.get("official_kyudb_access_control", {})
    if kyudb12m.get("adjudication") != "EXECUTION_ENVIRONMENT_ACCESS_BOUNDARY_ONLY_NOT_EVIDENCE_OF_CATALOG_ABSENCE":
        fail("Batch 12M Kyudb access boundary regressed")
    hy12m = ziwei_mingjingge_snu_evidence.get("hanyang_independent_holding_locator", {})
    if hy12m.get("recorded_extent") != "6卷6冊" or hy12m.get("recorded_year") != 1870 or hy12m.get("recorded_holding") != "漢陽大學校圖書館":
        fail("Batch 12M Hanyang holding locator regressed")
    if hy12m.get("target_volume_page_observed") is not False:
        fail("Batch 12M Hanyang target page was prematurely claimed")
    adj12m = ziwei_mingjingge_snu_evidence.get("adjudication", {})
    if adj12m.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12m.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12M HPA-ZDATE-006 boundary regressed")
    if adj12m.get("algorithm_reopen_authorized") is not False or adj12m.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12M algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("mingjingge_snu_physical_copy_artifact") != "docs/research/ZIWEI-MINGJINGGE-SNU-PHYSICAL-COPY-PROVENANCE-R1.json":
        fail("Batch 12M Matrix artifact binding regressed")
    if nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12m") != 0:
        fail("Batch 12M Matrix witness-count firewall regressed")

    # Batch 12N upgrades Hanyang from a secondary locator to a first-party physical-copy binding while preserving the target-page fail-closed boundary.
    if ziwei_mingjingge_hanyang_evidence.get("batch_id") != "BATCH-12-ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-N":
        fail("Batch 12N evidence batch identity mismatch")
    ui12n = ziwei_mingjingge_hanyang_evidence.get("public_search_ui", {})
    if ui12n.get("workflow_run_id") != 34177957476 or ui12n.get("artifact_id") != 10037915482:
        fail("Batch 12N public UI provenance regressed")
    sj12n = ziwei_mingjingge_hanyang_evidence.get("observed_search_json", {})
    if sj12n.get("volume4_biblio_id") != 484926 or sj12n.get("artifact_id") != 10037939265:
        fail("Batch 12N Hanyang volume-4 biblio binding regressed")
    det12n = ziwei_mingjingge_hanyang_evidence.get("official_volume4_detail", {})
    if det12n.get("biblio_id") != 484926 or det12n.get("edition") != "木板本" or det12n.get("accession") != "HOM000001861":
        fail("Batch 12N official Hanyang physical-copy identity regressed")
    if det12n.get("call_number") != "133.3 진412ㅅ v.4" or det12n.get("target_text_visible_in_bibliographic_detail") is not False:
        fail("Batch 12N detail/target boundary regressed")
    api12n = ziwei_mingjingge_hanyang_evidence.get("observed_public_api", {})
    if api12n.get("workflow_run_id") != 34178359903 or api12n.get("artifact_id") != 10038051901:
        fail("Batch 12N corrected API provenance regressed")
    if api12n.get("biblio_route", {}).get("sha256") != "244cde73f14720aff0cac11804fc2d108bfa0c7c6f016e4c54c02f4c4bf5b802":
        fail("Batch 12N biblio response digest regressed")
    if api12n.get("items_route", {}).get("barcode") != "HOM000001861" or api12n.get("items_route", {}).get("item_id") != 872523:
        fail("Batch 12N item identity regressed")
    res12n = api12n.get("resources_route", {})
    if res12n.get("http_status") != 200 or res12n.get("code") != "success.noRecord" or res12n.get("public_digital_resource_object_returned") is not False:
        fail("Batch 12N current public resource-route boundary regressed")
    prov12n = ziwei_mingjingge_hanyang_evidence.get("provenance_adjudication", {})
    if prov12n.get("hanyang_independent_holding_status") != "OFFICIALLY_BOUND_FIRST_PARTY_PHYSICAL_COPY" or prov12n.get("independent_target_text_witness_added") is not False:
        fail("Batch 12N Hanyang physical/textual independence boundary regressed")
    adj12n = ziwei_mingjingge_hanyang_evidence.get("adjudication", {})
    if adj12n.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12n.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12N HPA-ZDATE-006 boundary regressed")
    if adj12n.get("algorithm_reopen_authorized") is not False or adj12n.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12N algorithm boundary regressed")
    hy_source12n = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-HANYANG-MINGJINGGE-ZIWEI-QUANJI-V4-1870"), None)
    if not hy_source12n or hy_source12n.get("biblio_id") != 484926 or hy_source12n.get("public_digital_resource_status") != "NO_RECORD_ON_CURRENT_PUBLIC_RESOURCES_ROUTE":
        fail("Batch 12N Hanyang source-registry binding regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("mingjingge_hanyang_official_physical_copy_artifact") != "docs/research/ZIWEI-MINGJINGGE-HANYANG-OFFICIAL-PHYSICAL-COPY-PROVENANCE-R1.json":
        fail("Batch 12N Matrix artifact binding regressed")
    if nanyang_row.get("hanyang_current_public_digital_resource_status") != "NO_RECORD" or nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12n") != 0:
        fail("Batch 12N Matrix resource/witness-count boundary regressed")


    # Batch 12O closes post-12N access probes while binding Korea University as a first-party physical set; no holding count may be promoted to a target-text/glyph vote.
    if ziwei_korea_university_evidence.get("batch_id") != "BATCH-12-ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-O":
        fail("Batch 12O evidence batch identity mismatch")
    ku12o = ziwei_korea_university_evidence.get("official_catalog_detail", {})
    if ku12o.get("catalog_control") != "CAT000000737166" or ku12o.get("edition") != "木板本(中國)":
        fail("Batch 12O Korea University catalog identity regressed")
    if "江左書林" not in ku12o.get("publication", "") or ku12o.get("extent") != "6卷6冊 : 圖 ; 16.0 ×11.3 cm.":
        fail("Batch 12O Korea University imprint/extent regressed")
    ku_items12o = ku12o.get("items", ())
    if len(ku_items12o) != 6 or ku_items12o[0].get("registration_number") != "465000245" or ku_items12o[-1].get("registration_number") != "465000250":
        fail("Batch 12O Korea University physical item set regressed")
    if ku12o.get("target_page_observed") is not False:
        fail("Batch 12O target-page boundary regressed")
    search12o = ziwei_korea_university_evidence.get("korea_university_public_search_controls", {})
    if search12o.get("oldbook_workflow_run_id") != 34211721066 or search12o.get("negative_catalog_absence_claim_authorized") is not False:
        fail("Batch 12O Korea University search-surface boundary regressed")
    access12o = ziwei_korea_university_evidence.get("post_12n_access_controls", {})
    snu12o = access12o.get("snu_public_preview", {})
    if snu12o.get("workflow_run_id") != 34209828645 or snu12o.get("target_page_status") != "PREVIEW_ROUTE_BOUND_NOT_TARGET_PAGE":
        fail("Batch 12O SNU preview boundary regressed")
    hy12o = access12o.get("hanyang_material_requests", {})
    if hy12o.get("workflow_run_id") != 34189277789 or hy12o.get("rarebook_applicability") != "UNRESOLVED" or hy12o.get("request_submitted") is not False:
        fail("Batch 12O Hanyang request boundary regressed")
    prov12o = ziwei_korea_university_evidence.get("provenance_adjudication", {})
    if prov12o.get("korea_university_physical_copy_status") != "OFFICIALLY_BOUND_FIRST_PARTY_PHYSICAL_SET" or prov12o.get("textual_stemma_independence_established") is not False:
        fail("Batch 12O physical/textual independence boundary regressed")
    adj12o = ziwei_korea_university_evidence.get("adjudication", {})
    if adj12o.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12o.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12O HPA-ZDATE-006 witness-count boundary regressed")
    if adj12o.get("algorithm_reopen_authorized") is not False or adj12o.get("confirmed_chart_algorithm_defect_count") != 0:
        fail("Batch 12O algorithm boundary regressed")
    ku_source12o = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-KOREA-UNIVERSITY-JIANGZUO-ZIWEI-QUANJI-CAT737166"), None)
    if not ku_source12o or ku_source12o.get("catalog_control") != "CAT000000737166" or ku_source12o.get("target_page_status") != "PENDING_DIRECT_PAGE":
        fail("Batch 12O source-registry binding regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("korea_university_independent_physical_copy_artifact") != "docs/research/ZIWEI-KOREA-UNIVERSITY-INDEPENDENT-PHYSICAL-COPY-PROVENANCE-R1.json":
        fail("Batch 12O Matrix artifact binding regressed")
    if nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12o") != 0 or nanyang_row.get("snu_v4_public_preview_status_post_12n") != "PREVIEW_ROUTE_BOUND_NOT_TARGET_PAGE":
        fail("Batch 12O Matrix access/witness boundary regressed")


    # Batch 12P binds a secondary commercial physical-edition locator without promoting it to catalog, text, glyph or runtime authority.
    if ziwei_weijingtang_hanauction_evidence.get("batch_id") != "BATCH-12-ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-P":
        fail("Batch 12P evidence batch identity mismatch")
    listing12p = ziwei_weijingtang_hanauction_evidence.get("public_listing", {})
    if listing12p.get("workflow_run_id") != 34214086632 or listing12p.get("artifact_id") != 10051026199:
        fail("Batch 12P workflow/artifact binding regressed")
    if listing12p.get("stable_object_id") != "102923" or listing12p.get("visible_lot_number") != 134 or listing12p.get("auction_round") != 229:
        fail("Batch 12P lot identity regressed")
    dom12p = listing12p.get("exact_dom_binding", {})
    if dom12p.get("ac_num_observed_final_run") != "117" or dom12p.get("ac_num_observed_prior_successful_run") != "120" or dom12p.get("ac_num_is_stable_bibliographic_identity") is not False:
        fail("Batch 12P dynamic ac_num boundary regressed")
    thumb12p = ziwei_weijingtang_hanauction_evidence.get("rendered_thumbnail", {})
    if thumb12p.get("sha256") != "59973f47a016dc114c967506673b3e053681a6d4a3824ecb8385f7b450fd1385" or thumb12p.get("width_px") != 114 or thumb12p.get("height_px") != 66:
        fail("Batch 12P rendered thumbnail identity regressed")
    if thumb12p.get("target_page_observed") is not False or thumb12p.get("target_hai_glyph_observed") is not False:
        fail("Batch 12P thumbnail was promoted to target text/glyph authority")
    prov12p = ziwei_weijingtang_hanauction_evidence.get("provenance_adjudication", {})
    if prov12p.get("source_authority") != "SECONDARY_COMMERCIAL_AUCTION_PHYSICAL_EDITION_LOCATOR_NOT_TARGET_TEXT_AUTHORITY":
        fail("Batch 12P source-authority boundary regressed")
    if prov12p.get("institutional_holding_bound") is not False or prov12p.get("textual_stemma_independence_established") is not False:
        fail("Batch 12P commercial/institutional-stemma boundary regressed")
    adj12p = ziwei_weijingtang_hanauction_evidence.get("adjudication", {})
    if adj12p.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or adj12p.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12P HPA-ZDATE-006 witness boundary regressed")
    if adj12p.get("new_chart_rule_candidate_authorized") is not False or adj12p.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12P candidate/algorithm boundary regressed")
    wa_source12p = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-HANAUCTION-WEIJINGTANG-ZIWEI-QUANJI-LOT134-20260404"), None)
    if not wa_source12p or wa_source12p.get("stable_object_id") != "102923" or wa_source12p.get("target_page_status") != "PENDING_DIRECT_PAGE":
        fail("Batch 12P source-registry binding regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("weijingtang_hanauction_physical_edition_artifact") != "docs/research/ZIWEI-WEIJINGTANG-HANAUCTION-PHYSICAL-EDITION-PROVENANCE-R1.json":
        fail("Batch 12P Matrix artifact binding regressed")
    if nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12p") != 0:
        fail("Batch 12P Matrix witness-count firewall regressed")

    # Batch 12Q keeps manuscript/catalog-cover and access-preview controls below target-text authority.
    if ziwei_kostma_scribd_fozhu_evidence.get("batch_id") != "BATCH-12-ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-Q":
        fail("Batch 12Q evidence batch identity mismatch")
    k12q = ziwei_kostma_scribd_fozhu_evidence.get("kostma", {})
    if k12q.get("uci") != "RIKS+CRMA+KSM-WZ.0000.0000-20140423.TOYO_1646" or k12q.get("call_number") != "Ⅶ-3-157":
        fail("Batch 12Q KOSTMA object identity regressed")
    if k12q.get("edition_form") != "筆寫本/필사본" or k12q.get("extent") != "1冊(100張)":
        fail("Batch 12Q manuscript boundary regressed")
    if k12q.get("exact_image_sha256") != "e0fc07b305e12a5fe3636aafd727b0c27407006bb88f883f7f426c5ea54cff04" or k12q.get("target_page_observed") is not False:
        fail("Batch 12Q KOSTMA image/target boundary regressed")
    s12q = ziwei_kostma_scribd_fozhu_evidence.get("scribd", {})
    if s12q.get("captcha_detected") is not True or s12q.get("captcha_bypass_attempted") is not False:
        fail("Batch 12Q Scribd CAPTCHA boundary regressed")
    f12q = ziwei_kostma_scribd_fozhu_evidence.get("fozhu", {})
    if f12q.get("public_preview_count") != 6 or f12q.get("target_page_observed") is not False:
        fail("Batch 12Q Fozhu preview boundary regressed")
    a12q = ziwei_kostma_scribd_fozhu_evidence.get("adjudication", {})
    if a12q.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or a12q.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12Q HPA-ZDATE-006 witness boundary regressed")
    if a12q.get("new_chart_rule_candidate_authorized") is not False or a12q.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12Q candidate/algorithm boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("kostma_toyo1646_manuscript_access_artifact") != "docs/research/ZIWEI-KOSTMA-TOYO1646-MANUSCRIPT-AND-SCRIBD-FOZHU-ACCESS-CONTROLS-R1.json":
        fail("Batch 12Q Matrix artifact binding regressed")
    if nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12q") != 0:
        fail("Batch 12Q Matrix witness-count firewall regressed")

    # Batch 12R keeps dual catalog detail records and secondary genealogy below target-text authority.
    if ziwei_toyo_detail_provenance_evidence.get("batch_id") != "BATCH-12-ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R":
        fail("Batch 12R evidence batch identity mismatch")
    cap12r = ziwei_toyo_detail_provenance_evidence.get("controlling_research_capture", {})
    if cap12r.get("workflow_run_id") != 34220050125 or cap12r.get("artifact_id") != 10053423338:
        fail("Batch 12R controlling run/artifact binding regressed")
    if cap12r.get("artifact_zip_sha256") != "d107855bedcd579f89c2468f83aff047febe6cd94cd7d4ec6d06d27405d828c7":
        fail("Batch 12R artifact digest regressed")
    t12r = ziwei_toyo_detail_provenance_evidence.get("toyo_bunko_first_party", {})
    recs12r = {x.get("targetid"): x for x in t12r.get("detail_records", ())}
    if set(recs12r) != {"471894", "502596"}:
        fail("Batch 12R Toyo targetid set regressed")
    if recs12r["502596"].get("detail_sha256") != "f459ab7e651eec283d8c3b00be633ba36037ba13dc0f7d94c30ad5d17198d960":
        fail("Batch 12R target 502596 detail digest regressed")
    if recs12r["471894"].get("detail_sha256") != "b6a3e768d779fd0a5895b8936da9326ca8c4475513c5b78301ab1776193ae655":
        fail("Batch 12R target 471894 detail digest regressed")
    if any(x.get("five_xiong_shen_observed") is not False or x.get("hai_glyph_observed") is not False for x in recs12r.values()):
        fail("Batch 12R catalog detail was promoted to target text/glyph authority")
    if t12r.get("item_specific_rare_book_marker_observed") is not False:
        fail("Batch 12R generic rare-book notice was promoted to item-specific status")
    if t12r.get("dual_record_physical_multiplicity") != "UNRESOLVED_DO_NOT_COUNT_AS_TWO_PHYSICAL_OR_TEXTUAL_WITNESSES":
        fail("Batch 12R dual-record physical multiplicity boundary regressed")
    access12r = ziwei_toyo_detail_provenance_evidence.get("current_access_policy", {})
    if access12r.get("github_runner_snapshot_status") != "UNAVAILABLE_NO_HTTP_RESPONSE_FOR_DOT_OR_JP_POLICY_PAGES_IN_CONTROLLING_RUN":
        fail("Batch 12R runner policy-snapshot boundary regressed")
    if access12r.get("external_reservation_or_copy_request_submitted") is not False:
        fail("Batch 12R falsely records an external Toyo request")
    n12r = ziwei_toyo_detail_provenance_evidence.get("ncku_scholarly_genealogy", {})
    if n12r.get("pdf_sha256") != "17d0089c3328253230cb2f110ac40527abe41fbb97183483215a5e633e5b2e2e" or n12r.get("ocr_used") is not False:
        fail("Batch 12R NCKU PDF identity/no-OCR boundary regressed")
    if n12r.get("source_authority") != "MODERN_SCHOLARLY_EDITION_GENEALOGY_NOT_TARGET_TEXT_OR_GLYPH_AUTHORITY":
        fail("Batch 12R NCKU authority scope regressed")
    a12r = ziwei_toyo_detail_provenance_evidence.get("adjudication", {})
    if a12r.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or a12r.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12R HPA-ZDATE-006 witness boundary regressed")
    if a12r.get("new_chart_rule_candidate_authorized") is not False or a12r.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12R candidate/algorithm boundary regressed")
    toyo_source12r = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-TOYO-BUNKO-ZWDSQJ-VII-3-157"), None)
    if not toyo_source12r or toyo_source12r.get("exact_detail_targetids") != ["471894", "502596"]:
        fail("Batch 12R Toyo registry detail binding regressed")
    ncku_source12r = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-NCKU-CHEN-2021-ZIWEI-EDITION-GENEALOGY"), None)
    if not ncku_source12r or ncku_source12r.get("target_text_authority") is not False:
        fail("Batch 12R NCKU registry authority boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("toyo_vii3_157_first_party_detail_artifact") != "docs/research/ZIWEI-TOYO-VII3-157-FIRST-PARTY-DETAIL-AND-SCHOLARLY-PROVENANCE-TENSION-R1.json":
        fail("Batch 12R Matrix artifact binding regressed")
    if nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12r") != 0:
        fail("Batch 12R Matrix witness-count firewall regressed")

    # Batch 12S keeps the current public Media Repository search boundary below textual/glyph authority.
    if ziwei_toyo_media_repository_evidence.get("batch_id") != "BATCH-12-ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-S":
        fail("Batch 12S evidence batch identity mismatch")
    cap12s = ziwei_toyo_media_repository_evidence.get("controlling_research_capture", {})
    if cap12s.get("workflow_run_id") != 34221594363 or cap12s.get("artifact_id") != 10053963935:
        fail("Batch 12S controlling run/artifact binding regressed")
    if cap12s.get("artifact_zip_sha256") != "533efe6a70dbc7f1488adf13199e47a02b908ac3c184bb54be26b2075adedf0a":
        fail("Batch 12S artifact digest regressed")
    media12s = ziwei_toyo_media_repository_evidence.get("first_party_media_repository", {})
    if media12s.get("toyo_collection_item_set_id") != 42942 or media12s.get("valid_query_count") != 10:
        fail("Batch 12S source-emitted search scope regressed")
    searches12s = media12s.get("searches", ())
    if len(searches12s) != 10:
        fail("Batch 12S search evidence count regressed")
    if any(x.get("http_status") != 200 or x.get("visible_result_count_strings") != ["0 件", "0 件"] for x in searches12s):
        fail("Batch 12S visible zero-item result evidence regressed")
    if any(x.get("concrete_resource_links") or x.get("resource_node_count") != 0 or x.get("no_concrete_resource_objects") is not True for x in searches12s):
        fail("Batch 12S concrete-resource boundary regressed")
    if media12s.get("concrete_target_resource_object_count_returned") != 0 or media12s.get("target_page_observed") is not False:
        fail("Batch 12S target-resource/page boundary regressed")
    guard12s = ziwei_toyo_media_repository_evidence.get("guardrails", {})
    if guard12s.get("guessed_item_ids") is not False or guard12s.get("enumerated_item_ids") is not False or guard12s.get("api_route_guessed") is not False:
        fail("Batch 12S no-guess/no-enumeration guardrail regressed")
    if guard12s.get("pagination_control_used_as_query") is not False or guard12s.get("only_source_emitted_search_routes_and_fields_submitted") is not True:
        fail("Batch 12S source-emitted search guardrail regressed")
    a12s = ziwei_toyo_media_repository_evidence.get("adjudication", {})
    if a12s.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or a12s.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12S HPA-ZDATE-006 witness boundary regressed")
    if a12s.get("new_chart_rule_candidate_authorized") is not False or a12s.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12S candidate/algorithm boundary regressed")
    src12s = next((item for item in registry.get("sources", ()) if item.get("source_id") == "EXT-TOYO-BUNKO-MEDIA-REPOSITORY-PUBLIC-SEARCH"), None)
    if not src12s or src12s.get("target_text_authority") is not False or src12s.get("digitization_absence_authorized") is not False:
        fail("Batch 12S registry authority boundary regressed")
    nanyang_row = next((row for row in matrix.get("rows", ()) if row.get("rule_id") == "HPA-ZDATE-006"), None)
    if not nanyang_row or nanyang_row.get("toyo_media_repository_public_search_artifact") != "docs/research/ZIWEI-TOYO-MEDIA-REPOSITORY-PUBLIC-SEARCH-ROUTE-CONTROL-R1.json":
        fail("Batch 12S Matrix artifact binding regressed")
    if nanyang_row.get("toyo_media_repository_valid_target_query_count") != 10 or nanyang_row.get("toyo_media_repository_concrete_target_resource_object_count_returned") != 0:
        fail("Batch 12S Matrix search boundary regressed")
    if nanyang_row.get("independent_hai_glyph_witness_count_added_batch_12s") != 0:
        fail("Batch 12S Matrix witness-count firewall regressed")

    focus_text = "\n".join(audit_state.get("current_focus", ()))
    for fragment in (
        "Batch 11U",
        "RESOLVED_AT_CATALOG_IDENTIFIER_LEVEL",
        "1930 generic main sequence number 893",
        "Batch 11V",
        "ERROR - DIR NOT EXIST",
        "CLOSED_NO_DOWNLOADABLE_PDF_OBJECT_OBSERVED",
        "Batch 11W",
        "5c4276d953bd47ca2679c70209d179cf",
        "ZGKS802.008",
        "Batch 11X",
        "M/F73-102-37-A",
        "2024-02-01",
        "No G893 reproduction request has been submitted",
        "PENDING_DIRECT_TARGET_PAGE",
        "Batch 12A",
        "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7",
        "HPA-ZDATE-006",
        "MISSING_FROM_PRODUCT",
        "Batch 12B",
        "8-large+2-small-ke structure",
        "23:00–24:00",
        "runtime time",
        "Batch 12C",
        "9789888266944",
        "敦化堂",
        "繼述堂",
        "文誠堂",
        "34120317222",
        "10017909080",
        "UNRESOLVED",
        "Batch 12D",
        "aIRbDgAAQBAJ",
        "PT165",
        "34123161798",
        "10019011766",
        "34121401508",
        "10018315848",
        "Batch 12E",
        "1pjr6vy1ffsq3l1y",
        "子30814110",
        "清經綸堂刻本",
        "BBAA18036",
        "34124948029",
        "10019806060",
        "Batch 12F",
        "rZRcCwAAQBAJ",
        "34128596022",
        "10021127358",
        "34128847746",
        "10021385955",
        "34129199244",
        "10021353934",
        "UNRESOLVED_PENDING_DIRECT_PHYSICAL_TARGET_PAGES",
        "Batch 12G",
        "34133129317",
        "10022892119",
        "連元閣",
        "Batch 12H",
        "子０６０－０００１",
        "34134081787",
        "10023248966",
        "34134328002",
        "10023353526",
        "VII-3-157",
        "子海珍本編",
        "Batch 12I",
        "DO_NOT_DOUBLE_COUNT_SAME_PHYSICAL_COPY_OR_DIGITIZATION_LINEAGE",
        "kxdy0QEACAAJ",
        "RISpDgAAQBAJ",
        "34138050721",
        "10024763004",
        "DIRECT_INDEPENDENT_PHYSICAL_TARGET_PAGES",
        "Batch 12J",
        "34140027356",
        "10025522997",
        "校正紫薇斗數全書",
        "上海廣益書局印行",
        "UNRESOLVED",
        "Ronghetang",
        "Batch 12K",
        "34174455835",
        "10036772401",
        "PT10/PT11",
        "PT165",
        "UNRESOLVED_DUNHUATANG_VS_JISHUTANG",
        "index positions are not base-copy segmentation boundaries",
        "Batch 12L",
        "34174856657",
        "10036898985",
        "34175090423",
        "10036973127",
        "PDF p165 = printed p151",
        "上五刻属昨夜亥时 / 下五刻属今日子时",
        "MODERN_TYPESET_RECEIVED_TEXT_CORROBORATION_ONLY",
        "Batch 12M",
        "一簑古523.5-J562b-v.1-6",
        "523.5 J562b V.4",
        "太微賦總括",
        "DO_NOT_DOUBLE_COUNT_SAME_PHYSICAL_COPY_OR_DIGITIZATION_LINEAGE",
        "34176539049",
        "10037447325",
        "Client Challenge CAPTCHA",
        "Batch 12R",
        "502596",
        "471894",
        "f459ab7e651eec283d8c3b00be633ba36037ba13dc0f7d94c30ad5d17198d960",
        "b6a3e768d779fd0a5895b8936da9326ca8c4475513c5b78301ab1776193ae655",
        "17d0089c3328253230cb2f110ac40527abe41fbb97183483215a5e633e5b2e2e",
        "金陵益軒唐謙梓",
        "1942",
        "runner did not obtain",
        "Batch 12S",
        "34221594363",
        "10053963935",
        "533efe6a70dbc7f1488adf13199e47a02b908ac3c184bb54be26b2075adedf0a",
        "item_set_id=42942",
        "10 valid HTTP-200 searches",
        "0 件",
        "zero concrete item/document resource objects",
        "not proof of no digitization ever",
        "Batch 12T",
        "漢 / 子六十 / 一五八五六 / 全二",
        "1078787",
        "10054995877",
        "HIGH_CONFIDENCE",
        "not explicitly crosswalked",
        "Batch 12U",
        "000001237342",
        "12282052",
        "10.11501/12282052",
        "document-name list",
        "UNRESOLVED_PENDING_DIRECT_1971_CATALOG_ENTRY_OR_FIRST_PARTY_CROSSWALK",
                "34176383486",
        "Hanyang University Library",
        "五凶神 target page",
        "Batch 12N",
        "484926",
        "872523",
        "HOM000001861",
        "133.3 진412ㅅ v.4",
        "success.noRecord",
        "34178359903",
        "10038051901",
        "zero independent target-text/Hai-glyph votes",
        "Batch 12O",
        "CAT000000737166",
        "江左書林",
        "대학원 C10 B8",
        "465000245",
        "465000250",
        "34211567451",
        "10050023318",
        "34209828645",
        "10049328514",
        "34189277789",
        "10041642791",
        "Batch 12P",
        "102923",
        "味經堂藏板",
        "34214086632",
        "10051026199",
        "59973f47a016dc114c967506673b3e053681a6d4a3824ecb8385f7b450fd1385",
        "ac_num 120",
        "117",
        "Batch 12Q",
        "TOYO_1646",
        "Ⅶ-3-157",
        "34216448461",
        "10051997835",
        "34217047741",
        "10052200564",
        "e0fc07b305e12a5fe3636aafd727b0c27407006bb88f883f7f426c5ea54cff04",
        "34215179324",
        "10051466410",
        "Client Challenge CAPTCHA",
    ):
        if fragment not in focus_text:
            fail(f"current-state lost Batch 11V continuity boundary: {fragment}")

    # Batch 12T upgrades/deduplicates the Batch 12A facsimile provenance without adding a new witness.
    if ziwei_naikaku_lineage_evidence.get("batch_id") != "BATCH-12-ZIWEI-NAIKAKU-NANYANGTANG-FACSIMILE-PHYSICAL-LINEAGE-BRIDGE-T":
        fail("Batch 12T machine evidence batch identity mismatch")
    bridge = ziwei_naikaku_lineage_evidence.get("lineage_adjudication", {})
    if bridge.get("physical_lineage_relation") != "HIGH_CONFIDENCE_SAME_NAIKAKU_NATIONAL_ARCHIVES_MING_FULLBOOK_LINEAGE":
        fail("Batch 12T physical-lineage convergence regressed")
    if bridge.get("legacy_registration_15856_to_current_call_number_crosswalk") != "NOT_EXPLICITLY_DOCUMENTED_IN_REVIEWED_FIRST_PARTY_CATALOG_SURFACE":
        fail("Batch 12T old-registration crosswalk uncertainty regressed")
    if bridge.get("batch12a_and_batch12h_count_as_independent_textual_witnesses") is not False or bridge.get("independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12T dedup / zero-vote boundary regressed")
    b12a = ziwei_naikaku_lineage_evidence.get("batch12a_direct_facsimile", {})
    if b12a.get("pdf_sha256") != "32ca49bb3a02454067e6deddb97921779837a10e59e946c12d2f6d14f33509e7":
        fail("Batch 12T Batch12A PDF identity regressed")
    if b12a.get("page_1_visual_review_no_ocr", {}).get("legacy_registration_number") != "15856":
        fail("Batch 12T legacy registration visual binding regressed")
    naj12t = ziwei_naikaku_lineage_evidence.get("national_archives_japan", {})
    if naj12t.get("file_id") != "1078787" or naj12t.get("official_index_metadata", {}).get("call_number") != "子０６０－０００１":
        fail("Batch 12T NAJ object binding regressed")
    if naj12t.get("official_index_metadata", {}).get("quantity") != "2冊":
        fail("Batch 12T NAJ two-volume binding regressed")
    row12t = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12t or row12t.get("batch12a_naj_dedup_status") != "DO_NOT_DOUBLE_COUNT_AS_TWO_PHYSICAL_OR_TEXTUAL_WITNESSES":
        fail("Batch 12T matrix dedup boundary regressed")
    naj_source12t = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-NAJ-ZWDSQS-MING-1078787"), None)
    if not naj_source12t or naj_source12t.get("batch12t_provenance_bridge", {}).get("independent_hai_glyph_increment") != 0:
        fail("Batch 12T NAJ registry provenance bridge regressed")

    # Batch 12U binds the 1971 revised Naikaku catalog access route without fabricating the old-number crosswalk.
    if ziwei_naikaku_1971_catalog_evidence.get("batch_id") != "BATCH-12-ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-U":
        fail("Batch 12U machine evidence batch identity mismatch")
    ndl12u = ziwei_naikaku_1971_catalog_evidence.get("national_diet_library", {})
    if ndl12u.get("ndl_bibliographic_id") != "000001237342" or ndl12u.get("pid") != "12282052":
        fail("Batch 12U NDL catalog identity regressed")
    if ndl12u.get("doi") != "10.11501/12282052" or ndl12u.get("publication_year") != 1971:
        fail("Batch 12U NDL DOI/year binding regressed")
    if ndl12u.get("target_crosswalk_entry_observed") is not False:
        fail("Batch 12U falsely promotes the public NDL metadata to target crosswalk content")
    minna12u = ziwei_naikaku_1971_catalog_evidence.get("minna_search_ocr_surface", {})
    if minna12u.get("plain_text_label") != "プレーンテキスト" or minna12u.get("correction_status") != "未校正":
        fail("Batch 12U Minna Search OCR identity regressed")
    if minna12u.get("unauthenticated_full_text_downloaded") is not False or minna12u.get("target_crosswalk_entry_observed") is not False:
        fail("Batch 12U unauthenticated OCR boundary regressed")
    najmethod12u = ziwei_naikaku_1971_catalog_evidence.get("national_archives_method_control", {})
    if najmethod12u.get("doi") != "10.69245/kitanomaru.42.0_129" or najmethod12u.get("revised_1971_catalog_document_name_list_at_end") is not True:
        fail("Batch 12U National Archives catalog-index structure control regressed")
    if najmethod12u.get("target_ziwei_entry_or_legacy_number_crosswalk_quoted") is not False:
        fail("Batch 12U method article was promoted to target crosswalk content")
    ext12u = ziwei_naikaku_1971_catalog_evidence.get("external_action_boundary", {})
    if any(ext12u.get(k) is not False for k in (
        "ndl_login_used", "individual_transmission_session_used", "library_transmission_request_submitted",
        "remote_copy_request_submitted", "paid_request_submitted", "credentials_or_entitlement_bypass_attempted"
    )):
        fail("Batch 12U falsely records external NDL access/request activity")
    a12u = ziwei_naikaku_1971_catalog_evidence.get("adjudication", {})
    if a12u.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or a12u.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12U HPA-ZDATE-006 witness boundary regressed")
    if a12u.get("legacy_registration_crosswalk_status") != "UNRESOLVED_PENDING_DIRECT_1971_CATALOG_ENTRY_OR_FIRST_PARTY_CROSSWALK":
        fail("Batch 12U old-number crosswalk fail-closed status regressed")
    if a12u.get("new_chart_rule_candidate_authorized") is not False or a12u.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12U candidate/algorithm boundary regressed")
    src12u = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-NDL-NAIKAKU-KANSEKI-BUNRUI-MOKUROKU-1971"), None)
    if not src12u or src12u.get("target_crosswalk_entry_observed") is not False or src12u.get("target_text_authority") is not False:
        fail("Batch 12U registry source authority boundary regressed")
    row12u = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12u or row12u.get("naikaku_1971_revised_catalog_access_artifact") != "docs/research/ZIWEI-NAIKAKU-1971-REVISED-CATALOG-CROSSWALK-ACCESS-ROUTE-R1.json":
        fail("Batch 12U Matrix artifact binding regressed")
    if row12u.get("independent_hai_glyph_witness_count_added_batch_12u") != 0 or row12u.get("external_copy_request_submitted_batch_12u") is not False:
        fail("Batch 12U Matrix witness/request firewall regressed")

    # Batch 12V closes the tested unauthenticated NDL 1971 page routes without claiming target-entry absence.
    if ziwei_naikaku_1971_page_boundary_evidence.get("batch_id") != "BATCH-12-ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-V":
        fail("Batch 12V machine evidence batch identity mismatch")
    tp12v = ziwei_naikaku_1971_page_boundary_evidence.get("target_entry_probe", {})
    if tp12v.get("workflow_run_id") != 34230231815 or tp12v.get("artifact_id") != 10057469073:
        fail("Batch 12V target-entry probe run/artifact binding regressed")
    if tp12v.get("ndl_lab_page_search_hit_counts") != [0, 0, 0, 0, 0, 0, 0, 0]:
        fail("Batch 12V NDL Lab target-query zero-hit control regressed")
    if tp12v.get("ndl_lab_fulltext_json_status") != "HTTP_403_FORBIDDEN":
        fail("Batch 12V NDL Lab full-text access boundary regressed")
    if tp12v.get("item_api_status") != "HTTP_200" or tp12v.get("item_api_sha256") != "0642e44194b40c25380a3a8476d2e92f2b52eb94dcca99d2afb5bc08f91a4a8d":
        fail("Batch 12V exact NDL item API binding regressed")
    pr12v = ziwei_naikaku_1971_page_boundary_evidence.get("page_route_probe", {})
    if pr12v.get("workflow_run_id") != 34234090185 or pr12v.get("artifact_id") != 10059056472:
        fail("Batch 12V page-route probe run/artifact binding regressed")
    if pr12v.get("content_object_count") != 405 or pr12v.get("tested_api_emitted_publicpath_count") != 32:
        fail("Batch 12V 405-page / 32-route inventory regressed")
    if pr12v.get("unauthenticated_http_401_count") != 32 or pr12v.get("saved_image_count") != 0:
        fail("Batch 12V unauthenticated page access boundary regressed")
    if pr12v.get("route_policy") != "ONLY_API_EMITTED_PUBLICPATH_VALUES_NO_IDENTIFIER_GUESSING":
        fail("Batch 12V source-emitted-route policy regressed")
    a12v = ziwei_naikaku_1971_page_boundary_evidence.get("adjudication", {})
    if a12v.get("legacy_registration_crosswalk_status") != "UNRESOLVED_PENDING_DIRECT_1971_CATALOG_ENTRY_OR_EXPLICIT_FIRST_PARTY_CROSSWALK":
        fail("Batch 12V old-number crosswalk fail-closed status regressed")
    if a12v.get("target_entry_absence_proven") is not False or a12v.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12V target-absence/witness firewall regressed")
    if a12v.get("algorithm_reopen_authorized") is not False or a12v.get("new_chart_rule_candidate_authorized") is not False:
        fail("Batch 12V algorithm/candidate firewall regressed")
    row12v = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12v or row12v.get("naikaku_1971_public_page_access_artifact") != "docs/research/ZIWEI-NAIKAKU-1971-PUBLIC-PAGE-ACCESS-BOUNDARY-R1.json":
        fail("Batch 12V Matrix artifact binding regressed")
    if row12v.get("naikaku_1971_digital_content_object_count") != 405 or row12v.get("naikaku_1971_api_emitted_page_route_http_401_count") != 32:
        fail("Batch 12V Matrix page-access evidence regressed")
    if row12v.get("whole_catalog_target_absence_claim_authorized_batch_12v") is not False or row12v.get("independent_hai_glyph_witness_count_added_batch_12v") != 0:
        fail("Batch 12V Matrix negative-claim/witness firewall regressed")
    src12v = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-NDL-NAIKAKU-KANSEKI-BUNRUI-MOKUROKU-1971"), None)
    if not src12v or src12v.get("exact_item_api_content_object_count") != 405 or src12v.get("api_emitted_page_route_http_401_count") != 32:
        fail("Batch 12V registry page-access binding regressed")
    if src12v.get("whole_catalog_negative_authorized") is not False or src12v.get("target_crosswalk_entry_observed") is not False:
        fail("Batch 12V registry authority boundary regressed")

    # Batch 12W strengthens SNU v4 file-level public provenance and adds a second Fozhu preview route without target-text votes.
    if ziwei_snu_quark_fozhu_evidence.get("batch_id") != "BATCH-12-ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-W":
        fail("Batch 12W machine evidence batch identity mismatch")
    sq12w = ziwei_snu_quark_fozhu_evidence.get("snu_quark_public_share", {})
    inv12w = sq12w.get("full_inventory_run", {})
    if inv12w.get("workflow_run_id") != 34236492659 or inv12w.get("artifact_id") != 10060095594:
        fail("Batch 12W Quark inventory run/artifact binding regressed")
    if inv12w.get("accumulated_visible_filename_count") != 49 or inv12w.get("target_candidate_count") != 1:
        fail("Batch 12W Quark 49-of-49 / unique-target control regressed")
    if inv12w.get("exact_target_visible_size") != "31.5M" or "523.5-J562b-v.1-6" not in inv12w.get("exact_target_filename", ""):
        fail("Batch 12W exact SNU v4 public file binding regressed")
    if sq12w.get("target_pdf_obtained") is not False or sq12w.get("five_xiong_shen_target_page_observed") is not False:
        fail("Batch 12W falsely promotes Quark file inventory to target-page authority")
    if sq12w.get("independent_target_text_vote_added") != 0:
        fail("Batch 12W SNU same-lineage witness firewall regressed")
    ui12w = sq12w.get("web_preview_interaction_controls", {})
    if ui12w.get("selected_download_safety_gate_run", {}).get("selected_row_count_before") != 35:
        fail("Batch 12W Quark multi-selection safety control regressed")
    if ui12w.get("hover_download_run", {}).get("hidden_element_forced_click_attempted") is not False:
        fail("Batch 12W falsely records hidden-control forcing")
    fz12w = ziwei_snu_quark_fozhu_evidence.get("fozhu16991_public_preview_route", {})
    if fz12w.get("workflow_run_id") != 34238366994 or fz12w.get("artifact_id") != 10060843332:
        fail("Batch 12W Fozhu16991 run/artifact binding regressed")
    if fz12w.get("successfully_obtained_preview_count") != 6 or fz12w.get("paid_full_content_obtained") is not False:
        fail("Batch 12W Fozhu16991 public-preview / paid-content boundary regressed")
    vis12w = fz12w.get("direct_visual_review_without_ocr", {})
    if vis12w.get("target_page_observed") is not False or vis12w.get("five_xiong_shen_heading_observed") is not False or vis12w.get("shang_wu_ke_observed") is not False:
        fail("Batch 12W Fozhu non-target previews were promoted to target text")
    rel12w = fz12w.get("relation_to_batch_12q_fozhu", {})
    if rel12w.get("byte_level_same_preview_set") is not False or "UNRESOLVED" not in rel12w.get("physical_scan_or_exemplar_identity", ""):
        fail("Batch 12W Fozhu12Q dedup/independence boundary regressed")
    a12w = ziwei_snu_quark_fozhu_evidence.get("adjudication", {})
    if a12w.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or a12w.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12W HPA-ZDATE-006 witness boundary regressed")
    if a12w.get("new_chart_rule_candidate_authorized") is not False or a12w.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12W candidate/algorithm firewall regressed")
    row12w = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12w or row12w.get("batch_12w_snu_quark_fozhu_route_artifact") != "docs/research/ZIWEI-SNU-QUARK-V4-AND-FOZHU16991-PUBLIC-ROUTE-CONTROLS-R1.json":
        fail("Batch 12W Matrix artifact binding regressed")
    if row12w.get("snu_quark_public_folder_filename_count") != 49 or row12w.get("fozhu16991_successful_public_preview_count") != 6:
        fail("Batch 12W Matrix route-count binding regressed")
    if row12w.get("independent_hai_glyph_witness_count_added_batch_12w") != 0:
        fail("Batch 12W Matrix witness firewall regressed")
    snusrc12w = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-SNU-ILSA-MINGJINGGE-ZWDSQJ-DIGITIZATION-DERIVATIVE"), None)
    if not snusrc12w or snusrc12w.get("batch12w_quark_public_share", {}).get("folder_filename_count") != 49:
        fail("Batch 12W SNU registry Quark binding regressed")
    fzsrc12w = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-FOZHU-16991-EIGHTEEN-FLYING-STARS-PUBLIC-PREVIEWS"), None)
    if not fzsrc12w or fzsrc12w.get("public_preview_count_obtained") != 6:
        fail("Batch 12W Fozhu16991 registry source missing or regressed")
    if fzsrc12w.get("target_page_observed") is not False or fzsrc12w.get("independent_witness_increment") != 0:
        fail("Batch 12W Fozhu16991 registry authority boundary regressed")

    # Batch 12X binds Jiwen/Dayuan copy-text routes without silently normalizing directory variants or adding target-text votes.
    if ziwei_jiwen_dayuan_evidence.get("batch_id") != "BATCH-12-ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-X":
        fail("Batch 12X machine evidence batch identity mismatch")
    rw12x = ziwei_jiwen_dayuan_evidence.get("research_run", {})
    if rw12x.get("workflow_run_id") != 34240652003 or rw12x.get("artifact_id") != 10061841718:
        fail("Batch 12X research run/artifact binding regressed")
    if rw12x.get("artifact_zip_sha256") != "022d32ef5cb09043ea8b662a13b8a45d09c596e02cd612d673da1c7adde8d7ca":
        fail("Batch 12X research artifact digest regressed")
    jw12x = ziwei_jiwen_dayuan_evidence.get("jiwen_1982_1999_route", {})
    if jw12x.get("isbn13") != "9789579789806" or "清同治九年木刻再版" not in jw12x.get("preface_copy_provenance_surface", ""):
        fail("Batch 12X Jiwen copy-route provenance regressed")
    if jw12x.get("direct_five_xiong_shen_target_page_observed") is not False or jw12x.get("independent_textual_witness_increment") != 0:
        fail("Batch 12X Jiwen target/witness firewall regressed")
    dy12x = ziwei_jiwen_dayuan_evidence.get("dayuan_2012_route", {})
    if dy12x.get("isbn13") != "9789866171680" or dy12x.get("public_description", {}).get("main_text_page_count") != 434:
        fail("Batch 12X Dayuan identity/page-count binding regressed")
    phil12x = dy12x.get("public_toc_philology", {})
    if phil12x.get("observed_surface") != "五神 百字千金訣" or phil12x.get("mechanical_equivalence_authorized") is not False:
        fail("Batch 12X 五神/五凶神 philological firewall regressed")
    vis12x = dy12x.get("direct_visual_public_samples_no_ocr", {})
    if vis12x.get("completed") is not True or vis12x.get("five_xiong_shen_target_page_observed") is not False:
        fail("Batch 12X Dayuan sample-review target boundary regressed")
    if "金陵益軒唐謙繡梓" not in vis12x.get("sample_087", {}).get("direct_visible_glyphs", []):
        fail("Batch 12X Dayuan title/imprint visual control regressed")
    a12x = ziwei_jiwen_dayuan_evidence.get("adjudication", {})
    if a12x.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or a12x.get("direct_independent_hai_glyph_witness_count_added") != 0:
        fail("Batch 12X HPA-ZDATE-006 witness boundary regressed")
    if a12x.get("directory_variant_wushen_to_wuxiongshen_normalization_authorized") is not False or a12x.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12X philology/algorithm firewall regressed")
    row12x = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12x or row12x.get("batch_12x_jiwen_dayuan_copy_text_artifact") != "docs/research/ZIWEI-JIWEN-1982-1999-AND-DAYUAN-2012-COPY-TEXT-ROUTES-R1.json":
        fail("Batch 12X Matrix artifact binding regressed")
    if row12x.get("dayuan_wushen_to_wuxiongshen_mechanical_normalization_authorized") is not False or row12x.get("independent_hai_glyph_witness_count_added_batch_12x") != 0:
        fail("Batch 12X Matrix philology/witness firewall regressed")
    jwsrc12x = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-JIWEN-ZWDSQJ-1982-1999-ZHOU-COPY-REPRINT"), None)
    dysrc12x = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-DAYUAN-ZWDSQJ-JINGCHAOBEN-2012"), None)
    if not jwsrc12x or jwsrc12x.get("target_page_observed") is not False or jwsrc12x.get("independent_witness_increment") != 0:
        fail("Batch 12X Jiwen registry authority boundary regressed")
    if not dysrc12x or dysrc12x.get("main_text_page_count") != 434 or dysrc12x.get("wushen_to_wuxiongshen_normalization_authorized") is not False:
        fail("Batch 12X Dayuan registry authority boundary regressed")

    # Batch 12Y NCC/Kamo continuity evidence: direct sample review upgrades route evidence but adds no target-text vote.
    if ziwei_ncc_jiwen_dayuan_review_evidence.get("schema") != "ZIWEI-NCC-JIWEN-DAYUAN-PUBLIC-SAMPLE-VISUAL-REVIEW-R1":
        fail("Batch 12Y NCC sample-review schema mismatch")
    rr12y = ziwei_ncc_jiwen_dayuan_review_evidence.get("research_run", {})
    if rr12y.get("workflow_run_id") != 34241779981 or rr12y.get("artifact_id") != 10062285198:
        fail("Batch 12Y NCC research run/artifact binding regressed")
    if rr12y.get("artifact_zip_sha256") != "6fd5a1a6c160d93f186aa3a0e1572dd5fd0763ce4a27716ed8673ebf23eb5048":
        fail("Batch 12Y NCC artifact digest regressed")
    jw12y = ziwei_ncc_jiwen_dayuan_review_evidence.get("jiwen_995", {})
    if jw12y.get("source_emitted_relevant_image_object_count") != 11 or jw12y.get("facsimile_nature_directly_observed") is not True:
        fail("Batch 12Y Jiwen direct facsimile sample binding regressed")
    if jw12y.get("direct_five_xiong_shen_target_page_observed") is not False or jw12y.get("late_zi_target_sentence_observed") is not False:
        fail("Batch 12Y Jiwen target-page firewall regressed")
    dy12y = ziwei_ncc_jiwen_dayuan_review_evidence.get("dayuan_7346", {})
    if dy12y.get("source_emitted_relevant_image_object_count") != 11:
        fail("Batch 12Y Dayuan source-emitted image count regressed")
    if dy12y.get("direct_five_xiong_shen_target_page_observed") is not False or dy12y.get("direct_wushen_target_page_observed") is not False:
        fail("Batch 12Y Dayuan target-page firewall regressed")
    phil12y = ziwei_ncc_jiwen_dayuan_review_evidence.get("philological_control", {})
    if phil12y.get("wushen_to_wuxiongshen_mechanical_normalization_authorized") is not False:
        fail("Batch 12Y 五神/五凶神 philological firewall regressed")
    a12y = ziwei_ncc_jiwen_dayuan_review_evidence.get("adjudication", {})
    if a12y.get("direct_independent_hai_glyph_witness_count_added") != 0 or a12y.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12Y NCC witness/algorithm firewall regressed")

    if ziwei_kamo_access_evidence.get("schema") != "ZIWEI-KAMO-4174-03-04-PUBLIC-ROUTE-ACCESS-CONTROL-R1":
        fail("Batch 12Y Kamo route-control schema mismatch")
    if ziwei_kamo_access_evidence.get("workflow_run_id") != 34242503503 or ziwei_kamo_access_evidence.get("artifact_id") != 10062627609:
        fail("Batch 12Y Kamo run/artifact binding regressed")
    if ziwei_kamo_access_evidence.get("artifact_zip_sha256") != "d20f179a18834e7a7d18207df8810c96e9290c5188a5771e62546e89b2426c11":
        fail("Batch 12Y Kamo artifact digest regressed")
    routes12y = ziwei_kamo_access_evidence.get("routes", [])
    if len(routes12y) != 3 or any(r.get("result") != "TIMEOUT" or r.get("bytes") != 0 for r in routes12y):
        fail("Batch 12Y Kamo timeout access-boundary record regressed")
    ka12y = ziwei_kamo_access_evidence.get("adjudication", {})
    if ka12y.get("content_absence_claim_authorized") is not False or ka12y.get("target_page_absence_claim_authorized") is not False:
        fail("Batch 12Y Kamo negative-inference firewall regressed")
    if ka12y.get("independent_textual_witness_increment") != 0 or ka12y.get("algorithm_effect") != "NONE":
        fail("Batch 12Y Kamo witness/algorithm firewall regressed")

    row12y = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12y or row12y.get("batch_12y_ncc_direct_review_artifact") != "docs/research/ZIWEI-NCC-JIWEN-DAYUAN-PUBLIC-SAMPLE-VISUAL-REVIEW-R1.json":
        fail("Batch 12Y Matrix NCC artifact binding regressed")
    if row12y.get("kamo_public_route_access_control_artifact_batch_12y") != "docs/research/ZIWEI-KAMO-4174-03-04-PUBLIC-ROUTE-ACCESS-CONTROL-R1.json":
        fail("Batch 12Y Matrix Kamo artifact binding regressed")
    if row12y.get("independent_hai_glyph_witness_count_added_batch_12y") != 0:
        fail("Batch 12Y Matrix witness firewall regressed")

    if not jwsrc12x or jwsrc12x.get("direct_public_sample_review_status") != "OLD_PRINT_FACSIMILE_NATURE_DIRECTLY_OBSERVED_TARGET_PAGE_NOT_OBSERVED":
        fail("Batch 12Y Jiwen registry direct-sample status regressed")
    if not dysrc12x or dysrc12x.get("direct_public_sample_review_status") != "HANDWRITTEN_COPY_TEXT_SAMPLES_DIRECTLY_OBSERVED_TARGET_PAGE_NOT_OBSERVED":
        fail("Batch 12Y Dayuan registry direct-sample status regressed")

    # Batch 12Z Korea CNTS physical manuscript: direct target glyphs, no explicit Hai in exact span.
    if ziwei_korea_cnts_late_zi_evidence.get("batch_id") != "BATCH-12-ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-Z":
        fail("Batch 12Z machine evidence batch identity mismatch")
    acq12z = ziwei_korea_cnts_late_zi_evidence.get("korea_cnts_acquisition", {})
    if acq12z.get("workflow_run_id") != 34247945308 or acq12z.get("artifact_id") != 10064784871:
        fail("Batch 12Z Korea CNTS run/artifact binding regressed")
    if acq12z.get("artifact_zip_sha256") != "64b1729df1523991a4ac764e8a4672cf7b6edeb41f94b56a47da49d5b17a6f95":
        fail("Batch 12Z Korea CNTS artifact digest regressed")
    if acq12z.get("pdf_sha256") != "b21bbf3e2c7cdada4153f847ff9f359dbb29e71998e1f931417d108b571b23c3" or acq12z.get("pdf_page_count") != 153:
        fail("Batch 12Z Korea CNTS source PDF identity regressed")
    sid12z = ziwei_korea_cnts_late_zi_evidence.get("source_identity", {})
    if sid12z.get("cnts_id") != "CNTS-00047996572" or sid12z.get("format_identifier") != "KOL200100663":
        fail("Batch 12Z Korea CNTS institutional identity regressed")
    if sid12z.get("direct_cover_pdf_page_1") != "秘傳紫微 / 春岡藏":
        fail("Batch 12Z Springgang cover identity regressed")
    coll12z = ziwei_korea_cnts_late_zi_evidence.get("direct_physical_collation_no_ocr", {})
    p124z = coll12z.get("pdf_page_124", {})
    p125z = coll12z.get("pdf_page_125", {})
    if "五神天殤天使奏書直符將軍" not in p124z.get("direct_glyphs", ()) or not any("凡五凶神" in x for x in p124z.get("direct_glyphs", ())):
        fail("Batch 12Z 五神/五凶神 direct physical glyph binding regressed")
    if p125z.get("direct_glyphs") != "命有稱兩時者可詳之子有十刻上五刻屬昨夜下五刻屬今夜":
        fail("Batch 12Z late-Zi direct physical glyph binding regressed")
    if p125z.get("explicit_hai_glyph_observed_in_exact_target_span") is not False or p125z.get("explicit_current_night_zi_glyph_observed_in_exact_target_span") is not False:
        fail("Batch 12Z exact target-span non-Hai/non-Zi boundary regressed")
    phil12z = ziwei_korea_cnts_late_zi_evidence.get("philological_adjudication", {})
    if phil12z.get("relation") != "SAME_FIVE_ENTITY_SET_DIFFERENT_PHRASE_ROLES_IN_SAME_PHYSICAL_PASSAGE":
        fail("Batch 12Z 五神/五凶神 phrase-role adjudication regressed")
    if phil12z.get("silent_wushen_to_wuxiongshen_character_correction_authorized") is not False:
        fail("Batch 12Z silent normalization firewall regressed")
    temp12z = ziwei_korea_cnts_late_zi_evidence.get("temporal_adjudication", {})
    if temp12z.get("explicit_hai_reclassification_in_korea_manuscript") is not False:
        fail("Batch 12Z Korea explicit-Hai boundary regressed")
    ev12z = ziwei_korea_cnts_late_zi_evidence.get("evidence_independence", {})
    if ev12z.get("direct_physical_target_text_witness_increment") != 1 or ev12z.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12Z physical/Hai witness accounting regressed")
    ad12z = ziwei_korea_cnts_late_zi_evidence.get("adjudication", {})
    if ad12z.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or ad12z.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12Z HPA/algorithm firewall regressed")
    row12z = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12z or row12z.get("batch_12z_korea_cnts_direct_collation_artifact") != "docs/research/ZIWEI-KOREA-CNTS-ZIWEIDOUSHUFANGSHU-DIRECT-LATE-ZI-COLLATION-R1.json":
        fail("Batch 12Z Matrix artifact binding regressed")
    if row12z.get("korea_cnts_explicit_hai_glyph_in_exact_target_span") is not False or row12z.get("independent_hai_glyph_witness_count_added_batch_12z") != 0:
        fail("Batch 12Z Matrix Hai-glyph firewall regressed")
    src12z = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-KOREA-NLK-CNTS-00047996572-ZIWEIDOUSHUFANGSHU"), None)
    if not src12z or src12z.get("pdf_sha256") != "b21bbf3e2c7cdada4153f847ff9f359dbb29e71998e1f931417d108b571b23c3":
        fail("Batch 12Z registry source missing or PDF identity regressed")
    if src12z.get("explicit_hai_glyph_in_exact_target_span") is not False or src12z.get("direct_ocr_used") is not False:
        fail("Batch 12Z registry direct-glyph/no-OCR boundary regressed")

    # Batch 12AA Hui County official catalog binding: provenance upgrade only, zero Hai votes.
    if not ZIWEI_HUIXIAN_CATALOG_BATCH.is_file() or not ZIWEI_HUIXIAN_CATALOG_EVIDENCE.is_file():
        fail("Batch 12AA continuity artifacts missing")
    if ziwei_huixian_catalog_evidence.get("batch_id") != "BATCH-12-ZIWEI-HUIXIAN-MUSEUM-OFFICIAL-ILLUSTRATED-CATALOG-ROUTE-AA":
        fail("Batch 12AA evidence identity mismatch")
    off12aa = ziwei_huixian_catalog_evidence.get("official_catalog_publication", {})
    if off12aa.get("ziwei_entry_start_page") != 233 or off12aa.get("direct_page_233_image_observed") is not False:
        fail("Batch 12AA Hui County official catalog page boundary regressed")
    if off12aa.get("direct_late_zi_target_page_observed") is not False:
        fail("Batch 12AA target-page firewall regressed")
    ae12aa = ziwei_huixian_catalog_evidence.get("official_booktext_postback_ae", {})
    if ae12aa.get("response_sha256") != "9172da23a2d292c9fc86965a0dad0673ac25be7bfb5e0944f628fa0ad035be10":
        fail("Batch 12AA official Booktext digest regressed")
    if ae12aa.get("contains_late_zi_target_sentence") is not False:
        fail("Batch 12AA Booktext target firewall regressed")
    ad12aa = ziwei_huixian_catalog_evidence.get("adjudication", {})
    if ad12aa.get("direct_independent_fullbook_hai_glyph_witness_increment") != 0 or ad12aa.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AA witness/algorithm firewall regressed")
    row12aa = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12aa or row12aa.get("batch_12aa_huixian_official_catalog_artifact") != "docs/research/ZIWEI-HUIXIAN-MUSEUM-OFFICIAL-ILLUSTRATED-CATALOG-ROUTE-R1.json":
        fail("Batch 12AA Matrix artifact binding regressed")
    if row12aa.get("independent_hai_glyph_witness_count_added_batch_12aa") != 0:
        fail("Batch 12AA Matrix Hai-vote firewall regressed")
    src12aa = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-HUIXIAN-MUSEUM-NLCPRESS-2025-ZWDSQJ-CATALOG"), None)
    if not src12aa or src12aa.get("entry_start_page") != 233 or src12aa.get("independent_witness_increment") != 0:
        fail("Batch 12AA registry binding regressed")

    # Batch 12AB Jingshutang Artron physical imprint route: title-page identity only, zero target-text/Hai votes.
    if not ZIWEI_JINGSHUTANG_ARTRON_BATCH.is_file() or not ZIWEI_JINGSHUTANG_ARTRON_EVIDENCE.is_file():
        fail("Batch 12AB continuity artifacts missing")
    if ziwei_jingshutang_artron_evidence.get("batch_id") != "BATCH-12-ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-AB":
        fail("Batch 12AB evidence identity mismatch")
    img12ab = ziwei_jingshutang_artron_evidence.get("exact_source_emitted_image", {})
    if img12ab.get("sha256") != "44c0369f078d27894579b10208f8906ed3592a814a2bc8d58a8f2760090a9685":
        fail("Batch 12AB source image digest regressed")
    if img12ab.get("imprint_reading") != "經述堂藏板" or img12ab.get("direct_ocr_used") is not False:
        fail("Batch 12AB direct imprint/no-OCR boundary regressed")
    if img12ab.get("target_late_zi_page_observed") is not False or img12ab.get("target_hai_glyph_observed") is not False:
        fail("Batch 12AB target-page/Hai firewall regressed")
    phil12ab = ziwei_jingshutang_artron_evidence.get("philological_adjudication", {})
    if phil12ab.get("observed_imprint_is") != "經述堂" or phil12ab.get("independent_textual_witness_increment") != 0 or phil12ab.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12AB philology/witness accounting regressed")
    if "繼述堂" not in phil12ab.get("do_not_normalize_to", ()) or "經綸堂" not in phil12ab.get("do_not_normalize_to", ()):
        fail("Batch 12AB imprint-normalization firewall regressed")
    ad12ab = ziwei_jingshutang_artron_evidence.get("adjudication", {})
    if ad12ab.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or ad12ab.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AB HPA/algorithm firewall regressed")
    row12ab = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ab or row12ab.get("batch_12ab_jingshutang_artron_physical_imprint_artifact") != "docs/research/ZIWEI-JINGSHUTANG-ARTRON-PHYSICAL-IMPRINT-ROUTE-R1.json":
        fail("Batch 12AB Matrix artifact binding regressed")
    if row12ab.get("jingshutang_artron_source_image_sha256") != "44c0369f078d27894579b10208f8906ed3592a814a2bc8d58a8f2760090a9685":
        fail("Batch 12AB Matrix image binding regressed")
    if row12ab.get("independent_textual_witness_count_added_batch_12ab") != 0 or row12ab.get("independent_hai_glyph_witness_count_added_batch_12ab") != 0:
        fail("Batch 12AB Matrix witness firewall regressed")
    src12ab = next((s for s in registry.get("sources", ()) if s.get("source_id") == "EXT-ARTRON-TAIHEJIACHENG-2017-JINGSHUTANG-ZWDSQS"), None)
    if not src12ab or src12ab.get("source_image_sha256") != "44c0369f078d27894579b10208f8906ed3592a814a2bc8d58a8f2760090a9685":
        fail("Batch 12AB registry source/image binding regressed")
    if src12ab.get("target_page_observed") is not False or src12ab.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12AB registry target/Hai firewall regressed")


    # Batch 12AC Wenguang PT165 public Viewer-response closure: page metadata is not physical glyph authority.
    if not ZIWEI_WENGUANG_PT165_RESPONSE_BATCH.is_file() or not ZIWEI_WENGUANG_PT165_RESPONSE_EVIDENCE.is_file():
        fail("Batch 12AC continuity artifacts missing")
    if ziwei_wenguang_pt165_response_evidence.get("batch_id") != "BATCH-12-ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-AC":
        fail("Batch 12AC evidence identity mismatch")
    ctl12ac = ziwei_wenguang_pt165_response_evidence.get("controlling_public_probe", {})
    if ctl12ac.get("workflow_run_id") != 34310657883 or ctl12ac.get("artifact_id") != 10088226638:
        fail("Batch 12AC controlling execution binding regressed")
    if ctl12ac.get("artifact_zip_sha256") != "cdbfaf35561588e6001f7eb6af5b61a4aed83261beba749ee0e6ccc45e5378d2":
        fail("Batch 12AC controlling artifact digest regressed")
    run12ac = ctl12ac.get("viewer_run_response", {})
    if run12ac.get("http_status") != 200 or run12ac.get("bytes") != 0 or run12ac.get("source_emitted_image_url_count") != 0:
        fail("Batch 12AC public Viewer run-response boundary regressed")
    pages12ac = {item.get("page_id"): item for item in ctl12ac.get("click3_responses", ())}
    pt165_12ac = pages12ac.get("PT165", {})
    if pt165_12ac.get("http_status") != 200 or pt165_12ac.get("bytes") != 3288:
        fail("Batch 12AC PT165 click3 response binding regressed")
    if pt165_12ac.get("target_page_record") != {"pid": "PT165", "flags": 8, "order": 165}:
        fail("Batch 12AC PT165 page-object record regressed")
    if pt165_12ac.get("returned_page_record_count") != 209:
        fail("Batch 12AC click3 page-count binding regressed")
    if ctl12ac.get("source_emitted_image_url_count") != 0 or ctl12ac.get("pt165_image_saved") is not False or ctl12ac.get("target_glyph_directly_observed") is not False:
        fail("Batch 12AC image/glyph firewall regressed")
    ad12ac = ziwei_wenguang_pt165_response_evidence.get("adjudication", {})
    if ad12ac.get("hpa_zdate_006") != "MISSING_FROM_PRODUCT" or ad12ac.get("algorithm_reopen_authorized") is not False:
        fail("Batch 12AC HPA/algorithm firewall regressed")
    if ad12ac.get("independent_textual_witness_increment") != 0 or ad12ac.get("independent_hai_glyph_witness_increment") != 0:
        fail("Batch 12AC witness accounting regressed")
    row12ac = next((r for r in matrix.get("rows", ()) if r.get("rule_id") == "HPA-ZDATE-006"), None)
    if not row12ac or row12ac.get("batch_12ac_wenguang_pt165_public_viewer_response_artifact") != "docs/research/ZIWEI-WENGUANG-PT165-PUBLIC-VIEWER-RESPONSE-CLOSURE-R1.json":
        fail("Batch 12AC Matrix artifact binding regressed")
    if row12ac.get("wenguang_pt165_click3_target_record") != {"pid": "PT165", "flags": 8, "order": 165}:
        fail("Batch 12AC Matrix PT165 record regressed")
    if row12ac.get("wenguang_pt165_click3_source_emitted_image_url_count") != 0 or row12ac.get("wenguang_pt165_direct_target_image_observed_batch_12ac") is not False:
        fail("Batch 12AC Matrix image firewall regressed")
    if row12ac.get("independent_textual_witness_count_added_batch_12ac") != 0 or row12ac.get("independent_hai_glyph_witness_count_added_batch_12ac") != 0:
        fail("Batch 12AC Matrix witness firewall regressed")

    if invariants.get("confirmed_chart_algorithm_defect_count") != audit_summary.get("confirmed_chart_algorithm_defect_count"):
        fail("chart algorithm defect count drift")
    if invariants.get("algorithm_reopen_count") != audit_summary.get("algorithm_reopen_count"):
        fail("algorithm reopen count drift")
    if invariants.get("candidate_collapse_count") != audit_summary.get("candidate_collapse_count"):
        fail("candidate collapse count drift")

    bootstrap = "\n".join(state.get("new_chat_bootstrap_order", ()))
    for fragment in (
        "live GitHub branch HEAD",
        "recent commit history",
        "GitHub Actions",
        "PROJECT-CONTINUITY-PROTOCOL-R1.md",
        "PROJECT-CURRENT-STATE-R1.json",
        "FUSION-CHART-RESEARCH-AUTHORITY-POLICY-R1.md",
    ):
        if fragment not in bootstrap:
            fail(f"new-chat bootstrap order missing required step: {fragment}")

    authority_text = AUTHORITY.read_text(encoding="utf-8")
    protocol_text = PROTOCOL.read_text(encoding="utf-8")
    if "Philology / 训诂" not in authority_text or "PHILOLOGICALLY_AMBIGUOUS_PRESERVE_CANDIDATES" not in authority_text:
        fail("research authority policy lost philology/训诂 method")
    if "Exhaustive research horizon and conflict adjudication" not in authority_text:
        fail("research authority policy lost exhaustive-horizon/conflict-adjudication method")
    if "FIRST_SOURCE_STOP=FORBIDDEN_WHEN_MATERIAL_ADDITIONAL_WITNESSES_ARE_SEARCHABLE" not in authority_text:
        fail("research authority policy lost first-source stopping prohibition")
    if "FALSE_EQUIVALENCE_OF_DEMONSTRATED_TRANSMISSION_ERROR=FORBIDDEN" not in authority_text:
        fail("research authority policy lost false-equivalence prohibition")
    if "Philological continuity rule" not in protocol_text:
        fail("continuity protocol lost philological continuity rule")

    contract = state.get("continuity_contract", {})
    if contract.get("ci_gate_required") is not True:
        fail("continuity CI gate was disabled")
    if contract.get("verifier") != "scripts/verify-project-continuity-state-r1.py":
        fail("continuity verifier identity mismatch")

    print(json.dumps({
        "schema": "ZIWEI-BAZI-PROJECT-CONTINUITY-STATE-R1-GATE",
        "status": "PASS",
        "branch": EXPECTED_BRANCH,
        "stage": state.get("current_stage"),
        "row_count": audit_state.get("row_count"),
        "audited_row_count": audit_state.get("audited_row_count"),
        "completed_batch_count": len(state_batches),
        "latest_batch": LATEST_BATCH_ID,
        "provenance_defect_count": audit_state.get("confirmed_provenance_metadata_defect_count"),
        "chart_algorithm_defect_count": invariants.get("confirmed_chart_algorithm_defect_count"),
        "s00_s19_status": authority.get("s00_s19_status"),
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
