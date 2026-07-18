# DEV-GROUP-002 R10 freeze receipt

- Round: `R10`
- Frozen generated commit: `3def439723f354036d506e47e8fe6cb269d98b10`
- Validator schema: `DEV-GROUP-002-R10-VALIDATION-V2`
- Validation status: `PASS`
- Historical rounds preserved: `R1` through `R9`
- Diagnosed case: `DEV-EXAMPLE-002`
- Common-atom pair rows: `30`
- Rows with material common atoms: `5`
- Pairwise provenance audit rows: `30`
- Atom-level replayable R9 pairwise rows: `0`
- Selection changed: `NO`
- Group training regression score: TOP1 `13/25`, TOP2 `16/25`
- Formal-valid questions: `0`
- Machine-valid local seals: `0`
- S03 fusions: `0`
- S00–S19 modified: `NO`
- Base astrological knowledge changed: `NO`
- Case-specific direction rule added: `NO`
- New-case admission: `BLOCKED`
- Required next round: `R11_REBUILD_PAIRWISE_FROM_LITERAL_ATOM_DIRECTION_PARENTS_WITHOUT_ANSWER_GUIDANCE`

R10 identifies generic execution defects only: common atoms were not materialized before R9 comparison, pairwise rows did not reference atom-level direction parents, and hand-authored aggregate keys substituted for mechanical atom replay. It preserves every R9 selection and does not infer a direction change from the answer.
