"""Fila de RAM do controlador.

Um trabalho pesado por vez. Espera RAM livre >= 1,5 GB e nenhum processo
pesado externo rodando (suite de teste, DEM-Engine, graphify), executa o
proximo job da fila e so entao libera para o proximo.

Uso:  python fila_ram.py
Logs em: omniroute/fila_ram.log
"""
from __future__ import annotations

import io
import os
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

LOG = Path(__file__).with_name("fila_ram.log")
RAM_MIN_GB = 1.5
POLL_S = 30
MAX_WAIT_S = 60 * 60 * 4  # 4 h de espera maxima por job

# (nome, cwd, comando)
JOBS = [
    ("update Claude", r"C:\Users\yuri\OneDrive\Desktop\Claude",
     ["graphify", "update", ".", "--force"]),
]

# nomes de processo que contam como "trabalho pesado externo"
# (node NAO entra: o VS Code ja roda node e travaria a fila para sempre)
PESADOS = ("pytest", "DEM-Engine", "yade", "xmpi", "mpirun", "electron.exe")


def log(msg: str) -> None:
    linha = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(linha, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(linha + "\n")


def ram_livre_gb() -> float:
    try:
        import psutil
        return psutil.virtual_memory().available / 1e9
    except Exception:
        return 0.0


def Foreign_pesado() -> list[str]:
    """Processos pesados que NAO sejam o proprio graphify label."""
    achados = []
    try:
        import psutil
    except Exception:
        return achados
    for p in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            nome = (p.info["name"] or "").lower()
            cmd = " ".join(p.info["cmdline"] or []).lower()
            if "fila_ram.py" in cmd:
                continue
            if "graphify" in cmd and "label" in cmd:
                continue  # nosso proprio job
            for chave in PESADOS:
                if chave in nome or (chave in cmd and "graphify" not in cmd):
                    achados.append(f"{p.info['pid']}:{p.info['name']}")
                    break
        except Exception:
            continue
    return achados


def main() -> int:
    log("=== fila de RAM iniciada ===")
    for nome, cwd, cmd in JOBS:
        espera = 0
        while True:
            livre = ram_livre_gb()
            pesados = Foreign_pesado()
            if livre >= RAM_MIN_GB and not pesados:
                break
            if espera % 600 == 0:
                log(f"[{nome}] aguardando: RAM livre {livre:.2f} GB (min {RAM_MIN_GB}) | "
                    f"pesados={pesados or 'nenhum'} | espera {espera // 60} min")
            espera += POLL_S
            if espera > MAX_WAIT_S:
                log(f"[{nome}] TIMEOUT de espera ({MAX_WAIT_S // 60} min). Pulando.")
                break
            time.sleep(POLL_S)
        else:
            continue

        log(f"[{nome}] JANELA ABERTA (RAM {ram_livre_gb():.2f} GB). Executando.")
        t0 = time.time()
        try:
            proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                                  timeout=60 * 60 * 3, encoding="utf-8", errors="replace")
            log(f"[{nome}] exit={proc.returncode} em {time.time() - t0:.0f}s")
            if proc.stdout:
                for linha in proc.stdout.strip().splitlines()[-25:]:
                    log(f"[{nome}] | {linha}")
            if proc.stderr:
                for linha in proc.stderr.strip().splitlines()[-15:]:
                    log(f"[{nome}] ! {linha}")
        except subprocess.TimeoutExpired:
            log(f"[{nome}] TIMEOUT na execucao (3 h).")
        except Exception as exc:  # noqa: BLE001
            log(f"[{nome}] ERRO: {type(exc).__name__}: {exc}")
        time.sleep(60)  # janela de respiro entre jobs

    log("=== fila de RAM concluida ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
