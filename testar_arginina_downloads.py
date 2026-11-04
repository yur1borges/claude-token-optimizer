import os
import numpy as np
import pandas as pd
import joblib
from scipy.signal import find_peaks, peak_widths

print("=== TESTANDO A IA ROBUSTA COM ARQUIVOS DE L-ARGININA DOS DOWNLOADS ===")

model_path = "modelo_ia_raman_robusto.joblib"
clf = joblib.load(model_path)

downloads_dir = r"C:\Users\yuri\Downloads"
arquivos_teste = [
    "2l-argininehclh2o_raman_act.txt",
    "L-ARGININE_raman_act.txt",
    "l-argininehclh2o_raman_act.txt"
]

for nome in arquivos_teste:
    fp = os.path.join(downloads_dir, nome)
    if os.path.exists(fp):
        print(f"\n--- Analisando arquivo: {nome} ---")
        try:
            df = pd.read_csv(fp, sep=None, engine='python', header=None, names=['X', 'Y'], comment='#')
            df = df.dropna()
            x = df['X'].values
            y = df['Y'].values

            peaks, props = find_peaks(y, prominence=1.5, width=0.5)
            if len(peaks) == 0:
                print("  Nenhum pico detectado.")
                continue

            widths = peak_widths(y, peaks, rel_height=0.5)[0] * (x[1]-x[0])
            candidatos = []
            for i, p_idx in enumerate(peaks):
                altura = y[p_idx]
                fwhm = widths[i]
                prom = props['prominences'][i]
                noise = np.std(y[max(0, p_idx-10):min(len(y), p_idx+10)])
                snr = prom / noise if noise > 0 else 0.0
                area = altura * fwhm * 1.064
                candidatos.append([altura, fwhm, prom, snr, area])

            X_test = np.nan_to_num(np.array(candidatos), nan=0.0, posinf=0.0, neginf=0.0)
            preds = clf.predict(X_test)
            probs = clf.predict_proba(X_test)[:, 1]

            reais = np.sum(preds == 1)
            print(f"  Candidatos analisados: {len(preds)} | Modos Raman REAIS validados pela IA: {reais}")
            for i, p_idx in enumerate(peaks):
                if preds[i] == 1:
                    print(f"    ⭐ Pico real em X = {x[p_idx]:.2f} cm⁻¹ | Altura = {y[p_idx]:.1f} | Confiança = {probs[i]*100:.1f}%")
        except Exception as e:
            print(f"  Erro: {e}")
