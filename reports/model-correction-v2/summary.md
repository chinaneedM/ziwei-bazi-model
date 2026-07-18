# Global learning-model correction

The repository training model now uses:

> 汲取 → 拆解 → 填充 → 重塑 → 化用 → 生发

## Active training route

`DEV-GROUP-002` is configured as 25 serial question units. Each unit requires five clean cold-start attempts, TOP1 at least 80%, TOP2 at least 90%, complete provenance/pairwise replay, and retention of previously mastered units.

Below-target performance continues the learning cycle. It no longer triggers an arbitrary round-count HOLD.

## Corrected capabilities

- general method and mechanism changes are allowed;
- base-knowledge candidates are allowed after two independent source parents and two-unit reproduction;
- case/question/option-specific direction rules remain prohibited;
- training mastery, cold-start stability and unseen blind generalization are separate claims;
- full formal release remains fail-closed.

## Validation

Local static and synthetic validation passed:

- five new unit tests passed;
- synthetic diagnosis replay passed;
- synthetic mastery-regression replay passed.

GitHub Actions is still failing before any job step executes. Remote CI remains unverified and no CI PASS is claimed.

The next legitimate operation is to begin `DEV-EXAMPLE-001-Q1` under the new serial learning cycle, not to continue the old R19 technical-closure route.
