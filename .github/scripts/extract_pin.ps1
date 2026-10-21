$c = Get-Content 'C:\Users\ncibi\.gemini\antigravity-ide\brain\a7a8622d-0f29-42c5-b50a-c7820374f6f6\.system_generated\steps\447\content.md' -Raw

# og:image
$m = [regex]::Matches($c, 'og:image[^>]+content="([^"]+)"')
Write-Output "=== OG:IMAGE ==="
foreach ($x in $m) { Write-Output $x.Groups[1].Value }

# video URLs
$v = [regex]::Matches($c, '(https://v1\.pinimg\.com[^\s"]+)')
Write-Output "`n=== VIDEO ==="
foreach ($x in $v) { Write-Output $x.Value }

# GIF URLs
$g = [regex]::Matches($c, '(https://i\.pinimg\.com[^\s"]*\.gif)')
Write-Output "`n=== GIF ==="
foreach ($x in $g) { Write-Output $x.Value }

# originals
$o = [regex]::Matches($c, '(https://i\.pinimg\.com/originals/[^\s"]+)')
Write-Output "`n=== ORIGINALS ==="
foreach ($x in $o) { Write-Output $x.Value }
