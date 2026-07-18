# Clean-start requests

Create exactly one immutable JSON request per new group run. The request contains control metadata only; it must not contain case text, predictions, answers, reveal data, diagnostics, or prior-run summaries.

Required schema:

```json
{
  "schema": "GROUP-CLEAN-START-REQUEST-V1",
  "status": "REQUESTED",
  "requested_group_id": "DEV-GROUP-002",
  "group_run_id": "GROUP-R17-CLEAN-...",
  "session_id": "CHAT-R17-CLEAN-...",
  "mode": "CHAT_ONLY",
  "allowed_repository": "chinaneedM/ziwei-bazi-model",
  "forbidden_repository": "chinaneedM/fortune-answer-vault",
  "answer_vault_physical_access_test_status": "PASS_INACCESSIBLE",
  "repository_search_used_before_request": false,
  "commit_history_used_before_request": false,
  "old_run_objects_visible_before_request": false
}
```

A push containing `runtime/clean-start-requests/<GROUP_RUN_ID>.json` triggers the repository workflow. The resulting immutable object is written to `data/group-clean-starts/<GROUP_RUN_ID>/clean-start.json` with five derived case run IDs and an exact pre-freeze allowlist.
