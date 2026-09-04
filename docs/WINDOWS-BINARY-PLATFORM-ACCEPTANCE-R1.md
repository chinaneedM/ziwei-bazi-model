# Windows Binary Platform Acceptance R1

## Status

```text
WINDOWS_BINARY_PLATFORM_ACCEPTANCE=PENDING_PLATFORM_ACCEPTANCE
AUTOMATED_EMITTED_ZIP_BINARY_SMOKE=REQUIRED
MANUAL_WINDOWS_UPDATE_ACTIVATION_ACCEPTANCE=PENDING
```

This record is the platform-distribution acceptance boundary for the Windows portable build. It does not reopen the deterministic chart product, whose separate state remains `DETERMINISTIC_FUSION_CHART_PRODUCT_R1=CLOSED`.

## Automated evidence on the Windows runner

`.github/workflows/windows-portable.yml` must build the PyInstaller executables, create the final `FortuneChart-windows-x64.zip`, verify that ZIP against `fortune-chart-update.json`, extract that exact emitted archive into a fresh runner directory, and launch both executables from the extracted bundle.

`FortuneChart.exe --platform-smoke-receipt <path>` must prove packaged dependency loading, exact application/version/source metadata, ephemeral loopback binding, `/health`, the `FUSION-CHART-DESKTOP-PRODUCT-SHELL-R1` index marker, packaged product-shell CSS/JavaScript, and an ordinary deterministic `/api/resolve` whose combined integrity passes. `FortuneChartUpdater.exe --platform-smoke-receipt <path>` must prove that the standalone updater executable loads and exits without mutation. Both JSON receipts are uploaded with the build artifact.

This evidence is bound to the workflow's exact `SOURCE_COMMIT`, asset SHA-256, asset size, application version and combined manifest hash. A source-level test or a smoke against the pre-archive build directory is not a substitute.

## Why acceptance remains pending

The hosted-runner smoke closes several earlier evidence gaps, but it deliberately does not claim an end-user Windows release acceptance. The following still require a controlled two-version calibration and, for the visible interaction, a Windows operator:

1. launch the released ZIP on the target Windows edition/build and architecture with the default browser path enabled;
2. confirm the visible Workbench loads and complete the real-machine interaction checklist in `docs/COMBINED-WORKBENCH-REAL-MACHINE-CALIBRATION-R1.md`;
3. serve or publish a manifest-bound newer calibration build and allow the installed old build to launch the standalone updater;
4. verify parent-process exit, complete-tree replacement, relaunch, visible new version/source identity and absence of mixed old/new files;
5. induce one controlled activation failure and verify restoration/relaunch of the complete known-good tree;
6. record Windows build, architecture, old/new versions, both source commits, ZIP hashes/sizes, receipt artifacts, observations and final operator disposition.

Signing, SmartScreen reputation and installer-specific behavior are not claimed by the current unsigned portable ZIP. If code signing or an installer becomes part of the release contract, it requires its own platform evidence.

## Promotion rule

Change `WINDOWS_BINARY_PLATFORM_ACCEPTANCE` to `ACCEPTED` only after one immutable evidence record satisfies every item above for the exact release artifact. Automated executable smoke by itself must not promote the status.
