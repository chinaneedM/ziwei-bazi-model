# Fusion Chart Research Authority Policy R1

## Status

```text
FUSION_CHART_RESEARCH_AUTHORITY_POLICY_R1=ACTIVE
S00_S19_EPISTEMIC_STATUS=PROJECT_RESEARCH_CORPUS_NOT_INERRANT_AUTHORITY
MODERN_REFERENCE_SOFTWARE_STATUS=COMPATIBILITY_WITNESS_ONLY
HISTORICAL_WINNER_SELECTION=EVIDENCE_GATED
```

## 1. Purpose

This policy governs historical/provenance research for the deterministic Ziwei
Dou Shu + Four Pillars fusion chart system.

The repository directory name `sources/canonical/` is a **storage/freeze
identity inherited from the earlier project architecture**. It must not be read
as a claim that S00–S19 are infallible historical authorities.

S00–S19 were assembled, studied, normalized and summarized during project
development. They are valuable research material, but they can contain:

- transcription or extraction errors;
- modern editorial interpretations;
- unattributed or misattributed quotations;
- school-specific rules presented too broadly;
- compatibility-oriented summaries;
- omissions of competing historical methods;
- normalization choices that hide wording or edition differences.

Therefore every chart-affecting claim in S00–S19 remains auditable.

## 2. Evidence classes

Historical audit should distinguish at least these evidence classes.

### A. Primary / near-primary textual witness

Examples:

- dated early printed editions;
- reliable facsimiles;
- library-held rare-book scans;
- edition-specific transcriptions whose identity can be independently checked.

These are the strongest witnesses for historical wording and mechanical rules,
but even primary witnesses may represent one recension or school rather than a
universal winner.

### B. Received historical text

Later received editions or transcriptions of classical works. Useful and often
decisive for a received tradition, but edition history and textual variants must
remain explicit.

### C. Library / bibliographic witness

Library catalogs, linked-data records and bibliographies. Strong for title,
edition, date, printer/publisher, holding identity and provenance. They do not
substitute for rule-text collation.

### D. Project research corpus: S00–S19

Internal frozen research material. It is a high-value discovery/indexing source
and can preserve verbatim historical atoms, but each claim must be classified
by the underlying evidence it actually contains. The S-number itself is not
historical authority.

### E. Secondary scholarship / school manuals

Useful for transmission history, school attribution, disputed-method surveys,
commentary and locating primary sources. They must be labeled as secondary or
school-specific.

### F. Modern software / compatibility fixtures

Examples include Wenmo Tianji and Wenzhen Bazi. They may identify behavior,
compatibility deltas or candidate methods. Observation alone never proves
historical or classical authority.

## 3. Audit rule

A rule may be marked `HISTORICALLY_SUPPORTED` only when the support is bound
to the actual underlying witness, not merely to an S00–S19 summary label.

For each chart-affecting rule, prefer the following chain:

```text
implementation
-> exact mechanical rule
-> project atom / source locator
-> underlying work + chapter/section
-> edition / date / bibliographic identity
-> competing witnesses / schools
-> implementation replay
```

Where any link is missing, the audit status must preserve that uncertainty.

## 4. Contradictions

If S00–S19 conflict with stronger or more precise evidence:

1. do not silently rewrite history;
2. record the conflict in the Historical Provenance Audit Matrix;
3. identify whether the defect is transcription, attribution, normalization,
   school scope, provenance metadata or implementation;
4. preserve genuinely disputed methods as separate candidates;
5. reopen a deterministic algorithm only when a reproducible implementation
   mismatch is established against sufficiently strong scoped evidence;
6. make all repairs forward-only.

The existence of a contradiction does not automatically prove the repository
algorithm is wrong. It may instead reveal a provenance or scope defect.

## 5. No privileged corpus by filename

Neither of these statements is allowed:

```text
"S00-S19 says it, therefore it is correct."
"An ancient book says it, therefore it is the unique correct method."
```

Historical authority is scoped by edition, wording, transmission and school.
Where witnesses disagree, the product should preserve candidates unless a
specific product profile intentionally and transparently selects one.

## 6. Product relationship

This research policy does not itself reopen the already closed deterministic
Fusion Chart Product R1.

```text
DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED
ALGORITHM_REOPEN=EVIDENCE_AND_REPLAY_GATED
ZIWEI_SELF_INWARD_TRANSFORMATION_DIRECTION=NOT_YET_FORMALIZED
```

Historical audit may discover:

- no defect;
- provenance metadata defect;
- missing candidate family;
- school-specific method;
- true deterministic implementation defect.

Only the last category authorizes a local algorithm reopen, and only with the
explicit matrix gate.

## 7. Terminology

For historical/provenance work, use:

- **project research corpus** or **frozen project corpus** for S00–S19;
- **primary witness**, **received witness**, **bibliographic witness**,
  **secondary witness**, or **compatibility witness** for evidence;
- **canonical storage path** only when referring to the repository path or
  integrity/freeze mechanism, not epistemic truth.

This policy supersedes earlier wording that could imply S00–S19 were
infallible or uniquely authoritative for historical chart rules.

## 8. Philology / 训诂 and terminology normalization

Historical chart research must include philological interpretation before
mechanical rule extraction.

The same mechanical concept can be written with different vocabulary across
editions, periods or schools. Conversely, the same written term can carry
different technical meanings in different contexts. Therefore rule matching
must not rely on surface-string equality alone.

For every materially chart-affecting passage, distinguish:

1. **字词形态** — variant glyphs, traditional/simplified forms, scribal or
   editorial variants, aliases and historical spellings;
2. **训诂义** — what the word or phrase means in that edition and sentence,
   not what a modern software label happens to call it;
3. **句法角色** — anchor, direction, count, inclusion/exclusion, temporal
   layer, subject and object;
4. **mechanical concept identity** — whether differently worded passages
   actually describe the same algorithm;
5. **homonym separation** — whether identical names belong to different
   systems, stars, rings, calendar deities or rule families;
6. **school transmission** — whether later wording is a renamed inheritance,
   a scoped extension, or a genuinely different method.

Examples of terms requiring contextual normalization include `垣/宫`,
`岁建/太岁`, `运马/流马`, `起/从/加`, `月上/日上`, and historical
`杀/煞` spellings.

Allowed conclusion patterns include:

- `DIFFERENT_WORDING_SAME_MECHANICAL_RULE`;
- `SAME_TERM_DIFFERENT_TECHNICAL_CONCEPT`;
- `NORMALIZED_LABEL_WITH_EXPLICIT_HISTORICAL_NAME_BRIDGE`;
- `PHILOLOGICALLY_AMBIGUOUS_PRESERVE_CANDIDATES`.

训诂 is evidence interpretation, not evidence invention. If two readings are
both grammatically and historically viable and imply different coordinates,
preserve them as competing candidates until stronger evidence closes the
reading.
## 9. Exhaustive research horizon and conflict adjudication

Historical research is **open-ended**. Finding one plausible quotation, one familiar
manual, or one repository source does not close a rule when materially relevant
additional witnesses remain searchable.

The research horizon should expand, when relevant, across:

- different editions, recensions, manuscripts, printed books and facsimiles;
- official almanacs, court records, gazetteers, archival and institutional documents;
- Chinese, Japanese, Korean and other East Asian transmission witnesses;
- overseas library holdings and catalogues;
- Chinese- and foreign-language peer-reviewed scholarship, dissertations, critical editions and history-of-science research;
- modern computational reconstructions used strictly as validation, never as replacements for historical authority.

No finite search can prove that every surviving source has been found. Therefore the
operational requirement is **exhaustive to the current searchable horizon**: continue
until major source families, known edition variants, plausible contradictions and
independent validation routes have been actively searched.

### Conflict adjudication

Conflicting books are not decided by source-count voting. Weight evidence by:

1. chronological and textual proximity to the rule's actual use;
2. edition identity and directness of the witness;
3. independence of transmission;
4. whether the source preserves a worked mechanical example;
5. whether contemporary operational artifacts reproduce one reading rather than another;
6. internal mathematical/textual consistency;
7. deterministic replay against independently sourced oracle cases;
8. later scholarship only after the historical evidence classes above are kept distinct.

Candidate preservation is required for genuinely unresolved, school-specific or parallel
historical methods. It is **not** a reason to create false equivalence.

When primary/near-primary wording, independent contemporary worked evidence and
operational artifacts converge strongly on one mechanical rule, the audit should
adjudicate that historical rule and demote a contradicted reading to the appropriate
category, such as scribal/printing error, later received-text variant, editorial
normalization, school-specific alteration, or unresolved transmission variant.

Such historical adjudication does not automatically authorize runtime implementation.
Product implementation remains separately gated by complete mechanical reconstruction,
reproducible tests and the repository reopen policy.

RESEARCH_SCOPE=OPEN_ENDED_CROSS_EDITION_CROSS_REGION_CROSS_LANGUAGE_CROSS_DISCIPLINE
FIRST_SOURCE_STOP=FORBIDDEN_WHEN_MATERIAL_ADDITIONAL_WITNESSES_ARE_SEARCHABLE
CONFLICT_ADJUDICATION=EVIDENCE_WEIGHTED_NOT_SOURCE_COUNT
FALSE_EQUIVALENCE_OF_DEMONSTRATED_TRANSMISSION_ERROR=FORBIDDEN
