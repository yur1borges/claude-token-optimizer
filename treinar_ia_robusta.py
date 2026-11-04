import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
import joblib

print("Iniciando re-treinamento rigoroso da IA de detecção de modos Raman (Anti-Overfitting)...")

features = []
labels = []

peaks_dir = "resultado_peaks"
for f in os.listdir(peaks_dir):
    if f.endswith(".csv"):
        df_p = pd.read_csv(os.path.join(peaks_dir, f))
        if not df_p.empty:
            for _, row in df_p.iterrows():
                # Coletar parâmetros robustos do pico
                altura = float(row['altura'])
                fwhm = float(row['fwhm'])
                prominence = float(row['prominence'])
                snr = float(row['snr'])
                if np.isinf(snr) or np.isnan(snr):
                    snr = 0.0
                area = float(row['area'])

                features.append([altura, fwhm, prominence, snr, area])

                # Critério rigoroso para evitar falso positivo (ruído):
                # Um modo Raman real precisa ter proeminência expressiva E SNR considerável E FWHM fisiologicamente coerente (> 1.0 e < 150.0)
                is_real_mode = 1 if (prominence > 12.0 and snr > 5.0 and 1.0 < fwhm < 150.0 and altura > 10.0) else 0
                labels.append(is_real_mode)

X = np.array(features)
y = np.array(labels)
X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

print(f"Total de candidatos a picos analisados: {len(X)}")
print(f"Modos Raman reais rotulados como válidos: {np.sum(y)} ({np.mean(y)*100:.2f}%)")

if len(np.unique(y)) > 1:
    # Configurar Random Forest rigoroso com restrição de profundidade para evitar overfitting
    clf = RandomForestClassifier(
        n_estimators=150,
        max_depth=6,              # Limita a profundidade para não decorar ruídos
        min_samples_split=10,     # Exige mais amostras para criar nós
        min_samples_leaf=5,       # Evita folhas muito puras baseadas em outliers
        class_weight='balanced',  # Trata desbalanceamento entre ruído e pico real
        random_state=42
    )

    # Validação cruzada estratificada em 5 folds para métricas reais e honestas
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    f1_scores = cross_val_score(clf, X, y, cv=cv, scoring='f1')
    prec_scores = cross_val_score(clf, X, y, cv=cv, scoring='precision')
    rec_scores = cross_val_score(clf, X, y, cv=cv, scoring='recall')

    print("\n--- MÉTRICAS DE VALIDAÇÃO CRUZADA (5-Fold Rigoroso) ---")
    print(f"Precisão Média: {np.mean(prec_scores):.4f} (+/- {np.std(prec_scores):.4f})")
    print(f"Revocação Média: {np.mean(rec_scores):.4f} (+/- {np.std(rec_scores):.4f})")
    print(f"F1-Score Médio:  {np.mean(f1_scores):.4f} (+/- {np.std(f1_scores):.4f})")

    # Treinar no dataset completo com os parâmetros validados
    clf.fit(X, y)

    # Salvar modelo robusto
    joblib.dump(clf, "modelo_ia_raman_robusto.joblib")
    print("\nModelo robusto anti-ruído salvo com sucesso em 'modelo_ia_raman_robusto.joblib'.")
else:
    print("Erro: Apenas uma classe encontrada nos rótulos.")
