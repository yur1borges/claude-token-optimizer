import os
import numpy as np
import pandas as pd
import joblib
from scipy.signal import find_peaks, peak_widths

print("=== TESTANDO A IA ROBUSTA COM OS DADOS DE L-ARGININA REAIS ===")

model_path = "modelo_ia_raman_robusto.joblib"
clf = joblib.load(model_path)

# Vamos procurar arquivos txt dentro de originais_preservados que tenham arginine/la no caminho
target_dir = "originais_preservados"
encontrados = 0

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.txt') and ('arginine' in file.lower() or 'la_' in file.lower() or 'la-' in file.lower()):
            fp = os.path.join(root, file)
            encontrados += 1
            print(f"\nTestando espectro: {file}")
            try:
                df = pd.read_csv(fp, sep=None, engine='python', header=None, names=['X', 'Y'], comment='#')
                df = df.dropna()
                x = df['X'].values
                y = df['Y'].values

                peaks, props = find_peaks(y, prominence=2.0, width=0.5)
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
                print(f"  Total de candidatos: {len(preds)} | Modos Raman REAIS validados pela IA: {reais}")
                for i, p_idx in enumerate(peaks):
                    if preds[i] == 1:
                        print(f"    ⭐ Pico em X={x[p_idx]:.2f} cm⁻¹ (Intensidade: {y[p_idx]:.1f}, Confiança: {probs[i]*100:.1f}%)")
            except Exception as e:
                print(f"  Erro: {e}")

print(f"\nTotal de arquivos testados: {encontrados}")
