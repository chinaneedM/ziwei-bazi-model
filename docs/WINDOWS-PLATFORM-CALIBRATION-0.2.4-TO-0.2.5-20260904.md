# Windows Platform Calibration 0.2.4 → 0.2.5

## Status

```text
AUTOMATED_TWO_VERSION_UPDATE_CALIBRATION=ACCEPTED
MANUAL_WINDOWS_BROWSER_ACCEPTANCE=PENDING
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
```

## Bound release identities

- Old released version: `0.2.4`
- Old source commit: `7c20668b4ad301fc549beb4cd183d3ae69efbae7`
- Old release ZIP SHA-256: `d26321a0aa0956e6056852548a9cad5a0721432fc5270d1dfe65c3f1a47fc6df`
- Old release ZIP size: `55171934` bytes
- New stable version: `0.2.5`
- New source commit: `2b6b836879700a2ff8f20d75c7d7af76dc867b1a`
- New release ZIP SHA-256: `be3a2ec32c16d5ef8774287048483b75b6f3bab68699e8f39c77bd4aa31f8d0e`
- New release ZIP size: `55521226` bytes
- Stable/immutable 0.2.5 manifest SHA-256: `ce05f47623291ab2d07fb94750fd79e5884aa8718d5dfd1e13666ffb627ab7ce`

## Publication evidence

`fortune-chart-v0.2.5` was published from exact accepted `main` commit `2b6b836879700a2ff8f20d75c7d7af76dc867b1a`. The mutable `fortune-chart-stable` release pointer was then updated with the byte-identical 0.2.5 update manifest. Stable promotion workflow run `33850578562` completed successfully.

## Two-version activation evidence

Calibration workflow run `33851789847` on `windows-latest` downloaded the already-published 0.2.4 and 0.2.5 immutable artifacts plus the live stable manifest.

The released 0.2.4 `FortuneChart.exe` was launched with its normal startup update path enabled. It consumed the live stable manifest, downloaded and staged 0.2.5, handed activation to its standalone updater, exited with code 0, replaced the complete portable tree, and relaunched the new build.

The emitted receipt recorded:

- `activation_path=RELEASED_0_2_4_LAUNCHER_STARTUP_UPDATE`
- `activation_complete_tree_replacement=true`
- `activation_old_sentinel_removed=true`
- `activation_new_metadata_verified=true`
- `activation_relaunch_observed=true`

The active tree after activation reported version `0.2.5` and source commit `2b6b836879700a2ff8f20d75c7d7af76dc867b1a`.

## Controlled rollback evidence

The same Windows calibration used exact released 0.2.4 and 0.2.5 trees with the current update transaction implementation and injected a deterministic activation-health failure after the new tree had been rotated into place. The transaction restored the complete known-good 0.2.4 tree, removed the failed activated bundle, cleaned the empty staging root, and a recovery relaunch of the restored 0.2.4 executable was observed.

The emitted receipt recorded:

- `rollback_rotation_observed=true`
- `rollback_complete_old_tree_restored=true`
- `rollback_failed_staged_bundle_removed=true`
- `rollback_empty_staging_root_cleaned=true`
- `rollback_known_good_relaunch_observed=true`

## Remaining boundary

This automated evidence closes the real two-version download, activation, complete-tree replacement, recovery rollback and relaunch gap. It does **not** replace the final visible/default-browser operator check on an actual user Windows desktop. Overall `WINDOWS_BINARY_PLATFORM_ACCEPTANCE` therefore remains `PENDING_PLATFORM_ACCEPTANCE` until the operator confirms the visible Product Shell, browser launch, primary chart interaction and post-update presentation on the target machine.

The temporary calibration PR was closed without merge; its workflow/script changes are evidence-only and are not part of the released product tree.
