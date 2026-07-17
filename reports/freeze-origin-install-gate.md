# Freeze-origin installation gate

The installation validator now treats the CHAT/WORK handoff-to-freeze origin chain as a required runtime capability.

Required properties:

- `fortune-v1 freeze` requires `--handoff-receipt`;
- the handoff receipt schema is `CHAT-WORK-PREDICTION-HANDOFF-RECEIPT-V1`;
- identity, binding, prediction hash, and contract hash are replayed before freeze;
- the formal freeze receipt records `CHAT_WORK_HANDOFF_VERIFIED`;
- removing or weakening this registration fails `EXTERNAL_PREDICTION_RUNNER` during installation validation.

This change does not alter S00-S19 knowledge, prediction semantics, scoring, or answer data.
