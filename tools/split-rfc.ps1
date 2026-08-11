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

$lifecycleBridge = @'
### 2.2 Transport neutrality and lifecycle profiles

The single duration `T` is the conservative base mechanism, not necessarily the final shape of the service. The proposal applies to availability obligations over committed Ethereum data regardless of whether a future protocol exposes EIP-4844 blobs, granular Lean Data objects, payload-blobs, FullDAS cells, or another coded transport.

Research on Block-in-Blobs and integrated distributed history suggests a later generalization from one expiry to a lifecycle profile:

```text
L = (T_full, f_tail, T_tail)
```

where `T_full` is the full-strength serving window and an optional fraction `f_tail` remains under a reduced obligation for `T_tail`. Ordinary expiry remains the special case `L=(T,0,0)`. A permanent sparse-history tail is another possible profile; it is not equivalent to full retrievability forever.

The protocol still need not understand application semantics. It needs only the commitment, size, applicable access class, and lifecycle obligation. Some profiles may be purchaser-selected; protocol-mandated data such as canonical L1 history would inherit a protocol-defined profile.

[The Lean Ethereum compatibility note](10-how-does-lean-ethereum-change-the-proposal.md) develops this extension and its limits.
'@

$documents = @(
    @{
        Path = "docs/00-what-is-the-proposal.md"
        Title = "What is the proposal?"
        Body = $executive + "`n`n" +
            (Slice "## 1. Ingress and retention are distinct economic resources" "## 3. Minimum and maximum retention") +
            "`n`n" + $lifecycleBridge.Trim() + "`n`n" +
            (Slice "## 3. Minimum and maximum retention" "## 4. Flow and active retained stock")
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

    if ($document.Path -eq "docs/00-what-is-the-proposal.md") {
        $body = $body.Replace('DAService(B,T)', 'DAService(C,B,T)')
        $body = $body.Replace(
            'Letting a purchaser choose a bounded duration `T`, with `T_max` no longer than the current serving horizon, can only weakly reduce the logical retained-data obligation for a fixed admitted workload.',
            'Letting a purchaser choose a bounded duration `T`, with `T_max` no longer than the current minimum serving horizon, can only weakly reduce the logical retained-data obligation for a fixed admitted workload.'
        )
        $body = $body.Replace(
            'The existing fixed-retention service remains available as the special case `T=T_max`. Short-lived traffic can purchase less byte-time without changing its initial DA burden.',
            'The existing fixed-retention service remains available as the special case `T=T_max`. Here, `T_max` limits only the protocol serving obligation a purchaser may impose; it is not a mandatory deletion time or a prohibition on longer voluntary service. Short-lived traffic can purchase less byte-time without changing its initial DA burden.'
        )
        $body = $body.Replace(
            'This does not imply universal deletion. Applications, archives, storage providers, torrent-like swarms, EthStorage, Filecoin, or any interested third party may retain copies indefinitely. Expiration terminates the protocol requirement that the relevant custody participants continue retaining and serving enough of the data for reconstruction.',
            'This does not imply universal deletion. Custody participants, applications, archives, storage providers, torrent-like swarms, EthStorage, Filecoin, or any interested third party may retain and serve copies indefinitely. Expiration terminates only this lease''s protocol requirement that the relevant custody participants continue retaining and serving enough of the data for reconstruction. Continued service after expiry is permitted, but applications cannot rely on it without another guarantee.'
        )
        $body = $body.Replace(
            '## 3. Minimum and maximum retention',
            '## 3. Minimum and maximum guaranteed retention'
        )
        $body = $body.Replace(
            'A maximum horizon is important for a different reason. Every guaranteed lease is a promise about resource consumption through time. A conservative first implementation can set `T_max` no higher than the current PeerDAS serving horizon. It then never asks protocol participants to serve any individual object longer than the existing system already requires.',
            'A maximum guaranteed horizon is important for a different reason. Every guaranteed lease is a promise about resource consumption through time. A conservative first implementation can set `T_max` no higher than the current PeerDAS minimum serving horizon. It then never lets a purchaser impose a protocol serving obligation for any individual object beyond the duration already required by the existing system. `T_max` is not a pruning deadline: protocol participants may retain and serve the object longer, just as a minimum serving horizon does not require deletion when it ends. Such later service is best-effort unless backed by a separate guarantee.'
        )
        $body = $body.Replace(
            '**Conservative regime.** Ethereum leaves ingress limits unchanged and sets `T_max` no higher than the present serving horizon. The mechanism can reduce retained-data usage but cannot increase the logical worst case relative to fixed retention. In this regime the primary benefits are resource savings, price differentiation, and application flexibility.',
            '**Conservative regime.** Ethereum leaves ingress limits unchanged and sets `T_max` no higher than the present minimum serving horizon. The mechanism can reduce the guaranteed retained-data obligation but cannot increase its logical worst case relative to fixed retention. Nodes remain free to retain or serve expired objects voluntarily. In this regime the primary benefits are resource savings, price differentiation, and application flexibility.'
        )
        $body = $body.Replace(
            '> **Holding ingress and the maximum horizon fixed, variable retention weakly dominates fixed retention in logical retained-capacity consumption.**',
            '> **Holding ingress and the maximum guaranteed horizon fixed, variable retention weakly dominates fixed retention in logical retained-capacity consumption.**'
        )
    }

    if ($document.Path -eq "docs/02-is-variable-retention-safe-for-rollups.md") {
        $body = $body.Replace(
            'correlated applications may all seek maximum retention during the same crisis',
            'correlated applications may all seek the maximum guaranteed retention during the same crisis'
        )
    }

    if ($document.Path -eq "docs/03-how-do-future-resource-markets-work.md") {
        $body = $body.Replace('DAService(B,T,R)', 'DAService(C,B,T,R)')
    }

    if ($document.Path -eq "docs/09-what-is-the-conclusion.md") {
        $body = $body.Replace(
            'Under fixed ingress and `T_max` no greater than that horizon, variable retention weakly dominates fixed retention in **logical retained-capacity consumption**: the fixed service remains available as a special case, while shorter-lived objects consume less byte-time.',
            'Under fixed ingress and `T_max` no greater than that minimum serving horizon, variable retention weakly dominates fixed retention in **logical guaranteed retained-capacity consumption**: the fixed guaranteed service remains available as a special case, while shorter-lived objects consume less guaranteed byte-time. `T_max` limits the obligation a purchaser may impose; it neither requires pruning at expiry nor prevents voluntary service afterward.'
        )
    }

    Write-Utf8 $document.Path ("# " + $document.Title + "`n`n" + $body.Trim())
}

Write-Output "Generated $($documents.Count) base RFC documents from gist $GistId."
