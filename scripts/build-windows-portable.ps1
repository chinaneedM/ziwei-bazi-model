param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-fA-F]{40}$')]
    [string]$SourceCommit,
    [string]$OutputRoot = 'dist',
    [string]$ReleaseTag = ''
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$BuildRoot = Join-Path $RepoRoot 'build\windows-portable-r2'
$AppDistRoot = Join-Path $BuildRoot 'app-dist'
$AppWorkRoot = Join-Path $BuildRoot 'app-work'
$AppSpecRoot = Join-Path $BuildRoot 'app-spec'
$UpdaterDistRoot = Join-Path $BuildRoot 'updater-dist'
$UpdaterWorkRoot = Join-Path $BuildRoot 'updater-work'
$UpdaterSpecRoot = Join-Path $BuildRoot 'updater-spec'
$MetadataRoot = Join-Path $BuildRoot 'metadata'
$MetadataPath = Join-Path $MetadataRoot 'desktop-build-metadata.json'
$DistributionManifestPath = Join-Path $MetadataRoot 'desktop-distribution-manifest.json'

Push-Location $RepoRoot
try {
    if (Test-Path $BuildRoot) {
        Remove-Item -Recurse -Force $BuildRoot
    }
    New-Item -ItemType Directory -Force -Path `
        $AppDistRoot, $AppWorkRoot, $AppSpecRoot, `
        $UpdaterDistRoot, $UpdaterWorkRoot, $UpdaterSpecRoot, $MetadataRoot | Out-Null

    $Version = (python -c "from fortune_training.desktop_application.distribution import DESKTOP_APPLICATION_VERSION; print(DESKTOP_APPLICATION_VERSION)").Trim()
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Version)) {
        throw 'unable to resolve desktop application version'
    }
    if ([string]::IsNullOrWhiteSpace($ReleaseTag)) {
        $ReleaseTag = "fortune-chart-v$Version"
    }
    if ($ReleaseTag -ne "fortune-chart-v$Version") {
        throw "release tag/version mismatch: tag=$ReleaseTag version=$Version"
    }

    python -m fortune_training.desktop_application.distribution `
        --source-commit $SourceCommit `
        --metadata-out $MetadataPath `
        --manifest-out $DistributionManifestPath
    if ($LASTEXITCODE -ne 0) { throw 'desktop metadata generation failed' }

    $ConfigPath = Join-Path $RepoRoot 'config\time-calendar-policies.json'
    $EntryPath = Join-Path $RepoRoot 'scripts\fortune_chart_desktop.py'
    $UpdaterEntryPath = Join-Path $RepoRoot 'scripts\fortune_chart_updater.py'

    python -m PyInstaller `
        --noconfirm `
        --clean `
        --onefile `
        --windowed `
        --name FortuneChartUpdater `
        --distpath $UpdaterDistRoot `
        --workpath $UpdaterWorkRoot `
        --specpath $UpdaterSpecRoot `
        $UpdaterEntryPath
    if ($LASTEXITCODE -ne 0) { throw 'standalone updater PyInstaller build failed' }

    python -m PyInstaller `
        --noconfirm `
        --clean `
        --onedir `
        --windowed `
        --name FortuneChart `
        --contents-directory _internal `
        --add-data "$ConfigPath;runtime\config" `
        --add-data "$MetadataPath;runtime" `
        --add-data "$DistributionManifestPath;runtime" `
        --collect-data geonamescache `
        --collect-data tzdata `
        --hidden-import tzdata `
        --distpath $AppDistRoot `
        --workpath $AppWorkRoot `
        --specpath $AppSpecRoot `
        $EntryPath
    if ($LASTEXITCODE -ne 0) { throw 'FortuneChart PyInstaller build failed' }

    $BundleRoot = Join-Path $AppDistRoot 'FortuneChart'
    $ExePath = Join-Path $BundleRoot 'FortuneChart.exe'
    $UpdaterExePath = Join-Path $UpdaterDistRoot 'FortuneChartUpdater.exe'
    $RuntimeRoot = Join-Path $BundleRoot '_internal\runtime'
    if (-not (Test-Path $ExePath)) { throw "missing packaged launcher: $ExePath" }
    if (-not (Test-Path $UpdaterExePath)) { throw "missing standalone updater: $UpdaterExePath" }

    Copy-Item -Force $UpdaterExePath (Join-Path $BundleRoot 'FortuneChartUpdater.exe')

    if (-not (Test-Path (Join-Path $RuntimeRoot 'config\time-calendar-policies.json'))) {
        throw 'packaged runtime config missing'
    }
    if (-not (Test-Path (Join-Path $RuntimeRoot 'desktop-build-metadata.json'))) {
        throw 'packaged build metadata missing'
    }
    if (-not (Test-Path (Join-Path $RuntimeRoot 'desktop-distribution-manifest.json'))) {
        throw 'packaged distribution manifest missing'
    }

    $ForbiddenRuntimePaths = @(
        'training',
        'answers',
        'answer-vault',
        'answer_vault',
        'model-learning',
        'sources'
    )
    foreach ($Relative in $ForbiddenRuntimePaths) {
        if (Test-Path (Join-Path $RuntimeRoot $Relative)) {
            throw "forbidden repository data bundled into desktop runtime: $Relative"
        }
    }

    $OutputDir = Join-Path $RepoRoot $OutputRoot
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    $ZipPath = Join-Path $OutputDir 'FortuneChart-windows-x64.zip'
    $UpdateManifestPath = Join-Path $OutputDir 'fortune-chart-update.json'
    if (Test-Path $ZipPath) { Remove-Item -Force $ZipPath }
    if (Test-Path $UpdateManifestPath) { Remove-Item -Force $UpdateManifestPath }
    Compress-Archive -Path $BundleRoot -DestinationPath $ZipPath -CompressionLevel Optimal

    python -m fortune_training.desktop_application.updates `
        --source-commit $SourceCommit `
        --asset-path $ZipPath `
        --release-tag $ReleaseTag `
        --manifest-out $UpdateManifestPath
    if ($LASTEXITCODE -ne 0) { throw 'update manifest generation failed' }

    if (-not (Test-Path $UpdateManifestPath)) { throw 'release update manifest missing' }

    Write-Host "Portable desktop bundle: $ZipPath"
    Write-Host "Update manifest: $UpdateManifestPath"
    Write-Host "Application version: $Version"
    Write-Host "Source commit: $($SourceCommit.ToLowerInvariant())"
}
finally {
    Pop-Location
}
