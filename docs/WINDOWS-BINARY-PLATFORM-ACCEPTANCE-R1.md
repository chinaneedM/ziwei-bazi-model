# Windows Binary Platform Acceptance R1

## Status

```text
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
AUTOMATED_EMITTED_ZIP_BINARY_SMOKE=ACCEPTED
AUTOMATED_TWO_VERSION_UPDATE_CALIBRATION=ACCEPTED
MANUAL_WINDOWS_BROWSER_ACCEPTANCE=PENDING
```

This record is the platform-distribution acceptance boundary for the Windows portable build. It does not reopen the deterministic chart product, whose separate state remains `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## Automated evidence on the Windows runner

`.github/workflows/windows-portable.yml` must build the PyInstaller executables, create the final `FortuneChart-windows-x64.zip`, verify that ZIP against `fortune-chart-update.json`, extract that exact emitted archive into a fresh runner directory, and launch both executables from the extracted bundle.

`FortuneChart.exe --platform-smoke-receipt <path>` must prove packaged dependency loading, exact application/version/source metadata, ephemeral loopback binding, `/health`, the `FUSION-CHART-DESKTOP-PRODUCT-SHELL-R1` index marker, packaged product-shell CSS/JavaScript, and an ordinary deterministic `/api/resolve` whose combined integrity passes. `FortuneChartUpdater.exe --platform-smoke-receipt <path>` must prove that the standalone updater executable loads and exits without mutation. Both JSON receipts are uploaded with the build artifact.

This evidence is bound to the workflow's exact `SOURCE_COMMIT`, asset SHA-256, asset size, application version and combined manifest hash. A source-level test or a smoke against the pre-archive build directory is not a substitute.

## Two-version calibration now accepted

The released 0.2.4 → stable 0.2.5 activation and controlled rollback calibration is recorded in `docs/WINDOWS-PLATFORM-CALIBRATION-0.2.4-TO-0.2.5-20260904.md`. The Windows runner used the published immutable artifacts and live stable manifest, observed complete-tree activation to 0.2.5, then separately forced an activation-health failure on the exact release trees and verified complete restoration/relaunch of 0.2.4.

## Why acceptance remains pending

Automated binary, live-channel activation and rollback evidence is now accepted. The only remaining platform boundary is the visible/default-browser operator check on an actual user Windows desktop:

1. launch the released 0.2.5 ZIP on the target Windows edition/build and architecture with the default browser path enabled;
2. confirm the visible Product Shell loads and complete the real-machine interaction checklist in `docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md`;
3. confirm the post-update visible version/source identity and ordinary user interaction after the already-verified 0.2.4 → 0.2.5 activation path;
4. record Windows build, architecture, browser, observations and final operator disposition.

Signing, SmartScreen reputation and installer-specific behavior are not claimed by the current unsigned portable ZIP. If code signing or an installer becomes part of the release contract, it requires its own platform evidence.

## Promotion rule

Change `WINDOWS_BINARY_PLATFORM_ACCEPTANCE` to `ACCEPTED` only after one immutable evidence record satisfies every item above for the exact release artifact. Automated executable smoke by itself must not promote the status.
