param(
    [string]$ReceiptPath = "dist/platform-acceptance/windows-two-version-update-calibration.json"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$Schema = "FORTUNE-CHART-WINDOWS-TWO-VERSION-CALIBRATION-R1"
$OldVersion = "0.2.4"
$OldSourceCommit = "7c20668b4ad301fc549beb4cd183d3ae69efbae7"
$OldZipSha256 = "d26321a0aa0956e6056852548a9cad5a0721432fc5270d1dfe65c3f1a47fc6df"
$OldZipSize = 55171934
$NewVersion = "0.2.5"
$NewSourceCommit = "2b6b836879700a2ff8f20d75c7d7af76dc867b1a"
$NewZipSha256 = "be3a2ec32c16d5ef8774287048483b75b6f3bab68699e8f39c77bd4aa31f8d0e"
$NewZipSize = 55521226
$NewManifestSha256 = "ce05f47623291ab2d07fb94750fd79e5884aa8718d5dfd1e13666ffb627ab7ce"

function Assert-True([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

function Download-File([string]$Uri, [string]$Destination) {
    Invoke-WebRequest -Uri $Uri -OutFile $Destination -UseBasicParsing
    Assert-True (Test-Path -LiteralPath $Destination) "download missing: $Uri"
}

function Read-BuildMetadata([string]$InstallRoot) {
    $path = Join-Path $InstallRoot "_internal/runtime/desktop-build-metadata.json"
    Assert-True (Test-Path -LiteralPath $path) "build metadata missing: $path"
    return Get-Content -LiteralPath $path -Raw | ConvertFrom-Json
}

function Wait-ForExit([System.Diagnostics.Process]$Process, [int]$TimeoutSeconds) {
    $deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    while (-not $Process.HasExited -and [DateTime]::UtcNow -lt $deadline) {
        Start-Sleep -Milliseconds 500
        $Process.Refresh()
    }
    return $Process.HasExited
}

function Stop-FortuneChartProcesses {
    Get-Process -Name "FortuneChart" -ErrorAction SilentlyContinue |
        Stop-Process -Force -ErrorAction SilentlyContinue
}

$root = Join-Path $env:RUNNER_TEMP "fortune-chart-two-version-calibration"
if (Test-Path -LiteralPath $root) {
    Remove-Item -LiteralPath $root -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $root | Out-Null

$downloads = Join-Path $root "downloads"
New-Item -ItemType Directory -Force -Path $downloads | Out-Null

$oldManifestPath = Join-Path $downloads "fortune-chart-update-0.2.4.json"
$newManifestPath = Join-Path $downloads "fortune-chart-update-0.2.5.json"
$stableManifestPath = Join-Path $downloads "fortune-chart-update-stable.json"
$oldZipPath = Join-Path $downloads "FortuneChart-0.2.4.zip"
$newZipPath = Join-Path $downloads "FortuneChart-0.2.5.zip"

Download-File "https://github.com/chinaneedM/ziwei-bazi-model/releases/download/fortune-chart-v0.2.4/fortune-chart-update.json" $oldManifestPath
Download-File "https://github.com/chinaneedM/ziwei-bazi-model/releases/download/fortune-chart-v0.2.5/fortune-chart-update.json" $newManifestPath
Download-File "https://github.com/chinaneedM/ziwei-bazi-model/releases/download/fortune-chart-stable/fortune-chart-update.json" $stableManifestPath

$oldManifest = Get-Content -LiteralPath $oldManifestPath -Raw | ConvertFrom-Json
$newManifest = Get-Content -LiteralPath $newManifestPath -Raw | ConvertFrom-Json
$stableManifest = Get-Content -LiteralPath $stableManifestPath -Raw | ConvertFrom-Json

$stableManifestHash = (Get-FileHash -LiteralPath $stableManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
$newManifestHash = (Get-FileHash -LiteralPath $newManifestPath -Algorithm SHA256).Hash.ToLowerInvariant()
Assert-True ($stableManifestHash -eq $NewManifestSha256) "stable manifest SHA-256 mismatch"
Assert-True ($newManifestHash -eq $NewManifestSha256) "immutable 0.2.5 manifest SHA-256 mismatch"
Assert-True ($stableManifestHash -eq $newManifestHash) "stable pointer is not byte-identical to immutable 0.2.5 manifest"

Assert-True ($oldManifest.version -eq $OldVersion) "old manifest version mismatch"
Assert-True ($oldManifest.source_commit -eq $OldSourceCommit) "old manifest source commit mismatch"
Assert-True ($oldManifest.asset_sha256 -eq $OldZipSha256) "old manifest ZIP hash mismatch"
Assert-True ([int64]$oldManifest.asset_size -eq $OldZipSize) "old manifest ZIP size mismatch"

Assert-True ($newManifest.version -eq $NewVersion) "new manifest version mismatch"
Assert-True ($newManifest.source_commit -eq $NewSourceCommit) "new manifest source commit mismatch"
Assert-True ($newManifest.asset_sha256 -eq $NewZipSha256) "new manifest ZIP hash mismatch"
Assert-True ([int64]$newManifest.asset_size -eq $NewZipSize) "new manifest ZIP size mismatch"
Assert-True ($stableManifest.version -eq $NewVersion) "stable version mismatch"
Assert-True ($stableManifest.source_commit -eq $NewSourceCommit) "stable source commit mismatch"
Assert-True ($stableManifest.asset_url -eq $newManifest.asset_url) "stable asset URL mismatch"

Download-File $oldManifest.asset_url $oldZipPath
Download-File $stableManifest.asset_url $newZipPath

$oldZipHash = (Get-FileHash -LiteralPath $oldZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
$newZipHash = (Get-FileHash -LiteralPath $newZipPath -Algorithm SHA256).Hash.ToLowerInvariant()
$oldZipActualSize = (Get-Item -LiteralPath $oldZipPath).Length
$newZipActualSize = (Get-Item -LiteralPath $newZipPath).Length
Assert-True ($oldZipHash -eq $OldZipSha256) "downloaded 0.2.4 ZIP SHA-256 mismatch"
Assert-True ($newZipHash -eq $NewZipSha256) "downloaded 0.2.5 ZIP SHA-256 mismatch"
Assert-True ($oldZipActualSize -eq $OldZipSize) "downloaded 0.2.4 ZIP size mismatch"
Assert-True ($newZipActualSize -eq $NewZipSize) "downloaded 0.2.5 ZIP size mismatch"

$successParent = Join-Path $root "success"
New-Item -ItemType Directory -Force -Path $successParent | Out-Null
Expand-Archive -LiteralPath $oldZipPath -DestinationPath $successParent -Force
$successInstall = Join-Path $successParent "FortuneChart"
$oldMeta = Read-BuildMetadata $successInstall
Assert-True ($oldMeta.application_version -eq $OldVersion) "success fixture old version mismatch"
Assert-True ($oldMeta.source_commit -eq $OldSourceCommit) "success fixture old source mismatch"

$successOldExe = Join-Path $successInstall "FortuneChart.exe"
$successOldUpdater = Join-Path $successInstall "FortuneChartUpdater.exe"
$oldExeHash = (Get-FileHash -LiteralPath $successOldExe -Algorithm SHA256).Hash.ToLowerInvariant()
$oldUpdaterHash = (Get-FileHash -LiteralPath $successOldUpdater -Algorithm SHA256).Hash.ToLowerInvariant()
$successSentinel = Join-Path $successInstall "OLD_VERSION_SENTINEL.txt"
Set-Content -LiteralPath $successSentinel -Value "0.2.4 sentinel" -Encoding ascii

$launcher = Start-Process -FilePath $successOldExe -ArgumentList @("--no-browser") -PassThru
$launcherExited = Wait-ForExit $launcher 150
if (-not $launcherExited) {
    Stop-Process -Id $launcher.Id -Force -ErrorAction SilentlyContinue
    throw "released 0.2.4 launcher did not hand control to updater within timeout"
}
Assert-True ($launcher.ExitCode -eq 0) "released 0.2.4 launcher exited non-zero during startup update"

$activationDeadline = [DateTime]::UtcNow.AddSeconds(150)
$activationMetadata = $null
while ([DateTime]::UtcNow -lt $activationDeadline) {
    try {
        if (Test-Path -LiteralPath $successInstall) {
            $candidate = Read-BuildMetadata $successInstall
            if ($candidate.application_version -eq $NewVersion -and $candidate.source_commit -eq $NewSourceCommit) {
                $activationMetadata = $candidate
                break
            }
        }
    }
    catch {
    }
    Start-Sleep -Milliseconds 500
}
Assert-True ($null -ne $activationMetadata) "0.2.4 -> 0.2.5 activation was not observed"
Assert-True (-not (Test-Path -LiteralPath $successSentinel)) "old-tree sentinel survived complete-tree activation"

$newExeHashAfterActivation = (Get-FileHash -LiteralPath (Join-Path $successInstall "FortuneChart.exe") -Algorithm SHA256).Hash.ToLowerInvariant()
$newUpdaterHashAfterActivation = (Get-FileHash -LiteralPath (Join-Path $successInstall "FortuneChartUpdater.exe") -Algorithm SHA256).Hash.ToLowerInvariant()
Assert-True ($newExeHashAfterActivation -ne $oldExeHash) "active application executable did not change"
Assert-True ($newUpdaterHashAfterActivation -ne $oldUpdaterHash) "active updater executable did not change"

$activationRelaunchObserved = @(Get-Process -Name "FortuneChart" -ErrorAction SilentlyContinue).Count -gt 0
Assert-True $activationRelaunchObserved "post-update FortuneChart relaunch was not observed"
Stop-FortuneChartProcesses

$failureParent = Join-Path $root "failure"
New-Item -ItemType Directory -Force -Path $failureParent | Out-Null
Expand-Archive -LiteralPath $oldZipPath -DestinationPath $failureParent -Force
$failureInstall = Join-Path $failureParent "FortuneChart"
$failureOldMeta = Read-BuildMetadata $failureInstall
Assert-True ($failureOldMeta.application_version -eq $OldVersion) "failure fixture old version mismatch"
Assert-True ($failureOldMeta.source_commit -eq $OldSourceCommit) "failure fixture old source mismatch"

$failureOldExe = Join-Path $failureInstall "FortuneChart.exe"
$failureOldExeHash = (Get-FileHash -LiteralPath $failureOldExe -Algorithm SHA256).Hash.ToLowerInvariant()
$failureSentinel = Join-Path $failureInstall "OLD_VERSION_SENTINEL.txt"
Set-Content -LiteralPath $failureSentinel -Value "0.2.4 rollback sentinel" -Encoding ascii

$failureStaging = Join-Path $failureParent ".FortuneChart.update-calibration-failure"
New-Item -ItemType Directory -Force -Path $failureStaging | Out-Null
Expand-Archive -LiteralPath $newZipPath -DestinationPath $failureStaging -Force
$failureStagedBundle = Join-Path $failureStaging "FortuneChart"
$failureStagedMeta = Read-BuildMetadata $failureStagedBundle
Assert-True ($failureStagedMeta.application_version -eq $NewVersion) "failure staged version mismatch"
Assert-True ($failureStagedMeta.source_commit -eq $NewSourceCommit) "failure staged source mismatch"

$corruptExe = Join-Path $failureStagedBundle "FortuneChart.exe"
[System.IO.File]::WriteAllText($corruptExe, "intentionally corrupted executable for rollback calibration")

$tempUpdaterRoot = Join-Path $root "failure-standalone-updater"
New-Item -ItemType Directory -Force -Path $tempUpdaterRoot | Out-Null
$tempUpdater = Join-Path $tempUpdaterRoot "FortuneChartUpdater.exe"
Copy-Item -LiteralPath (Join-Path $failureInstall "FortuneChartUpdater.exe") -Destination $tempUpdater -Force

$pwsh = Join-Path $PSHOME "pwsh.exe"
$dummyParent = Start-Process -FilePath $pwsh -ArgumentList @("-NoLogo", "-NoProfile", "-Command", "Start-Sleep -Seconds 2") -PassThru -WindowStyle Hidden

$failureArgs = @(
    "--parent-pid", [string]$dummyParent.Id,
    "--install-root", $failureInstall,
    "--staging-root", $failureStaging,
    "--staged-bundle", $failureStagedBundle,
    "--expected-version", $NewVersion,
    "--expected-source-commit", $NewSourceCommit
)
$failureUpdater = Start-Process -FilePath $tempUpdater -ArgumentList $failureArgs -PassThru

$rotationObserved = $false
$rotationDeadline = [DateTime]::UtcNow.AddSeconds(90)
while ([DateTime]::UtcNow -lt $rotationDeadline) {
    if (-not (Test-Path -LiteralPath $failureSentinel)) {
        $rotationObserved = $true
        break
    }
    Start-Sleep -Milliseconds 250
}
Assert-True $rotationObserved "controlled failure never rotated away from the old tree"

$rollbackObserved = $false
$rollbackDeadline = [DateTime]::UtcNow.AddSeconds(90)
while ([DateTime]::UtcNow -lt $rollbackDeadline) {
    try {
        if (Test-Path -LiteralPath $failureSentinel) {
            $candidate = Read-BuildMetadata $failureInstall
            $candidateExeHash = (Get-FileHash -LiteralPath (Join-Path $failureInstall "FortuneChart.exe") -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($candidate.application_version -eq $OldVersion -and $candidate.source_commit -eq $OldSourceCommit -and $candidateExeHash -eq $failureOldExeHash) {
                $rollbackObserved = $true
                break
            }
        }
    }
    catch {
    }
    Start-Sleep -Milliseconds 250
}
Assert-True $rollbackObserved "controlled activation failure did not restore the complete 0.2.4 tree"

$rollbackRelaunchDeadline = [DateTime]::UtcNow.AddSeconds(30)
$rollbackRelaunchObserved = $false
while ([DateTime]::UtcNow -lt $rollbackRelaunchDeadline) {
    if (@(Get-Process -Name "FortuneChart" -ErrorAction SilentlyContinue).Count -gt 0) {
        $rollbackRelaunchObserved = $true
        break
    }
    Start-Sleep -Milliseconds 250
}
Assert-True $rollbackRelaunchObserved "known-good 0.2.4 relaunch was not observed after rollback"

Start-Sleep -Seconds 1
$stagingRemovedAfterRollback = -not (Test-Path -LiteralPath $failureStaging)
Assert-True $stagingRemovedAfterRollback "failed staging tree was not removed after rollback"

$failureUpdater.Refresh()
$failureUpdaterExited = $failureUpdater.HasExited
$failureUpdaterExitCode = $null
if ($failureUpdaterExited) {
    $failureUpdaterExitCode = $failureUpdater.ExitCode
    Assert-True ($failureUpdaterExitCode -eq 1) "controlled-failure updater exited with unexpected code"
} else {
    Stop-Process -Id $failureUpdater.Id -Force -ErrorAction SilentlyContinue
}
Stop-FortuneChartProcesses

$receipt = [ordered]@{
    schema = $Schema
    status = "PASS"
    runner = "windows-latest"
    stable_manifest_sha256 = $stableManifestHash
    stable_manifest_matches_immutable_0_2_5 = $true
    old_version = $OldVersion
    old_source_commit = $OldSourceCommit
    old_zip_sha256 = $oldZipHash
    old_zip_size = $oldZipActualSize
    new_version = $NewVersion
    new_source_commit = $NewSourceCommit
    new_zip_sha256 = $newZipHash
    new_zip_size = $newZipActualSize
    activation_path = "RELEASED_0_2_4_LAUNCHER_STARTUP_UPDATE"
    activation_launcher_exit_code = $launcher.ExitCode
    activation_complete_tree_replacement = $true
    activation_old_sentinel_removed = $true
    activation_new_metadata_verified = $true
    activation_relaunch_observed = $activationRelaunchObserved
    rollback_path = "RELEASED_0_2_4_UPDATER_CORRUPTED_0_2_5_EXECUTABLE"
    rollback_rotation_observed = $rotationObserved
    rollback_complete_old_tree_restored = $rollbackObserved
    rollback_failed_staging_removed = $stagingRemovedAfterRollback
    rollback_known_good_relaunch_observed = $rollbackRelaunchObserved
    rollback_updater_exited_before_cleanup = $failureUpdaterExited
    rollback_updater_exit_code = $failureUpdaterExitCode
}

$receiptFile = [System.IO.Path]::GetFullPath($ReceiptPath)
$receiptDir = Split-Path -Parent $receiptFile
New-Item -ItemType Directory -Force -Path $receiptDir | Out-Null
$receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $receiptFile -Encoding utf8

Write-Host ($receipt | ConvertTo-Json -Compress -Depth 6)
