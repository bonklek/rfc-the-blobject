param(
    [string]$GistId = "2eb406003118bd1e29476e54cc18a0c7"
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$rawUrl = gh api "gists/$GistId" --jq '.files[].raw_url' | Select-Object -First 1
$webClient = [System.Net.WebClient]::new()
try {
    $sourceBytes = $webClient.DownloadData($rawUrl.Trim())
}
finally {
    $webClient.Dispose()
}
$source = [System.Text.Encoding]::UTF8.GetString($sourceBytes)

if (-not $source.Contains("## 1. Ingress and retention are distinct economic resources")) {
    throw "The source gist does not contain the expected RFC headings."
}

function Slice {
    param(
        [string]$Start,
        [string]$End
    )

    $startIndex = $source.IndexOf($Start)
    if ($startIndex -lt 0) {
        throw "Missing start marker: $Start"
    }

    if ($End) {
        $endIndex = $source.IndexOf($End, $startIndex + $Start.Length)
        if ($endIndex -lt 0) {
            throw "Missing end marker: $End"
        }
    }
    else {
        $endIndex = $source.Length
    }

    return $source.Substring($startIndex, $endIndex - $startIndex).Trim()
}

function Write-Utf8 {
    param(
        [string]$RelativePath,
        [string]$Body
    )

    $Body = [regex]::Replace(
        $Body,
        '(?m)^(\*\*[^\r\n]+\*\*)  \r?$',
        { param($match) $match.Groups[1].Value + "`n" }
    )

    $path = Join-Path $repoRoot $RelativePath
    $directory = Split-Path -Parent $path
    [System.IO.Directory]::CreateDirectory($directory) | Out-Null
    [System.IO.File]::WriteAllText($path, ($Body.TrimEnd() + "`n"), [System.Text.UTF8Encoding]::new($false))
}

$executive = Slice "### Executive framing" "## 1. Ingress and retention are distinct economic resources"
$executive = $executive -replace '^### Executive framing', '## Executive framing'

$documents = @(
    @{
        Path = "docs/00-what-is-the-proposal.md"
        Title = "What is the proposal?"
        Body = $executive + "`n`n" + (Slice "## 1. Ingress and retention are distinct economic resources" "## 4. Flow and active retained stock")
    },
    @{
        Path = "docs/01-how-are-capacity-and-pricing-managed.md"
        Title = "How are capacity and pricing managed?"
        Body = Slice "## 4. Flow and active retained stock" "## 8. Security-critical applications and conditional graceful degradation"
    },
    @{
        Path = "docs/02-is-variable-retention-safe-for-rollups.md"
        Title = "Is variable retention safe for rollups?"
        Body = Slice "## 8. Security-critical applications and conditional graceful degradation" "# From a retention market to a market in network resources"
    },
    @{
        Path = "docs/03-how-do-future-resource-markets-work.md"
        Title = "How do future resource markets work?"
        Body = Slice "## 10. Future ingress and future-starting retention" "## 14. Retention-extension markets above Ethereum DA"
    },
    @{
        Path = "docs/04-what-happens-after-ethereum-retention-ends.md"
        Title = "What happens after Ethereum retention ends?"
        Body = Slice "## 14. Retention-extension markets above Ethereum DA" "## 17. FullDAS, distributed-storage leverage, and heterogeneous expiry"
    },
    @{
        Path = "docs/05-can-this-work-with-peerdas-and-fulldas.md"
        Title = "Can this work with PeerDAS and FullDAS?"
        Body = Slice "## 17. FullDAS, distributed-storage leverage, and heterogeneous expiry" "# Toward a generalized Ethereum data plane"
    },
    @{
        Path = "docs/06-what-does-a-generalized-data-plane-enable.md"
        Title = "What does a generalized Ethereum data plane enable?"
        Body = Slice "## 18. High-throughput ephemeral DA" "## 21. Prior art and adjacent mechanisms"
    },
    @{
        Path = "docs/07-what-is-the-prior-art-and-novelty.md"
        Title = "What is the prior art, and what is novel?"
        Body = Slice "## 21. Prior art and adjacent mechanisms" "## 22. Open questions and adversarial research agenda"
    },
    @{
        Path = "docs/08-what-remains-to-be-proven.md"
        Title = "What remains to be proven?"
        Body = Slice "## 22. Open questions and adversarial research agenda" "## 23. Conclusion"
    },
    @{
        Path = "docs/09-what-is-the-conclusion.md"
        Title = "What is the conclusion?"
        Body = Slice "## 23. Conclusion" "# Appendix A. Worked downstream construction: RetentionNotes"
    },
    @{
        Path = "appendices/retention-notes.md"
        Title = "Appendix: How could RetentionNotes work?"
        Body = Slice "# Appendix A. Worked downstream construction: RetentionNotes" ""
    }
)

foreach ($document in $documents) {
    $body = $document.Body
    $body = $body -replace '(?m)^# Appendix A\. Worked downstream construction: RetentionNotes\s*$', ''
    Write-Utf8 $document.Path ("# " + $document.Title + "`n`n" + $body.Trim())
}

Write-Output "Generated $($documents.Count) RFC documents from gist $GistId."
