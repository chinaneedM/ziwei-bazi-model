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
