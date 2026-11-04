import os
import numpy as np
import pandas as pd
import joblib

print("=== TESTANDO A IA ROBUSTA COM OS ESPECTROS DE L-ARGININA (SEM EMOJI) ===")

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
            x_vals = []
            y_vals = []
            with open(fp, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('#'):
                        parts = line.lstrip('#').strip().split()
                        if len(parts) == 2:
                            try:
                                x_vals.append(float(parts[0]))
                                y_vals.append(float(parts[1]))
                            except ValueError:
                                pass
                    elif line:
                        parts = line.split()
                        if len(parts) >= 2:
                            try:
                                x_vals.append(float(parts[0]))
                                y_vals.append(float(parts[1]))
                            except ValueError:
                                pass

            x = np.array(x_vals)
            y = np.array(y_vals)

            if len(x) == 0:
                print("  Nenhum dado numérico extraído.")
                continue

            candidatos = []
            for i in range(len(x)):
                altura = y[i]
                fwhm = 5.0
                prom = altura * 0.8
                snr = 50.0
                area = altura * fwhm
                candidatos.append([altura, fwhm, prom, snr, area])

            X_test = np.nan_to_num(np.array(candidatos), nan=0.0, posinf=0.0, neginf=0.0)
            preds = clf.predict(X_test)
            probs = clf.predict_proba(X_test)[:, 1]

            reais = np.sum(preds == 1)
            print(f"  Modos teóricos analisados: {len(preds)} | Modos Raman REAIS validados pela IA robusta: {reais}")
            for i in range(len(x)):
                if preds[i] == 1:
                    print(f"    [PICO REAL] Modo DFT em X = {x[i]:.2f} cm-1 | Atividade = {y[i]:.2f} | Confiança = {probs[i]*100:.1f}%")
        except Exception as e:
            print(f"  Erro: {e}")
