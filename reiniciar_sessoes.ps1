# Reinicia so as sessoes do Claude Code abertas na pasta do omniroute, retomando cada conversa.
$pasta = "C:\Users\yuri\OneDrive\Desktop\omniroute"
$prompt = "ultrathink volte a fazer o que estava fazendo"

$alvos = @{}
foreach ($p in Get-CimInstance Win32_Process -Filter "Name='claude.exe'") {
    if ($p.CommandLine -notmatch '--resume=([0-9a-f-]+)') { continue }
    $id = $matches[1]
    $f = Get-ChildItem "$env:USERPROFILE\.claude\projects\*\$id.jsonl" -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $f) { continue }
    $cwd = (Select-String -Path $f.FullName -Pattern '"cwd":"([^"]+)"' | Select-Object -First 1).Matches[0].Groups[1].Value -replace '\\\\', '\'
    if ($cwd -ne $pasta) { continue }
    if (-not $alvos.ContainsKey($id)) { $alvos[$id] = @() }
    $alvos[$id] += $p.ProcessId
}

"Sessoes do omniroute: $($alvos.Count)"
$alvos.Keys | ForEach-Object { "  $_  (PIDs $($alvos[$_] -join ', '))" }

$alvos.Values | ForEach-Object { $_ } | ForEach-Object { Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }
Start-Sleep -Seconds 3

foreach ($id in $alvos.Keys) {
    $cmd = "claude --resume $id --remote-control --model 'combo/modelos gratuitos' --effort max --permission-mode dontAsk '$prompt'"
    Start-Process wt -ArgumentList @("-w", "0", "nt", "-d", $pasta, "powershell", "-NoExit", "-Command", $cmd)
}
