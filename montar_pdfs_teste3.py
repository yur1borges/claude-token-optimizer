#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Monta a pasta de PDFs de teste da T4 - versao 3 (definitiva).

Regras do controlador:
  - 10 PDFs open access com DOI real, tipos mistos
  - nome do arquivo embute o DOI
  - indice TSV (doi/arquivo/titulo/ano/tipo) na mesma pasta = gabarito do teste
  - todo DOI precisa resolver no CrossRef (desconhecidos sao descartados com justificativa)
  - nao apagar nada existente

Correcoes da v3 sobre a v2:
  - o tipo gravado vem do CrossRef (tipo real), nao do bucket de busca
  - proceedings vem do CrossRef direto (OpenAlex nao indexa 'proceedings-article')
  - filtro de relevancia: titulo/resumo tem que ser do tema DEM/materiais

Uso:  python montar_pdfs_teste3.py
"""
import json
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

# tema: DEM / materiais / fluxo granular / desgaste
RELEV = [
    "discrete element", " dem ", "granular", "particle", "bulk solid", "wear",
    "tribolog", "abrasi", "chute", "conveyor", "belt convey", "silo", "hopper",
    "mineral processing", "ore", "mineral", "aggregate", "particle size distribution",
    "rheolog", "jamming", "shear cell", "compaction", "cement", "concrete",
    "material", "alloy", "steel", "ceramic", "polymer", "composite",
    "powder", "granulate", "pellet", "soil", "sediment", "flow",
]
# o que NAO serve: o artigo precisa ter ao menos um termo do tema
NEGATIVO = ["privacy", "covid", "vaccine", "cryptocurrency", "social media",
            "clinical trial", "patient", "cancer", "police", "election"]

TIPOS_ALVO = [
    # (rotulo, tipo_bibtex, tipos_crossref_aceitos, total_querido)
    ("artigo de revista", "article", {"article", "journal-article"}, 4),
    ("capitulo de livro", "incollection", {"book-chapter"}, 2),
    ("livro", "book", {"book", "monograph", "edited-book"}, 1),
    ("tese/dissertacao", "phdthesis", {"dissertation", "thesis"}, 1),
    ("proceedings", "inproceedings", {"proceedings-article", "proceedings"}, 1),
    ("preprint", "misc", {"posted-content"}, 1),
]

TEMA_Q = "discrete element method granular bulk solids wear material"
KEYWORDS = [
    "discrete element method granular flow bulk solids handling",
    "abrasive wear particle contact mechanics material",
    "particle size distribution mineral processing industrial",
    "DEM simulation chute conveyor wear liner steel",
    "granular material rheology silo segregation flow",
    "bulk solids handling chute flow design",
]


def get(url, timeout=45, binary=False, tries=3, mailto=False):
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
        time.sleep(1.0 * (i + 1))
    print("      ! falha de rede: %s" % last)
    return None


def oa_url(u, mailto=True):
    if mailto:
        u += ("&" if "?" in u else "?") + "mailto=" + MAIL
    return u


def openalex(tipo, per_page=60, search=None):
    u = oa_url("https://api.openalex.org/works?filter=is_oa:true,has_fulltext:true,type:%s&per-page=%d"
               % (tipo, per_page))
    if search:
        u += "&search=" + urllib.parse.quote(search)
    d = get(u)
    if not d:
        return []
    return d.get("results", [])


def crossref_works(tipo_cr, query, rows=40, extra=""):
    """Busca direta no CrossRef por tipo de obra."""
    f = "type:" + tipo_cr
    if extra:
        f += "," + extra
    u = ("https://api.crossref.org/works?filter=%s&rows=%d&select=DOI,title,type,"
         "container-title,author,issued,published-print,published-online,volume,issue,page,publisher"
         "&query.bibliographic=%s&mailto=%s" % (f, rows, urllib.parse.quote(query), MAIL))
    d = get(u)
    if not d:
        return []
    return d.get("message", {}).get("items", [])


def crossref_one(doi):
    d = get("https://api.crossref.org/works/" + urllib.parse.quote(doi), timeout=30)
    return (d or {}).get("message")


def unpaywall_pdfs(doi):
    up = get("https://api.unpaywall.org/v2/%s?email=%s" % (urllib.parse.quote(doi), MAIL), timeout=30)
    if not up:
        return []
    return [l["url_for_pdf"] for l in (up.get("oa_locations") or []) if l.get("url_for_pdf")]


def oa_pdf_from_openalex(work):
    locs = work.get("locations") or []
    urls = [l.get("pdf_url") for l in locs if l.get("pdf_url")]
    best = work.get("best_oa_location") or {}
    if best.get("pdf_url") and best["pdf_url"] not in urls:
        urls.insert(0, best["pdf_url"])
    return urls


def cr_type(cr):
    return ((cr.get("type") or "").lower() or "unknown")


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


def dois_de_openalex(tipo, per_page=60, search=None):
    out = []
    for w in openalex(tipo, per_page, search):
        doi = (w.get("doi") or "").replace("https://doi.org/", "").lower().strip()
        if not doi:
            continue
        out.append({"doi": doi, "title": w.get("title") or "", "pdfs": oa_pdf_from_openalex(w),
                    "abstract": (w.get("abstract_inverted_index") or {})})
    return out


def dois_de_crossref(tipo_cr, query, extra=""):
    out = []
    for it in crossref_works(tipo_cr, query, 40, extra):
        doi = (it.get("DOI") or "").lower().strip()
        if doi:
            out.append({"doi": doi, "title": (it.get("title") or [""])[0]})
    return out


def relevante(texto):
    t = (" " + (texto or "").lower() + " ")
    if any(n in t for n in NEGATIVO):
        return False
    return any(r in t for r in RELEV)


def baixar(urls):
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        except Exception:
            time.sleep(0.5)
            continue
        if data[:5] == b"%PDF-" and len(data) > 15000:
            return data
        time.sleep(0.5)
    return None


def doi_filename(doi):
    return doi.replace("/", "_").replace(".", "_") + ".pdf"


def main():
    DST.mkdir(parents=True, exist_ok=True)
    print("pasta:", DST)
    linhas = []
    usados = set()
    descartes = []

    for rotulo, btipo, tipos_cr, qtd in TIPOS_ALVO:
        pegos = 0
        # --- candidatos ---
        if btipo == "inproceedings":
            cands = dois_de_crossref("proceedings-article", TEMA_Q)
            for c in cands:
                c.setdefault("pdfs", [])
        elif btipo == "phdthesis":
            cands = dois_de_openalex("dissertation", 60, TEMA_Q)
            cands = [c for c in cands if not c["doi"].startswith("10.1111/j.1467")]
        elif btipo == "misc":
            # preprint: bioRxiv/medRxiv (10.1101), Research Square (10.21203), SSRN (10.2139)
            # arXiv (10.48550) nao registra no CrossRef -> descartado
            cands = dois_de_openalex("preprint", 50, TEMA_Q)
            cands = [c for c in cands
                     if c["doi"].startswith(("10.1101/", "10.21203/", "10.2139/", "10.48550/"))]
            cands = cands + dois_de_openalex("preprint", 120)
            cands = [c for c in cands
                     if c["doi"].startswith(("10.1101/", "10.21203/", "10.2139/"))]
        else:
            otipo = {"article": "article", "incollection": "book-chapter", "book": "book"}[btipo]
            cands = dois_de_openalex(otipo, 60, TEMA_Q)
            if len(cands) < 12:
                cands += dois_de_openalex(otipo, 80)
        print("  %-20s candidatos: %d (pedi %d)" % (rotulo, len(cands), qtd))

        for c in cands:
            if pegos >= qtd or len(linhas) >= 10:
                break
            doi = c["doi"]
            if doi in usados:
                continue
            cr = crossref_one(doi)
            if not cr:
                descartes.append((doi, rotulo, "CrossRef nao registra este DOI"))
                continue
            tcr = cr_type(cr)
            if tcr not in tipos_cr:
                descartes.append((doi, rotulo, "tipo CrossRef '%s' fora do esperado %s" % (tcr, sorted(tipos_cr))))
                continue
            titulo = (cr.get("title") or [""])[0]
            # preprint: exige so que nao seja claramente fora do escopo (o tema la e' ampla)
            if btipo == "misc":
                ok_tema = not any(n in (" " + titulo.lower() + " ") for n in NEGATIVO)
            else:
                ok_tema = relevante(titulo + " " + (cr.get("container-title") or [""])[0])
            if not ok_tema:
                descartes.append((doi, rotulo, "fora do tema DEM/materiais"))
                continue
            urls = list(c.get("pdfs") or [])
            up = unpaywall_pdfs(doi)
            urls += [u for u in up if u not in urls]
            data = baixar(urls)
            if not data:
                descartes.append((doi, rotulo, "sem PDF de acesso aberto baixavel"))
                continue
            fname = doi_filename(doi)
            (DST / fname).write_bytes(data)
            usados.add(doi)
            linhas.append([
                doi, fname, titulo.replace("\t", " "), str(cr_year(cr) or ""),
                btipo, rotulo,
                (cr.get("container-title") or [""])[0].replace("\t", " "),
                (cr.get("volume") or "").strip(), (cr.get("issue") or "").strip(),
                (cr.get("page") or "").strip(),
                "; ".join(cr_authors(cr)).replace("\t", " "),
                (cr.get("publisher") or "").replace("\t", " "),
            ])
            pegos += 1
            print("    ok %-40s %-13s %6d KB  %s" % (doi, btipo, len(data) // 1024, titulo[:40]))
            time.sleep(0.4)
        if pegos < qtd:
            print("  AVISO: %s -> %d de %d" % (rotulo, pegos, qtd))

    if not linhas:
        print("NENHUM PDF baixado.", file=sys.stderr)
        return 1

    cab = ["doi", "arquivo", "titulo", "ano", "tipo", "rotulo", "container", "volume",
           "issue", "pages", "autores", "publisher"]
    with INDEX.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(cab) + "\n")
        for l in linhas:
            f.write("\t".join(l) + "\n")
    print("\n%d PDFs -> %s" % (len(linhas), INDEX))
    print("\ndescartes (%d):" % len(descartes))
    for d, r, m in descartes:
        print("  %-42s %-18s %s" % (d, r, m))
    return 0


if __name__ == "__main__":
    sys.exit(main())
