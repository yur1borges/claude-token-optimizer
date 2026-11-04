#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Monta a pasta de PDFs de teste da T4 (citacoes no Write).

Busca artigos open access com DOI real em fontes legais (OpenAlex -> Unpaywall),
com tipos mistos: artigo de revista, capitulo de livro, tese/dissertacao, livro,
preprint e proceedings. Baixa o PDF de verdade, confere que o DOI responde no
CrossRef e grava um indice TSV que serve de gabarito para o teste.

Uso:  python montar_pdfs_teste.py
"""
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent
DST = BASE / "pdfs_teste"
INDEX = DST / "indice.tsv"
UA = "omniroute-t4/1.0 (mailto:omniroute@local)"
CUTOFF = 2024  # ano minimo para nao pegar obras classicicas sem PDF livre

TEMA = "bulk DEM granular flow wear tribology material"
KEYWORDS = [
    "discrete element method granular flow bulk solids handling",
    "abrasive wear particle contact mechanics",
    "particle size distribution industrial mineral processing",
    "DEM simulation chute conveyor wear",
    "granular material rheology silo segregation",
]


def get(url, timeout=45, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else json.loads(data.decode("utf-8", "replace"))


def openalex_candidates(per_page=40):
    """Busca trabalhos open access, priorizando o tema DEM/materiais."""
    vistos = {}
    for kw in KEYWORDS:
        url = (
            "https://api.openalex.org/works?filter=is_oa:true,has_fulltext:true,"
            "from_publication_date:%d-01-01&per-page=%d&mailto=omniroute@local&search=%s"
            % (CUTOFF, per_page, urllib.parse.quote(kw))
        )
        try:
            d = get(url)
        except Exception as e:
            print("  openalex falhou em %r: %s" % (kw, e))
            continue
        for w in d.get("results", []):
            doi = (w.get("doi") or "").replace("https://doi.org/", "").lower().strip()
            loc = w.get("best_oa_location") or {}
            pdf = loc.get("pdf_url")
            if not doi or not pdf:
                continue
            vistos[doi] = {
                "doi": doi,
                "title": (w.get("title") or "").strip(),
                "year": w.get("publication_year"),
                "type": w.get("type"),
                "pdf": pdf,
                "landing": loc.get("landing_page_url") or ("https://doi.org/" + doi),
                "host": (loc.get("source") or {}).get("display_name") or "",
            }
        time.sleep(0.4)
    return list(vistos.values())


def crossref(doi):
    """Metadados do CrossRef: confere que o DOI existe e devolve o registro."""
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    try:
        d = get(url, timeout=30)
    except urllib.error.HTTPError as e:
        return None if e.code == 404 else {"_err": str(e)}
    except Exception:
        return None
    return d.get("message") or None


def unpaywall(doi):
    url = "https://api.unpaywall.org/v2/%s?email=omniroute@local" % urllib.parse.quote(doi)
    try:
        return get(url, timeout=30)
    except Exception:
        return None


def cr_type(cr):
    """Tipo do CrossRef -> tipo BibTeX."""
    t = (cr.get("type") or "").lower()
    if "proceedings" in t:
        return "inproceedings"
    if "book" in t and "chapter" in t:
        return "incollection"
    if "book" in t or "monograph" in t or "edited" in t:
        return "book"
    if "dissertation" in t or "thesis" in t:
        return "phdthesis"
    if "journal" in t or "article" in t or "proceedings-article" in t:
        return "article"
    return "misc"


def cr_title(cr):
    t = cr.get("title") or []
    return (t[0] if t else "").strip()


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
        if not fam and not giv:
            continue
        out.append((fam + ", " + giv).strip(", "))
    return out


def cr_container(cr, crtype):
    if crtype == "article":
        return (cr.get("container-title") or [""])[0].strip()
    if crtype in ("inproceedings", "incollection"):
        return (cr.get("container-title") or [""])[0].strip()
    return ""


def cr_volume_issue_pages(cr):
    v = (cr.get("volume") or "").strip()
    n = (cr.get("issue") or "").strip()
    p = (cr.get("page") or "").strip()
    return v, n, p


def cr_publisher_place(cr):
    pub = (cr.get("publisher") or "").strip()
    place = ""
    for loc in cr.get("content-domain") and [] or []:
        pass
    # CrossRef raramente traz o lugar; tenta pelo campo editor/isbn nao ajuda. Mantem vazio.
    return pub, place


def slug(s, n=70):
    s = re.sub(r"[^\w\-.]+", "_", (s or "").strip(), flags=re.UNICODE)
    return s[:n].strip("_") or "item"


def doi_filename(doi, ext="pdf"):
    return doi.replace("/", "_").replace(".", "_") + "." + ext


def looks_like_pdf(data):
    return data[:5] == b"%PDF-"


def main():
    DST.mkdir(parents=True, exist_ok=True)
    print("pasta:", DST)

    cands = openalex_candidates()
    print("candidatos open access:", len(cands))

    # separa por tipo para cobrir a variedade pedida
    buckets = {"article": [], "incollection": [], "book": [],
               "phdthesis": [], "inproceedings": [], "preprint": []}
    for c in cands:
        buckets.setdefault(c["type"] if c["type"] in buckets else "article", []).append(c)

    escolhidos = []
    # 1) artigos (o grosso)
    escolhidos += [(c, "article") for c in buckets["article"][:5]]
    # 2) preprint
    escolhidos += [(c, "preprint") for c in buckets["preprint"][:1]]
    # 3) livros/capitulos/tese/proceedings vem de outra busca (OpenAlex rare e' assim)
    for c in buckets["incollection"][:1]:
        escolhidos.append((c, "incollection"))
    for c in buckets["book"][:1]:
        escolhidos.append((c, "book"))
    for c in buckets["phdthesis"][:1]:
        escolhidos.append((c, "phdthesis"))
    for c in buckets["inproceedings"][:1]:
        escolhidos.append((c, "inproceedings"))

    linhas = []
    usados = set()
    for cand, tipo_hint in escolhidos:
        if len(linhas) >= 10:
            break
        doi = cand["doi"]
        if doi in usados:
            continue
        cr = crossref(doi)
        if not cr or cr.get("_err"):
            print("  CrossRef nao conhece %s -> descartado" % doi)
            continue
        tipo = cr_type(cr)
        if tipo == "misc":
            print("  tipo nao mapeado (%s) para %s -> descartado" % (cr.get("type"), doi))
            continue
        # PDF: tenta o do OpenAlex; se falhar, tenta o do Unpaywall
        url = cand["pdf"]
        data = None
        for attempt in range(3):
            try:
                data = get(url, timeout=60, binary=True)
                if looks_like_pdf(data):
                    break
                data = None
            except Exception:
                data = None
            up = unpaywall(doi)
            alt = None
            if up:
                for loc in (up.get("oa_locations") or []):
                    if loc.get("url_for_pdf"):
                        alt = loc["url_for_pdf"]
                        break
            url = alt or url
            time.sleep(1.0)
        if not data or not looks_like_pdf(data):
            print("  sem PDF real para %s -> descartado" % doi)
            continue
        if len(data) < 20000:
            print("  PDF curto demais (%d bytes) %s -> descartado" % (len(data), doi))
            continue

        fname = doi_filename(doi)
        (DST / fname).write_bytes(data)
        usados.add(doi)
        v, n, p = cr_volume_issue_pages(cr)
        linhas.append("\t".join([
            doi, fname, cr_title(cr).replace("\t", " "), str(cr_year(cr) or ""),
            tipo, (cr.get("container-title") or [""])[0].replace("\t", " "),
            v, n, p, "; ".join(cr_authors(cr)).replace("\t", " "),
            (cr.get("publisher") or "").replace("\t", " "),
        ]))
        print("  ok %-42s %-14s %6d KB  %s" % (doi, tipo, len(data) // 1024, cr_title(cr)[:44]))
        time.sleep(0.5)

    if not linhas:
        print("NENHUM PDF Downloading. Verifique a rede.", file=sys.stderr)
        return 1

    cab = ["doi", "arquivo", "titulo", "ano", "tipo", "container", "volume", "issue", "pages", "autores", "publisher"]
    INDEX.write_text("\t".join(cab) + "\n" + "\n".join(linhas) + "\n", encoding="utf-8")
    print("\n%d PDFs baixados. Indice: %s" % (len(linhas), INDEX))
    tipos = {}
    for l in linhas:
        tipos[l.split("\t")[4]] = tipos.get(l.split("\t")[4], 0) + 1
    print("tipos:", tipos)
    return 0


if __name__ == "__main__":
    import urllib.parse  # noqa: F401  (usado acima)
    sys.exit(main())
