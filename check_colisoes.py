#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Checa colisao de nomes TOP-LEVEL entre os arquivos src/ do app Write.

O build concatena tudo em um unico <script>, entao dois `const X` no mesmo
escopo global = SyntaxError "Identifier 'X' has already been declared".
Este script simula a concatenacao e reporta o que colide de verdade.
"""
import collections
import pathlib
import re
import sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def strip_code(s):
    """Devolve o codigo com strings e comentarios trocados por espacos (mesmo tamanho)."""
    out = list(s)
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c in "\"'`":
            q = c
            i += 1
            while i < n:
                if s[i] == "\\":
                    out[i] = " "
                    if i + 1 < n:
                        out[i + 1] = " "
                    i += 2
                    continue
                if s[i] == q:
                    break
                if s[i] != "\n":
                    out[i] = " "
                i += 1
        elif c == "/" and i + 1 < n and s[i + 1] == "/":
            while i < n and s[i] != "\n":
                out[i] = " "
                i += 1
        elif c == "/" and i + 1 < n and s[i + 1] == "*":
            j = s.find("*/", i + 2)
            j = n if j < 0 else j + 2
            for k in range(i, j):
                if s[k] != "\n":
                    out[k] = " "
            i = j
            continue
        i += 1
    return "".join(out)


DECL = re.compile(r"\b(?:const|let|var|function|class)\s+([A-Za-z_$][\w$]*)")
KEYWORDS = {
    "if", "for", "while", "switch", "catch", "return", "typeof", "new", "delete",
    "function", "class", "const", "let", "var", "do", "else", "case", "await",
}


def top_level_decls(code):
    """Nomes declarados no escopo global (profundidade de chaves = 0)."""
    found = []
    depth = 0
    i, n = 0, len(code)
    while i < n:
        c = code[i]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif depth == 0:
            m = DECL.match(code, i)
            if m:
                found.append(m.group(1))
                i = m.end()
                continue
        i += 1
    return found


def main():
    names = collections.defaultdict(list)
    for f in sorted(SRC.glob("*.js")):
        code = strip_code(f.read_text(encoding="utf-8"))
        for nm in top_level_decls(code):
            names[nm].append(f.name)

    dups = {k: v for k, v in names.items() if len(v) > 1}
    if not dups:
        print("OK: nenhuma colisao de nome top-level entre os arquivos .js")
        return 0
    print("COLISOES TOP-LEVEL (viram SyntaxError no bundle):")
    for k, v in sorted(dups.items()):
        print("  %-24s %s" % (k, sorted(set(v))))
    return 1


if __name__ == "__main__":
    sys.exit(main())
