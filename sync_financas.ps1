$src = "C:\Users\yuri\OneDrive\Desktop\Dev\Claude\Financas"
$dst = "C:\Users\yuri\OneDrive\Desktop\Financas"

if (Test-Path $src) {
    if (-not (Test-Path $dst)) {
        New-Item -ItemType Directory -Path $dst | Out-Null
    }
    Copy-Item -Path $src -Destination $dst -Recurse -Force
    Write-Host "[OK] Pasta 'Financas' sincronizada para $dst"
} else {
    Write-Host "[!] Pasta '$src' nao encontrada."
}