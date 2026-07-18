# DEV-GROUP-002 Training Regression R16 Freeze Receipt

- Round: `R16`
- Processed case: `DEV-EXAMPLE-004`
- Run class: `ANSWER_VISIBLE_SAME_CASE_SHADOW_REBUILD`
- Frozen interface: `TR-R14-CAPABILITY-NEUTRAL-TIME-SCENE-NORMALIZED-BURDEN-V1`
- Materialization commit: `98dbbf9f0b71f257ee3a07ac5ca02030615c3e44`
- Materializer script SHA256: `49538f865e1153c41c071f50aa18201e095e89bcf7820414488e57b189e11894`
- Manifest canonical SHA256: `f3d6bfd0641b9172158f31d7f78f7e40bd9c63dd77d423ed1da51699eedd0748`
- Prediction-freeze canonical SHA256: `17b1ff8461d192893c2b1de28fb38ad7495711d4305fc2f0bcfa1632e1f0e8d6`
- Validation blob SHA: `13d89de9b81cf054af1bf97636800cef69814917`
- Validation status: `PASS`

## Frozen relative result

| Question | Full rank |
|---|---|
| Q1 | `CABD` |
| Q2 | `BACD` |
| Q3 | `CDAB` |
| Q4 | `BCDA` |
| Q5 | `DBCA` |

- TOP1 vector: `CBCBD`
- TOP2 vector: `AADCB`
- Same-case training-regression TOP1: `9/25`
- Same-case training-regression TOP2: `13/25`
- Delta from R15: TOP1 `-1`, TOP2 `0`

## Machine-validated coverage

- Source excerpts: `20`
- Literal atom-direction rows: `90` (`45` Ziwei, `45` Bazi)
- Common-atom pair rows: `30`
- Material-common-atom rows: `2`
- Atom-level replayable pairwise rows: `30`
- Low-information tiebreak rows: `3`
- Pairwise cycles: `0`

## Fail-closed formal state

- Formal-valid questions: `0`
- Machine-valid local seals: `0`
- S03 formal fusions: `0`
- Formal release permission: `NO`
- New external case admission: `BLOCKED`
- Answer-visible score tuning permission: `NO`
- S00–S19 modified: `false`
- Base astrological knowledge changed: `false`
- Case-specific direction rule added: `false`

The lower same-case score is retained without answer-derived repair. R16 permits only the next fixed-group gate: `R17_CROSS_CASE_STABILITY_REVIEW_AND_DEV_EXAMPLE_005_GATE`.
