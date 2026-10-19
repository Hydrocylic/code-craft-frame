<#
check-sensitive.ps1 - scan a repo for secrets, PII, and absolute paths.

Usage:
  .\check-sensitive.ps1 [-Root <path>] [-History] [-Out <report.md>]

Prints category / file / line only; matched values are never printed.
High-confidence findings (secrets, PII) exit 1; absolute paths are review items.
#>

[CmdletBinding()]
param(
    [string]$Root = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot)),
    [switch]$History,
    [string]$Out
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $Root -PathType Container)) {
    throw "Root not found: $Root"
}
$Root = (Resolve-Path -LiteralPath $Root).Path

$patterns = [ordered]@{
    'secret-token'  = 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,}'
    'secret-key'    = '-----BEGIN [A-Z ]*PRIVATE KEY-----'
    'secret-url'    = 'https?://[^/\s:]+:[^/\s@]+@'
    'secret-assign' = '(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*["'']?[A-Za-z0-9_\-]{12,}'
    'pii-email'     = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    'pii-phone'     = '\b1[3-9]\d{9}\b'
    'pii-id'        = '\b\d{17}[\dXx]\b'
    'path-absolute' = '[A-Za-z]:\\[^\s"''<>|]+|\\\\[^\\\s]+\\[^\\\s]+'
}

$failCategories = @(
    'secret-token', 'secret-key', 'secret-url', 'secret-assign',
    'pii-email', 'pii-phone', 'pii-id'
)

$excludeDirs = @('\\.git\\', '\\node_modules\\', '\\bin\\', '\\obj\\', '\\.venv\\', '\\venv\\', '\\dist\\', '\\build\\')
$excludeFiles = @('check-sensitive.ps1', 'sensitive-data-check.md')

$files = Get-ChildItem -LiteralPath $Root -Recurse -File -Force | Where-Object {
    $rel = $_.FullName
    $skip = $false
    foreach ($dir in $excludeDirs) {
        if ($rel -match $dir) { $skip = $true; break }
    }
    (-not $skip) -and ($excludeFiles -notcontains $_.Name)
}

$findings = New-Object 'System.Collections.Generic.List[object]'

foreach ($file in $files) {
    if ($file.Length -gt 2MB) { continue }
    try {
        $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    } catch {
        continue
    }
    if ([Array]::IndexOf($bytes, [byte]0) -ge 0) { continue }

    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    foreach ($name in $patterns.Keys) {
        $regex = [regex]::new($patterns[$name])
        foreach ($match in $regex.Matches($text)) {
            $before = $text.Substring(0, $match.Index)
            $line = ([regex]::Matches($before, "`n")).Count + 1
            $findings.Add([pscustomobject]@{
                Category = $name
                File     = $file.FullName.Substring($Root.Length).TrimStart('\')
                Line     = $line
            })
        }
    }
}

$historyFindings = @()
$authors = @()
$remotes = @()

if ($History) {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if ($git) {
        $revs = & git -C $Root rev-list --all 2>$null
        if ($revs) {
            # Git grep uses POSIX ERE: no (?i), \s, \d, or \b.
            $historyPattern = 'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|glpat-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|https?://[^/[:space:]:]+:[^/[:space:]@]+@'
            $hist = & git -C $Root grep -l -I -E $historyPattern $revs 2>$null
            if ($hist) {
                $historyFindings = @($hist | ForEach-Object {
                    [pscustomobject]@{ Category = 'history-secret'; File = $_; Line = '' }
                })
            }
        }
        $authors = @(& git -C $Root log --all --format='%an <%ae>' 2>$null | Sort-Object -Unique)
        $remotes = @(& git -C $Root remote -v 2>$null)
    }
}

$all = New-Object 'System.Collections.Generic.List[object]'
foreach ($f in $findings) { $all.Add($f) }
foreach ($f in $historyFindings) { $all.Add($f) }

Write-Host "Root: $Root"
Write-Host "Scanned files: $($files.Count)"
if ($all.Count -eq 0) {
    Write-Host 'No sensitive patterns found in content.'
} else {
    $all | Format-Table -AutoSize | Out-String -Width 200 | Write-Host
}
if ($History) {
    if ($authors.Count -gt 0) {
        Write-Host 'Commit authors (review, not a failure):'
        $authors | ForEach-Object { Write-Host "  $_" }
    }
    if ($remotes.Count -gt 0) {
        Write-Host 'Remotes:'
        $remotes | ForEach-Object { Write-Host "  $_" }
    }
}

$fail = @($all | Where-Object { $_.Category -in $failCategories })
$review = @($all | Where-Object { $_.Category -eq 'path-absolute' })

if ($Out) {
    $outDir = Split-Path -Parent $Out
    if ($outDir -and -not (Test-Path -LiteralPath $outDir)) {
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }
    $report = New-Object 'System.Collections.Generic.List[string]'
    $report.Add('# Sensitive data check')
    $report.Add('')
    $report.Add("- Root: ``$Root``")
    $report.Add("- Date: $(Get-Date -Format s)")
    $report.Add("- Scanned files: $($files.Count)")
    $report.Add('')
    $report.Add('## Findings')
    $report.Add('')
    if ($all.Count -eq 0) {
        $report.Add('No sensitive patterns found in content.')
    } else {
        $report.Add('| Category | File | Line |')
        $report.Add('|---|---|---|')
        foreach ($f in $all) {
            $report.Add("| $($f.Category) | ``$($f.File)`` | $($f.Line) |")
        }
    }
    $report.Add('')
    $report.Add('## Review items')
    $report.Add('')
    $report.Add("- path-absolute: $($review.Count)")
    $report.Add("- commit authors: $($authors.Count)")
    $report.Add('')
    $report.Add('Values are intentionally not printed. Treat a clean run as a hint, not a guarantee.')
    Set-Content -LiteralPath $Out -Value $report -Encoding UTF8
    Write-Host "Report written: $Out"
}

if ($fail.Count -gt 0) {
    Write-Host "FAIL: $($fail.Count) high-confidence finding(s)."
    exit 1
}

Write-Host "PASS: no high-confidence findings. Review items: $($review.Count)."
exit 0
