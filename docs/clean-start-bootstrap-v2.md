# Clean-start bootstrap V2

## Problem repaired

The former protocol required a fresh prediction chat to create `GROUP-CLEAN-START-REQUEST-V1` as its first repository action. The request itself required the active group ID, repository bindings, answer-vault status, session ID and pointer-derived release bindings. A fresh chat that only received a `GROUP_RUN_ID` could not know those fields without first reading or searching the repository. That read was then treated as pre-request contamination, creating an endless restart loop.

This was a protocol defect, not a user-operation error.

## V2 boundary

`GROUP-CLEAN-START-REQUEST-V2` is materialized before the prediction context starts by an engineering or repository automation context. It binds:

- the exact active `CURRENT_GROUP_MANIFEST` hash;
- the requested group run and session IDs;
- the allowed and forbidden repositories;
- the answer-vault isolation basis;
- the future exact clean-start path.

The request does not claim that the engineering context is blind. Instead, it records that the prediction context has not started. The repository workflow then creates and hardens the immutable staged clean start.

## Prediction entrypoint

For a prepared run ID, the prediction chat must not search the repository, inspect commit history, read a start-intent file or reconstruct hidden request fields. Its first repository action is an exact-path fetch of:

```text
data/group-clean-starts/{GROUP_RUN_ID}/clean-start.json
```

After that fetch, the chat may read only paths listed in the clean start's active PREBLIND allowlist. Option payloads remain withheld until all required machine-valid dual-track preblind seals exist.

## Compatibility

`GROUP-CLEAN-START-REQUEST-V1` remains accepted for existing callers. The staged clean-start script automatically routes V1 requests through the legacy validator and V2 requests through the preauthorized validator.

## Failure behavior

The run still fails closed when:

- the active pointer changes after authorization;
- the pointer does not prove answer isolation;
- the V2 request reports that the prediction context already started;
- the prediction context used repository search, commit history or old-run objects;
- the exact output run ID already exists.

The repair removes only the circular bootstrap dependency. It does not weaken answer isolation, staged option access, immutable run IDs or provenance validation.
