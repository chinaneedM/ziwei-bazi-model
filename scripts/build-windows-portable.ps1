param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-fA-F]{40}$')]
    [string]$SourceCommit,
    [string]$OutputRoot = 'dist'
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$BuildRoot = Join-Path $RepoRoot 'build\windows-portable-r1'
$DistRoot = Join-Path $BuildRoot 'dist'
$WorkRoot = Join-Path $BuildRoot 'work'
$SpecRoot = Join-Path $BuildRoot 'spec'
$MetadataRoot = Join-Path $BuildRoot 'metadata'
$MetadataPath = Join-Path $MetadataRoot 'desktop-build-metadata.json'
$ManifestPath = Join-Path $MetadataRoot 'desktop-distribution-manifest.json'

Push-Location $RepoRoot
try {
    if (Test-Path $BuildRoot) {
        Remove-Item -Recurse -Force $BuildRoot
    }
    New-Item -ItemType Directory -Force -Path $DistRoot, $WorkRoot, $SpecRoot, $MetadataRoot | Out-Null

    python -m fortune_training.desktop_application.distribution `
        --source-commit $SourceCommit `
        --metadata-out $MetadataPath `
        --manifest-out $ManifestPath
    if ($LASTEXITCODE -ne 0) { throw 'desktop metadata generation failed' }

    $ConfigPath = Join-Path $RepoRoot 'config\time-calendar-policies.json'
    $EntryPath = Join-Path $RepoRoot 'scripts\fortune_chart_desktop.py'

    python -m PyInstaller `
        --noconfirm `
        --clean `
        --onedir `
        --windowed `
        --name FortuneChart `
        --contents-directory _internal `
        --add-data "$ConfigPath;runtime\config" `
        --add-data "$MetadataPath;runtime" `
        --add-data "$ManifestPath;runtime" `
        --collect-data geonamescache `
        --collect-data tzdata `
        --hidden-import tzdata `
        --distpath $DistRoot `
        --workpath $WorkRoot `
        --specpath $SpecRoot `
        $EntryPath
    if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed' }

    $BundleRoot = Join-Path $DistRoot 'FortuneChart'
    $ExePath = Join-Path $BundleRoot 'FortuneChart.exe'
    $RuntimeRoot = Join-Path $BundleRoot '_internal\runtime'
    if (-not (Test-Path $ExePath)) { throw "missing packaged launcher: $ExePath" }
    if (-not (Test-Path (Join-Path $RuntimeRoot 'config\time-calendar-policies.json'))) {
        throw 'packaged runtime config missing'
    }
    if (-not (Test-Path (Join-Path $RuntimeRoot 'desktop-build-metadata.json'))) {
        throw 'packaged build metadata missing'
    }
    if (-not (Test-Path (Join-Path $RuntimeRoot 'desktop-distribution-manifest.json'))) {
        throw 'packaged distribution manifest missing'
    }

    # Only the explicit runtime repository-data inventory may be copied. These
    # checks protect against future wildcard additions that accidentally bundle
    # development/training data.
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
    if (Test-Path $ZipPath) { Remove-Item -Force $ZipPath }
    Compress-Archive -Path $BundleRoot -DestinationPath $ZipPath -CompressionLevel Optimal

    Write-Host "Portable desktop bundle: $ZipPath"
    Write-Host "Source commit: $($SourceCommit.ToLowerInvariant())"
}
finally {
    Pop-Location
}
