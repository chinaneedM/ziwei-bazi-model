# Public encrypted answer vault

This directory stores encrypted answer envelopes only.

Allowed path:

```text
public-answer-vault/encrypted/<GROUP_RUN_ID>.json.fernet
```

Rules:

- Never commit a plaintext `GROUP-ANSWER-VECTOR-V1` file.
- Never commit `FORTUNE_PUBLIC_ANSWER_KEY` or any generated key file.
- Encrypt plaintext outside the repository with `fortune-public-answer-vault encrypt`.
- Decrypt only after `GROUP_PREDICTION_FREEZE_PASS`.
- Decrypted plaintext must remain outside the repository tree and must be destroyed after the reveal job.
- No private repository or cross-repository token is part of this design.
