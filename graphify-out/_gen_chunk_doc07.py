import json, os

ROOT = r"C:\Users\yuri\OneDrive\Desktop\omniroute"
DP = os.path.join(ROOT, "dados_processados")

data_files = [
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\AutoCalibration - Laser 514nm_Edge - Grating 1800 (450-850nm) - Coeff 0.00201934  PASS_24-10-2022.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\C1_grat1800_633nm_4ac_t50s_300-1800cm-1_filter100__20x.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\C2_633NM_P100__L50X_t100S_AC3_100-200CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\C2_grat1800_633nm_4ac_t50s_300-1800cm-1_filter50__20x.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\C4_grat1800_633nm_4ac_t50s_300-1800cm-1_filter50__20x.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\CA228_633NM_t40s_ac4_FILTRO 100__X20_400_1800CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\CA328_633NM_t40s_ac4_FILTRO 100__X20_400_1800CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\Cu_633NM_t10s_6ac_FILTRO 10__X20_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\Dourado.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\LFMO 1000 MELHOR_.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\T1_633NM_t10s_6ac_FILTRO 10__X20_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\T1_633NM_t10s_6ac_FILTRO 3,2__X20_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\TA,Ni 0,5__633NM_t5s_6ac_FILTRO 10__X100_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\TA,Ni 1__633NM_t1s_4ac_FILTRO 10__X100_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\TA-NTC 0,1__633NM_t10s_6ac_FILTRO 10__X100_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\TA-NTC 0,5__0,5Ni_633NM_t10s_6ac_FILTRO 10__X100_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\TA-PURO_633NM_t10s_6ac_FILTRO 10__X100_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\TA-PURO_633NM_t10s_6ac_FILTRO 10__X20_100_3000CM-1.txt",
    r"C:\Users\yuri\OneDrive\Desktop\omniroute\dados_processados\verde.txt",
]

F_FONTES = os.path.join(ROOT, "fontes-chute-4-lacunas.md")
F_INBOX = os.path.join(ROOT, "inbox_vlrm.md")
F_ERR = os.path.join(ROOT, "error_log.txt")
F_FR = os.path.join(ROOT, "fr.html")
F_IZ = os.path.join(ROOT, "iz.html")
F_ICMJE = os.path.join(ROOT, "icmje_auth.html")

def norm(s):
    return "".join(c.lower() if c.isalnum() else "_" for c in s)

def stem_for(path, repo_root):
    rel = os.path.relpath(path, repo_root)
    if rel.lower().endswith(".txt"):
        rel = rel[:-4]
    segs = [norm(s) for s in rel.split(os.sep)]
    return "_".join(segs)

nodes = []
edges = []
hyperedges = []

def node(nid, label, ftype, path, loc=None, rationale=None):
    n = {
        "id": nid,
        "label": label,
        "file_type": ftype,
        "source_file": path,
        "source_location": loc,
        "source_url": None,
        "captured_at": None,
        "author": None,
        "contributor": None,
    }
    if rationale:
        n["rationale"] = rationale
    nodes.append(n)
    return nid

def edge(s, t, rel, conf, score, path, loc=None, weight=1.0):
    edges.append({
        "source": s, "target": t, "relation": rel, "confidence": conf,
        "confidence_score": score, "source_file": path, "source_location": loc,
        "weight": weight,
    })

# ---------- Raman spectra data files ----------
data_ids = []
for p in data_files:
    sid = stem_for(p, ROOT) + "_espectro_raman"
    label = os.path.basename(p)[:-4]
    node(sid, "Espectro Raman processado: " + label, "document", p)
    data_ids.append(sid)

# ---------- error_log.txt ----------
e_proc = node("error_log_process_raman_py", "process_raman.py / processar_espectro (linha 152)", "code", F_ERR, "L152")
e_key = node("error_log_peak_heights_keyerror", "KeyError 'peak_heights' em props (leitura de pico do espectro)", "code", F_ERR, "L1-L161")
e_falha = node("error_log_falha_processamento_raman", "Falha em lote do processamento Raman", "rationale", F_ERR, None,
               rationale="Todos os 19 espectros listados falham com KeyError 'peak_heights'; o processador assume que o parser expoe a chave 'peak_heights' em props, o que nao ocorre para esses arquivos.")
e_set = node("error_log_dados_processados", "Lote de espectros Raman em dados_processados", "concept", F_ERR)

edge(e_proc, e_key, "references", "EXTRACTED", 1.0, F_ERR, "L5")
edge(e_falha, e_key, "references", "EXTRACTED", 1.0, F_ERR)
edge(e_falha, e_proc, "references", "EXTRACTED", 1.0, F_ERR)
edge(e_falha, e_set, "references", "EXTRACTED", 1.0, F_ERR)
for sid, p in zip(data_ids, data_files):
    edge(e_key, sid, "references", "EXTRACTED", 1.0, F_ERR)
    edge(sid, e_set, "shares_data_with", "INFERRED", 0.95, F_ERR)

# ---------- fontes-chute-4-lacunas.md ----------
FS = stem_for(F_FONTES, ROOT)
f_doc = node(FS + "_fontes_primarias_lacunas", "Fontes primarias para as 4 lacunas do chute (G-11, G-09, G-06, G-04)", "document", F_FONTES, "L1-L206")
f_chute = node(FS + "_chute_anatomia_doc", "docs/CHUTE_ANATOMIA.md (secao 6, lacunas)", "document", F_FONTES, "L4")
f_semfonte = node(FS + "_regra_sem_fonte", "Regra SEM FONTE: nao reportar numero sem PDF/URL", "rationale", F_FONTES, "L6",
                  rationale="Regra do JP: se o valor for o mesmo do lado do codigo, reportar 'SEM FONTE' e manter o item bloqueado, porque numero errado entra no DEM e contamina a calibracao.")
f_grizzly = node(FS + "_grelha_g11", "Lacuna G-11: grelha (grizzly) e retencao de oversize", "concept", F_FONTES, "L12-L16")
f_liner = node(FS + "_liner_g09", "Lacuna G-09: espessura do liner e vida util", "concept", F_FONTES, "L18-L22")
f_cort = node(FS + "_cortina_de_po_g06", "Lacuna G-06: cortina de po (dust curtain) do transfer point", "concept", F_FONTES, "L24-L100")
f_rasp = node(FS + "_raspador_primario_g04", "Lacuna G-04: raspador primario de correia", "concept", F_FONTES, "L103-L177")
f_pecas = node(FS + "_tribodem_pecas_padrao", "TriboDEM pecas_padrao.py (codigo comparado)", "code", F_FONTES, "L80, L470, L485-488")
f_mfound = node(FS + "_martin_foundations", "Martin Engineering, Foundations (4a ed., 2009) - Cap. 18 Passive Dust Control", "document", F_FONTES, "L182")
f_tds = node(FS + "_martin_tds_l3298", "Martin Engineering, TDS L3298-06 Martin Dust Curtain Double", "document", F_FONTES, "L184")
f_asgco = node(FS + "_asgco_skirt_dust_control", "ASGCO, Skirt & Dust Control Sealing Systems (brochure ENG 2023)", "document", F_FONTES, "L186")
f_arg = node(FS + "_argonics_dust_curtain", "Argonics Inc., Dust Curtain (brochure rev. 2/26)", "document", F_FONTES, "L187")
f_epa = node(FS + "_epa_region5_fugitive_dust", "U.S. EPA Region 5, Fugitive Dust Control Measures and Best Practices (2022)", "document", F_FONTES, "L188")
f_v83 = node(FS + "_brelko_v8_3", "Brelko, Primary Head Pulley Belt Cleaners - Catalogue & Service Manual V8.3 (10/2022)", "document", F_FONTES, "L111")
f_v85 = node(FS + "_brelko_v8_5", "Brelko, Marketing File ENG-V8.5 A4 (10/2026) - Primary Cleaners", "document", F_FONTES, "L135")
f_l3651 = node(FS + "_martin_l3651", "Martin Engineering, Conveyor Belt Cleaners (brochure L3651, rev. 2017)", "document", F_FONTES, "L121")
f_l4047 = node(FS + "_martin_l4047", "Martin Engineering, Martin Replacement Blades for Belt Cleaners (L4047, 2023)", "document", F_FONTES, "L132")
f_lc = node(FS + "_martin_learning_center", "Martin Engineering, Foundations Learning Center (paginas vivas sobre raspadores e angulo de ataque)", "document", F_FONTES, "L109-L110")
f_press = node(FS + "_pressao_trabalho_cortina", "Pressao de trabalho da cortina de po (Pa/mmca)", "concept", F_FONTES, "L58-L69",
                rationale="Campo em branco real em fonte primaria publica: nenhuma das 6 fontes lidas publica pressao de trabalho da cortina. Nao reportar numero; a grandeza correta a modelar e velocidade de ar e vazao de entrada.")
f_velar = node(FS + "_velocidade_ar_settling_zone", "Velocidade de ar alvo na zona de carga (<= 1,0 m/s) e vazao de entrada (<= 0,50 m3/s)", "concept", F_FONTES, "L64-L65")
f_barreira = node(FS + "_barreira_settling_zone", "Cortina como barreira/baffle e 'settling zone' (vedacao e retencao, nao captura ativa)", "concept", F_FONTES, "L71-L84")
f_ang = node(FS + "_angulo_ataque_rake", "Angulo de ataque da lamina do raspador primario (30-45 graus, rake positivo)", "concept", F_FONTES, "L109-L113")
f_plam = node(FS + "_pressao_lamina_correia", "Pressao da lamina contra a correia (13,8-14 kPa / 2 psi)", "concept", F_FONTES, "L117-L125")
f_mlam = node(FS + "_material_lamina_pu_shore", "Material da lamina: poliuretano 83-91 Shore A (elastomero, nao metal)", "concept", F_FONTES, "L127-L137")
f_desg = node(FS + "_desgaste_capa_correia", "Efeito do raspador no desgaste da capa da correia (desgaste inevitavel e aceito)", "concept", F_FONTES, "L139-L151")
f_calor = node(FS + "_marca_de_calor_capa", "Marca de calor na capa da correia atribuida ao raspador", "concept", F_FONTES, "L153",
                rationale="Nao existe texto em fonte primaria lida que atribua marca de calor na capa da correia ao raspador; fusao/calor documentados sao do blade de poliuretana e da correia seca por atrito do material transportado. Nao reportar.")
f_desc = node(FS + "_descarte_alucinacao_busca", "Descarte de resultados de busca sem documento real (alucinacao de engine)", "rationale", F_FONTES, "L192-L205",
               rationale="Documentos inexistentes retornados pelo motor de busca com numeros e citacoes inventadas foram descartados; sem documento lido nao entra numero no DEM.")

edge(f_doc, f_chute, "references", "EXTRACTED", 1.0, F_FONTES, "L4")
edge(f_doc, f_grizzly, "references", "EXTRACTED", 1.0, F_FONTES, "L12")
edge(f_doc, f_liner, "references", "EXTRACTED", 1.0, F_FONTES, "L18")
edge(f_doc, f_semfonte, "implements", "EXTRACTED", 1.0, F_FONTES, "L6")
edge(f_doc, f_desc, "references", "EXTRACTED", 1.0, F_FONTES, "L192")
edge(f_doc, f_cort, "references", "EXTRACTED", 1.0, F_FONTES, "L24")
edge(f_doc, f_rasp, "references", "EXTRACTED", 1.0, F_FONTES, "L103")
edge(f_semfonte, f_press, "rationale_for", "EXTRACTED", 1.0, F_FONTES, "L58-L69")
edge(f_semfonte, f_calor, "rationale_for", "EXTRACTED", 1.0, F_FONTES, "L153")
edge(f_desc, f_semfonte, "conceptually_related_to", "INFERRED", 0.95, F_FONTES, "L205")
edge(f_cort, f_mfound, "cites", "EXTRACTED", 1.0, F_FONTES, "L30-L50")
edge(f_cort, f_tds, "cites", "EXTRACTED", 1.0, F_FONTES, "L31")
edge(f_cort, f_asgco, "cites", "EXTRACTED", 1.0, F_FONTES, "L32")
edge(f_cort, f_arg, "cites", "EXTRACTED", 1.0, F_FONTES, "L33")
edge(f_cort, f_epa, "cites", "EXTRACTED", 1.0, F_FONTES, "L82")
edge(f_barreira, f_mfound, "cites", "EXTRACTED", 1.0, F_FONTES, "L77")
edge(f_barreira, f_tds, "cites", "EXTRACTED", 1.0, F_FONTES, "L78")
edge(f_velar, f_mfound, "cites", "EXTRACTED", 1.0, F_FONTES, "L64")
edge(f_press, f_velar, "conceptually_related_to", "INFERRED", 0.95, F_FONTES, "L69")
edge(f_press, f_cort, "conceptually_related_to", "EXTRACTED", 1.0, F_FONTES, "L99")
edge(f_ang, f_lc, "cites", "EXTRACTED", 1.0, F_FONTES, "L109")
edge(f_ang, f_v83, "cites", "EXTRACTED", 1.0, F_FONTES, "L111-L113")
edge(f_plam, f_l3651, "cites", "EXTRACTED", 1.0, F_FONTES, "L121")
edge(f_plam, f_lc, "cites", "EXTRACTED", 1.0, F_FONTES, "L122")
edge(f_plam, f_v83, "cites", "EXTRACTED", 1.0, F_FONTES, "L123")
edge(f_mlam, f_l4047, "cites", "EXTRACTED", 1.0, F_FONTES, "L132-L133")
edge(f_mlam, f_lc, "cites", "EXTRACTED", 1.0, F_FONTES, "L131")
edge(f_mlam, f_v83, "cites", "EXTRACTED", 1.0, F_FONTES, "L134")
edge(f_rasp, f_v85, "cites", "EXTRACTED", 1.0, F_FONTES, "L135")
edge(f_desg, f_lc, "cites", "EXTRACTED", 1.0, F_FONTES, "L145-L149")
edge(f_desg, f_l3651, "cites", "EXTRACTED", 1.0, F_FONTES, "L148")
edge(f_desg, f_l4047, "cites", "EXTRACTED", 1.0, F_FONTES, "L150")
edge(f_desg, f_v83, "cites", "EXTRACTED", 1.0, F_FONTES, "L151")
edge(f_cort, f_pecas, "references", "EXTRACTED", 1.0, F_FONTES, "L88-L99")
edge(f_rasp, f_pecas, "references", "EXTRACTED", 1.0, F_FONTES, "L170-L176")
edge(f_ang, f_pecas, "references", "EXTRACTED", 1.0, F_FONTES, "L172")
edge(f_mlam, f_pecas, "references", "EXTRACTED", 1.0, F_FONTES, "L174")
edge(f_calor, f_l4047, "references", "EXTRACTED", 1.0, F_FONTES, "L153")

# ---------- inbox_vlrm.md ----------
IS = stem_for(F_INBOX, ROOT)
i_fluxo = node(IS + "_fluxo_qe_flow", "Fluxo de execucao: qe-flow-77 -> vlrm -> controlador -> outbox_vlrm.md", "concept", F_INBOX, "L3-L12")
i_t1 = node(IS + "_t1_entrevista_pre_tarefa", "Tarefa 1: skill de entrevista pre-tarefa (>=5 perguntas)", "concept", F_INBOX, "L16-L23")
i_t2 = node(IS + "_t2_agente_propostas_melhoria", "Tarefa 2: agente de propostas de melhoria dos 6 softwares", "concept", F_INBOX, "L25-L32")
i_t3 = node(IS + "_t3_agente_lattes", "Tarefa 3: agente do Lattes (3 agentes via Playwright)", "concept", F_INBOX, "L34-L41")
i_t4 = node(IS + "_t4_citacoes_automaticas_write", "Tarefa 4: citacoes automaticas no Write a partir de pasta de PDFs", "concept", F_INBOX, "L43-L49")
i_t5 = node(IS + "_t5_pipeline_referencias", "Tarefa 5: pipeline buscador de referencias (4 agentes)", "concept", F_INBOX, "L51-L58")
i_outbox = node(IS + "_outbox_vlrm", "outbox_vlrm.md (canal de saida da sessao vlrm)", "document", F_INBOX, "L11")
i_skill = node(IS + "_skill_entrevista_pre_tarefa", "Skill entrevista-pre-tarefa em ~/.claude/skills", "code", F_INBOX, "L20")
i_prop = node(IS + "_propostas_md", "omniroute/propostas.md (lista viva de melhorias)", "document", F_INBOX, "L30")
i_verif = node(IS + "_verificador_lattes", "Verificador de divergencias campo a campo no Lattes", "concept", F_INBOX, "L40")
i_diff = node(IS + "_lattes_diff_md", "lattes_diff.md (relatorio antes x depois)", "document", F_INBOX, "L39")
i_pw = node(IS + "_playwright_agentes_lattes", "Playwright: leitor / atualizador / verificador do Lattes", "concept", F_INBOX, "L38")
i_abnt = node(IS + "_abnt_nbr_6023", "Estilo de citacao ABNT NBR 6023", "concept", F_INBOX, "L47")
i_apa = node(IS + "_apa_7", "Estilo de citacao APA 7", "concept", F_INBOX, "L47")
i_vanc = node(IS + "_vancouver", "Estilo de citacao numerico (Vancouver)", "concept", F_INBOX, "L47")
i_crossref = node(IS + "_crossref", "CrossRef (metadados e DOI)", "concept", F_INBOX, "L47")
i_openalex = node(IS + "_openalex", "OpenAlex (metadados bibliograficos)", "concept", F_INBOX, "L47")
i_qualis = node(IS + "_qualis_a1_a2", "Avaliacao Qualis A1/A2 e area de avaliacao", "concept", F_INBOX, "L56-L58")
i_scholar = node(IS + "_google_scholar", "Fontes legais de busca: CAPES, Google Scholar, Scopus, Web of Science, BDTD, OpenAlex, Unpaywall", "concept", F_INBOX, "L55")

for t in (i_t1, i_t2, i_t3, i_t4, i_t5):
    edge(i_fluxo, t, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_fluxo, i_outbox, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t1, i_skill, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t2, i_prop, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t3, i_verif, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t3, i_diff, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t3, i_pw, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t4, i_abnt, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t4, i_apa, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t4, i_vanc, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t4, i_crossref, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t4, i_openalex, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t5, i_qualis, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t5, i_scholar, "references", "EXTRACTED", 1.0, F_INBOX)
edge(i_t5, i_t4, "conceptually_related_to", "INFERRED", 0.85, F_INBOX)

# ---------- fr.html ----------
FR = stem_for(F_FR, ROOT)
fr_g = node(FR + "_frontiers_author_guidelines", "Frontiers - Author guidelines (escrita e formatacao)", "document", F_FR, "L1")
fr_ai = node(FR + "_frontiers_ai_authorship_policy", "Frontiers: IA generativa nao pode ser autor; uso deve ser declarado e conferido", "rationale", F_FR, None,
              rationale="Autores nao podem listar IA ou tecnologia assistida por IA como autor/coautor; conteudo gerado por IA deve ser conferido quanto a exatidao factual, citacoes, figuras e plagio, e o uso deve ser reconhecido nos agradecimentos e metodos, listando nome, versao, modelo e fonte da ferramenta.")
fr_ref = node(FR + "_frontiers_reference_policy", "Frontiers: referencias devem ser de pesquisa revisada por pares; evitar fontes nao academicas", "rationale", F_FR, None,
               rationale="Submissoes devem ser fundamentadas em pesquisa academica revisada por pares atualizada e refletida na lista de referencias; citacao de blog, conteudo de site, fontes anonimas e sites comerciais deve ser evitada ou minimizada.")

edge(fr_g, fr_ai, "references", "EXTRACTED", 1.0, F_FR)
edge(fr_g, fr_ref, "references", "EXTRACTED", 1.0, F_FR)

# ---------- icmje_auth.html ----------
IC = stem_for(F_ICMJE, ROOT)
ic_rec = node(IC + "_icmje_recommendations", "ICMJE Recommendations (papel de autores e colaboradores)", "document", F_ICMJE, "L1")
ic_auth = node(IC + "_authorship_criteria", "ICMJE: quem e autor e quem nao e (criterios de autoria e responsabilidade)", "concept", F_ICMJE)
ic_contrib = node(IC + "_contributorship_policy", "ICMJE: politica de contributorship (creditos de contribuicao por pessoa)", "rationale", F_ICMJE, None,
                   rationale="Como autoria nao comunica quais contribuicoes qualificam um individuo, alguns diarios pedem e publicam informacao das contribuicoes de cada pessoa; editores sao fortemente encorajados a criar e implementar politica de contributorship.")
ic_ai = node(IC + "_ai_use_in_publishing", "ICMJE: uso de inteligencia artificial em publicacao (autoria, revisao, atribuicao)", "rationale", F_ICMJE, None,
              rationale="Autores nao devem listar IA e tecnologias assistidas por IA como autor ou coautor, nem citar IA como autor; humanos devem garantir atribuicao completa de todo material citado, incluindo citacoes completas.")

edge(ic_rec, ic_auth, "references", "EXTRACTED", 1.0, F_ICMJE)
edge(ic_rec, ic_contrib, "references", "EXTRACTED", 1.0, F_ICMJE)
edge(ic_rec, ic_ai, "references", "EXTRACTED", 1.0, F_ICMJE)

# ---------- iz.html ----------
IZ = stem_for(F_IZ, ROOT)
iz_art = node(IZ + "_efremov_tikalov_2022_disk_on_disk", "Efremov & Tikalov (2022): avaliacao experimental de wear de par de atrito 'disco sobre disco'", "paper", F_IZ)
iz_doi = node(IZ + "_doi_10_17586_0021_3454", "DOI 10.17586/0021-3454-2022-65-4-280-286", "document", F_IZ)
iz_bor = node(IZ + "_metodo_block_on_ring", "Metodo block-on-ring (base dos algoritmos de wear linear e volumetrico)", "concept", F_IZ)
iz_smc = node(IZ + "_maquina_smc_2", "Maquina de atrito SMC-2 (ensaio disco sobre disco)", "concept", F_IZ)
iz_ref = node(IZ + "_referencia_safonov", "Referencia bibliografica na lista de literatura (Safonov B. P. et al.)", "document", F_IZ)

edge(iz_art, iz_doi, "references", "EXTRACTED", 1.0, F_IZ)
edge(iz_art, iz_bor, "implements", "EXTRACTED", 1.0, F_IZ)
edge(iz_art, iz_smc, "references", "EXTRACTED", 1.0, F_IZ)
edge(iz_art, iz_ref, "cites", "EXTRACTED", 1.0, F_IZ)

# ---------- cross-file semantic ----------
edge(fr_ai, ic_ai, "semantically_similar_to", "INFERRED", 0.85, F_FR)
edge(fr_ref, i_t4, "semantically_similar_to", "INFERRED", 0.75, F_FR)
edge(ic_contrib, i_t3, "conceptually_related_to", "INFERRED", 0.70, F_ICMJE)
edge(f_semfonte, i_verif, "semantically_similar_to", "INFERRED", 0.70, F_FONTES)
edge(i_t4, iz_art, "conceptually_related_to", "INFERRED", 0.75, F_INBOX)

# ---------- hyperedges ----------
hyperedges.append({
    "id": "raman_spectrum_batch_peak_heights_failure",
    "label": "Falha em lote do processamento Raman (KeyError peak_heights)",
    "nodes": [e_proc, e_key, e_falha, data_ids[16], data_ids[17], data_ids[7]],
    "relation": "participate_in",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": F_ERR,
})
hyperedges.append({
    "id": "dust_curtain_primary_sources_g06",
    "label": "Fontes primarias da cortina de po (G-06)",
    "nodes": [f_cort, f_mfound, f_tds, f_asgco, f_arg, f_epa],
    "relation": "form",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": F_FONTES,
})
hyperedges.append({
    "id": "vlrm_task_pipeline_t1_t5",
    "label": "Cadeia de 5 tarefas do inbox VLRM (qe-flow-77 -> vlrm -> controlador)",
    "nodes": [i_fluxo, i_t1, i_t2, i_t3, i_t4, i_t5],
    "relation": "form",
    "confidence": "EXTRACTED",
    "confidence_score": 1.0,
    "source_file": F_INBOX,
})

out = {
    "nodes": nodes,
    "edges": edges,
    "hyperedges": hyperedges,
    "input_tokens": 0,
    "output_tokens": 0,
}

dest = os.path.join(ROOT, "graphify-out", ".graphify_chunk_doc07.json")
with open(dest, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=True, indent=1)
print("nodes", len(nodes), "edges", len(edges), "hyper", len(hyperedges))
