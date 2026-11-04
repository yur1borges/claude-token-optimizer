#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Monta a pasta de PDFs de teste da T4 (citacoes no Write) - versao 2.

Busca por TIPO no OpenAlex (artigo, capitulo de livro, livro, tese/dissertacao,
preprint, proceedings), so com PDF de acesso aberto. Baixa o PDF de verdade,
confere que o DOI responde no CrossRef e grava um indice TSV (gabarito).

Uso:  python montar_pdfs_teste2.py
"""
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent
DST = BASE / "pdfs_teste"
INDEX = DST / "indice.tsv"
UA = "omniroute-t4/1.0 (mailto:omniroute@local)"
MAIL = "omniroute@local"

# (tipo_openalex, tipo_bibtex, rotulo, quantos)
ALVO = [
    ("article", "article", "artigo de revista", 5),
    ("book-chapter", "incollection", "capitulo de livro", 2),
    ("book", "book", "livro", 1),
    ("dissertation", "phdthesis", "tese/dissertacao", 1),
    ("preprint", "misc", "preprint", 1),
    ("proceedings-article", "inproceedings", "proceedings", 1),
]

KEYWORDS = [
    "discrete element method granular flow bulk solids handling",
    "abrasive wear particle contact mechanics",
    "particle size distribution mineral processing industrial",
    "DEM simulation chute conveyor wear liner",
    "granular material rheology silo segregation flow",
    "bulk solids handling chute design wear",
]

TEMA = "DEM granular flow wear tribology bulk solids material engineering"


def get(url, timeout=45, binary=False, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            return data if binary else json.loads(data.decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            last = e
            if e.code in (404, 403, 400):
                return None
        except Exception as e:
            last = e
        time.sleep(1.2 * (i + 1))
    print("    falha de rede: %s" % last)
    return None


def openalex(tipo, search=None, per_page=50, extra_filter=""):
    """Works open access de um tipo, ordenados por citacao (trabalhos com PDF real)."""
    filtros = "is_oa:true,has_fulltext:true,type:%s" % tipo
    if extra_filter:
        filtros += "," + extra_filter
    url = ("https://api.openalex.org/works?filter=%s&per-page=%d&mailto=%s"
           % (filtros, per_page, MAIL))
    if search:
        url += "&search=" + urllib.parse.quote(search)
    d = get(url)
    if not d:
        return []
    return d.get("results", [])


def norm(works):
    out = []
    for w in works:
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower().strip()
        if not doi:
            continue
        locs = w.get("locations") or []
        pdfs = [l.get("pdf_url") for l in locs if l.get("pdf_url")]
        best = w.get("best_oa_location") or {}
        if best.get("pdf_url") and best["pdf_url"] not in pdfs:
            pdfs.insert(0, best["pdf_url"])
        if not pdfs:
            continue
        out.append({
            "doi": doi,
            "title": (w.get("title") or "").strip(),
            "year": w.get("publication_year"),
            "type": w.get("type"),
            "pdfs": pdfs,
            "landing": best.get("landing_page_url") or ("https://doi.org/" + doi),
        })
    return out


def crossref(doi):
    d = get("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=30)
    if not d:
        return None
    return d.get("message") or None


def unpaywall_pdfs(doi):
    up = get("https://api.unpaywall.org/v2/%s?email=%s" % (urllib.parse.quote(doi), MAIL), timeout=30)
    if not up:
        return []
    return [l["url_for_pdf"] for l in (up.get("oa_locations") or []) if l.get("url_for_pdf")]


def cr_type(cr):
    t = (cr.get("type") or "").lower()
    if "proceedings" in t:
        return "inproceedings"
    if "book" in t and "chapter" in t:
        return "incollection"
    if "book" in t or "monograph" in t or "edited" in t:
        return "book"
    if "dissertation" in t or "thesis" in t:
        return "phdthesis"
    if "journal" in t or "article" in t:
        return "article"
    if "posted-content" in t or "preprint" in t:
        return "misc"
    return "misc"


def cr_year(cr):
    for k in ("published-print", "published-online", "issued", "created"):
        p = (cr.get(k) or {}).get("date-parts") or []
        if p and p[0] and p[0][0]:
            return int(p[0][0])
    return None


def cr_authors(cr):
    out = []
    for a in cr.get("author") or []:
        fam, giv = (a.get("family") or "").strip(), (a.get("given") or "").strip()
        if fam or giv:
            out.append((fam + ", " + giv).strip(", "))
    return out


def doi_filename(doi):
    return doi.replace("/", "_").replace(".", "_") + ".pdf"


def is_pdf(data):
    return bool(data) and data[:5] == b"%PDF-"


def baixar(doi, urls):
    """Tenta baixar o PDF em varias URLs. Devolve bytes ou None."""
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except Exception:
            time.sleep(0.6)
            continue
        if is_pdf(data) and len(data) > 15000:
            return data
        time.sleep(0.6)
    return None


def main():
    DST.mkdir(parents=True, exist_ok=True)
    print("pasta:", DST)

    # junta candidatos por tipo
    pool = {}
    for otipo, btipo, rotulo, qtd in ALVO:
        works = openalex(otipo, per_page=60)
        if len(works) < 20 and otipo in ("article", "proceedings-article", "book-chapter"):
            works += openalex(otipo, search=TEMA, per_page=60)
        cands = norm(works)
        # prioriza os mais citados (OpenAlex ja devolve por citacao)
        pool[otipo] = cands
        print("  %-20s candidatos: %d (pedi %d)" % (rotulo, len(cands), qtd))
        time.sleep(0.4)

    # artigos: mistura o tema com qualquer artigo open access de boa citacao
    if len(pool.get("article", [])) < 6:
        extra = norm(openalex("article", per_page=80))
        pool["article"] = extra + pool.get("article", [])
        print("  artigos ampliados para %d" % len(pool["article"]))

    linhas = []
    usados = set()
    for otipo, btipo, rotulo, qtd in ALVO:
        pegos = 0
        for c in pool.get(otipo, []):
            if pegos >= qtd or len(linhas) >= 10:
                break
            doi = c["doi"]
            if doi in usados:
                continue
            cr = crossref(doi)
            if not cr:
                print("    CrossRef nao conhece %s -> descartado" % doi)
                continue
            tipo_real = cr_type(cr)
            # preprint: CrossRef devolve posted-content -> misc; mantemos misc
            if tipo_real == "misc" and btipo != "misc":
                continue
            urls = list(c["pdfs"])
            up = unpaywall_pdfs(doi)
            urls += [u for u in up if u not in urls]
            data = baixar(doi, urls)
            if not data:
                print("    sem PDF real (%s) %s -> descartado" % (rotulo, doi))
                continue
            fname = doi_filename(doi)
            (DST / fname).write_bytes(data)
            usados.add(doi)
            titulo = (cr.get("title") or [""])[0]
            if tipo_real == "misc":
                titulo = titulo or c["title"]
            linhas.append([
                doi, fname, titulo.replace("\t", " "), str(cr_year(cr) or c["year"] or ""),
                btipo, rotulo,
                (cr.get("container-title") or [""])[0].replace("\t", " "),
                (cr.get("volume") or "").strip(), (cr.get("issue") or "").strip(),
                (cr.get("page") or "").strip(),
                "; ".join(cr_authors(cr)).replace("\t", " "),
                (cr.get("publisher") or "").replace("\t", " "),
            ])
            pegos += 1
            print("    ok %-40s %-12s %6d KB  %s" % (doi, btipo, len(data) // 1024, titulo[:40]))
            time.sleep(0.4)
        if pegos < qtd:
            print("  AVISO: %s -> %d de %d" % (rotulo, pegos, qtd))

    if not linhas:
        print("NENHUM PDF baixado. Verifique a rede.", file=sys.stderr)
        return 1

    cab = ["doi", "arquivo", "titulo", "ano", "tipo", "rotulo", "container", "volume",
           "issue", "pages", "autores", "publisher"]
    with INDEX.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(cab) + "\n")
        for l in linhas:
            f.write("\t".join(l) + "\n")
    print("\n%d PDFs -> %s" % (len(linhas), INDEX))
    return 0


if __name__ == "__main__":
    sys.exit(main())
