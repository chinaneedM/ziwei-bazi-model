# DEV-GROUP-001 integrity repair

DEV-GROUP-001 is intentionally held at revision 0003. Four legacy gzip+Base64 case objects do not match their prewrite registry values and cannot be reproduced to the registered logical JSON hashes. They remain quarantined for audit and must not enter prediction.

The repair changes new runtime storage to plain canonical JSON, validates repository readback bytes and SHA-256 values, strictly materializes every case, checks the canonical logical JSON hash, and requires all cases to pass before `READY_FOR_BASELINE_PREDICTION` can be emitted.

Resume only after DEV-EXAMPLE-001 through DEV-EXAMPLE-004 are reimported from trusted no-answer sources and the group validator returns `PASS_READY`. Do not use answer-vault data to reconstruct runtime cases.
