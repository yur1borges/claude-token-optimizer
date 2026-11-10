#!/usr/bin/env python3
"""PreCompact hook for Claude Code: tell compaction what to preserve and drop.

Prints PRESERVE/DROP guidance as plain text (custom compact instructions) so a compacted session
keeps decisions, current state and next step, instead of re-injecting full
memory afterwards. Also writes HANDOFF.md in the project folder (cwd) so a
fresh session can resume by reading only that file.
"""
import json
import os
import sys
from datetime import datetime

GUIDANCE = (
    "Compact summary: at most 800 words, terse bullets, no code dumps or file "
    "contents (cite path:line instead). KEEP: goal, Yuri's literal requests and "
    "rules, pending items, decisions+why, file paths touched, exact commands and "
    "their results, errors with their fix, measured numbers with units, subagent "
    "grades, current state, next step, blockers. DROP: tool output already "
    "summarized, test logs, exploratory dead ends, superseded attempts, memory "
    "dumps, skill text."
)


def textos(content):
    if isinstance(content, str):
        return [content]
    return [c.get("text", "") for c in content or [] if isinstance(c, dict) and c.get("type") == "text"]


def escrever_handoff(dados):
    cwd = dados.get("cwd") or os.getcwd()
    # do not write to home or anything under ~/.claude (they are not projects)
    norm = lambda x: os.path.normcase(os.path.abspath(os.path.expanduser(x)))
    aqui, home, cfg = norm(cwd), norm("~"), norm("~/.claude")
    if aqui == home or aqui == cfg or aqui.startswith(cfg + os.sep):
        return
    pedidos, arquivos, ultima = [], [], ""
    with open(dados["transcript_path"], encoding="utf-8") as f:
        for linha in f:
            try:
                ev = json.loads(linha)
            except ValueError:
                continue
            msg = ev.get("message") or {}
            if ev.get("type") == "user" and not ev.get("isMeta"):
                for t in textos(msg.get("content")):
                    if t.strip() and not t.lstrip().startswith(("<", "[Request interrupted", "This session is being continued")):
                        pedidos.append(t.strip()[:500])
            elif ev.get("type") == "assistant":
                for c in msg.get("content") or []:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") == "tool_use" and c.get("name") in ("Edit", "Write", "NotebookEdit"):
                        caminho = (c.get("input") or {}).get("file_path")
                        if caminho and caminho not in arquivos:
                            arquivos.append(caminho)
                    elif c.get("type") == "text" and c.get("text", "").strip():
                        ultima = c["text"].strip()
    corpo = [
        f"# HANDOFF ({datetime.now():%Y-%m-%d %H:%M})",
        "New session: read this file first and continue from the next step.",
        "",
        "## Work in progress (Yuri's latest requests)",
        *[f"- {p}" for p in pedidos[-5:]],
        "",
        "## Changed files",
        *[f"- {a}" for a in arquivos[-30:]],
        "",
        "## Decisions, dead ends and next step (Claude's last reply)",
        ultima[:3000],
        "",
    ]
    with open(os.path.join(cwd, "HANDOFF.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(corpo))


try:
    escrever_handoff(json.load(sys.stdin))
except Exception:
    pass  # handoff is an extra; never block compaction

print(GUIDANCE)  # PreCompact stdout becomes the compaction instruction (plain text, not JSON)
