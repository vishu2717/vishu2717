param(
    [string]$Owner = 'vishu2717'
)

$headers = @{ 'User-Agent' = 'readme-updater' }
if ($env:GH_TOKEN) { $headers['Authorization'] = "token $env:GH_TOKEN" }

$repos = Invoke-RestMethod "https://api.github.com/users/$Owner/repos?per_page=100&type=owner" -Headers $headers

$lines = @()
foreach ($r in $repos) {
    if ($r.private -or $r.fork -or $r.name -eq $Owner) { continue }
    $name = $r.name
    $desc = if ($r.description) { $r.description } else { 'No description provided' }
    $lang = if ($r.language) { $r.language } else { 'N/A' }
    $lines += "- [![Issues](https://img.shields.io/github/issues/$Owner/$name`?style=flat-square&color=blue)](https://github.com/$Owner/$name/issues) [**$name**]($($r.html_url)) - $desc ``$lang``"
}

$lines = $lines | Sort-Object
$target = '## Featured Projects'
$readmePath = Join-Path $PSScriptRoot '..\..\README.md'
$content = Get-Content $readmePath -Raw

$start = '<!-- PROJECTS:START -->'
$end = '<!-- PROJECTS:END -->'
$body = ($lines -join "`r`n`r`n")

if ($content -match [regex]::Escape($start) -and $content -match [regex]::Escape($end)) {
    $pattern = '(?s)' + [regex]::Escape($start) + '.*?' + [regex]::Escape($end)
    $content = [regex]::Replace($content, $pattern, "$start`r`n`r`n$body`r`n`r`n$end", 1)
} else {
    throw "Could not find PROJECTS markers in README.md"
}

Set-Content -Path $readmePath -Value $content -NoNewline -Encoding utf8
Write-Output "Refreshed $($lines.Count) projects in README.md"