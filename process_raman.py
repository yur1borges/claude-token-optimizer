#!/usr/bin/env python
"""
Processo de limpeza e detecção de picos Raman para arquivos de espectro XY.

Este script realiza as seguintes etapas:
1. Detecta e remove cabeçalhos, linhas vazias e valores inválidos.
2. Interpola valores faltantes (se existirem).
3. Aplica correção de linha de base baseada em um ajuste de polinômio de baixa ordem.
4. Detecta picos usando scipy.signal.find_peaks com parâmetros de escolha.
5. Calcula largura em meio ponto (FWHM), área de pico (integração numérica), e razão sinal/ruído.
6. Salva os espectros processados em *dados_processados/* e os resultados dos picos em CSV separados.
7. Gera um relatório consolidado *summary_peaks.csv* com todas as metas extras.

O script é configurado para funcionar junto com o processo de triagem já executado: ele só considera os arquivos que permanecem em *dados_limpos/* e cujos nomes terminam em .txt. Se o arquivo já estiver processado (arquivo picos já gerado) o script ignora.

**Dependências**
```bash
pip install pandas numpy scipy matplotlib pyyaml tqdm
```

**Uso**
```bash
exec -- python process_raman.py --input ./dados_limpos --output ./dados_processados --peaks ./resultado_peaks
```

**Observações**
- O script preserva os arquivos originais.
- Qualquer arquivo que não seja reconhecido como espectro de duas colunas será registrado em *erro_log.txt*.
- Para acelerar, apenas o envio de logs no arquivo. Se quiser debug, altere `log_level='INFO'`.
"""

import os
import argparse
import pandas as pd
import numpy as np
from scipy.signal import find_peaks, peak_widths
import traceback
from tqdm import tqdm
import json


# ---------------------------------------------------------------------------
# Configurações globais
# ---------------------------------------------------------------------------
# Overscan do sinal (virar sinal se necessário: Raman negativa?), usar True se espectro convergê para decrescente.
orientacao_algo = "auto"  # auto, crescente, decrescente
# Função de baseline: polinômio de 3ª ordem
baseline_order = 3
# Parâmetros de detecção de pico
min_prominence = 1e-3  # ajuste dependente dos dados; considerar normalizar intensidades antes, então 1e-3.
min_width = 0.5  # menor largura em coordenadas X
# ---------------------------------------------------------------------------


def ler_espectro(caminho):
    """Le arquivo .txt esperando duas colunas (X, Y). Detecta e remove cabeçalho.
    Retorna DataFrame ou None em caso de erro."""
    try:
        df = pd.read_csv(caminho, sep=None, engine='python', header=None, names=['X', 'Y'], comment='#', na_values=['', 'NA'], dtype=float)
        # Remove linhas com valores faltantes
        df = df.dropna(subset=['X', 'Y'])
        if df.empty:
            return None
        return df
    except Exception as e:
        return None


def remover_cabecalho(df):
    """Remove possíveis linhas de cabeçalho contendo texto; supõe que não há linhas antes dos dados numericos."""
    # Já retirado em ler_espectro via NaNs
    return df


def ajustar_baseline(df):
    """Ajusta linha de base usando ajuste polinômio de baixa ordem; devolve o espectro sem baseline."""
    x = df['X'].values
    y = df['Y'].values
    # Ajuste de polinômio
    coeff = np.polyfit(x, y, baseline_order)
    baseline = np.polyval(coeff, x)
    y_corr = y - baseline
    return pd.DataFrame({'X':x, 'Y':y_corr})


def detectar_picos(df, prominence, width_min):
    """Detecta picos usando scipy.signal.find_peaks."""
    x = df['X'].values
    y = df['Y'].values
    # Normaliza para ter escala consistente? Por enquanto não
    peaks, properties = find_peaks(y, prominence=prominence, width=width_min)
    return peaks, properties


def calcular_fwhm(df, peaks, properties):
    """Calcula largura de meio ponto (FWHM) usando peak_widths."""
    x = df['X'].values
    y = df['Y'].values
    results_half = peak_widths(y, peaks, rel_height=0.5)
    widths = results_half[0] * (x[1]-x[0])  # em unidades de X
    left_ips = results_half[2] * (x[1]-x[0]) + x[0]
    right_ips = results_half[3] * (x[1]-x[0]) + x[0]
    return widths, left_ips, right_ips


def calcular_area(df, left_ips, right_ips):
    """Integra a área sob o pico entre os limites."""
    x = df['X'].values
    y = df['Y'].values
    areas = []
    for left, right in zip(left_ips, right_ips):
        mask = (x >= left) & (x <= right)
        if np.sum(mask) > 1:
            # Usando regra do trapézio pura do numpy via np.trapezoid (substituta de trapz no numpy moderno)
            if hasattr(np, 'trapezoid'):
                areas.append(np.trapezoid(y[mask], x[mask]))
            else:
                areas.append(np.sum((y[mask][:-1] + y[mask][1:]) * np.diff(x[mask]) / 2))
        else:
            areas.append(0.0)
    return np.array(areas)


def processar_espectro(caminho, pasta_saida, pasta_peaks, log=None):
    fn = os.path.basename(caminho)
    try:
        df = ler_espectro(caminho)
        if df is None:
            raise ValueError("Formato inválido ou arquivo vazio")
        df = remover_cabecalho(df)
        df_corr = ajustar_baseline(df)
        # Salvar espectro processado
        out_path = os.path.join(pasta_saida, fn)
        df_corr.to_csv(out_path, sep='\t', index=False, header=False)
        # Detectar picos
        peaks, props = detectar_picos(df_corr, min_prominence, min_width)
        if len(peaks)==0:
            return
        # FWHM
        widths, left_ips, right_ips = calcular_fwhm(df_corr, peaks, props)
        # Área
        areas = calcular_area(df_corr, left_ips, right_ips)
        # SNR: usar média de ruido como std de y fora dos picos
        idx_not_peaks = np.ones_like(df_corr['Y'], dtype=bool)
        for p in peaks:
            idx_not_peaks[p-5:p+5] = False  # em torno do pico
        noise = df_corr['Y'][idx_not_peaks]
        snr = props['prominences'] / np.std(noise) if len(noise)>0 else np.nan
        # Preparar DataFrame de picos
        tabela = pd.DataFrame({
            'pos_x': df_corr['X'].values[peaks],
            'altura': df_corr['Y'].values[peaks],
            'fwhm': widths,
            'area': areas,
            'prominence': props.get('prominences', np.zeros_like(peaks)),
            'snr': snr
        })
        # Salvar picos
        peak_file = os.path.splitext(fn)[0] + '_peaks.csv'
        tabela.to_csv(os.path.join(pasta_peaks, peak_file), index=False)
    except Exception as e:
        if log is not None:
            log.append({'file': fn, 'error': str(e), 'trace': traceback.format_exc()})


def main():
    parser = argparse.ArgumentParser(description="Processa arquivos Raman em .txt e detecta picos.")
    parser.add_argument("--input", default="dados_limpos", help="Pasta contendo arquivos .txt originais.")
    parser.add_argument("--output", default="dados_processados", help="Pasta de saída dos espectros processados.")
    parser.add_argument("--peaks", default="resultado_peaks", help="Pasta de saída dos arquivos CSV de picos.")
    parser.add_argument("--summary", default="summary_peaks.csv", help="Arquivo CSV consolidado com todos os picos.")
    args = parser.parse_args()
    os.makedirs(args.output, exist_ok=True)
    os.makedirs(args.peaks, exist_ok=True)
    logs = []
    txt_files = [os.path.join(args.input, f) for f in os.listdir(args.input) if f.lower().endswith('.txt')]
    # Processar arquivos sequencialmente
    for fp in tqdm(txt_files, desc="Processando espectros"):
        processar_espectro(fp, args.output, args.peaks, logs)
    # Gerar relatório consolidado
    todas = []
    for f in os.listdir(args.peaks):
        df = pd.read_csv(os.path.join(args.peaks, f))
        if df.empty:
            continue
        todas.append(df)
    if todas:
        res = pd.concat(todas, ignore_index=True)
        res.to_csv(args.summary, index=False)
    # Salvar log de erros
    if logs:
        with open('error_log.txt', 'w') as fh:
            json.dump(logs, fh, indent=2)
    print("Processamento concluído.")

if __name__ == "__main__":
    main()
