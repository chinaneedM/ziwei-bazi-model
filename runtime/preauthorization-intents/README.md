# Group clean-start preauthorization intents

This directory is the control-only entrypoint used before a prediction context starts.

Each new group run uses one immutable JSON intent:

```json
{
  "schema": "GROUP-CLEAN-START-PREAUTHORIZATION-INTENT-V1",
  "status": "REQUESTED",
  "requested_group_id": "DEV-GROUP-002",
  "group_run_id": "GROUP-RUN-...",
  "session_id": "CHAT-R17-CLEAN-...",
  "mode": "CHAT_ONLY"
}
```

The intent must not contain case content, options, predictions, answers, reveal data, prior-run summaries, private repository coordinates, or copied pointer fields.

A push containing `runtime/preauthorization-intents/*.json` runs the repository preauthorization workflow. Repository code reads the exact active `CURRENT_GROUP_MANIFEST`, creates the full `GROUP-CLEAN-START-REQUEST-V2`, materializes the staged clean start, validates answer isolation, and commits immutable generated objects to the same branch.

The future prediction context must begin by fetching only the exact generated `data/group-clean-starts/<GROUP_RUN_ID>/clean-start.json` path. Creating an intent does not begin prediction and does not make the run score-eligible.
