# -*- coding: utf-8 -*-
"""Sonda: qual query do CrossRef acha a tese com titulo de glifos embaralhados."""
import io
import json
import re
import urllib.parse
import urllib.request

UA = "omniroute-t4/1.0 (mailto:omniroute@local)"
ALVO = "10.5821/dissertation-2117-95384"
out = io.open("probe_tese.txt", "w", encoding="utf-8")


def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    return json.loads(urllib.request.urlopen(r, timeout=45).read().decode("utf-8"))


def cr(q, rows=8):
    u = ("https://api.crossref.org/works?rows=%d&query.bibliographic=%s"
         % (rows, urllib.parse.quote(q)))
    return get(u)["message"]["items"]


def cr_titulo(q, rows=8):
    u = ("https://api.crossref.org/works?rows=%d&query.title=%s"
         % (rows, urllib.parse.quote(q)))
    return get(u)["message"]["items"]


def cr_autor(q, rows=8):
    u = ("https://api.crossref.org/works?rows=%d&query.author=%s"
         % (rows, urllib.parse.quote(q)))
    return get(u)["message"]["items"]


def collapse(s):
    return re.sub(r"(.)\1+", r"\1", s)


GARBLED = "Particle finitee elemennt methoods for mmodellingg granular mmaterial flows"
AUTOR_PDF = "César Emmilio Dávvalos Chargoy"

casos = [
    ("raw", lambda: cr(GARBLED)),
    ("collapse", lambda: cr(collapse(GARBLED))),
    ("autor+raw", lambda: cr(AUTOR_PDF + " " + GARBLED)),
    ("autor+collapse", lambda: cr(collapse(AUTOR_PDF + " " + GARBLED))),
    ("so-autor", lambda: cr(collapse(AUTOR_PDF))),
    ("query.title raw", lambda: cr_titulo(GARBLED)),
    ("query.title collapse", lambda: cr_titulo(collapse(GARBLED))),
    ("query.author", lambda: cr_autor(collapse(AUTOR_PDF))),
]

for nome, fn in casos:
    out.write("=== %s\n" % nome)
    try:
        itens = fn()
        pos = None
        for i, it in enumerate(itens):
            d = it.get("DOI")
            if pos is None and d == ALVO:
                pos = i
            out.write("   %2d %-40s | %s\n" % (i, d, (it.get("title") or [""])[0][:60]))
        out.write("   --> ALVO na posicao %s\n" % pos)
    except Exception as e:
        out.write("   erro %s\n" % e)
out.close()
