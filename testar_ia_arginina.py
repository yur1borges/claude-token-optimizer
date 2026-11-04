import os
import numpy as np
import pandas as pd
import joblib
from scipy.signal import find_peaks, peak_widths

print("=== TESTANDO A IA ROBUSTA COM OS ESPECTROS DE L-ARGININA ===")

model_path = "modelo_ia_raman_robusto.joblib"
if not os.path.exists(model_path):
    print("Erro: Modelo robusto não encontrado.")
    exit(1)

clf = joblib.load(model_path)

arginine_dir = r"C:\Users\yuri\OneDrive\Desktop\fit l-arginine"
files = [os.path.join(arginine_dir, f) for f in os.listdir(arginine_dir) if f.endswith('.dat') or f.endswith('.txt')]

for fp in files:
    fn = os.path.basename(fp)
    print(f"\nAnalisando arquivo: {fn}")
    try:
        df = pd.read_csv(fp, sep=None, engine='python', header=None, names=['X', 'Y'], comment='#')
        df = df.dropna()
        x = df['X'].values
        y = df['Y'].values

        # Detecção de picos com find_peaks
        peaks, props = find_peaks(y, prominence=1.0, width=0.5)
        if len(peaks) == 0:
            print("  Nenhum pico candidato encontrado.")
            continue

        # Calcular features para a IA
        widths = peak_widths(y, peaks, rel_height=0.5)[0] * (x[1]-x[0])

        candidatos = []
        for i, p_idx in enumerate(peaks):
            altura = y[p_idx]
            fwhm = widths[i]
            prom = props['prominences'][i]

            # SNR estimado
            noise = np.std(y[max(0, p_idx-10):min(len(y), p_idx+10)])
            snr = prom / noise if noise > 0 else 0.0
            area = altura * fwhm * 1.064

            candidatos.append([altura, fwhm, prom, snr, area])

        X_test = np.array(candidatos)
        X_test = np.nan_to_num(X_test, nan=0.0, posinf=0.0, neginf=0.0)

        preds = clf.predict(X_test)
        probs = clf.predict_proba(X_test)[:, 1]

        real_modes = np.sum(preds == 1)
        print(f"  Total de candidatos testados pela IA: {len(preds)}")
        print(f"  Modos Raman REAIS validados pela IA robusta: {real_modes}")

        for i, p_idx in enumerate(peaks):
            if preds[i] == 1:
                print(f"    -> Pico real em X = {x[p_idx]:.2f} cm⁻¹ | Intensidade = {y[p_idx]:.2f} | Confiança IA = {probs[i]*100:.1f}%")

    except Exception as e:
        print(f"  Erro ao processar {fn}: {e}")
