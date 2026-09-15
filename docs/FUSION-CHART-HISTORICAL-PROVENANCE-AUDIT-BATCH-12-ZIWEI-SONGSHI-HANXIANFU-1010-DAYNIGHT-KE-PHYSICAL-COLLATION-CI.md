    # Fusion Chart Historical Provenance Audit R1 — Batch 12CI

    ## 1010 韓顯符精細二十四氣晝夜刻表 × 明代粗表 24/24 量化重放

    Status: **RECEIVED SONGSHI PHYSICAL WITNESS DIRECTLY COLLATED / RECORDED 1010 HAN XIANFU TECHNICAL EVENT DATE SEPARATED FROM SURVIVING COPY DATE / 147-UNIT RESIDUAL DENOMINATOR INFERRED BY 100-KE CONSERVATION / FULL 24-TERM MING COARSE TABLE DIRECTLY RECOLLATED / 24/24 SINGLE-THRESHOLD QUANTIZATION COMPATIBILITY CLOSED / MODERN 0.5 ROUNDING REJECTED BY DAHAN-XIAOXUE / EXACT HISTORICAL ROUNDING INSTRUCTION AND DIRECT TEXTUAL GENEALOGY STILL OPEN / SANMING STILL REQUIRES NANJING ADAPTATION / HPA-ZDATE-006 UNCHANGED / NO ALGORITHM REOPEN**

    ## 1. Direct source and date firewall

    `CADAL06060929《宋史·卷六十九~卷七十》` was downloaded from the Zhejiang University/CADAL object exposed through Wikimedia Commons and rendered page-by-page without OCR.

    ```text
    RUN=34932102620
    JOB=104262273291
    ARTIFACT=10382077226
    ARTIFACT_DIGEST=sha256:754a9132f6ec902fe6393a34ef0d9e1a254fc1f86104341af4ea26745a279e75
    SOURCE_DJVU_SHA256=de3e5f7311b4190d790df6ababde566a45a3c0e45c463d59b46b3a88671094a1
    DERIVED_PDF_SHA256=63866e4696bbd2f2950d983162d71e8587f04760ae0f06bc912ec4c98edb2976
    PAGES=152
    OCR_USED_FOR_GLYPH_CLAIMS=false
    ```

    Physical p119->p120 records `大中祥符三年春官正韓顯符上銅渾儀法要`, followed by the statement that the work contains a 24-qi day/night advance-retreat and sunrise/sunset ke-number established method, and then the table.

    The date firewall is mandatory:

    ```text
    1010 = recorded Northern-Song technical event/submission date
    1010 != date of the current surviving scanned physical copy
    later Songshi compilation != original Han Xianfu autograph
    modern CADAL surrogate != medieval physical object
    ```

    ## 2. The 147 residual denominator

    The physical table does **not** use modern decimal notation. Representative day/night rows are:

    ```text
    冬至  晝40刻5    夜59刻142
    大寒  晝41刻78   夜58刻69
    清明  晝52刻81   夜47刻66
    夏至  晝59刻142  夜40刻5
    ```

    In every non-equinox row:

    ```text
    integer(day) + integer(night) = 99
    residual(day) + residual(night) = 147
    total = 100 ke
    ```

    Therefore the mechanically implied residual denominator is `147` parts per ke. This is an inference from conservation, not an explicit unit-name sentence in the reviewed passage. `59刻142` must not be parsed as `59.142`.

    ## 3. Full physical comparison with the Ming coarse table

    Batch 12CE had already identified the Ming-print `《類編曆法通書》` coarse `40<->60` family. This batch re-reviews all physical pp18–24 so all 24 anchors, not only the earlier eight summer examples, participate in the replay.

    | 節氣 | 1010精細晝刻 | 明粗表晝刻 | 現代最近整數 | 閾值模型命中 |
    |---|---:|---:|---:|---:|
    | 冬至 | 40 + 5/147 | 40 | 40 | YES |
| 小寒 | 40 + 55/147 | 40 | 40 | YES |
| 大寒 | 41 + 78/147 | 41 | 42 | YES |
| 立春 | 43 + 34/147 | 43 | 43 | YES |
| 雨水 | 45 + 30/147 | 45 | 45 | YES |
| 驚蟄 | 47 + 66/147 | 47 | 47 | YES |
| 春分 | 50 + 0/147 | 50 | 50 | YES |
| 清明 | 52 + 81/147 | 53 | 53 | YES |
| 穀雨 | 54 + 137/147 | 55 | 55 | YES |
| 立夏 | 57 + 6/147 | 57 | 57 | YES |
| 小滿 | 58 + 99/147 | 59 | 59 | YES |
| 芒種 | 59 + 102/147 | 60 | 60 | YES |
| 夏至 | 59 + 142/147 | 60 | 60 | YES |
| 小暑 | 59 + 102/147 | 60 | 60 | YES |
| 大暑 | 58 + 99/147 | 59 | 59 | YES |
| 立秋 | 57 + 6/147 | 57 | 57 | YES |
| 處暑 | 54 + 137/147 | 55 | 55 | YES |
| 白露 | 52 + 81/147 | 53 | 53 | YES |
| 秋分 | 50 + 0/147 | 50 | 50 | YES |
| 寒露 | 47 + 66/147 | 47 | 47 | YES |
| 霜降 | 45 + 30/147 | 45 | 45 | YES |
| 立冬 | 43 + 34/147 | 43 | 43 | YES |
| 小雪 | 41 + 78/147 | 41 | 42 | YES |
| 大雪 | 40 + 55/147 | 40 | 40 | YES |

    Result:

    ```text
    SINGLE_THRESHOLD_24_OF_24_MATCH=true
    LARGEST_RESIDUAL_KEPT_DOWN=78
    SMALLEST_RESIDUAL_ADVANCED=81
    ADMISSIBLE_THRESHOLD=(78,81]/147
    MODERN_NEAREST_INTEGER_MATCH=22/24
    MODERN_NEAREST_INTEGER_MISSES=大寒,小雪
    ```

    At `大寒` and `小雪` the Song value is `41 + 78/147 ~= 41.530612`. Modern nearest-integer rounding would produce 42, while the direct Ming table prints 41. Therefore **modern 0.5 rounding is not the historical rule represented by this coarse table**.

    No row contains residual 79 or 80, so the physical data cannot distinguish an exact threshold of 79, 80 or 81 residual units. The correct conclusion is an interval, not an invented exact rounding command.

    ## 4. Transmission consequence

    The evidence now supports a materially stronger but still fail-closed model:

    ```text
    recorded 1010 precision 24-qi leak-clock table
        -> 24/24 mechanically compatible coarse integer 40<->60 family
           [exact textual route / rounding instruction unresolved]
        + early-Ming Nanjing/Datong locality layer
        -> later recomposed/adapted displays including 1578 Sanming
    ```

    This is not a direct-copy claim. It is a **structural ancestry candidate** with unusually strong numerical support.

    ## 5. Why this still does not generate the 1578 Sanming table

    The same coarse quantization gives values such as `小寒 40`, `立春 43`, `夏至 60`. The 1578 `《三命通會》` display instead includes `小寒 42/58`, `立春 45/55`, `雨水 47/53 then 48/52`, and `夏至 59/41`.

    Therefore Sanming is not simply the Song precision table rounded into integers. The already established Ming/Nanjing daily numerical and locality-standard layers remain necessary.

    ## 6. Product adjudication

    ```text
    HPA-ZDATE-006=MISSING_FROM_PRODUCT
    UPPER_ZI_TO_HAI_VOTE_INCREMENT=0
    NEW_RUNTIME_CANDIDATE=false
    RUNTIME_WINNER=false
    CANDIDATE_COLLAPSE=false
    CONFIRMED_CHART_ALGORITHM_DEFECT_COUNT=0
    ALGORITHM_REOPEN_COUNT=0
    DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
    ```

    This batch changes historical transmission knowledge, not deterministic chart code.

    ## 7. Next gate

    1. locate an independent early physical witness for the same precision/coarse conversion or an explicit rounding/selection instruction that can resolve the `(78,81]/147` threshold;
    2. audit the near-contemporary `《虎鈐經》傳箭` integer 48-arrow system as a separate Song operational lineage, without assuming it copied Han Xianfu;
    3. continue the separate pre-1578 search for the exact Nanjing/Sanming `59/41` cap plus intermediate change-day fingerprint;
    4. keep Fullbook upper-five-ke -> Hai research independent from this seasonal-table ancestry work.

    Research record: `docs/research/SONGSHI-HANXIANFU-1010-DAYNIGHT-KE-PHYSICAL-COLLATION-R1.json`.
