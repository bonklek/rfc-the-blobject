param()

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot

$baseFiles = @(
    Get-ChildItem (Join-Path $repoRoot "docs") -File |
        Where-Object Name -Match '^0[0-9]-'
) + @(
    Get-ChildItem (Join-Path $repoRoot "appendices") -File
)
$baseText = ($baseFiles | ForEach-Object {
    Get-Content -Raw -Encoding UTF8 $_.FullName
}) -join "`n"

foreach ($section in 1..23) {
    $count = ([regex]::Matches($baseText, "(?m)^## $section\.")).Count
    if ($count -ne 1) {
        throw "Base section $section appears $count times; expected exactly once."
    }
}

$markdownFiles = Get-ChildItem $repoRoot -Recurse -File -Filter *.md
foreach ($file in $markdownFiles) {
    $text = Get-Content -Raw -Encoding UTF8 $file.FullName

    foreach ($match in [regex]::Matches(
        $text,
        '\[[^\]]+\]\((?!https?://|#|mailto:)([^)#]+)(?:#[^)]+)?\)'
    )) {
        $target = Join-Path $file.DirectoryName $match.Groups[1].Value
        if (-not (Test-Path -LiteralPath $target)) {
            throw "Broken local link in $($file.FullName): $($match.Groups[1].Value)"
        }
    }

    $fenceCount = (Select-String -Path $file.FullName -Pattern '^```' -Encoding UTF8).Count
    if ($fenceCount % 2 -ne 0) {
        throw "Unbalanced code fences in $($file.FullName)."
    }
}

$signatureMatches = rg -n 'DAService\(' (Join-Path $repoRoot "docs")
if ($LASTEXITCODE -ne 0) {
    throw "No DAService signatures found."
}
if ($signatureMatches -match 'DAService\(B') {
    throw "A DAService signature omits commitment C."
}

$strongClaimArgs = @(
    "-n",
    "-i",
    "consensus-secured availability|DAS guarantees reconstructability",
    (Join-Path $repoRoot "docs"),
    (Join-Path $repoRoot "README.md")
)
$strongClaims = & rg @strongClaimArgs
if ($LASTEXITCODE -eq 0) {
    throw "Found an unqualified strong availability claim:`n$strongClaims"
}
if ($LASTEXITCODE -gt 1) {
    throw "rg failed while checking availability claims."
}

Push-Location $repoRoot
try {
    python tools/check-docs.py
    if ($LASTEXITCODE -ne 0) {
        throw "Markdown path, heading, or inventory checks failed."
    }

    python -m unittest discover -s models -p "test_*.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Model tests failed."
    }

    python tools/check-generated.py
    if ($LASTEXITCODE -ne 0) {
        throw "Generated artifact comparison failed."
    }

    python -m unittest discover -s tools -p "test_*.py"
    if ($LASTEXITCODE -ne 0) {
        throw "Documentation-tool regression tests failed."
    }

    git diff --check
    if ($LASTEXITCODE -ne 0) {
        throw "git diff --check failed."
    }
}
finally {
    Pop-Location
}

Write-Output "Mechanical checks passed: base numbering, chapter inventory, local paths and headings, fences, two phrase guards, model tests, generated artifacts, and diff whitespace. External sources, semantics, and visual layout require separate review."
